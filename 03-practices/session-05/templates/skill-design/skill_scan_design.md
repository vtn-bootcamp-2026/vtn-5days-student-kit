---
mo-ta: "Tài liệu thiết kế đầu vào IPO cho skill Scan CV hỗ trợ tuyển dụng."
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-23 16:30 +07:00
updated-at: 2026-06-24 10:08 +07:00
---

# Thiết kế kỹ năng: skill-scan-cv

> Tài liệu này mô tả chi tiết đầu vào, quy trình xử lý, và đầu ra (IPO) của kỹ năng chuyên biệt: skill-scan-cv (Scan CV tuyển dụng), đóng vai trò như một nhân sự số chuyên môn nghiệp vụ trong bộ phận hành chính nhân sự: HR.

---

## 0. Thông tin chung

- **Tên skill:** skill-scan-cv (hoặc `vibe-hr-cv-scanner` theo quy chuẩn đặt tên hệ thống)
- **Một câu mô tả:** Trích xuất thông tin từ hồ sơ ứng viên: CV, so khớp mức độ phù hợp với mô tả công việc: Job Description - JD, rà soát cờ đỏ: red flags, và định tuyến hồ sơ tự động hoặc chuyển người duyệt: HITL.
- **Người dùng:** Chuyên viên tuyển dụng trong phòng hành chính nhân sự: HR.
- **Mỏ neo lý thuyết:** Kiến trúc IPO (Input-Process-Output) phối hợp với chu trình PDCA để cải tiến chất lượng lọc hồ sơ tự động.

---

## 1. Kích hoạt: Trigger — Kích hoạt khi nào?

Kỹ năng sẽ tự động kích hoạt khi nhận diện các tín hiệu sau từ người dùng:

- **Loại file đầu vào:** Tệp tin văn bản đại diện cho CV ứng viên có định dạng `.docx`, `.pdf`, `.txt`.
- **Từ khóa người dùng nói:** "scan cv", "rà soát cv", "đánh giá hồ sơ", "cv screening", "chấm điểm ứng viên", "lọc hồ sơ".
- **Ngữ cảnh:** Khi chuyên viên tuyển dụng tải lên một hoặc nhiều tệp CV và yêu cầu kiểm tra, so sánh độ phù hợp với tiêu chí tuyển dụng.

---

## 2. Đầu vào: Input — Đầu vào là gì?

- **Dữ liệu chính:** Tệp CV của ứng viên (ví dụ: `synthetic-data/cv-sample.md` hoặc các tệp `.docx`, `.pdf` trong thư mục chờ xử lý).
- **Dữ liệu phụ trợ: knowledge base:** 
  - `kb/job-descriptions.md`: Tài liệu chứa thông tin mô tả công việc tiêu chuẩn cho các vị trí tuyển dụng.
  - `kb/evaluation-rubrics.md`: Bộ quy tắc chấm điểm và thang đánh giá ứng viên.
  - `kb/red-flag-rules.md`: Bộ quy tắc phát hiện các điểm bất thường hoặc bất lợi trong hồ sơ (cờ đỏ: red flags).
- **Điều kiện đầu vào hợp lệ:** Tệp tin CV không bị trống, có dung lượng tối đa 10MB, định dạng văn bản đọc được rõ ràng và có chứa tối thiểu thông tin học vấn hoặc kinh nghiệm làm việc để phân tích.
- **Dữ liệu cấm: data boundaries:** Tuyệt đối không nhận CV chứa thông tin cá nhân cực kỳ nhạy cảm: PII như số thẻ căn cước: National ID, thông tin tài khoản ngân hàng, hoặc địa chỉ nhà cụ thể (chỉ giữ lại thành phố cư trú).

---

## 3. Xử lý: Process — Xử lý như thế nào?

Quy trình xử lý tuần tự gồm 4 bước kỹ thuật:

1. **Tiếp nhận: Intake:** Đọc nội dung tệp CV thô, thực hiện chuẩn hóa văn bản và kiểm tra định dạng đầu vào hợp lệ (sử dụng script Python `scripts/intake.py`).
2. **Trích xuất thông tin: Extract:** Sử dụng mô hình ngôn ngữ để trích xuất các trường thông tin có cấu trúc (học vấn, kỹ năng, kinh nghiệm) theo tài liệu cấu trúc định dạng đầu ra `schema/evaluation.schema.json`. Mỗi thông tin trích xuất bắt buộc phải đi kèm dẫn chứng nguyên văn: source evidence từ CV gốc.
3. **Tự kiểm và chấm điểm: Validate & Evaluate:** So sánh kỹ năng và kinh nghiệm của ứng viên với mô tả công việc: JD bằng thang chấm điểm: rubric. Thực hiện kiểm tra chéo các quote trích dẫn để đảm bảo tính xác thực thông qua script `scripts/validator.py`.
4. **Định tuyến: Route:** Đối chiếu với quy tắc cờ đỏ tuyển dụng để xác định trạng thái hồ sơ: Tự động đạt: Auto Pass, Cần người duyệt: Needs Human Review (HITL), hoặc Từ chối: Reject (sử dụng script `scripts/router.py`).

- **Script gọi:** 
  - `scripts/intake.py`
  - `scripts/validator.py`
  - `scripts/router.py`
- **Công cụ AI dùng:** LLM thực hiện đọc hiểu, trích xuất cấu trúc và so khớp ngữ nghĩa; kết hợp với code Python để kiểm thử tất định và tính toán điểm số.

---

## 4. Đầu ra: Output — Đầu ra là gì?

- **File output:**
  - `outputs/screened-cvs/<candidate_name>.json`: Tệp lưu kết quả trích xuất cấu trúc chi tiết.
  - `outputs/reports/<candidate_name>-evaluation.md`: Báo cáo đánh giá chi tiết mức độ phù hợp và danh sách cờ đỏ (nếu có).
  - `outputs/execution-log.jsonl`: Nhật ký ghi lại quá trình vận hành hệ thống.
- **Schema đầu ra:** Định nghĩa chi tiết trong `schema/evaluation.schema.json` gồm các trường bắt buộc:
  - `candidate_name`: Tên ứng viên
  - `contact_info`: Điện thoại và Email
  - `experience_years`: Số năm kinh nghiệm
  - `education`: Trình độ học vấn cao nhất
  - `skills`: Danh sách kỹ năng chính
  - `suitability_score`: Điểm độ phù hợp (thang điểm 100)
  - `matched_criteria`: Các tiêu chí đáp ứng tốt
  - `missing_criteria`: Các tiêu chí còn thiếu
  - `red_flags`: Danh sách cờ đỏ phát hiện
  - `status`: Kết quả định tuyến (`auto_pass`, `needs_human_review`, `reject`)
  - `evidence`: Mảng chứa các dẫn chứng cụ thể từ hồ sơ gốc
  - `confidence_score`: Điểm tin cậy của mô hình (0.0 - 1.0)
  - `need_review`: Có cần người duyệt lại hay không (kiểu Boolean)
- **Trạng thái kết thúc:** `auto_pass` (đạt điểm cao, không có cờ đỏ) / `needs_human_review` (nằm trong khoảng điểm nghi vấn hoặc có cờ đỏ nhẹ) / `reject` (điểm quá thấp hoặc có cờ đỏ nghiêm trọng).

---

## 5. Quy tắc chất lượng: Quality Gate — Do / Don't

**Nên làm: DO:**
- Mỗi thông tin đánh giá quan trọng phải đi kèm dẫn chứng nguyên văn: verbatim quote và ghi rõ dòng/vị trí trích xuất từ CV.
- Kết quả xuất ra phải tuân thủ nghiêm ngặt định dạng JSON Schema được thiết lập sẵn.
- Tự động hạ điểm tin cậy: confidence score xuống dưới 0.7 nếu phát hiện bất kỳ sự thiếu nhất quán nào trong dẫn chứng hoặc thiếu thông tin quan trọng.

**Không được làm: DON'T:**
- Tuyệt đối không tự suy diễn hoặc bịa đặt kỹ năng, kinh nghiệm mà ứng viên không đề cập trong CV.
- Không tự động gửi email từ chối hay hẹn phỏng vấn trực tiếp tới ứng viên mà chưa qua bước kiểm duyệt của con người khi hồ sơ rơi vào trạng thái cần xem xét: needs_human_review.
- Không lưu lại bất kỳ thông tin cá nhân nhạy cảm: PII nào của ứng viên trong cơ sở dữ liệu dùng chung hoặc nhật ký hoạt động.

---

## 6. Con người kiểm duyệt: Human In the Loop — HITL

- **Khi nào chuyển người duyệt:** 
  - Khi điểm phù hợp của ứng viên nằm trong khoảng trung bình (từ 50 đến 70 trên thang điểm 100).
  - Khi phát hiện bất kỳ cờ đỏ: red flag nào liên quan đến khoảng trống kinh nghiệm làm việc: employment gaps hoặc số lần nhảy việc liên tục.
  - Khi điểm tin cậy trích xuất dữ liệu của AI dưới 0.7 (`confidence_score < 0.7`).
- **Người duyệt làm gì:** Đọc báo cáo đánh giá, kiểm tra các cờ đỏ được hệ thống cảnh báo, đối chiếu lại với CV gốc và đưa ra quyết định cuối cùng là chấp nhận phỏng vấn hay từ chối.
- **Phân công công việc:** AI thực hiện trích xuất dữ liệu, kiểm tra tính hợp lệ của evidence, so khớp tiêu chí và tính điểm sơ bộ; Con người đóng vai trò đưa ra phán quyết và kiểm chứng các trường hợp nghi ngờ.

---

## 7. Cấu trúc thư mục của kỹ năng sẽ tạo ra

Kỹ năng Scan CV sau khi được sinh ra sẽ có cấu trúc thư mục tiêu chuẩn như sau:

```text
skill-scan-cv/
  SKILL.md                  ← Bản đồ hướng dẫn chạy kỹ năng dành cho Agent (sinh từ §1–§6)
  skill.json                ← Metadata cấu hình trigger và phân quyền hệ thống
  schema/
    evaluation.schema.json  ← Lược đồ JSON ràng buộc đầu ra của quá trình đánh giá (từ §4)
  kb/
    evaluation-rubrics.md   ← Tiêu chuẩn và thang chấm điểm chi tiết (từ §2)
    red-flag-rules.md       ← Bộ quy tắc nhận diện cờ đỏ khi lọc hồ sơ (từ §2)
  scripts/
    intake.py               ← Script Python hỗ trợ đọc và chuẩn hóa văn bản CV (từ §3)
    validator.py            ← Script kiểm chứng tính khớp của dẫn chứng và schema (từ §3)
    router.py               ← Script định tuyến phân loại hồ sơ (từ §3)
  synthetic-data/
    cv-sample.md            ← Dữ liệu CV mô phỏng để chạy thử nghiệm kỹ năng
  test/
    smoke-test.md           ← Kịch bản kiểm thử nhanh các trường hợp đầu vào
```

---

## 8. Các trường hợp kiểm thử tối thiểu

| # | Ca kiểm thử | Trạng thái kỳ vọng | Dấu hiệu nhận biết |
|---|-------------|--------------------|-------------------|
| 1 | Ứng viên xuất sắc đáp ứng mọi tiêu chí | `auto_pass` | Điểm số >= 85, không có cờ đỏ, đầy đủ dẫn chứng rõ ràng. |
| 2 | CV thiếu thông tin học vấn hoặc kinh nghiệm | `needs_human_review` | Gắn nhãn thiếu trường thông tin quan trọng, điểm tin cậy `confidence_score < 0.7`. |
| 3 | CV chứa cờ đỏ (ví dụ: nhảy việc 3 lần trong 1 năm) | `needs_human_review` | Danh sách cờ đỏ `red_flags` chứa cảnh báo chi tiết, chuyển trạng thái HITL. |
| 4 | Hồ sơ hoàn toàn không phù hợp với JD | `reject` | Điểm số dưới 50, hệ thống tự động đưa ra đề xuất từ chối. |
