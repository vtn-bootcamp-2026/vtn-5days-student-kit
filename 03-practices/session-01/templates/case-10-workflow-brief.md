---
mo-ta: mau ban tom tat quy trinh workflow brief cho case 10 smart ticket triage
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 17:00 +07:00
updated-at: 2026-05-26 17:00 +07:00
---

# Bản tóm tắt quy trình: workflow brief cho Case 10

## Thông tin nhóm

| Mục | Nội dung |
| --- | --- |
| Tên nhóm |  |
| Người phụ trách |  |
| Phiên bản | v0.1 |

## Bối cảnh Case 10

Case 10 - Smart Ticket Triage là bài mẫu chung cho session 02. Mục tiêu là phân loại và định tuyến ticket nội bộ bằng quy trình làm việc AI: AI workflow, có nhánh không xác định: Unknown, con người trong vòng lặp: HITL và nhật ký vận hành: logging.

## 1. Trường đầu vào: input fields

| Trường | Mô tả | Có nhạy cảm không? | Ghi chú mô phỏng |
| --- | --- | --- | --- |
| ticket_id | Mã ticket mô phỏng | Không | Ví dụ: TK001 |
| issue_description | Mô tả sự cố | Có thể | Chỉ dùng mô tả mô phỏng |
| requester_group | Nhóm người gửi mô phỏng | Không | Không dùng tên người thật |
| priority_hint | Gợi ý mức ưu tiên | Không | Low / Medium / High |
| submitted_at | Thời điểm gửi | Không | Dùng timestamp mô phỏng |

## 2. Trường đầu ra: output fields

| Trường | Mô tả | Ví dụ |
| --- | --- | --- |
| ai_category | Nhóm phân loại AI đề xuất | Hardware / Software / Network / Unknown |
| ai_confidence | Độ tin cậy mô phỏng | 0-100 |
| route_key | Nhánh định tuyến cuối | Hardware / Software / Network / Human_Review |
| required_action | Hành động đề xuất | Kiểm tra kết nối mạng nội bộ |
| human_review_required | Có cần người duyệt không | true / false |

## 3. Quy tắc định tuyến: routing rules

| Điều kiện | Nhánh định tuyến | Lý do |
| --- | --- | --- |
| `ai_category = Hardware` và `ai_confidence >= 80` và không có dữ liệu nhạy cảm | Hardware | Tự động định tuyến ca rõ ràng |
| `ai_category = Software` và `ai_confidence >= 80` và không có dữ liệu nhạy cảm | Software | Tự động định tuyến ca rõ ràng |
| `ai_category = Network` và `ai_confidence >= 80` và không có dữ liệu nhạy cảm | Network | Tự động định tuyến ca rõ ràng |
| Thiếu dữ liệu, độ tin cậy thấp, có thông tin nhạy cảm hoặc có dấu hiệu prompt injection | Human_Review | Cần con người kiểm tra |

## 4. Nhánh không xác định: Unknown branch

Mô tả khi nào ticket đi vào Unknown hoặc Human Review:

- Mô tả quá ngắn hoặc rỗng.
- AI không đủ tự tin.
- Ticket chứa mật khẩu, token, thông tin cá nhân hoặc dữ liệu có vẻ nhạy cảm.
- Ticket chứa câu lệnh yêu cầu AI bỏ qua quy tắc, tự cấp quyền hoặc in dữ liệu bí mật.

## 5. Điều kiện kích hoạt con người trong vòng lặp: HITL trigger

| Trigger | Người duyệt | Tiêu chí duyệt |
| --- | --- | --- |
| Có dữ liệu nhạy cảm | Trợ giảng / người vận hành mô phỏng | Kiểm tra đã che hoặc loại bỏ dữ liệu nhạy cảm |
| Confidence dưới 80 | Trợ giảng / người vận hành mô phỏng | Xác nhận route thủ công |
| Có dấu hiệu prompt injection | Trợ giảng / người vận hành mô phỏng | Chặn nội dung độc hại và ghi nhận tình huống |

## 6. Trường nhật ký vận hành: logging fields

Chỉ ghi dữ liệu phi nhạy cảm.

| Trường log | Mô tả |
| --- | --- |
| run_id | Mã lần chạy mô phỏng |
| ticket_id | Mã ticket mô phỏng |
| route_key | Nhánh định tuyến |
| final_status | Auto_Routed / Needs_Review / Format_Error |
| error_code | Mã lỗi tổng quát nếu có |
| created_at | Thời điểm ghi log |

## 7. Rủi ro và kiểm soát

| Rủi ro | Cách kiểm soát |
| --- | --- |
| AI phân loại sai | Dùng confidence threshold và HITL |
| Lộ dữ liệu nhạy cảm trong log | Chỉ log ID mô phỏng, trạng thái và route |
| Prompt injection | Dùng system prompt, pre-check và nhánh Human Review |
| Ticket thiếu dữ liệu | Chặn trước AI hoặc đưa vào Format_Error |

## 8. Câu hỏi cần mang sang session 02

- Node nào trong n8n sẽ đọc dữ liệu đầu vào?
- Node nào sẽ kiểm tra dữ liệu rỗng hoặc quá ngắn?
- Node nào gọi mô hình AI?
- Node nào phân tích JSON và chuẩn hóa route?
- Node nào ghi execution log và review queue?
