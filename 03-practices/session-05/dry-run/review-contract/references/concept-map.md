---
mo-ta: tai lieu tham khao so do kien truc tac nhan AI contract term extractor
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 15:00 +07:00
updated-at: 2026-05-26 15:00 +07:00
---

# Sơ đồ kiến trúc tác nhân AI: concept map

## Luồng xử lý tổng thể

```text
┌─────────────────────────────────────────────────────────┐
│                    HỢP ĐỒNG ĐẦU VÀO                      │
│              (contract-001.txt / .pdf đã OCR)            │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              BƯỚC 1: KIỂM TRA ĐẦU VÀO                   │
│         (file rỗng? OCR lỗi? Thiếu metadata?)            │
├─────────────────────────────────────────────────────────┤
│  Hợp lệ → Bước 2     │     Lỗi → LOG + HITL             │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│         BƯỚC 2: TRÍCH XUẤT ĐIỀU KHOẢN                   │
│    (System prompt + User prompt → JSON output)           │
│    Yêu cầu: source_evidence cho mọi trường               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│             BƯỚC 3: TỰ KIỂM: SELF-CHECK                  │
│  Đủ trường? Đúng format? Có source_evidence?             │
│  Confidence hợp lý? HITL bật đúng chưa?                  │
├─────────────────────────────────────────────────────────┤
│  Pass → Bước 4      │     Fail → Quay Bước 2 sửa        │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│        BƯỚC 4: ĐỐI CHIẾU KHO ĐIỀU KHOẢN                 │
│   (clause library + red-flag rules)                      │
│   Phát hiện cờ đỏ? Mức rủi ro?                          │
├─────────────────────────────────────────────────────────┤
│  An toàn → Bước 5    │    Cờ đỏ → Thêm red_flags[]      │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              BƯỚC 5: XUẤT KẾT QUẢ                        │
│   JSON (extracted-terms) + Báo cáo cờ đỏ (nếu có)       │
│   + Execution log                                       │
├─────────────────────────────────────────────────────────┤
│  needs_human_review=false → DONE                        │
│  needs_human_review=true  → HÀNG ĐỢI NGƯỜI DUYỆT       │
└─────────────────────────────────────────────────────────┘
```

## Bảng thuật ngữ cốt lõi

| Thuật ngữ tiếng Việt | English term | Giải thích ngắn |
| --- | --- | --- |
| Tác nhân AI | AI Agent | Hệ thống AI tự chủ thực hiện nhiệm vụ theo vai trò đã định |
| Vai trò | Persona | Định nghĩa "AI đóng vai ai" trong lời nhắc hệ thống |
| Ranh giới xử lý | Processing boundary | Giới hạn tác nhân chỉ kết luận trong phạm vi dữ liệu có sẵn |
| Quy tắc tự kiểm | Self-check rule | Tác nhân tự rà soát output trước khi xuất |
| Lược đồ JSON | JSON Schema | Mô tả cấu trúc và kiểu dữ liệu chuẩn hóa cho đầu ra |
| Căn cứ nguồn | Source evidence | Trích dẫn nguyên văn từ văn bản gốc làm bằng chứng |
| Cờ đỏ | Red flag | Điều khoản có rủi ro cao cần con người rà soát |
| Âm tính giả | False negative | Rủi ro có thật nhưng tác nhân bỏ sót |
| Con người trong vòng lặp | Human-in-the-loop (HITL) | Điểm bắt buộc con người duyệt trước khi dùng kết quả |
| Nhật ký vận hành | Execution log | Ghi nhận quá trình xử lý để truy vết |
