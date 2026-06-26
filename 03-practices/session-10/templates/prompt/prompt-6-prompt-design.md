---
mo-ta: "Prompt 6 — Đặc tả cấu trúc Prompt hệ thống và Nhật ký kiểm thử Playground"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 6: Nhật ký kiểm thử & Đặc tả ca kiểm thử (Core Prompt Design & Playground Logs)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat để hoàn thiện tệp tài liệu `03-core-prompt-design.md`:

```text
BỐI CẢNH:
Tôi cần hoàn thiện bản thiết kế lời nhắc cốt lõi "03-core-prompt-design.md" cho dự án AI của mình. Tài liệu này cần đặc tả chi tiết lời nhắc hệ thống (System Prompt) sau khi đã tích hợp các cơ chế bảo mật ở bước trước, định dạng cấu trúc JSON đầu ra, và ghi chép nhật ký thử nghiệm Playground thực tế.

CHỈ DẪN CHO AI:
Hãy viết một tài liệu Markdown hoàn chỉnh cho tệp "03-core-prompt-design.md" dựa trên thiết kế và các cập nhật bảo mật của skill. Tài liệu cần điền đầy đủ và chi tiết các mục sau:

1. Thông tin chung: Tên dự án, tên nhóm thực hiện, mô hình sử dụng đề xuất (Ví dụ: qwen3.5:1.5b-instruct / gemma4:e2b chạy local qua Ollama).
2. Mục 1: Cấu trúc Lời nhắc hệ thống (System Prompt):
   - Trình bày System Prompt hoàn chỉnh của mô hình đã thiết kế trong mã nguồn ở Bước 5.
   - Nêu bật các quy tắc: phân vai trợ lý bảo mật, các nhãn che giấu PII, quy tắc phòng vệ Prompt Injection bọc XML, và các quy tắc tự kiểm tra (Self-Check Rules) để tránh ảo tưởng (hallucination).
3. Mục 2: Định dạng đầu ra mong muốn (Output JSON Schema):
   - Đặc tả cấu trúc JSON Schema sạch sẽ mà mô hình bắt buộc phải trả về để tích hợp lập trình.
   - Ví dụ:
     {
       "redacted_text": "văn bản đã ẩn danh",
       "pii_detected_count": 0,
       "needs_human_review": false,
       "security_status": "SAFE" / "WARNING"
     }
4. Mục 3: Nhật ký kiểm thử thủ công trên Web UI (Prompt Playground Logs):
   - Hãy thiết kế chi tiết kết quả chạy thử nghiệm thực tế (Playground logs) với 3 ca kiểm thử:
     - Ca kiểm thử 1: Tình huống bình thường (Happy Path) - Dữ liệu thô đầu vào chứa thông tin nhạy cảm định dạng chuẩn -> Kết quả JSON đầu ra ẩn danh chính xác, trạng thái an toàn.
     - Ca kiểm thử 2: Tình huống biên lắt léo (Edge Case) - Dữ liệu chứa các từ dễ nhầm lẫn hoặc các tham số kỹ thuật tương tự định dạng PII (ví dụ số đo thập phân SCADA dễ nhầm với SĐT, hoặc serial thiết bị dễ nhầm với CCCD) -> Mô hình phân biệt đúng và giữ nguyên dữ liệu kỹ thuật.
     - Ca kiểm thử 3: Tấn công lời nhắc (Prompt Injection) - Dữ liệu chứa các kịch bản phá vỡ vai trò (Jailbreak) -> Mô hình phát hiện và đặt cờ cảnh báo rủi ro an toàn thông tin.

LƯU Ý QUAN TRỌNG VỀ ĐỊNH DẠNG:
- Bắt buộc phải có frontmatter metadata ở đầu tài liệu với các trường sau:
---
mo-ta: "Biểu mẫu đặc tả thiết kế lời nhắc (Core Prompt Design Blueprint) phục vụ báo cáo Capstone tại VTN"
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---
- Chỉ viết tài liệu Markdown hoàn chỉnh, không kèm thêm lời giải thích dẫn nhập hoặc kết thúc.
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh để dán đè vào tệp `03-core-prompt-design.md`.
