---
mo-ta: "Tong quan bai thuc hanh session 06 - compliance capstone theo skill-based pattern"
trang-thai: active
phien-ban: v2.0
created-at: "2026-05-17 13:37 +07:00"
updated-at: "2026-05-27 19:00 +07:00"
---

# Buổi 06: Kiểm thử, Compliance & Capstone

## Mục tiêu

Buổi Capstone kéo dài 4 giờ, chuyển đổi Mini Tool Anonymizer (session-05) từ bản thử nghiệm thành giải pháp hoàn chỉnh sẵn sàng thí điểm tại VTN, thông qua 3 trụ cột: kiểm thử nghiêm ngặt, đánh giá tuân thủ + phòng thủ injection, và đóng gói hồ sơ triển khai.

## Cấu trúc bài thực hành

| Phần | Hoạt động | Hình thức | Đầu ra |
| --- | --- | --- | --- |
| A | Thiết kế Test Cases + chạy test pass đầu | Thực hành có hướng dẫn | test-cases-specification.md |
| B | Compliance Check + Prompt Injection Defense | Thực hành có hướng dẫn | compliance-checklist.md |
| C | E2E Testing + Bug Fixing | Thực hành nhóm | execution-log.csv (10/10 PASS) |
| D | Implementation Kit + Capstone Presentation | Bài tập nhóm | 7 templates + Capstone slides |

## Đầu vào

- **Từ session-05**: `anonymizer.py` (mã nguồn đã vibe coding), `anonymizer-skill/` (skill package)
- [synthetic-data/edge-cases-sample.txt](synthetic-data/edge-cases-sample.txt): dữ liệu biên (tên trùng danh từ, CCCD lỗi)
- [synthetic-data/prompt-injection-attacks.txt](synthetic-data/prompt-injection-attacks.txt): 3 kịch bản tấn công injection
- [references/anonymizer-solution.py](references/anonymizer-solution.py): mã nguồn tham khảo
- `03-practice/02-study-guides/safety-rules.md`: quy tắc an toàn dữ liệu

## Đầu ra

Mỗi nhóm nộp **`session-06-capstone-handover-[TenNhom].zip`** chứa:
1. `anonymizer.py` — mã nguồn đã qua kiểm thử (10/10 PASS + 3/3 injection blocked)
2. Implementation Kit — 7 templates đã điền đầy đủ
3. Capstone slide deck

## SLI/SLO kiểm soát chất lượng

| SLI | Đo lường | SLO (Target) | Measurement |
|-----|----------|-------------|-------------|
| E2E test pass rate | 10 ca kiểm thử PASS | 10/10 (100%) | test-cases-specification.md |
| Prompt injection defense | 3 kịch bản tấn công bị chặn | 3/3 (100%) | compliance-checklist.md |
| Clean logs | PII trong execution-log.csv | 0 | Scan CSV |
| Implementation Kit completeness | 7 templates điền đầy đủ | 7/7 (100%) | File count + content check |
| Capstone presentation | Slide deck delivered | Yes/No | Manual |

## Kiến trúc nghiệm thu

```text
+-------------------------------------------------------------------+
|               TẦNG TEST INPUT                                      |
|    [ edge-cases-sample.txt ]     [ prompt-injection-attacks.txt ] |
+-------------------------------------------------------------------+
                                  |
+-------------------------------------------------------------------+
|           TẦNG CORE MINI TOOL (Regex + LLM + Schema)              |
|    * Bộ lọc Regex + Local LLM    * Log phi nhạy cảm               |
|    * Ép Schema nghiêm ngặt       * HITL phê duyệt                 |
+-------------------------------------------------------------------+
                                  |
+-------------------------------------------------------------------+
|           TẦNG IMPLEMENTATION KIT                                  |
|    * Runbook    * Failure Modes    * One Pager    * 30/90 Plan     |
+-------------------------------------------------------------------+
```

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` lưu ảnh giảng viên thị phạm. Không commit ảnh chụp thô có email, API key, token.

## Tiêu chí hoàn thành

- [ ] 10/10 test cases PASS
- [ ] 3/3 injection attacks blocked
- [ ] execution-log.csv không chứa PII gốc
- [ ] 7/7 Implementation Kit templates hoàn chỉnh
- [ ] Capstone slide deck + demo trơn tru

## Quan hệ với session khác

Session-05 xây anonymizer (vibe coding). Session-06 là Capstone — nghiệm thu, vá lỗi, đóng gói. Artifact cuối cùng là Implementation Kit hoàn chỉnh, sẵn sàng trình Ban giám đốc VTN phê duyệt thí điểm.
