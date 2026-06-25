---
mo-ta: "Tong quan bai thuc hanh session 05 - mini tool vibe coding theo skill-based pattern"
trang-thai: active
phien-ban: v2.0
created-at: "2026-05-17 13:37 +07:00"
updated-at: "2026-05-27 19:00 +07:00"
---

# Buổi 05: Mini Tool & Vibe Coding

## Mục tiêu

Buổi thực hành giúp bạn làm chủ hai kỹ năng cốt lõi: (1) thiết lập trợ lý AI cá nhân cục bộ với 3 tác tử chuyên biệt cho VTN, đóng gói thành Skill Package chuẩn; (2) vibe coding công cụ che giấu PII kết hợp Regex + Local LLM.

## Cấu trúc bài thực hành

| Phần | Hoạt động | Hình thức | Đầu ra |
| --- | --- | --- | --- |
| A | Thiết kế Agent Profiles (SKILL.md + skill.json) | Thực hành có hướng dẫn | 3 SOUL.md + skill.json |
| B | Xây Security Layer (Hooks + Knowledge Base) | Thực hành có hướng dẫn | Hook script + kb/ + 8 test cases |
| C | Vibe Code Anonymizer Skill | Thực hành nhóm | anonymizer.py + kb/ + schemas/ |
| D | Kiểm thử & Đóng gói | Bài tập nhóm | Test report + cross-team validated |

## Đầu vào

- `synthetic-data/pii-sample-01.txt`: tài liệu có PII rõ ràng
- `synthetic-data/pii-sample-02-tricky.txt`: tài liệu lắt léo, bẫy SCADA, prompt injection
- `templates/agent-spec.md`: biểu mẫu đặc tả 3 agent
- `templates/anonymizer-starter.py`: mã nguồn khung ban đầu
- `templates/local-assistant-runbook.md`: biểu mẫu bàn giao
- `templates/anonymizer-test-report.md`: biểu mẫu báo cáo kiểm thử
- `03-practice/02-study-guides/safety-rules.md`: quy tắc an toàn dữ liệu

## Đầu ra — 2 Skill Packages

### vtn-agent-skill/ (Agent nội bộ)
```
vtn-agent-skill/
├── SKILL.md              ← Persona + Boundaries + Safety
├── skill.json            ← Config: triggers, permissions, quality_gates
├── schemas/              ← Agent output schema
├── kb/                   ← BGP config, incident template, inventory
└── scripts/              ← Hook block-write-and-shell
```

### anonymizer-skill/ (Công cụ che giấu PII)
```
anonymizer-skill/
├── SKILL.md              ← Persona, triggers, 4-step workflow
├── skill.json            ← Config: Regex+LLM hybrid, quality_gates
├── schemas/              ← Anonymized output schema
├── kb/                   ← PII categories, regex patterns, safe terms
└── scripts/              ← anonymizer.py + validator.py
```

### Files bàn giao bắt buộc
1. `agent-spec.md` — Đặc tả 3 agent + kết quả 8 ca kiểm thử hành vi
2. `anonymizer-test-report.md` — Báo cáo kiểm thử 8 ca nâng cao
3. `local-assistant-runbook.md` — Biên bản bàn giao kỹ thuật
4. `execution-log.csv` — Nhật ký thực thi (PII-free)

## SLI/SLO kiểm soát chất lượng

| SLI | Đo lường | SLO (Target) | Measurement |
|-----|----------|-------------|-------------|
| Behavioral test pass (Agent) | 6 ca kiểm thử hành vi PASS | 6/6 (100%) | agent-spec.md |
| Hook enforcement | write_file và terminal bị block | 2/2 PASS | Hook test output |
| Anonymizer test pass | 8 ca kiểm thử PASS | ≥6/8 (75%) | anonymizer-test-report.md |
| PII-free logs | Chuỗi PII thật trong execution-log.csv | 0 | Scan CSV |
| Ollama resilience | Anonymizer chạy khi Ollama disconnected | Regex fallback PASS | Manual test |
| Injection defense | Prompt injection bị phát hiện + HITL flag | T08 PASS | Test T08 result |
| Skill package completeness | Đủ file trong cả 2 skill packages | 8+8 files | File count |
| Cross-team run | ≥1 nhóm khác chạy được anonymizer | 1+ team | Cross-team report |

## Kiến trúc hệ thống

```text
+-----------------------------------------------------------------+
|               TẦNG GIAO DIỆN: CLI / Telegram Bot                |
+-----------------------------------------------------------------+
                                |
+-----------------------------------------------------------------+
|           TẦNG TÁC NHÂN: Hermes Agent (SOUL.md + Hook)          |
+-----------------------------------------------------------------+
                                |
+-----------------------------------------------------------------+
|           TẦNG MÔ HÌNH: Ollama (gemma4, qwen3.5)                |
+-----------------------------------------------------------------+
```

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` lưu ảnh giảng viên thị phạm. Không commit ảnh chụp thô có email, API key, token.

## Tiêu chí hoàn thành

- [ ] 6/6 behavioral agent tests PASS
- [ ] 2/2 hook enforcement tests PASS
- [ ] ≥6/8 anonymizer tests PASS (bắt buộc T03, T07, T08)
- [ ] execution-log.csv không chứa PII gốc
- [ ] Regex fallback chạy khi Ollama disconnected
- [ ] 2 Skill Package hoàn chỉnh (SKILL.md + skill.json + schemas/ + kb/ + scripts/)
- [ ] Cross-team validated

## Quan hệ với session khác

Session-04 (Agentic RAG) xây Skill Package cho RAG. Session-05 kế thừa pattern đó, mở rộng sang: (1) Agent framework cục bộ (Hermes), (2) Mini Tool (Anonymizer) bằng vibe coding. Artifact session-05 (anonymizer.py + Implementation Kit) là đầu vào cho session-06 (Compliance Capstone).
