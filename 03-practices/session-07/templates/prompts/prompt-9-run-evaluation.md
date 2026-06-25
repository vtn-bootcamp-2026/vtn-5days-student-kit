---
mo-ta: Prompt hướng dẫn chạy evaluator.py trên test set, sinh báo cáo đánh giá và phân tích lỗi
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 9: Chạy đánh giá và phân tích lỗi

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn chạy đánh giá định lượng trên toàn bộ bộ câu hỏi kiểm thử để đo lường hiệu năng của Kỹ năng Hỏi đáp Chính sách Nhân sự.

Hãy giúp tôi thực hiện các bước sau:
1. Chạy kịch bản đánh giá `evaluator.py` bằng cách truyền bộ câu hỏi kiểm thử từ `synthetic-data/test-questions.csv`, file chunks từ `outputs/skills/hr-policy-qa-skill/kb/chunks.json`, và file câu trả lời mẫu của tác nhân (nếu đã có) hoặc chạy pipeline tự động để sinh câu trả lời:
   ```bash
   python outputs/skills/hr-policy-qa-skill/scripts/evaluator.py --questions synthetic-data/test-questions.csv --chunks outputs/skills/hr-policy-qa-skill/kb/chunks.json --output outputs/skills/hr-policy-qa-skill/evaluation-report.md
   ```
2. Phân tích tệp báo cáo đánh giá sinh ra tại `outputs/skills/hr-policy-qa-skill/evaluation-report.md` và cho tôi biết:
   - Các chỉ số chất lượng dịch vụ: SLI thực tế đạt được là bao nhiêu so với mục tiêu chất lượng: SLO đã thiết lập? Chỉ số nào bị trượt (FAIL)?
   - Có bao nhiêu câu hỏi in-scope trả lời chính xác? Tỷ lệ từ chối câu hỏi ngoài phạm vi (out-of-scope refusal) có đạt 100% không?
   - Tỷ lệ trích dẫn bị ảo giác (hallucinated citations) có bằng 0% không? Có phát hiện trích dẫn nào bị diễn giải lại (paraphrased) thay vì giữ nguyên văn không?
3. Đối với các câu hỏi bị đánh giá là trượt (FAIL), hãy thực hiện phân tích nguyên nhân lỗi (phân tích nguyên nhân lỗi: root cause analysis) và đề xuất các giải pháp cụ thể để cải thiện.
```
