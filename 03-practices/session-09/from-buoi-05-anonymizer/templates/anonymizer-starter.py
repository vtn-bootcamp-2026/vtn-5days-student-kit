from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"(?:\+84\s?)?\b0?\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b"),
    "cccd": re.compile(r"\b\d{12}\b"),
}


def redact_text(text: str) -> tuple[str, dict[str, int], bool]:
    counts: dict[str, int] = {}
    redacted = text

    for pii_type, pattern in PATTERNS.items():
        matches = pattern.findall(redacted)
        counts[pii_type] = len(matches)
        redacted = pattern.sub(f"[REDACTED_{pii_type.upper()}]", redacted)

    needs_human_review = "prompt injection" in text.lower() or "khong chac chan" in text.lower()
    return redacted, counts, needs_human_review


def write_log(log_path: Path, input_file: Path, status: str, counts: dict[str, int], needs_human_review: bool) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()

    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["run_id", "input_file", "status", "pii_count", "needs_human_review", "created_at"],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "input_file": input_file.name,
                "status": status,
                "pii_count": sum(counts.values()),
                "needs_human_review": str(needs_human_review).lower(),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )


def main() -> None:
    # Tuỳ biến đường dẫn động để chạy được từ bất kỳ thư mục làm việc (CWD) nào
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent if script_dir.name == "templates" else script_dir

    input_path = base_dir / "synthetic-data/pii-sample-01.txt"
    output_path = base_dir / "outputs" / f"{input_path.stem}-redacted{input_path.suffix}"
    log_path = base_dir / "outputs/execution-log.csv"

    if not input_path.exists():
        print(f"Lỗi: Không tìm thấy tệp dữ liệu đầu vào tại: {input_path}")
        print("Vui lòng đảm bảo bạn đang chạy script trong đúng thư mục bài học.")
        return

    text = input_path.read_text(encoding="utf-8")
    redacted, counts, needs_human_review = redact_text(text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(redacted, encoding="utf-8")
    write_log(log_path, input_path, "success", counts, needs_human_review)

    print(f"Redacted {sum(counts.values())} items. needs_human_review={needs_human_review}")



if __name__ == "__main__":
    main()
