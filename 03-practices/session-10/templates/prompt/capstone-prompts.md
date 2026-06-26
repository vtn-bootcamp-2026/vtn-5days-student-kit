---
mo-ta: "Danh sách bộ prompt step-by-step phục vụ tự động hóa tài liệu Capstone — Session 10"
trang-thai: active
phien-ban: v2.0
created-at: 2026-06-26 10:00 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Bộ prompt tự động hóa hồ sơ Capstone — Viettel Networks

Tài liệu này cung cấp danh sách các prompt được thiết kế sẵn giúp các nhóm học viên tự động hóa việc soạn thảo bộ hồ sơ Capstone Blueprint và bộ tài liệu kỹ thuật phụ trợ. Học viên chỉ cần điền thông tin mô tả cơ bản của dự án vào prompt đầu tiên, sau đó chạy các prompt tiếp theo để hoàn thành nhanh chóng toàn bộ 10 tài liệu.

> 💡 **Quy tắc thực hành cốt lõi:**
> - Hãy mở một phiên chat mới trong **Antigravity** (hoặc các giao diện chat của LLM như Gemini, ChatGPT) tại thư mục dự án của nhóm.
> - Thực hiện tuần tự các prompt trên **cùng một phiên chat (conversation context)** để mô hình AI ghi nhớ các thông tin đặc thù của dự án từ các bước trước đó.
> - Sau mỗi phản hồi của AI, hãy sao chép nội dung được sinh ra vào đúng tệp tin template tương ứng trong thư mục `03-practice/session-10/templates/`.

## Danh sách các bước chạy prompt:

1. **[Prompt 1: Khảo sát & Khởi tạo dự án một trang (Use Case One Pager)](prompt-1-use-case.md)**
   - *Mục tiêu:* Điền tự động tệp `01-use-case-one-pager.md`.
2. **[Prompt 2: Thiết kế sơ đồ khối luồng xử lý và Con người kiểm duyệt (Logical Workflow)](prompt-2-workflow.md)**
   - *Mục tiêu:* Điền tự động tệp `02-logical-workflow.md` (bao gồm sơ đồ Mermaid).
3. **[Prompt 3: Thiết kế cấu trúc IPO của Skill (Generate skill_design.md)](prompt-3-skill-design.md)**
   - *Mục tiêu:* Sinh tự động tệp thiết kế kiến trúc skill `skill_design.md` theo mô hình Input-Process-Output.
4. **[Prompt 4: Xây dựng và đóng gói gói kỹ năng (Build Skill using vibe-aiworkforce)](prompt-4-build-skill.md)**
   - *Mục tiêu:* Hướng dẫn sử dụng subagent `vibe-aiworkforce` tự động sinh mã nguồn và thư mục skill.
5. **[Prompt 5: Cải tiến an toàn thông tin & chống Prompt Injection (PII Protection & Anti-injection)](prompt-5-security-improve.md)**
   - *Mục tiêu:* Nâng cấp mã nguồn của skill để bổ sung lớp anonymizer che giấu PII và chặn đứng các kịch bản Prompt Injection.
6. **[Prompt 6: Nhật ký kiểm thử & Đặc tả ca kiểm thử (Core Prompt Design & Playground Logs)](prompt-6-prompt-design.md)**
   - *Mục tiêu:* Điền tự động tệp `03-core-prompt-design.md` (System Prompt và Nhật ký kiểm thử Playground).
7. **[Prompt 7: Đánh giá & Rà soát tuân thủ an toàn thông tin (Compliance Checklist)](prompt-7-compliance.md)**
   - *Mục tiêu:* Điền tự động tệp `04-compliance-checklist.md`.
8. **[Prompt 8: Xây dựng Kế hoạch 30-90 ngày & Đề xuất 3 Use Cases mở rộng (Action Plan)](prompt-8-action-plan.md)**
   - *Mục tiêu:* Điền tự động tệp `05-action-plan-30-90-days.md`.
9. **[Prompt 9: Đóng gói hồ sơ vận hành & Bàn giao kỹ thuật (Implementation Kit Docs)](prompt-9-technical-docs.md)**
   - *Mục tiêu:* Điền đồng thời 4 tệp tin kỹ thuật bổ sung:
     - `06-test-cases-specification.md` (10 ca kiểm thử)
     - `07-failure-modes-rollback.md` (Phương án xử lý lỗi)
     - `08-runbook-template.md` (Tài liệu vận hành Runbook)
     - `09-handoff-contract.md` (Biên bản bàn giao)
10. **[Prompt 10: Tự động hóa soạn dàn ý Slide thuyết trình báo cáo (Presentation Outline)](prompt-10-presentation.md)**
   - *Mục tiêu:* Điền tự động tệp `10-presentation-outline.md`.
