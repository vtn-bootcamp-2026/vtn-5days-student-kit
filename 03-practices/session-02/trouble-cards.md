# Trouble Cards — Session 2

> Thẻ xử lý lỗi thường gặp. GV tải sẵn; khi nhóm stuck > 5 phút → rút thẻ phù hợp.

## Từ lab chính: Lab S2 — Thiết kế workflow cho bài toán đã chọn
- **Lỗi tổng:** Mermaid lỗi cú pháp → dán lỗi vào AI sửa; hoặc paste vào mermaid.live xem preview. Render ảnh mờ → thêm mô tả style vào prompt.

## Thẻ theo công cụ
### Antigravity
- **Workspace không kết nối cloud** → Đăng nhập lại; kiểm tra mạng; dùng Claude.ai web làm backup.
- **Skill không trigger** → Kiểm phần triggers trong skill.json; đảm bảo tên file SKILL.md ở root skill folder.
- **Output lệch schema** → Thêm ví dụ đúng/sai (few-shot) vào kb; yêu cầu AI 'chỉ trả JSON đúng schema'.

## Nguyên tắc cứu nhóm chậm
- Stuck > 5' → TA can thiệp, không để cả nhóm chờ.
- Không kịp xong → dùng **fallback**: Cung cấp design doc mẫu (HCNS/Marketing) để HV điền vào.
- Luôn giữ tinh thần: AI không judge, thử lại thoải mái.