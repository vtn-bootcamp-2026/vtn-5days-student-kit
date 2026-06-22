---
mo-ta: phieu mo ta case tu dong thu thap va canh bao thong so may tinh
trang-thai: active
phien-ban: v0.1
created-at: 2026-06-22 11:15 +07:00
updated-at: 2026-06-22 11:15 +07:00
---

# Phiếu mô tả trường hợp sử dụng 01 trang

## Thông tin chung

| Mục | Nội dung |
| --- | --- |
| Tên nhóm | Nhóm 01 |
| Tên bài toán | Hệ thống tự động giám sát thông số máy tính, cảnh báo hỏng hóc và đề xuất thay thế phần cứng (AI Hardware Health Monitor) |
| Người dùng chính | Bộ phận Quản trị Thiết bị / IT Admin của đơn vị |
| Người chịu trách nhiệm trình bày | Học viên Nhóm 01 |
| Phiên bản | v0.1 |

## Mô tả bài toán

Hiện nay, việc kiểm tra sức khỏe máy tính của nhân viên trong đơn vị đang được thực hiện thủ công hoặc chỉ khi máy tính gặp sự cố nghiêm trọng nhân viên mới báo cáo cho bộ phận IT. Việc này dẫn đến rủi ro mất dữ liệu quan trọng, gián đoạn công việc của nhân viên và tốn thời gian của đội ngũ IT Admin khi phải kiểm tra, chuẩn đoán thủ công từng máy. 
Hệ thống AI đề xuất sẽ tự động phân tích các thông số kỹ thuật (như nhiệt độ CPU, trạng thái SMART của ổ cứng, dung lượng RAM khả dụng, wear level của SSD) thu thập định kỳ từ các máy tính, tự động phân tích và đưa ra cảnh báo sớm về các phần cứng có nguy cơ hỏng hóc cao. Đồng thời, AI hỗ trợ soạn thảo dự thảo tệp đề xuất mua sắm/thay thế linh kiện tương ứng để con người phê duyệt nhanh chóng.

## Đầu vào

| Loại đầu vào | Mô tả | Nguồn dữ liệu mô phỏng |
| --- | --- | --- |
| Tài liệu | Danh mục linh kiện chuẩn và đơn giá tham chiếu | [reference-hardware-catalog.csv](file:///Users/shimazu/Desktop/vtn-5days-student-kit/03-practices/session-01/outputs/nhom-01/reference-hardware-catalog.csv) |
| Bảng dữ liệu | Bảng kê khai danh sách máy tính nội bộ (Mã máy, CPU, RAM, Disk) | Dữ liệu mô phỏng danh sách tài sản IT |
| Log/ticket/email | Nhật ký thông số phần cứng định kỳ (SMART log, CPU Temperature, RAM Spikes, Write cycles) | [mock-pc-hardware-logs.csv](file:///Users/shimazu/Desktop/vtn-5days-student-kit/03-practices/session-01/outputs/nhom-01/mock-pc-hardware-logs.csv) |

## Đầu ra mong muốn

| Đầu ra | Định dạng | Người sử dụng |
| --- | --- | --- |
| Danh sách cảnh báo sự cố phần cứng sớm | Giao diện bảng (Mã máy, Linh kiện lỗi, Mức độ nghiêm trọng, Khuyến nghị) | IT Admin |
| Tệp đề xuất mua sắm, thay thế linh kiện | File văn bản/Markdown (Danh sách cần mua, Lý do chi tiết, Dự toán chi phí) | Trưởng bộ phận IT duyệt và gửi Ban Giám đốc |

## Giá trị kỳ vọng

- Thời gian tiết kiệm dự kiến: Giảm 85% thời gian tổng hợp dữ liệu thủ công và soạn thảo văn bản đề xuất mua sắm thiết bị.
- Lỗi hoặc thiếu sót muốn giảm: Giảm 90% các sự cố sập máy đột ngột gây mất mát dữ liệu do không được cảnh báo hỏng ổ cứng hoặc pin phồng sớm.
- Chỉ số đo hiệu quả: Tỷ lệ phát hiện sớm lỗi phần cứng trước khi hỏng hoàn toàn (Proactive Failure Detection Rate) > 90%; Thời gian từ khi phát hiện lỗi đến khi tạo đề xuất thay thế < 15 phút.

## Phạm vi bản thử nghiệm tối thiểu (MVP)

- Chỉ xử lý: Phân tích thông số SMART ổ cứng (SSD/HDD Wear Level, Read/Write Error Rate) và Nhiệt độ CPU để cảnh báo lỗi ổ cứng và lỗi tản nhiệt. Tạo file đề xuất thay thế ổ cứng hoặc keo tản nhiệt/quạt CPU dựa trên mẫu giá có sẵn.
- Chưa xử lý: Chưa tự động đặt hàng trên hệ thống mua sắm, chưa gửi mail trực tiếp cho Ban Giám đốc khi chưa có người duyệt, chưa tự động can thiệp kỹ thuật từ xa (như format hay tối ưu hệ thống).
- Điều kiện để xem là hoàn thành: Hệ thống đọc file CSV chứa log thông số phần cứng mô phỏng của 10 máy tính, lọc ra đúng các máy có thông số vượt ngưỡng an toàn, hiển thị cảnh báo trên dashboard và xuất ra file đề xuất thay thế bằng tiếng Việt chính xác.

## Kiểm soát rủi ro

| Rủi ro | Cách kiểm soát |
| --- | --- |
| Dữ liệu thật hoặc nhạy cảm | Chỉ dùng dữ liệu mô phỏng, thay thế tên nhân viên và mã nhân sự thật bằng mã định danh máy ảo (PC-001, PC-002...). |
| AI trả lời sai | IT Admin kiểm tra chéo các thông số kỹ thuật thực tế của máy tính trước khi bấm duyệt đề xuất. |
| Đầu ra vượt phạm vi | Đưa hệ thống luật cứng (Rule-based Guardrail) vào prompt (Ví dụ: SSD Wear Level > 90% hoặc SMART error > 0 thì bắt buộc phân loại Warning/Critical). |
| Thiếu truy vết | Lưu trữ toàn bộ log thô của máy tính, phiên bản prompt của AI và lịch sử duyệt của IT Admin vào cơ sở dữ liệu. |

## Điểm con người duyệt

IT Admin thực hiện vai trò con người trong vòng lặp (Human-in-the-loop) qua hai bước kiểm duyệt chính:
- **Bước 1 (IT Admin duyệt cảnh báo)**: IT Admin rà soát danh sách cảnh báo phần cứng do AI đề xuất. Xác nhận thực tế xem máy tính đó có đang hoạt động bình thường hay có hiện tượng giật lag, đơ hay không theo phản hồi của người dùng. Duyệt chuyển sang bước tạo đề xuất.
- **Bước 2 (Trưởng bộ phận IT duyệt đề xuất)**: Trưởng bộ phận IT kiểm tra nội dung file đề xuất mua sắm linh kiện (số lượng, loại linh kiện, tổng chi phí dự toán) để ký duyệt trước khi chuyển lên cấp trên hoặc phòng mua sắm.

## Dữ liệu mô phỏng và bàn giao sang buổi 2

Liệt kê dữ liệu mô phỏng và quy tắc chuẩn bị để dựng quy trình làm việc AI ở buổi 2:

- **Dữ liệu mô phỏng cần chuẩn bị**: File [mock-pc-hardware-logs.csv](file:///Users/shimazu/Desktop/vtn-5days-student-kit/03-practices/session-01/outputs/nhom-01/mock-pc-hardware-logs.csv) chứa thông số của 10 máy tính ảo (bao gồm các chỉ số CPU Temp, Disk SMART Errors, SSD Wear Level, RAM usage, Battery Wear).
- **Quy tắc định tuyến hoặc phân loại**: Định tuyến các cảnh báo: `Critical` (Lỗi ổ cứng nặng, SSD Wear Level > 95% -> cần thay ngay) chuyển trực tiếp đến IT Admin trực ca; `Warning` (Nhiệt độ CPU liên tục > 85 độ -> cần vệ sinh/tra keo) xếp vào danh sách bảo trì tuần.
- **Điểm con người duyệt**: Trưởng bộ phận IT phê duyệt file đề xuất thay thế thiết bị cuối cùng.
- **Trường nhật ký vận hành cần ghi**: `log_id`, `machine_id`, `hardware_status`, `alert_level` (Normal/Warning/Critical), `action_taken`, `hitl_approval_status` (Approved/Rejected), `timestamp`.
