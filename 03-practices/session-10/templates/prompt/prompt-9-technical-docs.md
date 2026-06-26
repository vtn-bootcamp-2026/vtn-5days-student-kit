---
mo-ta: "Prompt 9 — Tự động sinh bộ 4 tài liệu kỹ thuật vận hành và bàn giao"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

# Prompt 9: Đóng gói hồ sơ vận hành & Bàn giao kỹ thuật (Implementation Kit Docs)

Hãy sao chép nội dung dưới đây và gửi cho trợ lý ảo AI trên cùng phiên chat để sinh 4 tài liệu kỹ thuật phụ trợ còn lại:

```text
BỐI CẢNH:
Để hoàn thành bộ hồ sơ Implementation Kit đầy đủ bàn giao cho đơn vị vận hành tại Viettel Net, nhóm chúng tôi cần soạn thảo 4 tài liệu kỹ thuật chuyên sâu sau:
1. "06-test-cases-specification.md" (Đặc tả 10 ca kiểm thử)
2. "07-failure-modes-rollback.md" (Phân tích lỗi và kịch bản Rollback/Fallback)
3. "08-runbook-template.md" (Tài liệu hướng dẫn vận hành chi tiết)
4. "09-handoff-contract.md" (Biên bản bàn giao kỹ thuật)

CHỈ DẪN CHO AI:
Hãy viết nội dung Markdown hoàn chỉnh cho cả 4 tệp tin này dựa trên giải pháp kỹ thuật của dự án. Hãy phân tách rõ ràng từng tệp tin bằng tiêu đề tệp và đặt nội dung trong các khối mã code block Markdown riêng biệt để tôi dễ dàng copy-paste.

Yêu cầu chi tiết cho từng tệp tin:

---
### TỆP 1: 06-test-cases-specification.md
- **Thông tin chung:** Tên nhóm, thành viên, phiên bản công cụ (v1.0), ngày thực hiện.
- **Nội dung:** Thiết kế bộ 10 ca kiểm thử (Test Cases - TC) bao phủ 4 nhóm tình huống sau:
  - Nhóm 1: Tình huống bình thường (Normal cases) - 3 TC (Ví dụ: che giấu chuẩn các trường dữ liệu).
  - Nhóm 2: Tình huống lỗi (Error cases) - 2 TC (Ví dụ: dữ liệu đầu vào sai định dạng, thiếu độ dài).
  - Nhóm 3: Tình huống thiếu dữ liệu (Missing data cases) - 2 TC (Ví dụ: thiếu trường bắt buộc).
  - Nhóm 4: Tình huống vượt phạm vi / bảo mật (Out of bounds/Security cases) - 3 TC (Ví dụ: tấn công Prompt Injection, văn bản quá dài, ký tự đặc biệt phá vỡ cấu trúc).
  - *Mỗi TC phải ghi rõ: Mô tả đầu vào, Kết quả mong đợi, Kết quả thực tế (Đạt), Trạng thái (Pass).*
- **Frontmatter Metadata bắt buộc:**
---
mo-ta: "Biểu mẫu đặc tả ca kiểm thử cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

---
### TỆP 2: 07-failure-modes-rollback.md
- **Thông tin chung:** Tên công cụ, nhóm chịu trách nhiệm, ngày cập nhật.
- **Nội dung:** 
  - Phân tích và đưa ra giải pháp ứng phó cho ít nhất 3 tình huống lỗi kỹ thuật (Failure modes):
    - Tình huống lỗi 1: Mất kết nối tới máy chủ mô hình cục bộ (Local LLM connection failure) -> giải pháp fallback sang chế độ Regex/Rule-based.
    - Tình huống lỗi 2: Tràn bộ nhớ RAM hệ điều hành khi chạy mô hình lớn (Out of memory - OOM) -> giải pháp giới hạn tài nguyên và chuyển đổi sang mô hình siêu nhẹ.
    - Tình huống lỗi 3: Lọc sót thông tin nhạy cảm của nhân sự (Data leakage do AI ảo tưởng/bỏ sót) -> giải pháp Human-in-the-loop duyệt kết quả và rollback xóa log/file lỗi.
  - Quy trình khôi phục phiên bản mã nguồn cũ (Rollback runbook) qua Git hoặc sao lưu thủ công.
- **Frontmatter Metadata bắt buộc:**
---
mo-ta: "Biểu mẫu phân tích các tình huống lỗi và phương án khôi phục/dự phòng cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.3
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

---
### TỆP 3: 08-runbook-template.md
- **Thông tin chung:** Mã tài liệu, người biên soạn, đơn vị phê duyệt, phiên bản hệ thống áp dụng.
- **Nội dung:** 
  - Yêu cầu hệ thống và chuẩn bị môi trường: RAM, CPU, SSD, cài đặt Python 3.10+, cài đặt Ollama, các lệnh pull mô hình cục bộ (`qwen3.5:1.5b-instruct` hoặc `gemma4:e2b`).
  - Quy trình cài đặt chi tiết (Deployment steps): khởi tạo thư mục, cài đặt môi trường ảo `.venv`, cài đặt thư viện qua `requirements.txt`, cấu hình tệp `.env`.
  - Hướng dẫn vận hành chi tiết: lệnh khởi chạy công cụ, cách nhập dữ liệu và lấy file đầu ra trong thư mục `outputs/`.
  - Quy trình xử lý sự cố thường gặp (Troubleshooting guide).
- **Frontmatter Metadata bắt buộc:**
---
mo-ta: "Biểu mẫu hướng dẫn vận hành công cụ Mini Tool Anonymizer cho đội ngũ kỹ thuật VTN"
trang-thai: active
phien-ban: v1.2
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---

---
### TỆP 4: 09-handoff-contract.md
- **Thông tin chung:** Tên dự án, bên giao (nhóm phát triển), bên nhận (đơn vị tiếp nhận), ngày ký kết.
- **Nội dung:**
  - Danh mục các tài sản bàn giao (Deliverables): mã nguồn chính, file cấu hình `.env`, requirements.txt, tài liệu vận hành Runbook, đặc tả test case, checklist tuân thủ bảo mật, tệp dữ liệu giả lập.
  - Cam kết mức độ dịch vụ và Hỗ trợ kỹ thuật (SLA & Support guidelines): trách nhiệm của Bên giao (hỗ trợ ban đầu, sửa lỗi khẩn cấp, chuyển giao tri thức) và Bên nhận (chuẩn bị hạ tầng, giám sát log, sử dụng đúng mục đích).
- **Frontmatter Metadata bắt buộc:**
---
mo-ta: "Biểu mẫu biên bản bàn giao kỹ thuật Handoff Contract cho Mini Tool Anonymizer"
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-26 10:15 +07:00
updated-at: 2026-06-26 10:15 +07:00
---
```

**Kết quả kỳ vọng:** Bạn nhận được nội dung Markdown hoàn chỉnh của 4 tệp tin trên, sẵn sàng để sao chép vào các tệp tương ứng.
