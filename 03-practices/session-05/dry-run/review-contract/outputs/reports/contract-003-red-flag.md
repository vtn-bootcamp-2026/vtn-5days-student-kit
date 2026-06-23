# Báo cáo cờ đỏ: contract-003-risky

**Ngày tạo:** 2026-06-12 13:50
**Confidence:** 0.65
**Tuyến:** HITL

## Cờ đỏ phát hiện

1. Tự gia hạn bất lợi: chỉ cần thông báo 15 ngày trước
2. Phạt không giới hạn: không có mức tối đa
3. Giới hạn trách nhiệm quá thấp: chỉ bằng 1 tháng giá trị
4. Mâu thuẫn giữa điều khoản chấm dứt và tự gia hạn

## Nguồn dẫn

- **penalty_clause** (Điều 4): "Không giới hạn mức phạt tối đa"
- **red_flag_auto_renew** (Điều 2): "tự động gia hạn thêm 12 tháng...chấm dứt trước 15 ngày"

## Đề xuất hành động

- needs_human_review=true
- 4 cờ đỏ: Tự gia hạn bất lợi: chỉ cần thông báo 15 ngày trước; Phạt không giới hạn: không có mức tối đa; Giới hạn trách nhiệm quá thấp: chỉ bằng 1 tháng giá trị
- Confidence thấp: 0.65
- Chuyển người rà soát. Đính kèm báo cáo cờ đỏ và danh sách trường thiếu.