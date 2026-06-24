---
mo-ta: "Quy tắc phát hiện cờ đỏ trong hồ sơ ứng viên (Red Flag Rules)"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-24 10:09 +07:00
updated-at: 2026-06-24 10:09 +07:00
---

# Quy tắc nhận diện cờ đỏ khi duyệt hồ sơ: Red Flag Rules

Hệ thống lọc tự động phải quét và phát hiện các dấu hiệu bất thường hoặc các điểm bất lợi (cờ đỏ: red flags) trong CV của ứng viên. Phát hiện cờ đỏ sẽ lập tức kích hoạt trạng thái **Cần người duyệt: needs_human_review (HITL)** bất kể điểm số của ứng viên cao thế nào.

---

## 1. Danh sách cờ đỏ tiêu chuẩn

### Cờ đỏ 1: Khoảng trống kinh nghiệm kéo dài: Employment Gaps
- **Định nghĩa:** Có khoảng thời gian trống không làm việc giữa các công ty kéo dài từ **6 tháng trở lên** mà không có lý do giải trình rõ ràng (ví dụ: học nâng cao, nghỉ thai sản, dự án cá nhân).
- **Hành động của AI:** Ghi nhận cờ đỏ và trích xuất khoảng thời gian trống đó vào phần dẫn chứng để HR đối chất khi phỏng vấn.

### Cờ đỏ 2: Tần suất nhảy việc quá cao: Job Hopping
- **Định nghĩa:** Thay đổi công việc liên tục (làm việc tại **3 công ty trở lên trong vòng 2 năm gần nhất**), ngoại trừ các công việc ghi rõ là thực tập sinh hoặc làm việc theo hợp đồng dự án ngắn hạn: Freelance/Contractor.
- **Hành động của AI:** Đánh dấu cảnh báo về mức độ gắn kết lâu dài của ứng viên.

### Cờ đỏ 3: Bất nhất về mặt thời gian: Time Inconsistency
- **Định nghĩa:** Trùng lặp thời gian làm việc toàn thời gian: Full-time tại hai công ty khác nhau mà không có giải thích, hoặc ngày tháng bắt đầu làm việc sau ngày tháng kết thúc (lỗi logic thời gian).
- **Hành động của AI:** Đánh dấu cờ đỏ nghi ngờ về độ trung thực của hồ sơ hoặc lỗi định dạng CV nghiêm trọng.

### Cờ đỏ 4: Thiếu thông tin liên hệ cơ bản: Missing Contact Info
- **Định nghĩa:** CV không chứa số điện thoại hoặc địa chỉ email hợp lệ để liên lạc.
- **Hành động của AI:** Ghi nhận lỗi và tự động hạ điểm tin cậy `confidence_score` xuống dưới 0.5, buộc chuyển trạng thái HITL.

### Cờ đỏ 5: Suy giảm cấp bậc chức vụ bất thường: Career Regression
- **Định nghĩa:** Ứng viên chuyển từ vai trò quản lý cấp cao (ví dụ: Team Leader, Manager) xuống vai trò nhân viên thực thi cấp thấp hơn ở công ty sau đó mà không có giải trình rõ ràng.
- **Hành động của AI:** Đánh dấu cờ đỏ để HR kiểm tra nguyên nhân (năng lực hay định hướng cá nhân).

---

## 2. Cách thức xử lý khi gặp Cờ đỏ

Khi phát hiện bất kỳ cờ đỏ nào từ danh sách trên:
1. Ghi nhận mô tả cụ thể về cờ đỏ vào mảng `red_flags` trong JSON đầu ra.
2. Buộc thiết lập thuộc tính `need_review` thành `true`.
3. Chuyển trạng thái định tuyến `status` thành `needs_human_review`.
4. Trích xuất chính xác đoạn văn bản trong CV gây ra cờ đỏ vào mảng `evidence` làm cơ sở đối chiếu cho HR.
