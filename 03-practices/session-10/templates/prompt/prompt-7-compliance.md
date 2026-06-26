---
mo-ta: "Prompt 7 — Đánh giá & Rà soát tuân thủ an toàn thông tin"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 7: Đánh giá & Rà soát tuân thủ an toàn thông tin (Compliance Checklist)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat để hoàn thiện tệp tài liệu `04-compliance-checklist.md`:

```text
BỐI CẢNH:
Tôi cần hoàn thiện bảng kiểm tuân thủ bảo mật và dữ liệu "04-compliance-checklist.md" trước khi thử nghiệm công cụ AI của mình tại Viettel Net. Bản đánh giá này sẽ làm rõ cách giải pháp kỹ thuật của chúng tôi đáp ứng các tiêu chuẩn bảo mật dữ liệu của tổng công ty.

CHỈ DẪN CHO AI:
Hãy viết một tài liệu Markdown hoàn chỉnh cho tệp "04-compliance-checklist.md" dựa trên giải pháp kỹ thuật của dự án. Tài liệu cần điền đầy đủ và chi tiết các hạng mục sau:

1. Thông tin chung: Tên dự án/công cụ, đơn vị phát triển, người chịu trách nhiệm kỹ thuật, người phê duyệt nghiệp vụ.
2. Mục 1: Mục đích bảng kiểm: Mô tả vai trò kiểm soát an toàn thông tin của tài liệu này tại VTN.
3. Mục 2: Các hạng mục kiểm tra tuân thủ (Đánh dấu hoàn thành [x] và mô tả giải pháp kỹ thuật thực tế cho tất cả các tiêu chí sau):
   - Hạng mục A: An toàn dữ liệu cá nhân nhạy cảm (PII compliance)
     - Tiêu chí A1: Che giấu thông tin định danh trực tiếp (Mô tả cách bộ lọc Regex hoặc LLM thay thế tên, SĐT, email, CCCD bằng nhãn).
     - Tiêu chí A2: Xử lý dữ liệu tại máy trạm cục bộ (Mô tả việc triển khai offline 100% qua cổng localhost 11434 với các mô hình siêu nhẹ qwen3.5:1.5b-instruct hoặc gemma4:e2b).
     - Tiêu chí A3: Ngăn chặn lưu trữ tạm thời (Mô tả việc xử lý In-Memory trực tiếp trên RAM, không ghi bộ nhớ đệm tạm chứa PII thô).
   - Hạng mục B: Quản lý phân quyền và cổng kết nối (Endpoint & Access control)
     - Tiêu chí B1: Giới hạn cổng kết nối mô hình (Mô tả cấu hình Ollama chỉ bind vào localhost 127.0.0.1, nạp biến môi trường từ tệp `.env`).
     - Tiêu chí B2: Kiểm soát quyền thực thi của mã nguồn (Mô tả việc chạy script dưới quyền User thông thường, không yêu cầu đặc quyền Admin/Root).
   - Hạng mục C: Cơ chế kiểm soát của con người (Human-in-the-loop - HITL)
     - Tiêu chí C1: Giao diện phê duyệt kết quả ẩn danh (Mô tả giao diện hoặc cơ chế bật cờ review thủ công khi có sự cố).
     - Tiêu chí C2: Quyền can thiệp thủ công (Mô tả cách người dùng trực tiếp chỉnh sửa các trường bị ẩn sót hoặc ẩn nhầm).
   - Hạng mục D: Quản lý log và Audit trail (Audit Logging)
     - Tiêu chí D1: Bảo mật nhật ký log (Đảm bảo file log vận hành `execution-log.csv` không ghi lại dữ liệu thô nhạy cảm, chỉ lưu số lượng xử lý và trạng thái).
     - Tiêu chí D2: Lưu trữ an toàn và phân quyền log (Mô tả quyền truy cập tệp tin log chỉ cho admin hoặc nhân sự có thẩm quyền).

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Bản giải pháp mẫu - Bảng kiểm tuân thủ bảo mật và dữ liệu trước khi thí điểm công cụ AI tại VTN"
trang-thai: active
phien-ban: v1.3
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không kèm thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh với đầy đủ các tiêu chí bảo mật đã được check [x] và mô tả giải pháp tương ứng để dán đè vào tệp `04-compliance-checklist.md`.
