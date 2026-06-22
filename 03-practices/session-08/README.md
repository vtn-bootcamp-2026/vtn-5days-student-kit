---
mo-ta: tong quan bai thuc hanh session 03 dong goi Agent Skill contract term extractor
trang-thai: active
phien-ban: v3.0
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-18 09:15 +07:00
---

# Session 03: đóng gói Agent Skill trích xuất điều khoản hợp đồng

## Mục tiêu

Học viên đóng gói toàn bộ quy trình trích xuất điều khoản hợp đồng thành một "Kỹ năng chuyên biệt của AI" (Agent Skill). Thay vì viết script Python chạy đơn lẻ, học viên học cách thiết kế chỉ dẫn cho Agent (SKILL.md), cấu hình metadata (skill.json), xây kho tri thức (kb/) và công cụ thi hành (scripts/).

Sau khi hoàn thành, học viên nắm vững:

* Thiết kế SKILL.md — bản đồ chỉ dẫn cho Agent, bao gồm vai trò, quy trình, hướng dẫn gọi tool
* Xây schemas/ — lược đồ JSON ép định dạng đầu ra
* Tạo kb/ — kho tri thức phục vụ tra cứu (điều khoản mẫu, quy tắc phát hiện cờ đỏ)
* Viết scripts/ — công cụ Python được Agent gọi chạy tự động (intake, validator, router)
* Chạy test chéo giữa các nhóm — nạp Skill của nhóm khác vào Agent để kiểm tra độ ổn định

## Cấu trúc bài thực hành

| Phần | Hoạt động | Hình thức | Đầu ra |
| --- | --- | --- | --- |
| A | Thiết kế SKILL.md và skill.json | Thực hành có hướng dẫn | SKILL.md + skill.json |
| B | Xây schemas và kho tri thức | Bài tập nhóm | JSON schema + clause library + red-flag rules |
| C | Viết scripts công cụ thi hành | Bài tập nhóm | intake.py + validator.py + router.py |
| D | Test chéo và đóng gói Skill Package | Bài tập nhóm | test report + execution log + cross-team validation |

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

**Đầu vào từ session 02:** học viên đã nắm quy trình AI workflow, xử lý lỗi và HITL trên n8n. Session 03 chuyển từ workflow tự động sang đóng gói Agent Skill chuyên biệt.

**Bàn giao sang session 04:** Agent Skill này làm tiền đề cho Knowledge Base. Kho tri thức (kb/) trong Skill là RAG mini — session 04 sẽ mở rộng thành hệ thống RAG quy mô lớn cho Case 7 (HR Policy Q&A).
