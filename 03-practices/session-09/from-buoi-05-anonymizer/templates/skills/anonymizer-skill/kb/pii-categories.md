---
mo-ta: "Danh muc cac loai PII can che giau trong tai lieu VTN"
trang-thai: active
phien-ban: v1.0
created-at: "2026-05-27 10:00 +07:00"
updated-at: "2026-05-27 10:00 +07:00"
---

# PII Categories — Phân loại thông tin cần che giấu

## 1. Căn cước công dân (CCCD)
- **Định dạng**: 12 chữ số liên tiếp
- **Ví dụ**: `079123456789`
- **Placeholder**: `[REDACTED_CCCD]`
- **Lưu ý**: Kiểm tra `safe-terms.md` trước khi che — số serial thiết bị cũng có 12 chữ số

## 2. Số điện thoại
- **Di động Việt Nam**: 10 chữ số, bắt đầu bằng `0` + mã mạng (3x, 5x, 7x, 8x, 9x)
  - Ví dụ: `0982123456`, `0361234567`
- **Định dạng quốc tế**: `+84` + 9-10 chữ số
  - Ví dụ: `+84 982-123-456`
- **Số bàn**: Mã vùng 3 chữ số + 7-8 chữ số
  - Ví dụ: `024.3123.4567`, `028-3823-4567`
- **Placeholder**: `[REDACTED_PHONE]`
- **Lưu ý**: Số SCADA dạng `x.xxx.xxx.xxx` có thể bị nhận nhầm → kiểm tra `safe-terms.md`

## 3. Địa chỉ email
- **Định dạng**: `username@domain`
- **Ví dụ**: `nguyenvts@viettel.com.vn`
- **Placeholder**: `[REDACTED_EMAIL]`
- **Lưu ý**: Email tổ chức/kỹ thuật (vd: `anhvan-support@viettel.com.vn`) → kiểm tra ngữ cảnh, không che nhầm

## 4. Địa chỉ IP
- **IPv4**: 4 cụm số 1-3 chữ số cách nhau bằng dấu chấm
- **Ví dụ**: `203.162.4.1`
- **Placeholder**: `[REDACTED_IP]`
- **Lưu ý**: IP nội bộ (10.x, 172.16-31.x, 192.168.x) → kiểm tra chính sách, có thể không cần che

## 5. Họ tên người
- **Định dạng**: Tiếng Việt có dấu, 2-5 chữ
- **Ví dụ**: `Nguyễn Trần Khánh Lâm`, `Lê Hoàng Phương Vy`
- **Placeholder**: `[REDACTED_NAME]`
- **Lưu ý**:
  - Kiểm tra Unicode NFC/NFD trước khi so khớp
  - Tên doanh nghiệp, tên phòng ban, tên tổ → kiểm tra `safe-terms.md`
  - "Viễn thông Hoàng Long" → tên doanh nghiệp, KHÔNG phải tên người

## 6. Địa chỉ
- **Định dạng**: Số nhà + tên đường/phường/quận/tỉnh
- **Ví dụ**: `123 Nguyễn Văn Linh, Quận 7, TP.HCM`
- **Placeholder**: `[REDACTED_ADDRESS]`

## 7. Thông tin khác
- Mã số thuế, số tài khoản ngân hàng, số hộ chiếu → che giấu nếu phát hiện
- **Placeholder**: `[REDACTED_OTHER]`
