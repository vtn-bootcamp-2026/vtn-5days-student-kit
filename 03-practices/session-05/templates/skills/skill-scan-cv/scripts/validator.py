#!/usr/bin/env python3
"""
CV Screening Skill — Validator Tool
Tự kiểm chứng dữ liệu trích xuất từ CV, so khớp evidence và hiệu chỉnh độ tin cậy.

Usage:
    python scripts/validator.py --json <extracted_json> --source <cv_text>
"""

import argparse
import json
import os
import sys
from difflib import SequenceMatcher

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


def load_json(filepath: str) -> dict:
    """Nạp dữ liệu JSON từ file hoặc chuỗi JSON."""
    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return json.loads(filepath)
    except Exception as e:
        print(f"Lỗi nạp JSON: {e}", file=sys.stderr)
        sys.exit(1)


def load_text(filepath: str) -> str:
    """Nạp văn bản thô từ file (.txt, .md, .docx, .pdf)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".docx" and HAS_DOCX:
        doc = DocxDocument(filepath)
        return "\n".join(p.text for p in doc.paragraphs)
    elif ext == ".pdf" and HAS_PDF:
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def fuzzy_match(quote: str, source: str, threshold: float = 0.75) -> dict:
    """
    So khớp mờ (fuzzy match) quote với văn bản nguồn.
    Trả về tỷ lệ khớp và đoạn khớp tốt nhất.
    """
    quote = quote.strip()
    if not quote:
        return {"match": False, "ratio": 0.0, "reason": "Dẫn chứng rỗng"}

    best_ratio = 0.0
    best_segment = ""

    quote_len = len(quote)
    source_len = len(source)
    
    # Tìm kiếm trượt cửa sổ
    step = max(1, quote_len // 4)
    for i in range(0, source_len - quote_len + 1, step):
        segment = source[i:i + quote_len]
        ratio = SequenceMatcher(None, quote.lower(), segment.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_segment = segment

    return {
        "match": best_ratio >= threshold,
        "ratio": round(best_ratio, 3),
        "threshold": threshold,
        "best_segment": best_segment[:100] + "..." if len(best_segment) > 100 else best_segment
    }


def check_required_fields(data: dict, required: list) -> list:
    """Kiểm tra sự tồn tại của các trường bắt buộc."""
    missing = []
    for field in required:
        if field not in data:
            missing.append(field)
    return missing


def calibrate_confidence(data: dict) -> dict:
    """
    Hiệu chỉnh độ tin cậy dựa trên số lượng dẫn chứng (evidence).
    """
    evidence_count = len(data.get("evidence", []))
    red_flag_count = len(data.get("red_flags", []))
    
    # Tính điểm nền dựa trên số lượng evidence
    if evidence_count >= 4:
        base = 0.95
    elif evidence_count >= 2:
        base = 0.80
    elif evidence_count >= 1:
        base = 0.65
    else:
        base = 0.35

    # Phạt điểm tin cậy nếu phát hiện có nhiều cờ đỏ
    penalty = red_flag_count * 0.08
    adjusted = max(0.1, base - penalty)

    reported = data.get("confidence_score", 0.5)
    diff = abs(reported - adjusted)

    return {
        "reported_confidence": reported,
        "adjusted_confidence": round(adjusted, 2),
        "evidence_count": evidence_count,
        "deviation": round(diff, 2),
        "needs_adjustment": diff > 0.2,
        "reason": f"Base={base}, penalty=-{penalty:.2f} ({red_flag_count} cờ đỏ)"
    }


def run_validation(json_data: dict, source_text: str) -> dict:
    """Thực thi toàn bộ quy trình kiểm chứng."""
    result = {
        "valid": True,
        "issues": [],
        "evidence_check": [],
        "confidence_calibration": None,
        "field_check": None
    }

    # 1. Kiểm tra các trường bắt buộc
    required = [
        "candidate_name", "contact_info", "experience_years", "education",
        "skills", "suitability_score", "red_flags", "status",
        "evidence", "confidence_score", "need_review"
    ]
    missing = check_required_fields(json_data, required)
    result["field_check"] = {
        "required": len(required),
        "present": len(required) - len(missing),
        "missing": missing
    }
    if missing:
        result["issues"].append(f"Thiếu trường bắt buộc trong schema: {', '.join(missing)}")
        result["valid"] = False

    # 2. So khớp mờ các evidence dẫn chứng
    evidence = json_data.get("evidence", [])
    for ev in evidence:
        quote = ev.get("verbatim_quote", "")
        match = fuzzy_match(quote, source_text)
        result["evidence_check"].append({
            "claim": ev.get("claim"),
            "match_ratio": match["ratio"],
            "passed": match["match"]
        })
        if not match["match"]:
            result["issues"].append(f"Dẫn chứng không khớp văn bản gốc: '{ev.get('claim')}' (tỷ lệ={match['ratio']})")
            result["valid"] = False

    # 3. Hiệu chỉnh độ tin cậy
    calibration = calibrate_confidence(json_data)
    result["confidence_calibration"] = calibration
    if calibration["needs_adjustment"]:
        result["issues"].append(
            f"Độ tin cậy khai báo lệch lớn: khai báo {calibration['reported_confidence']}, "
            f"hiệu chỉnh {calibration['adjusted_confidence']}"
        )

    # 4. Kiểm tra điều kiện định tuyến HITL
    has_red_flags = len(json_data.get("red_flags", [])) > 0
    low_confidence = json_data.get("confidence_score", 1.0) < 0.7
    should_hitl = has_red_flags or low_confidence
    is_hitl = json_data.get("need_review", False)

    if should_hitl and not is_hitl:
        result["issues"].append("need_review đang là false nhưng hồ sơ có cờ đỏ hoặc độ tin cậy thấp -> Phải đổi thành true")
        result["valid"] = False

    return result


def main():
    parser = argparse.ArgumentParser(description="CV extraction data validator")
    parser.add_argument("--json", required=True, help="File JSON kết quả trích xuất")
    parser.add_argument("--source", required=True, help="File văn bản CV gốc")
    parser.add_argument("--output", help="File ghi kết quả validation (mặc định xuất stdout)")
    args = parser.parse_args()

    json_data = load_json(args.json)
    source_text = load_text(args.source)

    # Tự động che PII của source_text trước khi validation để khớp với dữ liệu đã che PII của AI
    try:
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from condact_pii import condact_text
        source_text = condact_text(source_text)
    except ImportError:
        try:
            from scripts.condact_pii import condact_text
            source_text = condact_text(source_text)
        except ImportError:
            pass

    result = run_validation(json_data, source_text)

    # Tự động sửa chữa thuộc tính need_review nếu phát hiện vấn đề cần kiểm duyệt
    if not result["valid"] and not json_data.get("need_review"):
        json_data["need_review"] = True
        result["auto_corrected"] = {"need_review": True}

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Kết quả kiểm chứng đã lưu tại: {args.output}")
    else:
        print(output)

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
