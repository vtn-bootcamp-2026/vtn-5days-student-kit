"""
Vệ sĩ văn phòng VTN — BẢN KHỞI ĐIỂM (starter)
================================================
Mục đích: bản mã nguồn "thô" để học viên (non-tech) nạp vào Antigravity,
rồi dùng các prompt step-by-step trong lab.md để nâng cấp dần thành Skill hoàn chỉnh.

TRẠNG THÁI HIỆN TẠI (chỉ làm được một phần — cần học viên nâng cấp):
- [x] Đọc văn bản tiếng Việt có dấu
- [x] Ẩn email, số điện thoại, CCCD bằng Regex
- [ ] CHƯA ẩn tên người (cần Antigravity bổ sung)
- [ ] CHƯA giữ lại thuật ngữ an toàn (mã phiếu, số tiền, tên bộ phận)
- [ ] CHƯA phát hiện prompt injection
- [ ] CHƯA có hook chặn thao tác nguy hiểm

→ Học viên KHÔNG cần viết code tay. Mở file này trong Antigravity,
  rồi dán lần lượt các prompt ở lab.md (Part B, C, D). Antigravity sẽ sửa giúp.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from datetime import datetime
from pathlib import Path

# --- Bộ quy tắc nhận diện (Regex) ---
PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"(?:\+84\s?)?\b0?\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b"),
    "cccd": re.compile(r"\b\d{12}\b"),
}


def redact_text(text: str) -> tuple[str, dict[str, int], bool]:
    """Ẩn danh PII dạng chuẩn. Trả về (văn bản đã ẩn, bộ đếm, cờ cần người rà soát)."""
    text = unicodedata.normalize("NFC", text)  # chuẩn hoá tiếng Việt
    counts: dict[str, int] = {}
    redacted = text
    for pii_type, pattern in PATTERNS.items():
        counts[pii_type] = len(pattern.findall(redacted))
        redacted = pattern.sub(f"[REDACTED_{pii_type.upper()}]", redacted)

    # Phát hiện sơ bộ dấu hiệu injection (sẽ được Antigravity nâng cấp ở Part C)
    needs_human_review = any(
        sign in redacted.lower()
        for sign in ["bỏ qua toàn bộ", "chế độ gỡ lỗi", "in lại nguyên văn"]
    )
    return redacted, counts, needs_human_review


def write_log(log_path: Path, input_file: Path, counts: dict[str, int], flag: bool) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["run_id", "input_file", "pii_count", "needs_human_review", "created_at"],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "input_file": input_file.name,
                "pii_count": sum(counts.values()),
                "needs_human_review": str(flag).lower(),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )


def main() -> None:
    # Đường dẫn động: chạy được từ bất kỳ thư mục nào
    here = Path(__file__).resolve().parent
    base = here.parent if here.name == "scripts" else here.parent / "templates"
    base = base if (base / "synthetic-data").exists() else here.parent.parent

    input_path = base / "synthetic-data/vp-vtn-ban-giao-ca.txt"
    output_path = base / "outputs/vp-vtn-ban-giao-ca-redacted.txt"
    log_path = base / "outputs/execution-log.csv"

    if not input_path.exists():
        print(f"Không tìm thấy tệp đầu vào: {input_path}")
        return

    text = input_path.read_text(encoding="utf-8")
    redacted, counts, flag = redact_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(redacted, encoding="utf-8")
    write_log(log_path, input_path, counts, flag)
    print(f"Đã ẩn {sum(counts.values())} mục. Cờ cần người rà soát = {flag}")


if __name__ == "__main__":
    main()
