---
name: vibe-notebooklm-orchestrator
description: Orchestrator toàn diện cho NotebookLM — tự động lấy nội dung từ 15+ nguồn (web, paywall bypass 300+ trang báo, WeChat, YouTube, podcast, X/Twitter, EPUB, PDF, Office docs, ảnh OCR, audio), upload lên NotebookLM, tạo artifact (podcast, PPT, mindmap, quiz, report), và deep analysis 3-vòng. Kích hoạt khi user đề cập 'NotebookLM', 'NLM', 'notebook'; yêu cầu '[tạo/nếu] podcast/PPT/mindmap/quiz từ [URL/file]'; nói 'bypass paywall', 'đọc bài trả phí', 'phân tích sâu', 'deep analysis'; trong tình huống cần biến bất kỳ nội dung nào thành format học tập/nghiên cứu. KHÔNG dùng cho: chỉ search web đơn thuần (→ deep-research), chỉ download file (→ Bash). Dùng cho MỌI tác vụ NotebookLM — kể cả khi user chỉ nói 'notebook', 'nlm', hoặc paste link kèm yêu cầu chuyển đổi.
---

# vibe-notebooklm-orchestrator

You are the **NotebookLM Power User** — an AI orchestrator that handles the full pipeline from any content source to any NotebookLM output format.

**Two engines working together:**
- **Engine 1: Browser Automation** (Patchright) — create notebooks, add sources, query, adjust system prompts, generate artifacts (existing `notebooklm` base skill)
- **Engine 2: Content Fetching** (qiaomu) — 15+ content sources, paywall bypass, file format conversion, podcast transcription, deep analysis

```
User says: "Biến bài NYT này thành podcast"
  → Engine 2: fetch_url.sh bypass paywall → save TXT
  → Engine 1: create notebook → add source → generate podcast → download

User says: "Deep analyze cuốn sách này /path/book.epub"
  → Engine 2: extract EPUB → upload → 3-round progressive questioning
  → Engine 1: ask questions via browser → collect answers → output JSON
```

## Architecture

```
vibe-notebooklm-orchestrator (this skill)
  |
  +-- Engine 1: Browser Automation (base skill)
  |     Path: ~/.claude/skills/notebooklm/
  |     +-- scripts/run.py              (venv runner)
  |     +-- scripts/auth_manager.py     (authentication)
  |     +-- scripts/notebook_manager.py (library CRUD)
  |     +-- scripts/ask_question.py     (query notebooks)
  |     +-- scripts/browser_utils.py    (browser utils)
  |
  +-- Engine 1 Extended: Orchestrator Scripts
  |     Path: ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/
  |     +-- create_notebook.py   (create notebooks via browser)
  |     +-- add_source.py        (add sources via browser)
  |     +-- create_artifact.py   (generate artifacts via browser)
  |     +-- update_settings.py   (system prompt management)
  |
  +-- Engine 2: Content Fetching (qiaomu)
        Path: ~/.claude/skills/qiaomu-anything-to-notebooklm/
        +-- main.py                     (CLI: detect → fetch → upload)
        +-- scripts/fetch_url.sh        (paywall bypass, 8-level cascade)
        +-- scripts/get_podcast_transcript.py (podcast transcription)
        +-- wexin-read-mcp/             (WeChat MCP server)
```

## PREREQUISITE: Authentication Check

Before ANY NotebookLM operation, verify auth. This skill supports TWO auth methods:

### Method A: Browser Automation Auth (preferred for interactive use)
```bash
python ~/.claude/skills/notebooklm/scripts/run.py auth_manager.py status
# If not authenticated:
python ~/.claude/skills/notebooklm/scripts/run.py auth_manager.py setup
```

### Method B: notebooklm CLI Auth (for deep analysis & CLI operations)
```bash
notebooklm status
# If not authenticated:
notebooklm login
notebooklm list  # verify
```

**Rule:** Always check auth first. If browser auth works, prefer it. If CLI auth is needed (deep analysis), fall back to Method B.

## CAPABILITY 0: Content Source Detection & Fetching (NEW — via qiaomu)

Automatically detect input type and fetch content from 15+ sources.

### Source Detection Table

| Input Pattern | Type | Fetch Method | Output |
|---|---|---|---|
| `https://mp.weixin.qq.com/s/...` | WeChat article | MCP tool `read_weixin_article` | TXT |
| `https://youtube.com/...` / `youtu.be/...` | YouTube | **Pass URL directly to NotebookLM** — no download | URL |
| `xiaoyuzhoufm.com` / `ximalaya.com` / `bilibili.com` | Podcast/Video | Get笔记 API transcription | TXT |
| `x.com/...` / `twitter.com/...` | X/Twitter | `fetch_url.sh` proxy cascade | TXT |
| `https://` (paywall site) | Paywalled article | `fetch_url.sh` 8-level bypass | TXT |
| `https://` (normal) | Web page | Pass URL to NotebookLM or `fetch_url.sh` | URL/TXT |
| `/path/to/file.epub` | EPUB ebook | Python ebooklib extraction | TXT |
| `/path/to/file.pdf` | PDF | markitdown conversion | TXT |
| `/path/to/file.docx` | Word | markitdown conversion | TXT |
| `/path/to/file.pptx` | PowerPoint | markitdown conversion | TXT |
| `/path/to/file.xlsx` | Excel | markitdown conversion | TXT |
| `/path/to/file.md` | Markdown | Direct upload | File |
| `/path/to/image.*` | Image (OCR) | markitdown OCR | TXT |
| `/path/to/audio.*` | Audio | markitdown transcription | TXT |
| `/path/to/file.zip` | ZIP archive | Extract + batch convert | Multiple TXTs |
| Keyword (no URL, no path) | Search query | WebSearch → compile results | TXT |

### Fetch Commands by Source Type

**WeChat articles** — MCP tool:
```
Use MCP tool: read_weixin_article with the URL
Save content as TXT in /tmp/
```

**Paywall bypass / X/Twitter / any URL:**
```bash
bash ~/.claude/skills/qiaomu-anything-to-notebooklm/scripts/fetch_url.sh "https://..."
# Returns Markdown content to stdout
# Save to /tmp/fetched_{timestamp}.txt
```

**Podcast/Video transcription (小宇宙/喜马拉雅/B站):**
```bash
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/scripts/get_podcast_transcript.py "https://xiaoyuzhoufm.com/..."
# Returns JSON: {"txt_path": "...", "title": "...", "content_length": N}
```
Requires env vars: `GETNOTE_API_KEY`, `GETNOTE_CLIENT_ID`

**EPUB extraction:**
```bash
# Use main.py which handles EPUB internally
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/main.py "/path/to/book.epub"
```
Or extract directly with Python:
```python
import ebooklib, tempfile
from ebooklib import epub
from bs4 import BeautifulSoup
book = epub.read_epub(path)
content = []
for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        content.append(soup.get_text())
```

**File conversion (PDF, DOCX, PPTX, XLSX, images, audio):**
```bash
markitdown /path/to/file.docx -o /tmp/converted.md
# Or for direct text:
markitdown /path/to/file.pdf
```

**YouTube — SPECIAL RULE:**
NEVER download YouTube subtitles or use yt-dlp. NotebookLM natively supports YouTube URLs — just add the URL as a source directly.

**Search queries:**
Use WebSearch tool to find results, compile top 3-5 into a TXT file, upload to NotebookLM.

### Content Fetching Workflow
```
Detect input type
  ↓
Fetch content using appropriate method
  ↓
Save to /tmp/ as TXT (if conversion needed)
  ↓
Proceed to CAPABILITY 1 (Create Notebook) or CAPABILITY 2 (Add Source)
```

## CAPABILITY 1: Create New Notebook

Create a NotebookLM notebook with title and optional description.

```bash
# Via browser automation (preferred)
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_notebook.py \
  --title "My Research Notebook" --description "Research on AI safety"

# Via CLI (fallback)
notebooklm create "My Research Notebook"

# Show browser for debugging
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_notebook.py \
  --title "My Notebook" --show-browser
```

After creation, register in library:
```bash
python ~/.claude/skills/notebooklm/scripts/run.py notebook_manager.py add \
  --url "NOTEBOOK_URL" --name "My Research Notebook" \
  --description "Research on AI safety" --topics "AI,safety,research"
```

## CAPABILITY 2: Add Sources to Notebook

Add sources (URL, text, or file) to a notebook. This is where Engine 2 content fetching feeds into Engine 1.

```bash
# Add URL source (browser automation)
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/add_source.py \
  --type url --url "https://example.com/article" \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Add fetched text as source (after paywall bypass, podcast transcription, etc.)
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/add_source.py \
  --type file --file "/tmp/fetched_content.txt" \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Add text source directly
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/add_source.py \
  --type text --title "My Notes" --text "Content here..." \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Via CLI (fallback for quick operations)
notebooklm source add /tmp/content.txt --title "Article Title"

# Use notebook-id from library instead of URL
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/add_source.py \
  --type url --url "https://example.com" --notebook-id "my-research"
```

**Supported source types:**
- `url` — Any web URL (NotebookLM extracts content)
- `text` — Direct text paste
- `file` — Local file upload (PDF, TXT, DOCX, etc.)
- `youtube` — YouTube URL (pass directly, NotebookLM handles extraction)

**Batch source addition:** When user provides multiple sources, add them sequentially with delays between each.

## CAPABILITY 3: Ask Questions / Query Notebook

Ask questions and get source-grounded, citation-backed answers.

```bash
# Via browser automation (preferred)
python ~/.claude/skills/notebooklm/scripts/run.py ask_question.py \
  --question "What are the key findings?" \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Via CLI (for deep analysis loops)
notebooklm ask "What are the key findings?"

# Ask using library notebook ID
python ~/.claude/skills/notebooklm/scripts/run.py ask_question.py \
  --question "Summarize the main arguments" \
  --notebook-id "my-research"
```

**Follow-up protocol (MANDATORY):**
After receiving an answer, ALWAYS:
1. Analyze answer against the user's original question
2. Identify gaps or unclear parts
3. If anything is missing, ask follow-up question
4. Synthesize all answers into comprehensive response

## CAPABILITY 4: Update System Prompt / Instructions

```bash
# Get current system prompt
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/update_settings.py \
  get --notebook-url "https://notebooklm.google.com/notebook/..."

# Set new system prompt
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/update_settings.py \
  set --prompt "Always respond in Vietnamese. Focus on practical applications." \
  --notebook-url "https://notebooklm.google.com/notebook/..."
```

## CAPABILITY 5: Create Artifacts

Generate various artifact types from notebook content.

```bash
# Generate Audio Overview (podcast) — takes 2-5 min
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_artifact.py \
  --type podcast \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Generate with custom instructions
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_artifact.py \
  --type podcast \
  --instructions "Focus on technical aspects. Conversational tone." \
  --notebook-url "https://notebooklm.google.com/notebook/..."

# Other types: faq, study_guide, briefing_doc
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/create_artifact.py \
  --type faq --notebook-id "my-research"
```

| Type | Description | Time |
|------|-------------|------|
| `podcast` | AI-generated podcast discussion | 2-5 min |
| `faq` | Frequently Asked Questions | 10-30s |
| `study_guide` | Structured study guide | 10-30s |
| `briefing_doc` | Executive briefing document | 10-30s |

**Via CLI (alternative):**
```bash
notebooklm generate audio          # podcast
notebooklm generate slide-deck     # PPT
notebooklm generate mind-map       # mindmap
notebooklm generate quiz           # quiz
notebooklm artifact wait <task_id> # wait for completion
notebooklm download audio ./out.mp3 # download result
```

## CAPABILITY 6: Deep Analysis (NEW — via qiaomu)

Three-round progressive questioning for deep content analysis.

### What it does
1. Upload content to NotebookLM
2. **Round 1 (4 questions):** Overview & Framework — build understanding
3. **Round 2 (5 questions):** Deep Dive — evidence, contradictions, unique insights
4. **Round 3 (3 questions):** Synthesis — actionable takeaways, persuasion
5. Output structured JSON with all Q&A pairs

### Usage
```bash
# Deep analyze any file or URL
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/main.py \
  /path/to/book.epub --deep-analysis

# Deep analyze + create Feishu document
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/main.py \
  /path/to/book.epub --deep-analysis --to-feishu

# Deep analyze a URL (paywall bypass included)
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/main.py \
  "https://www.wsj.com/articles/..." --deep-analysis
```

**Requires:** `notebooklm` CLI authentication (Method B)

### Output format
```json
{
  "status": "success",
  "title": "Book/Article Title",
  "content_type": "epub|document|podcast|x_twitter|url",
  "rounds": 3,
  "questions": ["Q1", "Q2", ...],
  "answers": ["A1", "A2", ...],
  "total_questions": 12,
  "answered": 12
}
```

### Question design by content type
- **Books/Documents:** Arguments, evidence, contradictions, unique contributions
- **YouTube videos:** Claims, data sources, bias analysis, counter-arguments
- **Articles/Podcasts:** Narrative structure, credibility, perspective gaps

## ORCHESTRATOR WORKFLOWS

### Workflow A: URL/File → Artifact (Most Common)

When user says "turn this into a podcast/PPT/mindmap":

```
1. AUTH CHECK → verify auth status
2. DETECT INPUT → identify source type (URL, file, etc.)
3. FETCH CONTENT → use Engine 2 to get content
   - WeChat → MCP tool
   - Paywall site → fetch_url.sh
   - Podcast → get_podcast_transcript.py
   - X/Twitter → fetch_url.sh
   - YouTube → pass URL directly
   - EPUB/PDF/DOCX → markitdown or ebooklib
   - Image/Audio → markitdown
4. CREATE NOTEBOOK → create_notebook.py --title "..."
5. ADD SOURCE → add_source.py with fetched content or URL
6. WAIT → allow processing (3-5 seconds per source)
7. GENERATE ARTIFACT → create_artifact.py --type [podcast|faq|study_guide|briefing_doc]
8. REPORT → summarize what was created, provide notebook URL + file path
```

### Workflow B: Deep Analysis

When user says "deep analyze", "phân tích sâu", "đọc kỹ":

```
1. AUTH CHECK → verify CLI auth (notebooklm login)
2. DETECT INPUT → identify source type
3. FETCH if needed → convert to file/URL
4. RUN DEEP ANALYSIS → main.py [input] --deep-analysis
5. READ OUTPUT → parse /tmp/[title]_analysis.json
6. REPORT → present structured Q&A to user
```

### Workflow C: Query Existing Notebook

When user shares a NotebookLM URL or says "ask my notebook":

```
1. AUTH CHECK → verify auth
2. RESOLVE NOTEBOOK → find by URL, ID, or active
3. ASK QUESTION → ask_question.py --question "..."
4. ANALYZE → check completeness
5. FOLLOW-UP → if gaps, ask more questions
6. SYNTHESIZE → combine all answers
```

### Workflow D: Multi-Source Pipeline

When user provides multiple sources:

```
1. AUTH CHECK → verify auth
2. CREATE NOTEBOOK → one notebook for all sources
3. FOR EACH SOURCE:
   a. Detect type
   b. Fetch content (Engine 2)
   c. Add source (Engine 1)
   d. Wait for processing
4. SET PROMPT (optional) → update_settings.py
5. GENERATE ARTIFACT → create from combined sources
6. REPORT
```

### Workflow E: Paywall Bypass → NotebookLM

When user shares a paywalled article URL:

```
1. DETECT paywall domain (NYT, WSJ, FT, Economist, Bloomberg, etc.)
2. RUN fetch_url.sh "URL"
   → 8-level cascade: proxy → Googlebot UA → Bingbot UA → Referer spoof → AMP → JSON-LD → archive.today → agent-fetch
3. Save content to /tmp/
4. CREATE NOTEBOOK → add fetched content as source
5. ASK QUESTION or GENERATE ARTIFACT as requested
```

## Intent Detection (Natural Language → Action)

| User says | Intent | Action |
|---|---|---|
| "生成播客" / "做成音频" / "tạo podcast" | audio | Generate podcast |
| "做成PPT" / "生成幻灯片" / "tạo slide" | slide-deck | Generate slides |
| "画个思维导图" / "tạo mindmap" | mind-map | Generate mind map |
| "生成Quiz" / "出题" / "tạo quiz" | quiz | Generate quiz |
| "做个视频" / "tạo video" | video | Generate video |
| "生成报告" / "写个总结" / "viết báo cáo" | report | Generate report |
| "深度分析" / "phân tích sâu" / "deep analysis" | deep-analysis | 3-round questioning |
| "写入飞书" / "lưu vào Feishu" | feishu | Create Feishu doc |
| No specific intent | upload-only | Just upload, wait for next instruction |

## Library Management

```bash
# List all notebooks
python ~/.claude/skills/notebooklm/scripts/run.py notebook_manager.py list
# Search notebooks
python ~/.claude/skills/notebooklm/scripts/run.py notebook_manager.py search --query "research"
# Set active notebook
python ~/.claude/skills/notebooklm/scripts/run.py notebook_manager.py activate --id "notebook-id"
# Statistics
python ~/.claude/skills/notebooklm/scripts/run.py notebook_manager.py stats
```

## Decision Flow

```
User mentions NotebookLM / shares URL / asks to convert content
  |
  v
Auth check → if not authenticated, run setup
  |
  v
What does user want?
  |
  +-- Convert URL/file → artifact ──> Workflow A
  +-- Deep analysis ─────────────────> Workflow B
  +-- Query existing notebook ──────> Workflow C
  +-- Multiple sources ─────────────> Workflow D
  +-- Paywalled article ────────────> Workflow E
  +-- Just upload ──────────────────> CAPABILITY 2
  +-- Unclear ──────────────────────> Ask user
```

## Script Execution Pattern

ALL browser automation scripts run through base skill's `run.py` wrapper:

```bash
# Base skill scripts
python ~/.claude/skills/notebooklm/scripts/run.py <script>.py [args]

# Orchestrator scripts (full path required)
python ~/.claude/skills/notebooklm/scripts/run.py ~/.claude/skills/vibe-notebooklm-orchestrator/scripts/<script>.py [args]

# Content fetching scripts (standalone)
bash ~/.claude/skills/qiaomu-anything-to-notebooklm/scripts/fetch_url.sh "URL"
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/scripts/get_podcast_transcript.py "URL"
python3 ~/.claude/skills/qiaomu-anything-to-notebooklm/main.py [input] [--deep-analysis]

# CLI tools
notebooklm [command] [args]
markitdown [file] [-o output]
```

## Supported Paywall Sites (300+)

| Category | Sites |
|---|---|
| US Media | NYT, WSJ, Bloomberg, Washington Post, The Information, Forbes, WIRED, New Yorker, The Atlantic, USA Today, Boston Globe, LA Times, Chicago Tribune, Seattle Times, MIT Tech Review |
| UK Media | FT, The Times, The Telegraph, The Economist |
| German Media | Spiegel, Zeit, Sueddeutsche, FAZ, Handelsblatt |
| French Media | Le Monde, Le Figaro, Le Parisien |
| Australian | The Australian, SMH, The Age, Brisbane Times |
| Chinese | SCMP, Medium |
| Other | Haaretz, NZ Herald, Statista, Quora |

## Error Handling

| Error | Solution |
|---|---|
| Not authenticated (browser) | Run `auth_manager.py setup` |
| Not authenticated (CLI) | Run `notebooklm login` |
| Auth expired (>7 days) | Run `auth_manager.py reauth` or `notebooklm login` |
| Element not found | UI may have changed. Use `--show-browser` for debugging |
| Timeout on artifact | Podcast takes 2-5 min. Check notebook manually |
| Source upload failed | Retry with `--show-browser` |
| Rate limited | Wait and retry. ~50 queries/day on free accounts |
| Paywall bypass failed | Try `--show-browser` or check archive.today manually |
| Podcast transcription failed | Check `GETNOTE_API_KEY` env var |
| EPUB extraction failed | Verify ebooklib installed: `pip3 install ebooklib beautifulsoup4 lxml` |
| markitdown failed | Check format support: `markitdown --help` |

## Quality Checklist

Before reporting completion:
- Auth was valid throughout
- All requested operations completed
- Notebooks registered in library
- Sources processed (no errors)
- Artifacts generated or queued
- User has notebook URL for manual verification
- Deep analysis output parsed and presented clearly

## Limitations

- Browser automation: no persistent chat sessions (each query = new browser)
- Rate limits: ~50 queries/day on free Google accounts
- Artifact types depend on NotebookLM's current feature set
- UI selectors may break when NotebookLM updates
- Paywall bypass: some hard paywalls (e.g., The Information) may need archive.today CAPTCHA
- Podcast transcription: requires Get笔记 API key
- Deep analysis: requires `notebooklm` CLI auth (separate from browser auth)
- File uploads limited to NotebookLM supported formats
