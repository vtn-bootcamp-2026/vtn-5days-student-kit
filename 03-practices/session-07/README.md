---
mo-ta: Tổng quan bài thực hành Session 07 - Hermes Basic thiết lập Trợ lý cá nhân và Đóng gói Quy trình (Skill) cho học viên non-tech
trang-thai: active
phien-ban: v3.2
created-at: 2026-06-21 09:00 +07:00
updated-at: 2026-06-21 09:45 +07:00
---

# Buổi 07: Hermes Basic — Thiết lập Trợ lý cá nhân & Đóng gói Quy trình (Skill)

## Mục tiêu

Buổi thực hành giúp học viên phi kỹ thuật: non-tech làm quen và làm chủ phần mềm Hermes Desktop Client để xây dựng lực lượng lao động AI cá nhân: Personal AI Workforce có kỷ luật và ranh giới an toàn:
1. **Cấu hình kết nối API:** Kết nối API Key từ 1 trong 2 nhà cung cấp: Google Gemini (qua `hermes model`) hoặc OpenRouter. Học viên chọn 1 phương pháp và ghi nhận vào `runbook-log.json`.
2. **Đóng gói quy trình (Skill):** Chuyển đổi một chỉ thị: prompt thô thành một kỹ năng: Skill có cấu trúc nghiệp vụ lặp lại ổn định.
3. **Quản lý đa tác nhân (Multi-profile):** Tạo và vận hành song song 2 Trợ lý ảo (`HR_Admin_Assistant` và `HR_Recruitment_Assistant`) biệt lập ngữ cảnh 100%.
4. **Tích hợp tri thức cục bộ (Knowledge Base):** Nạp tài liệu quy trình vận hành vào Profile để Trợ lý tự tra cứu.
5. **Tự động hóa tác vụ (Cron Job):** Lên lịch quét và tóm tắt dữ liệu tự động theo khung giờ quy định.
6. **Kiểm thử ranh giới an toàn & Dọn dẹp bộ nhớ:** Chạy 3 ca kiểm thử: Test Cases nghiệp vụ bắt buộc và thực hiện quy trình xóa bộ nhớ: Memory Clear Protocol để bảo vệ dữ liệu.

## Cấu trúc bài thực hành

Bài thực hành bao gồm 8 bài Lab liên hoàn được thiết kế chi tiết:

| Bài Lab | Hoạt động chính | Thời lượng | Đầu ra cần đạt |
|---|---|---:|---|
| **Lab 0** | **Cài đặt Hermes trên Windows:** Mở PowerShell và chạy lệnh cài đặt CLI. | 15 phút | Lệnh `hermes --version` phản hồi phiên bản. |
| **Lab 1** | **Cấu hình kết nối ban đầu:** Kết nối Google Gemini HOẶ OpenRouter API và chọn mô hình. | 15 phút | Trò chuyện kiểm thử xác nhận mô hình đang chạy. |
| **Lab 2** | **Từ Prompt thành Skill:** Tạo cấu trúc prompt nghiệp vụ và lưu thành Skill. | 15 phút | Cấu hình Skill `Report-Summary-Admin` lưu thành công. |
| **Lab 3** | **Thiết lập Profile thứ nhất & SOUL.md:** Định danh Trợ lý báo cáo tuần. | 20 phút | Profile `HR_Admin_Assistant` hoạt động kèm `SOUL.md` 5 dòng. |
| **Lab 4** | **Tích hợp Tri thức cục bộ (Knowledge Base):** Gắn thư mục tài liệu quy trình. | 20 phút | Agent tra cứu tự động SLA quy trình mức Cao đạt 4 giờ. |
| **Lab 5** | **Thiết lập Profile thứ hai & Cách ly ngữ cảnh:** Định danh Trợ lý biên bản họp. | 20 phút | Profile `HR_Recruitment_Assistant` độc lập, không lẫn ngữ cảnh. |
| **Lab 6** | **Tự động hóa tác vụ (Cron Job):** Cấu hình biểu thức định thời tự động chạy. | 25 phút | Cron Job quét và ghi nhận tóm tắt báo cáo ra tệp tin output. |
| **Lab 7** | **Kiểm thử Ranh giới & Memory Clear:** Chạy 3 test case và xóa sạch tệp SQLite vật lý. | 25 phút | Test case đạt yêu cầu, xóa thành công `state.db` / `hermes.db`. |
| **Nghiệm thu** | **Nghiệm thu & Chấm chéo:** Chấm chéo giữa các nhóm và phản tư. | 10 phút | Bảng điểm Rubric và tệp tin `runbook-log.json`. |

> [!TIP]
> **Dành cho học viên hoàn thành sớm (Fast-trackers):** Hãy thực hiện ít nhất 1 trong 3 **Thử thách nâng cao (Bonus Challenges)** ở cuối hướng dẫn thực hành [lab.md](lab.md) để nhận điểm cộng đặc biệt từ giảng viên.

## Tài nguyên đầu vào (Resources)

Học viên sử dụng kho dữ liệu giả lập có sẵn trong thư mục `synthetic-data/`:
- [bao-cao-tuan-hanh-chinh-nhan-su.md](synthetic-data/bao-cao-tuan-hanh-chinh-nhan-su.md): Báo cáo tuần thô của Tổ Hành chính.
- [bien-ban-hop-hanh-chinh-nhan-su.md](synthetic-data/bien-ban-hop-hanh-chinh-nhan-su.md): Biên bản cuộc họp giao ban tuần của bộ phận Hành chính - Nhân sự.
- [quy-dinh-phuc-loi-va-sla-hanh-chinh.md](synthetic-data/quy-dinh-phuc-loi-va-sla-hanh-chinh.md): Quy chế hành chính và quy định hạn mức tạm ứng (mã quy trình QC-HC-05).

## Đầu ra bàn giao bắt buộc (Artifacts)

Cuối buổi thực hành, nhóm học viên nộp lại các sản phẩm sau vào kho lưu trữ: repository của nhóm:
1. `SOUL.md` (cho Trợ lý hành chính nhân sự) - Viết theo đúng công thức 5 dòng.
2. `SOUL.md` (cho Trợ lý hỗ trợ tuyển dụng) - Viết theo đúng công thức 5 dòng.
3. Tệp cấu hình Skill dạng JSON hoặc Markdown.
4. Ảnh chụp màn hình hoặc log chạy 3 ca kiểm thử bắt buộc (đủ dữ liệu, thiếu dữ liệu, ngoài phạm vi).
5. Tệp tin `runbook-log.json` lưu thông số chạy của Agent.
6. Safety Checklist xác nhận đã hoàn thành xóa tệp `state.db` hoặc `hermes.db` vật lý trên PowerShell.

## SLI/SLO Kiểm soát chất lượng (Quality Gates)

| SLI | Đo lường | SLO (Mục tiêu) | Phương thức xác thực |
|---|---|---|---|
| Cài đặt môi trường | Lệnh `hermes --version` phản hồi đúng | 100% học viên | Kiểm tra CLI |
| Độ chính xác SOUL | SOUL.md tuân thủ đúng công thức 5 dòng | 100% profiles | Đọc duyệt file |
| Khả năng tra cứu KB | Truy vấn đúng SLA yêu cầu khẩn cấp (Mức Cao) là 4 giờ | 100% nhóm | Chạy thử nghiệm |
| Cô lập ngữ cảnh | Profile 2 từ chối trả lời thông tin của Profile 1 | 100% nhóm | Chạy Multi-profile test |
| Tự động hóa tác vụ | Cron Job tạo thành công tệp đầu ra output | 100% nhóm | Kiểm tra thư mục outputs |
| Tỷ lệ kiểm thử đạt | Đạt tối thiểu 3 test case bắt buộc | 3/3 ca (100%) | Xem báo cáo test |
| Bảo mật thông tin | Xóa sạch bộ nhớ SQLite vật lý sau khi chạy | 100% máy trạm | Kiểm tra file vật lý |
