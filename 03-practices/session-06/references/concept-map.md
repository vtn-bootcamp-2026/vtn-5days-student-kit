---
mo-ta: Sơ đồ kiến trúc và bản đồ khái niệm cho Agentic RAG Skill HR Policy QA
trang-thai: active
phien-ban: v3.0
created-at: 2026-05-27 17:00 +07:00
updated-at: 2026-05-27 17:00 +07:00
---

# Concept Map: Agentic RAG Skill

## Sơ đồ kiến trúc tổng thể

```
                          AGENTIC RAG SKILL PACKAGE
                          ========================

  SKILL.md (Bản đồ chỉ dẫn)          skill.json (Metadata)
  ┌──────────────────────┐          ┌──────────────────────┐
  │ 1. Persona           │          │ name, version         │
  │ 2. Triggers          │◄────────►│ triggers (keywords)   │
  │ 3. Execution Workflow│          │ permissions            │
  │ 4. Output Format     │          │ quality_gates          │
  │ 5. Boundaries        │          └──────────────────────┘
  │ 6. Safety Rules      │
  └──────────┬───────────┘
             │
             │ Agent đọc và thi hành
             ▼
  ┌─────────────────────────────────────────────────────┐
  │                 EXECUTION WORKFLOW                   │
  │                                                     │
  │  Bước 1: Intake & Classification                    │
  │    ↓                                                 │
  │  Bước 2: Hybrid Retrieval                           │
  │    ├── scripts/retriever.py                         │
  │    ├── ChromaDB (vector) + keyword fallback         │
  │    └── kb/hr-policies/ ←───── Knowledge Base        │
  │    ↓                                                 │
  │  Bước 3: Synthesis + Citation + Self-check          │
  │    ├── schemas/hr-response.schema.json              │
  │    ├── Cross-check quote vs chunk gốc               │
  │    └── Confidence calibration                       │
  │    ↓                                                 │
  │  Bước 4: Output / Refusal                           │
  │    ├── In-scope → answer + citations                │
  │    ├── Out-of-scope → refusal + HR contact          │
  │    └── Ambiguous → clarify request                  │
  └─────────────────────────────────────────────────────┘
             │
             │ Tự đánh giá
             ▼
  ┌──────────────────────────┐
  │ scripts/evaluator.py     │
  │ ├── 12 test questions    │
  │ ├── Cross-check quotes   │
  │ └── SLI vs SLO report    │
  └──────────────────────────┘
```

## So sánh: Static RAG vs Agentic RAG

| Khía cạnh | Static RAG | Agentic RAG Skill |
|-----------|-----------|-------------------|
| Cấu trúc | Code Python chạy tuần tự | Skill Package (SKILL.md + scripts/) |
| Phân loại câu hỏi | Không có — tất cả đều được retrieval | 4 loại: in-scope, out-of-scope, ambiguous, injection |
| Retrieval | Chỉ vector hoặc chỉ keyword | Hybrid: vector (ưu tiên) + keyword (fallback) |
| Trích dẫn | Có nhưng không verify | Bắt buộc, có cross-check quote với chunk gốc |
| Tự kiểm duyệt | Không có | Self-check: tự động phát hiện hallucination |
| Từ chối | Thủ công | Tự động, dựa trên threshold và phân loại |
| Đánh giá | Thủ công | Tự động: evaluator.py chạy 12 câu, xuất báo cáo SLI |
| Tái sử dụng | Không — mỗi lần viết riêng | Có — Skill package nạp được vào bất kỳ Agent nào |

## Bản đồ thuật ngữ (Glossary)

| Thuật ngữ tiếng Việt | English term | Giải thích |
|----------------------|-------------|-----------|
| Truy xuất tăng cường | Retrieval-Augmented Generation (RAG) | Kết hợp truy xuất thông tin với sinh văn bản |
| Tìm kiếm lai | Hybrid Retrieval | Kết hợp vector search và keyword matching |
| Kho tri thức | Knowledge Base (KB) | Bộ tài liệu dành cho Agent tra cứu |
| Chunk | Chunk | Đoạn văn bản nhỏ tách từ tài liệu gốc |
| Trích dẫn | Citation | Thông tin nguồn gồm doc_id, section, quote |
| Tự kiểm duyệt | Self-check / Cross-check | Tự đối chiếu quote với chunk gốc để bắt sai |
| Từ chối an toàn | Safe Refusal | Từ chối trả lời khi không đủ bằng chứng |
| Gói kỹ năng | Skill Package | Folder chứa SKILL.md, skill.json, schemas/, kb/, scripts/ |
| Ngưỡng chất lượng | Quality Gate | Điều kiện SLI/SLO cần đạt trước khi nghiệm thu |
| Người-vòng-lặp | Human-in-the-Loop (HITL) | Chuyển xử lý cho người thật khi gặp edge case |
| Mã hóa vector | Embedding | Biểu diễn văn bản dưới dạng vector số để tìm kiếm tương đồng |
| Trộm kho vector | Vector Store (ChromaDB) | CSDL lưu trữ và truy vấn vector |

## Luồng dữ liệu trong Agentic RAG Skill

```
1. XÂY DỰNG KB (trước khi hỏi)
   HR Policy .md → chunker.py → chunks (15-20) → ChromaDB
                                      ↓
                              metadata (7 fields)
                                      ↓
                              embeddings (384 chiều)

2. TRUY VẤN (khi có câu hỏi)
   Câu hỏi → Phân loại → Hybrid Retrieval → Top-3 chunks
              ↓                                    ↓
         In-scope?                        Score ≥ 0.3?
              ↓                                    ↓
           Có → Synthesis                    Có → Tiếp tục
           Không → Refusal                   Không → Refusal

3. TỔNG HỢP (sau khi có chunks)
   Top-3 chunks → Sinh câu trả lời → Gắn citations
                                       ↓
                                  Self-check: quote vs chunk
                                       ↓
                                  OK → Output JSON
                                  Fail → Xóa claim sai → Giảm confidence

4. ĐÁNH GIÁ (tự động)
   12 test questions → Chạy qua luồng 1-3 → Cross-check
                                                    ↓
                                              evaluation-report.md
```
