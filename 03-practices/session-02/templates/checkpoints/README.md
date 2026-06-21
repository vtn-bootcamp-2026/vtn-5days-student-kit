# Checkpoint rescue — Session 2

> Session 2 (3h30): Workflow design (hiện trạng + ESIA + Mermaid + render ảnh). Lab deliverable: **Workflow design doc**.

## Jump-point files (mở theo stuck-point)

| File | Khi nào mở | Trạng thái kỳ vọng |
|---|---|---|
| `checkpoint-as-is-mermaid.md` | Mermaid lỗi / sơ đồ rối | sơ đồ as-is render được |
| `checkpoint-esia-tobe.md` | không ra ý cải tiến | bảng ESIA + sơ đồ to-be |
| `checkpoint-render-design-doc.md` | ảnh mờ / doc thiếu (FINAL) | Workflow design doc hoàn chỉnh |

## Rescue map

| Stuck ở | Cấp cứu | Kết quả kỳ vọng |
|---|---|---|
| Vẽ hiện trạng (as-is) rối | Gợi ý vẽ theo "ai làm gì → công cụ → đầu ra" | Sơ đồ as-is rõ ≥5 bước |
| ESIA không ra ý | Cho bảng mẫu 4 cột (Eliminate/Simplify/Integrate/Automate) + ví dụ Agribank (`reference/agribank-workflow/`) | ≥2 ý cải tiến to-be |
| Mermaid lỗi cú pháp | Dán vào mermaid.live; TA sửa flowchart | Sơ đồ Mermaid render được |
| Render ảnh mờ/lỗi | Dùng Nano Banana/Gemini theo prompt style; fallback screenshot mermaid.live | 1 ảnh render rõ |

## Final state (checkpoint-final)

- **Workflow design doc**: hiện trạng (as-is) + ESIA đề xuất to-be + sơ đồ Mermaid + ảnh render. → bàn giao S3.

> Kế thừa: `reference/agribank-workflow/` (ESIA + Mermaid) + `reference/ai-workforce-k3/k3-buoi4-workflow/`.
