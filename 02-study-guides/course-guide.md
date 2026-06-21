---
mo-ta: huong dan tong quan va cam nang hoc tap cho hoc vien
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-05-29 20:07 +07:00
---

# Cẩm nang học tập dành cho học viên: course guide

Chào mừng các anh/chị học viên đến với khóa học **AI thực chiến cho nhân sự nòng cốt - Viettel Net**. 

Tài liệu này cung cấp đầy đủ thông tin về lộ trình học tập, yêu cầu thực hành và quy chế đánh giá tốt nghiệp cuối khóa.

---

## 1. Lộ trình học tập & Dòng chảy bàn giao sản phẩm

Khóa học kéo dài **3 ngày (6 buổi, tổng cộng 24 giờ học thực chiến)**. Sản phẩm của buổi học trước sẽ là nguyên liệu trực tiếp để phát triển nâng cao trong buổi học sau.

| Ngày | Buổi | Chủ đề chính | Sản phẩm bàn giao (Đầu ra bắt buộc) |
|---|---|---|---|
| **Ngày 1** | Buổi 1 | Lựa chọn bài toán và tuân thủ AI sơ bộ | Danh sách 3-5 quy trình ưu tiên, bảng chấm điểm lựa chọn bài toán và checklist tuân thủ an toàn dữ liệu sơ bộ. |
| **Ngày 1** | Buổi 2 | Thiết kế quy trình làm việc AI: AI Workflow | Sơ đồ luồng tự động hóa (n8n workflow) có xử lý lỗi (error handling), ghi nhật ký vận hành (logging) và điểm Human-in-the-loop. |
| **Ngày 2** | Buổi 3 | Thiết kế tác nhân AI chuyên sâu: AI Agent | Cấu phần tác nhân AI (Contract Term Extractor) chạy thực tế, có đầu ra định dạng chuẩn JSON và cơ chế tự kiểm lời nhắc (prompt self-check). |
| **Ngày 2** | Buổi 4 | Xây dựng kho tri thức doanh nghiệp: RAG | Quy trình RAG (HR Policy Q&A) chạy end-to-end, trích xuất thông tin chính xác từ kho tri thức và có trích dẫn nguồn (citation). |
| **Ngày 3** | Buổi 5 | Vibe coding & Ẩn danh hóa dữ liệu local | Mã nguồn công cụ nhỏ (Local AI Data Anonymizer) hoàn chỉnh chạy local bằng mô hình Ollama an toàn dữ liệu. |
| **Ngày 3** | Buổi 6 | Đóng gói triển khai & Bảo vệ Capstone | **Bộ đóng gói triển khai (Implementation Kit)** hoàn chỉnh và trình bày bảo vệ dự án tốt nghiệp trước giảng viên. |

---

## 2. Yêu cầu sản phẩm tốt nghiệp: Capstone Implementation Kit

Vào Buổi 6, mỗi nhóm học viên bắt buộc phải nộp và trình bày **Bộ đóng gói triển khai (Implementation Kit)** hoàn chỉnh của dự án nhóm. Bộ kit này bao gồm **7 hồ sơ cốt lõi** được chuẩn hóa:

1. **Use Case One-Pager:** Bản mô tả dự án trên 1 trang giấy (mẫu biểu chuẩn).
2. **Capstone Blueprint (5 hồ sơ con):**
   - *Sơ đồ luồng logic (Logical Workflow):* Bản vẽ kỹ thuật quy trình.
   - *Đặc tả lời nhắc cốt lõi (Core Prompt Design):* Chi tiết prompt của Agent, persona và self-check.
   - *Thiết kế cơ sở tri thức (KB Schema):* Cách cấu trúc và chia nhỏ tài liệu (chunking).
   - *Kịch bản kiểm thử (Test Cases):* Danh sách 10+ trường hợp thử nghiệm.
   - *Phân tích rủi ro (Failure Modes & Effects Analysis):* Các tình huống lỗi và cách xử lý.
3. **Runbook:** Hướng dẫn từng bước cách triển khai, cấu hình và vận hành hệ thống.
4. **Handoff Contract:** Hợp đồng bàn giao và cam kết duy trì chất lượng hệ thống.

---

## 3. Quy chế đánh giá & Nghiệm thu dự án Capstone

Dự án Capstone của các nhóm sẽ được **đánh giá độc lập bởi đội ngũ giảng viên** dựa trên Thang chấm điểm chuẩn hóa **(Scoring Rubric 100 điểm)** nhằm bảo đảm tính khách quan và chuyên môn kỹ thuật cao nhất.

### 3.1 Tiêu chí chấm điểm cốt lõi (Core Rubrics)
- **Tính thực tiễn & Giá trị ứng dụng (20%):** Bài toán lựa chọn có giải quyết được điểm nghẽn thực tế tại đơn vị Viettel Net không?
- **Kiến trúc luồng AI Workflow (20%):** Thiết kế luồng xử lý tự động hóa có hoàn thiện không? Có cơ chế bắt lỗi (error branch) và điểm phê duyệt của con người (Human-in-the-loop) để bảo đảm an toàn vận hành không?
- **Kỹ nghệ Prompt & Tính năng tự kiểm (20%):** Prompt thiết kế cho Agent có rõ ràng, có ranh giới hành vi và có cơ chế bắt buộc Agent tự kiểm tra kết quả trước khi trả về không?
- **Tính tuân thủ & Bảo mật dữ liệu (20%):** Hệ thống có được rà soát an toàn thông tin (anonymization) không? Có cơ chế phòng thủ tấn công prompt injection không?
- **Mức độ hoàn thiện của sản phẩm chạy thử (20%):** Demo hoạt động trơn tru trên dữ liệu mô phỏng, chứng minh được khả năng vận hành thực tế.

### 3.2 Lộ trình sau khóa học dành cho các dự án xuất sắc
- **Chọn lọc TOP 3:** Đội ngũ giảng viên sẽ đánh giá và lựa chọn **3 dự án xuất sắc nhất** có tiềm năng thực chiến cao nhất.
- **Báo cáo đề xuất thí điểm:** Giảng viên sẽ viết báo cáo đánh giá kỹ thuật và trực tiếp đề xuất lên Ban Giám đốc Viettel Net để đưa 3 dự án này vào chương trình chạy thử nghiệm thực tế (Pilot Sandbox) trong kế hoạch hành động 30 và 90 ngày sau đào tạo.
- **Hỗ trợ kỹ thuật sau khóa học:** Các dự án lọt vào danh sách thí điểm sẽ tiếp tục nhận được sự cố vấn và hỗ trợ kỹ thuật từ đội ngũ giảng viên và trợ giảng để hoàn thiện đưa vào sản xuất (production).

