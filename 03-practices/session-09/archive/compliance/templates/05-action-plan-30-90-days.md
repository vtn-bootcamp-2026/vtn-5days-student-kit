---
mo-ta: "Biểu mẫu kế hoạch hành động 30/90 ngày áp dụng AI tại đơn vị và danh mục use case tiếp theo"
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-26 07:30 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Kế hoạch hành động 30/90 ngày áp dụng AI tại đơn vị (Action plan)

*   **Tên nhóm thực hiện:** [Điền tên nhóm]
*   **Đơn vị áp dụng:** [Ví dụ: Trung tâm Vận hành khai thác mạng / Phòng Hạ tầng Viettel Net]
*   **Người chịu trách nhiệm chính:** [Điền tên trưởng nhóm]
*   **Phiên bản tài liệu:** v1.0

---

## 1. Mục tiêu kế hoạch hành động

Bản kế hoạch hành động này thiết lập lộ trình cụ thể nhằm hiện thực hóa tri thức và công cụ AI đã được trang bị từ khóa học `vtn-ai-builders-bootcamp-2026` vào quy trình làm việc thực tế tại đơn vị trong **30 ngày đầu tiên** (giai đoạn thử nghiệm, thích ứng nhanh) và **90 ngày tiếp theo** (giai đoạn tối ưu hóa, chuẩn hóa quy trình và đề xuất ý tưởng mới).

---

## 2. Lộ trình hành động chi tiết (Milestone roadmaps)

### Giai đoạn 30 ngày đầu: Thử nghiệm thực tế và Tích hợp nhanh (Days 1 - 30)
*Mục tiêu: Đưa Mini Tool Anonymizer vào vận hành thực tế ở quy mô nhỏ, huấn luyện nhân viên nghiệp vụ sử dụng.*

*   - [ ] **Mốc 1 (Ngày 1 - 10): Hoàn thiện cài đặt hạ tầng cục bộ**
    *   *Nội dung:* Cài đặt Python, Ollama và tải mô hình cục bộ (`qwen3.5:1.5b-instruct` hoặc `gemma4:e2b` siêu nhẹ) tại trạm làm việc của ít nhất 03 nhân viên nòng cốt trực tiếp xử lý báo cáo nhân sự/kỹ thuật.
    *   *Người chịu trách nhiệm:* [Điền tên]
*   - [ ] **Mốc 2 (Ngày 11 - 20): Thử nghiệm song song (Parallel testing)**
    *   *Nội dung:* Áp dụng công cụ ẩn danh song song với quy trình duyệt thủ công hiện tại. So sánh độ trễ và độ chính xác để tinh chỉnh Regex.
    *   *Người chịu trách nhiệm:* [Điền tên]
*   - [ ] **Mốc 3 (Ngày 21 - 30): Đánh giá vòng 1 và Hoàn thiện tài liệu**
    *   *Nội dung:* Thu thập ý kiến phản hồi về trải nghiệm người dùng, lập danh mục các từ khóa bị lọc nhầm hoặc lọc sót để cập nhật System Prompt.
    *   *Người chịu trách nhiệm:* [Điền tên]

---

### Giai đoạn 90 ngày tiếp theo: Chuẩn hóa, tối ưu và Mở rộng quy mô (Days 31 - 90)
*Mục tiêu: Quy chuẩn hóa công cụ thành quy trình vận hành chính thức tại phòng ban, tự động hóa tối đa.*

*   - [ ] **Mốc 4 (Ngày 31 - 60): Đóng gói nâng cao và Tích hợp luồng công việc**
    *   *Nội dung:* Tạo file đóng gói giao diện dòng lệnh tương tác tiện dụng, tích hợp phím tắt hoặc liên kết trực tiếp để mở nhanh file đầu vào.
    *   *Người chịu trách nhiệm:* [Điền tên]
*   - [ ] **Mốc 5 (Ngày 61 - 75): Xây dựng quy chế vận hành và Hướng dẫn bảo mật**
    *   *Nội dung:* Ban hành văn bản hướng dẫn bảo mật thông tin nội bộ khi ứng dụng các công cụ AI cục bộ tại phòng ban.
    *   *Người chịu trách nhiệm:* [Điền tên]
*   - [ ] **Mốc 6 (Ngày 76 - 90): Nghiệm thu và Đánh giá hiệu quả kinh tế**
    *   *Nội dung:* Lập báo cáo định lượng hiệu quả (Ví dụ tổng số giờ lao động tiết kiệm được, số lượng lỗi bảo mật đã ngăn ngừa) trình lãnh đạo đơn vị.
    *   *Người chịu trách nhiệm:* [Điền tên]

---

## 3. Danh mục đề xuất 03 trường hợp ứng dụng (Use cases) tiếp theo

Dựa trên nhu cầu thực tế của đơn vị, nhóm đề xuất 3 ý tưởng ứng dụng AI thực chiến tiếp theo để phát triển sau khóa học:

### Use case 1: Trợ lý AI tóm tắt nhật ký vận hành trạm truyền dẫn (SCADA log summarizer)
*   **Mục tiêu:** Tự động tóm tắt các tệp tin log sự cố SCADA dài hàng nghìn dòng thành báo cáo cô đọng 10 dòng bằng mô hình cục bộ.
*   **Dữ liệu sử dụng:** Log hệ thống SCADA dạng text thô của Viettel Net.
*   **Hiệu quả mong đợi:** Kỹ sư trực ca nắm bắt nguyên nhân lỗi hệ thống trong vòng 2 phút thay vì mất 45 phút đọc log thủ công.

### Use case 2: Công cụ AI sinh mã kịch bản tự động hóa hạ tầng (Infrastructure-as-code generator)
*   **Mục tiêu:** Hỗ trợ kỹ sư hạ tầng viết nhanh các đoạn mã Ansible/Terraform để cấu hình tự động trạm phát sóng thông qua mô tả ngôn ngữ tự nhiên tiếng Việt.
*   **Dữ liệu sử dụng:** Các tài liệu thiết kế mạng chuẩn và tệp script Ansible mẫu của VTN.
*   **Hiệu quả mong đợi:** Giảm thiểu 50% thời gian viết script cấu hình hạ tầng mạng mới, hạn chế lỗi cú pháp do con người gõ sai.

### Use case 3: Chatbot tra cứu quy trình kỹ thuật vận hành O&M offline (Offline O&M procedures assistant)
*   **Mục tiêu:** Tạo trợ lý AI hỏi đáp (RAG offline) tra cứu hàng nghìn trang tài liệu quy trình vận hành và bảo trì trạm biến áp, truyền dẫn mà không cần kết nối internet.
*   **Dữ liệu sử dụng:** Các file PDF quy trình vận hành tiêu chuẩn kỹ thuật nội bộ của tập đoàn.
*   **Hiệu quả mong đợi:** Kỹ sư hiện trường tra cứu tức thời cách xử lý sự cố thiết bị tại trạm mà không cần liên hệ trung tâm hỗ trợ kỹ thuật.
