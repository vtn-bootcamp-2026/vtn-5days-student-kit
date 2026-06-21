#!/usr/bin/env python3
"""
Contract Term Extractor Skill — Router Tool
Ghi log CSV hoạt động và định tuyến ca khó sang HITL.

Usage:
    python router.py --json <validated_json> [--rules <red_flag_rules>] [--log <log_file>]
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime


LOG_COLUMNS = [
    "run_id", "contract_id", "status", "error_type",
    "needs_human_review", "confidence", "red_flag_count",
    "missing_field_count", "source_evidence_count",
    "route_reason", "created_at"
]


def load_json(filepath: str) -> dict:
    """Nạp JSON từ file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Lỗi đọc JSON: {e}", file=sys.stderr)
        sys.exit(1)


def determine_route(data: dict) -> dict:
    """
    Xác định tuyến định tuyến dựa trên kết quả trích xuất.
    - AUTO: đầy đủ, confidence cao, không cờ đỏ
    - HITL: có cờ đỏ, thiếu trường, confidence thấp
    - REJECT: lỗi nghiêm trọng, không thể xử lý
    """
    red_flags = data.get("red_flags", [])
    missing = data.get("missing_fields", [])
    confidence = data.get("confidence", 0.0)
    needs_review = data.get("needs_human_review", False)
    notes = data.get("extraction_notes", "")

    reasons = []

    # Kiểm tra reject (lỗi nghiêm trọng)
    if "OCR lỗi nghiêm trọng" in notes or confidence < 0.3:
        return {
            "route": "REJECT",
            "reasons": ["Confidence quá thấp hoặc OCR lỗi nghiêm trọng"],
            "action": "Trả về người dùng kèm yêu cầu gửi lại văn bản chất lượng cao hơn"
        }

    # Kiểm tra HITL
    if needs_review:
        reasons.append("needs_human_review=true")

    if red_flags:
        reasons.append(f"{len(red_flags)} cờ đỏ: {'; '.join(red_flags[:3])}")

    if len(missing) >= 2:
        reasons.append(f"Thiếu {len(missing)} trường quan trọng: {', '.join(missing)}")

    if confidence < 0.7:
        reasons.append(f"Confidence thấp: {confidence}")

    if reasons:
        return {
            "route": "HITL",
            "reasons": reasons,
            "action": "Chuyển người rà soát. Đính kèm báo cáo cờ đỏ và danh sách trường thiếu."
        }

    # AUTO — xử lý tự động
    return {
        "route": "AUTO",
        "reasons": [],
        "action": "Xử lý tự động. Lưu kết quả và tiếp tục."
    }


def generate_run_id() -> str:
    """Tạo run ID duy nhất."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"RUN-{timestamp}"


def append_to_log(log_path: str, row: dict):
    """Ghi một dòng vào CSV log."""
    file_exists = os.path.exists(log_path)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def generate_red_flag_report(data: dict, route: dict) -> str:
    """Tạo báo cáo cờ đỏ dạng Markdown."""
    red_flags = data.get("red_flags", [])
    if not red_flags:
        return ""

    lines = [
        f"# Báo cáo cờ đỏ: {data.get('contract_id', 'N/A')}",
        "",
        f"**Ngày tạo:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Confidence:** {data.get('confidence', 'N/A')}",
        f"**Tuyến:** {route['route']}",
        "",
        "## Cờ đỏ phát hiện",
        ""
    ]

    for i, flag in enumerate(red_flags, 1):
        lines.append(f"{i}. {flag}")

    # Source evidence cho red flags
    evidence = data.get("source_evidence", [])
    if evidence:
        lines.extend([
            "",
            "## Nguồn dẫn",
            ""
        ])
        for ev in evidence:
            if any(keyword in ev.get("field", "").lower() for keyword in ["red_flag", "penalty", "renewal", "liability"]):
                lines.append(f"- **{ev.get('field')}** ({ev.get('section')}): \"{ev.get('quote')}\"")

    lines.extend([
        "",
        "## Đề xuất hành động",
        ""
    ])
    for reason in route.get("reasons", []):
        lines.append(f"- {reason}")

    lines.append(f"- {route.get('action', 'Chờ xử lý')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Contract routing and logging tool")
    parser.add_argument("--json", required=True, help="File JSON đã validate")
    parser.add_argument("--rules", help="File red-flag rules (hiện chỉ để tham chiếu)")
    parser.add_argument("--log", default="execution-log.csv", help="File CSV log (mặc định: execution-log.csv)")
    parser.add_argument("--report", help="Xuất báo cáo cờ đỏ ra file Markdown")
    args = parser.parse_args()

    data = load_json(args.json)

    # 1. Determine route
    route = determine_route(data)

    # 2. Generate run ID and log
    run_id = generate_run_id()
    log_row = {
        "run_id": run_id,
        "contract_id": data.get("contract_id", "UNKNOWN"),
        "status": route["route"],
        "error_type": "; ".join(route["reasons"]) if route["reasons"] else "",
        "needs_human_review": data.get("needs_human_review", False),
        "confidence": data.get("confidence", 0.0),
        "red_flag_count": len(data.get("red_flags", [])),
        "missing_field_count": len(data.get("missing_fields", [])),
        "source_evidence_count": len(data.get("source_evidence", [])),
        "route_reason": route["route"],
        "created_at": datetime.now().isoformat()
    }

    append_to_log(args.log, log_row)

    # 3. Output
    output = {
        "run_id": run_id,
        "contract_id": data.get("contract_id"),
        "route": route["route"],
        "reasons": route["reasons"],
        "action": route["action"],
        "logged_to": args.log
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    # 4. Generate red flag report if needed
    if route["route"] == "HITL" and args.report:
        report = generate_red_flag_report(data, route)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nBáo cáo cờ đỏ đã lưu: {args.report}")

    sys.exit(0)


if __name__ == "__main__":
    main()
