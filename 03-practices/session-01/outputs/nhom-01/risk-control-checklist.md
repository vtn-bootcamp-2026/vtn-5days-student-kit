---
mo-ta: bang kiem rui ro va kiem soat so bo cho bai toan phan tich thong so may tinh
trang-thai: active
phien-ban: v0.1
created-at: 2026-06-22 11:16 +07:00
updated-at: 2026-06-22 11:16 +07:00
---

# Bảng kiểm rủi ro và kiểm soát

## Dữ liệu

- [x] Không dùng dữ liệu thật của VTN
- [x] Không dùng thông tin khách hàng thật
- [x] Không dùng IP thật, mã trạm thật hoặc cấu hình thật
- [x] Có dữ liệu mô phỏng thay thế
- [x] Có mô tả nguồn dữ liệu mô phỏng

## Phân quyền và điểm kết nối

- [x] Không dùng token thật
- [x] Không dùng API key thật
- [x] Không hard-code thông tin bí mật
- [x] Không đưa API key hoặc token vào prompt, ảnh chụp màn hình, log, n8n export hoặc bài nộp
- [x] Nếu mô tả điểm kết nối (endpoint), chỉ dùng endpoint giả lập
- [x] Quyền truy cập trong bài thực hành là quyền đọc hoặc quyền mô phỏng

## Con người trong vòng lặp

- [x] Có bước con người trong vòng lặp (human in the loop)
- [x] Có người chịu trách nhiệm duyệt đầu ra
- [x] Có tiêu chí duyệt hoặc từ chối
- [x] Không để AI tự quyết định việc có rủi ro kỹ thuật, pháp lý, nhân sự hoặc vận hành

## Nhật ký và truy vết

- [x] Có lưu đầu vào mẫu
- [x] Có lưu đầu ra mẫu
- [x] Có ghi phiên bản prompt hoặc hướng dẫn
- [x] Có ghi trạng thái thành công hoặc lỗi
- [x] Có cách truy lại lý do AI đưa ra kết quả
- [x] Nhật ký vận hành chỉ chứa dữ liệu phi nhạy cảm

## Lan can an toàn

- [x] Có quy tắc từ chối nếu câu hỏi vượt phạm vi
- [x] Có quy tắc không suy đoán khi thiếu dữ liệu
- [x] Có quy tắc yêu cầu trích dẫn hoặc nêu căn cứ khi dùng tài liệu
- [x] Có quy tắc chuyển sang con người khi rủi ro cao

## Kết luận

| Mục | Kết luận |
| --- | --- |
| Bài toán đủ an toàn để làm trong lớp? | Có |
| Điều kiện cần sửa trước khi chốt | Hoàn thiện 2 file dữ liệu mô phỏng: danh mục linh kiện chuẩn và log thông số máy tính ảo. |
| Người xác nhận | Học viên Nhóm 01 |

## Ghi chú

Bảng này là rà rủi ro sơ bộ ở session 01, không thay thế bảng kiểm tuân thủ trước khi thí điểm trong session 06.
