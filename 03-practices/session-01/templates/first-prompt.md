---
mo-ta: mau loi nhac markdown dau tien cho session 01
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 17:00 +07:00
updated-at: 2026-05-26 17:00 +07:00
---

# Lời nhắc Markdown đầu tiên

## Thông tin nhóm

| Mục | Nội dung |
| --- | --- |
| Tên nhóm |  |
| Người soạn prompt |  |
| Công cụ dùng thử | Antigravity IDE / Antigravity CLI / khác |
| Trạng thái Gemini API | Đã kết nối / dùng tài khoản demo / chưa kết nối |

## Mục tiêu prompt

Mô tả ngắn tác vụ AI cần hỗ trợ:

> Ví dụ: tóm tắt log O&M mô phỏng thành báo cáo 1 trang, nêu sự cố chính, mức độ ưu tiên và hành động đề xuất.

## Dữ liệu đầu vào mô phỏng

Dán một đoạn dữ liệu mô phỏng ngắn. Không dùng dữ liệu thật, IP thật, mã trạm thật, email thật, tên khách hàng thật hoặc API key.

```text
[Dán dữ liệu mô phỏng ở đây]
```

## Prompt bản nháp

```text
Bạn là trợ lý AI hỗ trợ vận hành kỹ thuật.

Nhiệm vụ:
- Đọc dữ liệu mô phỏng bên dưới.
- Tóm tắt vấn đề chính trong 3-5 gạch đầu dòng.
- Đề xuất mức độ ưu tiên: Low / Medium / High.
- Đề xuất hành động tiếp theo cho người vận hành.
- Nếu thiếu dữ liệu hoặc có rủi ro, ghi rõ cần con người kiểm tra.

Ràng buộc an toàn:
- Không suy đoán thông tin không có trong dữ liệu.
- Không lặp lại dữ liệu nhạy cảm nếu phát hiện.
- Không yêu cầu hoặc hiển thị API key, token, mật khẩu.
- Chỉ trả lời bằng tiếng Việt.

Dữ liệu:
"""
[Dán dữ liệu mô phỏng ở đây]
"""
```

## Đầu ra kỳ vọng

- Tóm tắt sự cố:
- Mức độ ưu tiên:
- Hành động đề xuất:
- Điểm cần con người kiểm tra:

## Ghi chú sau khi chạy thử

- AI trả lời đúng cấu trúc không?
- Có suy đoán ngoài dữ liệu không?
- Có cần thêm ràng buộc an toàn không?
