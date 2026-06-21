---
mo-ta: tong quan bai thuc hanh session 01 chon bai toan an toan va khoi dong case 10
trang-thai: active
phien-ban: v3.1
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-05 00:00 +07:00
---

# Buổi 1: chọn bài toán an toàn và khởi động Case 10

## Mục tiêu

Sau session 01, học viên hiểu bức tranh AI thực chiến ở mức doanh nghiệp, nhận diện được ranh giới an toàn dữ liệu, kiểm tra được môi trường tối thiểu và tạo được bộ đầu ra khởi tạo để sang session 02 dựng quy trình làm việc AI: AI workflow cho Case 10 - Smart Ticket Triage.

Session này có hai luồng song song:

- **Luồng chung bắt buộc:** mọi nhóm phác thảo Case 10 ở mức bản tóm tắt quy trình: workflow brief để dùng ngay trong session 02.
- **Luồng khám phá của nhóm:** mỗi nhóm chọn 1 case phù hợp từ `case-studies.md` hoặc từ đơn vị mình để luyện tư duy chọn bài toán, chấm điểm và kiểm soát rủi ro.

## Cấu trúc bài thực hành

| Phần | Hoạt động | Hình thức | Đầu ra |
| --- | --- | --- | --- |
| A | Demo dẫn nhập Antigravity với log O&M giả lập | Giảng viên thị phạm | Học viên hiểu đích đến, không cần nộp |
| B | Setup môi trường và tạo lời nhắc Markdown: Markdown prompt đầu tiên | Thực hành có hướng dẫn | `first-prompt.md` bản nháp |
| C | Chọn và chấm 2-3 bài toán từ danh mục case | Bài tập nhóm | one-pager, rubbric, risk checklist bản nháp |
| D | Phác thảo Case 10 - Smart Ticket Triage | Bài tập nhóm bắt buộc | `case-10-workflow-brief.md` |
| E | Checkpoint bàn giao sang session 02 | Nộp nhanh cuối buổi | Bộ artifact khởi tạo của nhóm |

## Đầu vào

- `../../../02-study-guides/case-studies.md`: danh mục 12 case chuẩn và định hướng chọn case theo từng buổi.
- `../../../02-study-guides/safety-rules.md`: quy tắc an toàn dữ liệu và vận hành.
- `../../../02-study-guides/vtn-ai-builders-12-priority-use-cases-v0.2.pdf`: tài liệu tham khảo danh mục bài toán ưu tiên.
- `synthetic-data/sample-use-cases.md`: bài toán mẫu để luyện chấm điểm.
- `synthetic-data/sample-noc-alerts.csv`: cảnh báo NOC giả lập cho demo/log thinking.
- `templates/use-case-one-pager.md`: mẫu phiếu mô tả case nhóm chọn.
- `templates/use-case-scoring-rubbric.md`: mẫu thang chấm điểm: rubbric.
- `templates/risk-control-checklist.md`: bảng kiểm rủi ro sơ bộ.
- `templates/first-prompt.md`: mẫu lời nhắc Markdown đầu tiên.
- `templates/case-10-workflow-brief.md`: mẫu bản tóm tắt quy trình cho Case 10.

## Đầu ra

Mỗi nhóm cần hoàn thành ở mức bản nháp khởi tạo:

- `use-case-one-pager.md`: bản nháp v0.1 cho case nhóm chọn.
- `use-case-scoring-rubbric.md`: chấm 2-3 bài toán ứng viên để tạo danh sách quy trình ưu tiên.
- `risk-control-checklist.md`: rà rủi ro sơ bộ cho case nhóm chọn.
- `first-prompt.md`: lời nhắc Markdown đầu tiên, không chứa API key hoặc dữ liệu thật.
- `case-10-workflow-brief.md`: bản tóm tắt quy trình bắt buộc cho Case 10, gồm đầu vào, đầu ra, routing, Unknown, HITL và logging.

Nếu lớp dùng repo để thu bài, mỗi nhóm copy template sang `outputs/[ten-nhom]/`. Nếu giảng viên dùng LMS/Drive, nhóm vẫn giữ đúng tên file ở trên để dễ đối chiếu.

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` dùng để lưu ảnh giảng viên thị phạm đã kiểm duyệt, ví dụ ảnh demo Antigravity, trạng thái setup công cụ hoặc ví dụ workflow brief mẫu.

Ảnh trong thư mục này không phải đầu ra bắt buộc của học viên. Không commit ảnh chụp thô có email, API key, token, đường dẫn cá nhân, tab trình duyệt nhạy cảm hoặc dữ liệu thật.

## Tiêu chí hoàn thành

- Nhóm có danh sách 2-3 bài toán ứng viên và lý do chấm điểm.
- Nhóm chọn được 1 case đủ nhỏ, rõ, lặp lại, đo được và có dữ liệu mô phỏng.
- Nhóm có bảng kiểm rủi ro sơ bộ và điểm con người trong vòng lặp: HITL.
- Nhóm có bằng chứng setup tối thiểu: n8n mở được, Antigravity IDE mở được, Gemini API dùng qua cấu hình an toàn hoặc tài khoản demo của giảng viên.
- Nhóm có `case-10-workflow-brief.md` đủ để session 02 bắt đầu dựng workflow n8n.

## Quan hệ với session 06

Artifact session 01 là bản nháp đầu khóa để luyện tư duy chọn bài toán và khóa phạm vi. Session 06 hiện đóng gói Mini Tool Anonymizer từ session 05 thành bộ hồ sơ triển khai: Implementation Kit, nên không nộp lại nguyên trạng các file session 01 như tài liệu capstone cuối khóa.
