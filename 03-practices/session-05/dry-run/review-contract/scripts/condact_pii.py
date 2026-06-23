#!/usr/bin/env python3
"""Condact PII: mask thông tin cá nhân TRƯỚC khi đưa qua AI. (BT4)
Pattern đích — tránh khớp trong từ thông thường."""
import re, argparse

# 1. Mã số thuế: "Mã số thuế: 0301234567-001"
TAX = re.compile(r'(Mã\s+số\s+thuế:\s*)[\d\-]+', re.I)
# 2. SĐT: số đứng riêng, 10-11 chữ số bắt đầu 0 (có thể có dấu chấm/dấu cách)
PHONE = re.compile(r'(?<![\d])(0\d{3}[\.\s]?\d{3}[\.\s]?\d{3,4})(?![\d])')
# 3. Email
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
# 4. Tên người (danh sách cụ thể, ranh giới từ)
NAMES = ["Hoàng Văn Em", "Võ Thị Phúc", "Nguyễn Văn A", "Trần Thị B", "Lê Minh C"]

def condact(text):
    text = TAX.sub(r'\1[TAX_ID]', text)
    text = PHONE.sub('[PHONE]', text)
    text = EMAIL.sub('[EMAIL]', text)
    for name in NAMES:
        text = re.sub(r'(?<![A-ZÀ-Ỹa-zà-ỹ])' + re.escape(name) + r'(?![A-ZÀ-Ỹa-zà-ỹ])', '[PERSON]', text)
    return text

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    src = open(a.file, encoding="utf-8").read()
    out = condact(src)
    (open(a.out, "w", encoding="utf-8").write(out) if a.out else print(out))
