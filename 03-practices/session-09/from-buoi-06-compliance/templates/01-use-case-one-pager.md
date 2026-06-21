---
mo-ta: "Biểu mẫu đề xuất dự án một trang Use Case One Pager phục vụ báo cáo Capstone tại VTN"
trang-thai: active
phien-ban: v1.3
created-at: 2026-05-26 07:20 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Đề xuất dự án một trang (Use case one pager)

*   **Tên dự án ứng dụng:** [Ví dụ: Ứng dụng trợ lý AI ẩn danh dữ liệu nhân sự tự động]
*   **Đơn vị đề xuất:** [Điền tên nhóm/phòng ban]
*   **Người đầu mối liên hệ:** [Điền tên]
*   **Mức độ ưu tiên:** [Cao / Trung bình]
*   **Mốc thời gian dự kiến thí điểm:** [Điền tháng/năm]

---

## 1. Vấn đề và Nhu cầu thực tế (Problem statement)
*Mô tả ngắn gọn nỗi đau (pain point) hiện tại tại đơn vị mà giải pháp này sẽ giải quyết.*

*   **Hiện trạng:** Nhân sự phòng Tổ chức Lao động / Kỹ thuật vận hành thường xuyên phải xử lý các báo cáo có chứa thông tin cá nhân nhạy cảm (PII) như tên tuổi, số CCCD, điện thoại của kỹ sư trực ca, lịch làm việc.
*   **Rủi ro:** Quy trình ẩn danh thủ công tốn nhiều thời gian, dễ bỏ sót. Nếu gửi trực tiếp các báo cáo thô này lên các công cụ AI đám mây công cộng (như ChatGPT) hoặc chia sẻ ra ngoài sẽ vi phạm nghiêm trọng Nghị định 356/2025/NĐ-CP về Bảo vệ dữ liệu cá nhân và quy chế bảo mật thông tin nội bộ của Viettel Net.

---

## 2. Giải pháp đề xuất (Proposed solution)
*Mô tả cách thức ứng dụng AI/Local LLM giải quyết vấn đề trên.*

*   **Giải pháp:** Phát triển và triển khai **Mini Tool Anonymizer** chạy hoàn toàn cục bộ (offline) trên máy trạm của nhân viên hoặc hạ tầng private cloud của VTN.
*   **Cơ chế hoạt động:** 
    *   Tự động quét và phát hiện các trường dữ liệu nhạy cảm (Tên, CCCD, Điện thoại, Email, Địa chỉ) bằng thuật toán Regex tối ưu.
    *   Sử dụng mô hình ngôn ngữ lớn cục bộ siêu nhẹ (**qwen3.5:1.5b-instruct** hoặc **gemma4:e2b**) thông qua **Ollama** để phân tích ngữ cảnh, phát hiện các thực thể lắt léo (tên riêng trùng danh từ thường) và thay thế bằng các nhãn chuẩn hóa như `[NAME]`, `[CCCD_NUMBER]`.
    *   Cung cấp màn hình duyệt kết quả cho người dùng (Human-in-the-loop) để đảm bảo độ chính xác tuyệt đối 100%.

---

## 3. Hiệu quả mang lại (Business value & Impact)
*Định lượng hiệu quả (thời gian, chi phí, mức độ an toàn) của dự án.*

*   **Tiết kiệm thời gian:** Giảm thời gian rà soát và lọc tài liệu báo cáo từ **15 phút/tài liệu** xuống còn dưới **30 giây/tài liệu** (Năng suất tăng 30 lần).
*   **Đảm bảo tuân thủ bảo mật:** Triển khai offline 100%, bảo vệ an toàn tuyệt đối dữ liệu nội bộ của Viettel Net, loại bỏ hoàn toàn nguy cơ rò rỉ thông tin nhân sự.
*   **Tối ưu chi phí:** Sử dụng mã nguồn mở và chạy offline trên phần cứng máy trạm có sẵn của nhân viên, chi phí đầu tư bản quyền phần mềm và bản quyền API mô hình bằng **0 VNĐ**.

---

## 4. Kiến trúc kỹ thuật và Phương án triển khai (Technical architecture)

*   **Tầng Client (Giao diện):** Giao diện dòng lệnh (CLI interactive) trực quan, có highlight màu sắc cảnh báo lỗi.
*   **Tầng Core (Logic):** Python 3.10+, thư viện regex và Pydantic để kiểm soát dữ liệu.
*   **Tầng Model (Trí tuệ nhân tạo):** Ollama Server chạy cục bộ, tải mô hình lượng tử hóa siêu nhẹ `qwen3.5:1.5b-instruct` hoặc `gemma4:e2b` (Mức tiêu hao RAM thực tế tối ưu chỉ từ 1.5 GB - 3 GB).
*   **Phương án tích hợp:** Đóng gói thành file chạy `.bat` một chạm, người dùng chỉ cần nhấp đúp để khởi chạy mà không cần gõ lệnh kỹ thuật phức tạp.

---

## 5. Rủi ro và Biện pháp phòng ngừa (Risks & Defenses)

*   **Rủi ro 1: Lọc sót tên riêng lắt léo trùng danh từ thường.**
    *   *Phòng ngừa:* Bắt buộc áp dụng cơ chế phê duyệt thủ công (Human-in-the-loop) đối với các văn bản lưu trữ chính thức.
*   **Rủi ro 2: Tràn bộ nhớ RAM trên các máy tính cấu hình yếu (RAM 8GB).**
    *   *Phòng ngừa:* Thiết lập giới hạn kích thước file quét và cấu hình tối ưu hóa tham số mô hình trong Ollama để giải phóng bộ nhớ ngay sau khi suy luận hoàn tất.

---

## 6. Đề xuất kế hoạch hành động tiếp theo (Next steps)

1.  **Tuần 1:** Triển khai thử nghiệm cho 05 nhân sự nòng cốt tại Phòng Tổ chức Lao động để đánh giá thực tế.
2.  **Tuần 2:** Thu thập ý kiến phản hồi, tinh chỉnh bộ từ điển Regex và tinh chỉnh System Prompt của LLM.
3.  **Tuần 3:** Đóng gói bản cài đặt hoàn thiện bàn giao kỹ thuật cho bộ phận IT vận hành lớp.
4.  **Tuần 4:** Nghiệm thu toàn trình và đề xuất nhân rộng ứng dụng tại các chi nhánh kỹ thuật của Viettel Net.
