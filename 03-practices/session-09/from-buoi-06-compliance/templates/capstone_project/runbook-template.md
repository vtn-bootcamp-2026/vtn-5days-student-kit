---
mo-ta: "Biểu mẫu hướng dẫn vận hành công cụ NetSaveAI cho Admin NOC VTN"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-26 07:10 +07:00
updated-at: 2026-06-10 15:55 +07:00
---

# Hướng dẫn vận hành hệ thống: NetSaveAI (Runbook)

*   **Mã tài liệu:** VTN-RB-NETSAVEAI-01
*   **Người biên soạn:** [Điền tên nhóm/cá nhân]
*   **Đơn vị phê duyệt:** Trung tâm Vận hành khai thác mạng (NOC) / Viettel Net
*   **Phiên bản hệ thống áp dụng:** v1.0

---

## 1. Tổng quan hệ thống (System overview)

Tài liệu này hướng dẫn cài đặt, cấu hình, quản trị tài liệu RAG và xử lý sự cố đối với **NetSaveAI** - Chatbot RAG hỗ trợ kỹ sư trực ca tìm kiếm tài liệu nghiệp vụ (PA, MOP, Checklist) và trích xuất quy trình/câu lệnh CLI xử lý sự cố mạng viễn thông.

---

## 2. Yêu cầu hệ thống và Chuẩn bị môi trường (Prerequisites)

### Yêu cầu phần cứng máy chủ (NOC Server):
*   **RAM:** Tối thiểu 32 GB (Để chạy mượt mà cả Ollama và Vector DB).
*   **CPU/GPU:** Tối thiểu 8 Cores (Khuyến nghị có thẻ GPU Nvidia T4/A10 để tăng tốc inference LLM).
*   **Ổ cứng trống:** Tối thiểu 50 GB SSD lưu trữ tài liệu mạng và models.
*   **Mạng:** Chạy trên dải IP LAN quản trị, hoàn toàn block truy cập ra Internet.

### Yêu cầu phần mềm cài đặt sẵn:
1.  **Docker & Docker Compose:** Cài đặt bản mới nhất.
2.  **Ollama:** Cài đặt trực tiếp trên host hoặc qua container.
3.  **Tải mô hình (Thực hiện qua proxy hoặc tải offline):**
    ```bash
    ollama pull qwen3.5:1.5b-instruct
    # Hoặc nếu server mạnh:
    ollama pull batiai/gemma4-e4b:q4
    ```

---

## 3. Quy trình cài đặt và Khởi động (Deployment steps)

### Bước 1: Khởi tạo hệ thống bằng Docker Compose
Di chuyển vào thư mục chứa source code của hệ thống và chạy lệnh build:

```bash
cd /opt/netsaveai/
docker-compose up -d --build
```
*Lệnh này sẽ khởi chạy 3 container: (1) Vector DB Milvus, (2) Backend FastAPI, (3) Frontend Streamlit/React.*

### Bước 2: Kiểm tra trạng thái dịch vụ
Đảm bảo tất cả các container đều đang trạng thái `Up`:

```bash
docker ps
```

### Bước 3: Đăng nhập giao diện quản trị (Admin)
Mở trình duyệt, truy cập vào IP của server: `http://10.x.x.x:8080/admin`
Đăng nhập bằng tài khoản SSO nội bộ dành cho Admin NOC.

---

## 4. Hướng dẫn Quản trị Dữ liệu Tài liệu (Admin Guide)

Để Chatbot có dữ liệu trả lời, Quản trị viên (Trưởng ca/Admin) cần thực hiện đẩy file (Ingestion) vào Vector DB:

### Upload và Lập chỉ mục tài liệu MOP mới (Indexing):
1.  Truy cập tab **[Tài liệu & Tri thức]** trên Web UI.
2.  Bấm nút **[Upload Files]** và chọn các file Excel/Word chứa kịch bản MOP (VD: `PA_GGSN_UCTT_v2.xlsx`).
3.  Chọn loại **Profile mạng** tương ứng ở menu thả xuống (Ví dụ: `PS_Core_GGSN`). Đây là bước bắt buộc để hệ thống phân mảng Vector.
4.  Bấm **[Lập chỉ mục]** (Start Indexing). 
5.  Chờ khoảng 30 giây - 1 phút. Quá trình xử lý chunking, tạo vector embedding và insert vào Milvus DB sẽ chạy ngầm.
6.  *Lưu ý:* Chatbot sẽ lập tức đọc được dữ liệu mới ngay khi tiến trình báo 100% (Không cần khởi động lại app).

### Xóa/Cập nhật tài liệu cũ:
Khi có bản MOP mới thay thế bản cũ, Admin vào danh sách tài liệu, tìm bản cũ (`v1.0`), bấm biểu tượng **[Thùng rác]** để xóa Vector tương ứng, sau đó upload bản mới (`v2.0`).

---

## 5. Xử lý nhật ký lỗi và Khắc phục sự cố (Troubleshooting)

### Các mã lỗi thường gặp và Giải pháp:

| Trạng thái / Hiện tượng | Nguyên nhân | Hướng khắc phục |
| :--- | :--- | :--- |
| **Chatbot báo: "Lỗi kết nối đến LLM Engine"** | Container Ollama bị crash hoặc bị Firewall nội bộ chặn cổng 11434. | 1. Chạy lệnh `systemctl status ollama` trên host.<br>2. Thử curl `http://localhost:11434`. |
| **Tìm không ra kết quả (Dù file MOP có chứa từ khóa)** | Vector DB chưa được index xong hoặc lỗi đọc file Excel do sai format table. | Admin vào tab Debug, kiểm tra xem file Excel đó có trạng thái "Indexed: Success" hay "Failed". Nếu Failed, chuyển file Excel về định dạng chuẩn (bỏ merge cells) và upload lại. |
| **LLM trả lời lặp từ, sinh ký tự lạ** | Tham số Temperature bị cấu hình sai hoặc RAM server cạn kiệt. | Chỉnh sửa file `.env`: `LLM_TEMPERATURE=0.1`. Khởi động lại container backend: `docker restart netsaveai-backend`. |
| **Mạng chậm, UI xoay tròn quá 1 phút** | Server đang xử lý đồng thời quá nhiều câu hỏi (Queue đầy). | Theo dõi RAM/CPU bằng lệnh `htop`. Nếu thường xuyên xảy ra, cần scale-up tài nguyên máy chủ NOC. |

### Hướng dẫn kiểm tra nhật ký log:
Để trace luồng RAG và lý do AI trả lời sai lệnh, Admin có thể đọc log hệ thống:

```bash
# Xem log Real-time của bộ xử lý Backend
docker logs -f netsaveai-backend
```
