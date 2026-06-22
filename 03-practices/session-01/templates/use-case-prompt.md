---
mo-ta: mau goi y loi nhac tu dong hoa phac thao use case bang AI cho session 01
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-26 12:09 +07:00
updated-at: 2026-06-18 09:15 +07:00
---
# Lời nhắc đồng sáng tạo use case cùng AI

## Cách sử dụng

Học viên copy toàn bộ nội dung lời nhắc: prompt bên dưới, thay thế các thông tin trong dấu ngoặc vuông `[...]` bằng ý tưởng thực tế của nhóm mình.

Nếu chưa có ý tưởng riêng, nhóm có thể lựa chọn và tham chiếu trực tiếp 1 trong các bài toán mẫu an toàn từ:

- [synthetic-data/sample-use-cases.md](../synthetic-data/sample-use-cases.md) (ví dụ: Trợ lý chính sách nhân sự giả lập, Tóm tắt cảnh báo NOC giả lập, Định tuyến ticket hỗ trợ giả lập).
- [02-study-guides/case-studies.md](../../../../02-study-guides/case-studies.md) (các case study của chương trình).

Sau khi điền xong thông tin, gửi toàn bộ nội dung lời nhắc này cho trợ lý AI Antigravity trên IDE để tự động sinh ra bản thảo cho 3 tài liệu: One-Pager, thang chấm điểm: rubbric và Risk Checklist.

## Nội dung lời nhắc mẫu

```text
Bạn là trợ lý AI chuyên nghiệp về thiết kế và đánh giá các trường hợp sử dụng AI: use cases trong doanh nghiệp.

Tôi có một ý tưởng bài toán muốn triển khai AI tại đơn vị dựa trên các nguồn tham chiếu (hoặc ý tưởng tự chọn):

[MÔ TẢ BÀI TOÁN CỦA ANH CHỊ VÀO ĐÂY]

Hãy giúp tôi đồng sáng tạo và tự động phác thảo nội dung chi tiết cho 3 tài liệu sau dưới dạng Markdown (chỉ sử dụng dữ liệu mô phỏng, không suy đoán dữ liệu thật):

1. Nội dung cho "Phiếu mô tả trường hợp sử dụng 01 trang" (One-Pager):
   - Đề xuất người dùng chính (primary user), đầu vào dự kiến (input) và đầu ra mong muốn (output).
   - Xác định giá trị kỳ vọng (thời gian tiết kiệm, chỉ số đo hiệu quả).
   - Xác định phạm vi sản phẩm khả dụng tối thiểu (MVP) - những gì CHƯA xử lý để đảm bảo an toàn.
   - Đề xuất điểm dừng kiểm duyệt của con người trong vòng lặp (Human-in-the-loop - HITL).

2. Bảng chấm điểm sơ bộ theo "thang chấm điểm: rubbric" (Scoring Rubbric):
   - Đánh giá sơ bộ điểm số của bài toán này theo các tiêu chí: tính khả thi của dữ liệu, mức độ lặp lại, khả năng đo lường, rủi ro bảo mật và sự tham gia của con người (HITL).
   - Đưa ra điểm số ước lượng trên thang điểm 100 và nhận xét ngắn gọn.

3. Bản rà soát "Danh sách kiểm tra rủi ro" (Risk Checklist):
   - Phân tích 3-4 rủi ro bảo mật thông tin và tuân thủ dữ liệu nhạy cảm (PII).
   - Đề xuất các rào cản an toàn (guardrails) tương ứng để kiểm soát rủi ro.

Yêu cầu ràng buộc:
- Tuyệt đối không sử dụng hoặc suy đoán bất kỳ dữ liệu thật, tên khách hàng thật, số điện thoại thật hoặc thông tin nhạy cảm của VTN.
- Đảm bảo có cơ chế con người kiểm duyệt (HITL) rõ ràng trước khi sử dụng kết quả của AI.
- Chỉ trả lời bằng tiếng Việt.
```
