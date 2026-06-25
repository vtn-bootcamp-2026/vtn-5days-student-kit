---
mo-ta: Prompt yêu cầu Antigravity thiết lập và thực hiện xác thực kỹ năng vibe-notebooklm-orchestrator lần đầu để truy cập NotebookLM
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-25 07:43 +07:00
updated-at: 2026-06-25 07:44 +07:00
---
# Prompt 6: Thiết lập và xác thực kỹ năng kết nối NotebookLM (Vibe NotebookLM skill setup & auth)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn thiết lập và thực hiện xác thực (xác thực: authentication) cho kỹ năng kết nối NotebookLM: `vibe-notebooklm-orchestrator` để lưu thông tin truy cập (thông tin truy cập: access state) trên máy tính của tôi.

Hãy giúp tôi thực hiện các yêu cầu sau:

1. **Khởi tạo và cài đặt môi trường (cài đặt môi trường: environment setup):**
   Chạy các lệnh thiết lập lần đầu cho kỹ năng `vibe-notebooklm-orchestrator` tại đường dẫn `03-practice/session-07/skills/vibe-notebooklm-orchestrator/`:
   ```bash
   bash 03-practice/session-07/skills/vibe-notebooklm-orchestrator/run.sh setup
   03-practice/session-07/skills/vibe-notebooklm-orchestrator/lib/notebooklm/.venv/bin/patchright install chrome
```

2. **Xác thực quyền truy cập NotebookLM (xác thực quyền truy cập: access authentication):**
   Khởi động quy trình xác thực bằng cách chạy lệnh sau. Lưu ý: lệnh này sẽ mở một trình duyệt Chrome tự động hóa (automated Chrome browser) để tôi đăng nhập vào tài khoản Google của mình. Hãy chạy lệnh:

   ```bash
   bash 03-practice/session-07/skills/vibe-notebooklm-orchestrator/run.sh notebooklm auth_manager setup
   ```
3. **Kiểm tra trạng thái xác thực (trạng thái xác thực: authentication status):**
   Sau khi tôi hoàn tất đăng nhập trên trình duyệt và đóng lại, hãy kiểm tra lại trạng thái xác thực để đảm bảo thông tin truy cập (session/auth state) đã được lưu thành công vào thư mục `03-practice/session-07/skills/vibe-notebooklm-orchestrator/lib/notebooklm/data/`:

   ```bash
   bash 03-practice/session-07/skills/vibe-notebooklm-orchestrator/run.sh notebooklm auth_manager status
   ```

Hãy thực thi các lệnh trên, hướng dẫn tôi các bước thao tác trên màn hình (nếu có) và báo cáo kết quả chi tiết cho tôi.

```
```
