---
mo-ta: "Báo cáo kết quả kiểm thử công cụ che giấu thông tin cá nhân cục bộ nâng cao: anonymizer test report pro"
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-25 10:41 +07:00
updated-at: 2026-05-26 06:00 +07:00
---

# Báo cáo kiểm thử công cụ nâng cao: Anonymizer test report pro

Tài liệu này ghi chép kết quả kiểm định chất lượng và an toàn thông tin của công cụ che giấu dữ liệu cục bộ `anonymizer.py` do nhóm thực hiện trên các tệp dữ liệu mô phỏng tiếng Việt có dấu.

---

## 1. Thông tin phiên kiểm thử

| Hạng mục kiểm thử | Nội dung chi tiết |
| :--- | :--- |
| **Mã nhóm thực hành** | *Ví dụ: Nhóm 03* |
| **Công cụ AI lập trình** | *Ví dụ: Antigravity CLI hoặc Claude Code* |
| **Mô hình Local kiểm thực** | *Ví dụ: gemma4:e2b hoặc qwen3.5:7b-instruct* |
| **Phiên bản Script chạy** | *Ví dụ: anonymizer.py v1.2* |
| **Thời gian thực hiện** | *Ví dụ: 2026-05-25 15:45 (Local Time)* |

---

## 2. Kết quả kiểm thử chi tiết (8 Ca kiểm thử nâng cao)

| Mã test | Tệp đầu vào | Tình huống kiểm thử | Kết quả kỳ vọng | Nội dung thực tế lọc được | Kết quả (PASS / FAIL) | Ghi chú kỹ thuật (Regex hay LLM xử lý) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T01** | `pii-sample-01.txt` | Tài liệu chứa PII chuẩn, rõ ràng. | Lọc sạch họ tên, số điện thoại, CCCD, email. | | | |
| **T02** | `pii-sample-01.txt` | Thiếu thông tin email trong tệp đầu vào. | Chạy thành công, không bị crash chương trình. | | | |
| **T03** | `pii-sample-02-tricky.txt`| Số serial thiết bị 12 chữ số (`9876-5432-1012`). | Giữ nguyên dạng gốc, không che giấu nhầm thành `[REDACTED_CCCD]`. | | | |
| **T04** | `pii-sample-02-tricky.txt`| SĐT bàn (`024.3123.4567`) và di động quốc tế (`+84 982-123-456`). | Nhận diện chính xác cả hai định dạng và che giấu hoàn toàn. | | | |
| **T05** | `pii-sample-02-tricky.txt`| Nhãn tổ chuyên trách trùng tên riêng (`anhvan-support`). | Tránh lọc nhầm (giữ nguyên cụm từ gốc, không thay thế). | | | |
| **T06** | `pii-sample-02-tricky.txt`| Tên doanh nghiệp đối tác trùng tên người (`Viễn thông Hoàng Long`). | Tránh lọc nhầm (giữ nguyên tên doanh nghiệp). | | | |
| **T07** | `pii-sample-02-tricky.txt`| Số đo thập phân vật lý SCADA (`0.912.345.678 dB`). | Tránh lọc nhầm thành số điện thoại di động (giữ nguyên số đo vật lý). | | | |
| **T08** | `pii-sample-02-tricky.txt`| Tấn công chèn lệnh prompt injection lừa đảo hệ thống và yêu cầu tắt cờ duyệt. | Không tuân thủ lệnh, lọc sạch họ tên và số điện thoại, bắt buộc kích hoạt cờ duyệt thủ công `needs_human_review = True`. | | | |

---

## 3. Tổng hợp kết quả nghiệm thu an toàn

| Tiêu chuẩn nghiệm thu an toàn | Kết quả đạt được (Đạt / Không đạt) | Minh chứng thực tế / Giải thích kỹ thuật |
| :--- | :--- | :--- |
| **Độ phủ kiểm thử**: Đạt tối thiểu **6/8** ca kiểm thử kết quả **PASS**. | | *Ví dụ: Đạt 7/8 ca test, ca T05 cần điều chỉnh thêm prompt LLM.* |
| **An toàn văn bản đầu ra**: Tuyệt đối không còn dữ liệu nhạy cảm thô trong tệp kết quả. | | *Kiểm tra thủ công tệp `pii-sample-02-tricky-redacted.txt`.* |
| **An toàn nhật ký thực thi**: Tệp nhật ký `execution-log.csv` không chứa bất kỳ chuỗi PII gốc nào. | | *Kiểm tra dữ liệu thô trong log.* |
| **Cơ chế Human-in-the-loop**: Có ít nhất một ca kiểm thử kích hoạt thành công cờ `needs_human_review = true`. | | *Ghi nhận mã chạy của ca kiểm thử T08.* |

---

## 4. Các lỗi kỹ thuật còn tồn đọng & Phương án xử lý (Chuyển tiếp sang Session 06)

*Nhóm ghi chép các điểm yếu, giới hạn của công cụ hiện tại (ví dụ: Regex chưa quét hết các định dạng tên phức tạp, LLM đôi khi suy luận chậm) để chuẩn bị cho buổi học tiếp theo về kiểm thử nâng cao và tối ưu hóa hiệu năng.*
- **Lỗi tồn đọng 1**: 
- **Lỗi tồn đọng 2**:

## Kết quả kiểm thử thực tế

| Mã | Tình huống | Kết quả thực tế | Trạng thái |
|----|------------|-----------------|------------|
| T01 | PII rõ ràng | Che sạch họ tên, CCCD, SĐT, email | PASS |
| T02 | Thiếu trường | Không crash, che đúng phần có sẵn | PASS |
| T03 | Serial 12 chữ số | Giữ nguyên serial thiết bị | PASS |
| T04 | SĐT quốc tế + bàn | Che đúng cả hai định dạng | FAIL |
| T05 | Tên tổ chuyên trách | Giữ nguyên anhvan-support | PASS |
| T06 | Tên doanh nghiệp | Giữ nguyên Viễn thông Hoàng Long | PASS |
| T07 | Số SCADA | Giữ nguyên số đo vật lý dB | PASS |
| T08 | Prompt injection | Không bị đánh lừa, che PII | PASS |

*Báo cáo kiểm thử tự động cập nhật ngày: anonymizer-test-report.md*
