# Checkpoint S2-C — Render ảnh + Workflow design doc (FINAL)

> **Dùng khi:** ảnh render mờ / design doc thiếu thành phần. Đây là final state S2.

## Trạng thái kỳ vọng (FINAL)

1 **Workflow design doc** gồm: hiện trạng (as-is) + ESIA + to-be (Mermaid) + **1 ảnh render** rõ.

## Cấp cứu nhanh

- **Ảnh render mờ/lỗi:** dùng Nano Banana/Gemini/Codex với prompt style đồng nhất; fallback screenshot mermaid.live xuất PNG.
- **Design doc thiếu phần:** đảm bảo đủ 4 phần (as-is + ESIA + Mermaid + ảnh) — đây là 1 trong 6 đầu ra tối thiểu.
- **Mermaid → ảnh:** export PNG từ mermaid.live hoặc render qua tool.

## Bàn giao

Workflow design doc → **S3/S4** (dựng n8n theo to-be).
