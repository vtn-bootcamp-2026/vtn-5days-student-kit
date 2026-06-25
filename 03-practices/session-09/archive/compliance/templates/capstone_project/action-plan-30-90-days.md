---
mo-ta: "Biểu mẫu kế hoạch hành động 30/90 ngày áp dụng AI tại đơn vị và danh mục use case tiếp theo"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-26 07:30 +07:00
updated-at: 2026-06-10 15:55 +07:00
---

# Kế hoạch hành động 30/90 ngày áp dụng AI tại đơn vị (Action plan)

*   **Tên nhóm thực hiện:** [Điền tên nhóm]
*   **Đơn vị áp dụng:** Trung tâm Vận hành khai thác mạng (Viettel Net)
*   **Người chịu trách nhiệm chính:** [Điền tên trưởng nhóm]
*   **Phiên bản tài liệu:** v1.0

---

## 1. Mục tiêu kế hoạch hành động

Bản kế hoạch hành động này thiết lập lộ trình cụ thể nhằm đưa Chatbot RAG **NetSaveAI** vào quy trình vận hành mạng thực tế tại NOC trong **30 ngày đầu tiên** (thử nghiệm trên tập thiết bị quy mô nhỏ để đánh giá độ chính xác lệnh) và **90 ngày tiếp theo** (mở rộng số lượng tài liệu MOP/PA, chuẩn hóa quy trình phân quyền, cập nhật hệ thống định kỳ).

---

## 2. Lộ trình hành động chi tiết (Milestone roadmaps)

### Giai đoạn 30 ngày đầu: Thử nghiệm thực tế nhóm PS Core (Days 1 - 30)
*Mục tiêu: Đưa Chatbot NetSaveAI vào tra cứu quy trình cô lập/cutover thử nghiệm cho nhóm node mạng PS Core (GGSN, SGSN).*

*   - [ ] **Mốc 1 (Ngày 1 - 10): Chuẩn bị cơ sở hạ tầng cục bộ và Tài liệu mẫu**
    *   *Nội dung:* Cài đặt Ollama, Vector Database (Milvus/FAISS), tải mô hình LLM `qwen3.5` hoặc `gemma4` lên máy chủ RAG đặt tại trung tâm NOC. Kỹ sư upload sẵn 100 file Excel/PDF MOP và PA của mạng 4G/3G nhóm PS Core.
    *   *Người chịu trách nhiệm:* Admin hệ thống, Kỹ sư PS Core
*   - [ ] **Mốc 2 (Ngày 11 - 20): Tinh chỉnh Hybrid Search và Metadata Filtering**
    *   *Nội dung:* Test thử các câu hỏi cô lập, cutover phức tạp để tối ưu `must_contain` và điểm số BM25/FAISS, đảm bảo chatbot không bao giờ trộn lẫn quy trình mạng 3G và 4G hoặc lẫn lộn lệnh của node này sang node khác.
    *   *Người chịu trách nhiệm:* Kỹ sư Data/AI
*   - [ ] **Mốc 3 (Ngày 21 - 30): Thử nghiệm Alpha trên kíp trực ban**
    *   *Nội dung:* Tổ chức 1 kíp trực gồm 3 kỹ sư NOC sử dụng song song NetSaveAI và cách tìm thủ công. Thu thập phản hồi về UI/UX và độ tin cậy của quy trình trả về, đánh giá tính sẵn sàng của link tải tài liệu gốc.
    *   *Người chịu trách nhiệm:* Trưởng ca trực NOC

---

### Giai đoạn 90 ngày tiếp theo: Chuẩn hóa, mở rộng IP/Transport và VAS (Days 31 - 90)
*Mục tiêu: Đưa vào sử dụng chính thức cho 100% nhân sự NOC, phủ rộng RAG cho các thiết bị mạng IP, MPLS, Router lõi và VAS.*

*   - [ ] **Mốc 4 (Ngày 31 - 60): Mở rộng Vector Store và Phân Profile tài liệu**
    *   *Nội dung:* Thu thập thêm hàng nghìn file tài liệu hướng dẫn vận hành của nhóm IP/Transport (BRAS, Router) và VAS (HSS, DNS, AAA). Cấu hình Routing Profile động để đảm bảo tìm kiếm chính xác theo domain chuyên môn.
    *   *Người chịu trách nhiệm:* Kỹ sư Network toàn trình
*   - [ ] **Mốc 5 (Ngày 61 - 75): Hoàn thiện tính năng Quản trị tài liệu cho Admin**
    *   *Nội dung:* Phát triển UI cho phép quản trị viên hệ thống (Không cần Dev) tự động upload các phiên bản tài liệu PA mới khi mạng lưới nâng cấp, hệ thống tự động re-index lại vào Vector Database dưới 30 giây.
    *   *Người chịu trách nhiệm:* Dev UI/UX
*   - [ ] **Mốc 6 (Ngày 76 - 90): Nghiệm thu và Đánh giá hiệu quả kinh tế**
    *   *Nội dung:* Báo cáo giảm thiểu thời gian tra cứu MOP (Từ 30 phút xuống còn 30 giây) và số lỗi thao tác sai quy trình. Xin phê duyệt chính thức đưa vào SOP (Standard Operating Procedure) của Viettel Net.
    *   *Người chịu trách nhiệm:* Ban Giám đốc NOC

---

## 3. Danh mục đề xuất 03 trường hợp ứng dụng (Use cases) tiếp theo

Dựa trên nhu cầu thực tế của đơn vị, nhóm đề xuất 3 ý tưởng ứng dụng AI thực chiến tiếp theo để phát triển sau khóa học:

### Use case 1: Chatbot AI Tra cứu Alarm Code Thiết bị Vô Tuyến (Radio Alarm RAG)
*   **Mục tiêu:** Tương tự như NetSaveAI nhưng tập trung vào khối vô tuyến. Kỹ sư hiện trường chỉ cần gõ mã lỗi (VD: Alarm 7215 trạm BTS Ericsson) để AI trả về nguyên nhân, đèn chỉ thị và cách khắc phục mà không cần mở cẩm nang dày hàng trăm trang.
*   **Dữ liệu sử dụng:** Các file PDF sổ tay kỹ thuật thiết bị trạm phát sóng vô tuyến.
*   **Hiệu quả mong đợi:** Kỹ sư hiện trường xử lý sự cố tức thì, giảm MTTR (Mean Time To Repair).

### Use case 2: Trợ lý AI Phân tích Log Sự cố BGP/OSPF (Routing Protocol Log Analyzer)
*   **Mục tiêu:** Nhúng file cấu hình hoặc file log từ thiết bị Router vào AI, AI tự động chỉ ra dòng lệnh bị sai cú pháp hoặc phân tích nguyên nhân BGP session bị drop.
*   **Dữ liệu sử dụng:** File log txt và cấu hình dump từ thiết bị Cisco/Juniper.
*   **Hiệu quả mong đợi:** Cắt giảm thời gian đọc log thủ công của kỹ sư IP/Transport xuống còn vài phút.

### Use case 3: AI Sinh Script Cấu hình Lệnh (Network Automation Script Generator)
*   **Mục tiêu:** Kỹ sư chỉ cần mô tả "Tạo script Ansible để mở khóa port 80 trên 50 con router PE", mô hình AI nội bộ tự động sinh ra mã kịch bản Ansible playbook chuẩn xác với kiến trúc mạng VTN.
*   **Dữ liệu sử dụng:** Dữ liệu cấu hình chuẩn và kho playbook Ansible đang có của đơn vị.
*   **Hiệu quả mong đợi:** Thúc đẩy tự động hóa hạ tầng (Infrastructure as Code) nhanh chóng và hạn chế lỗi cú pháp.
