---
mo-ta: thang cham diem rubbric lua chon bai toan phan tich thong so may tinh
trang-thai: active
phien-ban: v0.1
created-at: 2026-06-22 11:16 +07:00
updated-at: 2026-06-22 11:16 +07:00
---

# Thang chấm điểm (rubbric) lựa chọn bài toán

## Cách dùng

Chấm từng bài toán ứng viên theo thang 100 điểm. Ưu tiên bài toán đạt từ 70 điểm trở lên, không dùng dữ liệu thật và có điểm con người duyệt rõ ràng.

## Bảng điểm

| Tiêu chí | Điểm tối đa | Câu hỏi kiểm tra | Điểm nhóm tự chấm |
| --- | ---: | --- | ---: |
| Giá trị nghiệp vụ | 20 | Bài toán có giảm thời gian, giảm lỗi hoặc tăng chất lượng đầu ra không? | 18 |
| Tính khả thi trong lớp | 15 | Có thể tạo bản thử nghiệm tối thiểu (MVP) trong 6 buổi không? | 14 |
| Dữ liệu mô phỏng | 15 | Có thể tạo dữ liệu mô phỏng đủ đại diện mà không dùng dữ liệu thật không? | 15 |
| Mức độ đo lường | 10 | Có chỉ số đo hiệu quả tối thiểu không? | 9 |
| Khả năng phát triển | 10 | Bài toán có thể mở rộng sau lớp mà không đổi toàn bộ thiết kế không? | 8 |
| Kiểm soát rủi ro | 20 | Có điểm con người duyệt, logging, trace và guardrail không? | 19 |
| Năng lực AI phù hợp | 10 | AI có phù hợp với tác vụ đọc, tóm tắt, phân loại, trích xuất hoặc tạo nháp không? | 9 |
| **Tổng** | **100** | | **92** |

## Quy tắc loại nhanh

Loại hoặc thu hẹp bài toán nếu có một trong các điều kiện sau:
- [x] Cần dữ liệu thật của VTN (Không, dùng dữ liệu mô phỏng).
- [x] Cần token thật, API key thật hoặc certificate thật (Không cần).
- [x] Cần quyền ghi hoặc thực thi trên hệ thống thật (Không, chỉ đọc dữ liệu logs/CSVs mô phỏng và tạo đề xuất văn bản).
- [x] Không có người duyệt trước khi sử dụng đầu ra (Đã có 2 bước duyệt rõ ràng).
- [x] Không mô tả được đầu vào hoặc đầu ra (Đầu vào/Đầu ra đã được định nghĩa chi tiết).
- [x] Không thể đo hiệu quả tối thiểu (Đo lường bằng tỷ lệ phát hiện sớm và thời gian tiết kiệm).

## Kết luận nhóm

- **Bài toán được chọn**: Hệ thống tự động giám sát thông số máy tính, cảnh báo hỏng hóc và đề xuất thay thế phần cứng (AI Hardware Health Monitor)
- **Tổng điểm**: 92 / 100
- **Lý do chọn**: Bài toán có tính thực tiễn cao, dữ liệu đầu vào (logs thông số phần cứng) dễ mô phỏng hoàn toàn mà không chạm đến dữ liệu thật của VTN. Đồng thời, nghiệp vụ có quy trình kiểm duyệt (HITL) rõ ràng thông qua đội ngũ IT Admin trước khi chuyển tiếp đề xuất, giảm thiểu tối đa các rủi ro hoạt động hoặc an toàn thông tin.
- **Danh sách quy trình ưu tiên của nhóm**:
  1. Thu thập và đọc tệp log thông số máy tính mô phỏng dạng CSV.
  2. Dùng AI phân tích lỗi phần cứng (ổ cứng, nhiệt độ CPU) và gắn nhãn cảnh báo (Warning/Critical).
  3. Tạo văn bản đề xuất mua sắm linh kiện thay thế dựa trên bảng giá linh kiện tham chiếu.
  4. Giao diện IT Admin phê duyệt đề xuất.
- **Điều kiện cần chuẩn bị trước buổi 2 để dựng AI workflow/Case 10**:
  - Chuẩn bị file dữ liệu CSV mô phỏng chứa thông số sức khỏe ổ cứng và nhiệt độ CPU của 10 thiết bị.
  - Chuẩn bị danh mục thiết bị và giá linh kiện thay thế chuẩn (file tham chiếu).
  - Tìm hiểu cơ chế routing logic trên n8n để phân loại cảnh báo phần cứng.
