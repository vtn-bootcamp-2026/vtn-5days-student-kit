# Safety Checklist — Xác nhận an toàn vận hành Agent
**Nhóm:** ______________   **Ca thực hành:** Buổi 08 - Hermes Basic   **Ngày:** ____________

> [!IMPORTANT]
> Mẫu này dùng cho Session 08 - Hermes Basic. Học viên điền và nộp cùng `runbook-log.json` để xác nhận đã hoàn thành xóa bộ nhớ (Memory Clear Protocol) và không rò rỉ dữ liệu.

---

## A. Bảo mật dữ liệu & API Key
- [ ] **A1.** Toàn bộ dữ liệu đưa cho Agent là dữ liệu giả lập trong `synthetic-data/` — không upload dữ liệu thật / PII / bí mật vận hành VTN lên Cloud API.
- [ ] **A2.** API Key (OpenRouter hoặc Google AI Studio) chỉ lưu cục bộ trong cấu hình bảo mật của Hermes Client — không dán vào `SOUL.md`, `README.md`, `runbook-log.json` hoặc kênh chung.
- [ ] **A3.** Đã rà soát các tệp nộp bài (SOUL.md, Skill, runbook-log.json, Safety Checklist) không chứa chuỗi API Key.

## B. Phê duyệt bởi con người (HITL)
- [ ] **B1.** Agent không tự ý phê duyệt tạm ứng / chi tiêu vượt hạn mức (30 triệu đồng / mức Cao theo QC-HC-05).
- [ ] **B2.** Mọi quyết định nhạy cảm đã được chuyển cho Trưởng phòng duyệt thủ công (HITL).

## C. Memory Clear Protocol (Bắt buộc nghiệm thu)
- [ ] **C1.** Đã nhấp **Clear Chat / New Session** trên giao diện Hermes Client cho cả 2 Profile.
- [ ] **C2.** Đã tắt hẳn ứng dụng Hermes Desktop Client (kiểm tra System Tray / Task Manager) trước khi xóa tệp vật lý.
- [ ] **C3.** Đã chạy lệnh PowerShell xóa tệp trạng thái SQLite thành công:
      ```powershell
      Remove-Item -Path "$HOME\.hermes\profiles\hr_admin_assistant\state.db" -ErrorAction SilentlyContinue
      Remove-Item -Path "$HOME\.hermes\profiles\hr_admin_assistant\hermes.db" -ErrorAction SilentlyContinue
      ```
- [ ] **C4.** Đã làm tương tự cho Profile `hr_recruitment_assistant` (nếu có state.db / hermes.db riêng).
- [ ] **C5.** Đã khởi động lại Hermes Client và xác nhận 2 Trợ lý bị xóa sạch ký ức phiên cũ.

## D. Bàn giao
- [ ] **D1.** Đã nộp đủ 6 sản phẩm: 2 SOUL.md, 1 Skill, 3 Test Cases, 1 runbook-log.json, 1 Safety Checklist.
- [ ] **D2.** Đạt 3/3 test case bắt buộc (đủ dữ liệu / thiếu dữ liệu / ngoài phạm vi).

---

**Ký xác nhận nhóm trưởng:** __________________   **Chấm chéo bởi nhóm:** ______________
