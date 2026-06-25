---
mo-ta: "Biểu mẫu phân tích các tình huống lỗi và phương án khôi phục/dự phòng cho hệ thống NetSaveAI"
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-26 07:15 +07:00
updated-at: 2026-06-10 15:55 +07:00
---

# Phân tích tình huống lỗi và Phương án ứng phó (Failure modes & Rollback/Fallback)

*   **Tên công cụ/dự án:** NetSaveAI — Chatbot RAG cho Vận Hành Mạng Viễn Thông
*   **Nhóm chịu trách nhiệm:** Nhóm AI Builders - Trung tâm Vận hành khai thác mạng (NOC)
*   **Ngày cập nhật cuối cùng:** [Điền ngày]

---

## 1. Định nghĩa và Mục đích

Bảng phân tích các tình huống lỗi (Failure modes) và phương án ứng phó (Rollback/Fallback) giúp đội ngũ vận hành và quản trị viên hệ thống chủ động kiểm soát rủi ro, đảm bảo hệ thống tra cứu RAG NetSaveAI luôn phục vụ tốt cho kỹ sư trực ca, ngăn chặn các rủi ro cung cấp sai quy trình dẫn đến thao tác lỗi trên thiết bị mạng thực tế.

---

## 2. Bảng phân tích các tình huống lỗi kỹ thuật (Failure modes analysis)

### Tình huống lỗi 1: Hybrid Search trả về sai tài liệu/sai mạng (Wrong Document Retrieved)
*   **Mô tả sự cố:** Kỹ sư tìm quy trình "cô lập node SGHL04 4G", nhưng Vector Search lại trả về đoạn tài liệu của node SGHL04 mạng 3G, dẫn đến LLM tổng hợp các lệnh CLI của mạng 3G.
*   **Mức độ nghiêm trọng (S):** Cực kỳ nghiêm trọng (Critical - Kỹ sư có thể gõ nhầm lệnh 3G vào mạng 4G gây rớt dịch vụ diện rộng).
*   **Tác động kinh doanh:** Thao tác sai trên thiết bị core gây downtime, ảnh hưởng chất lượng dịch vụ của hàng triệu thuê bao.
*   **Phương án kiểm soát & Fallback (Hard-filter):**
    *   *Bước 1 (Kỹ thuật phòng ngừa):* Không chỉ dựa vào vector semantics (ngữ nghĩa), bắt buộc Query Analyzer phải trích xuất từ "4G" thành bộ lọc metadata (Must_Contain). Engine Vector DB sẽ loại bỏ (filter out) toàn bộ các hàng dữ liệu có chứa tag "3G".
    *   *Bước 2 (Human-in-the-loop):* Bắt buộc hiển thị Tên File, Tên Sheet và Hàng/Dòng ngay dưới kết quả. Giao diện có dòng cảnh báo màu đỏ: `"LƯU Ý: Kỹ sư phải kiểm tra lại file tài liệu gốc được trích dẫn ở dưới trước khi copy lệnh vào thiết bị."`

---

### Tình huống lỗi 2: Ảo giác sinh lệnh không tồn tại (LLM CLI Hallucination)
*   **Mô tả sự cố:** Document gốc chứa một lệnh rất dài, nhưng LLM do bản chất sinh token tự động đã "cắt gọt" hoặc "sáng tạo" ra một tham số lệnh CLI lạ không có trong tài liệu gốc.
*   **Mức độ nghiêm trọng (S):** Cao (High - Gõ lệnh lạ có thể bị báo lỗi syntax hoặc thiết bị bị treo).
*   **Tác động kinh doanh:** Kỹ sư mất thời gian debug lệnh, làm chậm tiến độ xử lý sự cố.
*   **Phương án ứng phó và Fallback:**
    *   *Bước 1:* Thiết lập tham số Temperature = 0.0 hoặc 0.1 cho mô hình LLM để ép mô hình trả về nội dung deterministic (ít sáng tạo nhất có thể).
    *   *Bước 2:* Tối ưu System Prompt nhấn mạnh: `KHÔNG thay đổi bất kỳ ký tự nào trong khối lệnh CLI, hãy copy-paste nguyên văn từ <context>`.
    *   *Bước 3 (Fallback):* Nếu kỹ sư phát hiện lệnh không giống thường lệ, bấm nút "Báo lỗi câu trả lời này" trên UI để gửi log (gồm câu hỏi, chunk trả về, prompt) đến Admin. Kỹ sư mở file Excel MOP gốc được đính kèm để dùng lệnh gốc.

---

### Tình huống lỗi 3: Mất kết nối DB / Quá tải Local LLM Server (Service Outage)
*   **Mô tả sự cố:** Hệ thống Vector DB (Milvus/FAISS) bị crash hoặc server chạy Ollama hết RAM GPU/CPU khi nhiều kỹ sư cùng lúc hỏi chatbot trong một ca trực lớn. Hệ thống trả về lỗi timeout.
*   **Mức độ nghiêm trọng (S):** Trung bình (Medium - Công cụ AI bị hỏng, nhưng thiết bị viễn thông không bị ảnh hưởng).
*   **Tác động kinh doanh:** Kỹ sư không dùng được chatbot, phải quay về phương pháp tìm file MOP thủ công trong thư mục máy tính.
*   **Phương án Fallback dự phòng lập tức:**
    *   *Bước 1:* Bắt lỗi Timeout/Connection Error trên Web UI.
    *   *Bước 2:* Nếu Chatbot RAG sập, hiển thị popup: `[Hệ thống AI đang quá tải. Vui lòng truy cập Kho Tài Liệu MOP dự phòng tại dải IP: 10.x.x.x để tra cứu thủ công]`.
    *   *Bước 3:* Quản trị viên theo dõi Grafana/Zabbix, thiết lập rule tự động restart container Ollama và Vector DB nếu RAM > 95%.

---

## 3. Quy trình khôi phục phiên bản tài liệu RAG cũ (Vector DB Rollback runbook)

Khi có đợt nâng cấp thiết bị mạng mới, Admin upload file PA/MOP v2.0 vào hệ thống NetSaveAI. Tuy nhiên, nếu phát hiện file v2.0 bị lỗi cấu trúc khiến Chatbot đọc sai dòng, Admin cần thực hiện Rollback Vector DB về bản v1.0 như sau:

```powershell
# Bước 1: Liệt kê các collection index tài liệu hiện tại trong Vector DB
python vector_admin.py --list-collections --target GGSN_PA_Profile

# Bước 2: Xóa collection bị lỗi (v2.0)
python vector_admin.py --delete-collection --name GGSN_PA_v2.0_20260610

# Bước 3: Khôi phục lại collection ổn định trước đó làm index chính (v1.0)
python vector_admin.py --set-active-collection --name GGSN_PA_v1.0_20260101

# Bước 4: Test thử lại nghiệm thu bằng một câu truy vấn cắt chuyển
python cli_test.py --query "Quy trình cắt chuyển SGHL04" --expected-file "PA_GGSN_v1.0.xlsx"
```
