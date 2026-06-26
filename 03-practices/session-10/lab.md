---
mo-ta: "Hướng dẫn thực hành Session 10: Capstone — từ bài toán đến Implementation Kit - hoàn thiện sản phẩm nhóm, đóng gói hồ sơ Capstone Blueprint và bảo vệ cuối khóa"
trang-thai: active
phien-ban: v3.1
created-at: "2026-05-17 13:37 +07:00"
updated-at: "2026-06-26 10:25 +07:00"
---

# Hướng dẫn thực hành Session 10: Capstone — từ bài toán đến Implementation Kit

## 1. Mục tiêu bài thực hành

Kết thúc bài Capstone này, học viên sẽ có thể:
*   Tích hợp và hoàn thiện luồng sản phẩm kỹ thuật nhóm (luồng n8n, Agent Skill, RAG, bộ lọc an toàn) hoạt động ổn định toàn trình (end-to-end).
*   Đóng gói bộ hồ sơ thiết kế giải pháp (**Capstone Blueprint**) gồm 5 tài liệu cốt lõi phục vụ bảo vệ cuối khóa.
*   Soạn thảo Slide thuyết trình báo cáo Capstone đúng cấu trúc chuẩn để trình bày trước hội đồng nghiệm thu.
*   Demo sản phẩm chạy live thực tế và tham gia phản biện trước lớp.

---

## 2. Bối cảnh tình huống

Hãy tưởng tượng bạn là kỹ sư AI thực chiến hoặc cán bộ nghiệp vụ tại Viettel Networks. Nhóm của bạn đã trải qua chặng đường từ việc chọn bài toán (S1), thiết kế workflow (S2), dựng luồng tự động hóa n8n (S3, S4), đóng gói Agent/Skill (S5), xây dựng tri thức RAG (S6, S7), cấu hình Local Assistant (S8) cho tới thiết lập các chốt chặn bảo mật (S9). Hôm nay, nhóm sẽ hội tụ tất cả các cấu phần này lại, đóng gói hồ sơ Implementation Kit hoàn chỉnh để sẵn sàng trình Ban Giám đốc phê duyệt thí điểm thực tế tại đơn vị.

---

## 3. Phân định hồ sơ: Capstone Blueprint (5) vs Implementation Kit (7)

Để tối ưu hóa thời gian thực hành và phân định rõ vai trò, bộ tài liệu triển khai được định nghĩa theo công thức chuẩn hóa sau:

$$\text{Implementation Kit (7 hồ sơ)} = \text{Capstone Blueprint (5 hồ sơ)} + \text{Runbook} + \text{Handoff Contract}$$

### A. Bộ 5 hồ sơ Capstone Blueprint (Học viên thực hiện bắt buộc)
Học viên hoàn thiện 5 biểu mẫu nghiệp vụ và tư duy thiết kế cốt lõi này để phục vụ slide trình bày bảo vệ cuối khóa:

| STT | Tài liệu Blueprint của Học viên | Mục đích |
| :--- | :--- | :--- |
| 1 | [01-use-case-one-pager.md](templates/01-use-case-one-pager.md) | Đề xuất dự án ứng dụng AI trên 1 trang giấy |
| 2 | [02-logical-workflow.md](templates/02-logical-workflow.md) | Sơ đồ luồng logic, phân vai AI và điểm Human-in-the-loop |
| 3 | [03-core-prompt-design.md](templates/03-core-prompt-design.md) | Đặc tả lời nhắc cốt lõi và nhật ký chạy thử nghiệm trên Web UI |
| 4 | [04-compliance-checklist.md](templates/04-compliance-checklist.md) | Bảng tự kiểm tra tuân thủ bảo mật thông tin nội bộ |
| 5 | [05-action-plan-30-90-days.md](templates/05-action-plan-30-90-days.md) | Lộ trình áp dụng thực tế và đề xuất 3 use cases tiếp theo |
| 10 | [10-presentation-outline.md](templates/10-presentation-outline.md) | Dàn ý Slide thuyết trình báo cáo bảo vệ Capstone |

### B. Bộ 7 hồ sơ Implementation Kit hoàn chỉnh (Giảng viên Demo & Cung cấp mẫu)
Giảng viên thực hành giải thích, demo trực tiếp và cung cấp sẵn bộ hồ sơ vận hành hoàn chỉnh này (gồm 5 tài liệu Capstone Blueprint của học viên cộng thêm 2 tài liệu kỹ thuật chuyên sâu) để học viên nắm vững quy trình bàn giao thực tế trong doanh nghiệp:

| STT | Tài liệu Implementation Kit của Giảng viên | Mô tả |
| :--- | :--- | :--- |
| 1-5 | **Bộ 5 hồ sơ Capstone Blueprint** | (Use Case One Pager, Logical Workflow, Core Prompt Design, Compliance Checklist, Action Plan) |
| 6 | [08-runbook-template.md](templates/08-runbook-template.md) | **Runbook:** Đặc tả cấu hình phần cứng, lệnh cài đặt và lệnh chạy CLI 1 dòng |
| 7 | [09-handoff-contract.md](templates/09-handoff-contract.md) | **Handoff Contract:** Biên bản bàn giao sản phẩm kỹ thuật, phân tích Failure Modes & kịch bản Rollback |

---

## 4. Phân bổ thời gian thực tế (Tổng cộng 210 phút - 3h30)

Để đảm bảo chất lượng tiếp thu và tiến độ bảo vệ của cả **6 nhóm** trước lớp, thời lượng của Session 10 được chia như sau:

*   **15 phút đầu: Khởi động & Nhắc nhở tiêu chí nghiệm thu**
    *   Giảng viên định hướng, chốt yêu cầu kỹ thuật và công bố rubric chấm điểm Capstone.
*   **60 phút tiếp theo: Học viên Đóng gói hồ sơ & Làm Slide Capstone (Phần A, B, C)**
    *   Các nhóm làm việc tập trung hoàn thiện sản phẩm kỹ thuật, chạy 10 bước prompt tự động hóa để điền hồ sơ Capstone và chuẩn bị Slide thuyết trình kèm demo.
*   **120 phút tiếp theo: Thuyết trình bảo vệ trước lớp & Phản biện hội đồng (Phần D)**
    *   6 nhóm lần lượt thuyết trình bảo vệ (mỗi nhóm tối đa 15-20 phút bao gồm cả Q&A và phản biện) và tổng kết khóa học.
*   **15 phút cuối: Bế mạc & Công bố kết quả**
    *   Hội đồng giảng viên đánh giá, công bố điểm Capstone và bế mạc bootcamp.

| Phần | Nội dung thực hiện | Thời gian | Vai trò |
|------|-----------|-----------|:--- |
| **Khởi động** | Công bố tiêu chí nghiệm thu và rubric đánh giá | **15 phút** | Giảng viên hướng dẫn |
| **Part A** | Thiết kế & Khởi tạo dự án (Prompt 1 & 2) | **15 phút** | Nhóm học viên tự thực hiện |
| **Part B** | Thiết kế & Xây dựng gói kỹ năng (Prompt 3, 4 & 5) | **25 phút** | Nhóm học viên tự thực hiện |
| **Part C** | Hoàn thiện hồ sơ tuân thủ & Kiểm thử (Prompt 6, 7, 8 & 9) | **20 phút** | Nhóm học viên tự thực hiện |
| **Part D** | Soạn Slide & Thuyết trình bảo vệ (Prompt 10) | **120 phút** | Học viên thực hiện & Hội đồng chấm điểm |
| **Bế mạc** | Tổng kết, nhận xét chung và công bố điểm số | **15 phút** | Giảng viên & Ban tổ chức |

---

## 5. Các bước thực hiện chi tiết

### Phần A: Thiết kế & Khởi tạo dự án (15 phút)

> [!NOTE]
> **Mục tiêu**: Định hình bài toán thực tế của nhóm, xây dựng các biểu mẫu ban đầu và thiết kế sơ đồ luồng logic của giải pháp.

1. **Bước 1: Khảo sát & Khởi tạo dự án một trang (Use Case One Pager)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-1-use-case.md](templates/prompt/prompt-1-use-case.md).
   - Sao chép prompt mẫu, thay thế các thông tin nghiệp vụ thực tế của nhóm tại mục `DỮ LIỆU ĐẦU VÀO CỦA NHÓM`.
   - Gửi cho trợ lý ảo (Antigravity hoặc các công cụ LLM như ChatGPT, Gemini) để sinh nội dung cho tệp `01-use-case-one-pager.md`.
   - Sao chép kết quả và dán vào tệp [templates/01-use-case-one-pager.md](templates/01-use-case-one-pager.md).
2. **Bước 2: Thiết kế sơ đồ khối luồng xử lý và Con người kiểm duyệt (Logical Workflow)**:
   - Tiếp tục trên cùng phiên chat, học viên mở tệp chỉ dẫn [templates/prompt/prompt-2-workflow.md](templates/prompt/prompt-2-workflow.md).
   - Gửi prompt mẫu cho AI để sinh sơ đồ luồng logic dạng mã Mermaid và đặc tả chi tiết các bước xử lý cũng như ranh giới Human-in-the-loop (HITL).
   - Sao chép kết quả và dán vào tệp [templates/02-logical-workflow.md](templates/02-logical-workflow.md).

---

### Phần B: Thiết kế & Xây dựng gói kỹ năng (25 phút)

> [!NOTE]
> **Mục tiêu**: Chuyển đổi thiết kế nghiệp vụ thành cấu trúc kỹ thuật (gói kỹ năng) và xây dựng mã nguồn tự động, sau đó tích hợp các giải pháp bảo mật dữ liệu.

3. **Bước 3: Thiết kế cấu trúc IPO của Skill (Generate skill_design.md)**:
   - Trên cùng phiên chat, học viên mở tệp chỉ dẫn [templates/prompt/prompt-3-skill-design.md](templates/prompt/prompt-3-skill-design.md).
   - Gửi prompt cho AI để tự động tạo bản đặc tả kỹ thuật `skill_design.md` theo cấu trúc IPO (Input-Process-Output) chuẩn của Session 5.
   - Sao chép và lưu kết quả vào tệp `skill_design.md` trong thư mục làm việc của nhóm.
4. **Bước 4: Xây dựng và đóng gói gói kỹ năng (Build Skill using vibe-aiworkforce)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-4-build-skill.md](templates/prompt/prompt-4-build-skill.md).
   - Gửi chỉ thị cho trợ lý AI Antigravity để gọi subagent `vibe-aiworkforce` tự động sinh toàn bộ khung thư mục skill (gồm `SKILL.md`, `skill.json`, `schemas/`, `kb/`, `scripts/`).
   - Đảm bảo các script python trong thư mục `scripts/` (như `intake.py`, `validator.py`, `router.py`) đã được sinh đầy đủ.
5. **Bước 5: Cải tiến an toàn thông tin & chống Prompt Injection (PII Protection & Anti-injection)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-5-security-improve.md](templates/prompt/prompt-5-security-improve.md).
   - Gửi prompt cho AI để nâng cấp các script trong thư mục `scripts/` (ví dụ `anonymizer.py` hoặc logic xử lý cốt lõi của skill) nhằm tích hợp bộ lọc ẩn danh PII (Regex + Local LLM) và bộ lọc bảo vệ chống Prompt Injection bằng thẻ XML `<user_data>`.

---

### Phần C: Hoàn thiện hồ sơ tuân thủ & Kiểm thử (20 phút)

> [!NOTE]
> **Mục tiêu**: Hoàn tất tài liệu đặc tả prompts cốt lõi, rà soát tuân thủ an toàn thông tin của dự án và đóng gói các hồ sơ vận hành kỹ thuật.

6. **Bước 6: Đặc tả Prompt hệ thống & Nhật ký kiểm thử Playground (Core Prompt Design)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-6-prompt-design.md](templates/prompt/prompt-6-prompt-design.md).
   - Gửi prompt cho AI để đặc tả System Prompt bảo mật, cấu trúc Output JSON Schema và sinh nhật ký 3 ca kiểm thử Playground (happy path, edge case, prompt injection).
   - Sao chép và lưu kết quả vào tệp [templates/03-core-prompt-design.md](templates/03-core-prompt-design.md).
7. **Bước 7: Đánh giá & Rà soát tuân thủ an toàn thông tin (Compliance Checklist)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-7-compliance.md](templates/prompt/prompt-7-compliance.md).
   - Gửi prompt cho AI để tự động đánh giá tuân thủ 8 tiêu chí an toàn bảo mật dữ liệu của Viettel Net (đánh dấu hoàn thành `[x]` và mô tả giải pháp kỹ thuật đã triển khai thực tế).
   - Sao chép và lưu kết quả vào tệp [templates/04-compliance-checklist.md](templates/04-compliance-checklist.md).
8. **Bước 8: Xây dựng Kế hoạch 30-90 ngày & Đề xuất 3 Use Cases mở rộng (Action Plan)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-8-action-plan.md](templates/prompt/prompt-8-action-plan.md).
   - Gửi prompt cho AI để soạn thảo lộ trình áp dụng 30-90 ngày chi tiết tại đơn vị và đề xuất 3 use cases tiếp theo.
   - Sao chép và lưu kết quả vào tệp [templates/05-action-plan-30-90-days.md](templates/05-action-plan-30-90-days.md).
9. **Bước 9: Đóng gói hồ sơ vận hành & Bàn giao kỹ thuật (Implementation Kit Docs)**:
   - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-9-technical-docs.md](templates/prompt/prompt-9-technical-docs.md).
   - Gửi prompt cho AI để đồng thời tạo ra bộ 4 tài liệu kỹ thuật phụ trợ bao gồm: Đặc tả 10 ca kiểm thử (`06-test-cases-specification.md`), Phân tích lỗi & Rollback (`07-failure-modes-rollback.md`), Hướng dẫn vận hành Runbook (`08-runbook-template.md`), và Biên bản bàn giao (`09-handoff-contract.md`).
   - Sao chép nội dung sinh ra vào 4 file template tương ứng trong thư mục `templates/`.

---

### Phần D: Soạn Slide thuyết trình & Đóng gói nộp bài (20 phút làm Slide + 120 phút Thuyết trình)

> [!NOTE]
> **Mục tiêu**: Đóng gói sản phẩm cuối cùng và slide trình bày để thuyết trình trước lớp.

10. **Bước 10: Tự động hóa soạn dàn ý Slide thuyết trình báo cáo (Presentation Outline)**:
    - Học viên mở tệp chỉ dẫn [templates/prompt/prompt-10-presentation.md](templates/prompt/prompt-10-presentation.md).
    - Gửi prompt cho AI để tổng hợp toàn bộ hồ sơ của nhóm thành dàn ý slide báo cáo 6 trang chuẩn hóa.
    - Sao chép kết quả và dán vào tệp [templates/10-presentation-outline.md](templates/10-presentation-outline.md).
11. **Chạy kiểm định và đóng gói nộp bài tự động**:
    - Học viên mở và chạy tệp Jupyter Notebook kiểm định **`templates/checkpoints/checkpoint-step-d2.ipynb`**.
    - Tệp này sẽ quét và tự động kiểm tra xem nhóm đã điền đầy đủ và đúng định dạng 10 tài liệu trong thư mục `templates/` chưa.
    - Sau khi xác nhận thành công, checkpoint sẽ tự động nén toàn bộ mã nguồn, tài liệu và slide thành file **`session-10-capstone-handover-[TenNhom].zip`**.
    - Học viên nộp file zip này lên hệ thống theo hướng dẫn của ban tổ chức.

---

## 6. Tiêu chí nghiệm thu tối thiểu (Definition of Done)

Dự án Capstone của nhóm được đánh giá **Đạt** khi thỏa mãn đầy đủ các tiêu chí:
*   [ ] **Sản phẩm chạy E2E ổn định**: Luồng n8n / Agent Skill hoạt động tốt trên các dữ liệu thử nghiệm của nhóm mà không bị crash.
*   [ ] **Hoàn thành 10/10 tài liệu**: 10 file markdown trong thư mục `templates/` được điền đầy đủ và đúng định dạng.
*   [ ] **Đóng gói nộp bài thành công**: Tạo ra tệp `session-10-capstone-handover-[TenNhom].zip` thông qua công cụ kiểm định tự động.
*   [ ] **Slide thuyết trình chuẩn chỉnh**: Hoàn thành slide báo cáo theo dàn ý và đúng thời gian chuẩn bị.
*   [ ] **Thuyết trình bảo vệ thành công**: Trình bày rõ ràng bài toán, chạy demo live thành công và phản biện tốt các câu hỏi của hội đồng nghiệm thu.
