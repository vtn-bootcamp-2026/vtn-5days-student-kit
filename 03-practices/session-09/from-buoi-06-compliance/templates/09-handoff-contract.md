---
mo-ta: "Biểu mẫu biên bản bàn giao kỹ thuật Handoff Contract cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-26 07:25 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Biên bản bàn giao kỹ thuật (Handoff contract)

*   **Dự án ứng dụng:** Mini Tool Anonymizer (Ẩn danh dữ liệu PII)
*   **Bên giao (Đơn vị phát triển):** Nhóm học viên AI Builders - [Điền tên nhóm]
*   **Bên nhận (Đơn vị vận hành/Người dùng):** [Điền tên đơn vị tiếp nhận, ví dụ: Phòng Tổ chức Lao động / IT Viettel Net]
*   **Ngày ký kết bàn giao:** [Điền ngày]

---

## 1. Mục đích biên bản

Biên bản bàn giao kỹ thuật (Handoff contract) xác nhận việc chuyển giao toàn bộ mã nguồn, cấu hình, dữ liệu mẫu, tài liệu vận hành và cam kết bảo trì kỹ thuật của công cụ **Mini Tool Anonymizer** từ nhóm phát triển sang đơn vị vận hành, nhằm đảm bảo công cụ được tiếp quản và vận hành ổn định, đúng quy chế bảo mật của **Viettel Net**.

---

## 2. Danh mục các tài sản bàn giao (Deliverables)

Bên giao cam kết chuyển giao đầy đủ các cấu phần dưới đây cho Bên nhận:

| STT | Tên tài sản bàn giao | Định dạng / Đường dẫn | Trạng thái bàn giao | Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Mã nguồn ứng dụng chính | `anonymizer.py` | [Đầy đủ] | Viết bằng Python 3.10+, tích hợp thư viện Regex & Pydantic. |
| 2 | File cấu hình môi trường | `.env` | [Đầy đủ] | Chứa biến môi trường kết nối Ollama cục bộ. |
| 3 | Bộ cài đặt thư viện | `requirements.txt` | [Đầy đủ] | Danh sách các thư viện Python cần cài đặt. |
| 4 | Tài liệu hướng dẫn vận hành | `runbook-template.md` | [Đầy đủ] | Hướng dẫn cài đặt, chạy thử và xử lý sự cố. |
| 5 | Bộ ca kiểm thử đã xác thực | `test-cases-specification.md` | [Đầy đủ] | Ghi nhận kết quả của 10 ca kiểm thử. |
| 6 | Tài liệu tuân thủ bảo mật | `compliance-checklist.md` | [Đầy đủ] | Đánh giá tuân thủ an toàn thông tin của VTN. |
| 7 | Tệp dữ liệu giả lập mẫu | `synthetic-data/` | [Đầy đủ] | Chứa các kịch bản kiểm thử edge cases & prompt injection. |

---

## 3. Cam kết mức độ dịch vụ và Hỗ trợ kỹ thuật (SLA & Support guidelines)

Để đảm bảo công cụ vận hành trơn tru sau bàn giao, hai bên thống nhất các điều khoản hỗ trợ kỹ thuật như sau:

### Trách nhiệm của Bên giao (Nhóm phát triển):
*   **Hỗ trợ kỹ thuật ban đầu:** Hỗ trợ cài đặt môi trường ảo Python và cài đặt Ollama trực tiếp tại máy trạm của Bên nhận trong vòng **03 ngày làm việc** kể từ ngày ký biên bản.
*   **Sửa lỗi phát sinh khẩn cấp (Hotfix):** Cam kết xử lý các lỗi nghiêm trọng gây sập chương trình hoặc rò rỉ dữ liệu (Critical bugs) trong vòng **24 giờ** kể từ khi nhận được thông báo.
*   **Chuyển giao tri thức:** Tổ chức 01 buổi hướng dẫn sử dụng (kéo dài 30-45 phút) để chuyển giao cách vận hành và cập nhật các mẫu Regex cho Bên nhận.

### Trách nhiệm của Bên nhận (Đơn vị tiếp nhận):
*   **Chuẩn bị hạ tầng:** Đảm bảo máy trạm vận hành đáp ứng đúng yêu cầu phần cứng tối thiểu (RAM >= 8GB, cài đặt sẵn Python và Ollama).
*   **Giám sát vận hành:** Thường xuyên kiểm tra tệp log hệ thống (`logs/anonymizer.log`) để chủ động phát hiện sự cố tràn RAM hoặc mất kết nối API.
*   **Sử dụng đúng mục đích:** Chỉ sử dụng công cụ trong phạm vi nội bộ của Viettel Net, không tự ý chỉnh sửa mã nguồn cốt lõi để gửi dữ liệu chưa ẩn danh ra bên ngoài.

---

## 4. Xác nhận ký kết bàn giao

Hai bên cùng thống nhất các nội dung trên và cam kết thực hiện đúng trách nhiệm được giao.

**ĐẠI DIỆN BÊN GIAO (Nhóm phát triển)**  
*(Ký, ghi rõ họ tên)*  

<br><br><br>

**ĐẠI DIỆN BÊN NHẬN (Đơn vị tiếp quản)**  
*(Ký, ghi rõ họ tên)*  
