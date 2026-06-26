---
mo-ta: "Prompt 3 — Thiết kế cấu trúc IPO của Skill và sinh tệp skill_design.md"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 3: Thiết kế cấu trúc IPO của Skill (Generate skill_design.md)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat để tạo tệp thiết kế `skill_design.md`:

```text
BỐI CẢNH:
Tôi cần thiết kế chi tiết kiến trúc cho Skill (gói kỹ năng/nhân viên số) của dự án này dưới dạng tệp `skill_design.md` theo cấu trúc IPO (Input – Process – Output) chuẩn hóa từ Session 5. File này sẽ làm cơ sở đầu vào để subagent sinh mã tự động.

CHỈ DẪN CHO AI:
Hãy viết nội dung hoàn chỉnh của tệp `skill_design.md` dựa trên bối cảnh dự án của chúng ta. File thiết kế phải gồm chính xác các mục sau đây (không được bỏ mục nào):

0. Thông tin chung: Tên skill (dùng kebab-case), mô tả ngắn 1 câu, người dùng chính.
1. Trigger: Điều kiện kích hoạt skill (loại file đầu vào như .txt/.csv/.docx, từ khóa đặc thù, ngữ cảnh).
2. Input: Đặc tả đầu vào (văn bản/dữ liệu cần xử lý, file cấu hình, điều kiện hợp lệ của dữ liệu đầu vào, dữ liệu cấm/nhạy cảm chưa lọc).
3. Process: Chi tiết luồng xử lý 4 bước:
   - Intake: Tiếp nhận và đọc dữ liệu.
   - Extract: Phân tích và trích xuất thực thể.
   - Validate: Kiểm tra tính hợp lệ và toàn vẹn của kết quả.
   - Route: Chuyển hướng kết quả đầu ra (xuất file hoặc chuyển người duyệt nếu cần).
   - Phân vai rõ ràng: Phần nào do Code Python chạy độc lập quyết định (Regex, lưu file, ghi log) và phần nào do Local LLM (suy luận ngữ cảnh) thực hiện.
4. Output: Đặc tả đầu ra (file kết quả, cấu trúc JSON Schema chi tiết với các trường thông tin cụ thể, các trạng thái kết thúc).
5. Quality Gate: Danh sách quy tắc Do / Don't (mỗi bên ít nhất 3 quy tắc) để kiểm soát chất lượng kết quả đầu ra của skill.
6. Human-In-The-Loop (HITL): Điểm chặn phê duyệt của con người, phân định rõ AI làm gì và con người làm gì.
7. Cấu trúc folder dự kiến của Skill Package: Đặc tả cấu trúc thư mục gồm:
   - `SKILL.md` (Hướng dẫn sử dụng skill)
   - `skill.json` (Cấu hình kích hoạt & quyền hạn)
   - `schemas/` (Định dạng schema kiểm định JSON)
   - `kb/` (Thư viện tri thức bổ trợ)
   - `scripts/` (Các tệp mã nguồn python: intake, validator, router)
   - `outputs/` (Thư mục lưu tệp kết quả sạch)
8. Test cases tối thiểu: Ít nhất 3 ca kiểm thử cơ bản (Normal case, Missing data case, Error/Risky case).

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Bản thiết kế cấu trúc IPO (Input-Process-Output) của Skill phục vụ bài Capstone tại VTN"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không kèm thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh của tệp `skill_design.md` để lưu lại trong thư mục làm việc của nhóm.
