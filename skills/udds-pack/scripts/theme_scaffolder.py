#!/usr/bin/env python3
"""
UDDS Theme Scaffolder Engine
Tự động hóa việc tạo một theme mới chuẩn cấu trúc Design System, 
sửa các lỗi chính tả phổ biến (như Guidelinnes) và chuẩn bị sẵn cấu hình theme.json.
"""

import argparse
import json
import sys
from pathlib import Path

# Cấu hình lại stdout hỗ trợ in Unicode trên console Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Template mặc định cho theme.json tuân thủ theme.schema.json
THEME_JSON_TEMPLATE = {
    "name": "{theme_name_display}",
    "scope": "Mô tả phạm vi ứng dụng và triết lý thị giác của theme {theme_name_display}",
    "base": {
        "typography": {
            "font-heading": "Montserrat",
            "font-body": "Open Sans",
            "font-mono": "Consolas"
        },
        "colors": {
            "background-primary": "#FFFFFF",
            "background-light": "#F8F9FA",
            "accent-primary": "#006CB5",
            "text-primary-on-dark": "#FFFFFF",
            "text-primary-on-light": "#0F172A",
            "text-secondary": "#64748B",
            "divider-line": "#E2E8F0"
        }
    },
    "moods": {
        "standard_mood": {
            "prompt_aesthetic": "Standard corporate visual identity for {theme_name_display}. High contrast, minimalist layouts, glassmorphism card surfaces, clean corporate lighting.",
            "icon_style": "Compass, target, roadmap, gear, shield, checklist.",
            "color_overrides": {}
        }
    }
}

# Template mặc định cho DESIGN.template.md để compile DESIGN.md
DESIGN_TEMPLATE_MD = """# 🔷 {{ theme.name }} Design System Guidelines

Chào mừng đến với cẩm nang thiết kế của thương hiệu **{{ theme.name }}**. Tài liệu này được biên dịch tự động dựa trên Single Source of Truth (SSOT).

## 🏛 Cấu hình Tokens Hệ thống

### 🎨 Typography (Phông chữ)
- **Heading Font (Tiêu đề):** {{ typography.font-heading }}
- **Body Font (Nội dung):** {{ typography.font-body }}

### 🎨 Bảng màu (Brand Colors)
- **Màu nền chủ đạo (Primary Background):** `{{ colors.background-primary }}`
- **Màu nhấn thương hiệu (Accent Primary):** `{{ colors.accent-primary }}`
- **Màu chữ trên nền tối (Text on Dark):** `{{ colors.text-primary-on-dark }}`
- **Màu chữ phụ (Secondary Text):** `{{ colors.text-secondary }}`
- **Đường phân cách (Divider):** `{{ colors.divider-line }}`

---
*Tài liệu này được sinh tự động. Vui lòng cập nhật các giá trị thiết kế trong file `theme.json` để đồng bộ lại.*
"""

# Hướng dẫn chi tiết cho designer trong thư mục theme
DESIGNER_README_MD = """# 🔷 {theme_name} Brand Asset Package

Chào mừng bạn đến với gói tài sản thương hiệu của **{theme_name}**. Thư mục này được tổ chức theo tiêu chuẩn của UDDS Modular Design System.

## 📂 Cấu trúc Thư mục chuẩn:

### `theme.json` (Nguồn Sự Thật Duy Nhất - SSOT)
- Chứa toàn bộ các biến số thiết kế (Design Tokens) như màu sắc, font chữ và các phong cách thị giác (moods).
- **Quy tắc cốt lõi:** Nếu bạn muốn đổi màu thương hiệu, **CHỈ ĐỔI TẠI ĐÂY**.

### `01_Guidelines/` (Cẩm nang & Nguyên tắc)
- **`DESIGN.md`**: "Hiến pháp thiết kế" sinh tự động từ `theme.json` bằng cách chạy script compiler. Tuyệt đối không sửa mã màu bằng tay trong file này.

### `02_Logos/` (Logo chuẩn)
- Đặt các file logo chuẩn SVG hoặc PNG (nền trong suốt) tại đây để dùng cho hệ thống slide/web.

### `03_Moodboards/` (Bảng cảm hứng)
- Chứa các slide mẫu hoặc các ảnh tham chiếu thị giác để định hướng phong cách thiết kế.

## 🛠 Hướng dẫn biên dịch Guidelines:
Sau khi thay đổi `theme.json`, hãy chạy script compiler để cập nhật lại `01_Guidelines/DESIGN.md`:
```bash
python .agents/skills/udds-pack/scripts/theme_compiler.py --pack <path-to-udds-pack> --theme {theme_folder}
```
"""

def default_asset_root() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"


def create_theme(name_arg: str, asset_root: Path) -> int:
    # Chuẩn hóa tên folder (slugify đơn giản)
    folder_name = name_arg.lower().replace(" ", "-").strip()
    theme_dir = asset_root / "themes" / folder_name
    
    if theme_dir.exists():
        print(f"[!] Error: Thư mục theme '{folder_name}' đã tồn tại ở: {theme_dir}")
        return 1
        
    print(f"[*] Đang khởi tạo theme mới: '{name_arg}' (Thư mục: assets/themes/{folder_name})")
    
    # 1. Tạo các thư mục chuẩn (Đúng chính tả!)
    directories = [
        theme_dir / "01_Guidelines",
        theme_dir / "02_Logos",
        theme_dir / "03_Moodboards",
        theme_dir / "exports"
    ]
    
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  [+] Đã tạo thư mục: {d.relative_to(asset_root)}")
        
    # 2. Khởi tạo theme.json
    theme_json = THEME_JSON_TEMPLATE.copy()
    theme_json["name"] = name_arg
    theme_json["scope"] = theme_json["scope"].format(theme_name_display=name_arg)
    
    # Format moods
    theme_json["moods"]["standard_mood"]["prompt_aesthetic"] = \
        theme_json["moods"]["standard_mood"]["prompt_aesthetic"].format(theme_name_display=name_arg)
        
    theme_json_path = theme_dir / "theme.json"
    with open(theme_json_path, "w", encoding="utf-8") as f:
        json.dump(theme_json, f, indent=2, ensure_ascii=False)
    print(f"  [+] Đã tạo cấu hình: {theme_json_path.relative_to(asset_root)}")
    
    # 3. Khởi tạo DESIGN.template.md
    template_path = theme_dir / "DESIGN.template.md"
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(DESIGN_TEMPLATE_MD)
    print(f"  [+] Đã tạo template guidelines: {template_path.relative_to(asset_root)}")
    
    # 4. Khởi tạo DESIGNER_README.md
    readme_path = theme_dir / "DESIGNER_README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(DESIGNER_README_MD.format(theme_name=name_arg, theme_folder=folder_name))
    print(f"  [+] Đã tạo tài liệu hướng dẫn: {readme_path.relative_to(asset_root)}")
    
    print(f"\n[OK] Khởi tạo thành công theme '{name_arg}'!")
    print(f"👉 Hãy vào chỉnh sửa file 'assets/themes/{folder_name}/theme.json' để cấu hình màu sắc và font chữ của thương hiệu.")
    print(f"👉 Tiếp theo chạy lệnh sau để tự sinh DESIGN.md:")
    print(f"   python .agents/skills/udds-pack/scripts/theme_compiler.py --pack <path-to-udds-pack> --theme {folder_name}")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Khởi tạo cấu trúc theme UDDS chuẩn mực.")
    parser.add_argument("name", help="Tên hiển thị của Theme (Ví dụ: 'Viettel Telecom', 'Vinamilk')")
    parser.add_argument(
        "--pack",
        type=Path,
        default=None,
        help="Path to udds-pack. Defaults to the pack that contains this script.",
    )
    args = parser.parse_args()
    asset_root = (args.pack.resolve() / "assets") if args.pack is not None else default_asset_root()
    sys.exit(create_theme(args.name, asset_root.resolve()))

if __name__ == "__main__":
    main()
