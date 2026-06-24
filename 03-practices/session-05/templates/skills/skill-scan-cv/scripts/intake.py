#!/usr/bin/env python3
"""
CV Screening Skill — Intake Tool
Kiểm tra tính hợp lệ của hồ sơ ứng viên (CV) đầu vào.

Usage:
    python scripts/intake.py --file <path_to_cv>
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

try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False


def check_file_exists(filepath: str) -> dict:
    """Kiểm tra tệp tin tồn tại."""
    if not os.path.exists(filepath):
        return {"valid": False, "error": "FILE_NOT_FOUND", "message": f"Tệp tin không tồn tại: {filepath}"}
    return {"valid": True}


def check_file_not_empty(filepath: str) -> dict:
    """Kiểm tra tệp tin không rỗng."""
    if os.path.getsize(filepath) == 0:
        return {"valid": False, "error": "FILE_EMPTY", "message": "Tệp tin rỗng, không có dữ liệu để quét"}
    return {"valid": True}


def check_min_length(content: str, min_chars: int = 100) -> dict:
    """Kiểm tra độ dài tối thiểu của văn bản."""
    clean = content.strip()
    if len(clean) < min_chars:
        return {
            "valid": False,
            "error": "TEXT_TOO_SHORT",
            "message": f"Hồ sơ quá ngắn ({len(clean)} ký tự). Yêu cầu tối thiểu {min_chars} ký tự."
        }
    return {"valid": True, "char_count": len(clean)}


def estimate_ocr_error_rate(content: str) -> dict:
    """Ước lượng tỷ lệ lỗi trích xuất hoặc OCR."""
    indicators = 0
    total_chars = len(content)

    if total_chars == 0:
        return {"ocr_error_rate": 1.0, "status": "EMPTY"}

    # Đếm ký tự lỗi font, ký tự rác phổ biến
    ocr_noise_chars = content.count("\ufffd") + content.count("##")
    # Đếm từ quá dài bất thường (do dính chữ khi parse)
    long_chunks = sum(1 for w in content.split() if len(w) > 50)

    indicators = ocr_noise_chars + long_chunks * 5
    error_rate = min(indicators / total_chars, 1.0)

    if error_rate > 0.3:
        return {"ocr_error_rate": error_rate, "status": "SEVERE", "message": f"Lỗi định dạng/OCR nghiêm trọng ({error_rate:.0%})"}
    elif error_rate > 0.1:
        return {"ocr_error_rate": error_rate, "status": "MODERATE", "message": f"Lỗi định dạng/OCR vừa ({error_rate:.0%})"}
    else:
        return {"ocr_error_rate": error_rate, "status": "OK", "message": f"Chất lượng văn bản tốt ({error_rate:.0%})"}


def run_intake(filepath: str) -> dict:
    """Chạy toàn bộ quy trình kiểm tra intake."""
    result = {
        "file": filepath,
        "timestamp": datetime.now().isoformat(),
        "checks": [],
        "valid": True,
        "needs_human_review": False
    }

    # Kiểm tra 1: File tồn tại
    check = check_file_exists(filepath)
    result["checks"].append({"name": "file_exists", **check})
    if not check["valid"]:
        result["valid"] = False
        return result

    # Kiểm tra 2: File không rỗng
    check = check_file_not_empty(filepath)
    result["checks"].append({"name": "not_empty", **check})
    if not check["valid"]:
        result["valid"] = False
        return result

    # Đọc nội dung file dựa trên đuôi mở rộng
    ext = os.path.splitext(filepath)[1].lower()
    content = ""

    if ext == ".docx":
        if not HAS_DOCX:
            result["valid"] = False
            result["checks"].append({
                "name": "format", 
                "valid": False, 
                "error": "MISSING_DEP", 
                "message": "Vui lòng cài python-docx để đọc file .docx: pip install python-docx"
            })
            return result
        try:
            doc = DocxDocument(filepath)
            content = "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            result["valid"] = False
            result["checks"].append({"name": "format", "valid": False, "error": "DOCX_ERROR", "message": f"Lỗi đọc .docx: {e}"})
            return result
    elif ext == ".pdf":
        if not HAS_PDF:
            result["valid"] = False
            result["checks"].append({
                "name": "format", 
                "valid": False, 
                "error": "MISSING_DEP", 
                "message": "Vui lòng cài pdfplumber để đọc file .pdf: pip install pdfplumber"
            })
            return result
        try:
            with pdfplumber.open(filepath) as pdf:
                content = "\n".join(page.extract_text() or "" for page in pdf.pages)
        except Exception as e:
            result["valid"] = False
            result["checks"].append({"name": "format", "valid": False, "error": "PDF_ERROR", "message": f"Lỗi đọc .pdf: {e}"})
            return result
    elif ext in [".txt", ".md"]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            result["valid"] = False
            result["checks"].append({"name": "encoding", "valid": False, "error": "ENCODING_ERROR", "message": "Lỗi mã hóa tệp tin (hãy dùng UTF-8)"})
            return result
    else:
        result["valid"] = False
        result["checks"].append({
            "name": "format", 
            "valid": False, 
            "error": "UNSUPPORTED", 
            "message": f"Định dạng không hỗ trợ: {ext}. Vui lòng dùng .docx, .pdf, .txt hoặc .md"
        })
        return result

    # Che thông tin nhạy cảm PII trước khi kiểm tra và chuyển qua bước tiếp theo
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from condact_pii import condact_text
    except ImportError:
        from scripts.condact_pii import condact_text

    content = condact_text(content)

    # Ghi file sạch đã che PII ra outputs
    base_name = os.path.basename(filepath)
    name_part, _ = os.path.splitext(base_name)
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    redacted_filepath = os.path.join(output_dir, f"redacted-{name_part}.txt")
    with open(redacted_filepath, "w", encoding="utf-8") as f:
        f.write(content)

    result["redacted_file"] = redacted_filepath
    result["redacted_content"] = content

    # Kiểm tra 3: Độ dài tối thiểu
    check = check_min_length(content, min_chars=100)
    result["checks"].append({"name": "min_length", **check})
    if not check["valid"]:
        result["valid"] = False
        result["needs_human_review"] = True
        return result

    # Kiểm tra 4: Ước lượng chất lượng OCR/văn bản
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
    parser = argparse.ArgumentParser(description="CV Screening intake validation tool")
    parser.add_argument("--file", required=True, help="Đường dẫn tới file CV")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới dạng JSON")
    args = parser.parse_args()

    result = run_intake(args.file)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== Kết quả Intake: {args.file} ===")
        print(f"Hợp lệ: {result['valid']}")
        print(f"Cần người duyệt: {result['needs_human_review']}")
        if "redacted_file" in result:
            print(f"File đã che PII: {result['redacted_file']}")
        for check in result["checks"]:
            status = "ĐẠT" if check.get("valid", True) else "LỖI"
            print(f"  [{status}] {check['name']}: {check.get('message', 'Thành công')}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
