---
mo-ta: Hướng dẫn sử dụng trợ lý Antigravity để chạy kiểm thử kỹ năng HR Policy QA vừa hoàn thiện
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-09 13:15 +07:00
updated-at: 2026-06-09 13:15 +07:00
---

# Hướng dẫn sử dụng Antigravity kiểm thử Skill

Sau khi hoàn thành việc đóng gói Kỹ năng Hỏi đáp Chính sách Nhân sự (HR Policy Q&A Skill) tại thư mục `outputs/skills/hr-policy-qa-skill/`, bạn có thể kiểm thử kỹ năng này bằng cách yêu cầu trợ lý ảo Antigravity đóng vai trò thực thi hoặc sử dụng trực tiếp các công cụ đã được phát triển.

### Prompt mẫu để yêu cầu Antigravity thực thi Skill

Bạn hãy sao chép câu lệnh dưới đây và gửi trực tiếp vào khung chat với Antigravity:

```markdown
Antigravity ơi, mình vừa hoàn thành việc phát triển "Kỹ năng Hỏi đáp Chính sách Nhân sự" tại thư mục `outputs/skills/hr-policy-qa-skill/`.

Hãy đọc tài liệu hướng dẫn kỹ năng `outputs/skills/hr-policy-qa-skill/SKILL.md` và file cấu hình `outputs/skills/hr-policy-qa-skill/skill.json` để hiểu vai trò, quy trình thực thi và ranh giới xử lý của kỹ năng này.

Sau đó, hãy đóng vai trò là Agent thực thi kỹ năng này để trả lời câu hỏi sau đây từ nhân viên:
"Tôi là nhân viên chính thức có thâm niên làm việc là 6 năm. Tôi muốn biết mình được nghỉ phép năm tối đa bao nhiêu ngày?"

Yêu cầu:
1. Thực hiện đầy đủ quy trình 4 bước: Intake (Phân loại) -> Retrieval (Truy xuất từ kho tri thức kb/) -> Synthesis (Tổng hợp kèm đối chiếu trích dẫn nguyên văn) -> Evaluation (Tự đánh giá độ tự tin).
2. Kết quả trả ra phải tuân thủ chính xác định dạng JSON schema tại `outputs/skills/hr-policy-qa-skill/schemas/hr-response.schema.json`.
```

### Cách Antigravity sẽ xử lý yêu cầu của bạn:

1. **Đọc cấu hình và hướng dẫn:** Antigravity sẽ mở và phân tích `SKILL.md` và `skill.json` trong thư mục skill bạn vừa tạo.
2. **Kích hoạt quy trình RAG:**
   - **Intake:** Phân loại câu hỏi là `in-scope` và nhận diện các thực thể (thâm niên 6 năm).
   - **Retrieval:** Truy xuất thông tin từ kho tri thức `outputs/skills/hr-policy-qa-skill/kb/hr-policies/` bằng cách đọc các tệp markdown chính sách nghỉ phép và chính sách thâm niên.
   - **Synthesis:** Tổng hợp câu trả lời, tính toán số ngày phép (14 ngày cơ bản + 2 ngày cộng thêm theo thâm niên = 16 ngày) và đối chiếu trích dẫn nguyên văn (verbatim).
   - **Evaluation:** Đưa ra đánh giá độ tin cậy và tự kiểm tra kết quả.
3. **Phản hồi:** Xuất ra kết quả dạng JSON khớp chính xác với schema yêu cầu.
