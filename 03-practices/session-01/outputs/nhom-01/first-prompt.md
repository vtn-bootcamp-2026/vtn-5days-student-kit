---
mo-ta: mau loi nhac markdown dau tien cho session 01 - nhom 01
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 12:05 +07:00
updated-at: 2026-05-26 12:05 +07:00
---

# Lời nhắc Markdown đầu tiên

## Thông tin nhóm

| Mục | Nội dung |
| --- | --- |
| Tên nhóm | Nhóm 01 (Vui lòng cập nhật tên nhóm của bạn) |
| Người soạn prompt | Học viên nhóm 01 |
| Công cụ dùng thử | Antigravity IDE |
| Trạng thái Gemini API | Đã kết nối |

## Mục tiêu prompt

Mô tả ngắn tác vụ AI cần hỗ trợ:

> Tóm tắt 3 dòng log cảnh báo NOC mô phỏng, phân tích sự cố, đề xuất mức độ ưu tiên (Low / Medium / High), đưa ra hành động tiếp theo cho người vận hành (HITL) và tự động ẩn/lọc bỏ thông tin cá nhân nhạy cảm (PII).

## Dữ liệu đầu vào mô phỏng

```text
ALERT-001,2026-05-01 08:02:00,TEST_SITE_018,server,high,database query latency spike in performance test [Contact: Nguyen Van A (0987654321)],open
ALERT-009,2026-05-01 21:52:00,TEST_SITE_012,base-station,high,RF module communication failure in lab environment [Assigned to: Nguyen Hoang E (0912345678)],open
ALERT-013,2026-05-01 18:03:00,TEST_SITE_020,firewall,medium,high memory usage alert on training cluster [Contact: Nguyen Van A (0987654321)],in-progress
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
ALERT-001,2026-05-01 08:02:00,TEST_SITE_018,server,high,database query latency spike in performance test [Contact: Nguyen Van A (0987654321)],open
ALERT-009,2026-05-01 21:52:00,TEST_SITE_012,base-station,high,RF module communication failure in lab environment [Assigned to: Nguyen Hoang E (0912345678)],open
ALERT-013,2026-05-01 18:03:00,TEST_SITE_020,firewall,medium,high memory usage alert on training cluster [Contact: Nguyen Van A (0987654321)],in-progress
"""
```

## Đầu ra kỳ vọng

- **Tóm tắt sự cố:**
  - ALERT-001 (server tại TEST_SITE_018) tăng độ trễ truy vấn cơ sở dữ liệu khi test hiệu năng. Trạng thái: open.
  - ALERT-009 (base-station tại TEST_SITE_012) lỗi truyền thông mô-đun RF trong lab. Trạng thái: open.
  - ALERT-013 (firewall tại TEST_SITE_020) quá tải bộ nhớ trên cụm đào tạo. Trạng thái: in-progress.
- **Mức độ ưu tiên:** High (do có hai sự cố nghiêm trọng mức High đang mở).
- **Hành động đề xuất (HITL):** Kiểm tra cáp vật lý và trạng thái mô-đun RF cho ALERT-009, phân tích slow query log cho ALERT-001, và giám sát tiến trình bộ nhớ cho ALERT-013.
- **Điểm cần con người kiểm tra:** Lọc bỏ thông tin PII (họ tên, số điện thoại) xuất hiện trong log thô để tránh rò rỉ bảo mật; kiểm tra xem lỗi môi trường test/lab có ảnh hưởng tới môi trường production thật hay không.

## Ghi chú sau khi chạy thử

- **AI trả lời đúng cấu trúc không?** Có, AI trả về kết quả rõ ràng, chia mục tóm tắt sự cố, độ ưu tiên, hành động đề xuất và điểm cần con người kiểm tra một cách trực quan.
- **Có suy đoán ngoài dữ liệu không?** Không, AI bám sát dữ liệu mô phỏng và không tự ý bịa thêm trạm hay thiết bị khác.
- **Có cần thêm ràng buộc an toàn không?** Các ràng buộc an toàn hiện tại (ẩn PII, không suy đoán) hoạt động rất tốt, đã lọc sạch số điện thoại và họ tên của kỹ sư trực ca.
