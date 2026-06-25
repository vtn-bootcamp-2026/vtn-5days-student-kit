---
mo-ta: Prompt yêu cầu Antigravity hỗ trợ thiết lập kho tri thức nhân sự (Knowledge Base) và lược đồ phản hồi (response schema) JSON
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 2: Thiết lập kho tri thức và lược đồ phản hồi

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, hãy hỗ trợ tôi thực hiện bước thiết lập kho tri thức (kho tri thức: knowledge base - KB) và lược đồ phản hồi (lược đồ phản hồi: response schema) cho Kỹ năng Hỏi đáp Chính sách Nhân sự.

Hãy thực hiện các công việc sau:
1. Sao chép 4 tệp chính sách nhân sự mô phỏng (leave, allowance, seniority, training) từ thư mục `synthetic-data/hr-policies/` sang thư mục `outputs/skills/hr-policy-qa-skill/kb/hr-policies/`.
2. Kiểm tra xem các tệp chính sách này có chứa phần đầu khai báo siêu dữ liệu: frontmatter metadata đầy đủ chưa (gồm các trường như doc_id, version, status).
3. Tạo tệp kiểm kê tri thức `outputs/skills/hr-policy-qa-skill/kb/kb-inventory.md` liệt kê danh sách 4 tài liệu trên, mã tài liệu tương ứng (POL-LEAVE-001, POL-ALLOW-001, POL-SENIOR-001, POL-TRAIN-001) và tóm tắt ngắn gọn phạm vi bao phủ của từng tài liệu.
4. Viết tệp lược đồ JSON tại `outputs/skills/hr-policy-qa-skill/schemas/hr-response.schema.json` tuân thủ tiêu chuẩn Draft-07 để cấu trúc hóa câu trả lời của tác nhân: Agent. Lược đồ cần bắt buộc chứa đúng 10 trường sau:
   - `question` (câu hỏi gốc)
   - `classification` (phân loại ý định: in-scope, out-of-scope, ambiguous, prompt-injection)
   - `answer` (câu trả lời)
   - `citations` (danh sách trích dẫn, mỗi trích dẫn chứa doc_id, section, quote, relevance_score)
   - `confidence` (độ tin cậy từ 0.0 đến 1.0)
   - `is_out_of_scope` (boolean chỉ định câu hỏi ngoài phạm vi)
   - `refusal_message` (thông báo từ chối khi out-of-scope)
   - `self_check_result` (kết quả tự kiểm duyệt gồm passed, issues_found, corrected)
   - `retrieval_method` (phương pháp truy xuất: vector, keyword, hybrid)
   - `top_chunks_used` (số đoạn văn đã dùng)

Hãy hiển thị cấu trúc thư mục sau khi hoàn thành và mã nguồn lược đồ JSON để tôi kiểm tra.
```
