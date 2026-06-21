---
mo-ta: Mẫu prompt hướng dẫn AI sinh mã Mermaid flowchart cho quy trình mới (to-be)
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-20 02:27 +07:00
updated-at: 2026-06-20 02:27 +07:00
---

# Prompt sinh sơ đồ quy trình mới (Mermaid)

Hãy sao chép toàn bộ nội dung ô lệnh dưới đây, thay thế các thông tin trong ngoặc vuông `[...]` bằng quy trình thực tế của nhóm bạn, sau đó dán vào khung chat của **Antigravity** hoặc **Codex** để sinh mã Mermaid.

```text
[BỐI CẢNH]
Tôi đang thiết kế lại quy trình "[Tên quy trình của bạn, ví dụ: Phê duyệt văn bản trình ký]" cho phòng ban "[Tên phòng ban, ví dụ: Hành chính Nhân sự]".
Quy trình mới (quy trình to-be: to-be workflow) đã được tinh gọn và chốt như sau:
- Bước 1: [Mô tả bước 1, ví dụ: Nhân viên tạo văn bản trên hệ thống quản lý tập trung (Simplify)]
- Bước 2: [Mô tả bước 2, ví dụ: AI tự động phân loại, kiểm tra lỗi định dạng và chính tả (Automate)]
- Bước 3: [Mô tả bước 3, ví dụ: Trưởng phòng duyệt nội dung và ký số (điểm duyệt con người: Human-in-the-loop - HITL)]
- Bước 4: [Mô tả bước 4, ví dụ: Hệ thống tự động lưu trữ và gửi thông báo đến các bên liên quan (Automate)]

Kiểu thiết kế quy trình (workflow style) ưu tiên: [Tuyến tính / Song song / Có điều kiện].

[CHỈ DẪN]
Hãy viết mã nguồn Mermaid dạng flowchart LR (sơ đồ khối từ trái qua phải) mô tả trực quan quy trình to-be này:
- Mỗi bước thực hiện là một nút (node), ghi rõ ai làm và công cụ/hệ thống nào được sử dụng.
- Đối với các bước rẽ nhánh điều kiện, sử dụng nút hình thoi dạng {} (ví dụ: {Đạt yêu cầu?}).
- Đánh dấu nút có sự tham gia của trí tuệ nhân tạo (AI) bằng màu nền nổi bật (sử dụng class aiNode fill:#FFE0B2,stroke:#FB8C00,stroke-width:2px).
- Đánh dấu nút có điểm duyệt con người (Human-in-the-loop - HITL) bằng màu nền cảnh báo nhẹ (sử dụng class hitlNode fill:#FFCDD2,stroke:#E53935,stroke-width:2px).

[TIÊU CHUẨN ĐẦU RA]
- Chỉ trả về duy nhất khối mã Mermaid hợp lệ nằm trong thẻ ```mermaid ... ```.
- Không kèm theo bất kỳ lời giải thích dài dòng nào.
- Số lượng nút tối đa là 8 nút để giữ sơ đồ tinh gọn và dễ đọc.
- Bắt buộc có tối thiểu 1 nút đại diện cho điểm duyệt con người (HITL).
```
