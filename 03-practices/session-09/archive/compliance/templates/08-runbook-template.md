---
mo-ta: "Biểu mẫu hướng dẫn vận hành công cụ Mini Tool Anonymizer cho đội ngũ kỹ thuật VTN"
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-26 07:10 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Hướng dẫn vận hành công cụ: Mini tool anonymizer (Runbook)

*   **Mã tài liệu:** VTN-RB-ANON-01
*   **Người biên soạn:** [Điền tên nhóm/cá nhân]
*   **Đơn vị phê duyệt:** Tổng Công ty Mạng lưới Viettel (Viettel Net)
*   **Phiên bản hệ thống áp dụng:** v1.0

---

## 1. Tổng quan hệ thống (System overview)

Tài liệu này hướng dẫn cài đặt, cấu hình, chạy thử và xử lý sự cố đối với **Mini Tool Anonymizer** - Công cụ cục bộ hỗ trợ tự động nhận diện và che giấu dữ liệu cá nhân nhạy cảm (PII) trong các báo cáo nhân sự, kỹ thuật của Viettel Net trước khi gửi lên các hệ thống cloud hoặc chia sẻ ra bên ngoài.

---

## 2. Yêu cầu hệ thống và Chuẩn bị môi trường (Prerequisites)

### Yêu cầu phần cứng tối thiểu:
*   **RAM:** Tối thiểu 8 GB (Khuyến nghị 16 GB để chạy mượt mà).
*   **CPU:** Tối thiểu 4 Cores.
*   **Ổ cứng trống:** Tối thiểu 10 GB SSD để lưu trữ mã nguồn và các tệp mô hình cục bộ.

### Yêu cầu phần mềm cài đặt sẵn:
1.  **Python:** Phiên bản 3.10 trở lên.
2.  **Ollama:** Trình quản lý mô hình ngôn ngữ lớn cục bộ chạy nền.
3.  **Mô hình cục bộ:** Đã tải sẵn bằng một trong các lệnh sau:
    ```powershell
    # Option 1: Máy RAM 8GB (Siêu nhẹ)
    ollama pull qwen3.5:1.5b-instruct
    # HOẶC bản gemma4 siêu nhẹ (4GB) tối ưu cho tiếng Việt và lý luận:
    ollama pull batiai/gemma4-e2b:q4

    # Option 2: Máy RAM >= 12-16GB (Cấu hình trung bình - mạnh)
    ollama pull qwen3.5:7b-instruct
    # HOẶC bản gemma4 trung bình (6GB) cân bằng cực tốt:
    ollama pull batiai/gemma4-e4b:q4
    ```

---

## 3. Quy trình cài đặt chi tiết (Deployment steps)

### Bước 1: Thiết lập thư mục làm việc và Môi trường ảo Python
Mở PowerShell tại thư mục chứa mã nguồn của bạn và chạy các lệnh sau để cô lập môi trường:

```powershell
# Tạo môi trường ảo Python
python -m venv .venv

# Kích hoạt môi trường ảo trên Windows
.venv\Scripts\Activate.ps1

# Nâng cấp pip lên bản mới nhất
python -m pip install --upgrade pip
```

### Bước 2: Cài đặt các thư viện phụ thuộc (Dependencies)
Cài đặt các gói thư viện Python cần thiết bằng cách tạo tệp `requirements.txt` và cài đặt:

```powershell
# Cài đặt trực tiếp qua pip
pip install requests pydantic colorama
```

### Bước 3: Cấu hình các biến môi trường
Tạo file `.env` tại thư mục gốc của dự án và cấu hình các thông số kết nối:

```env
# Địa chỉ cổng máy chủ Ollama cục bộ
OLLAMA_API_URL=http://127.0.0.1:11434/api/generate

# Tên mô hình cục bộ sử dụng (Ví dụ: qwen3.5:1.5b-instruct, gemma4:e2b, qwen3.5:7b-instruct, gemma4:e4b)
LOCAL_MODEL_NAME=qwen3.5:1.5b-instruct

# Cấu hình mức độ log (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

---

## 4. Hướng dẫn vận hành và Sử dụng (Execution guide)

### Khởi chạy công cụ ở chế độ dòng lệnh (CLI Mode):
Chạy script Python bằng lệnh dưới đây:

```powershell
python anonymizer.py --input path/to/input.txt --output path/to/output.txt
```

### Các tham số tùy chọn hỗ trợ:
*   `--input`: Đường dẫn tới tệp tin văn bản cần lọc dữ liệu nhạy cảm (bắt buộc).
*   `--output`: Đường dẫn lưu trữ tệp kết quả sau khi đã lọc (bắt buộc).
*   `--model`: Ghi đè tên mô hình cấu hình trong file `.env` (ví dụ: `--model qwen3.5:7b-instruct`).
*   `--interactive`: Bật chế độ tương tác từng dòng và xác nhận Human-in-the-loop (HITL) trực tiếp trên giao diện CLI.

---

## 5. Quy trình cấu hình và Cập nhật luật lọc dữ liệu (Rules configuration)

Học viên có thể cấu hình cập nhật danh sách các thực thể PII cần lọc bằng cách chỉnh sửa từ khóa hoặc thay thế mẫu Regex trong hàm khởi tạo luật của mã nguồn `anonymizer.py`:

```python
# Cấu hình Regex tùy biến trong mã nguồn
PII_PATTERNS = {
    "CCCD": r"\b\d{12}\b", # Luật lọc số Căn cước công dân 12 số
    "PHONE_NUMBER": r"\b(0[3|5|7|8|9])\d{8}\b", # Luật lọc số điện thoại di động Việt Nam
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
}
```

---

## 6. Xử lý nhật ký lỗi và Khắc phục sự cố (Troubleshooting)

### Các mã lỗi thường gặp và Giải pháp:

| Mã lỗi / Trạng thái | Nguyên nhân | Hướng khắc phục |
| :--- | :--- | :--- |
| **`ConnectionError: Failed to connect to Ollama`** | Máy chủ Ollama chưa được bật hoặc đang cấu hình sai cổng. | 1. Mở terminal mới chạy lệnh `ollama serve`. <br>2. Kiểm tra xem Ollama có phản hồi tại cổng 11434 bằng cách gõ `curl http://127.0.0.1:11434` trên trình duyệt. |
| **`FileNotFoundError`** | Không tìm thấy tệp đầu vào tại đường dẫn chỉ định. | Kiểm tra lại đường dẫn tệp tin đầu vào xem đã chính xác chưa. Nên dùng đường dẫn tuyệt đối. |
| **`JSONDecodeError`** | Mô hình cục bộ phản hồi đầu ra không đúng định dạng JSON Schema cấu trúc. | 1. Tối ưu hóa System Prompt trong mã nguồn để ép mô hình phản hồi đúng định dạng.<br>2. Kiểm tra tài nguyên RAM máy tính, nếu RAM quá tải mô hình có thể in ra kết quả rác hoặc cắt cụt. |
| **`Out of Memory (OOM)`** | Máy tính bị tràn RAM khi đang chạy mô hình suy luận. | Tắt các ứng dụng chạy ngầm không cần thiết. Đổi cấu hình sang mô hình nhẹ hơn trong tệp `.env` (ví dụ: `qwen3.5:1.5b-instruct`). |

### Hướng dẫn kiểm tra nhật ký log:
Toàn bộ hoạt động và cảnh báo của hệ thống được lưu tự động vào tệp `logs/anonymizer.log`. Đội ngũ vận hành có thể giám sát liên tục log bằng lệnh PowerShell sau:

```powershell
Get-Content -Path .\logs\anonymizer.log -Wait -Tail 20
```
