---
mo-ta: Hướng dẫn nhanh cú pháp JavaScript để xử lý và làm sạch JSON trên n8n cho học viên
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-23 15:10 +07:00
updated-at: 2026-05-24 13:25 +07:00
---

# Hướng dẫn nhanh xử lý dữ liệu và làm sạch JSON trên n8n

Tài liệu này cung cấp các đoạn mã mẫu bằng <span class="pill-academic">ngôn ngữ kịch bản: JavaScript (JS)</span> được tối ưu hóa riêng cho các <span class="pill-academic">nút mã xử lý: Code nodes</span> trên <span class="pill-academic">công cụ tự động hóa quy trình: n8n</span>. Các đoạn mã này giúp học viên giải quyết các chướng ngại kỹ thuật phổ biến khi làm việc với đầu ra của mô hình trí tuệ nhân tạo.

---

## 1. Làm sạch chuỗi phản hồi JSON bị bọc bởi định dạng Markdown

> [!WARNING]
> **TÌNH HUỐNG LỖI:** Nhiều mô hình ngôn ngữ lớn (LLM) có thói quen tự động bọc chuỗi JSON đầu ra trong ký tự định dạng Markdown dạng <code>```json ... ```</code> hoặc <code>``` ... ```</code> mặc dù đã có chỉ thị nghiêm ngặt trong câu lệnh hệ thống. Điều này khiến nút phân tích cú pháp JSON mặc định của n8n bị lỗi đỏ hệ thống.

### Giải pháp xử lý bằng Code Node (JavaScript)
Chèn đoạn mã sau vào nút **`Parse Gemini JSON`** (Code Node ở chế độ `Run Once for Each Item`) để tiến hành làm sạch, trích xuất và phân tích cú pháp chuỗi JSON an toàn:

```javascript
// Parse Gemini JSON sau khi đã có field raw_ai_output từ node Attach raw AI output
const raw =
  $json.raw_ai_output ||
  $json.content?.parts?.[0]?.text ||
  $json.text ||
  $json.output ||
  $json.response ||
  "";

let cleaned = String(raw)
  .replace(/```json/gi, "")
  .replace(/```/g, "")
  .trim();

// Nếu model trả thêm chữ trước/sau JSON, cố gắng cắt phần nằm giữa { ... }
const firstBrace = cleaned.indexOf("{");
const lastBrace = cleaned.lastIndexOf("}");

if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
  cleaned = cleaned.slice(firstBrace, lastBrace + 1);
}

let parsed;

try {
  parsed = JSON.parse(cleaned);
} catch (error) {
  parsed = {
    category: "Unknown",
    confidence: 0,
    reason: "AI trả về JSON không hợp lệ.",
    required_action: "Chuyển người duyệt thủ công.",
    human_review_required: true,
    parse_error: error.message
  };
}

// Ép kiểu boolean an toàn
const humanReview =
  parsed.human_review_required === true ||
  parsed.human_review_required === "true";

return {
  json: {
    ...$json,

    ai_category: parsed.category || "Unknown",
    ai_confidence: Number(parsed.confidence || 0),
    ai_reason: parsed.reason || "",
    required_action: parsed.required_action || "",
    human_review_required: humanReview,

    parse_error: parsed.parse_error || "",
    cleaned_ai_json: cleaned
  }
};
```

---

## 2. Lọc và ẩn thông tin cá nhân nhạy cảm (Data Masking)

> [!IMPORTANT]
> **AN TOÀN THÔNG TIN:** Khi người dùng nhập các yêu cầu hỗ trợ có chứa mật khẩu rõ (plain text password) hoặc thông tin thẻ, hệ thống tuyệt đối không được phép lưu trữ nguyên văn các chuỗi này vào nhật ký chung để tránh nguy cơ rò rỉ dữ liệu.

### Giải pháp lọc dữ liệu nhạy cảm (Tích hợp trực tiếp vào nút Parse Gemini JSON)
Đoạn mã JavaScript nâng cấp dưới đây giúp tích hợp đồng thời việc trích xuất làm sạch JSON và tự động khử mật khẩu nhạy cảm thô ở tầng code bằng biểu thức chính quy (<span class="pill-academic">biểu thức chính quy: Regular Expression (Regex)</span>) trước khi xuất kết quả phân loại:

```javascript
// Parse Gemini JSON và tự động khử mật khẩu nhạy cảm thô ở tầng code bằng Regex bảo mật
const raw =
  $json.raw_ai_output ||
  $json.content?.parts?.[0]?.text ||
  $json.text ||
  $json.output ||
  $json.response ||
  "";

let cleaned = String(raw)
  .replace(/```json/gi, "")
  .replace(/```/g, "")
  .trim();

// Nếu model trả thêm chữ trước/sau JSON, cố gắng cắt phần nằm giữa { ... }
const firstBrace = cleaned.indexOf("{");
const lastBrace = cleaned.lastIndexOf("}");

if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
  cleaned = cleaned.slice(firstBrace, lastBrace + 1);
}

let parsed;

try {
  parsed = JSON.parse(cleaned);
} catch (error) {
  parsed = {
    category: "Unknown",
    confidence: 0,
    reason: "AI trả về JSON không hợp lệ.",
    required_action: "Chuyển người duyệt thủ công.",
    human_review_required: true,
    parse_error: error.message
  };
}

// Khử mật khẩu nhạy cảm thô ở tầng code bằng Regex bảo mật
let reasonText = parsed.reason || "";
let requiredActionText = parsed.required_action || "";

// Danh sách các biểu thức chính quy (Regex) phát hiện các mẫu mật khẩu phổ biến
const passwordRegex = /(mật khẩu|mat khau|password|pwd|pass)[:\s]+([^\s,]+)/gi;

if (reasonText) {
  reasonText = reasonText.replace(passwordRegex, "$1: [REDACTED]");
}
if (requiredActionText) {
  requiredActionText = requiredActionText.replace(passwordRegex, "$1: [REDACTED]");
}

// Ép kiểu boolean an toàn
const humanReview =
  parsed.human_review_required === true ||
  parsed.human_review_required === "true";

return {
  json: {
    ...$json,

    ai_category: parsed.category || "Unknown",
    ai_confidence: Number(parsed.confidence || 0),
    ai_reason: reasonText,
    required_action: requiredActionText,
    human_review_required: humanReview,

    parse_error: parsed.parse_error || "",
    cleaned_ai_json: cleaned
  }
};
```

---

## 3. Quy tắc tiền kiểm tra dữ liệu đầu vào (Input Pre-checking Rules)

Trước khi thực hiện cuộc gọi API tốn phí gửi đến mô hình AI, quy trình cần thực hiện tiền lọc cục bộ để loại bỏ các dữ liệu rác hoặc quá ngắn bằng cú pháp `$json` đồng bộ:

```javascript
const description = ($json.issue_description || "").trim();

let validationStatus = "Valid";
let errorCode = "";

if (description.length === 0) {
  validationStatus = "Invalid";
  errorCode = "Missing_Data";
} else if (description.length < 10) {
  validationStatus = "Invalid";
  errorCode = "Format_Error";
}

return {
  json: {
    ...$json,
    validation_status: validationStatus,
    error_code: errorCode
  }
};
```
