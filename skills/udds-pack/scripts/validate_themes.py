#!/usr/bin/env python3
"""
UDDS Deep Theme Validator Gate
Nâng cấp từ validate_themes.py gốc:
1. Xác thực JSON Schema cho theme.json.
2. Xác thực tính nhất quán của Token (Kiểm tra xem token tham chiếu {navy-900} có tồn tại trong primitives.json không).
3. Xác thực tài nguyên vật lý (Kiểm tra xem thư mục có lỗi chính tả như '01_Guidelinnes' không, có bị thiếu Logos/Moodboards/Design template không).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

# Cấu hình lại stdout hỗ trợ in Unicode trên console Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def default_pack_root() -> Path:
    return Path(__file__).resolve().parents[1]


def folder_name_to_mood_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def has_visual_asset(path: Path) -> bool:
    return any(path.rglob(pattern) for pattern in ("*.png", "*.jpg", "*.jpeg", "*.webp"))


def deep_validate(asset_root: Path, schema_path: Path) -> int:
    print(f"[*] Bắt đầu kiểm duyệt chuyên sâu hệ thống theme (Deep Theme Validation Gate)...")
    themes_root = asset_root / "themes"
    tokens_root = asset_root / "tokens"
    print(f"[*] Theme root: {themes_root}")
    
    # 1. Load Schema
    if not schema_path.exists():
        print(f"[ERROR] Không tìm thấy tệp Schema tại: {schema_path}")
        return 2

    with schema_path.open("r", encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)

    # 2. Load Primitives
    primitives_path = tokens_root / "primitives.json"
    primitives = set()
    if primitives_path.exists():
        try:
            with open(primitives_path, "r", encoding="utf-8") as f:
                prim_data = json.load(f)
                primitives.update(prim_data.get("colors", {}).keys())
                primitives.update(prim_data.get("typography", {}).keys())
        except Exception as exc:
            print(f"[ERROR] Không đọc được primitives.json: {exc}")
            return 2
    else:
        print(f"[WARNING] Thiếu file primitives.json tại {primitives_path}!")

    theme_dirs = sorted(themes_root.iterdir())
    theme_dirs = [d for d in theme_dirs if d.is_dir() and d.name != "schema"]

    if not theme_dirs:
        print(f"[ERROR] Không tìm thấy thư mục theme nào dưới: {themes_root}")
        return 2

    failures = 0
    total_checked = 0

    for theme_dir in theme_dirs:
        theme_json = theme_dir / "theme.json"
        if not theme_json.exists():
            continue
            
        total_checked += 1
        theme_failures = 0
        rel_path = theme_json.relative_to(asset_root)
        print(f"\n🔹 Đang kiểm duyệt theme: '{theme_dir.name}' ({rel_path})")

        # Phân đoạn 1: Xác thực JSON Schema
        try:
            with theme_json.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            failures += 1
            print(f"  [FAIL] JSON không hợp lệ: {exc}")
            continue

        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
        if errors:
            theme_failures += 1
            print(f"  [FAIL] Schema JSON lỗi:")
            for err in errors[:5]:
                loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
                print(f"    - {loc}: {err.message}")
        else:
            print(f"  [PASS] Cấu trúc JSON Schema hoàn toàn hợp lệ.")

        # Phân đoạn 2: Xác thực tham chiếu Token nguyên thủy (Primitive references)
        token_errors = []
        base_colors = data.get("base", {}).get("colors", {})
        for color_key, color_val in base_colors.items():
            if isinstance(color_val, str) and color_val.startswith("{") and color_val.endswith("}"):
                prim_key = color_val[1:-1]
                if prim_key not in primitives:
                    token_errors.append(f"Màu '{color_key}' tham chiếu đến token ảo '{{{prim_key}}}' không có trong primitives.json")
                    
        base_typo = data.get("base", {}).get("typography", {})
        for typo_key, typo_val in base_typo.items():
            if isinstance(typo_val, str) and typo_val.startswith("{") and typo_val.endswith("}"):
                prim_key = typo_val[1:-1]
                if prim_key not in primitives:
                    token_errors.append(f"Typography '{typo_key}' tham chiếu đến token ảo '{{{prim_key}}}' không có trong primitives.json")

        if token_errors:
            theme_failures += 1
            print(f"  [FAIL] Lỗi tham chiếu Token nguyên thủy:")
            for err in token_errors:
                print(f"    - {err}")
        else:
            print(f"  [PASS] Tất cả các tham chiếu Token nguyên thủy hợp lệ.")

        # Phân đoạn 3: Xác thực cấu trúc thư mục và tài nguyên (Directory & Assets sanity check)
        asset_errors = []
        
        # Check lỗi chính tả thư mục phổ biến '01_Guidelinnes'
        typo_dir = theme_dir / "01_Guidelinnes"
        correct_dir = theme_dir / "01_Guidelines"
        
        if typo_dir.exists():
            asset_errors.append(
                f"Phát hiện sai chính tả thư mục guidelines: '{typo_dir.name}'. Nên đổi tên thành '{correct_dir.name}'."
            )
        elif not correct_dir.exists():
            asset_errors.append(f"Thiếu thư mục guidelines tiêu chuẩn: '{correct_dir.name}'.")
            
        # Check Logos
        logo_dir = theme_dir / "02_Logos"
        if not logo_dir.exists():
            asset_errors.append("Thiếu thư mục chứa logos: '02_Logos'.")
        elif not any(logo_dir.iterdir()):
            print(f"  [WARN] Thư mục '02_Logos' trống. Cần thêm logo để phục vụ watermark/branding.")

        # Check Moodboards
        mood_dir = theme_dir / "03_Moodboards"
        if not mood_dir.exists():
            asset_errors.append("Thiếu thư mục moodboard: '03_Moodboards'.")
        else:
            mood_data = data.get("moods", {})
            if not isinstance(mood_data, dict) or not mood_data:
                asset_errors.append("Theme chưa khai báo mood nào trong trường 'moods'.")
            else:
                mood_keys = set(mood_data.keys())
                normalized_mood_keys = {folder_name_to_mood_key(key): key for key in mood_keys}
                moodboard_dirs = sorted(d for d in mood_dir.iterdir() if d.is_dir())
                folder_by_key = {folder_name_to_mood_key(folder.name): folder for folder in moodboard_dirs}
                for mood_key in sorted(mood_keys):
                    normalized_mood_key = folder_name_to_mood_key(mood_key)
                    expected_dir = folder_by_key.get(normalized_mood_key)
                    if expected_dir is None:
                        print(
                            f"  [WARN] Mood '{mood_key}' chưa có thư mục ảnh tương ứng dưới '03_Moodboards/'."
                        )
                    elif not has_visual_asset(expected_dir):
                        asset_errors.append(
                            f"Mood '{mood_key}' không có ảnh tham chiếu trong: '03_Moodboards/{expected_dir.name}'."
                        )

                for folder in moodboard_dirs:
                    if folder.name.strip() != folder.name or "  " in folder.name:
                        asset_errors.append(
                            f"Tên thư mục moodboard có khoảng trắng bất thường: '03_Moodboards/{folder.name}'."
                        )
                    folder_key = folder_name_to_mood_key(folder.name)
                    if folder_key not in normalized_mood_keys:
                        print(
                            f"  [WARN] Thư mục moodboard '03_Moodboards/{folder.name}' chưa có key tương ứng trong theme.json: '{folder_key}'."
                        )
                    elif not has_visual_asset(folder):
                        asset_errors.append(
                            f"Thư mục moodboard '03_Moodboards/{folder.name}' không có ảnh tham chiếu."
                        )

        # Check DESIGN.template.md
        template_file = theme_dir / "DESIGN.template.md"
        if not template_file.exists():
            asset_errors.append("Thiếu file thiết kế gốc 'DESIGN.template.md' phục vụ sinh guidelines.")

        if asset_errors:
            theme_failures += 1
            print(f"  [FAIL] Lỗi cấu trúc tài nguyên và thư mục:")
            for err in asset_errors:
                print(f"    - {err}")
        else:
            print(f"  [PASS] Cấu trúc thư mục tài nguyên đúng quy chuẩn và đầy đủ.")

        if theme_failures > 0:
            failures += 1
            print(f"❌ Kết luận: Theme '{theme_dir.name}' KHÔNG đạt yêu cầu kiểm duyệt.")
        else:
            print(f"✅ Kết luận: Theme '{theme_dir.name}' vượt qua kiểm duyệt xuất sắc.")

    print("\n" + "="*70)
    if failures:
        print(f"[FAIL] Có {failures} theme không vượt qua được bài kiểm tra deep-validation.")
        return 1
    else:
        print(f"[PASS] Tất cả {total_checked} theme đã vượt qua deep-validation thành công!")
        return 0

def main() -> int:
    parser = argparse.ArgumentParser(description="UDDS Deep Theme Validation Gate CLI")
    parser.add_argument(
        "--pack",
        type=Path,
        default=None,
        help="Path to udds-pack. Defaults to the pack that contains this script.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=None,
        help="Path to theme.schema.json",
    )
    args = parser.parse_args()

    if args.pack is not None:
        pack_root = args.pack.resolve()
    else:
        pack_root = default_pack_root().resolve()

    asset_root = pack_root / "assets"
    schema_path = (args.schema or (asset_root / "schemas" / "theme.schema.json")).resolve()

    return deep_validate(asset_root, schema_path)

if __name__ == "__main__":
    sys.exit(main())
