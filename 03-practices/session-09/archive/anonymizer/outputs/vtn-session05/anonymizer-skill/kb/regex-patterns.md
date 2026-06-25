---
mo-ta: "Bo mau Regex cho viec phat hien PII tieng Viet"
trang-thai: active
phien-ban: v1.0
created-at: "2026-05-27 10:00 +07:00"
updated-at: "2026-05-27 10:00 +07:00"
---

# Regex Patterns — Mẫu biểu thức chính quy phát hiện PII

> **Nguyên tắc**: Regex là tầng lọc đầu tiên (nhanh, tĩnh). Kết quả phải được LLM xác minh ở tầng 2 (ngữ cảnh).
> **Unicode**: Tất cả chuỗi đầu vào phải được chuẩn hóa NFC trước khi áp dụng Regex.

## 1. CCCD (Căn cước công dân)

```python
# CCCD: chính xác 12 chữ số liên tiếp
# Lưu ý: có thể trùng với serial thiết bị → kiểm tra safe-terms.md
pattern_cccd = r'\b\d{12}\b'
```

## 2. Số điện thoại di động

```python
# SĐT di động: 10 chữ số, bắt đầu bằng 03x, 05x, 07x, 08x, 09x
pattern_phone_mobile = r'\b(03|05|07|08|09)\d{8}\b'

# SĐT định dạng quốc tế: +84 + 9-10 chữ số (có thể chứa dấu gạch ngang, khoảng trắng)
pattern_phone_intl = r'\+84[\s\-]?\d[\s\-]?\d{2,3}[\s\-]?\d{3}[\s\-]?\d{2,3}'
```

## 3. Số điện thoại bàn

```python
# SĐT bàn: mã vùng 3 chữ số + 7-8 chữ số (có thể chứa dấu chấm, gạch ngang)
pattern_phone_landline = r'\b(02[0-9])[\.\-\s]?\d{3,4}[\.\-\s]?\d{3,4}\b'
```

## 4. Email

```python
pattern_email = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
```

## 5. Địa chỉ IP

```python
pattern_ip = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
```

## 6. Tên người tiếng Việt

```python
# Regex tên tiếng Việt có dấu — kết hợp Unicode NFC
# Pattern cơ bản: 2-5 từ có dấu tiếng Việt, viết hoa chữ cái đầu
# Lưu ý: cần LLM xác minh ngữ cảnh (tên người vs tên doanh nghiệp)
import re

# Danh sách họ Việt phổ biến (sử dụng để tăng độ chính xác)
common_surnames = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan',
                   'Vũ', 'Võ', 'Đặng', 'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý']

# Tên người: họ + 1-4 từ có dấu tiếng Việt
# Chỉ dùng làm gợi ý cho LLM, KHÔNG dùng Regex đơn thuần để quyết định
```

## Quy tắc sử dụng

1. **Luôn chuẩn hóa NFC** trước khi áp dụng Regex
2. **Luôn kiểm tra safe-terms.md** sau khi Regex tìm thấy — loại trừ false positive
3. **Luôn gửi kết quả Regex qua LLM** để xác minh ngữ cảnh
4. **Fallback**: Khi LLM không khả dụng → chỉ dùng Regex + bật `needs_human_review`
