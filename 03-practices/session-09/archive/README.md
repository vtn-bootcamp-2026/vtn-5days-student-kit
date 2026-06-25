---
mo-ta: "Nguồn lưu trữ — 2 lab gốc kỹ thuật của Session 09 trước khi gộp & đơn giản hoá"
trang-thai: archived
phien-ban: v1.0
created-at: 2026-06-25 16:22 +07:00
updated-at: 2026-06-25 16:22 +07:00
---

# archive/ — Nguồn gốc của Session 09

> ⚠️ Đây là **bản kỹ thuật dành cho kỹ sư NOC** (Ollama + Hermes + Python vibe coding + 10 test cases + Capstone).
> Đã được **gộp và đơn giản hoá** thành lab hiện tại ở [`../lab.md`](../lab.md)
> (chạy trong Antigravity, cho nhóm non-tech). Giữ lại đây để **truy ngược nguồn** và tham khảo sâu.

| Thư mục | Concept gốc | Output gốc |
|---|---|---|
| [`anonymizer/`](anonymizer/) | Anonymizer mini-tool + Hook bảo mật | anonymizer-skill + vtn-agent-skill |
| [`compliance/`](compliance/) | Compliance checklist + Chống Prompt Injection + Capstone | Implementation Kit (7 hồ sơ) |

## Bảng ánh xạ — concept gốc → lab mới

| Nguồn gốc (archive) | Đơn giản hoá thành (lab mới) |
|---|---|
| `anonymizer/` — Ollama + Hermes + Regex/LLM hybrid | **Part A + B** — Antigravity vibe coding, kb/pii + safe-terms |
| `anonymizer/` — pre_tool_call Hook chặn write/shell | **Part C1** — `scripts/hook.py` chặn ghi ngoài `outputs/` |
| `compliance/` — System Prompt Hardening `<user_data>` | **Part C2** — bọc `<user_data>`, cản injection trong email khách |
| `compliance/` — Compliance checklist (Nghị định 356/2025) | **Part D** — compliance-checklist 8 hạng mục (đơn giản hoá) |

## Khi nào nên quay lại archive?

- Cần dạy nhóm **kỹ thuật** (có thể cài Ollama, biết Python).
- Cần **Capstone trình bày** 7 hồ sơ bàn giao đầy đủ.
- Cần **10 test cases** bao phủ 4 nhóm tình huống (bình thường/lỗi/thiếu/vượt phạm vi).
