---
mo-ta: mau bo test case cho contract term extractor
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 15:00 +07:00
updated-at: 2026-05-26 15:00 +07:00
---

# Mẫu bộ test case: test cases specification

## Cấu trúc mỗi test case

| Trường | Mô tả |
| --- | --- |
| TC ID | Mã test case, ví dụ: TC-001 |
| Loại | Bình thường / Thiếu trường / Mâu thuẫn / Cờ đỏ / Lỗi OCR / False negative |
| Đầu vào | Hợp đồng dùng cho test |
| Đầu ra kỳ vọng | JSON kỳ vọng, các trường cần kiểm tra |
| Tiêu chí PASS | Điều kiện cụ thể để đánh giá PASS |
| Kết quả thực tế | Ghi sau khi chạy test |
| Trạng thái | PASS / FAIL |

## Danh sách test case bắt buộc (12 ca)

### TC-001: hợp đồng đầy đủ, bình thường (contract-001)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-001.txt |
| Đầu ra kỳ vọng | JSON đầy đủ, effective_date=2026-01-01, expiry_date=2026-12-31, needs_human_review=false |
| Tiêu chí PASS | Đúng ngày, có source_evidence cho mọi trường, confidence > 0.8 |

### TC-002: hợp đồng thiếu ngày hết hạn (contract-002)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-002.txt |
| Đầu ra kỳ vọng | expiry_date trong missing_fields[], needs_human_review=true |
| Tiêu chí PASS | Phát hiện thiếu expiry_date, bật HITL |

### TC-003: hợp đồng thiếu điều khoản bảo mật (contract-002)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-002.txt |
| Đầu ra kỳ vọng | Phát hiện Điều 5 bị lỗi OCR/thiếu, thêm vào missing_fields[] |
| Tiêu chí PASS | Phát hiện thiếu bảo mật, bật HITL |

### TC-004: phát hiện cờ đỏ — tự gia hạn bất lợi (contract-003-risky)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-003-risky.txt |
| Đầu ra kỳ vọng | red_flags[] chứa cảnh báo tự gia hạn, needs_human_review=true |
| Tiêu chí PASS | Phát hiện tự gia hạn, có source_evidence trích Điều 2 |

### TC-005: phát hiện cờ đỏ — phạt không giới hạn (contract-003-risky)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-003-risky.txt |
| Đầu ra kỳ vọng | red_flags[] chứa cảnh báo phạt không giới hạn, needs_human_review=true |
| Tiêu chí PASS | Phát hiện "không giới hạn mức phạt", có source_evidence |

### TC-006: mâu thuẫn — ngày hiệu lực trước ngày ký (nếu có)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | Hợp đồng có ngày hiệu lực trước ngày ký |
| Đầu ra kỳ vọng | red_flags[] phát hiện mâu thuẫn ngày, needs_human_review=true |
| Tiêu chí PASS | Phát hiện mâu thuẫn thời gian |

### TC-007: mâu thuẫn — điều khoản trái nhau

| Trường | Nội dung |
| --- | --- |
| Đầu vào | Hợp đồng có điều khoản chấm dứt mâu thuẫn với tự gia hạn |
| Đầu ra kỳ vọng | red_flags[] phát hiện mâu thuẫn, needs_human_review=true |
| Tiêu chí PASS | Phát hiện mâu thuẫn nội dung |

### TC-008: bình thường — trích xuất số tiền chính xác

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-001.txt |
| Đầu ra kỳ vọng | penalty_amount="1% giá trị hợp đồng hàng tháng cho mỗi 0.5% giảm hiệu suất" |
| Tiêu chí PASS | Số tiền trích chính xác, có source_evidence |

### TC-009: bình thường — confidence phản ánh đúng mức chắc chắn

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-001.txt |
| Đầu ra kỳ vọng | confidence > 0.8 vì hợp đồng đầy đủ, rõ ràng |
| Tiêu chí PASS | Confidence hợp lý, không phải 1.0 mặc định |

### TC-010: lỗi OCR — đoạn văn bản bị cắt

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-002.txt (Điều 2 và Điều 5 bị lỗi OCR) |
| Đầu ra kỳ vọng | missing_fields[] chứa các trường từ đoạn bị lỗi, needs_human_review=true |
| Tiêu chí PASS | Phát hiện đoạn lỗi OCR, không tự tạo dữ liệu |

### TC-011: false negative — điều khoản rủi ro diễn đạt kín

| Trường | Nội dung |
| --- | --- |
| Đầu vào | Hợp đồng có giới hạn trách nhiệm rất thấp (contract-003, Điều 5) |
| Đầu ra kỳ vọng | red_flags[] phát hiện giới hạn trách nhiệm thấp bất thường |
| Tiêu chí PASS | Phát hiện "không vượt quá giá trị 01 tháng" là quá thấp cho hợp đồng 1.8 tỷ |

### TC-012: bình thường — trích xuất điều khoản bảo mật

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-001.txt |
| Đầu ra kỳ vọng | Trích xuất được Điều 5 bảo mật với thời hạn 2 năm |
| Tiêu chí PASS | Nội dung bảo mật đầy đủ, có source_evidence |

### TC-013: telecom SLA — trích xuất SLA chi tiết (contract-004)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-004-telecom-sla.txt |
| Đầu ra kỳ vọng | Trích xuất SLA: uptime 99.99%, RTO < 4h, RPO < 1h. Phạt SLA: 0.1%/phút vượt. Giá trị 4.8 tỷ/năm. |
| Tiêu chí PASS | SLA numbers chính xác, có source_evidence cho từng thông số, confidence > 0.8 |

### TC-014: telecom SLA — phát hiện rủi ro chấm dứt theo SLA (contract-004)

| Trường | Nội dung |
| --- | --- |
| Đầu vào | contract-004-telecom-sla.txt |
| Đầu ra kỳ vọng | Phát hiện: (1) Điều 6d — chấm dứt khi SLA vi phạm 3 tháng liên tiếp, (2) Penalty RTO không giới hạn, (3) Auto-renewal với notice 90 ngày |
| Tiêu chí PASS | Phát hiện ít nhất 2/3 đặc thù, có source_evidence, needs_human_review=true nếu phát hiện rủi ro |

## Tóm tắt yêu cầu nghiệm thu

| Loại ca | Số lượng bắt buộc | SLI |
| --- | ---: | --- |
| Bình thường, đủ thông tin | ≥5 | Trích xuất chính xác |
| Thiếu trường quan trọng | ≥2 | needs_human_review=true |
| Mâu thuẫn điều khoản | ≥2 | red_flags[] có cảnh báo |
| Cờ đỏ rõ ràng | ≥2 | red_flags[] + source_evidence |
| Lỗi OCR | ≥1 | Không tự tạo dữ liệu |
| False negative | ≥1 | Phát hiện rủi ro kín |
| Telecom SLA đặc thù | ≥2 | SLA/DR/Penalty chính xác |

**Mục tiêu:** ≥75% pass rate (≥11/14 PASS). 100% ca rủi ro bật HITL.
