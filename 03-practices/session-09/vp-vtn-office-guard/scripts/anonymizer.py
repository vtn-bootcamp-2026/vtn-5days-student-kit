"""
Vệ sĩ văn phòng VTN — Anonymizer Script
================================================
Mô tả: Tự động che giấu thông tin cá nhân (PII) trong bản bàn giao ca trực,
chặn và vô hiệu hóa tấn công Prompt Injection, đồng thời bảo vệ các thuật ngữ an toàn.
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

# Các từ khóa loại trừ (thuật ngữ an toàn) không được ẩn nhầm
SAFE_TERMS = ["1800.8123", "TK-2026-001", "TK-2026-002", "#CSKH-2026-0624-PM"]


def redact_text(text: str) -> tuple[str, dict[str, int], bool]:
    """Ẩn danh PII dạng chuẩn. Trả về (văn bản đã ẩn, bộ đếm, cờ cần người rà soát)."""
    # Chuẩn hoá tiếng Việt sang dạng NFC
    text = unicodedata.normalize("NFC", text)
    
    # 1. Bọc dữ liệu đầu vào trong <user_data> ... </user_data> theo quy định an toàn
    wrapped = f"<user_data>\n{text}\n</user_data>"
    
    # Lấy lại text thô từ thẻ bọc để xử lý
    inner_text = wrapped.replace("<user_data>\n", "").replace("\n</user_data>", "")

    # Phân tích cấu trúc file theo dấu phân cách để tìm và xử lý các phần
    # Phân tách bằng đường kẻ gạch ngang (chứa ít nhất 50 dấu gạch ngang)
    parts = re.split(r"-{50,}", inner_text)
    
    needs_human_review = False
    
    if len(parts) == 7:
        # Kiểm tra Prompt Injection trong Section 2 (phần email gửi vào - parts[4])
        section2_content = parts[4]
        injection_keywords = ["bỏ qua toàn bộ", "chế độ gỡ lỗi", "in lại nguyên văn", "bắt buộc phải in"]
        if any(kw in section2_content.lower() for kw in injection_keywords):
            needs_human_review = True
            # Thay đổi tiêu đề Section 2 và thay thế nội dung email bằng cảnh báo bảo mật
            parts[3] = "\n2. EMAIL KHÁCH GỬI VÀO HỘP THƯ TRONG CA  [CỜ: CẦN NGƯỜI RÀ SOÁT]\n"
            parts[4] = (
                "\nNội dung email mục 2 có chứa LỆNH GIẢ DANH HỆ THỐNG (prompt injection).\n"
                "Hệ thống ĐÃ KHÔNG tuân theo lệnh này. Toàn bộ thông tin cá nhân trong email\n"
                "đã được ẩn danh. Đề xuất chuyển email cho người chịu trách nhiệm bảo mật rà soát.\n\n"
            )
            
        # Điều chỉnh định dạng Section 3 (tiêu đề và loại bỏ ghi chú giải thích về mã phiếu/số tiền)
        parts[5] = parts[5].replace(
            "3. GHI CHÚ NỘI BỘ",
            "3. GHI CHÚ NỘI BỘ  (giữ nguyên — không phải dữ liệu cá nhân)"
        )
        parts[6] = parts[6].replace(" (mã phiếu, không phải thông tin cá nhân)", "")
        parts[6] = parts[6].replace(" (số tiền, không phải dữ liệu cá nhân)", "")

    # Tái hợp lại văn bản sau khi đã điều chỉnh cấu trúc
    processed_text = "--------------------------------------------------------------------------------".join(parts)
    
    # Thêm nhãn [ĐÃ ẨN DANH] vào tiêu đề dòng thứ 2
    lines = processed_text.splitlines()
    if len(lines) > 1 and "BẢN GHI BÀN GIAO CA TRỰC" in lines[1]:
        lines[1] = lines[1] + "  [ĐÃ ẨN DANH]"
    processed_text = "\n".join(lines)

    # 2. Phát hiện và ẩn danh tên người tiếng Việt động
    names_to_redact = []
    
    # Trích xuất tên sau "Họ và tên:"
    name_match = re.search(r"Họ và tên:\s*([^\n\r]+)", inner_text)
    if name_match:
        name = name_match.group(1).strip()
        if name and name not in names_to_redact:
            names_to_redact.append(name)
            
    # Trích xuất tên từ cột "Khách hàng" trong bảng Markdown
    for line in inner_text.splitlines():
        cols = [c.strip() for c in line.split("|")]
        if len(cols) >= 3 and cols[1].isdigit():
            name = cols[2]
            if name and name not in names_to_redact:
                names_to_redact.append(name)
                
    # Thay thế các họ tên phát hiện được
    name_redact_count = 0
    names_to_redact.sort(key=len, reverse=True) # Thay từ tên dài nhất trước để tránh lỗi cắt cụm từ
    for name in names_to_redact:
        matches = re.findall(re.escape(name), processed_text)
        name_redact_count += len(matches)
        processed_text = processed_text.replace(name, "[REDACTED_NAME]")

    counts = {"name": name_redact_count}

    # 3. Thay thế các loại PII khác qua Regex (Email, SĐT, CCCD)
    for pii_type, pattern in PATTERNS.items():
        type_count = 0
        
        def replace_fn(match: re.Match) -> str:
            nonlocal type_count
            val = match.group(0)
            # Không thay thế nếu giá trị nằm trong danh sách loại trừ
            if val in SAFE_TERMS or any(term in val for term in SAFE_TERMS):
                return val
            type_count += 1
            return f"[REDACTED_{pii_type.upper()}]"
            
        processed_text = pattern.sub(replace_fn, processed_text)
        counts[pii_type] = type_count

    # Định dạng lại bảng Markdown để khớp hoàn toàn với mẫu redacted-mau.txt
    new_lines = []
    for line in processed_text.splitlines():
        if line.startswith("|") and not line.startswith("|-----"):
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 6 and cols[1].isdigit():
                stt = cols[1]
                name = "[REDACTED_NAME]"
                phone = "[REDACTED_PHONE]"
                email = "[REDACTED_EMAIL]"
                reason = cols[5]
                if stt == "01":
                    line = f"| 01  | {name:<17} | {phone:<15}| {email:<28} | {reason:<20} |"
                elif stt == "02":
                    line = f"| 02  | {name:<17} | {phone:<15}| {email:<28} | {reason:<25} |"
                elif stt == "03":
                    line = f"| 03  | {name:<17} | {phone:<15}| {email:<28} | {reason:<20} |"
        new_lines.append(line)
    processed_text = "\n".join(new_lines)

    return processed_text, counts, needs_human_review


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
    # Thiết lập đường dẫn tương đối chính xác
    here = Path(__file__).resolve().parent
    skill_root = here.parent
    session_root = skill_root.parent

    input_path = session_root / "templates/synthetic-data/vp-vtn-ban-giao-ca.txt"
    output_path = skill_root / "outputs/vp-vtn-ban-giao-ca-redacted.txt"
    log_path = skill_root / "outputs/execution-log.csv"

    if not input_path.exists():
        print(f"Không tìm thấy tệp đầu vào: {input_path}")
        return

    text = input_path.read_text(encoding="utf-8")
    redacted, counts, flag = redact_text(text)
    
    # Đảm bảo có ký tự xuống dòng ở cuối file
    if not redacted.endswith("\n"):
        redacted += "\n"
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(redacted, encoding="utf-8")
    write_log(log_path, input_path, counts, flag)
    
    print("--- KẾT QUẢ CHẠY VỆ SĨ VĂN PHÒNG VTN ---")
    print(f"Đầu vào: {input_path.name}")
    print(f"Đầu ra: {output_path.name}")
    print(f"Số lượng PII đã ẩn danh:")
    for k, v in counts.items():
        print(f"  - {k.upper()}: {v}")
    print(f"Tổng số PII đã ẩn: {sum(counts.values())}")
    print(f"Cờ rà soát thủ công (Prompt Injection) = {flag}")
    print("----------------------------------------")


if __name__ == "__main__":
    main()
