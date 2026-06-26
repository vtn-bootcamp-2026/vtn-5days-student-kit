---
mo-ta: "Prompt A — Dựng bộ khung Skill Package cho học viên non-tech"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 08:00 +07:00
updated-at: 2026-06-26 08:00 +07:00
---

# Prompt A: Dựng bộ khung Skill Package

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```text
BỐI CẢNH:
Tôi đang học xây "Vệ sĩ văn phòng VTN" — một Skill chạy trong Antigravity để ẩn danh
thông tin cá nhân (PII) trong tài liệu văn phòng, không dùng LLM API ngoài.
Thư mục làm việc: 03-practice/session-09/. Đã có sẵn:
- templates/SKILL.md, templates/skill.json (template chưa điền)
- templates/office-guard-starter.py (mã khởi điểm)
- templates/kb/pii-categories.md, templates/kb/safe-terms.md

CHỈ DẪN:
1. Tạo cấu trúc Skill Package tên `vp-vtn-office-guard/` ở thư mục gốc session-09.
2. Sao chép templates/SKILL.md và templates/skill.json vào đó, rồi ĐIỀN phần {placeholder}:
   - Persona: "Vệ sĩ ẩn danh tài liệu văn phòng VTN".
   - Author = "Nhóm {điền tên nhóm}". Điền các trigger/giới hạn đúng như template gợi ý.
3. Tạo thư mục `outputs/` rỗng (để Skill ghi kết quả).
KHÔNG sinh mã phức tạp, KHÔNG cài thư viện ngoài.

TIÊU CHUẨN ĐẦU RA:
- Thư mục vp-vtn-office-guard/ có: SKILL.md (đã điền), skill.json (đã điền), outputs/.
- In danh sách file đã tạo để tôi kiểm tra.
```

**Kết quả kỳ vọng:** Có thư mục `vp-vtn-office-guard/` chứa `SKILL.md` + `skill.json` đã điền tên nhóm.
