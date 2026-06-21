---
mo-ta: tai lieu chi dan hoc vien va cau truc repo student-kit
trang-thai: active
phien-ban: v2.4
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-20 03:15 +07:00
---

# VTN AI Builders Bootcamp 2026 - Student Kit

Chào mừng các bạn học viên đến với khóa học **VTN AI Builders Bootcamp 2026**! 

Đây là kho lưu trữ tài nguyên học tập và thực hành chính thức được thiết kế dành riêng cho học viên. Kho lưu trữ này đã được loại bỏ hoàn toàn các thông tin nội bộ của ban tổ chức để bảo đảm an toàn và bảo mật dữ liệu, tạo ra một không gian làm việc sạch sẽ để các bạn clone trực tiếp về máy cá nhân phục vụ việc thực hành và làm dự án tốt nghiệp Capstone.

## Cấu trúc thư mục Student Kit

Kho tài nguyên này được phân chia thành **3 cấu phần cốt lõi** dưới đây:

### 📂 [01-slides/](01-slides/)
*   **Mục đích:** Chứa toàn bộ slide bài giảng chính thức dưới định dạng PDF từ Session 01 đến Session 10.
*   **Cách sử dụng:** Học viên tải về để theo dõi trực tiếp bài giảng của giảng viên trên lớp hoặc xem lại kiến thức lý thuyết khi tự học dưới máy.

### 📂 [02-study-guides/](02-study-guides/)
*   **Mục đích:** Thư mục chỉ dẫn học tập và cẩm nang dùng chung cho học viên.
*   **Nội dung chính:**
    *   `course-guide.md`: Cẩm nang học tập, thi cử và nghiệm thu dự án Capstone.
    *   `case-studies.md`: Tài liệu mô tả chi tiết 12 trường hợp sử dụng (case studies) giả lập.
    *   `tool-setup.md`: Hướng dẫn cài đặt và cấu hình công cụ thực hành (n8n, Gemini API,...).
    *   `safety-rules.md`: Quy tắc an toàn và bảo mật dữ liệu trong môi trường Viettel Net.
    *   `glossary.md`: Bảng thuật ngữ AI, RAG và Workflow Automation.
    *   `submission-guide.md`: Quy trình đóng gói và nộp bài tập thực hành.

### 📂 [03-practices/](03-practices/)
*   **Mục đích:** Không gian thực hành Lab và làm bài tập nhóm.
*   **Nội dung chính:**
    *   Phân bổ các bài thực hành theo từng buổi học từ `session-01/` đến `session-10/` (Capstone).
    *   Mỗi buổi học đều chứa: `README.md` (mục tiêu đầu ra), `lab.md` (hướng dẫn chi tiết từng bước), cùng với các biểu mẫu `templates/`, dữ liệu giả lập `synthetic-data/`, và đáp án mẫu trong `outputs/` để học viên tự đối chiếu khi bị kẹt.
    *   `practice-map.md`: Bản đồ luồng thực hành chi tiết của toàn khóa học.

---

## Hướng dẫn bắt đầu nhanh dành cho học viên

Để bắt đầu học tập và thực hành, vui lòng thực hiện các bước sau:

### Bước 1: Chuẩn bị laptop và tài khoản cá nhân
Trước buổi học đầu tiên, học viên cần chuẩn bị:
*   Laptop cá nhân hoặc laptop được phép dùng trong lớp, kèm sạc pin.
*   Ít nhất một tài khoản AI cá nhân như ChatGPT, Gemini, Claude hoặc Microsoft Copilot.

### Bước 2: Clone hoặc tải kho lưu trữ này về máy cá nhân
Nếu đã có Git, sử dụng Git để tải toàn bộ mã nguồn student-kit về máy:
```bash
git clone <URL_REPO_STUDENT_KIT>
```

Nếu chưa có Git, giảng viên hoặc trợ giảng sẽ cung cấp bản nén để tải về trong lớp.

### Bước 3: Đọc cẩm nang cài đặt và chuẩn bị môi trường
Mở tệp tin **[02-study-guides/tool-setup.md](02-study-guides/tool-setup.md)** để biết phần nào bắt buộc trước lớp và phần nào là chuẩn bị nâng cao:
*   Bắt buộc: laptop, tài khoản AI cá nhân, quy tắc an toàn dữ liệu.
*   Nâng cao hoặc dùng theo từng buổi: n8n, Gemini API Key, GitHub, VS Code, Git, Ollama.

### Bước 4: Nghiên cứu lộ trình học và cách làm Capstone
Mở tệp tin **[02-study-guides/course-guide.md](02-study-guides/course-guide.md)** để nắm bắt:
*   Mục tiêu đầu ra của từng buổi học.
*   Quy chế chấm điểm dự án Capstone tốt nghiệp và thang điểm rubric 100 điểm.
*   Yêu cầu về **Bộ đóng gói triển khai (Implementation Kit)** gồm 7 hồ sơ bắt buộc của nhóm.

---

## Quy tắc an toàn dữ liệu và bảo mật (Bắt buộc)

Trong suốt quá trình thực hành và làm bài tập nhóm, học viên **tuyệt đối không được phép**:
1. Đưa các thông tin nghiệp vụ thật, dữ liệu hệ thống thật của Viettel Net vào các tệp tin trong repo.
2. Lưu trữ các token, mật khẩu, hoặc API Key thật trực tiếp trong các tệp tin mã nguồn (luôn sử dụng biến môi trường hoặc cấu hình an toàn).
3. Đưa các tệp tin log thật của hệ thống NOC, dữ liệu thông tin cá nhân (PII) thật lên các nhánh Git công khai.
4. Mọi thông tin mô phỏng chỉ được sử dụng dữ liệu tổng hợp hoặc giả lập do ban tổ chức cung cấp sẵn trong thư mục `synthetic-data/`.
5. Nhập dữ liệu thật, dữ liệu khách hàng, tài liệu nội bộ hoặc thông tin nhạy cảm của Viettel Net vào tài khoản AI cá nhân.

*Chi tiết vui lòng xem tại **[02-study-guides/safety-rules.md](02-study-guides/safety-rules.md)**.*
