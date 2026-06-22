#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script này dùng để tự động cập nhật Google Sheet URL/ID mới cho toàn bộ các file checkpoint JSON
trong thư mục templates/checkpoints, đồng thời chuẩn hóa cấu trúc Resource Locator của n8n
sang dạng tĩnh (mode id & name) để tránh lỗi mất credentials và reset cấu hình cột (schema) khi import.

Cách sử dụng:
    python3 fix_checkpoint_with_new_sheet.py "<GOOGLE_SHEET_URL_OR_ID>"

Ví dụ:
    python3 fix_checkpoint_with_new_sheet.py "https://docs.google.com/spreadsheets/d/1CGDEsYlHjHie8BZCLNWwx4QP2nqU8hEd4wLGVUwEd-8/edit?gid=1451865645#gid=1451865645"
"""

import os
import sys
import re
import json

def extract_spreadsheet_id(input_str):
    # Regex trích xuất spreadsheet ID từ URL Google Sheets
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', input_str)
    if match:
        return match.group(1)
    # Nếu không khớp URL, coi như người dùng truyền trực tiếp ID
    if re.match(r'^[a-zA-Z0-9-_]+$', input_str):
        return input_str
    return None

def process_file(file_path, new_doc_id):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[-] Không thể đọc file {file_path}: {e}")
        return False

    nodes = data.get("nodes", [])
    sheet_nodes_count = 0

    for node in nodes:
        if node.get("type") == "n8n-nodes-base.googleSheets":
            sheet_nodes_count += 1
            params = node.get("parameters", {})
            
            orig_sheet = params.get("sheetName", {})
            
            # Trích xuất tên sheet (cachedResultName)
            sheet_name = "input"
            if isinstance(orig_sheet, dict):
                sheet_name = orig_sheet.get("cachedResultName", "input")
            elif isinstance(orig_sheet, str):
                sheet_name = orig_sheet
            
            # Chuẩn hóa documentId thành RL tĩnh với mode "id"
            params["documentId"] = {
                "__rl": True,
                "value": new_doc_id,
                "mode": "id"
            }
            
            # Chuẩn hóa sheetName thành RL tĩnh với mode "name"
            params["sheetName"] = {
                "__rl": True,
                "value": sheet_name,
                "mode": "name"
            }
            
            # Làm sạch credentials để tránh xung đột kết nối
            if "credentials" in node:
                node["credentials"] = {
                    "googleSheetsOAuth2Api": {
                        "id": "",
                        "name": ""
                    }
                }

    if sheet_nodes_count > 0:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[+] Đã cập nhật thành công {sheet_nodes_count} node Google Sheets trong file: {os.path.basename(file_path)}")
            return True
        except Exception as e:
            print(f"[-] Không thể ghi file {file_path}: {e}")
            return False
    else:
        return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_arg = sys.argv[1].strip()
    new_doc_id = extract_spreadsheet_id(input_arg)

    if not new_doc_id:
        print(f"[-] Lỗi: Không thể nhận diện được Spreadsheet ID hợp lệ từ đối số đầu vào: '{input_arg}'")
        sys.exit(1)

    print(f"[*] Đang sử dụng Spreadsheet ID: {new_doc_id}")

    # Đường dẫn thư mục chứa script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tìm tất cả các file .json trong thư mục hiện hành
    files = [f for f in os.listdir(current_dir) if f.endswith('.json')]
    
    updated_files = 0
    for file_name in sorted(files):
        file_path = os.path.join(current_dir, file_name)
        if process_file(file_path, new_doc_id):
            updated_files += 1

    print(f"[*] Hoàn tất! Đã cập nhật {updated_files} file checkpoint.")

if __name__ == "__main__":
    main()
