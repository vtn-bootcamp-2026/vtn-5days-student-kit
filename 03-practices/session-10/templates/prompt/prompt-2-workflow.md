---
mo-ta: "Prompt 2 — Thiết kế sơ đồ khối luồng xử lý và Con người kiểm duyệt"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:00 +07:00
updated-at: 2026-06-26 10:00 +07:00
---

# Prompt 2: Thiết kế sơ đồ khối luồng xử lý và Con người kiểm duyệt (Logical Workflow)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat:

```text
BỐI CẢNH:
Tôi cần xây dựng bản đặc tả luồng công việc logic "02-logical-workflow.md" cho dự án AI đã chọn ở bước trước. Tôi muốn sơ đồ khối của quy trình hoạt động được biểu diễn bằng mã Mermaid và có phân vai rõ ràng giữa AI và con người kiểm duyệt (Human-in-the-loop).

CHỈ DẪN CHO AI:
Hãy viết một tài liệu Markdown hoàn chỉnh cho tệp "02-logical-workflow.md" dựa trên bối cảnh và giải pháp kỹ thuật của dự án. Tài liệu cần bao gồm các phần sau:

1. Thông tin chung: Tên dự án, tên nhóm thực hiện, đơn vị áp dụng.
2. Mục 1: Sơ đồ khối quy trình (Logical Flowchart):
   - Thiết kế một sơ đồ Mermaid chi tiết dạng `graph TD`. Sơ đồ phải mô tả rõ các tầng xử lý dữ liệu: tiếp nhận đầu vào -> xử lý Regex/Pre-processing -> gửi tới Local LLM -> kiểm tra các rủi ro bảo mật (như Prompt Injection) -> cơ chế kích hoạt cờ kiểm duyệt thủ công `needs_human_review` -> điểm kiểm duyệt của con người (Human-in-the-loop) -> đầu ra an toàn hoặc chỉnh sửa thủ công.
3. Mục 2: Mô tả chi tiết các bước trong luồng:
   - Viết đặc tả chi tiết cho từng bước được mô tả trong sơ đồ Mermaid bao gồm: Đầu vào (Input), Hành động (Action), và Mục tiêu (Target).
   - Làm rõ cơ chế tự động hóa hoạt động như thế nào và cách hệ thống xử lý khi có lỗi hoặc sự cố ở mỗi bước.
4. Mục 3: Ranh giới Phân vai (Human-in-the-loop Boundaries):
   - Đặc tả rõ những nhiệm vụ nào mô hình AI được phép tự động thực hiện và những nhiệm vụ nào bắt buộc phải có con người kiểm duyệt và phê duyệt cuối cùng (Chốt chặn cuối cùng).

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Biểu mẫu đặc tả luồng logic (Logical Workflow Blueprint) phục vụ báo cáo Capstone tại VTN"
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-26 10:00 +07:00
updated-at: 2026-06-26 10:00 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không kèm thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh chứa sơ đồ Mermaid để dán đè vào tệp `02-logical-workflow.md`.
