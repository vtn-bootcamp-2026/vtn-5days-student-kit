---
mo-ta: Lời nhắc gợi ý cách thực hiện bài tập nâng cao (BT4) mở rộng luật cờ đỏ và che dữ liệu cá nhân (PII)
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 22:45 +07:00
updated-at: 2026-06-23 22:45 +07:00
---

# Lời nhắc hỗ trợ bài tập nâng cao (BT4)

Bài tập 4 yêu cầu mở rộng bộ thư viện cờ đỏ và xây dựng script `condact_pii.py` để che thông tin nhạy cảm. Bạn có thể sử dụng các gợi ý prompt sau đây để nhờ Agent hỗ trợ hoàn thành.

## 1. Lời nhắc viết kịch bản che thông tin cá nhân (`condact_pii.py`)

Hãy dán nội dung này vào ô chat của Agent để sinh mã nguồn Python tự động che PII bằng RegEx hoặc thuật toán đơn giản trước khi gửi văn bản tới LLM:

```text
Hãy viết script Python `review-contract/scripts/condact_pii.py` nhận vào chuỗi text của hợp đồng và che (mask) các thông tin nhạy cảm sau đây:
- Tên người (ví dụ: Nguyễn Văn A) -> `[PERSON]`
- Số điện thoại/Email -> `[CONTACT]`
- Mã số thuế / Số CCCD -> `[TAX_ID]`
- Số tài khoản ngân hàng -> `[BANK_ACCT]`

Script cần có hàm `condact_text(text: str) -> str` trả về văn bản đã che thông tin. Hãy viết mã nguồn thật đơn giản và sạch sẽ, không dùng thư viện bên ngoài nặng nề.
```

## 2. Lời nhắc tích hợp bước che thông tin PII vào quy trình (workflow)

Sau khi có script `condact_pii.py`, bạn có thể yêu cầu Agent tích hợp nó vào `intake.py` và cập nhật chỉ dẫn trong `SKILL.md`:

```text
Hãy cập nhật script `review-contract/scripts/intake.py` để gọi hàm `condact_text` từ `condact_pii.py` ngay sau khi đọc được nội dung hợp đồng và trước khi chuyển qua bước Extract. Đồng thời cập nhật mô tả quy trình Process trong file `review-contract/SKILL.md` để ghi nhận bước che thông tin (PII Redaction/Condacting) này.
```
