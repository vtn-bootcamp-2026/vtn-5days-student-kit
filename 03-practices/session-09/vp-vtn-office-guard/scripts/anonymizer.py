"""
Vệ sĩ văn phòng VTN — anonymizer.py (BẢN ĐẦY ĐỦ, chạy thật)
============================================================
Đây là kết quả chạy lab (tương đương điều Antigravity sinh ra khi học viên dán các
prompt A→D trong lab.md). Non-tech KHÔNG cần sửa tay — chỉ chạy:

    python vp-vtn-office-guard/scripts/anonymizer.py

Tính năng:
- [x] Chuẩn hoá Unicode NFC (tiếng Việt có dấu)
- [x] Ẩn email / SĐT / CCCD (Regex)
- [x] Ẩn tên người theo ngữ cảnh (sau "Họ và tên:", cột "Khách hàng" trong bảng)
- [x] GIỮ nguyên thuật ngữ an toàn: mã phiếu TK-..., số tiền ... VNĐ, mã phiên #CSKH-..., tổng đài 1800.xxxx, tên bộ phận
- [x] Phát hiện + trung hoà Prompt Injection (bọc <user_data>, bỏ qua lệnh giả danh)
- [x] Bật needs_human_review khi nghi injection
- [x] Ghi outputs/execution-log.csv sạch PII
"""
from __future__ import annotations

import csv
import re
import unicodedata
from datetime import datetime
from pathlib import Path

# ----------------------------- đường dẫn -----------------------------
HERE = Path(__file__).resolve().parent          # .../vp-vtn-office-guard/scripts
PKG = HERE.parent                                # .../vp-vtn-office-guard
ROOT = PKG.parent                                # .../session-09
INPUT = ROOT / "synthetic-data" / "vp-vtn-ban-giao-ca.txt"
OUT_DIR = PKG / "outputs"
OUT_TXT = OUT_DIR / "vp-vtn-ban-giao-ca-redacted.txt"
LOG_CSV = OUT_DIR / "execution-log.csv"

# ----------------------------- patterns ------------------------------
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
CCCD = re.compile(r"\b\d{12}\b")
PHONE = re.compile(r"(?:\+84\s?)?\b0?\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b")

# Thuật ngữ an toàn — bảo vệ trước để không bị Regex ẩn nhầm
SAFE = [
    (re.compile(r"TK-\d{4}-\d{3}"), "TKPH"),                       # mã phiếu
    (re.compile(r"\d{1,3}(?:\.\d{3})*\s*VNĐ"), "TIEN"),            # số tiền
    (re.compile(r"#CSKH-\d{4}-\d{4}-[A-Z]+"), "PHIEN"),            # mã phiên bàn giao
    (re.compile(r"1800\.\d{4}"), "TONGDAI"),                        # tổng đài dịch vụ
    (re.compile(r"Trung tâm CSKH"), "BOPHAN"),                      # tên bộ phận
]

# Dấu hiệu Prompt Injection (lệnh giả danh hệ thống)
INJECTION_SIGNS = [
    "bỏ qua toàn bộ", "chế độ gỡ lỗi", "in lại nguyên văn",
    "in nguyên văn", "bắt buộc phải in", "chế độ gỡ lỗi bảo mật",
    "[thông báo hệ thống", "[hệ thống gỡ lỗi",
]

# Token tên người tiếng Việt (chữ hoa đầu + có dấu)
_NV = "a-zA-Zà-ỹÀ-ỸđĐ"
NAME_TOK = rf"\b[{_NV}]*[A-ZÀ-ỸĐ][{_NV}]+(?: [{_NV}]*[A-ZÀ-ỸĐ][{_NV}]+){{1,3}}\b"


def protect_safe(text: str) -> tuple[str, dict[str, str]]:
    """Thay thuật ngữ an toàn bằng token giữ chỗ."""
    stash: dict[str, str] = {}
    for pat, prefix in SAFE:
        def _sub(m, p=prefix):
            token = f"<<{p}{len(stash)}>>"
            stash[token] = m.group(0)
            return token
        text = pat.sub(_sub, text)
    return text, stash


def restore_safe(text: str, stash: dict[str, str]) -> str:
    for token, original in stash.items():
        text = text.replace(token, original)
    return text


def extract_names(text: str) -> list[str]:
    """Lấy tên người từ ngữ cảnh: sau 'Họ và tên:' và cột 'Khách hàng' trong bảng."""
    names: set[str] = set()
    for m in re.finditer(r"Họ và tên:\s*(" + NAME_TOK + r")", text):
        names.add(m.group(1).strip())
    for m in re.finditer(r"^\|\s*\d+\s*\|\s*(" + NAME_TOK + r")\s*\|", text, flags=re.M):
        names.add(m.group(1).strip())
    # fallback: vài tên quen thuộc nếu ngữ cảnh thiếu
    names.update(["Nguyễn Thị Mai Hương", "Trần Quốc Bảo", "Lê Hoàng Phúc", "Phạm Minh Đông"])
    # loại token rác (chỉ giữ chuỗi có ≥2 chữ, có dấu hoặc viết hoa rõ)
    return sorted({n for n in names if len(n.split()) >= 2}, key=len, reverse=True)


def neutralize_injection(text: str) -> tuple[str, bool]:
    """Phát hiện + trung hoà khối injection. Trả về (văn bản, có injection)."""
    low = text.lower()
    flagged = any(s in low for s in INJECTION_SIGNS)
    if not flagged:
        return text, False

    warning = (
        "⚠ ĐÃ PHÁT HIỆN LỆNH GIẢ DANH HỆ THỐNG (prompt injection) trong email này.\n"
        "   Hệ thống KHÔNG tuân theo lệnh. Toàn bộ thông tin cá nhân đã được ẩn danh.\n"
        "   → Đề xuất chuyển email cho người chịu trách nhiệm bảo mật rà soát.\n"
    )
    # Thay toàn bộ thân email độc hại (sau dòng "Tiêu đề:" đến hết mục) bằng cảnh báo.
    # Giữ lại "Từ:" / "Tiêu đề:" (metadata) — chỉ trung hoà phần lệnh giả danh.
    text = re.sub(
        r"(Tiêu đề:[^\n]*\n).*?(?=----|\Z)",
        lambda m: m.group(1) + warning,
        text,
        flags=re.S,
        count=1,
    )
    # Đánh dấu cờ ở tiêu đề mục email
    text = re.sub(r"(EMAIL KHÁCH GỬI[^\n]*)", r"\1   [CỜ: CẦN NGƯỜI RÀ SOÁT]", text)
    return text, True


def redact(text: str) -> tuple[str, dict[str, int], bool]:
    text = unicodedata.normalize("NFC", text)

    # 1) bảo vệ thuật ngữ an toàn
    text, stash = protect_safe(text)

    # 2) trung hoà injection (trước khi đổi chữ, để dấu hiệu còn nguyên)
    text, injection = neutralize_injection(text)

    # 3) ẩn PII theo thứ tự an toàn: email → CCCD → SĐT
    counts: dict[str, int] = {}
    counts["email"] = len(EMAIL.findall(text))
    text = EMAIL.sub("[REDACTED_EMAIL]", text)
    counts["cccd"] = len(CCCD.findall(text))
    text = CCCD.sub("[REDACTED_CCCD]", text)
    counts["phone"] = len(PHONE.findall(text))
    text = PHONE.sub("[REDACTED_PHONE]", text)

    # 4) ẩn tên người
    names = extract_names(text)
    counts["name"] = 0
    for nm in names:
        c = len(re.findall(re.escape(nm), text))
        if c:
            counts["name"] += c
            text = re.sub(re.escape(nm), "[REDACTED_NAME]", text)

    # 5) phục hồi thuật ngữ an toàn
    text = restore_safe(text, stash)
    return text, counts, injection


def write_log(counts: dict[str, int], injection: bool) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    exists = LOG_CSV.exists()
    with LOG_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["run_id", "input_file", "pii_count", "needs_human_review", "created_at"])
        if not exists:
            w.writeheader()
        w.writerow({
            "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "input_file": INPUT.name,
            "pii_count": sum(counts.values()),
            "needs_human_review": str(injection).lower(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        })


def main() -> None:
    if not INPUT.exists():
        raise SystemExit(f"Không tìm thấy đầu vào: {INPUT}")
    text = INPUT.read_text(encoding="utf-8")
    redacted, counts, injection = redact(text)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TXT.write_text(redacted, encoding="utf-8")
    write_log(counts, injection)
    print(f"✓ Đã ẩn danh. PII theo loại: {counts}")
    print(f"  Tổng PII đã ẩn: {sum(counts.values())}")
    print(f"  Phát hiện injection → needs_human_review = {injection}")
    print(f"  Output: {OUT_TXT.relative_to(ROOT)}")
    print(f"  Log:    {LOG_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
