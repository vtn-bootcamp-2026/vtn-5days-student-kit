---
mo-ta: "tong quan bai thuc hanh session 05 — 2 track song song: Track A (vibe-working, build skill review-contract) va Track B (lam tay, contract-term-extractor)"
trang-thai: active
phien-ban: v4.1
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-23 22:45 +07:00
---

# Session 05: AI Agent review hợp đồng — đóng gói Agent Skill (2 track)

> [!NOTE]
> **Cùng chủ đề "AI Agent review hợp đồng" — 2 lối vào:**
>
> | Track | File | Cách tiếp cận | Phù hợp |
> |-------|------|--------------|---------|
> | **A — Vibe Working** | [lab.md](lab.md) | Dùng skill `vibe-aiworkforce` + `vibe-improve` để design → generate → improve skill `review-contract` | HV muốn học workflow thời AI, ít code tay |
> | **B — Làm tay** | [lab-handbuilt.md](lab-handbuilt.md) | Tự viết SKILL.md / skill.json / schemas / kb / scripts | HV muốn hiểu sâu "ruột" một skill |
>
> Chọn 1 track, hoặc làm Track A rồi_Vertief Track B. Cả 2 cùng build một loại skill (review/extract điều khoản hợp đồng).

## Mục tiêu (chung cả 2 track)

Học viên đóng gói quy trình rà soát hợp đồng viễn thông thành một **Agent Skill** — một "kỹ năng chuyên biệt" (giống App): cài đặt được, chạy được, nâng cấp được. Khác biệt giữa 2 track là **cách build**:

- **Track A:** HV viết `skill_design.md` (IPO) → skill `vibe-aiworkforce` tự sinh skill → `vibe-improve` nâng cấp. (hiện thực hóa slide vibe-working)
- **Track B:** HV tự viết từng file (SKILL.md, skill.json, schemas/, kb/, scripts/). (hiểu sâu cấu trúc)

Sau khi hoàn thành (cả 2 track), HV nắm vững:
* Thiết kế skill theo cấu trúc IPO / SKILL.md — bản đồ chỉ dẫn cho Agent
* Triggers + permissions — kiểm soát khi nào skill chạy, làm gì được
* schemas/ — lược đồ JSON ép định dạng đầu ra
* kb/ — kho tri thức (điều khoản mẫu, quy tắc cờ đỏ)
* Quality Gate + HITL — Do/Don't, khi nào chuyển người duyệt

Học viên đóng gói toàn bộ quy trình trích xuất điều khoản hợp đồng thành một "Kỹ năng chuyên biệt của AI" (Agent Skill). Thay vì viết script Python chạy đơn lẻ, học viên học cách thiết kế chỉ dẫn cho Agent (SKILL.md), cấu hình metadata (skill.json), xây kho tri thức (kb/) và công cụ thi hành (scripts/).

Sau khi hoàn thành, học viên nắm vững:

* Thiết kế SKILL.md — bản đồ chỉ dẫn cho Agent, bao gồm vai trò, quy trình, hướng dẫn gọi tool
* Xây schemas/ — lược đồ JSON ép định dạng đầu ra
* Tạo kb/ — kho tri thức phục vụ tra cứu (điều khoản mẫu, quy tắc phát hiện cờ đỏ)
* Viết scripts/ — công cụ Python được Agent gọi chạy tự động (intake, validator, router)
* Chạy test chéo giữa các nhóm — nạp Skill của nhóm khác vào Agent để kiểm tra độ ổn định

## Cấu trúc bài thực hành

### Track A — Vibe Working ([lab.md](lab.md))

| Bài | Hoạt động | Đầu ra |
|-----|-----------|--------|
| BT1 | Viết `skill_design.md` theo IPO | skill_design.md hoàn chỉnh |
| BT2 | `vibe-aiworkforce` generate + `vibe-packaging` đóng ZIP + cài + test | review-contract.zip, test ≥ 3/4 ca |
| BT3 | `vibe-improve` mở rộng `.pdf` + `.xlsx` | skill chạy multi-format |
| BT4 (nâng cao) | red-flag library + condact PII | skill an toàn hơn |

### Track B — Làm tay ([lab-handbuilt.md](lab-handbuilt.md))

| Phần | Hoạt động | Đầu ra |
| --- | --- | --- |
| A | Thiết kế SKILL.md và skill.json | SKILL.md + skill.json |
| B | Xây schemas và kho tri thức | JSON schema + clause library + red-flag rules |
| C | Viết scripts công cụ thi hành | intake.py + validator.py + router.py |
| D | Test chéo và đóng gói Skill Package | test report + execution log + cross-team validation |

## Đầu vào

- [02-study-guides/case-studies.md](../../../02-study-guides/case-studies.md): mô tả Case 8 - Contract Term Extractor
- [03-practice/02-study-guides/safety-rules.md](../../../02-study-guides/safety-rules.md): quy tắc an toàn dữ liệu
- [synthetic-data/contracts/](synthetic-data/contracts/): 4 hợp đồng mô phỏng (.docx, trình bày Nghị định 30)
- [synthetic-data/contracts-index.csv](synthetic-data/contracts-index.csv): bảng chỉ mục hợp đồng
- [templates/SKILL.md](templates/SKILL.md): mẫu bản đồ chỉ dẫn Agent
- [templates/skill.json](templates/skill.json): mẫu cấu hình metadata
- [templates/test-cases.md](templates/test-cases.md): mẫu bộ test case
- [templates/skills/contract-term-extractor/schemas/contract-term.schema.json](templates/skills/contract-term-extractor/schemas/contract-term.schema.json): lược đồ JSON hoàn chỉnh
- [templates/skills/contract-term-extractor/kb/clause-library.md](templates/skills/contract-term-extractor/kb/clause-library.md): thư viện điều khoản mẫu
- [templates/skills/contract-term-extractor/kb/red-flag-rules.md](templates/skills/contract-term-extractor/kb/red-flag-rules.md): quy tắc phát hiện cờ đỏ
- [templates/skills/contract-term-extractor/scripts/intake.py](templates/skills/contract-term-extractor/scripts/intake.py): tool tiếp nhận mẫu
- [templates/skills/contract-term-extractor/scripts/validator.py](templates/skills/contract-term-extractor/scripts/validator.py): tool tự kiểm mẫu
- [templates/skills/contract-term-extractor/scripts/router.py](templates/skills/contract-term-extractor/scripts/router.py): tool định tuyến mẫu

### Đầu vào riêng Track A (vibe-working)

- [skills/](skills/): 2 skill cài sẵn (`vibe-aiworkforce.zip`, `vibe-improve-orchestrator.zip`) + [hướng dẫn cài](skills/README.md)
- [templates/skill-design/skill_design.md](templates/skill-design/skill_design.md): template IPO (BT1)
- [templates/skill-design/generate_skill_design.md](templates/skill-design/generate_skill_design.md): prompt generate skill_design (BT1 đường 2)
- [templates/prompt/](templates/prompt/): thư mục chứa các prompt mẫu tạo sẵn hỗ trợ thực hành từ BT1 đến BT4
- [templates/skill-design/skill_design.review-contract.example.md](templates/skill-design/skill_design.review-contract.example.md): đáp án tham khảo BT1
- [templates/skills/review-contract/](templates/skills/review-contract/): **skill mẫu** (cấu trúc kỳ vọng BT2) — HV đối chiếu skill mình build
- [synthetic-data/contracts/contract-001.pdf](synthetic-data/contracts/contract-001.pdf), [contract-005-spreadsheet.xlsx](synthetic-data/contracts/contract-005-spreadsheet.xlsx): biến thể đa-format cho BT3

## Đầu ra

Mỗi nhóm hoàn thành Agent Skill Package gồm:

1. `SKILL.md` — bản đồ chỉ dẫn cho Agent (vai trò, quy trình, hướng dẫn gọi tool)
2. `skill.json` — metadata, triggers, permission gates
3. `contract-term.schema.json` — lược đồ JSON chuẩn hóa đầu ra
4. `clause-library.md` — kho điều khoản mẫu, tối thiểu 8 điều khoản
5. `red-flag-rules.md` — quy tắc phát hiện cờ đỏ, tối thiểu 5 rule
6. `intake.py` + `validator.py` + `router.py` — 3 scripts thi hành
7. `extracted-terms JSON` — kết quả trích xuất contract-001 và contract-003, có source evidence
8. `test-report.md` — báo cáo kiểm thử tối thiểu 14 ca
9. `execution-log.csv` — nhật ký chạy 4 hợp đồng

## SLI/SLO kiểm soát chất lượng

| SLI | Đo lường | SLO (Target) | Measurement |
| --- | --- | --- | --- |
| Test case pass rate | % test cases PASS | >= 75% (11/14) | test-report.md |
| HITL coverage | % risk cases bật needs_human_review=true | 100% | Kiểm tra JSON output |
| Source evidence | % extractions có source_evidence | 100% | Kiểm tra trường source_evidence |
| Self-check success | % cases self-check phát hiện lỗi | >= 80% | Log self-check |
| Schema compliance | % outputs khớp JSON schema | 100% | JSON validation |
| Cross-team pass | Tối thiểu 1 nhóm khác chạy được Skill | 1+ | Cross-team test report |
| No real data | Số lần lộ dữ liệu thật | 0 | Quét contracts, output, log |

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` lưu ảnh giảng viên thị phạm đã kiểm duyệt. Không commit ảnh chụp thô có email, mã số thuế, tên đối tác hoặc số tiền thương mại thật.

## Tiêu chí hoàn thành

- [ ] Agent Skill Package có đủ SKILL.md, skill.json, schemas/, kb/, scripts/
- [ ] SKILL.md đủ rõ để Agent (hoặc đồng nghiệp) đọc và thực thi đúng quy trình 4 bước
- [ ] Chạy được ít nhất 14 test case với tỷ lệ pass >= 75%
- [ ] 100% ca thiếu dữ liệu, mâu thuẫn hoặc cờ đỏ chuyển HITL (needs_human_review=true)
- [ ] Kết quả trích xuất có source_evidence, không khẳng định suông
- [ ] Tối thiểu 1 nhóm khác chạy được Skill của nhóm mình
- [ ] Không chứa dữ liệu thật: hợp đồng thật, tên đối tác thật, mã số thuế thật

## Quan hệ với session khác

**Đầu vào từ session 04:** học viên đã nắm quy trình AI workflow, xử lý lỗi và HITL trên n8n. Session 05 chuyển từ workflow tự động sang đóng gói Agent Skill chuyên biệt.

**Bàn giao sang session 06:** Agent Skill này làm tiền đề cho Knowledge Base. Kho tri thức (kb/) trong Skill là RAG mini — session 06 sẽ mở rộng thành hệ thống RAG quy mô lớn cho Case 7 (HR Policy Q&A).
