---
mo-ta: huong dan thiet lap cong cu thuc hanh va tai khoan ca nhan
trang-thai: active
phien-ban: v1.8
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-20 01:25 +07:00
---

# Hướng dẫn thiết lập công cụ thực hành: tool setup

Tài liệu này hướng dẫn cách chuẩn bị laptop, tài khoản cá nhân và công cụ thực hành trước khi tham gia khóa học **AI thực chiến cho nhân sự nòng cốt - Viettel Net**.

## 1. Chuẩn bị bắt buộc trước buổi học đầu tiên

Học viên cần chuẩn bị các mục tối thiểu sau:

1. Laptop cá nhân hoặc laptop được phép dùng trong lớp, kèm sạc pin.
2. Ít nhất một tài khoản AI cá nhân đăng nhập được trên trình duyệt, ví dụ ChatGPT, Gemini, Claude hoặc Microsoft Copilot.
3. Đọc trước [safety-rules.md](safety-rules.md) và cam kết chỉ dùng dữ liệu mô phỏng trong lớp.

> [!IMPORTANT]
> Không nhập dữ liệu thật, dữ liệu khách hàng, tài liệu nội bộ hoặc thông tin nhạy cảm của Viettel Net vào tài khoản AI cá nhân.

## 2. Chuẩn bị nâng cao theo từng buổi

Các công cụ dưới đây giúp làm bài lab sâu hơn. Nếu chưa kịp chuẩn bị, học viên vẫn có thể theo lớp bằng tài khoản AI cá nhân, dữ liệu mô phỏng và các đáp án mẫu trong `outputs/`.

### 2.1 Google Gemini API - Google AI Studio (khuyên dùng cho lab API)
- **Địa chỉ:** [https://aistudio.google.com/](https://aistudio.google.com/)
- **Cách chuẩn bị:** Đăng nhập bằng tài khoản Google cá nhân hoặc tài khoản Google Workspace của doanh nghiệp (nếu đơn vị đã trang bị Google Pro / Gemini Advanced). Nhấp vào nút **Get API Key** và tạo một khóa API mới.
- **Ưu điểm vượt trội:** Google AI Studio cung cấp hạn mức miễn phí (Free Tier) cực kỳ hào phóng cho các mô hình thế hệ mới (như `gemini-1.5-flash`, `gemini-2.0-flash` hoặc các dòng gemini-3 thế hệ mới). Học viên **không cần liên kết thẻ thanh toán quốc tế** và **không mất phí** mà vẫn có thể thực hành đầy đủ các bài lab về Agent, RAG và Workflow trên lớp.
- **Mục đích:** Tạo API Key chính để kết nối vào các quy trình n8n và tác nhân AI thực hành ở các buổi lab cần gọi API.

### 2.2 OpenAI API Platform (tùy chọn nâng cao)
- **Địa chỉ:** [https://platform.openai.com/](https://platform.openai.com/)
- **Cách chuẩn bị:** Chỉ thực hiện nếu học viên muốn tự so sánh API của OpenAI. Đăng ký tài khoản, truy cập mục **Settings > Billing**, liên kết thẻ thanh toán quốc tế cá nhân (VISA/Mastercard) và nạp tiền (Top-up) mức nhỏ theo nhu cầu cá nhân.
- **Mục đích:** Sử dụng làm API Key dự phòng để thực hành, so sánh chất lượng phản hồi và cấu trúc JSON đầu ra giữa các dòng mô hình (GPT-4o vs Gemini).
- **Lưu ý:** Không sử dụng tài khoản ChatGPT Plus (bản web 20 USD/tháng) vì dịch vụ API yêu cầu tài khoản API Platform riêng biệt.

### 2.3 n8n Cloud (khuyên dùng cho phần AI Workflow)
- **Địa chỉ:** [https://n8n.io/](https://n8n.io/)
- **Cách chuẩn bị:** Đăng ký tài khoản n8n Cloud để sử dụng gói dùng thử miễn phí **14 ngày (Free Trial)**.
- **Mục đích:** Thiết kế trực quan các quy trình tự động hóa thông minh (Smart Ticket Triage).

### 2.4 GitHub cá nhân (khuyên dùng cho Vibe Coding)
- **Địa chỉ:** [https://github.com/](https://github.com/)
- **Cách chuẩn bị:** Đăng ký một tài khoản cá nhân miễn phí.
- **Mục đích:** Quản lý mã nguồn, lưu trữ bộ Implementation Kit và nộp bài tốt nghiệp nếu lớp dùng GitHub để thu bài.

---

## 3. Cài đặt các công cụ cục bộ: Local tools

Các công cụ cục bộ giúp thực hành sâu hơn và tạo phương án dự phòng khi mất mạng internet. Đây là phần khuyến nghị, không phải điều kiện bắt buộc để tham gia buổi đầu tiên.

### 3.1 Cài đặt Ollama (Trình chạy mô hình AI cục bộ)
- **Tải về:** [https://ollama.com/](https://ollama.com/) (Tải phiên bản phù hợp với OS Windows).
- **Mô hình khuyến nghị:** Mở PowerShell và chạy lệnh sau để tải mô hình siêu nhẹ tối ưu tiếng Việt và JSON:
  ```powershell
  ollama run qwen3.5:1.5b-instruct
  ```
- **Đối với máy cấu hình mạnh (RAM >= 16GB):** Tải thêm mô hình chuyên viết code:
  ```powershell
  ollama run qwen3.5-coder:7b
  ```

### 3.2 Visual Studio Code & Git
- **VS Code:** Tải và cài đặt tại [https://code.visualstudio.com/](https://code.visualstudio.com/)
- **Git:** Tải và cài đặt tại [https://git-scm.com/](https://git-scm.com/)

### 3.3 Antigravity IDE & Antigravity 2.0 (Khuyên dùng cho Vibe Coding & Agentic AI)
- **Tải về:** Tải bản cài đặt từ trang chủ **[antigravity.google](https://antigravity.google)** hoặc từ đường dẫn phân phối nội bộ do BTC lớp học cung cấp.
- **Mục đích:** Thực hành các bài lab lập trình tự trị bằng ngôn ngữ tự nhiên (Vibe coding) và điều phối tác nhân AI (Agent orchestration) ở Ngày 2 & 3.
- **Cấu hình:** Kết nối Gemini API Key cá nhân vào IDE để bắt đầu làm việc.
- **Cài đặt các extension hỗ trợ (Khuyên dùng):** Truy cập vào mục **Extensions** ở thanh bên trái (hoặc nhấn `Ctrl + Shift + X` trên Windows / `Cmd + Shift + X` trên macOS), tìm kiếm và cài đặt hai extension sau:
  - `Nord Markdown Preview`: hỗ trợ xem trước các file tài liệu Markdown (`.md`) trực quan với giao diện Nord dịu mắt.
  - `Office Viewer`: hỗ trợ mở và xem trực tiếp các file tài liệu Excel (`.xlsx`), Word (`.docx`) của bài tập ngay trong workspace Antigravity.

### 3.4 Cài đặt Python & Tiện ích Jupyter (Jupyter Extension)
- **Python**: Tải và cài đặt Python (phiên bản khuyến nghị **3.10 trở lên**) từ trang chủ [python.org](https://www.python.org/downloads/).
  * *Lưu ý khi cài đặt*: Hãy tích chọn vào ô **"Add Python to PATH"** (hoặc **"Add python.exe to PATH"**) trong giao diện cài đặt trên Windows để các công cụ và terminal nhận diện lệnh `python`.
- **Extension Python & Jupyter Notebook cho Antigravity / VS Code**:
  * Mở Antigravity IDE (hoặc VS Code).
  * Truy cập mục **Extensions** (phím tắt `Ctrl + Shift + X`).
  * Tìm kiếm và cài đặt 2 tiện ích sau:
    1. **Python** (của Microsoft) - hỗ trợ phát hiện môi trường, IntelliSense và gỡ lỗi Python.
    2. **Jupyter** (của Microsoft) - bắt buộc để hiển thị trực quan và thực thi các tệp thực hành dạng Notebook (`.ipynb`) trong các checkpoint của bài lab.


