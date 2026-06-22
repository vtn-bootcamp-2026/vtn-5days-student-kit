---
mo-ta: "Hướng dẫn cấu trúc và dàn ý chi tiết slide báo cáo bảo vệ Capstone Project tại Viettel Networks"
trang-thai: active
phien-ban: v1.0
created-at: "2026-06-14 23:19 +07:00"
updated-at: "2026-06-14 23:19 +07:00"
---

# Dàn ý Slide báo cáo bảo vệ dự án Capstone

Tài liệu này cung cấp cấu trúc chuẩn hóa cho **Slide báo cáo bảo vệ** (từ 5 đến 7 trang) để các nhóm học viên chuẩn bị trước hội đồng giám khảo Viettel Networks. Hãy thay thế các phần trong dấu ngoặc vuông `[...]` bằng nội dung thực tế của nhóm.

---

## Slide 1: Trang tiêu đề & Giới thiệu nhóm
*   **Tiêu đề slide:** [Tên bài toán/Dự án AI của nhóm - Ví dụ: Tự động hóa che giấu dữ liệu nhạy cảm cục bộ tại NOC]
*   **Danh sách thành viên nhóm:**
    *   Trưởng nhóm: [Điền tên trưởng nhóm] - Vai trò: [Ví dụ: Thiết kế hệ thống, Viết code]
    *   Thành viên 1: [Điền tên] - Vai trò: [Ví dụ: Thiết kế test case, Viết tài liệu]
    *   Thành viên 2: [Điền tên] - Vai trò: [Ví dụ: Đánh giá tuân thủ bảo mật]
*   **Đơn vị:** [Ví dụ: Tổ BSS / Trung tâm NOC - Viettel Networks]

---

## Slide 2: Vấn đề nghiệp vụ & Giá trị đo lường được (KPI)
*Tham chiếu: [01-use-case-one-pager.md](01-use-case-one-pager.md)*

*   **Nỗi đau thực tế (Pain Point):**
    *   [Mô tả quy trình xử lý dữ liệu thủ công mất thời gian thế nào]
    *   [Rủi ro lộ thông tin cá nhân PII khi sử dụng AI Cloud công cộng theo Nghị định 356/2025/NĐ-CP]
*   **Giải pháp đề xuất:** [Tóm tắt giải pháp Mini Tool Anonymizer cục bộ]
*   **KPI hiệu quả kỳ vọng:**
    *   **Năng suất:** Giảm từ [15 phút] xuống còn [dưới 30 giây] mỗi báo cáo.
    *   **Mức độ bảo mật:** Chạy cục bộ offline 100%, bảo vệ tuyệt đối thông tin.

---

## Slide 3: Kiến trúc giải pháp & Luồng xử lý dữ liệu
*Tham chiếu: [02-logical-workflow.md](02-logical-workflow.md)*

*   **Sơ đồ luồng logic (Logical Workflow):**
    *   [Mô tả ngắn gọn luồng đi từ văn bản thô -> qua bộ lọc Regex -> qua phân tích ngữ cảnh của Local LLM]
*   **Điểm kiểm duyệt của con người (Human-in-the-loop - HITL):**
    *   Cờ kiểm duyệt `needs_human_review` được tự động kích hoạt khi nào? [Ví dụ: khi phát hiện prompt injection hoặc khi Regex chuyển sang chế độ dự phòng fallback].
    *   [Mô tả cách thức kỹ sư rà soát và phê duyệt thủ công kết quả che giấu].

---

## Slide 4: Thiết kế Prompt & Phòng thủ bảo mật (Prompt Defense)
*Tham chiếu: [03-core-prompt-design.md](03-core-prompt-design.md) & [04-compliance-checklist.md](04-compliance-checklist.md)*

*   **Đặc tả cấu trúc System Prompt:**
    *   Cách thức bọc dữ liệu người dùng bằng thẻ XML `<user_data>` để chống tráo vai trò.
    *   Cấu hình tham số mô hình: `temperature = 0.0` để tối ưu tính nhất quán.
*   **Kết quả phòng thủ Prompt Injection (Ngăn chặn thành công 3/3 loại tấn công):**
    *   *Jailbreak:* [Bị block và che giấu bình thường]
    *   *Data Exfiltration:* [Không rò rỉ dữ liệu hệ thống]
    *   *Role Confusion:* [Mô hình giữ vững vai trò trợ lý bảo mật]

---

## Slide 5: Kết quả kiểm thử chức năng & An toàn nhật ký log
*Tham chiếu: [06-test-cases-specification.md](06-test-cases-specification.md)*

*   **Tỷ lệ PASS bộ kiểm thử tự động:** Vượt qua **10/10 ca kiểm thử (100% PASS)**.
*   **Ví dụ xử lý Edge Cases (Tránh ẩn nhầm dữ liệu kỹ thuật):**
    *   Giữ nguyên số đo SCADA thập phân (ví dụ: `0.912.345.678 dB`) không ẩn nhầm thành Số điện thoại.
    *   Giữ nguyên mã số Serial thiết bị 12 chữ số không ẩn nhầm thành số CCCD.
*   **Bảo mật nhật ký log (`execution-log.csv`):** Nhật ký sạch PII 100%, chỉ lưu số lượng trường bị ẩn danh và mã định danh duy nhất (run_id).

---

## Slide 6: Lộ trình triển khai 30-90 ngày & Đề xuất mở rộng
*Tham chiếu: [05-action-plan-30-90-days.md](05-action-plan-30-90-days.md)*

*   **Lộ trình 30-90 ngày:**
    *   *Mốc 30 ngày:* [Triển khai thử nghiệm cho nhóm nhỏ 5 người, thu thập phản hồi]
    *   *Mốc 60 ngày:* [Tối ưu hóa Prompts, cập nhật từ điển Regex, vá lỗi phát sinh]
    *   *Mốc 90 ngày:* [Đóng gói bàn giao runbook kỹ thuật, nghiệm thu và triển khai diện rộng]
*   **3 Trường hợp sử dụng (Use Cases) mở rộng đề xuất:**
    *   [Đề xuất mở rộng 1 - Ví dụ: Ẩn danh log lỗi SCADA tự động]
    *   [Đề xuất mở rộng 2 - Ví dụ: Che giấu thông tin trong biên bản bàn giao mạng lưới]
    *   [Đề xuất mở rộng 3 - Ví dụ: Tích hợp RAG tra cứu nhanh chính sách kỹ thuật an toàn]
