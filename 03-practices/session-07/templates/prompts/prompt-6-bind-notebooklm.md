---
mo-ta: Prompt yêu cầu Antigravity tích hợp NotebookLM vào cấu hình của Agent (Source Routing + Call Skill)
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 6: Tích hợp NotebookLM vào gói cấu hình của tác nhân (Agent)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn thực hiện Lab C để tích hợp NotebookLM vào tác nhân nhân sự: HR-Policy Agent. Hãy giúp tôi chỉnh sửa tệp hướng dẫn kỹ năng `SKILL.md` và tệp cấu hình `skill.json` trong gói kỹ năng của nhóm tại:
`outputs/skills/hr-policy-qa-skill/`

Hãy thực hiện các yêu cầu sau:
1. Trong tệp `SKILL.md`, hãy chèn thêm bước **Định tuyến nguồn (định tuyến nguồn: source routing)** vào sau bước phân loại ý định (Intake) và trước bước truy xuất thông tin (Retrieval):
   - Nếu câu hỏi thuộc phạm vi 4 tệp chính sách cốt lõi (dữ liệu nhỏ) hoặc cần độ chính xác từ khóa tuyệt đối -> Sử dụng bộ truy xuất lai `retriever.py` cục bộ (local hybrid retriever).
   - Nếu câu hỏi phức tạp, quy mô lớn liên quan đến toàn bộ sổ tay nhân sự, các phụ lục chi tiết và tài liệu mở rộng -> Gọi kỹ năng tích hợp NotebookLM: `vibe-notebooklm-orchestrator` để truy xuất từ cloud notebook "HR-Policy Knowledge Base — Viettel Network".
   - Nếu câu hỏi mơ hồ, thực hiện chạy cục bộ trước, nếu bị từ chối (refused) thì chuyển sang NotebookLM làm phương án dự phòng.
2. Trong tệp `skill.json`, hãy cập nhật trường quyền hạn `permissions` để cho phép tác nhân gọi kỹ năng ngoài:
   ```json
   "permissions": {
     "read_files": [
       "kb/hr-policies/*.md",
       "kb/kb-inventory.md",
       "kb/chunks.json"
     ],
     "write_files": [],
     "execute_scripts": [
       "scripts/chunker.py",
       "scripts/retriever.py",
       "scripts/evaluator.py"
     ],
     "call_skills": [
       "vibe-notebooklm-orchestrator"
     ],
     "network_access": true
   }
   ```
3. Đảm bảo mọi trích dẫn (citation) trả về từ NotebookLM ở bước tổng hợp đều phải đi qua khâu tự kiểm duyệt (self-check) để đối chiếu nguyên văn (verbatim) với tài liệu gốc trong kho tri thức cục bộ. Nếu không khớp nguyên văn, phải loại bỏ trích dẫn hoặc hạ điểm tin cậy.

Hãy thực hiện chỉnh sửa các tệp và hiển thị các khối mã thay đổi (diff blocks) cho tôi xem.
```
