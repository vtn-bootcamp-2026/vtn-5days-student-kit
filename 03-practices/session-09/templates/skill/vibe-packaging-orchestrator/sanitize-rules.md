# Sanitize Rules Reference

Dùng trong PHASE 3 của vibe-packaging-orchestrator.

## Personal Info Patterns

### Tên người / Thương hiệu cá nhân

| Pattern | Replacement | Ghi chú |
|---------|-------------|---------|
| Lộc Đặng | [Your Brand Name] | Thương hiệu cá nhân |
| Loc Dang | [Your Brand Name] | Variant không dấu |
| locdang | [your-brand] | Trong URL/path/filename |
| Shimazu | [Your Name] | Tên cá nhân |
| shimazu | [your-name] | Trong path/username |

### Paths cá nhân

| Pattern | Replacement | Ghi chú |
|---------|-------------|---------|
| /Users/shimazu/ | ~/ | Home directory |
| /Users/[any-name]/ | ~/ | Bất kỳ username |
| com~apple~CloudDocs | [Cloud Storage] | iCloud path segment |
| Library/Mobile Documents/... | ... | iCloud full path |

### Brand-specific values

| Pattern | Replacement | Khi nào |
|---------|-------------|---------|
| #8B4513 | [CUSTOMIZE: your brand color] | Brand color trong slide/CSS |
| Montserrat | [CUSTOMIZE: your brand font] | Brand font |
| Brand colors/pillars/key-messages | [CUSTOMIZE: your brand guidelines] | Brand-specific sections |

### Internal system names

| Pattern | Replacement | Ghi chú |
|---------|-------------|---------|
| Core Brain v1 | [Your Knowledge Base] | Tên internal system |
| Core Brain | [Your Knowledge Base] | Variant ngắn |

### Không sanitize (giữ nguyên)

- Tên public tools: DEVONthink, Tinderbox, OmniFocus, iTerm, CleanShot, Mountain Duck
- Tên public frameworks: Claude, Antigravity, Gemini, MCP
- Tên domain chung: marketing, content, sales, HR
- Code blocks (```...```) trừ khi chứa personal paths
- YAML frontmatter fields không chứa personal info
- Generic placeholder patterns đã tồn tại

## Sanitize Process

```
1. Scan file → find all matches
2. For each match:
   a. Check if inside code block → if YES, only sanitize paths
   b. Check if generic term → if YES, skip
   c. Apply replacement
3. Write back
4. Re-scan → verify 0 matches
```
