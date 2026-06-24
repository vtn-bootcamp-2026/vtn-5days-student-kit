---
mo-ta: Lời nhắc để AI tạo cấu trúc skill_design.md theo mô hình IPO cho bài toán rà soát hợp đồng
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 22:45 +07:00
updated-at: 2026-06-23 22:45 +07:00
---

# Lời nhắc tạo thiết kế kỹ năng (skill_design.md)

Hãy sao chép toàn bộ nội dung trong ô dưới đây và dán vào **Antigravity** hoặc **Codex** / **Claude** để tự động tạo bản thiết kế `skill_design.md` cho kỹ năng rà soát hợp đồng viễn thông.

```text
Bạn là một Workforce Architect. Nhiệm vụ: chuyển mô tả task tiếng Việt dưới đây thành một file `skill_design.md` theo cấu trúc IPO (Input – Process – Output), đủ chi tiết để một skill builder khác (vibe-aiworkforce) đọc và sinh ra gói skill chạy được.

### BỐI CẢNH
Tôi đang đóng gói một "nhân viên số" (skill) cho đội của mình. Tôi là kiến trúc sư — viết thiết kế bằng tiếng Việt; AI (bạn) là người thi hành. Môi trường: doanh nghiệp viễn thông, dữ liệu mô phỏng (không dùng dữ liệu thật/PII thật).

### MÔ TẢ TASK
Rà soát hợp đồng viễn thông: đọc file .docx, trích xuất điều khoản (ngày hiệu lực, SLA, phạt, gia hạn), phát hiện cờ đỏ, xuất JSON có dẫn chứng, chuyển người duyệt khi rủi ro cao.

### CHỈ DẪN
Viết file `skill_design.md` theo đúng 9 mục sau (không thêm mục lạ, không bỏ mục):
0. Thông tin chung (tên skill, 1 câu mô tả, người dùng)
1. Trigger — kích hoạt khi nào (loại file, từ khóa, ngữ cảnh)
2. Input — đầu vào (dữ liệu chính + knowledge base + điều kiện hợp lệ + dữ liệu cấm)
3. Process — xử lý (các bước theo intake→extract→validate→route, scripts gọi, công cụ AI vs code)
4. Output — đầu ra (file, schema với các trường cụ thể, trạng thái kết thúc)
5. Quality Gate — Do / Don't (mỗi bên ≥ 3 điều)
6. Human In the Loop — khi nào chuyển người duyệt, AI làm gì vs Human làm gì
7. Cấu trúc folder skill (SKILL.md, skill.json, schemas/, kb/, scripts/, data/, outputs/, tests/)
8. Test cases tối thiểu (≥ 3 ca: bình thường / thiếu trường / có cờ đỏ)

Nguyên tắc:
- Mỗi điều khoản/kết luận phải có source_evidence (không khẳng định suông).
- Tách rõ phần AI phán đoán (đọc hiểu) vs code thi hành tất định (kiểm schema, so khớp, ghi log).
- Triggers cụ thể, không chung chung.

### TIÊU CHUẨN ĐẦU RA
- 1 file markdown duy nhất.
- Mỗi mục có nội dung cụ thể cho task của tôi (không để `<...>` placeholder).
- Đủ chi tiết để vibe-aiworkforce đọc và build được folder skill mà không cần hỏi lại.
- Tiếng Việt, thuật ngữ kỹ thuật giữ tiếng Anh khi cần.
```
