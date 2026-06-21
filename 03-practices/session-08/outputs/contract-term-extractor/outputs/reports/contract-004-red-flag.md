# Báo cáo cờ đỏ: HD-TD-2026-004

**Ngày tạo:** 2026-06-12 14:15
**Confidence:** 0.75
**Tuyến:** HITL

## Cờ đỏ phát hiện

1. Phạt không giới hạn: không có mức tối đa cho phạt vi phạm RTO (50.000.000 VNĐ/giờ)
2. Giới hạn trách nhiệm quá thấp: chỉ bằng 3 tháng giá trị hợp đồng (25% giá trị hợp đồng năm)
3. Điều khoản bất lợi ẩn: phạt vi phạm RTO không giới hạn có thể dễ dàng vượt quá giới hạn trách nhiệm bồi thường (1.200.000.000 VNĐ)

## Nguồn dẫn

- **penalty_clause** (ĐIỀU 5: ĐIỀU KHOẢN PHẠT): "Nếu Bên B không đạt SLA uptime 99.99% trong một tháng:
- Phạt 0.1% giá trị hợp đồng hàng tháng cho mỗi phút ngừng dịch vụ vượt quá mức cho phép.
- Mức cho phép: 4.38 phút/tháng (= 52.56 phút/năm ÷ 12).
- Tối đa phạt không quá 25% giá trị hợp đồng hàng tháng.
Nếu Bên B không khôi phục sự cố trong RTO 4 giờ:
- Phạt thêm 50.000.000 VNĐ cho mỗi giờ vượt RTO.
- Không giới hạn mức phạt RTO."
- **auto_renewal** (ĐIỀU 3: THỜI HẠN HỢP ĐỒNG): "Tự động gia hạn thêm 12 tháng trừ khi một bên thông báo bằng văn bản trước 90 ngày."
- **liability_cap** (ĐIỀU 8: BẢO HIỂM VÀ BỒI THƯỜNG): "Tổng trách nhiệm bồi thường của Bên B không vượt quá giá trị hợp đồng của 03 tháng."

## Đề xuất hành động

- needs_human_review=true
- 3 cờ đỏ: Phạt không giới hạn: không có mức tối đa cho phạt vi phạm RTO (50.000.000 VNĐ/giờ); Giới hạn trách nhiệm quá thấp: chỉ bằng 3 tháng giá trị hợp đồng (25% giá trị hợp đồng năm); Điều khoản bất lợi ẩn: phạt vi phạm RTO không giới hạn có thể dễ dàng vượt quá giới hạn trách nhiệm bồi thường (1.200.000.000 VNĐ)
- Chuyển người rà soát. Đính kèm báo cáo cờ đỏ và danh sách trường thiếu.