---
mo-ta: ban do luong thuc hanh v5.1 (non-tech, 10 session x 3h30)
trang-thai: active
phien-ban: v5.1
updated-at: 2026-06-20 +07:00
---

# Bản đồ thực hành (v5.1 — non-tech, 10 Session × 3h30)

| Session | Ngày | Chủ đề | Lab chính (artifact) | Đầu ra bàn giao |
|---|---|---|---|---|
| S1 | Ngày 1 | Làm chủ công cụ AI: Antigravity + Codex (free 1 tháng) + Git + Skill — và chọn bài toán | Setup toolkit & chọn bài toán | Workspace AI (Antigravity+Codex+Git) đã setup, prompt chuẩn,… |
| S2 | Ngày 1 | Xây dựng workflow: hiện trạng + ESIA + Mermaid + render ảnh | Thiết kế workflow cho bài toán đã chọn | Workflow design doc (hiện trạng + ESIA + Mermaid + ảnh rende… |
| S3 | Ngày 2 | n8n Phần A — cài đặt, node cơ bản, node LLM | Sinh nội dung tự động vào Google Sheet | Kinh nghiệm node n8n + node LLM → dựng luồng tổng hợp báo cá… |
| S4 | Ngày 2 | n8n Phần B — định tuyến, HITL, xử lý lỗi (lab tổng hợp báo cáo chuẩn) | Tổng hợp báo cáo theo format chuẩn | Workflow 3 nhánh (Auto/HITL/Unknown) + báo cáo chuẩn → patte… |
| S5 | Ngày 3 | AI Agent & Vibe Working — đóng gói chuyên môn thành Skill/Agent | Đóng gói skill nghiệp vụ (kế toán / văn phòng) | Agent/Skill đã đóng gói (schema + kb + validate) → cho 'nhân… |
| S6 | Ngày 3 | RAG Phần A — naive RAG: BM25 + vector, embedding, chunk | Naive RAG no-code trên NotebookLM | KB + hiểu vector vs BM25 → kết hợp hybrid + NotebookLM + tíc… |
| S7 | Ngày 4 | RAG Phần B — **Advanced RAG** (Query Rewriting · HyDE · Multi-hop via LangGraph) + Agent + NotebookLM second brain (no-code) | Advanced RAG + Agent + NotebookLM (no-code) | Agent tích hợp Advanced RAG + NotebookLM second brain → tạo trợ lý cá nhâ… (🧩 skill vibe-notebooklm = Hộp nâng cao) |
| S8 | Ngày 4 | **Personal Agent (Hermes) + local AI + SOUL.md** *(nhẹ)* | Trợ lý cá nhân chạy local (profile + SOUL) | Personal Agent chạy local → S9 |
| S9 | Ngày 5 | **Anonymizer + Hook (bảo mật 2 lớp) + chống prompt injection** *(mới, kế thừa vtn-2026)* | Anonymizer mini-tool + test prompt injection | Anonymizer + Hook + compliance checklist → S10 |
| S10 | Ngày 5 | **Capstone** | Bài toán non-tech end-to-end | Implementation Kit + presentation |

**Nguyên tắc thực hành:** không dùng dữ liệu thật · luôn có điểm con người kiểm duyệt (HITL) · tính toán quan trọng dùng code/bảng tính · mọi đầu ra có tiêu chí nghiệm thu · mọi workflow có rủi ro phải có nhánh dừng an toàn.

> Cấu trúc cũ (3 ngày/6 session tech) đã archive tại `../99-archive/v3-6session-tech/`.