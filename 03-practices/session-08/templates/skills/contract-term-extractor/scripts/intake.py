#!/usr/bin/env python3
"""
Contract Term Extractor Skill — Intake Tool
Kiểm tra tính hợp lệ của file hợp đồng đầu vào.

Usage:
    python intake.py --file <path_to_contract>
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


def check_file_exists(filepath: str) -> dict:
    """Kiểm tra file tồn tại."""
    if not os.path.exists(filepath):
        return {"valid": False, "error": "FILE_NOT_FOUND", "message": f"File không tồn tại: {filepath}"}
    return {"valid": True}


def check_file_not_empty(filepath: str) -> dict:
    """Kiểm tra file không rỗng."""
    if os.path.getsize(filepath) == 0:
        return {"valid": False, "error": "FILE_EMPTY", "message": "File rỗng, không có nội dung để xử lý"}
    return {"valid": True}


def check_min_length(content: str, min_chars: int = 100) -> dict:
    """Kiểm tra độ dài tối thiểu (bỏ qua khoảng trắng)."""
    clean = content.strip()
    if len(clean) < min_chars:
        return {
            "valid": False,
            "error": "TEXT_TOO_SHORT",
            "message": f"Văn bản quá ngắn ({len(clean)} ký tự). Tối thiểu {min_chars} ký tự."
        }
    return {"valid": True, "char_count": len(clean)}


def estimate_ocr_error_rate(content: str) -> dict:
    """Ước lượng tỷ lệ lỗi OCR dựa trên các dấu hiệu phổ biến."""
    indicators = 0
    total_chars = len(content)

    if total_chars == 0:
        return {"ocr_error_rate": 1.0, "status": "EMPTY"}

    # Dấu hiệu OCR lỗi: ký tự lạ lặp lại, khoảng trắng bất thường, ký tự không xác định
    ocr_noise_chars = content.count("�") + content.count("�") + content.count("##")
    # Từ dính nhau (không khoảng trắng giữa các từ tiếng Việt dài)
    long_chunks = sum(1 for w in content.split() if len(w) > 50)

    indicators = ocr_noise_chars + long_chunks * 5
    error_rate = min(indicators / total_chars, 1.0)

    if error_rate > 0.3:
        return {"ocr_error_rate": error_rate, "status": "SEVERE", "message": f"OCR lỗi nghiêm trọng ({error_rate:.0%})"}
    elif error_rate > 0.1:
        return {"ocr_error_rate": error_rate, "status": "MODERATE", "message": f"OCR lỗi vừa ({error_rate:.0%})"}
    else:
        return {"ocr_error_rate": error_rate, "status": "OK", "message": f"OCR chấp nhận được ({error_rate:.0%})"}


def run_intake(filepath: str) -> dict:
    """Chạy toàn bộ kiểm tra intake."""
    result = {
        "file": filepath,
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "valid": True,
        "needs_human_review": False
    }

    # Check 1: File tồn tại
    check = check_file_exists(filepath)
    result["checks"].append({"name": "file_exists", **check})
    if not check["valid"]:
        result["valid"] = False
        return result

    # Check 2: File không rỗng
    check = check_file_not_empty(filepath)
    result["checks"].append({"name": "not_empty", **check})
    if not check["valid"]:
        result["valid"] = False
        return result

    # Đọc nội dung
    ext = os.path.splitext(filepath)[1].lower()
    content = ""

    if ext == ".docx":
        if not HAS_DOCX:
            result["valid"] = False
            result["checks"].append({"name": "format", "valid": False, "error": "MISSING_DEP", "message": "Cài python-docx để đọc .docx: pip install python-docx"})
            return result
        try:
            doc = DocxDocument(filepath)
            content = "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            result["valid"] = False
            result["checks"].append({"name": "format", "valid": False, "error": "DOCX_ERROR", "message": f"Lỗi đọc .docx: {e}"})
            return result
    elif ext == ".txt":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            result["valid"] = False
            result["checks"].append({"name": "encoding", "valid": False, "error": "ENCODING_ERROR", "message": "Không đọc được file (lỗi encoding)"})
            return result
    else:
        result["valid"] = False
        result["checks"].append({"name": "format", "valid": False, "error": "UNSUPPORTED", "message": f"Định dạng không hỗ trợ: {ext}. Dùng .docx hoặc .txt"})
        return result

    # Check 3: Độ dài tối thiểu
    check = check_min_length(content, min_chars=100)
    result["checks"].append({"name": "min_length", **check})
    if not check["valid"]:
        result["valid"] = False
        result["needs_human_review"] = True
        return result

    # Check 4: OCR error rate
    ocr = estimate_ocr_error_rate(content)
    result["checks"].append({"name": "ocr_quality", **ocr})
    if ocr["status"] == "SEVERE":
        result["valid"] = False
        result["needs_human_review"] = True
    elif ocr["status"] == "MODERATE":
        result["needs_human_review"] = True

    result["char_count"] = len(content)
    result["line_count"] = len(content.splitlines())

    return result


def main():
    parser = argparse.ArgumentParser(description="Contract intake validation tool")
    parser.add_argument("--file", required=True, help="Đường dẫn file hợp đồng")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dạng JSON")
    args = parser.parse_args()

    result = run_intake(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== Intake Result: {args.file} ===")
        print(f"Valid: {result['valid']}")
        print(f"Needs human review: {result['needs_human_review']}")
        for check in result["checks"]:
            status = "PASS" if check.get("valid", True) else "FAIL"
            print(f"  [{status}] {check['name']}: {check.get('message', 'OK')}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
