---
mo-ta: "Biên bản bàn giao kỹ thuật và hướng dẫn vận hành trợ lý AI cá nhân local assistant runbook"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-25 10:41 +07:00
updated-at: 2026-05-25 13:40 +07:00
---

# Biên bản bàn giao kỹ thuật: Local assistant runbook

Tài liệu này được biên soạn bởi nhóm kỹ sư thực hành nhằm ghi chép cấu hình chi tiết, quy trình gỡ lỗi và các giới hạn vận hành an toàn của hệ thống Trợ lý AI cá nhân chạy cục bộ tại Viettel Networks.

---

## 1. Thông số môi trường vận hành

| Tham số cấu hình | Giá trị thiết lập thực tế của nhóm |
| :--- | :--- |
| **Hệ điều hành Host** | *Ví dụ: Windows 11 Enterprise* |
| **Môi trường thực thi** | *Ví dụ: WSL2 - Ubuntu 22.04 LTS / PowerShell 7* |
| **Phiên bản Ollama** | *Ví dụ: Ollama v0.1.48* |
| **Địa chỉ API cục bộ** | `http://127.0.0.1:11434` |

---

## 2. Nhật ký bàn giao kỹ thuật (Local Assistant Runbook - 8 Phần bắt buộc)

Học viên điền đầy đủ 8 nội dung bàn giao kỹ thuật chi tiết dưới đây:

### a. Công cụ sử dụng (Framework)
*Ghi rõ hệ thống nền: framework chính được lựa chọn để thiết lập trợ lý (ví dụ: Hermes Agent hoặc OpenClaw).*

### b. Phiên bản công cụ (Engine CLI Version)
*Ghi lại phiên bản CLI của framework khi kiểm tra (ví dụ: Hermes v0.14.0, OpenClaw npm latest).*

### c. Mô hình ngôn ngữ sử dụng (Local Model)
*Ghi rõ tên tệp tin lượng tử hóa: quantized model chính xác được nạp vào hệ thống (ví dụ: `qwen3.5:7b-instruct`, `gemma4:e2b` hoặc `qwen3.5:1.5b-instruct`).*

### d. Tham số cổng kết nối (Ollama API Endpoint)
*Ghi lại địa chỉ endpoint API chính xác được nạp vào tệp cấu hình của tác tử. Giải trình rõ việc sử dụng hoặc không sử dụng hậu tố `/v1` tùy theo framework để tránh lỗi mất khả năng gọi công cụ.*

### e. Hướng dẫn khởi chạy hệ thống (Execution Commands)
*Liệt kê chính xác chuỗi lệnh liên tục để khởi động toàn bộ dịch vụ từ máy chủ mô hình đến cổng giao tiếp (ví dụ: lệnh khởi chạy Ollama daemon -> lệnh mở gateway -> lệnh kết nối CLI/Telegram).*

### f. Nhật ký lỗi phát sinh trong buổi Lab (Troubleshooting Log)
*Mô tả chi tiết các hiện tượng lỗi thực tế mà nhóm đã gặp phải trong quá trình cài đặt (ví dụ: lỗi tràn bộ nhớ OOM, lỗi lệch cổng, lỗi chặn tường lửa firewall giữa Windows và WSL2, lỗi chồng chéo ngữ cảnh).*

### g. Giải pháp khắc phục lỗi đã áp dụng (Resolutions)
*Ghi lại chính xác các câu lệnh hoặc thao tác xử lý kỹ thuật nhóm đã thực hiện để khắc phục các lỗi ở mục f (ví dụ: đặt biến môi trường `OLLAMA_HOST=0.0.0.0`, cấu hình tăng context window lên `16000`, thực thi Memory Clear Protocol bằng cách xóa SQLite `.db`...).*

### h. Thiết lập giới hạn an toàn thông tin (Security Blacklist & Guardrails)
*Liệt kê danh sách các lệnh cấm thực thi: shell command blacklist, các hạn chế truy cập thư mục được nhóm nạp vào agent để đảm bảo tính an toàn dữ liệu cho hệ thống.*

---

## 3. Nhật ký kiểm tra kết nối ban đầu

*Học viên thực hiện chạy prompt kiểm tra kết nối cục bộ:*
> `"Bạn đang chạy bằng local model nào? Trả lời ngắn gọn và không dùng dữ liệu bên ngoài."`

- **Nội dung phản hồi thô của mô hình**:
  ```text
  
  ```
- **Kết luận kết nối (Đạt / Không đạt)**: 
