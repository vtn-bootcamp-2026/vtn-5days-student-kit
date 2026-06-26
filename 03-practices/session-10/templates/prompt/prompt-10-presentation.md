---
mo-ta: "Prompt 10 — Tổng hợp toàn bộ hồ sơ thành slide thuyết trình Capstone hoàn chỉnh"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 10: Tự động hóa soạn dàn ý Slide thuyết trình báo cáo (Presentation Outline)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat để hoàn thiện tài liệu slide trình bày:

```text
BỐI CẢNH:
Tôi cần chuẩn bị dàn ý và nội dung slide thuyết trình báo cáo bảo vệ dự án Capstone "10-presentation-outline.md". Dàn ý này cần tóm tắt cực kỳ súc tích và ấn tượng toàn bộ kết quả của nhóm từ các tài liệu trước đó (đề xuất dự án, luồng xử lý Mermaid, đặc tả prompt, kiểm thử tuân thủ bảo mật, kế hoạch 30-90 ngày) để trình bày trước hội đồng giám khảo Viettel Networks trong vòng 8 phút thuyết trình.

CHỈ DẪN CHO AI:
Hãy viết một tài liệu Markdown hoàn chỉnh cho tệp "10-presentation-outline.md" dựa trên toàn bộ thông tin của dự án đã xây dựng qua các bước chat trước. Dàn ý Slide cần bám sát cấu trúc chuẩn hóa gồm 6 trang slide dưới đây:

- **Slide 1: Trang tiêu đề & Giới thiệu nhóm**
  - Tiêu đề slide: Tên dự án/ứng dụng AI của nhóm.
  - Danh sách thành viên: Trưởng nhóm, các thành viên và vai trò cụ thể.
  - Đơn vị áp dụng thực tế tại Viettel Networks.
- **Slide 2: Vấn đề nghiệp vụ & Giá trị đo lường được (KPI)**
  - Tóm tắt nỗi đau thực tế (Pain points) của đơn vị.
  - Phân tích rủi ro bảo mật thông tin nội bộ (Nghị định 356/2025/NĐ-CP).
  - KPI hiệu quả đo lường được (Năng suất trước vs sau áp dụng, tính an toàn bảo mật, chi phí).
- **Slide 3: Kiến trúc giải pháp & Luồng xử lý dữ liệu**
  - Sơ đồ luồng logic (sử dụng mã Mermaid `graph TD` đã tối ưu ở Bước 2).
  - Mô tả điểm kiểm duyệt của con người (Human-in-the-loop) để quản lý rủi ro.
- **Slide 4: Thiết kế Prompt & Phòng thủ bảo mật (Prompt Defense)**
  - Tóm tắt đặc tả cấu trúc System Prompt, cấu hình tham số (temperature = 0.0).
  - Kết quả thử nghiệm và phòng vệ chống tấn công lời nhắc (Jailbreak, Data Exfiltration, Role Confusion).
- **Slide 5: Kết quả kiểm thử chức năng & An toàn nhật ký log**
  - Tỷ lệ PASS bộ kiểm thử tự động (Ví dụ: 10/10 ca kiểm thử thành công).
  - Ví dụ thực tế xử lý các Edge Cases lắt léo (Ví dụ: tránh che giấu nhầm mã thiết bị SCADA hoặc số đo kỹ thuật).
  - Đảm bảo an toàn log vận hành (`execution-log.csv` không chứa PII).
- **Slide 6: Lộ trình triển khai 30-90 ngày & Đề xuất mở rộng**
  - Lộ trình hành động 30-90 ngày với các mốc thời gian rõ ràng và phân công người chịu trách nhiệm.
  - Đề xuất 3 trường hợp sử dụng (Use Cases) tiếp theo phù hợp với định hướng nghiệp vụ của đơn vị.

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Hướng dẫn cấu trúc và dàn ý chi tiết slide báo cáo bảo vệ Capstone Project tại Viettel Networks"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không kèm thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh để dán đè vào tệp `10-presentation-outline.md`.
