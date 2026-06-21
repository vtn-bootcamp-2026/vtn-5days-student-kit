# Session 2 — Xây dựng workflow: hiện trạng + ESIA + Mermaid + render ảnh

> **Ngày 1 · Tư duy lõi:** Workflow Thinking — 'Thiết kế quy trình trước khi tự động'
> **Chữ kí:** _Tự động hóa một quy trình sai chỉ làm sai diễn ra nhanh hơn. Vẽ hiện trạng, dùng ESIA để gọt, rồi mới thiết kế workflow mới._

- **Giảng viên:** Lộc · **Trợ giảng:** Hằng
- **Phong cách:** offline/bootcamp · 3h30 · 4 module

## 4 Module

| # | Tên hợp phần | Lý thuyết (JIT) | Thực hành | Công cụ |
|---|---|---|---|---|
| M1 | Vẽ hiện trạng (as-is) | Tự động hóa quy trình sai chỉ làm sai nhanh hơn. Vẽ hiện trạng TRƯỚC khi đề xuất cái mới; … | Vẽ hiện trạng quy trình đã chọn ở S1 (các bước, người thực hiện, công cụ, điểm nghẽn, lỗi … | Antigravity / Mermaid |
| M2 | ESIA — đề xuất quy trình mới | Khung ESIA: Eliminate (bỏ) · Simplify (đơn giản hóa) · Integrate (gộp/kết nối) · Automate … | Áp ESIA lên hiện trạng; đánh dấu mỗi bước E/S/I/A; chốt quy trình mới (to-be).… | Antigravity |
| M3 | 3 kiểu workflow + Mermaid | 3 kiểu: tuyến tính (A→B→C), song song (A→B+C+D), có điều kiện (if X then Y). Mermaid = ngô… | Nhận diện kiểu workflow cho to-be; dùng AI (Antigravity/Codex) sinh code Mermaid.… | Antigravity / Codex |
| M4 | Render ảnh + Workflow design doc | Render sơ đồ Mermaid thành ảnh đẹp để đưa vào tài liệu/báo cáo. Tiêu chuẩn 1 design doc đủ… | Render ảnh workflow bằng Codex/Nano Banana (Gemini); viết Workflow design doc (hiện trạng … | Codex / Nano Banana (Gemini) |

## Lab chính

**Lab S2 — Thiết kế workflow cho bài toán đã chọn** — Ra 1 Workflow design doc hoàn chỉnh: hiện trạng + ESIA + sơ đồ Mermaid + ảnh render.

- **Thời lượng:** ~100 phút
- **Bối cảnh:** Dùng Use case one-pager từ S1. Mục tiêu: chuyển 'cách làm thủ công hôm nay' thành 'quy trình mới có chỗ cho AI' — chưa code, mới thiết kế.
- **Các bước:**
  1. Vẽ hiện trạng (as-is): bảng Bước | Người | Công cụ | Nghẽn | Lỗi (L1).
  2. Áp ESIA: đánh dấu mỗi bước E/S/I/A; chốt to-be và điểm HITL (L2).
  3. Sinh code Mermaid cho to-be bằng AI (L3).
  4. Render sơ đồ Mermaid thành ảnh bằng Codex/Nano Banana (L4).
  5. Vẽ sơ đồ so sánh Trước & Sau (Before & After) bằng AI (L5).
  6. Gộp thành Workflow design doc hoàn chỉnh và kiểm tra tuân thủ (L6).
- **Đầu ra:** Workflow design doc (.md) + 1 ảnh sơ đồ workflow + 1 ảnh sơ đồ Before & After.
- **Nghiệm thu (SLI/SLO):** Có đủ as-is + to-be · sơ đồ Mermaid hợp lệ render được · ≥1 bước được đánh dấu Automate · ≥1 điểm HITL · sơ đồ Before & After.

> Chi tiết đầy đủ: `lab.md` (đồng bộ với syllabus xlsx sheet tương ứng).

## Bàn giao sang Session sau

Workflow design doc (hiện trạng + ESIA + Mermaid + ảnh render + sơ đồ Before & After) → dựng trên n8n ở S3.

---
*Nội dung lý thuyết slide (design spec): `01-slides/designs/session-02-theory.md`. Per-session deep content (PPTX, instructor guide, synthetic data) = Phase 2.*