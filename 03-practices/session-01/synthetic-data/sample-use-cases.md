---
mo-ta: ba bai toan mau an toan de luyen cham diem buoi 1
trang-thai: draft
phien-ban: v1.0
created-at: 2026-05-17 13:54 +07:00
updated-at: 2026-05-17 13:54 +07:00
---

# Bài toán mẫu để luyện chấm điểm

## Case 1: trợ lý chính sách nhân sự giả lập

Mục tiêu: giúp nhân sự tra cứu nhanh chính sách nghỉ phép, công tác phí và quy trình xin xác nhận.

Đầu vào mô phỏng:

- FAQ chính sách nhân sự giả lập.
- Quy trình duyệt nghỉ phép giả lập.
- Câu hỏi của nhân viên.

Đầu ra mong muốn:

- Câu trả lời ngắn.
- Nguồn trích dẫn từ tài liệu giả lập.
- Khuyến nghị liên hệ nhân sự nếu câu hỏi vượt phạm vi.

Rủi ro chính: trả lời sai chính sách hoặc suy đoán khi thiếu căn cứ.

## Case 2: tóm tắt cảnh báo NOC giả lập

Mục tiêu: đọc danh sách cảnh báo giả lập và tạo bản tóm tắt ưu tiên xử lý.

Đầu vào mô phỏng:

- File `sample-noc-alerts.csv`.
- Quy tắc ưu tiên giả lập.

Đầu ra mong muốn:

- Danh sách cảnh báo theo mức ưu tiên.
- Lý do ưu tiên.
- Câu hỏi cần kỹ sư xác nhận.

Rủi ro chính: nhầm mức độ nghiêm trọng hoặc bỏ sót cảnh báo.

## Case 3: định tuyến ticket hỗ trợ giả lập

Mục tiêu: phân loại ticket giả lập theo nhóm xử lý và tạo bản nháp phản hồi.

Đầu vào mô phỏng:

- Tiêu đề ticket.
- Mô tả ticket.
- Nhóm xử lý giả lập.

Đầu ra mong muốn:

- Nhãn phân loại.
- Nhóm xử lý đề xuất.
- Bản nháp phản hồi cho người gửi.

Rủi ro chính: định tuyến sai hoặc tạo phản hồi vượt phạm vi.
