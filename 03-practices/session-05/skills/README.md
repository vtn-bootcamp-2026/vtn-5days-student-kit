---
mo-ta: Huấn luyện kỹ năng cài đặt và sử dụng skill cho học viên trong Session 05
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 10:15:37 +07:00
updated-at: 2026-06-23 17:15:30 +07:00
---

# Skills cài sẵn — Session 05 (Track A: vibe-working)

2 skill dưới đây do HV cài vào super agent (Antigravity / Codex / Claude Code) để làm BT2 + BT3.

| Skill | ZIP | Dùng ở | Vai trò |
|-------|-----|--------|---------|
| `vibe-aiworkforce` | [vibe-aiworkforce.zip](vibe-aiworkforce.zip) | BT2 | Build skill `review-contract` từ `skill_design.md` |
| `vibe-improve-orchestrator` | [vibe-improve-orchestrator.zip](vibe-improve-orchestrator.zip) | BT3 | Improve skill đã có (7-phase, có verify) |

> Cả 2 đã được sanitize (không PII) + validate cấu trúc + đóng gói install-ready. Source gốc: kho skill của giảng viên.

## Cài đặt

### Claude Code (personal — áp dụng mọi project)
```bash
unzip vibe-aiworkforce.zip -d ~/.claude/skills/
unzip vibe-improve-orchestrator.zip -d ~/.claude/skills/
```
Khởi động lại Claude Code → gọi `/vibe-aiworkforce` để kiểm tra.

### Antigravity
1. Kéo thả file `.zip` của skill (ví dụ `vibe-aiworkforce.zip` hoặc `vibe-improve-orchestrator.zip`) trực tiếp vào ô chat.
2. Gõ thêm câu lệnh: *"cài đặt skill này vào project hiện tại để sử dụng lại trong các lần sau"*.
3. Verify: hỏi *"Bạn có skill vibe-aiworkforce không?"* → phải trả lời có.

### Codex / Claude Desktop
Giải nén ZIP vào thư mục skill tương ứng của client, restart.

## Xác nhận cài thành công

Sau khi cài, yêu cầu super agent:
> "Dùng skill vibe-aiworkforce để build một skill test đơn giản."

Nếu AI phản hồi theo workflow của `vibe-aiworkforce` (hỏi COMPANY_ROOT, sinh cấu trúc skill) → cài OK.

## Gỡ cài đặt
```bash
rm -rf ~/.claude/skills/vibe-aiworkforce
rm -rf ~/.claude/skills/vibe-improve-orchestrator
```

## Lưu ý

- 2 skill này là **công cụ của HV** (dùng để build/improve skill `review-contract`), KHÔNG phải output bài nộp.
- Output bài nộp (BT2) là skill `review-contract` mà HV build ra — đóng gói riêng bằng `vibe-packaging-orchestrator`.
