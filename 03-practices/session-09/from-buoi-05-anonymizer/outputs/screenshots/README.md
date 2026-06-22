---
mo-ta: "Huong dan chup anh man hinh thi pham cho session 05"
trang-thai: active
phien-ban: v1.0
created-at: "2026-05-27 19:00 +07:00"
updated-at: "2026-05-27 19:00 +07:00"
---

# Hướng dẫn chụp ảnh màn hình thị phạm — Session 05

## Danh sách ảnh cần chụp

### Part A: Agent Profiles

| STT | Tên file | Nội dung chụp | Ghi chú |
|-----|----------|---------------|---------|
| 1 | `ollama-running.jpg` | Ollama xác nhận chạy (`Ollama is running`) | Terminal |
| 2 | `hermes-chat.jpg` | Hermes chat xác nhận model đúng | Terminal |

### Part B: Security Layer + Behavioral Tests

| STT | Tên file | Nội dung chụp | Ghi chú |
|-----|----------|---------------|---------|
| 3 | `BGP.jpg` | Agent 1 trả lời đúng câu hỏi BGP | Hermes chat |
| 4 | `OSPF.jpg` | Agent 1 từ chối câu hỏi ngoài phạm vi (OSPF) | Hermes chat |
| 5 | `bao_cao_su_co.jpg` | Agent 2 viết báo cáo sự cố | Hermes chat |
| 6 | `bao_cao_mat_ping.jpg` | Agent 2 che IP, không suy diễn | Hermes chat |
| 7 | `check_list_5_phan.jpg` | Agent 3 lập checklist 5 phần | Hermes chat |
| 8 | `format_drive.jpg` | Agent 3 từ chối thao tác phá hoại | Hermes chat |
| 9 | `write_file_blocked_hook.jpg` | Hook chặn write_file | Terminal output |

### Part C: Anonymizer Vibe Coding

| STT | Tên file | Nội dung chụp | Ghi chú |
|-----|----------|---------------|---------|
| 10 | `anonymizer-pii-sample-01.jpg` | Chạy anonymizer trên pii-sample-01.txt | Terminal output |
| 11 | `anonymizer-pii-sample-02.jpg` | Chạy anonymizer trên pii-sample-02-tricky.txt | Terminal output |

### Part D: Testing + Packaging

| STT | Tên file | Nội dung chụp | Ghi chú |
|-----|----------|---------------|---------|
| 12 | `test-report.jpg` | anonymizer-test-report.md điền đầy đủ | Text editor |
| 13 | `execution-log.jpg` | execution-log.csv sạch PII | Spreadsheet |

## Ảnh hiện có

7 ảnh đã chụp từ phiên bản cũ (Part B — Agent behavioral tests):
- `BGP.jpg`, `OSPF.jpg` — Agent 1 tests
- `bao_cao_su_co.jpg`, `bao_cao_mat_ping.jpg` — Agent 2 tests
- `check_list_5_phan.jpg`, `format_drive.jpg` — Agent 3 tests
- `write_file_blocked_hook.jpg` — Hook validation

## Quy tắc chụp

- KHÔNG commit ảnh chụp thô có email thật, API key, token
- Ảnh cần rõ nét, chữ đọc được
- Đặt tên file theo convention: kebab-case, mô tả nội dung
- Kích thước tối đa: 500KB/ảnh (resize nếu cần)
