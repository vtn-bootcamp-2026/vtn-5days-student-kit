---
mo-ta: "Prompt 1 — Sinh tệp Use Case One Pager tự động dựa trên thông tin bài toán"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:00 +07:00
updated-at: 2026-06-26 10:00 +07:00
---

# Prompt 1: Khảo sát & Khởi tạo dự án một trang (Use Case One Pager)

Sao chép toàn bộ nội dung trong khung dưới đây, thay thế các thông tin trong ngoặc vuông `[...]` ở phần **DỮ LIỆU ĐẦU VÀO CỦA NHÓM** bằng thông tin thực tế của nhóm bạn, rồi gửi cho trợ lý ảo AI:

```text
BỐI CẢNH:
Tôi là thành viên nhóm học viên tham gia khóa học VTN AI Builders Bootcamp 2026. Nhóm chúng tôi đang xây dựng một giải pháp AI/GenAI thực chiến để giải quyết một bài toán nghiệp vụ thực tế tại Viettel Networks (VTN). Tôi cần tạo tệp tài liệu đề xuất dự án một trang "01-use-case-one-pager.md" theo biểu mẫu tiêu chuẩn.

DỮ LIỆU ĐẦU VÀO CỦA NHÓM:
- Tên dự án: [Ví dụ: NetSaveAI — Chatbot RAG cho Vận Hành Mạng Viễn Thông]
- Đơn vị đề xuất: [Ví dụ: Trung tâm Vận hành khai thác mạng (NOC) - Viettel Net]
- Người đầu mối liên hệ: [Ví dụ: Nguyễn Văn A - Trưởng nhóm]
- Mức độ ưu tiên: [Ví dụ: Cao]
- Mốc thời gian dự kiến thí điểm: [Ví dụ: Tháng 07/2026]
- Nỗi đau nghiệp vụ (Pain point): [Ví dụ: Khi thiết bị lỗi, kỹ sư phải tìm kiếm tài liệu quy trình vận hành MOP/Checklist thủ công trong hàng trăm file PDF/Word mất 15-30 phút, dễ thao tác sai lệnh dưới áp lực cao. Không thể dùng AI công cộng vì dữ liệu bảo mật.]
- Giải pháp đề xuất & Công nghệ: [Ví dụ: Chatbot RAG offline chạy cục bộ. Index tài liệu MOP vào Vector DB, dùng Hybrid Search (BM25 + FAISS) để tìm kiếm chính xác, dùng Local LLM qwen3.5:7b-instruct qua Ollama để tổng hợp các bước xử lý kèm trích dẫn nguồn.]
- Hiệu quả KPI mong đợi: [Ví dụ: Giảm thời gian tra cứu từ 15-30 phút xuống dưới 30 giây; Đảm bảo an toàn 100% dữ liệu không lộ ra ngoài; Tối ưu hóa đào tạo kỹ sư trực ca mới.]

CHỈ DẪN CHO AI:
Hãy viết một tài liệu Markdown hoàn chỉnh cho tệp "01-use-case-one-pager.md" dựa trên dữ liệu đầu vào trên. Hãy điền đầy đủ và chi tiết các phần sau theo phong cách chuyên nghiệp của Viettel Net:
1. Tiêu đề dự án, đơn vị, người liên hệ, mức độ ưu tiên, mốc thời gian.
2. Mục 1: Vấn đề và Nhu cầu thực tế (Problem statement): Phân tích hiện trạng nghiệp vụ và các rủi ro bảo mật thông tin nội bộ (bao gồm cả Nghị định 356/2025/NĐ-CP về Bảo vệ dữ liệu cá nhân nếu có liên quan).
3. Mục 2: Giải pháp đề xuất (Proposed solution): Mô tả giải pháp, cơ chế hoạt động chi tiết bao gồm mô hình ngôn ngữ lớn cục bộ (local LLM) sử dụng qua Ollama (khuyên dùng qwen3.5:1.5b-instruct / gemma4:e2b cho RAM 8GB hoặc qwen3.5:7b-instruct cho RAM 16GB) và các tầng xử lý.
4. Mục 3: Hiệu quả mang lại (Business value & Impact): Định lượng cụ thể về thời gian tiết kiệm, tính tuân thủ bảo mật và tối ưu chi phí đầu tư.
5. Mục 4: Kiến trúc kỹ thuật và Phương án triển khai (Technical architecture): Phân tách rõ 3 tầng: Client (giao diện), Core (logic xử lý), Model (mô hình AI cục bộ).
6. Mục 5: Rủi ro và Biện pháp phòng ngừa (Risks & Defenses): Đưa ra ít nhất 2 rủi ro (ví dụ: AI ảo tưởng/sót lỗi, hoặc tài nguyên phần cứng) và biện pháp phòng ngừa tương ứng (ví dụ: Human-in-the-loop, Filter Metadata).
7. Mục 6: Đề xuất kế hoạch hành động tiếp theo (Next steps): Kế hoạch hành động 4 tuần đầu tiên để triển khai PoC.

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Biểu mẫu đề xuất dự án một trang Use Case One Pager phục vụ báo cáo Capstone tại VTN"
trang-thai: active
phien-ban: v1.3
created-at: 2026-06-26 10:00 +07:00
updated-at: 2026-06-26 10:00 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh để dán đè vào tệp `01-use-case-one-pager.md`.
