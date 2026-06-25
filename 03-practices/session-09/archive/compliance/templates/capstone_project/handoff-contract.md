---
mo-ta: "Biểu mẫu biên bản bàn giao kỹ thuật Handoff Contract cho hệ thống NetSaveAI"
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 07:25 +07:00
updated-at: 2026-06-10 15:55 +07:00
---

# Biên bản bàn giao kỹ thuật (Handoff contract)

*   **Dự án ứng dụng:** NetSaveAI — Chatbot RAG cho Vận Hành Mạng Viễn Thông
*   **Bên giao (Đơn vị phát triển):** Nhóm học viên AI Builders - [Điền tên nhóm]
*   **Bên nhận (Đơn vị vận hành/Người dùng):** Trung tâm Vận hành khai thác mạng (NOC) / Viettel Net
*   **Ngày ký kết bàn giao:** [Điền ngày]

---

## 1. Mục đích biên bản

Biên bản bàn giao kỹ thuật (Handoff contract) xác nhận việc chuyển giao toàn bộ mã nguồn hệ thống Chatbot RAG, cấu hình Vector Database, Model LLM offline, bộ dữ liệu test MOP/PA, tài liệu vận hành và cam kết bảo trì kỹ thuật của **NetSaveAI** từ nhóm phát triển sang đơn vị vận hành NOC, nhằm đảm bảo công cụ được tiếp quản, duy trì server và vận hành ổn định 24/7 phục vụ kỹ sư trực ca.

---

## 2. Danh mục các tài sản bàn giao (Deliverables)

Bên giao cam kết chuyển giao đầy đủ các cấu phần dưới đây cho Bên nhận:

| STT | Tên tài sản bàn giao | Định dạng / Đường dẫn | Trạng thái bàn giao | Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Mã nguồn RAG Backend | `app/api_router.py` | [Đầy đủ] | Viết bằng Python (FastAPI, Langchain), logic Hybrid Search. |
| 2 | Mã nguồn Frontend UI | `app/chat_ui.js` | [Đầy đủ] | Giao diện Chat nội bộ và giao diện Upload file cho Admin. |
| 3 | File cấu hình môi trường | `.env` | [Đầy đủ] | Chứa biến môi trường kết nối Ollama và Milvus/FAISS DB. |
| 4 | Bộ cài đặt Docker | `docker-compose.yml` | [Đầy đủ] | Đóng gói toàn bộ services để deploy 1 click lên NOC Server. |
| 5 | Tài liệu hướng dẫn vận hành | `runbook-template.md` | [Đầy đủ] | Hướng dẫn cài đặt, start/stop service, upload/index tài liệu. |
| 6 | Tài liệu tuân thủ bảo mật | `compliance-checklist.md` | [Đầy đủ] | Đánh giá tuân thủ an toàn thông tin 100% offline nội bộ mạng lõi. |
| 7 | Tệp dữ liệu MOP Demo | `data/sample_PA/` | [Đầy đủ] | Bộ file Excel MOP/PA mạng PS Core đã được làm sạch để test. |

---

## 3. Cam kết mức độ dịch vụ và Hỗ trợ kỹ thuật (SLA & Support guidelines)

Để đảm bảo hệ thống tra cứu tài liệu vận hành trơn tru sau bàn giao, hai bên thống nhất các điều khoản hỗ trợ kỹ thuật như sau:

### Trách nhiệm của Bên giao (Nhóm phát triển):
*   **Hỗ trợ kỹ thuật ban đầu:** Hỗ trợ Admin NOC cài đặt Docker, kéo mô hình Ollama (qwen3.5/gemma4) và cấu hình dải IP truy cập hợp lệ trong vòng **03 ngày làm việc** kể từ ngày ký biên bản.
*   **Sửa lỗi phát sinh khẩn cấp (Hotfix):** Cam kết xử lý các lỗi nghiêm trọng (Ví dụ: Hệ thống bị crash, trả về sai hoàn toàn tài liệu khác mạng lưới) trong vòng **24 giờ** kể từ khi nhận được thông báo.
*   **Chuyển giao tri thức:** Tổ chức 01 buổi hướng dẫn sử dụng (kéo dài 1 tiếng) cho các Trưởng ca/Admin NOC về cách đọc log lỗi và cách upload file Excel MOP mới để index vào Vector DB.

### Trách nhiệm của Bên nhận (Đơn vị tiếp nhận NOC):
*   **Chuẩn bị hạ tầng:** Đảm bảo cấp phát máy chủ nội bộ (Server) đáp ứng đúng yêu cầu phần cứng (RAM >= 32GB, khuyến nghị có GPU, CPU tối thiểu 8 Cores, cài sẵn Docker).
*   **Giám sát vận hành:** Thường xuyên kiểm tra tệp log hệ thống (`logs/rag_engine.log`) để chủ động phát hiện sự cố tràn RAM Vector DB.
*   **Cập nhật dữ liệu:** Admin NOC chịu trách nhiệm tải lên các phiên bản tài liệu PA/MOP mới nhất ngay sau mỗi đợt cutover, nâng cấp lớn của mạng lưới để AI không trả về dữ liệu cũ.

---

## 4. Xác nhận ký kết bàn giao

Hai bên cùng thống nhất các nội dung trên và cam kết thực hiện đúng trách nhiệm được giao.

**ĐẠI DIỆN BÊN GIAO (Nhóm phát triển)**  
*(Ký, ghi rõ họ tên)*  

<br><br><br>

**ĐẠI DIỆN BÊN NHẬN (Trung tâm NOC)**  
*(Ký, ghi rõ họ tên)*  
