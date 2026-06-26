# Phân loại thông tin cá nhân (PII) cần ẩn

> "Vệ sĩ văn phòng VTN" chỉ ẩn các loại thông tin CÁ NHÂN dưới đây.
> Mọi thứ khác (mã phiếu, số tiền, tên bộ phận) xem `safe-terms.md`.

| Loại | Nhãn thay thế | Ví dụ |
|------|---------------|-------|
| Họ tên người | `[REDACTED_NAME]` | Nguyễn Thị Mai Hương, Trần Quốc Bảo |
| Email | `[REDACTED_EMAIL]` | maihuong.nguyen@viettel.vn |
| Số điện thoại | `[REDACTED_PHONE]` | 0912.345.678, 0987 654 321 |
| Số CCCD | `[REDACTED_CCCD]` | 079012345678 (12 chữ số) |

## Dấu hiệu để nhận diện tên người (không phải code — để Antigravity dùng)
- 2–4 âm tiết tiếng Việt có dấu, đứng cạnh "Họ và tên", "Khách hàng", "Nhân viên".
- KHÔNG phải tên bộ phận (xem `safe-terms.md`).
- Khi phân vân → giữ nguyên + bật cờ rà soát, KHÔNG đoán bừa.
