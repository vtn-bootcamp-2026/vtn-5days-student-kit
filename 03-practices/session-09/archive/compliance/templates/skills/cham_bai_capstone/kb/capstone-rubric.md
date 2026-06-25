---
mo-ta: Thang chấm điểm: rubbric đánh giá dự án Capstone cho các nhóm học viên
trang-thai: active
phien-ban: v2.0
created-at: "2026-06-10 16:00 +07:00"
updated-at: "2026-06-15 14:00 +07:00"
---

# Thang chấm điểm: rubbric đánh giá dự án Capstone

Tài liệu này cung cấp khung đánh giá chi tiết và thang điểm chuẩn hóa dành cho hội đồng giám khảo để đánh giá dự án Capstone cuối khóa của các nhóm học viên. Tổng điểm tối đa của phần chấm chính là **100 điểm**, ngoài ra các nhóm có thể nhận thêm tối đa **20 điểm cộng khuyến khích** từ việc triển khai mã nguồn.

---

## 1. Cơ cấu thang điểm tổng quan

Dự án Capstone được đánh giá toàn diện dựa trên 5 khía cạnh cốt lõi của bộ hồ sơ giải pháp (Blueprint) và phần thuyết trình, cùng các điểm cộng khuyến khích cho phần triển khai mã nguồn:

| STT | Khía cạnh đánh giá | Điểm tối đa | Phương thức xác minh |
| :--- | :--- | :---: | :--- |
| **I** | **Phần chấm điểm chính (Main score)** | **100 điểm** | |
| 1 | Biểu mẫu bản thiết kế giải pháp: blueprint | 30 điểm | Đầy đủ thông tin, logic và bám sát nghiệp vụ phòng ban (`01-use-case-one-pager.md` & `04-compliance-checklist.md`) |
| 2 | Luồng logic hợp lý | 20 điểm | Sơ đồ rõ ràng, phân định tự động và chốt chặn con người (`02-logical-workflow.md`) |
| 3 | Lời nhắc bền vững | 20 điểm | System prompt chuẩn, cấu trúc JSON sạch, phòng thủ injection trên lý thuyết (`03-core-prompt-design.md`) |
| 4 | Lộ trình khả thi | 15 điểm | Action plan 30/90 ngày, phân công cụ thể (`05-action-plan-30-90-days.md`) |
| 5 | Slide & Thuyết trình chuyên nghiệp | 15 điểm | Trình bày mạch lạc, slide rõ chữ, trả lời tốt chất vấn cuối khóa |
| **II** | **Phần điểm cộng khuyến khích (Bonus points)** | **Tối đa +20 điểm** | |
| + | Triển khai mã nguồn & Kiểm thử thực tế | Tối đa +10 điểm | Vượt qua 10/10 ca kiểm thử trên mã nguồn, đóng gói Hermes Agent Skill với `skill.json` và `SKILL.md` |
| + | An toàn bảo mật & Logs vận hành | Tối đa +10 điểm | Chặn đứng 3 kịch bản prompt injection trên mã nguồn, nhật ký `execution-log.csv` sạch không lộ PII và cấu hình `.env` an toàn |

---

## 2. Tiêu chí đánh giá chi tiết

### I. Phần chấm điểm chính (Tối đa 100 điểm)

#### Khía cạnh 1: Biểu mẫu bản thiết kế giải pháp: blueprint (Tối đa 30 điểm)
Đánh giá mức độ đầy đủ thông tin, tính logic của bộ tài liệu và mức độ bám sát nghiệp vụ phòng ban qua các tài liệu:
*   **Mức Đạt tối đa (25 - 30 điểm):**
    *   Điền đầy đủ tất cả các hạng mục trong `01-use-case-one-pager.md` và `04-compliance-checklist.md`.
    *   Mô tả cực kỳ rõ ràng vấn đề nghiệp vụ thực tế tại phòng ban, đối tượng sử dụng rõ nét, chỉ ra các KPI đo lường được của ứng dụng AI tại NOC/phòng ban.
    *   Bảng tự kiểm tuân thủ bảo mật điền chi tiết, trung thực và có giải pháp kiểm soát cụ thể cho từng mục.
*   **Mức Đạt yêu cầu (15 - 24 điểm):**
    *   Điền đầy đủ tài liệu nhưng mô tả nghiệp vụ hoặc KPI còn chung chung.
    *   Mẫu checklist tuân thủ có điền nhưng phần giải pháp kiểm soát chưa thực sự chi tiết.
*   **Mức Cần cải thiện (0 - 14 điểm):**
    *   Tài liệu sơ sài, bỏ trống nhiều mục hoặc chỉ copy placeholder mẫu mà không liên hệ nghiệp vụ phòng ban.

#### Khía cạnh 2: Luồng logic hợp lý (Tối đa 20 điểm)
Đánh giá chất lượng sơ đồ quy trình và cơ chế kiểm soát qua tệp `02-logical-workflow.md`:
*   **Mức Đạt tối đa (18 - 20 điểm):**
    *   Sơ đồ thiết kế luồng xử lý chi tiết, rõ ràng, phân định chính xác ranh giới tự động hóa của AI và điểm chốt chặn của con người (Human-in-the-loop).
    *   Định nghĩa rõ vai trò của nhân sự phê duyệt và các kịch bản xử lý khi AI đưa ra kết quả lỗi/ảo giác.
*   **Mức Đạt yêu cầu (10 - 17 điểm):**
    *   Quy trình logic chạy được nhưng thiếu các điểm kiểm soát HITL tại các khâu nhạy cảm hoặc thiếu kịch bản xử lý lỗi chi tiết.
*   **Mức Cần cải thiện (0 - 9 điểm):**
    *   Quy trình quá đơn giản (chỉ có 1 bước gọi AI trực tiếp), không có điểm dừng phê duyệt hoặc giao quyền tự động thực thi quá mức (Excessive Agency).

#### Khía cạnh 3: Lời nhắc bền vững (Tối đa 20 điểm)
Đánh giá thiết kế lời nhắc và các biện pháp phòng vệ lý thuyết qua tệp `03-core-prompt-design.md`:
*   **Mức Đạt tối đa (18 - 20 điểm):**
    *   System prompt được cấu trúc chuẩn hóa, phân tách rõ ràng hướng dẫn hệ thống và dữ liệu người dùng.
    *   Định nghĩa cấu trúc đầu ra JSON sạch, có schema chi tiết.
    *   Thiết kế các biện pháp phòng vệ lý thuyết chống prompt injection (bọc thẻ XML, chỉ dẫn ngăn chặn jailbreak) chặt chẽ.
*   **Mức Đạt yêu cầu (10 - 17 điểm):**
    *   System prompt hoạt động ổn định nhưng cấu trúc chưa tối ưu hoặc thiếu các chỉ dẫn phòng thủ prompt injection chi tiết.
*   **Mức Cần cải thiện (0 - 9 điểm):**
    *   Lời nhắc viết sơ sài, chỉ là các câu lệnh hỏi đáp thông thường, dễ bị hack hoặc không có cấu trúc dữ liệu đầu ra rõ ràng.

#### Khía cạnh 4: Lộ trình khả thi (Tối đa 15 điểm)
Đánh giá tính thực tiễn và kế hoạch triển khai qua tệp `05-action-plan-30-90-days.md`:
*   **Mức Đạt tối đa (13 - 15 điểm):**
    *   Lập lộ trình cụ thể về kỹ thuật, quy trình và con người để áp dụng giải pháp vào thực tế trong vòng 30 đến 90 ngày.
    *   Xác định rõ ràng các tài nguyên và sự phối hợp cần thiết. Đề xuất thêm 3 trường hợp sử dụng mở rộng khả thi.
*   **Mức Đạt yêu cầu (8 - 12 điểm):**
    *   Lộ trình triển khai có đầy đủ các bước nhưng mốc thời gian hoặc phân công nhân sự chưa thực sự thuyết phục.
*   **Mức Cần cải thiện (0 - 7 điểm):**
    *   Lộ trình quá chung chung, không có phân công cụ thể hoặc thiếu tính khả thi trong bối cảnh thực tế của phòng ban.

#### Khía cạnh 5: Slide & Thuyết trình chuyên nghiệp (Tối đa 15 điểm)
Đánh giá kỹ năng báo cáo, slide trình chiếu và phản biện trước hội đồng giám khảo:
*   **Mức Đạt tối đa (13 - 15 điểm):**
    *   Báo cáo mạch lạc, thiết kế slide rõ chữ, chuyên nghiệp (từ 5 đến 7 trang) bám sát dàn ý `10-presentation-outline.md`.
    *   Thuyết trình đúng thời gian quy định. Trả lời xuất sắc, có tính phản tư cao đối với các câu hỏi chất vấn của hội đồng.
*   **Mức Đạt yêu cầu (8 - 12 điểm):**
    *   Trình bày đầy đủ nội dung, slide rõ ràng nhưng kỹ năng thuyết trình chưa thực sự lôi cuốn hoặc bị quá giờ quy định.
    *   Trả lời được hầu hết các câu hỏi chuyên môn nhưng chưa làm nổi bật được giải pháp tối ưu.
*   **Mức Cần cải thiện (0 - 7 điểm):**
    *   Slide sơ sài hoặc quá nhiều chữ, không trả lời được các câu hỏi cơ bản về thiết kế giải pháp của nhóm.

---

### II. Phần điểm cộng khuyến khích (Tối đa +20 điểm cộng thêm)

#### Cộng điểm 1: Triển khai mã nguồn & Kiểm thử thực tế (Tối đa +10 điểm)
*   **Cộng 9 - 10 điểm:**
    *   Triển khai mã nguồn hoàn chỉnh, vượt qua 10/10 ca kiểm thử mặc định (PASS) bao phủ đầy đủ các nhóm tình huống.
    *   Đóng gói mã nguồn sạch sẽ, tích hợp đúng chuẩn Hermes Agent Skill với đầy đủ `skill.json` và `SKILL.md` mô tả kỹ năng.
    *   Thực hiện demo sản phẩm chạy thực tế mượt mà, làm chủ các tình huống kỹ thuật.
*   **Cộng 5 - 8 điểm:**
    *   Mã nguồn chạy được, vượt qua từ 7 đến 9 ca kiểm thử.
    *   Có đóng gói Agent Skill nhưng tài liệu mô tả kỹ năng còn thiếu sót nhỏ.
*   **Cộng 1 - 4 điểm:**
    *   Mã nguồn chỉ chạy được một số tính năng cơ bản, vượt dưới 7 ca kiểm thử hoặc không đóng gói đúng chuẩn Agent Skill.

#### Cộng điểm 2: An toàn bảo mật & Logs vận hành thực tế (Tối đa +10 điểm)
*   **Cộng 9 - 10 điểm:**
    *   Chặn đứng hoàn toàn 3 kịch bản tấn công prompt injection thực tế (Jailbreak, Data exfiltration, Role confusion).
    *   Tệp nhật ký `execution-log.csv` ghi nhận đầy đủ lịch sử hoạt động nhưng hoàn toàn không lưu trữ dữ liệu nhạy cảm gốc (đã redact PII thành công).
    *   Bảo mật API key an toàn trong `.env`, không để lộ trong mã nguồn hoặc đẩy lên Git.
*   **Cộng 5 - 8 điểm:**
    *   Chặn được 1 hoặc 2 kịch bản tấn công prompt injection.
    *   Logs không lộ dữ liệu nhạy cảm gốc nhưng định dạng hoặc nội dung ghi chưa thực sự đầy đủ.
*   **Cộng 1 - 4 điểm:**
    *   Không chặn được kịch bản tấn công nào hoặc để lộ thông tin nhạy cảm trong logs hoặc lộ API key trong mã nguồn.

---

## 3. Hướng dẫn dành cho hội đồng chấm điểm

> [!TIP]
> **Nguyên tắc chấm điểm:**
> 1.  **Trọng tâm vào thiết kế:** Đánh giá cao tư duy thiết kế hệ thống, khả năng tích hợp chốt chặn con người (HITL) và sự hiểu biết nghiệp vụ phòng ban thể hiện qua bộ hồ sơ Blueprint.
> 2.  **Khuyến khích thực chiến:** Sử dụng phần điểm cộng (+20 điểm) để ghi nhận xứng đáng nỗ lực lập trình, kiểm thử và bảo mật thực tế của các nhóm có kỹ năng lập trình tốt.
> 3.  **Tư duy phản biện:** Đánh giá cao các nhóm hiểu rõ giới hạn của giải pháp hiện tại và chủ động đề xuất phương án xử lý rủi ro trong tài liệu `07-failure-modes-rollback.md` hoặc `09-handoff-contract.md`.
