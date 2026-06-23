---
mo-ta: Mô tả kiến trúc kỹ thuật mong đợi của Agentic RAG Skill Package HR Policy QA
trang-thai: active
phien-ban: v3.0
created-at: 2026-05-27 17:00 +07:00
updated-at: 2026-05-27 17:00 +07:00
---

# Kiến trúc mong đợi: Agentic RAG Skill HR Policy QA

## Tổng quan kiến trúc

```
hr-policy-qa-skill/
  ├── SKILL.md                     ← Agent đọc và tự thi hành
  ├── skill.json                   ← Metadata + quality gates
  ├── schemas/
  │    └── hr-response.schema.json ← Ép đầu ra JSON
  ├── kb/
  │    ├── kb-inventory.md         ← Danh mục 4 tài liệu
  │    └── hr-policies/            ← 4 file .md chính sách
  └── scripts/
       ├── chunker.py              ← Tiền xử lý: tách chunk + metadata + embedding
       ├── retriever.py            ← Tìm kiếm lai: ChromaDB vector + keyword fallback
       └── evaluator.py            ← Tự đánh giá: 12 câu test + cross-check + report
```

## Phase 1: Xây dựng KB (trước khi hỏi)

```
HR Policy .md files
       │
       ▼
  chunker.py
       │
       ├── Parse YAML frontmatter (doc_id, version, status)
       ├── Split by H2 headings (overlap 50 words)
       ├── Generate 7-field metadata per chunk
       └── Embed with sentence-transformers (384 chiều)
              │
              ▼
         ChromaDB Collection "hr_policies"
         (fallback: chunks.json dict)
              │
              ├── 15-20 chunks total
              └── Mỗi chunk: metadata + embedding
```

## Phase 2: Truy vấn real-time (khi có câu hỏi)

```
Câu hỏi người dùng
       │
       ▼
  Bước 1: Phân loại ý định
       │
       ├── In-scope → Tiếp tục Bước 2
       ├── Out-of-scope → Refusal response
       ├── Ambiguous → Clarify request
       └── Prompt injection → Detect + refuse
              │
              ▼ (in-scope)
  Bước 2: Hybrid Retrieval
       │
       ├── scripts/retriever.py --query "..." --top-k 3
       │
       ├── Thử vector search (ChromaDB)
       │   └── Score = 1/(1+distance), range 0.3-0.8
       │
       └── Fallback: keyword search (TF-IDF)
           └── Score range 0.0-0.5
              │
              ▼
  Top-3 chunks + scores
       │
       ├── Score ≥ 0.3 → Tiếp tục
       └── Score < 0.3 → Refusal
              │
              ▼
  Bước 3: Synthesis + Citation + Self-check
       │
       ├── Tổng hợp câu trả lời CHỈ từ chunks
       ├── Gắn citations: doc_id + section + quote (nguyên văn)
       ├── Self-check: cross_check_citation()
       │   ├── Quote khớp chunk gốc → OK
       │   └── Quote KHÔNG khớp → Xóa claim, giảm confidence
       └── Validate JSON schema
              │
              ▼
  Bước 4: Output
       │
       ├── In-scope: answer + citations + confidence
       ├── Out-of-scope: refusal_message + HR contact
       └── Ambiguous: clarification_request
```

## Phase 3: Tự đánh giá (evaluator.py)

```
test-questions.csv (12 câu)
       │
       ▼
  scripts/evaluator.py
       │
       ├── Load 12 test questions
       ├── Chạy từng qua workflow Phase 2
       ├── evaluate_answer(): correctness + citation + refusal
       ├── cross_check_citation(): verify mọi quote
       └── generate_report(): SLI vs SLO
              │
              ▼
  evaluation-report.md
       │
       ├── Bảng SLI tổng hợp
       ├── Chi tiết mỗi câu (PASS/FAIL + lý do)
       └── Khuyến nghị cải thiện
```

## So sánh với Session-03 Agent Skill (tham khảo)

| Thành phần | Session-03 (AI Agent) | Session-04 (Agentic RAG) |
|-----------|----------------------|--------------------------|
| SKILL.md | Trích xuất điều khoản | Hỏi đáp chính sách + RAG |
| schemas/ | contract-term.schema.json | hr-response.schema.json (có self_check_result) |
| kb/ | clause-library + red-flag-rules | kb-inventory + 4 HR policy docs |
| scripts/ | intake + validator + router | chunker + retriever + evaluator |
| Khả năng mới | Routing AUTO/HITL/REJECT | Hybrid retrieval + Citation + Self-check |
| SLI focus | Schema compliance + HITL | Accuracy + Citation rate + No hallucination |
