---
mo-ta: Prompt yêu cầu Antigravity đóng vai làm HR-Policy Agent để chạy kiểm thử luồng hỏi đáp đầy đủ và xuất kết quả chuẩn JSON
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:44 +07:00
---

# Prompt 8: Chạy kiểm thử tác nhân hỏi đáp (HR-Policy Agent QA)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, chúng ta vừa hoàn thành việc tích hợp và cấu hình gói kỹ năng hỏi đáp chính sách tại thư mục `03-practice/session-07/outputs/skills/hr-policy-qa-skill/`.

Bây giờ, hãy đóng vai trò là tác nhân hỏi đáp chính sách nhân sự: HR-Policy Agent thực thi kỹ năng này để trả lời câu hỏi sau của nhân viên:
"Tôi là nhân viên chính thức có thâm niên làm việc là 6 năm. Tôi muốn biết mình được nghỉ phép năm tối đa bao nhiêu ngày?"

Yêu cầu thực hiện nghiêm ngặt quy trình 5 bước sau:
1. **Bước 1: Tiếp nhận và phân loại ý định (intake & classification):** Phân loại câu hỏi của người dùng và xác định xem có phải là in-scope không.
2. **Bước 2: Định tuyến nguồn (source routing):** Quyết định xem câu hỏi này nên chạy cục bộ (local) hay gọi NotebookLM. Giải thích lý do lựa chọn.
3. **Bước 3: Truy xuất (retrieval):** Đọc các tệp chính sách liên quan trong thư mục `03-practice/session-07/outputs/skills/hr-policy-qa-skill/kb/hr-policies/` (Chính sách nghỉ phép POL-LEAVE-001 và Chính sách thâm niên POL-SENIOR-001).
4. **Bước 4: Tổng hợp và tự kiểm duyệt (synthesis & self-check):** Tổng hợp câu trả lời (14 ngày cơ bản + 2 ngày thâm niên = 16 ngày). Tự đối chiếu trích dẫn (citation) với văn bản gốc để đảm bảo trích nguyên văn (verbatim), không bịa đặt (hallucination).
5. **Bước 5: Xuất kết quả:** Trả về kết quả đầu ra khớp chính xác với định dạng JSON schema tại `03-practice/session-07/outputs/skills/hr-policy-qa-skill/schemas/hr-response.schema.json`.

Hãy hiển thị kết quả JSON cuối cùng trong khối mã để tôi kiểm tra.
```
