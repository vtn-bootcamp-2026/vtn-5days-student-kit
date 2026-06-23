#!/usr/bin/env python3
"""
Contract Term Extractor Skill — Validator Tool
Tự kiểm (self-check): fuzzy match nguồn dẫn, hiệu chỉnh confidence.

Usage:
    python validator.py --json <extracted_json> --source <contract_text>
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


def load_json(filepath: str) -> dict:
    """Nạp JSON từ file hoặc chuỗi JSON."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Thử parse trực tiếp nếu là chuỗi JSON
        try:
            return json.loads(filepath)
        except json.JSONDecodeError as e:
            print(f"Lỗi đọc JSON: {e}", file=sys.stderr)
            sys.exit(1)


def load_text(filepath: str) -> str:
    """Nạp text từ file (.txt hoặc .docx)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".docx" and HAS_DOCX:
        doc = DocxDocument(filepath)
        return "\n".join(p.text for p in doc.paragraphs)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def fuzzy_match(quote: str, source: str, threshold: float = 0.75) -> dict:
    """
    So sánh fuzzy giữa quote và đoạn text trong source.
    Trả về match ratio và đoạn best match.
    """
    quote = quote.strip()
    if not quote:
        return {"match": False, "ratio": 0.0, "reason": "Quote rỗng"}

    # Tìm đoạn best match trong source
    best_ratio = 0.0
    best_segment = ""

    # Sliding window
    quote_len = len(quote)
    source_len = len(source)
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
    """Kiểm tra đủ trường bắt buộc."""
    missing = []
    for field in required:
        if field not in data:
            missing.append(field)
        elif data[field] is None and field in ["effective_date", "expiry_date"]:
            # null cho ngày là chấp nhận được nhưng cần note
            missing.append(f"{field} (null)")
    return missing


def calibrate_confidence(data: dict) -> dict:
    """
    Hiệu chỉnh confidence dựa trên số lượng evidence thực tế.
    Rule: 3+ evidence → 0.85-0.95, 1-2 → 0.6-0.8, 0 → < 0.5
    """
    evidence_count = len(data.get("source_evidence", []))
    red_flag_count = len(data.get("red_flags", []))
    missing_count = len(data.get("missing_fields", []))

    # Base score từ evidence count
    if evidence_count >= 5:
        base = 0.90
    elif evidence_count >= 3:
        base = 0.85
    elif evidence_count >= 1:
        base = 0.70
    else:
        base = 0.40

    # Giảm nếu có red flags hoặc missing fields
    penalty = red_flag_count * 0.05 + missing_count * 0.03
    adjusted = max(0.1, base - penalty)

    reported = data.get("confidence", 0.5)
    diff = abs(reported - adjusted)

    return {
        "reported_confidence": reported,
        "adjusted_confidence": round(adjusted, 2),
        "evidence_count": evidence_count,
        "deviation": round(diff, 2),
        "needs_adjustment": diff > 0.2,
        "reason": f"Base={base}, penalty=-{penalty:.2f} ({red_flag_count} red_flags, {missing_count} missing)"
    }


def run_validation(json_data: dict, source_text: str) -> dict:
    """Chạy toàn bộ validation."""
    result = {
        "valid": True,
        "issues": [],
        "source_evidence_check": [],
        "confidence_calibration": None,
        "field_check": None
    }

    # 1. Check required fields
    required = ["contract_id", "effective_date", "expiry_date", "penalty_clause",
                "source_evidence", "confidence", "needs_human_review",
                "red_flags", "missing_fields", "extraction_notes"]
    missing = check_required_fields(json_data, required)
    result["field_check"] = {
        "required": len(required),
        "present": len(required) - len(missing),
        "missing": missing
    }
    if missing:
        result["issues"].append(f"Thiếu trường: {', '.join(missing)}")
        result["valid"] = False

    # 2. Fuzzy match source evidence
    evidence = json_data.get("source_evidence", [])
    for ev in evidence:
        quote = ev.get("quote", "")
        match = fuzzy_match(quote, source_text)
        result["source_evidence_check"].append({
            "field": ev.get("field"),
            "match_ratio": match["ratio"],
            "passed": match["match"]
        })
        if not match["match"]:
            result["issues"].append(f"Source evidence không khớp: field '{ev.get('field')}' (ratio={match['ratio']})")

    # 3. Calibrate confidence
    calibration = calibrate_confidence(json_data)
    result["confidence_calibration"] = calibration
    if calibration["needs_adjustment"]:
        result["issues"].append(
            f"Confidence lệch lớn: báo cáo {calibration['reported_confidence']}, "
            f"hiệu chỉnh {calibration['adjusted_confidence']} (deviation={calibration['deviation']})"
        )

    # 4. Check HITL trigger correctness
    has_red_flags = len(json_data.get("red_flags", [])) > 0
    has_missing = len(json_data.get("missing_fields", [])) > 0
    low_confidence = json_data.get("confidence", 1.0) < 0.7
    should_hitl = has_red_flags or has_missing or low_confidence
    is_hitl = json_data.get("needs_human_review", False)

    if should_hitl and not is_hitl:
        result["issues"].append("needs_human_review=false nhưng có red_flags/missing/low_confidence → phải bật true")
        result["valid"] = False

    return result


def main():
    parser = argparse.ArgumentParser(description="Contract extraction validator")
    parser.add_argument("--json", required=True, help="File JSON đã trích xuất")
    parser.add_argument("--source", required=True, help="File text hợp đồng gốc")
    parser.add_argument("--output", help="File xuất kết quả (mặc định: stdout)")
    args = parser.parse_args()

    json_data = load_json(args.json)
    source_text = load_text(args.source)

    result = run_validation(json_data, source_text)

    # Cập nhật needs_human_review nếu phát hiện vấn đề
    if not result["valid"] and not json_data.get("needs_human_review"):
        json_data["needs_human_review"] = True
        result["auto_corrected"] = {"needs_human_review": True}

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Kết quả validation đã lưu: {args.output}")
    else:
        print(output)

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
