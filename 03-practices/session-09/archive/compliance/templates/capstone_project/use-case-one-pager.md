---
mo-ta: "Biểu mẫu đề xuất dự án một trang Use Case One Pager phục vụ báo cáo Capstone tại VTN"
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-26 07:20 +07:00
updated-at: 2026-06-10 15:55 +07:00
---

# Đề xuất dự án một trang (Use case one pager)

*   **Tên dự án ứng dụng:** NetSaveAI — Chatbot RAG cho Vận Hành Mạng Viễn Thông
*   **Đơn vị đề xuất:** Trung tâm Vận hành khai thác mạng (Viettel Net)
*   **Người đầu mối liên hệ:** [Điền tên]
*   **Mức độ ưu tiên:** Cao
*   **Mốc thời gian dự kiến thí điểm:** [Điền tháng/năm]

---

## 1. Vấn đề và Nhu cầu thực tế (Problem statement)
*Mô tả ngắn gọn nỗi đau (pain point) hiện tại tại đơn vị mà giải pháp này sẽ giải quyết.*

*   **Hiện trạng:** Khi nhận được alert thiết bị mạng lỗi (VD: Node GGHL14), kỹ sư trực ca phải tìm kiếm thủ công trong hàng trăm file Excel/PDF/Word (PA, MOP, Checklist) để tra cứu quy trình xử lý.
*   **Rủi ro:** Mất từ 15–30 phút chỉ để tìm đúng file, đúng sheet và đúng bước xử lý. Dưới áp lực cao dễ dẫn đến sai sót, thực hiện sai lệnh gây ảnh hưởng đến hàng triệu thuê bao. Không thể sử dụng ChatGPT công cộng vì tài liệu cấu trúc mạng nội bộ là dữ liệu tuyệt mật.

---

## 2. Giải pháp đề xuất (Proposed solution)
*Mô tả cách thức ứng dụng AI/Local LLM giải quyết vấn đề trên.*

*   **Giải pháp:** Xây dựng hệ thống **NetSaveAI** - Chatbot RAG (Retrieval-Augmented Generation) hoạt động hoàn toàn offline trên hạ tầng nội bộ.
*   **Cơ chế hoạt động:** 
    *   Hệ thống sẽ index các file tài liệu PA, MOP, Checklist vào Vector Database.
    *   Sử dụng Hybrid Search (BM25 + FAISS) để tìm kiếm chính xác theo ngữ cảnh, loại node (GGSN, SGSN, BRAS...) và loại kịch bản (cô lập, cutover).
    *   Sử dụng Local LLM (VD: qwen3.5 hoặc gemma4) để tổng hợp đúng lệnh, đúng thứ tự từ các dòng tài liệu được truy xuất, kèm theo trích dẫn nguồn cụ thể để kỹ sư dễ dàng tải về kiểm chứng.

---

## 3. Hiệu quả mang lại (Business value & Impact)
*Định lượng hiệu quả (thời gian, chi phí, mức độ an toàn) của dự án.*

*   **Tiết kiệm thời gian:** Giảm thời gian tìm kiếm tài liệu và quy trình từ **15–30 phút** xuống còn **< 30 giây**.
*   **Đảm bảo an toàn mạng lưới:** Hạn chế sai sót thao tác (nhầm lệnh, nhầm node) nhờ hệ thống cung cấp chính xác quy trình từng bước.
*   **Bảo mật dữ liệu:** Hệ thống chạy 100% offline nội bộ, không có nguy cơ lộ lọt IP address, cấu trúc node hay mật khẩu ra Internet.
*   **Tối ưu đào tạo:** Hỗ trợ kỹ sư mới (onboarding) tra cứu kiến thức dễ dàng, không mất nhiều thời gian hỏi mentor.

---

## 4. Kiến trúc kỹ thuật và Phương án triển khai (Technical architecture)

*   **Tầng Giao diện (Client):** Chat UI tích hợp khả năng upload file (dành cho Admin) và hiển thị kết quả chat kèm theo nút tải file nguồn.
*   **Tầng Xử lý (Core):** Query Analyzer để bóc tách Node Type, Scenario; Routing Engine; Vector Database để thực hiện Hybrid Search (lọc Metadata `must_contain` kết hợp vector ngữ nghĩa).
*   **Tầng Mô hình (Model):** Ollama Server chạy cục bộ, tải LLM tối ưu cho RAG (qwen3.5 hoặc gemma4) và Embedding Model tiếng Việt.
*   **Phương án triển khai:** Cài đặt đóng gói trên server vận hành tại NOC (Network Operations Center), kỹ sư trực ca truy cập qua mạng nội bộ.

---

## 5. Rủi ro và Biện pháp phòng ngừa (Risks & Defenses)

*   **Rủi ro 1: RAG trả về kết quả quy trình sai hoặc nhầm dịch vụ (VD: trả quy trình 3G cho node 4G).**
    *   *Phòng ngừa:* Sử dụng hệ thống Filter Metadata cực kỳ nghiêm ngặt (`must_contain` key) khi tìm kiếm. Chỉ đạo System Prompt LLM: "Chỉ trích xuất các bước có trong tài liệu, tuyệt đối KHÔNG tự thêm lệnh hay thay thế lệnh".
*   **Rủi ro 2: Tài liệu PA/MOP bị lỗi thời sau khi mạng lưới nâng cấp.**
    *   *Phòng ngừa:* Thiết kế luồng cho phép Admin upload tài liệu mới và tự động re-index trong 30 giây mà không cần khởi động lại hệ thống hoặc cần lập trình viên.

---

## 6. Đề xuất kế hoạch hành động tiếp theo (Next steps)

1.  **Tuần 1:** Thử nghiệm PoC trên tập tài liệu của nhóm thiết bị PS Core (GGSN, vEPC) với các kịch bản như "Cô lập dịch vụ", "Cutover".
2.  **Tuần 2:** Đánh giá độ chính xác của Hybrid Search, điều chỉnh Query Analyzer để bắt đúng các tiền tố node mạng đặc thù (VD: SGHL04, PEKH01).
3.  **Tuần 3:** Tích hợp giao diện Chat và tính năng Upload tài liệu động cho quản trị viên.
4.  **Tuần 4:** Đưa vào trực ca song song, lấy phản hồi từ kỹ sư NOC và nghiệm thu dự án.
