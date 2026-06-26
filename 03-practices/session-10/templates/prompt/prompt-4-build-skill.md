---
mo-ta: "Prompt 4 — Hướng dẫn sử dụng vibe-aiworkforce để sinh tự động mã nguồn và thư mục Skill"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 4: Xây dựng và đóng gói gói kỹ năng (Build Skill using vibe-aiworkforce)

Đây là bước thực thi kỹ thuật. Hãy sao chép chỉ dẫn dưới đây và gửi cho trợ lý ảo AI trên cửa sổ tương tác đầu lệnh (hoặc gọi trực tiếp subagent trong Antigravity) để bắt đầu quá trình tạo mã nguồn tự động:

```text
BỐI CẢNH:
Tôi đã hoàn thành tệp thiết kế kiến trúc skill `skill_design.md` ở thư mục hiện tại. Bây giờ tôi cần đóng gói và sinh mã nguồn tự động cho skill này theo chuẩn Session 5.

CHỈ DẪN:
Hãy sử dụng công cụ/subagent `vibe-aiworkforce` để tự động xây dựng gói skill (Skill Package) dựa trên file `skill_design.md` đã có.
- Tên thư mục skill: [tên-dự-án-kebab-case] (Ví dụ: `netsave-ai-censor`)
- COMPANY_ROOT: Cấu hình thư mục làm việc hiện tại của tôi (03-practice/session-10/templates/).
- Yêu cầu sinh đầy đủ các tệp cấu hình và mã nguồn:
  1. `SKILL.md` và `skill.json` (chứa triggers và permissions đọc/ghi cục bộ).
  2. Thư mục `schemas/` chứa tệp định dạng `.schema.json` để kiểm định JSON đầu ra.
  3. Thư mục `kb/` chứa các tệp tri thức nền tảng hỗ trợ.
  4. Thư mục `scripts/` chứa các tệp mã nguồn python: `intake.py` (đọc tệp đầu vào), `validator.py` (kiểm tra an toàn cấu trúc), `router.py` (điều hướng và phân vai con người).
  5. Thư mục `outputs/` rỗng để ghi nhận tệp tin kết quả sạch PII sau khi chạy.

TIÊU CHUẨN ĐẦU RA:
- In ra danh sách cấu trúc thư mục skill đã được tạo thành công để tôi kiểm tra.
- Xác nhận các script python đã được viết hoàn chỉnh các hàm cơ bản (đọc file, ghi log, gọi mô hình local qua Ollama) và không bị lỗi cú pháp.
```

**Kết quả kỳ vọng:** Thư mục skill của dự án (ví dụ `netsave-ai-censor/`) được sinh ra tự động chứa đầy đủ `SKILL.md`, `skill.json`, `schemas/`, `kb/`, `scripts/` và `outputs/`.
