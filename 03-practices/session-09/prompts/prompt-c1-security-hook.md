---
mo-ta: "Prompt C1 — Concept 2: Hook bảo mật lớp cứng cho học viên non-tech"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 08:00 +07:00
updated-at: 2026-06-26 08:00 +07:00
---

# Prompt C1: Concept 2 — Hook bảo mật lớp cứng

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```text
BỐI CẢNH:
Tiếp tục. "Vệ sĩ" cần một "bảo vệ cửa" (hook) chặn mọi thao tác ghi/xoá file ngoài thư mục outputs/kb/schemas.
Đã có mẫu: templates/scripts/hook.py.

CHỈ DẪN:
1. Tạo vp-vtn-office-guard/scripts/hook.py dựa trên mẫu (chặn write_file/patch/terminal/process/
   execute_code/delete_file ngoài thư mục an toàn outputs|kb|schemas; luôn cho phép read/search).
2. Gắn ghi chú trong SKILL.md mục "Boundaries": "Mọi thao tác ghi chỉ trong outputs/; Hook chặn phần còn lại".
3. CHẠY 2 phép thử và cho tôi kết quả:
   - Thử ghi ra /etc/passwd  → phải là {"action":"block",...}
   - Thử ghi ra outputs/ok.txt → phải là {"action":"allow"}

TIÊU CHUẨN ĐẦU RA:
- File hook.py hoạt động. 2 phép thử trả đúng kết quả. In bằng chứng ra màn hình.
```

**Kết quả kỳ vọng:** `/etc/passwd` → `block`; `outputs/ok.txt` → `allow`.
