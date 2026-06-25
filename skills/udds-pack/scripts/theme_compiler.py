#!/usr/bin/env python3
"""
UDDS Theme Compiler & Exporter Engine
Biên dịch theme từ Single Source of Truth (SSOT) theme.json sang:
1. DESIGN.md (Tài liệu hướng dẫn thiết kế chuẩn)
2. CSS Variables (exports/theme.css - dành cho Web Frontend)
3. Tailwind Config Object (exports/tailwind-theme.json - dành cho Tailwind)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Cấu hình lại stdout hỗ trợ in Unicode trên console Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def default_asset_root() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"


class UDDSThemeCompiler:
    def __init__(self, theme_name, asset_root):
        self.theme_name = theme_name
        self.asset_root = asset_root
        self.theme_dir = asset_root / "themes" / theme_name
        self.theme_json_path = self.theme_dir / "theme.json"
        self.template_path = self.theme_dir / "DESIGN.template.md"
        
        # Paths đầu ra chuẩn
        self.output_guideline_dir = self.theme_dir / "01_Guidelines"
        self.output_design_md = self.output_guideline_dir / "DESIGN.md"
        self.exports_dir = self.theme_dir / "exports"
        
        self.primitives_path = asset_root / "tokens" / "primitives.json"

    def load_resolved_tokens(self):
        # 1. Load Primitives
        primitives = {}
        if self.primitives_path.exists():
            try:
                with open(self.primitives_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    primitives.update(data.get("colors", {}))
                    primitives.update(data.get("typography", {}))
            except Exception as e:
                print(f"[!] Warning: Không đọc được primitives.json: {e}")

        # 2. Load Theme JSON
        if not self.theme_json_path.exists():
            print(f"[!] Error: File theme.json không tồn tại ở: {self.theme_json_path}")
            return None
            
        try:
            with open(self.theme_json_path, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
        except Exception as e:
            print(f"[!] Error: File theme.json không đúng định dạng JSON: {e}")
            return None
            
        base_tokens = {}
        if "base" in theme_data:
            base_tokens.update(theme_data["base"].get("colors", {}))
            base_tokens.update(theme_data["base"].get("typography", {}))
            
        # 3. Phân giải token dạng {navy-900} thành mã màu/giá trị thực tế
        resolved_tokens = {}
        for key, value in base_tokens.items():
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                prim_key = value[1:-1]
                if prim_key in primitives:
                    resolved_tokens[key] = primitives[prim_key]
                else:
                    print(f"[!] Warning: Token nguyên thủy '{prim_key}' chưa được định nghĩa trong primitives.json")
                    resolved_tokens[key] = value
            else:
                resolved_tokens[key] = value
                
        return {
            "name": theme_data.get("name", self.theme_name),
            "tokens": resolved_tokens,
            "raw": theme_data
        }

    def compile(self) -> bool:
        theme_pack = self.load_resolved_tokens()
        if not theme_pack:
            return False
            
        theme_display_name = theme_pack["name"]
        tokens = theme_pack["tokens"]
        
        print(f"[*] Đang biên dịch theme: '{theme_display_name}'...")
        
        # 1. Biên dịch DESIGN.md
        if self.template_path.exists():
            with open(self.template_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Regex thay thế {{ category.key }} hoặc {{ theme.name }}
            def replacer(match):
                expr = match.group(1).strip()
                if expr == "theme.name":
                    return theme_display_name
                
                parts = expr.split(".")
                if len(parts) == 2:
                    category, key = parts
                    return str(tokens.get(key, match.group(0)))
                return match.group(0)

            compiled_content = re.sub(r"\{\{\s*(.*?)\s*\}\}", replacer, content)
            
            self.output_guideline_dir.mkdir(parents=True, exist_ok=True)
            with open(self.output_design_md, "w", encoding="utf-8") as f:
                f.write(compiled_content)
            print(f"  [+] Đã xuất tài liệu hướng dẫn: {self.output_design_md.relative_to(self.asset_root)}")
        else:
            print(f"  [!] Bỏ qua biên dịch DESIGN.md (Không thấy file DESIGN.template.md)")

        # 2. Xuất CSS Variables cho Web Team
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        css_path = self.exports_dir / "theme.css"
        with open(css_path, "w", encoding="utf-8") as f:
            f.write("/* ==========================================================================\n")
            f.write(f"   UDDS DESIGN SYSTEM CODES - AUTOMATICALLY COMPILED FOR THEME: {theme_display_name.upper()}\n")
            f.write("   ========================================================================== */\n\n")
            f.write(":root {\n")
            for key, val in tokens.items():
                css_key = key.replace("_", "-")
                if "font" in css_key and " " in str(val) and not str(val).startswith(("'", '"')):
                    val = f"'{val}'"
                f.write(f"  --{css_key}: {val};\n")
            f.write("}\n")
        print(f"  [+] Đã xuất CSS Variables: {css_path.relative_to(self.asset_root)}")

        # 3. Xuất Tailwind Config Extension JSON
        tailwind_path = self.exports_dir / "tailwind-theme.json"
        
        tailwind_config = {
            "theme": {
                "extend": {
                    "colors": {},
                    "fontFamily": {}
                }
            }
        }
        
        for key, val in tokens.items():
            if "font" in key:
                clean_key = key.replace("font-", "").replace("font_", "")
                tailwind_config["theme"]["extend"]["fontFamily"][clean_key] = [val] if isinstance(val, str) else val
            else:
                clean_key = key.replace("color-", "").replace("color_", "")
                tailwind_config["theme"]["extend"]["colors"][clean_key] = val
                
        with open(tailwind_path, "w", encoding="utf-8") as f:
            json.dump(tailwind_config, f, indent=2, ensure_ascii=False)
        print(f"  [+] Đã xuất Tailwind Config extension: {tailwind_path.relative_to(self.asset_root)}")

        print(f"[OK] Biên dịch theme '{self.theme_name}' hoàn tất thành công!\n")
        return True

def main():
    parser = argparse.ArgumentParser(description="UDDS Theme Compiler & Multi-format Exporter CLI")
    parser.add_argument("--theme", required=True, help="Tên thư mục theme cần compile (ví dụ: uncle-dao)")
    parser.add_argument(
        "--pack",
        type=Path,
        default=None,
        help="Path to udds-pack. Defaults to the pack that contains this script.",
    )
    args = parser.parse_args()
    
    asset_root = (args.pack.resolve() / "assets") if args.pack is not None else default_asset_root()
    compiler = UDDSThemeCompiler(args.theme, asset_root.resolve())
    if compiler.compile():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
