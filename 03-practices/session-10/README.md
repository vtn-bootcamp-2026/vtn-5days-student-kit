---
mo-ta: "Tổng quan bài thực hành Session 10 - hoàn thiện dự án Capstone và đóng gói hồ sơ"
trang-thai: active
phien-ban: v3.0
created-at: "2026-05-17 13:37 +07:00"
updated-at: "2026-06-26 10:00 +07:00"
---

# Session 10: Capstone — từ bài toán đến Implementation Kit

## Mục tiêu

Buổi Capstone kéo dài 3 giờ 30 phút, giúp các nhóm hoàn thiện sản phẩm end-to-end (từ ý tưởng sơ bộ ở các session trước thành giải pháp hoàn chỉnh) thông qua việc đóng gói bộ hồ sơ thiết kế giải pháp (**Capstone Blueprint** / **Implementation Kit**) và thực hiện thuyết trình bảo vệ, phản biện trước hội đồng nghiệm thu.

## Cấu trúc bài thực hành

| Phần | Hoạt động | Hình thức | Đầu ra |
| --- | --- | --- | --- |
| A | Hoàn thiện & Tích hợp sản phẩm kỹ thuật nhóm | Thực hành nhóm | Luồng n8n / Agent Skill / RAG hoàn chỉnh |
| B | Đóng gói bộ 5 hồ sơ Capstone Blueprint | Thực hành nhóm | Bộ 5 tài liệu Blueprint hoàn chỉnh |
| C | Chuẩn bị Slide báo cáo Capstone & Demo | Thực hành nhóm | Slide thuyết trình + Demo chạy thực tế |
| D | Thuyết trình bảo vệ trước lớp & Phản biện | Nghiệm thu nhóm | Slide thuyết trình + Phản biện hội đồng |

## Đầu vào

- **Từ các session trước (S1–S9)**:
  - Bản thảo Use case one-pager, Workflow design doc (Mermaid, ESIA)
  - Luồng n8n tự động hóa, Agent Skill đã đóng gói (vibe-aiworkforce)
  - Dữ liệu tri thức (Knowledge Base) và RAG tích hợp
  - Công cụ ẩn danh hóa dữ liệu (Anonymizer) và Hook bảo mật
- Các biểu mẫu mẫu tại thư mục [templates/](templates/)

## Đầu ra

Mỗi nhóm nộp gói sản phẩm **`session-10-capstone-handover-[TenNhom].zip`** chứa:
1. Mã nguồn sản phẩm kỹ thuật (file `.zip` chứa luồng n8n, Agent Skill, mã anonymizer/hook).
2. Bộ 5 hồ sơ Capstone Blueprint đã điền đầy đủ thông tin.
3. Slide thuyết trình báo cáo Capstone.

## SLI/SLO kiểm soát chất lượng

| SLI | Đo lường | SLO (Target) | Measurement |
|-----|----------|-------------|-------------|
| Capstone Blueprint completeness | 5/5 tài liệu Capstone Blueprint hoàn chỉnh | 5/5 (100%) | Đăng kiểm qua validator checkpoint |
| Technical E2E validation | Luồng chạy trơn tru, không gặp lỗi hệ thống | 100% PASS | Demo trực tiếp trước hội đồng |
| Security compliance | Không rò rỉ dữ liệu nhạy cảm thực tế | 100% tuân thủ | Compliance checklist và log audit |
| Presentation delivery | Thuyết trình và phản biện đúng hạn | Đúng thời gian quy định | Hội đồng đánh giá và chấm điểm |

## Kiến trúc nghiệm thu bài toán Capstone

```text
+-------------------------------------------------------------------+
|               TẦNG TRẢI NGHIỆM & ĐẦU VÀO                          |
|       [ Use case one-pager ]       [ Dữ liệu thực tế nhóm ]       |
+-------------------------------------------------------------------+
                                  |
+-------------------------------------------------------------------+
|            TẦNG CORE AI WORKFLOW & AGENTIC RAG                    |
|    * Luồng tự động hóa n8n       * Tác tử AI Agent (Hermes/Cloud) |
|    * Tri thức RAG tích hợp       * Bộ lọc Anonymizer & Hook       |
+-------------------------------------------------------------------+
                                  |
+-------------------------------------------------------------------+
|            TẦNG HỒ SƠ BÀN GIAO (IMPLEMENTATION KIT)               |
|    * Runbook cài đặt             * Phân tích Failure Modes        |
|    * Action Plan 30/90 ngày      * Biên bản bàn giao kỹ thuật     |
+-------------------------------------------------------------------+
```

## Vai trò của ảnh thị phạm

Thư mục `outputs/screenshots/` lưu ảnh chụp demo sản phẩm. Tuyệt đối không commit ảnh chứa thông tin nhạy cảm, email thật, API key, token.

## Tiêu chí hoàn thành

- [ ] Hoàn thiện tích hợp luồng sản phẩm AI chạy ổn định.
- [ ] Điền đầy đủ bộ 5 tài liệu Capstone Blueprint.
- [ ] Chuẩn bị slide báo cáo Capstone đúng cấu trúc.
- [ ] Thực hiện demo chạy trực tế và thuyết trình trước hội đồng.
- [ ] Đóng gói và nộp bài đúng hạn cấu trúc quy định.

## Quan hệ với session khác

Session 10 là chặng cuối (Capstone) của toàn bộ chương trình bootcamp. Nó kết hợp toàn bộ thành quả từ việc chọn bài toán (S1), thiết kế workflow (S2), cài đặt n8n (S3, S4), đóng gói Agent/Skill (S5), xây dựng RAG (S6, S7), cấu hình Local Assistant (S8) và bảo mật dữ liệu (S9) thành một gói giải pháp sẵn sàng trình Ban Giám đốc phê duyệt thí điểm.
