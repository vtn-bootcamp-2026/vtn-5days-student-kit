---
mo-ta: Skills cài sẵn cho học viên Session 07 — điều khiển NotebookLM (Lab B + Lab C)
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-24 22:20 +07:00
updated-at: 2026-06-24 22:20 +07:00
---

# Skills cài sẵn — Session 07 (Agentic RAG — HR Policy QA)

2 skill dưới đây do HV cài vào super agent (Antigravity / Claude Code) để làm **Lab B** (NotebookLM quy mô lớn) và **Lab C** (Agent gọi NotebookLM để source routing cloud).

| Skill | ZIP | Dùng ở | Vai trò |
|-------|-----|--------|---------|
| `notebooklm` | [notebooklm.zip](notebooklm.zip) | Lab B/C | Engine browser automation (Patchright) — auth, tạo notebook, add source, query, artifact |
| `vibe-notebooklm-orchestrator` | [vibe-notebooklm-orchestrator.zip](vibe-notebooklm-orchestrator.zip) | Lab B/C | Orchestrator gọi engine `notebooklm` + fetch nội dung (qiaomu, tùy chọn) |

> Cả 2 đã được **sanitize** (không PII — auth state/cookies đã loại) + **validate cấu trúc** + đóng gói install-ready. Source gốc: kho skill của giảng viên (`~/.claude/skills/`).

> [!IMPORTANT]
> `vibe-notebooklm-orchestrator` **phụ thuộc** `notebooklm` (engine). Bắt buộc cài **cả 2** theo thứ tự: `notebooklm` trước, rồi `vibe-notebooklm-orchestrator`.

## Yêu cầu hệ thống (dependency runtime — KHÔNG nằm trong zip)

Zip **không bao gồm** venv (platform-specific) và **không bao gồm** auth state (PII). HV cần setup 2 thứ sau khi unzip:

1. **Python venv + Patchright** — chạy 1 lần:
   ```bash
   cd ~/.claude/skills/notebooklm
   python3 scripts/setup_environment.py     # tạo .venv + pip install -r requirements.txt (patchright, ...)
   ```
2. **Google auth** (login NotebookLM lần đầu) — mỗi HV 1 tài khoản:
   ```bash
   python3 ~/.claude/skills/notebooklm/scripts/run.py auth_manager.py setup
   ```
   Mở browser → login Google → state lưu tại `data/browser_state/state.json` (riêng tư, KHÔNG commit).

(Optional) **qiaomu** — engine fetch nội dung (URL/paywall/YouTube/EPUB...). Lab B dùng upload file trực tiếp nên **không bắt buộc**. Nếu cần: cài thêm `~/.claude/skills/qiaomu-anything-to-notebooklm/`.

## Cài đặt

### Claude Code (personal — áp dụng mọi project)
```bash
unzip notebooklm.zip -d ~/.claude/skills/
unzip vibe-notebooklm-orchestrator.zip -d ~/.claude/skills/
# rồi setup venv + auth (xem mục "Yêu cầu hệ thống")
```
Khởi động lại Claude Code → gọi `/vibe-notebooklm-orchestrator` để kiểm tra.

### Antigravity
1. Kéo thả `notebooklm.zip` vào ô chat → cài engine.
2. Kéo thả `vibe-notebooklm-orchestrator.zip` → cài orchestrator.
3. Setup venv + auth qua terminal (xem trên).

## Workflow dùng trong Lab B / Lab C

```bash
# Lab B — tạo notebook + upload corpus HR-policy
python3 ~/.claude/skills/notebooklm/scripts/run.py \
  ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_notebook.py \
  --title "HR-Policy KB — Viettel Network"

python3 ~/.claude/skills/notebooklm/scripts/run.py \
  ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/add_source.py \
  --type file --notebook-url "<URL>" --file synthetic-data/hr-policies/policy-leave.md

# Query (verify grounding + citation)
python3 ~/.claude/skills/notebooklm/scripts/run.py \
  ~/.claude/skills/notebooklm/scripts/ask_question.py \
  --notebook-url "<URL>" --question "Nghỉ ốm quá 30 ngày thì lương thế nào?"
```

> [!CAUTION]
> Dữ liệu HR/nội bộ doanh nghiệp viễn thông thường **nhạy cảm**. NotebookLM là **cloud Google** — chỉ upload tài liệu đã **anon hóa** hoặc public. Với dữ liệu thật, ưu tiên RAG local hybrid (Lab A). Xem §8.1 trong `lab.md`.

## Lỗi thường gặp

| Lỗi | Khắc phục |
|-----|-----------|
| `ModuleNotFoundError: patchright` | Chưa chạy `setup_environment.py` (tạo venv) |
| Auth expired / query trả kết quả chung chung | Chạy lại `auth_manager.py setup`, login lại Google |
| Query trả stale answer (lặp đáp án cũ) | Bug đã biết khi notebook có chat history — query trên notebook sạch, hoặc verify thủ công |
| `GETNOTE_API_KEY` missing | Chỉ cần cho podcast transcription (Lab B không dùng) — bỏ qua được |
