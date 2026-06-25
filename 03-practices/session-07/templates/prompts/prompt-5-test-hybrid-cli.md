---
mo-ta: Prompt hướng dẫn chạy các dòng lệnh truy vấn để kiểm thử và so sánh kết quả của retriever hybrid qua CLI
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 5: Kiểm thử bộ truy xuất lai qua CLI

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn chạy thử nghiệm và kiểm chứng hiệu quả của bộ truy xuất lai (truy xuất lai: hybrid retrieval) vừa viết qua giao diện dòng lệnh: CLI.

Hãy thực thi trực tiếp các dòng lệnh sau trên hệ thống và phân tích kết quả trả về cho tôi:

1. **Kiểm thử tìm kiếm ngữ nghĩa (tìm kiếm ngữ nghĩa: semantic search):**
   ```bash
   python outputs/skills/hr-policy-qa-skill/scripts/retriever.py --query "nghỉ ốm lương như thế nào?" --top-k 3
   ```
   *Yêu cầu:* Kiểm tra xem kết quả có trỏ đúng tài liệu `POL-LEAVE-001` mục Nghỉ ốm không? Vector search có đóng vai trò chính không?

2. **Kiểm thử tìm kiếm từ khóa chính xác (tìm kiếm từ khóa: keyword search - mã số/tên riêng):**
   ```bash
   python outputs/skills/hr-policy-qa-skill/scripts/retriever.py --query "POL-LEAVE-001 mục 2.1 ngày phép" --top-k 3
   ```
   *Yêu cầu:* Kiểm tra xem bộ tìm kiếm từ khóa BM25 có bắt chính xác mã tài liệu `POL-LEAVE-001` không? (Đây là trường hợp vector search thuần túy thường trả về kết quả kém chính xác).

3. **Kiểm thử câu hỏi kết hợp chéo (đối chiếu chéo: cross-reference):**
   ```bash
   python outputs/skills/hr-policy-qa-skill/scripts/retriever.py --query "thâm niên 6 năm nghỉ phép bao nhiêu ngày" --top-k 3
   ```
   *Yêu cầu:* Xem kết quả RRF fuse có kéo cả hai tài liệu `POL-LEAVE-001` (nghỉ phép cơ bản) và `POL-SENIOR-001` (thâm niên cộng thêm phép) lên đầu danh sách không?

Hãy phân tích và so sánh chi tiết kết quả của ba câu lệnh trên (hiển thị rõ doc_id, section, score và method của từng chunk trả về trong khối raw JSON).
```
