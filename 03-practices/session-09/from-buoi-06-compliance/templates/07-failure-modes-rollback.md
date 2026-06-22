---
mo-ta: "Biểu mẫu phân tích các tình huống lỗi và phương án khôi phục/dự phòng cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.3
created-at: 2026-05-26 07:15 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Phân tích tình huống lỗi và Phương án ứng phó (Failure modes & Rollback/Fallback)

*   **Tên công cụ/dự án:** Mini Tool Anonymizer (Ẩn danh dữ liệu PII)
*   **Nhóm chịu trách nhiệm:** [Điền tên nhóm]
*   **Ngày cập nhật cuối cùng:** [Điền ngày]

---

## 1. Định nghĩa và Mục đích

Bảng phân tích các tình huống lỗi (Failure modes) và phương án ứng phó (Rollback/Fallback) giúp đội ngũ vận hành kỹ thuật tại **Viettel Net** chủ động kiểm soát rủi ro, duy trì tính ổn định của hệ thống và bảo vệ dữ liệu cá nhân ngay cả khi gặp sự cố phần cứng, phần mềm hoặc bị tấn công mạng.

---

## 2. Bảng phân tích các tình huống lỗi kỹ thuật (Failure modes analysis)

Học viên điền các kịch bản lỗi hệ thống phát sinh trong quá trình vận hành thực tế và giải pháp xử lý tương ứng:

### Tình huống lỗi 1: Mất kết nối tới máy chủ mô hình cục bộ (Local LLM connection failure)
*   **Mô tả sự cố:** Script chạy nhưng không kết nối được tới Ollama (cổng 11434), gây lỗi crash chương trình.
*   **Mức độ nghiêm trọng (S):** Cao (High - Hệ thống ngừng hoạt động hoàn toàn).
*   **Tác động kinh doanh:** Người dùng không thể lọc dữ liệu nhạy cảm của văn bản báo cáo.
*   **Phương án Fallback dự phòng lập tức:**
    *   *Bước 1:* Bắt lỗi `try-except` trong mã nguồn đối với hàm gọi API của Ollama.
    *   *Bước 2:* Nếu kết nối thất bại, tự động chuyển sang chế độ **"Fallback Rule-based Mode"** (Chỉ chạy các bộ lọc Regex cứng offline để phát hiện CCCD, Điện thoại, Email và bỏ qua phần suy luận ngữ cảnh lắt léo của LLM).
    *   *Bước 3:* In ra cảnh báo màu đỏ trên giao diện người dùng: `[WARNING: FALLBACK MODE ACTIVATED - ONLY REGEX FILTERS APPLIED]`.

---

### Tình huống lỗi 2: Tràn bộ nhớ RAM hệ điều hành khi chạy mô hình lớn (Out of memory - OOM)
*   **Mô tả sự cố:** Khi người dùng gửi văn bản quá dài hoặc máy chạy song song ứng dụng nặng, RAM bị đẩy lên 100%, hệ điều hành tự động kill tiến trình Ollama/Python.
*   **Mức độ nghiêm trọng (S):** Cao (High - Sập máy trạm vật lý).
*   **Tác động kinh doanh:** Gián đoạn công việc của nhân viên nghiệp vụ, có nguy cơ làm mất file văn bản gốc đang xử lý.
*   **Phương án ứng phó và Fallback:**
    *   *Bước 1 (Giới hạn tài nguyên):* Cấu hình giới hạn kích thước văn bản đầu vào tối đa trong file code (ví dụ: tối đa 50.000 ký tự cho mỗi lần lọc).
    *   *Bước 2 (Chuyển đổi mô hình tự động):* Nếu phát hiện lỗi trễ phản hồi > 30 giây hoặc RAM vượt ngưỡng 90%, tự động giải phóng bộ nhớ và chuyển đổi cấu hình sang các dòng mô hình siêu nhẹ như `qwen3.5:1.5b-instruct` hoặc `gemma4:e2b` (lượng tử hóa cao) hoặc chuyển hẳn sang bộ lọc Regex offline.

---

### Tình huống lỗi 3: Lọc sót thông tin nhạy cảm của nhân sự (Data leakage due to AI omission)
*   **Mô tả sự cố:** Mô hình LLM không nhận diện được một tên riêng lắt léo (ví dụ: tên viết tắt hoặc tên không chuẩn) dẫn đến việc in thẳng tên thật ra báo cáo public.
*   **Mức độ nghiêm trọng (S):** Cực kỳ nghiêm trọng (Critical - Vi phạm quy chế bảo mật của VTN và Luật bảo vệ dữ liệu cá nhân Nghị định 356/2025/NĐ-CP).
*   **Tác động kinh doanh:** Nguy cơ rò rỉ dữ liệu nhân sự ra bên ngoài, ảnh hưởng uy tín của tập đoàn.
*   **Phương án kiểm soát và Khắc phục (Rollback/HITL):**
    *   *Bước 1 (Human-in-the-loop):* Bắt buộc hiển thị bảng so sánh "trước và sau khi ẩn danh" trên màn hình cho người dùng phê duyệt trước khi ghi đè file lưu.
    *   *Bước 2 (Rollback dữ liệu):* Nếu người dùng phát hiện sót thông tin nhạy cảm ở bản báo cáo đã lưu, kích hoạt quy trình **"Log Clear & File Revocation"**: Xóa ngay lập tức file lỗi khỏi thư mục dùng chung, thu hồi email gửi lỗi, và sử dụng tính năng ghi đè thủ công (Manual override) để ép bộ lọc ẩn danh từ khóa đó trong các lần tiếp theo.

---

## 3. Quy trình khôi phục phiên bản mã nguồn cũ (Rollback runbook)

Khi phát hiện phiên bản mã nguồn mới nâng cấp gặp lỗi nghiêm trọng (ví dụ lỗi bảo mật, sập hệ thống liên tục), đội ngũ kỹ thuật thực hiện quy trình Rollback phiên bản theo các bước sau:

```powershell
# Bước 1: Lưu trữ phiên bản lỗi hiện tại vào thư mục tạm để phân tích
mv .\anonymizer.py .\logs\anonymizer_failed_v1.1.py

# Bước 2: Khôi phục phiên bản ổn định gần nhất từ Git hoặc từ backup
git checkout HEAD -- .\anonymizer.py

# Bước 3: Khởi động lại dịch vụ Ollama cục bộ để giải phóng RAM
Restart-Service -Name "Ollama"

# Bước 4: Chạy thử lại bộ 10 ca kiểm thử (TC-01 đến TC-10) để xác nhận hệ thống đã hoạt động bình thường
python anonymizer.py --input .\synthetic-data\edge-cases-sample.txt --output .\outputs\test-result.txt
```
