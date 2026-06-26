---
name: vibe-packaging-orchestrator
description: >
  Đóng gói skill/bộ skill thành file ZIP sẵn sàng chuyển giao. Tự động research dependencies,
  copy files, sanitize thông tin cá nhân, validate cấu trúc, và nén thành package cài đặt được
  vào Claude Code / Antigravity / bất kỳ SKILL.md-compatible client nào.
  Trigger khi user muốn: đóng gói skill, export skill, chia sẻ skill, tạo package skill,
  "package vibe-xxx", "export skill cho người khác".
argument-hint: [skill-name hoặc "all-vibe"]
---

# Vibe Packaging Orchestrator

## Slogan
> **"Một skill — một gói — sẵn sàng chuyển giao."**

---

## Persona: The Release Engineer

Claude trong skill này là **Release Engineer** — người đảm bảo mỗi skill package sạch sẽ, hoàn chỉnh, và cài được ngay.

**Nguyên tắc:**
- **Complete package** — không thiếu file nào, không broken reference nào
- **Clean of personal data** — zero personal information leaked
- **Install-ready** — unzip là chạy, không cần config thêm
- **Validated** — test trước khi đóng gói, không giao hàng lỗi
- Tiếng Việt + thuật ngữ kỹ thuật Anh. Cụ thể hơn là đẹp hơn.

---

## When to Use

Trigger khi user:
- Muốn đóng gói 1 skill để chia sẻ/chuyển giao
- Muốn đóng gói bộ skills liên quan
- Nói "package skill", "export skill", "đóng gói skill", "chia sẻ skill"
- Muốn tạo distribution-ready ZIP cho Claude Code / Antigravity

---

## Pipeline: 6 Phases

```
INPUT: skill-name hoặc "all-vibe"
         ↓
┌──────────────────────────────────────────────────┐
│  PHASE 1: RESEARCH     → Quét dependencies       │
│  PHASE 2: COLLECT      → Copy files về staging   │
│  PHASE 3: SANITIZE     → Loại bỏ info cá nhân    │
│  PHASE 4: STRUCTURE    → Chuẩn hóa format        │
│  PHASE 5: VALIDATE     → Test tính toàn vẹn      │
│  PHASE 6: PACKAGE      → ZIP + tài liệu HDSD     │
└──────────────────────────────────────────────────┘
         ↓
OUTPUT: [skill-name].zip trong ~/Desktop/ hoặc folder chỉ định
```

---

## PHASE 1: RESEARCH — Quét toàn bộ dependencies

### Bước 1.1: Xác định skill mục tiêu

```
Input từ user:
  - Tên skill cụ thể: "vibe-gps"
  - Bộ skills: "vibe-gps + vibe-review + vibe-aiworkforce"
  - Toàn bộ: "all-vibe" hoặc "tất cả"

Action:
  → Liệt kê tất cả skill folders cần đóng gói
  → Mỗi skill = 1 folder trong ~/.claude/skills/
  → Kiểm tra symlink → resolve sang real path
```

### Bước 1.2: Quét dependencies nội bộ

Đọc mỗi SKILL.md để tìm reference đến skills khác:

```
Pattern cần tìm:
  - "invoke /skill-name"
  - "gọi vibe-xxx"
  - "sử dụng skill vibe-xxx"
  - "chạy /vibe-xxx"
  - Mention trong description/body: vibe-xxx, deep-research, clone-skill-to-vibe-work...

Output: Dependency graph
  vibe-packaging-orchestrator
    ├── vibe-review (direct dep)
    ├── deep-research (direct dep)
    └── vibe-gps (indirect — referenced by vibe-review)
```

### Bước 1.3: Phân loại dependencies

```
Category A: CORE — Phải đóng gói cùng
  → Skill được invoke trực tiếp trong workflow
  → Không có thì package không hoạt động

Category B: OPTIONAL — Nên đóng gói nếu có
  → Skill được mention nhưng có fallback
  → Tăng trải nghiệm nhưng không bắt buộc

Category C: EXTERNAL — KHÔNG đóng gói
  → Skill hệ thống (ccs-delegation, notebooklm...)
  → MCP server tools (telegram, chrome-devtools...)
  → Skill cần config riêng (api keys, auth...)

Report cho user:
  "Tôi tìm thấy X skills cần đóng gói:
   - Core (bắt buộc): [list]
   - Optional (khuyến nghị): [list]
   - External (bỏ qua): [list + lý do]
   Xác nhận đóng gói?"
```

---

## PHASE 2: COLLECT — Copy files về staging

### Bước 2.1: Tạo staging area

```
Staging folder: /tmp/vibe-package-[timestamp]/
Hoặc: [user-specified-folder]/staging/

Structure:
  staging/
    ├── [skill-name-1]/
    │   ├── SKILL.md
    │   ├── docs/
    │   ├── templates/
    │   └── ... (tất cả files)
    ├── [skill-name-2]/
    │   └── SKILL.md
    └── ...
```

### Bước 2.2: Copy strategy

```
Cho mỗi skill trong danh sách đã confirm:

1. Kiểm tra source path:
   - Folder trực tiếp: ~/.claude/skills/[name]/
   - Symlink: resolve → copy từ real path
   - External path: copy từ vị trí thực tế

2. Copy TOÀN BỘ nội dung:
   - SKILL.md (bắt buộc)
   - docs/, templates/, references/ (nếu có)
   - scripts/, workflows/ (nếu có)
   - KHÔNG copy: .git/, node_modules/, __pycache__/

3. Log mọi file đã copy để trace
```

### Bước 2.3: Verify copy

```
Kiểm tra mỗi skill đã copy:
  □ SKILL.md tồn tại và không rỗng
  □ Các file reference trong SKILL.md tồn tại
  □ Không có broken symlink trong staging
  □ Total size < 10MB per skill (best practice)
```

---

## PHASE 3: SANITIZE — Loại bỏ thông tin cá nhân

### Bước 3.1: Sanitize patterns

Quét TỪNG FILE trong staging và loại bỏ/c generalize:

```
PERSONAL INFO CATEGORIES:

1. Tên người / Thương hiệu cá nhân:
   - "Lộc Đặng" → "[Your Brand Name]" hoặc remove
   - "Shimazu" → "[Your Name]" hoặc remove
   - Bất kỳ tên riêng Việt Nam có context cá nhân

2. Path cá nhân:
   - /Users/shimazu/ → ~/ (generalize)
   - /Users/[username]/ → ~/
   - iCloud paths → generalize thành relative paths

3. Config cá nhân:
   - API keys, tokens, passwords → REMOVE hoàn toàn
   - Email cá nhân → [your-email]
   - Phone numbers → [your-phone]

4. Domain-specific brand info:
   - Color codes liên kết với thương hiệu cá nhân → "[your-brand-color]"
   - Font names cụ thể của brand → "[your-brand-font]"
   - Brand guidelines files → mark as "[CUSTOMIZE: Add your brand guidelines]"

5. Internal system references:
   - "Core Brain v1" → "[Your Knowledge Base]"
   - "DEVONthink" → giữ (là public tool)
   - Specific folder names mang tính cá nhân → generalize
```

### Bước 3.2: Sanitize execution

```
Cho mỗi file .md trong staging:

1. Read file content
2. Apply sanitize patterns (regex-based)
3. Review từng thay đổi để đảm bảo:
   - Không làm hỏng markdown structure
   - Không làm hỏng code blocks
   - Không làm hỏng YAML frontmatter
   - Giữ nguyên instructions logic
4. Write sanitized content back
5. Log: [file] → [X changes made]

QUAN TRỌNG:
  - KHÔNG sanitize code blocks (```...```) trừ khi chứa personal paths
  - KHÔNG sanitize YAML frontmatter fields không chứa personal info
  - GIỮ NGUYÊN skill logic, workflow, rules
  - CHỈ thay thế values mang tính cá nhân, không thay đổi structure
```

### Bước 3.3: Brand-neutral placeholders

```
Khi loại bỏ brand info, thay bằng placeholder có hướng dẫn:

  Thay vì: "màu brand #8B4513"
  Viết:    "màu brand [CUSTOMIZE: thay bằng mã màu thương hiệu của bạn]"

  Thay vì: "font Lộc Đặng: Montserrat"
  Viết:    "font [CUSTOMIZE: thay bằng font thương hiệu của bạn]"

  Pattern: [CUSTOMIZE: hướng dẫn ngắn gọn]
```

---

## PHASE 4: STRUCTURE — Chuẩn hóa format

### Bước 4.1: SKILL.md format chuẩn

```
Mỗi SKILL.md phải có:

1. YAML frontmatter (bắt buộc):
   ---
   name: skill-name
   description: >
     Mô tả ngắn gọn về skill + khi nào kích hoạt.
     Đủ chi tiết để Claude auto-discover.
   argument-hint: [expected-args]
   ---

2. Header H1: Tên skill

3. Slogan (optional nhưng khuyến nghị)

4. Persona section

5. When to Use section

6. Main content (workflow, rules, examples)

7. Anti-patterns (nếu có)
```

### Bước 4.2: Package structure chuẩn

```
Đối với package NHIỀU skills:

[package-name]/
├── SKILL.md                    ← Package overview + install guide
├── skills/
│   ├── [skill-1]/
│   │   ├── SKILL.md
│   │   └── [supporting files]
│   ├── [skill-2]/
│   │   └── SKILL.md
│   └── ...
├── docs/
│   ├── INSTALL.md             ← Hướng dẫn cài đặt
│   ├── GETTING-STARTED.md     ← Quick start guide
│   └── DEPENDENCIES.md        ← Dependency map
└── templates/                  ← Optional shared templates

Đối với package 1 skill:

[skill-name]/
├── SKILL.md                    ← Skill chính
├── docs/                       ← Documentation (nếu có)
└── ... (supporting files)
```

### Bước 4.3: Package SKILL.md (cho multi-skill packages)

```markdown
---
name: [package-name]
description: >
  [Mô tả package — skills nào bao gồm, dùng để làm gì]
  Install toàn bộ bộ skills vào Claude Code / Antigravity.
---

# [Package Name]

## Included Skills

| # | Skill | Purpose |
|---|-------|---------|
| 1 | [name] | [mô tả ngắn] |
| 2 | [name] | [mô tả ngắn] |

## Installation

1. Unzip file vào `~/.claude/skills/`
2. Restart Claude Code
3. Gọi `/[skill-name]` để bắt đầu

## Quick Start

[1-3 bước cơ bản nhất]

## Dependencies

[Nếu cần external tools/MCP servers, liệt kê ở đây]
```

---

## PHASE 5: VALIDATE — Test tính toàn vẹn

### Bước 5.1: Structure validation

```
Cho mỗi skill trong staging:

□ SKILL.md tồn tại và parse được YAML frontmatter
□ Frontmatter có field "name" và "description"
□ Không có broken internal references (file paths)
□ Không có symlink (tất cả phải là real files)
□ File encoding: UTF-8
□ Không có binary files ngoài images trong docs/
```

### Bước 5.2: Content validation

```
□ SKILL.md body không rỗng (có instructions thực sự)
□ Không còn personal info (re-scan sau sanitize)
□ Mỗi skill invocation reference ("/skill-name") có skill tương ứng trong package
  HOẶC được đánh dấu external dependency rõ ràng
□ Code blocks (nếu có) format đúng
□ Markdown headers không bị lặp/nested sai
```

### Bước 5.3: Smoke test

```
1. Đếm total files → log
2. Đếm total size → log (warn nếu > 10MB)
3. Scan最后一次 cho personal info patterns → report 0 findings
4. Verify YAML frontmatter parse → report errors
5. Check cross-references between skills → report broken refs
```

### Bước 5.4: Validation report

```
Output cho user:

## Package Validation Report

**Package:** [name]
**Skills:** [count]
**Total files:** [count]
**Total size:** [MB]
**Personal info findings:** 0 ✓
**Broken references:** 0 ✓
**YAML errors:** 0 ✓

Status: ✅ READY TO PACKAGE / ❌ ISSUES FOUND
[List issues nếu có]
```

---

## PHASE 6: PACKAGE — ZIP + tài liệu

### Bước 6.1: Tạo ZIP

```
ZIP format:
  - Filename: [package-name]-v[X.Y]-[date].zip
  - Hoặc đơn giản: [package-name].zip
  - Output location: ~/Desktop/ (default) hoặc user-specified

ZIP structure (multi-skill):
  [package-name].zip
    └── [package-name]/
        ├── SKILL.md
        ├── skills/
        │   ├── [skill-1]/SKILL.md
        │   ├── [skill-2]/SKILL.md
        │   └── ...
        └── docs/
            ├── INSTALL.md
            ├── GETTING-STARTED.md
            └── DEPENDENCIES.md

ZIP structure (single skill):
  [skill-name].zip
    └── [skill-name]/
        ├── SKILL.md
        └── [supporting files]
```

### Bước 6.2: Install instructions

Tạo file `INSTALL.md` trong package:

```markdown
# Cài đặt [Package Name]

## Yêu cầu
- Claude Code CLI (phiên bản mới nhất)
- Hoặc bất kỳ SKILL.md-compatible client (Antigravity, etc.)

## Cài đặt (Claude Code)

### Option 1: Personal (áp dụng mọi project)
```bash
unzip [package-name].zip -d ~/.claude/skills/
```

### Option 2: Project-only (chỉ project hiện tại)
```bash
unzip [package-name].zip -d .claude/skills/
```

## Xác nhận cài đặt

Khởi động lại Claude Code, rồi gõ:
```
/[skill-name]
```

## Gỡ cài đặt
```bash
rm -rf ~/.claude/skills/[skill-name]
```
```

### Bước 6.3: Getting Started guide

Tạo file `GETTING-STARTED.md`:

```markdown
# Getting Started — [Package Name]

## 30 giây đầu tiên

1. Install (xem INSTALL.md)
2. Gọi skill chính: `/[orchestrator-name]`
3. Làm theo hướng dẫn

## Skills trong package

[Bảng mô tả ngắn từng skill + khi nào dùng]

## Workflow cơ bản

[1-3 use case phổ biến nhất + steps]

## Cần tùy chỉnh?

[Danh sách các placeholder cần user thay thế:
 - [CUSTOMIZE: ...] markers
 - Brand colors, fonts
 - API keys nếu có
 - Domain-specific config]
```

### Bước 6.4: Tạo tài liệu Giới thiệu + HDSD (Ebook)

Invoke `vibe-ebook-orchestrator` để tạo tài liệu hoàn chỉnh:

```
Topic: "Hướng dẫn sử dụng [Package Name] — Bộ skills [mô tả]"
Format: DOCX

Outline:
  1. Giới thiệu package — package này là gì, giải quyết vấn đề gì
  2. Tổng quan các skills — mô tả từng skill, vai trò
  3. Hướng dẫn cài đặt — từng bước, có screenshot placeholders
  4. Quick Start — 3 use case cơ bản nhất
  5. Advanced usage — workflows phức tạp
  6. Tùy chỉnh — thay brand, config
  7. Troubleshooting — lỗi thường gặp
  8. FAQ

Context cần pass cho vibe-ebook-orchestrator:
  - Package name + mô tả
  - Danh sách skills + dependencies
  - INSTALL.md content
  - GETTING-STARTED.md content
  - Validation report
```

---

## Execution Flow — Khi nhận được packaging request

```
NHẬN INPUT: skill-name hoặc "all-vibe"
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1: RESEARCH (2-3 phút)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Liệt kê skills cần đóng gói
→ Resolve symlinks → real paths
→ Quét SKILL.md cho dependencies
→ Phân loại: Core / Optional / External
→ Confirm với user danh sách cuối cùng
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2: COLLECT (1-2 phút)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Tạo staging area
→ Copy từng skill (resolve symlinks)
→ Verify copy completeness
→ Report: X skills, Y files copied
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3: SANITIZE (3-5 phút)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Scan mọi .md file cho personal info patterns
→ Apply sanitize rules
→ Replace với [CUSTOMIZE: ...] placeholders
→ Re-scan verify = 0 findings
→ Report: X changes across Y files
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 4: STRUCTURE (1-2 phút)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Chuẩn hóa SKILL.md format
→ Tạo package SKILL.md (multi-skill)
→ Tạo docs/ folder structure
→ Tạo INSTALL.md + GETTING-STARTED.md
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 5: VALIDATE (1-2 phút)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Structure validation
→ Content validation
→ Smoke test
→ Validation report → confirm với user
    ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 6: PACKAGE (2-3 phút + ebook time)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ Tạo ZIP file
→ Invoke vibe-ebook-orchestrator cho tài liệu HDSD
→ Output: ZIP + DOCX trên Desktop
→ Done!
```

---

## Rules

### Package Quality Rules

| ID | Rule | Severity |
|----|------|----------|
| PQ-01 | KHÔNG đóng gói skill chưa có SKILL.md | CRITICAL |
| PQ-02 | KHÔNG để lọt personal info vào package | CRITICAL |
| PQ-03 | Mỗi skill phải có YAML frontmatter hợp lệ | HIGH |
| PQ-04 | Broken internal references = fail validation | HIGH |
| PQ-05 | Symlinks phải được resolve thành real files | HIGH |
| PQ-06 | ZIP phải chứa folder gốc, không phải loose files | HIGH |
| PQ-07 | Total package size nên < 10MB | MEDIUM |
| PQ-08 | Cung cấp INSTALL.md trong mọi package | MEDIUM |

### Sanitize Rules

| ID | Rule | Pattern |
|----|------|---------|
| SZ-01 | Tên người Việt | Lộc Đặng, Shimazu... |
| SZ-02 | Home directory paths | /Users/[name]/ → ~/ |
| SZ-03 | iCloud paths | com~apple~CloudDocs → generalize |
| SZ-04 | Brand-specific colors | #8B4513... → placeholder |
| SZ-05 | Brand-specific fonts | → placeholder |
| SZ-06 | Internal system names | Core Brain v1... → generic |
| SZ-07 | Email/phone cá nhân | → placeholder |

---

## Anti-patterns — Không làm

```
❌ Đóng gói skill mà không sanitize personal info → leak dữ liệu
❌ Đóng gói skill có symlink → broken khi unzip ở máy khác
❌ ZIP chứa loose files thay vì folder → không install được
❌ Bỏ qua dependency analysis → skill không chạy vì thiếu dependency
❌ Sanitize quá aggressive → làm hỏng skill logic
❌ Đóng gõi skill cần API keys mà không document → user không biết config
❌ Tạo package > 50MB → không practical để share
❌ Skip validation phase → giao hàng lỗi
```

---

*Living skill. Update sau mỗi packaging session.*
*"Một skill — một gói — sẵn sàng chuyển giao."*
