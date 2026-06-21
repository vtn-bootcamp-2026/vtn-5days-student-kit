---
mo-ta: Prompt chuyên dụng cho tác tử Antigravity để tự động thay thế liên kết Google Sheet trong các tệp JSON checkpoints của bài thực hành
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-11 13:42 +07:00
updated-at: 2026-06-11 13:42 +07:00
---

# Chỉ thị tác vụ thay thế liên kết Google Sheet tự động trong các tệp checkpoints

Bạn là tác tử: agent coding AI Antigravity. Hãy thực hiện tác vụ tự động cập nhật liên kết trang tính Google: Google Sheet link trong toàn bộ các tệp mốc kiểm tra: checkpoints dạng JSON của bài thực hành.

## 1. Thông tin liên kết mới
- **Liên kết Google Sheet mới từ người dùng**: `{{NEW_GOOGLE_SHEET_URL}}`
*(Lưu ý: Người dùng sẽ cung cấp liên kết thực tế khi gọi prompt này. Nếu đây là lời nhắc trực tiếp, hãy lấy URL do người dùng cung cấp.)*

## 2. Quy trình xử lý tự động
Hãy thực hiện các bước sau một cách chính xác:

### Bước 2.1: Phân tích liên kết mới và trích xuất mã nhận diện: spreadsheet ID
- Phân tích liên kết mới do người dùng cung cấp và trích xuất chuỗi mã nhận diện: spreadsheet ID (chuỗi ký tự nằm giữa `/d/` và `/edit` hoặc `/view` trong URL).
  - *Ví dụ*: Từ `https://docs.google.com/spreadsheets/d/1DBS2rYiRQ3NzcHjg0zA_hURZDllfICnar9YDqSGzWwY/edit#gid=1733173600`, mã nhận diện trích xuất được là `1DBS2rYiRQ3NzcHjg0zA_hURZDllfICnar9YDqSGzWwY`.

### Bước 2.2: Xác định phạm vi và mã nhận diện cũ
- **Thư mục chứa các tệp checkpoints**: `03-practice/day-01/session-02-ai-workflow-smart-ticket-triage/templates/checkpoints/`
- **Các tệp cần xử lý**: Tất cả các tệp có định dạng `.json` trong thư mục trên (ví dụ: `checkpoint-step-2.json`, `checkpoint-step-3.json`, ..., `checkpoint-step-8.json`).
- **Mã nhận diện trang tính cũ cần tìm kiếm**: `1DBS2rYiRQ3NzcHjg0zA_hURZDllfICnar9YDqSGzWwY`

### Bước 2.3: Thực hiện thay thế chuỗi tự động
Đối với mỗi tệp `.json` trong danh sách:
1. Đọc nội dung tệp JSON.
2. Tìm kiếm tất cả các vị trí xuất hiện mã nhận diện cũ `1DBS2rYiRQ3NzcHjg0zA_hURZDllfICnar9YDqSGzWwY` và thay thế chúng bằng mã nhận diện mới đã trích xuất ở bước 2.1.
   - Cần thay thế chính xác giá trị của trường `"value"` (ví dụ: `"value": "MÃ_NHẬN_DIỆN_MỚI"`).
   - Cần thay thế mã nhận diện cũ trong các trường địa chỉ URL `"cachedResultUrl"` (ví dụ: `"cachedResultUrl": "https://docs.google.com/spreadsheets/d/MÃ_NHẬN_DIỆN_MỚI/edit..."`).
3. Đảm bảo cấu trúc cú pháp JSON của tệp không bị lỗi sau khi thay thế.
4. Lưu tệp với mã hóa UTF-8.

### Bước 2.4: Xác minh kết quả
- Kiểm tra xem các tệp JSON đã cập nhật có hợp lệ hay không (phân tích cú pháp: JSON parse).
- Ghi nhận và liệt kê danh sách tất cả các tệp đã cập nhật thành công kèm theo mã nhận diện mới để báo cáo cho người dùng.
