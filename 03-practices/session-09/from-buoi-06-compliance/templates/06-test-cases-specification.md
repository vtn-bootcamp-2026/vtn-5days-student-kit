---
mo-ta: "Biểu mẫu đặc tả ca kiểm thử cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-26 07:00 +07:00
updated-at: 2026-06-14 23:15 +07:00
---

# Đặc tả ca kiểm thử: Mini tool anonymizer

*   **Tên nhóm thực hiện:** [Điền tên nhóm]
*   **Thành viên:** [Điền tên các thành viên]
*   **Phiên bản công cụ kiểm thử:** v1.0 (Nâng cấp từ Buổi 5)
*   **Ngày thực hiện kiểm thử:** [Điền ngày]

---

## 1. Khung tổng quan ca kiểm thử (Test suite overview)

Bộ kiểm thử yêu cầu thiết lập tối thiểu **10 ca kiểm thử (test cases)** bao phủ đầy đủ 4 nhóm tình huống nghiệp vụ:
1.  **Tình huống bình thường (Normal cases):** 3 test cases.
2.  **Tình huống lỗi (Error cases):** 2 test cases.
3.  **Tình huống thiếu dữ liệu (Missing data cases):** 2 test cases.
4.  **Tình huống vượt phạm vi (Out of bounds cases):** 3 test cases.

---

## 2. Chi tiết các ca kiểm thử

### Nhóm 1: Tình huống bình thường (Normal cases)
*Đảm bảo các dữ liệu nhạy cảm chuẩn hóa được phát hiện và che giấu đúng nhãn đại diện.*

#### Ca kiểm thử TC-01: Che giấu tên người và số điện thoại chuẩn Việt Nam
*   **Mô tả đầu vào:** "Kỹ sư Nguyễn Văn A có số điện thoại cá nhân là 0987654321."
*   **Kết quả mong đợi:** "Kỹ sư [NAME] có số điện thoại cá nhân là [PHONE_NUMBER]."
*   **Kết quả thực tế:** [Đạt / Không đạt (Ghi chi tiết)]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-02: Che giấu email và địa chỉ cơ bản
*   **Mô tả đầu vào:** "Mọi thắc mắc xin gửi về hòm thư điện tử support@viettel.com.vn hoặc đến trực tiếp Văn phòng Viettel Net tại Duy Tân, Cầu Giấy, Hà Nội."
*   **Kết quả mong đợi:** "Mọi thắc mắc xin gửi về hòm thư điện tử [EMAIL] hoặc đến trực tiếp Văn phòng Viettel Net tại [ADDRESS]."
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-03: Che giấu số thẻ Căn cước công dân (CCCD) hợp lệ
*   **Mô tả đầu vào:** "Trưởng phòng B có số CCCD là 037198001234."
*   **Kết quả mong đợi:** "Trưởng phòng B có số CCCD là [CCCD_NUMBER]."
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

---

### Nhóm 2: Tình huống lỗi (Error cases)
*Đảm bảo công cụ nhận diện và xử lý tốt các dữ liệu đầu vào bị lỗi cấu trúc hoặc sai quy chuẩn định dạng.*

#### Ca kiểm thử TC-04: Số CCCD thiếu số (Lỗi định dạng nghiêm trọng)
*   **Mô tả đầu vào:** "Thông tin kê khai của nhân sự C bị thiếu, số định danh ghi là 0371980012." (Chỉ có 10 chữ số thay vì 12 chữ số).
*   **Kết quả mong đợi:** Công cụ phát hiện độ dài không hợp lệ, không che giấu bừa bãi và ghi nhận cảnh báo: `[WARNING: INVALID_CCCD_LENGTH]`.
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-05: Địa chỉ email viết sai định dạng tên miền
*   **Mô tả đầu vào:** "Liên hệ lập lịch trực ca qua email admin@viettelnet..vn hoặc admin@viettelnet@com."
*   **Kết quả mong đợi:** Công cụ nhận diện đây là chuỗi lỗi, ghi nhận log cảnh báo hoặc bỏ qua để tránh nhận diện sai email chuẩn.
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

---

### Nhóm 3: Tình huống thiếu dữ liệu (Missing data cases)
*Đảm bảo công cụ không bị sập và phản hồi an toàn khi đầu vào trống hoặc thiếu các trường thông tin bắt buộc.*

#### Ca kiểm thử TC-06: Văn bản đầu vào trống (Empty input)
*   **Mô tả đầu vào:** Chuỗi rỗng `""` hoặc chỉ chứa khoảng trắng `"   "`.
*   **Kết quả mong đợi:** Công cụ trả về chuỗi rỗng một cách an toàn, ghi nhận log `INFO: Empty input received` và không gây sập ứng dụng (No crash).
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-07: Văn bản chỉ có ký tự đặc biệt hoặc thẻ HTML rỗng
*   **Mô tả đầu vào:** `<div><br></div> &nbsp; @#$%^&*`
*   **Kết quả mong đợi:** Công cụ làm sạch hoặc trả lại chuỗi an toàn, không cố gắng phân tích PII trên các ký tự vô nghĩa.
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

---

### Nhóm 4: Tình huống vượt phạm vi (Out of bounds cases)
*Đảm bảo công cụ đứng vững trước các tình huống biên phức tạp và các kịch bản tấn công bảo mật.*

#### Ca kiểm thử TC-08: Tên riêng trùng danh từ thường lắt léo
*   **Mô tả đầu vào:** "Sáng nay, anh Hoa đã đi mua một bó hoa rất đẹp để tặng chị Hồng nhân dịp sinh nhật."
*   **Kết quả mong đợi:** "Sáng nay, anh [NAME] đã đi mua một bó hoa rất đẹp để tặng chị [NAME] nhân dịp sinh nhật." (Chỉ ẩn "Hoa", "Hồng" đóng vai trò tên riêng; giữ nguyên từ "hoa", "hồng" đóng vai trò danh từ/tính từ thường).
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-09: Tấn công Prompt Injection kiểu vượt rào (Jailbreak)
*   **Mô tả đầu vào:** Lấy mẫu từ file `synthetic-data/prompt-injection-attacks.txt` (Kịch bản 1).
*   **Kết quả mong đợi:** Công cụ từ chối lệnh gỡ lỗi thô của hacker, vẫn giữ nguyên cơ chế ẩn danh và in ra văn bản đã được lọc PII an toàn.
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

#### Ca kiểm thử TC-10: Tấn công đánh cắp dữ liệu qua Base64 (Data exfiltration)
*   **Mô tả đầu vào:** Lấy mẫu từ file `synthetic-data/prompt-injection-attacks.txt` (Kịch bản 2).
*   **Kết quả mong đợi:** Mô hình phát hiện yêu cầu chuyển đổi trái phép, từ chối nhúng PII vào URL Base64 và thực hiện ẩn danh bình thường.
*   **Kết quả thực tế:** [Đạt / Không đạt]
*   **Trạng thái:** [Pass / Fail]

---

## 3. Tổng hợp kết quả và Đánh giá (Test summary)

*   **Tổng số ca kiểm thử đã chạy:** 10
*   **Số ca ĐẠT (Pass):** 0 / 10
*   **Số ca THẤT BẠI (Fail):** 0 / 10
*   **Tỷ lệ thành công:** 0%

### Ghi chú lỗi phát hiện và Phương án khắc phục:
1.  *Lỗi 1:* [Mô tả lỗi nếu bộ lọc Regex hoặc LLM lọc sót/lọc nhầm]
    *   *Cách khắc phục:* [Ví dụ: Thêm System Prompt giới hạn hoặc tối ưu hóa Regex]
2.  *Lỗi 2:* [Mô tả lỗi]
    *   *Cách khắc phục:* [Mô tả]
