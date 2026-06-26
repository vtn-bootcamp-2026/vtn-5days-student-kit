---
mo-ta: "Tổng quan Session 09 — lab gộp Vệ sĩ văn phòng VTN (4 concept, non-tech, vibe coding qua Antigravity)"
trang-thai: active
phien-ban: v2.1
created-at: 2026-06-20 22:25 +07:00
updated-at: 2026-06-26 08:00 +07:00
---

# Session 09 — Vệ sĩ văn phòng VTN (Anonymizer + Hook + Chống Injection + Compliance)

> **1 lab duy nhất, 1 ví dụ duy nhất, dạy đủ 4 concept bảo mật AI** — qua **Antigravity**,
> dành cho nhóm **non-tech** (vibe coding: copy-paste prompt, không code tay, không LLM API ngoài).

## Bản dạy chính thức

| File | Vai trò |
|---|---|
| **[lab.md](lab.md)** | **Lab chính** — 4 phần (A–D) tương ứng 4 concept, có prompt inline + analogy + trouble cards |
| [prompts/](prompts/) | Thư mục chứa các tệp prompt riêng lẻ (mục lục: [vibe-coding-prompts.md](prompts/vibe-coding-prompts.md)) |
| [synthetic-data/](synthetic-data/) | Ví dụ xuyên suốt: bản ghi bàn giao ca CSKH (có PII + injection) + kết quả đúng |
| [templates/](templates/) | Starter code, SKILL.md/skill.json, kb/, hook mẫu, compliance checklist, runbook |

## 4 concept & 4 phần (mỗi concept = 1 phần thực hành)

| Phần | Concept | Đầu ra |
|---|---|---|
| Part A | Dựng bộ khung Skill | `vp-vtn-office-guard/` (SKILL.md + skill.json) |
| Part B | **1. Anonymizer** — ẩn PII, giữ thuật ngữ an toàn | bản ghi ca đã ẩn danh |
| Part C | **2. Hook** + **3. Chống Prompt Injection** | hook chặn file + cản lệnh giả danh |
| Part D | **4. Compliance checklist** | bảng kiểm tuân thủ ≥ 7/8 |

**Ví dụ xuyên suốt:** bản ghi bàn giao ca CSKH VTN chứa PII khách/nhân viên **và** 1 email khách
mang **prompt injection** — tài liệu này chạy qua cả 4 concept theo chuỗi móc nối.

## Nguồn (lưu trữ)

2 lab gốc (kỹ thuật, cho kỹ sư NOC — Ollama/Hermes/Python) đã gộp & đơn giản hoá thành lab trên:
xem [`archive/`](archive/README.md).

- `archive/anonymizer/` — nguồn ẩn danh + hook (từ session-05)
- `archive/compliance/` — nguồn chống injection + checklist (từ session-06)
