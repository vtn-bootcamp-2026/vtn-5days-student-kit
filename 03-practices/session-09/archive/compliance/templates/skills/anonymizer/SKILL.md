---
mo-ta: "Tài liệu kỹ thuật mô tả Kỹ năng tác nhân che giấu dữ liệu nhạy cảm cục bộ (Local AI Anonymizer Skill) tại Viettel Networks"
trang-thai: active
phien-ban: v1.0
created-at: "2026-06-14 23:20 +07:00"
updated-at: "2026-06-14 23:20 +07:00"
---

# Kỹ năng tác nhân: Local AI Anonymizer Skill

Kỹ năng này cho phép tác nhân AI tự động phát hiện, che giấu và chuẩn hóa thông tin cá nhân nhạy cảm: Personal Identifiable Information (PII) cục bộ (offline 100%) trước khi truyền dữ liệu ra các mô hình AI Cloud công cộng, đảm bảo tuân thủ nghiêm ngặt Nghị định 356/2025/NĐ-CP của Chính phủ.

---

## 1. Cấu trúc thư mục Kỹ năng
Khi được phân phối trong hệ thống tác nhân, kỹ năng này tuân theo cấu trúc chuẩn hóa sau:

```text
skills/anonymizer/
├── skill.json              # File cấu hình metadata khai báo đầu vào/đầu ra của kỹ năng
├── SKILL.md                # Tài liệu hướng dẫn sử dụng kỹ năng này (file này)
└── src/
    └── anonymizer.py       # Mã nguồn xử lý chính (Regex + Local LLM API)
```

---

## 2. Các tham số Đầu vào & Đầu ra (Spec)

### Đầu vào (Inputs)
*   `text` (Kiểu: `string` - Bắt buộc): Đoạn văn bản chứa thông tin kỹ thuật, log vận hành thô có khả năng chứa PII.

### Đầu ra (Outputs)
*   `redacted_text` (Kiểu: `string`): Đoạn văn bản đã che giấu sạch PII.
*   `needs_human_review` (Kiểu: `boolean`): Cờ kích hoạt phê duyệt HITL.
*   `pii_counts` (Kiểu: `object`): Số lượng phần tử đã bị che giấu theo từng loại (ví dụ: `email`, `phone`, `cccd`, `name`).

---

## 3. Cơ chế hoạt động & Xử lý ngữ cảnh (Hybrid Logic)

Kỹ năng này hoạt động bằng cách kết hợp hai lớp xử lý chính:

1.  **Lớp Regex (Lọc nhanh tốc độ cao):** Sử dụng các biểu thức chính quy tối ưu để tìm kiếm nhanh các trường dữ liệu có cấu trúc định dạng chuẩn (Email, Số điện thoại Việt Nam, Số CCCD 12 chữ số).
2.  **Lớp Local LLM (Xử lý ngữ cảnh tinh tế):** Gọi mô hình cục bộ (`qwen3.5:1.5b-instruct` hoặc `gemma4:e2b`) qua Ollama để phân tích các từ lắt léo (phân biệt tên riêng người như "anh Hoa" và danh từ thường "đi mua hoa"), chặn tấn công Prompt Injection bảo mật và kích hoạt cờ kiểm duyệt HITL kịp thời.

---

## 4. Hướng dẫn Tích hợp & Gọi Kỹ năng

Để tích hợp kỹ năng này vào Tác nhân chính (Hermes Agent), hãy khai báo tệp `skill.json` vào danh mục kỹ năng hoạt động của Agent trong tệp `config.yaml` của dự án:

```yaml
agent:
  name: security-gateway-agent
  skills:
    - path: "skills/anonymizer"
      enabled: true
```
