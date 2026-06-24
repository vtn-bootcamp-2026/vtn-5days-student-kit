#!/usr/bin/env python3
"""
CV Screening Skill — PII Redaction Tool
Tự động che (mask) các thông tin cá nhân và nhạy cảm (PII) khỏi văn bản.
"""

import re

# Bảng chữ cái tiếng Việt hoa và thường đầy đủ để hỗ trợ regex tiếng Việt không dấu và có dấu
VNM_UPPER = "A-ZÀÁẢẠÃĂẰẮẲẶẴÂẦẤẨẬẪEÈÉẺẸẼÊỀẾỂỆỄIÌÍỈỊĨOÒÓỎỌÕÔỒỔỘỐỖƠỜỚỞỢỠUÙÚỦỤŨƯỪỨỬỰỮYỲÝỶỴỸDĐ"
VNM_LOWER = "a-zàáảạãăằắẳặẵâầấẩậẫeèéẻẹẽêềểệễiìỉịĩoòỏọõôồổộỗơờởợớỡuùúủụũưừứửựữyỳỷỵỹdđ"

# Khớp một từ tiếng Việt viết hoa chữ cái đầu (ví dụ: Nguyễn, Văn, A)
VNM_WORD = f"[{VNM_UPPER}][{VNM_LOWER}]*"

# Khớp tên người (gồm 2 đến 5 từ viết hoa chữ cái đầu, chỉ trên cùng một dòng)
VNM_NAME_PAT = f"{VNM_WORD}(?:[ \\t]+{VNM_WORD}){{1,4}}"


def condact_text(text: str) -> str:
    """
    Nhận vào chuỗi văn bản (CV) và che các thông tin nhạy cảm:
    - Tên người -> [PERSON]
    - Số điện thoại/Email -> [CONTACT]
    - Mã số thuế / Số CCCD -> [TAX_ID]
    - Số tài khoản ngân hàng -> [BANK_ACCT]
    """
    if not text:
        return text

    # 1. Tìm và che tên ứng viên chính (qua các nhãn Họ và tên, Tên, v.v. trên cùng một dòng)
    candidate_name = None
    candidate_keywords = [
        r'(?i)(?:họ[ \t]*(?:và|&)?[ \t]*tên|tên(?:[ \t]*ứng[ \t]*viên)?|name|full[ \t]*name|ứng[ \t]*viên)[ \t]*[:\-\* \t]+(' + VNM_NAME_PAT + ')'
    ]
    for pat in candidate_keywords:
        match = re.search(pat, text)
        if match:
            candidate_name = match.group(1).strip()
            break

    if candidate_name:
        # Thay thế tất cả các lần xuất hiện của tên ứng viên này trong văn bản
        text = text.replace(candidate_name, "[PERSON]")

    # 2. Tìm và che tên những người khác (người tham chiếu, liên hệ... trên cùng một dòng)
    other_name_pats = [
        r'(?i)(?:người[ \t]*tham[ \t]*chiếu|người[ \t]*liên[ \t]*hệ|người[ \t]*đại[ \t]*diện|reference|contact[ \t]*person)[ \t]*[:\-\* \t]+(' + VNM_NAME_PAT + ')'
    ]
    for pat in other_name_pats:
        def replace_other_name(m):
            matched_full = m.group(0)
            name_part = m.group(1)
            return matched_full.replace(name_part, "[PERSON]")
        text = re.sub(pat, replace_other_name, text)

    # 3. Che Email & Số điện thoại -> [CONTACT]
    # Email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = re.sub(email_pattern, "[CONTACT]", text)

    # Số điện thoại di động và cố định Việt Nam (chấp nhận khoảng trắng ngang, gạch ngang, dấu chấm)
    phone_pattern = r'\b(?:\+?84|0)[ \t]*[235789](?:[ \t\.\-]?\d){8,9}\b'
    text = re.sub(phone_pattern, "[CONTACT]", text)

    # 4. Che số tài khoản ngân hàng -> [BANK_ACCT]
    # Nhận diện số tài khoản ngân hàng đi sau từ khóa liên quan
    bank_pattern = r'(?i)(?:số[ \t]*tài[ \t]*khoản|stk|số[ \t]*tk|tài[ \t]*khoản(?:[ \t]*ngân[ \t]*hàng)?|bank[ \t]*account|account[ \t]*number)[ \t]*[:\-\* \t]+([0-9]+(?:[ \t\.\-]*[0-9]+)*)\b'
    def replace_bank(m):
        matched_full = m.group(0)
        bank_part = m.group(1)
        # Chỉ che nếu độ dài chuỗi số (lược bỏ ký tự không phải số) nằm trong khoảng từ 8 đến 16
        digits_only = re.sub(r'\D', '', bank_part)
        if 8 <= len(digits_only) <= 16:
            return matched_full.replace(bank_part, "[BANK_ACCT]")
        return matched_full
    text = re.sub(bank_pattern, replace_bank, text)

    # 5. Che Mã số thuế & CCCD / CMND -> [TAX_ID]
    # Khớp MST chi nhánh (10 số - 3 số), CCCD (12 số), MST (10 số), CMND (9 số)
    tax_pattern = r'\b\d{10}-\d{3}\b|\b\d{12}\b|\b\d{10}\b|\b\d{9}\b'
    text = re.sub(tax_pattern, "[TAX_ID]", text)

    return text


if __name__ == "__main__":
    # Test nhanh chức năng che PII
    sample_text = """
    HỌ VÀ TÊN: Nguyễn Văn A
    Số điện thoại: 090 123 4567 hoặc +84901234567
    Email: nguyen.van.a@example.com
    Số CMND: 123456789
    Số CCCD: 012345678901
    Mã số thuế: 0102030405
    Người đại diện: Trần Thị B
    Số tài khoản: 1902 3456 7890 12 tại ngân hàng Techcombank.
    Năm làm việc: 2020-2023. Kỹ năng: Python.
    """
    print("--- Văn bản gốc ---")
    print(sample_text)
    print("--- Văn bản đã che PII ---")
    print(condact_text(sample_text))
