---
mo-ta: Prompt hướng dẫn thực thi script phân đoạn tài liệu (chunker) và kiểm tra tệp kết quả chunks.json
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 3: Thực thi và kiểm tra tệp phân đoạn (Chunker output)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn chạy công cụ phân đoạn tài liệu: chunker để chuẩn bị dữ liệu cho hệ thống tìm kiếm. Hãy hỗ trợ tôi thực hiện các bước sau:

1. Copy tệp kịch bản chia nhỏ: chunker.py từ `templates/skills/hr-policy-qa-skill/scripts/chunker.py` sang thư mục code của nhóm tại `outputs/skills/hr-policy-qa-skill/scripts/chunker.py`.
2. Thực thi dòng lệnh chạy script `chunker.py` để chia nhỏ 4 tệp chính sách trong thư mục `outputs/skills/hr-policy-qa-skill/kb/hr-policies/` và ghi kết quả ra tệp JSON:
   ```bash
   python outputs/skills/hr-policy-qa-skill/scripts/chunker.py --kb-dir outputs/skills/hr-policy-qa-skill/kb/hr-policies --output outputs/skills/hr-policy-qa-skill/kb/chunks.json
   ```
3. Sau khi chạy xong, hãy đọc tệp kết quả `outputs/skills/hr-policy-qa-skill/kb/chunks.json` để kiểm tra và xác nhận:
   - Có bao nhiêu phân đoạn (chunks) được tạo ra? (Kỳ vọng khoảng 15-20 chunks).
   - Mỗi chunk có chứa đủ 8 trường siêu dữ liệu (siêu dữ liệu: metadata) yêu cầu không? Các trường bao gồm: `chunk_id`, `doc_id`, `section`, `version`, `status`, `access_level`, `word_count`, và `content`.
   - Hiển thị ví dụ nội dung và cấu trúc của chunk đầu tiên cho tôi xem.
```
