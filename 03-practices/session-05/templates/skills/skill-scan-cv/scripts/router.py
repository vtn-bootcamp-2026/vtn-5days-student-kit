#!/usr/bin/env python3
"""
CV Screening Skill — Router Tool
Định tuyến hồ sơ (Auto/HITL/Reject), ghi nhật ký hoạt động (execution log) và xuất báo cáo.

Usage:
    python scripts/router.py --json <validated_json> [--log <log_file>] [--report <report_file>]
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

LOG_COLUMNS = [
    "run_id", "candidate_name", "status", "suitability_score",
    "need_review", "confidence_score", "red_flag_count",
    "evidence_count", "route_reasons", "created_at"
]


def load_json(filepath: str) -> dict:
    """Nạp JSON từ file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi nạp JSON: {e}", file=sys.stderr)
        sys.exit(1)


def determine_route(data: dict) -> dict:
    """
    Xác định tuyến dựa trên điểm và cờ đỏ.
    - AUTO_PASS: Điểm >= 80, không có cờ đỏ, confidence >= 0.7
    - REJECT: Điểm < 50
    - HITL: Các trường hợp còn lại
    """
    score = data.get("suitability_score", 0)
    red_flags = data.get("red_flags", [])
    confidence = data.get("confidence_score", 0.0)
    need_review = data.get("need_review", False)
    
    reasons = []

    # 1. Kiểm tra REJECT
    if score < 50:
        return {
            "route": "reject",
            "reasons": [f"Điểm phù hợp quá thấp: {score}/100"],
            "action": "Tự động loại hồ sơ do không đáp ứng tiêu chuẩn tối thiểu."
        }

    # 2. Kiểm tra HITL (Cần người duyệt)
    if need_review:
        reasons.append("Yêu cầu duyệt thủ công từ bước trước (need_review=true)")
    
    if red_flags:
        reasons.append(f"Phát hiện {len(red_flags)} cờ đỏ: {'; '.join(red_flags)}")

    if confidence < 0.7:
        reasons.append(f"Độ tin cậy trích xuất của AI thấp: {confidence}")

    if 50 <= score < 80:
        reasons.append(f"Điểm phù hợp nằm trong vùng nghi vấn: {score}/100")

    if reasons:
        return {
            "route": "needs_human_review",
            "reasons": reasons,
            "action": "Chuyển hồ sơ sang hàng đợi duyệt của phòng HR. Đính kèm báo cáo cờ đỏ."
        }

    # 3. Tự động đạt (AUTO_PASS)
    return {
        "route": "auto_pass",
        "reasons": [],
        "action": "Tự động chấp nhận hồ sơ. Xếp lịch phỏng vấn sơ bộ."
    }


def generate_run_id() -> str:
    """Sinh mã định danh lượt chạy duy nhất."""
    return f"RUN-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def append_to_log(log_path: str, row: dict):
    """Ghi nhật ký vận hành ra file CSV."""
    file_exists = os.path.exists(log_path)
    
    # Tạo thư mục cha nếu chưa có
    parent_dir = os.path.dirname(log_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def generate_evaluation_report(data: dict, route: dict) -> str:
    """Sinh báo cáo đánh giá chi tiết định dạng Markdown."""
    candidate_name = data.get("candidate_name", "N/A")
    score = data.get("suitability_score", 0)
    red_flags = data.get("red_flags", [])
    matched = data.get("matched_criteria", [])
    missing = data.get("missing_criteria", [])
    evidence = data.get("evidence", [])

    lines = [
        f"# Báo cáo đánh giá hồ sơ ứng viên: {candidate_name}",
        "",
        f"**Thời gian quét:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Điểm độ phù hợp:** {score}/100",
        f"**Kết quả định tuyến:** `{route['route'].upper()}`",
        f"**Độ tin cậy trích xuất:** {data.get('confidence_score', 0.0)}",
        "",
        "## Phân tích độ phù hợp",
        "",
        "### Tiêu chí đáp ứng tốt (Matched):",
    ]

    if matched:
        for item in matched:
            lines.append(f"- ✅ {item}")
    else:
        lines.append("- *Không có ghi nhận tiêu chí nổi bật hoặc đầy đủ*")

    lines.extend([
        "",
        "### Tiêu chí còn thiếu hoặc yếu (Missing):",
    ])

    if missing:
        for item in missing:
            lines.append(f"- ❌ {item}")
    else:
        lines.append("- *Không có thiếu sót nghiêm trọng nào được phát hiện*")

    if red_flags:
        lines.extend([
            "",
            "## Cảnh báo cờ đỏ (Red Flags) ⚠️",
            ""
        ])
        for flag in red_flags:
            lines.append(f"- **{flag}**")

    if evidence:
        lines.extend([
            "",
            "## Dẫn chứng trích xuất từ CV (Evidence)",
            ""
        ])
        for ev in evidence:
            lines.append(f"- **{ev.get('claim')}**: \"*{ev.get('verbatim_quote')}*\" (Nguồn: `{ev.get('source')}`) ")

    lines.extend([
        "",
        "## Đề xuất hành động từ hệ thống",
        "",
        f"**Lý do định tuyến:**"
    ])
    
    if route["reasons"]:
        for reason in route["reasons"]:
            lines.append(f"- {reason}")
    else:
        lines.append("- Hồ sơ sạch, điểm số cao, đáp ứng đầy đủ tiêu chí.")

    lines.append(f"\n**Hành động tiếp theo:** {route['action']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CV evaluation routing and logging tool")
    parser.add_argument("--json", required=True, help="File JSON kết quả đã qua validate")
    parser.add_argument("--log", default="output/skill-scan-cv/outputs/execution-log.csv", help="Đường dẫn file CSV ghi log")
    parser.add_argument("--report", help="Đường dẫn lưu báo cáo Markdown đánh giá")
    args = parser.parse_args()

    data = load_json(args.json)

    # 1. Định tuyến hồ sơ
    route = determine_route(data)

    # 2. Sinh run ID và ghi nhật ký
    run_id = generate_run_id()
    log_row = {
        "run_id": run_id,
        "candidate_name": data.get("candidate_name", "UNKNOWN"),
        "status": route["route"],
        "suitability_score": data.get("suitability_score", 0),
        "need_review": data.get("need_review", False),
        "confidence_score": data.get("confidence_score", 0.0),
        "red_flag_count": len(data.get("red_flags", [])),
        "evidence_count": len(data.get("evidence", [])),
        "route_reasons": "; ".join(route["reasons"]) if route["reasons"] else "None",
        "created_at": datetime.now().isoformat()
    }

    append_to_log(args.log, log_row)

    # 3. In kết quả định tuyến ra stdout
    output = {
        "run_id": run_id,
        "candidate_name": data.get("candidate_name"),
        "route": route["route"],
        "reasons": route["reasons"],
        "action": route["action"],
        "logged_to": args.log
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

    # 4. Tạo báo cáo Markdown nếu được yêu cầu
    if args.report:
        # Đảm bảo thư mục lưu báo cáo tồn tại
        parent_dir = os.path.dirname(args.report)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
            
        report = generate_evaluation_report(data, route)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nBáo cáo đánh giá đã được lưu tại: {args.report}")

    sys.exit(0)


if __name__ == "__main__":
    main()

