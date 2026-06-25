---
mo-ta: Prompt yêu cầu Antigravity hoàn thiện script đánh giá evaluator.py với kiểm tra trích dẫn nguyên văn và fix logic chấm điểm
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 8: Hoàn thiện công cụ đánh giá tự động (Evaluator)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn hoàn thành Lab D bằng cách triển khai công cụ đánh giá tự động (đánh giá tự động: auto-evaluation) cho hệ thống RAG của chúng tôi. Hãy giúp tôi sao chép và hoàn thiện kịch bản đánh giá `evaluator.py` tại thư mục:
`outputs/skills/hr-policy-qa-skill/scripts/evaluator.py`

Hãy thực hiện các công việc sau:
1. Sao chép tệp mẫu `templates/skills/hr-policy-qa-skill/scripts/evaluator.py` sang thư mục đích `outputs/skills/hr-policy-qa-skill/scripts/evaluator.py` (nếu chưa có).
2. Kiểm tra và hoàn thiện hàm đối chiếu trích dẫn nguyên văn `cross_check_citation(quote, source_chunks)`. Hàm này phải đảm bảo:
   - Dọn dẹp khoảng trắng và viết thường hóa chuỗi.
   - Tìm kiếm chuỗi khớp tuyệt đối (exact match) của trích dẫn `quote` trong các phân đoạn nguồn `source_chunks`.
   - Nếu không khớp tuyệt đối, chạy giải thuật so khớp từ (fuzzy word overlap similarity). Nếu tỷ lệ trùng lặp từ >= 70%, coi như hợp lệ (fuzzy match) và trả về tỷ lệ tương đồng. Ngược lại, báo lỗi không tìm thấy trích dẫn.
3. Sửa lỗi logic chấm điểm câu trả lời đúng (sửa lỗi logic: bug fix) trong hàm `evaluate_answer()`. Thay vì so sánh trùng khớp từ khóa cứng nhắc giữa câu trả lời và câu mẫu mong đợi (Expected Behavior - vốn chỉ là phần mô tả yêu cầu trong CSV), hãy sử dụng kết hợp hai tín hiệu sau:
   - Tỷ lệ trùng khớp từ khóa ý nghĩa (signal token coverage) sau khi loại bỏ các từ dừng (stop words) đạt ít nhất 34% (>= 0.34).
   - HOẶC mã tài liệu được trích dẫn (doc_id) trùng khớp với mã tài liệu mong đợi (expected_source).
4. Viết hàm tạo báo cáo đánh giá `generate_report()` để xuất ra định dạng Markdown so sánh trực quan giữa các chỉ số chất lượng dịch vụ (Service Level Indicator - SLI) thu được và các mục tiêu chất lượng dịch vụ (Service Level Objective - SLO) đã cấu hình.

Hãy thực hiện các chỉnh sửa và hiển thị các phần thay đổi để tôi kiểm tra.
```
