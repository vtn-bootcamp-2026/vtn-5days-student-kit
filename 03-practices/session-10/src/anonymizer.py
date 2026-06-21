import re
import json
from pathlib import Path

# Regex cho các loại PII chuẩn
PATTERNS = {
    'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'),
    'phone': re.compile(r'\b(?:\+84\s?|0)\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b'),
    'cccd': re.compile(r'\b\d{12}\b'),

    # Ngày sinh: các định dạng phổ biến DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
    'dob': re.compile(
        r'\b(?:(?:0?[1-9]|[12]\d|3[01])[/\-.](?:0?[1-9]|1[0-2])[/\-.][12]\d{3}'
        r'|[12]\d{3}[/\-.](?:0?[1-9]|1[0-2])[/\-.](?:0?[1-9]|[12]\d|3[01]))\b'
    ),

    # Số tài khoản ngân hàng Việt Nam: 9–19 chữ số liên tiếp
    # (loại trừ các số bắt đầu bằng đầu số di động 03/05/07/08/09 có độ dài 12-13 số để tránh nhận nhầm SĐT lỗi)
    'bank_account': re.compile(r'\b(?!0[35789]\d{10,11}\b)\d{9,19}\b'),

    # Địa chỉ nhà: nhận diện cụm bắt đầu bằng số + tên đường / phố / hẻm / ngõ
    # hoặc có từ khoá phường/xã/quận/huyện/tỉnh/thành phố
    'address': re.compile(
        r'\b\d{1,4}[/\-]?[A-Za-zÀ-ỹ\d\s,./]*?'
        r'(?:đường|phố|phường|xã|quận|huyện|thị trấn|thị xã|tỉnh|thành phố|TP\.?|Q\.?|P\.?|hẻm|ngõ|ngách|lô|khu)'
        r'[A-Za-zÀ-ỹ\d\s,./]{0,80}',
        re.IGNORECASE | re.UNICODE,
    ),
}

def anonymize_text(text: str) -> str:
    if not text:
        return ''
    result = text
    # Ẩn Email
    result = PATTERNS['email'].sub('[REDACTED_EMAIL]', result)
    # Ẩn Số điện thoại
    result = PATTERNS['phone'].sub('[REDACTED_PHONE]', result)
    # Ẩn Ngày sinh (trước CCCD/bank để tránh khớp nhầm chuỗi số)
    result = PATTERNS['dob'].sub('[REDACTED_DOB]', result)
    # Ẩn CCCD
    result = PATTERNS['cccd'].sub('[REDACTED_CCCD]', result)
    # Ẩn Số tài khoản ngân hàng
    result = PATTERNS['bank_account'].sub('[REDACTED_BANK_ACCOUNT]', result)
    # Ẩn Địa chỉ nhà
    result = PATTERNS['address'].sub('[REDACTED_ADDRESS]', result)
    return result
