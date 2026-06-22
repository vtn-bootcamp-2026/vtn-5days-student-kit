---
mo-ta: quy tac phat hien co do trong hop dong vien thong
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-27 00:50 +07:00
updated-at: 2026-05-27 00:50 +07:00
---

# Quy tắc phát hiện cờ đỏ: red-flag rules

Mỗi rule mô tả điều kiện phát hiện và hành động tương ứng.

## RF-01: Phạt vi phạm không giới hạn hoặc quá cao

**Điều kiện:**
- Điều khoản phạt không ghi mức tối đa
- Hoặc mức phạt vượt 15% tổng giá trị hợp đồng
- Hoặc phạt tính theo "mỗi giờ/mỗi ngày" mà không có ceiling

**Hành động:**
- Thêm vào `red_flags[]`: "Phạt không giới hạn: không có mức tối đa cho phạt vi phạm"
- Bật `needs_human_review = true`

## RF-02: Tự gia hạn với thời hạn thông báo quá ngắn

**Điều kiện:**
- Hợp đồng tự gia hạn
- Thời hạn thông báo chấm dứt dưới 30 ngày
- Hoặc không ghi rõ thời hạn thông báo

**Hành động:**
- Thêm vào `red_flags[]`: "Tự gia hạn bất lợi: chỉ cần thông báo {N} ngày trước, dễ lỡ thời hạn"
- Bật `needs_human_review = true`

## RF-03: Giới hạn trách nhiệm bất cân xứng

**Điều kiện:**
- Giới hạn trách nhiệm dưới 30% giá trị hợp đồng
- Hoặc giới hạn dưới 3 tháng giá trị hợp đồng
- Tính: `liability_cap / contract_value`

**Hành động:**
- Thêm vào `red_flags[]`: "Giới hạn trách nhiệm quá thấp: chỉ bằng {X} tháng giá trị hợp đồng ({Y}%)"
- Bật `needs_human_review = true`

## RF-04: Mâu thuẫn giữa điều khoản

**Điều kiện:**
- Ngày hiệu lực sau ngày hết hạn
- Điều khoản phạt trái với cam kết SLA
- Hai điều khoản mô tả cùng một nội dung nhưng khác nhau

**Hành động:**
- Thêm vào `red_flags[]`: "Mâu thuẫn: {mô tả hai điều khoản mâu thuẫn}"
- Bật `needs_human_review = true`

## RF-05: Thiếu điều khoản quan trọng

**Điều kiện:**
- Không có điều khoản chấm dứt
- Không có điều khoản bảo mật (với hợp đồng có dữ liệu khách hàng)
- Không có điều khoản phạt vi phạm
- Không có điều khoản giải quyết tranh chấp

**Hành động:**
- Thêm trường đó vào `missing_fields[]`
- Nếu thiếu từ 2 điều khoản trở lên → bật `needs_human_review = true`

## RF-06: Điều khoản bảo mật yếu

**Điều kiện:**
- Thời gian bảo mật dưới 1 năm sau khi hợp đồng hết hạn
- Phạm vi bảo mật quá hẹp (chỉ đề cập chung chung, không liệt kê)
- Không có hậu quả vi phạm bảo mật

**Hành động:**
- Thêm vào `red_flags[]`: "Điều khoản bảo mật yếu: {chi tiết}"
- Bật `needs_human_review = true`

## RF-07: Điều khoản bất lợi ẩn (phát hiện bằng đối chiếu tỷ lệ)

**Điều kiện:**
- Giới hạn trách nhiệm / giá trị hợp đồng < 0.1 (dưới 10%)
- Phạt vi phạm / giới hạn trách nhiệm > 2.0 (phạt có thể vượt bồi thường)
- Thời hạn hợp đồng > 36 tháng không có điều khoản tái đàm phán giá

**Hành động:**
- Thêm vào `red_flags[]`: "Điều khoản bất lợi ẩn: {chi tiết tỷ lệ}"
- Bật `needs_human_review = true`
