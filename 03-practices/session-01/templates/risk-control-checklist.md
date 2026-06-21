---
mo-ta: bang kiem rui ro va kiem soat so bo cho bai toan buoi 1
trang-thai: active
phien-ban: v2.1
created-at: 2026-05-17 13:54 +07:00
updated-at: 2026-05-26 17:00 +07:00
---

# Bảng kiểm rủi ro và kiểm soát

## Dữ liệu

- [ ] Không dùng dữ liệu thật của VTN
- [ ] Không dùng thông tin khách hàng thật
- [ ] Không dùng IP thật, mã trạm thật hoặc cấu hình thật
- [ ] Có dữ liệu mô phỏng thay thế
- [ ] Có mô tả nguồn dữ liệu mô phỏng

## Phân quyền và điểm kết nối

- [ ] Không dùng token thật
- [ ] Không dùng API key thật
- [ ] Không hard-code thông tin bí mật
- [ ] Không đưa API key hoặc token vào prompt, ảnh chụp màn hình, log, n8n export hoặc bài nộp
- [ ] Nếu mô tả điểm kết nối (endpoint), chỉ dùng endpoint giả lập
- [ ] Quyền truy cập trong bài thực hành là quyền đọc hoặc quyền mô phỏng

## Con người trong vòng lặp

- [ ] Có bước con người trong vòng lặp (human in the loop)
- [ ] Có người chịu trách nhiệm duyệt đầu ra
- [ ] Có tiêu chí duyệt hoặc từ chối
- [ ] Không để AI tự quyết định việc có rủi ro kỹ thuật, pháp lý, nhân sự hoặc vận hành

## Nhật ký và truy vết

- [ ] Có lưu đầu vào mẫu
- [ ] Có lưu đầu ra mẫu
- [ ] Có ghi phiên bản prompt hoặc hướng dẫn
- [ ] Có ghi trạng thái thành công hoặc lỗi
- [ ] Có cách truy lại lý do AI đưa ra kết quả
- [ ] Nhật ký vận hành chỉ chứa dữ liệu phi nhạy cảm

## Lan can an toàn

- [ ] Có quy tắc từ chối nếu câu hỏi vượt phạm vi
- [ ] Có quy tắc không suy đoán khi thiếu dữ liệu
- [ ] Có quy tắc yêu cầu trích dẫn hoặc nêu căn cứ khi dùng tài liệu
- [ ] Có quy tắc chuyển sang con người khi rủi ro cao

## Kết luận

| Mục | Kết luận |
| --- | --- |
| Bài toán đủ an toàn để làm trong lớp? | Có / Không |
| Điều kiện cần sửa trước khi chốt |  |
| Người xác nhận |  |

## Ghi chú

Bảng này là rà rủi ro sơ bộ ở session 01, không thay thế bảng kiểm tuân thủ trước khi thí điểm trong session 06.
