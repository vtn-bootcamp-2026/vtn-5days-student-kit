---
mo-ta: tong quan bai thuc hanh session 04 Agentic RAG Skill cho HR Policy QA
trang-thai: active
phien-ban: v3.0
created-at: 2026-05-27 17:00 +07:00
updated-at: 2026-06-18 09:15 +07:00
---

# Buổi 04: Đóng gói Kỹ năng Hỏi đáp Chính sách Nhân sự (Agentic RAG Skill)

## Mục tiêu

Buổi này học viên đóng gói hệ thống hỏi đáp chính sách nhân sự thành **Agentic RAG Skill**, vận dụng mẫu Agent Skill Packaging ở buổi 03. Thay vì xây RAG riêng lẻ, học viên tích hợp SKILL.md, kho tri thức, schema đầu ra, và tool scripts thành Skill Package hoàn chỉnh -- sẵn sàng nạp vào Agent và chạy chéo giữa các nhóm.

Kết thúc buổi, học viên có khả năng:

* Thiết kế SKILL.md -- bản đồ chỉ dẫn Agent xử lý RAG (truy xuất, tổng hợp, trích dẫn, từ chối an toàn)
* Xây kb/ -- kho tri thức cấu trúc, có phiên bản và metadata từ 4 tài liệu chính sách nhân sự
* Tạo schemas/ -- lược đồ JSON chuẩn hóa câu trả lời (trích dẫn nguồn, self-check, cờ HITL)
* Viết scripts/ -- 3 tool Python để Agent gọi tự động: chunker, retriever, evaluator
* Test chéo và tự đánh giá -- 12 câu hỏi kiểm thử, SLI/SLO rõ ràng

## Bối cảnh tình huống

**Case 7: HR Policy Q&A** -- Bạn là thành viên phòng Nhân sự tại một doanh nghiệp viễn thông. Hàng tuần, nhân viên và quản lý liên tục hỏi về nghỉ phép, phụ cấp, thâm niên và đào tạo -- phần lớn là câu lặp lại. Nhiệm vụ: đóng gói Agentic RAG Skill để Agent truy xuất đúng tài liệu, trả lời trúng trọng tâm, trích dẫn rõ nguồn -- và từ chối an toàn khi thiếu căn cứ.

> **NGUYÊN TẮC CỐT LÕI:** Hệ thống chỉ trả lời trong phạm vi tri thức đã nạp. Không phỏng đoán bằng kiến thức chung. Câu hỏi ngoài phạm vi hoặc mơ hồ phải từ chối hoặc yêu cầu làm rõ. Mọi câu trả lời phải có trích dẫn nguồn.

## Nền tảng từ buổi 03

Buổi 03 đã giới thiệu mẫu **Agent Skill Packaging**: SKILL.md (chỉ dẫn Agent), skill.json (metadata + triggers), schemas/ (chuẩn hóa đầu ra), kb/ (kho tri thức), scripts/ (tool thực thi). Buổi 04 áp dụng toàn bộ mẫu đó vào bài toán RAG -- chuyển từ Agent trích xuất hợp đồng sang Agent hỏi đáp kho tri thức.

## Công nghệ

| Công nghệ | Phiên bản | Mục đích |
| --- | --- | --- |
| ChromaDB | >=0.4.0 | Vector store cho semantic search |
| sentence-transformers | >=2.2.0 | Embedding model (paraphrase-multilingual-MiniLM-L12-v2) |
| Google Gemini API | gemini-2.0-flash | Sinh câu trả lời |
| Antigravity IDE | -- | Môi trường phát triển local (Python) |

**Cài đặt:** `pip install chromadb sentence-transformers`

> ChromaDB không bắt buộc. Nếu chưa cài, retriever tự động dùng keyword matching. Dù vậy, vector search cho kết quả ổn hơn nhiều khi xử lý câu hỏi phức tạp.

## Cấu trúc bài thực hành

| Phần | Thời lượng | Hoạt động | Đầu ra |
| --- | ---: | --- | --- |
| A | 45 phút | Thiết kế SKILL.md + skill.json | Agent instruction map + metadata config |
| B | 60 phút | Xây kb/ + schemas/ | KB inventory + 4 tài liệu HR + JSON response schema |
| C | 75 phút | Viết scripts/ (chunker, retriever, evaluator) | 3 tool scripts cho Agent |
| D | 60 phút | Test chéo + tự đánh giá | Evaluation report (12 câu hỏi, SLI/SLO) |

## Đầu vào

- [02-study-guides/case-studies.md](../../../02-study-guides/case-studies.md): mô tả Case 7 -- HR Policy Q&A
- [03-practice/02-study-guides/safety-rules.md](../../../02-study-guides/safety-rules.md): quy tắc an toàn dữ liệu
- [synthetic-data/hr-policies/](synthetic-data/hr-policies/): 4 tài liệu chính sách nhân sự mô phỏng
  - `policy-leave.md` -- chính sách nghỉ phép, nghỉ ốm, nghỉ thai sản
  - `policy-allowance.md` -- chính sách phụ cấp (ăn trưa, đi lại, điện thoại)
  - `policy-seniority.md` -- chính sách thâm niên và thưởng
  - `policy-training.md` -- chính sách đào tạo và phát triển
- [synthetic-data/test-questions.csv](synthetic-data/test-questions.csv): 12 câu hỏi kiểm thử (8 trong phạm vi, 2 mơ hồ, 2 ngoài phạm vi)
- [templates/SKILL.md](templates/SKILL.md): mẫu bản đồ chỉ dẫn Agent
- [templates/skill.json](templates/skill.json): mẫu cấu hình metadata
- [templates/test-cases.md](templates/test-cases.md): mẫu bộ test case
- [templates/skills/hr-policy-qa-skill/](templates/skills/hr-policy-qa-skill/): worked-example Skill Package (tham khảo)

## Đầu ra -- Skill Package (8 artifact bắt buộc)

Mỗi nhóm hoàn thành một Agentic RAG Skill Package gồm 8 file:

| # | Artifact | Mô tả |
| ---: | --- | --- |
| 1 | `SKILL.md` | Bản đồ chỉ dẫn cho Agent -- 6 section (vai trò, quy trình, KB, tools, giới hạn, self-check) |
| 2 | `skill.json` | Metadata, triggers, permission gates, model config |
| 3 | `schemas/hr-response.schema.json` | Lược đồ JSON chuẩn hóa câu trả lời (answer, citations, confidence, needs_review) |
| 4 | `kb/kb-inventory.md` | Danh mục kho tri thức -- 4 tài liệu HR, chủ sở hữu, chu kỳ cập nhật, trạng thái |
| 5 | `scripts/chunker.py` | Tool chia nhỏ tài liệu thành chunks + gán metadata, lưu vào ChromaDB |
| 6 | `scripts/retriever.py` | Tool truy xuất chunks liên quan (vector search + fallback keyword matching) |
| 7 | `scripts/evaluator.py` | Tool tự đánh giá -- chạy 12 câu hỏi, tính SLI, sinh evaluation report |
| 8 | `evaluation-report.md` | Báo cáo đánh giá 12 câu hỏi -- kết quả, trích dẫn, pass/fail, phân tích lỗi |

## SLI/SLO kiểm soát chất lượng

| SLI | Đo lường | SLO (Target) | Measurement |
| --- | --- | --- | --- |
| In-scope accuracy | % câu trong phạm vi trả lời đúng + trích dẫn | >= 75% (6/8) | evaluation-report |
| Out-of-scope refusal | % câu ngoài phạm vi từ chối trả lời | 100% (2/2) | evaluation-report |
| Citation rate | % câu trả lời có trích dẫn nguồn | >= 90% | evaluation-report |
| No hallucinated citations | % citations khớp tài liệu gốc | 100% | Cross-check quote nguyên văn |
| Self-check success | % cases self-check phát hiện lỗi | >= 80% | evaluator.py log |
| Skill package completeness | Số file bắt buộc hoàn chỉnh | 8/8 | Kiểm tra thư mục |
| Cross-team run | Tối thiểu 1 nhóm khác chạy được Skill | >= 1 | Cross-team test report |
| No sensitive info leak | Số lần lộ thông tin nhạy cảm | 0 | Manual review |

## Quy tắc an toàn

- Chỉ sử dụng tài liệu chính sách nhân sự mô phỏng trong `synthetic-data/`
- Không đưa chính sách nội bộ thật, thông tin lương thật hay dữ liệu nhân sự thật vào bài
- Không đính kèm token, API key hay mật khẩu trong bài nộp
- Nếu dùng Gemini API, chỉ cấu hình qua biến môi trường local hoặc tài khoản demo
- Không commit ảnh chụp chứa thông tin nội bộ hoặc dữ liệu nhân sự thật

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` chứa ảnh giảng viên thị phạm đã kiểm duyệt. Các ảnh minh họa kết quả từng bước (chunking, vector search, RAG pipeline, evaluation) để học viên đối chiếu trong lúc thực hành.

## Tiêu chí hoàn thành

- [ ] **Skill Package hoàn chỉnh 8/8 files** -- SKILL.md, skill.json, hr-response.schema.json, kb-inventory.md, chunker.py, retriever.py, evaluator.py, evaluation-report.md
- [ ] **In-scope accuracy >= 75%** -- ít nhất 6/8 câu hỏi trong phạm vi trả lời đúng + trích dẫn
- [ ] **Out-of-scope refusal 100%** -- 2/2 câu hỏi ngoài phạm vi từ chối rõ ràng
- [ ] **Citation rate >= 90%** -- câu trả lời có trích dẫn nguồn hợp lệ
- [ ] **Không có trích dẫn giả** -- cross-check 100% citations khớp tài liệu gốc
- [ ] **Cross-team >= 1 nhóm khác** -- Skill của nhóm mình chạy được trên nhóm khác

## Quan hệ với session khác

**Đầu vào từ session 03:** Học viên đã biết đóng gói Agent Skill với SKILL.md, skill.json, schemas, kb, scripts. Session 04 áp dụng toàn bộ mẫu này vào bài toán RAG -- chuyển từ Agent trích xuất hợp đồng sang Agent hỏi đáp kho tri thức.

**Bàn giao sang session 05:** Skill Package RAG này làm tiền đề cho session 05 (Mini Tool -- Local AI Data Anonymizer). Mẫu Agent Skill Packaging tiếp tục được sử dụng và mở rộng.
