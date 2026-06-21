---
mo-ta: ban do luong thuc hanh khoa hoc
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-05-27 17:35 +07:00
---

# Bản đồ thực hành: practice map

## Luồng thực hành

| Ngày | Buổi | Thực hành | Đầu ra |
| --- | --- | --- | --- |
| Ngày 1 | Buổi 1 | Chọn bài toán triển khai | Phiếu mô tả trường hợp sử dụng: use case one pager |
| Ngày 1 | Buổi 2 | Thiết kế quy trình làm việc AI: AI Workflow cho Smart Ticket Triage | Workflow chạy được, có xử lý lỗi, logging, nhánh Unknown và điểm Human-in-the-loop |
| Ngày 2 | Buổi 3 | Thiết kế tác nhân AI: AI Agent cho Contract Term Extractor | Đặc tả agent, prompt, JSON schema, self-check rule và test cases |
| Ngày 2 | Buổi 4 | Đóng gói Kỹ năng Hỏi đáp Chính sách Nhân sự: Agentic RAG Skill | Skill package hoàn chỉnh (SKILL.md + skill.json + schemas + kb + scripts), evaluation report 12 câu hỏi |
| Ngày 3 | Buổi 5 | Tạo công cụ nhỏ: mini tool Local AI Data Anonymizer | Công cụ redact dữ liệu nhạy cảm chạy local |
| Ngày 3 | Buổi 6 | Kiểm thử, tuân thủ và capstone | Bộ đóng gói triển khai: Implementation Kit |

## Tài liệu tham khảo cho team

- `../02-study-guides/vtn-ai-builders-12-priority-use-cases-v0.2.pdf`: Danh mục 12 bài toán ưu tiên, ma trận chọn case, gợi ý dữ liệu mô phỏng và playbook điều phối.

## Nguyên tắc thực hành

Không dùng dữ liệu thật.

Luôn có điểm con người kiểm duyệt.

Tính toán quan trọng phải dùng code hoặc bảng tính, không giao hoàn toàn cho LLM.

Mọi đầu ra phải có tiêu chí nghiệm thu rõ ràng.

Mọi workflow có rủi ro phải có nhánh dừng an toàn.
