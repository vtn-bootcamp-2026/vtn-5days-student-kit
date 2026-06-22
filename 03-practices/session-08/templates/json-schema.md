---
mo-ta: mau luoc do JSON cho contract term extractor
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 15:00 +07:00
updated-at: 2026-05-26 15:00 +07:00
---

# Mẫu lược đồ JSON: JSON schema template

## Schema: contract-term.schema.json

Sao chép schema dưới đây vào tệp `schemas/contract-term.schema.json` trong project nhóm.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Contract Term Extraction Result",
  "description": "Lược đồ JSON cho kết quả trích xuất điều khoản hợp đồng",
  "type": "object",
  "required": [
    "contract_id",
    "effective_date",
    "expiry_date",
    "penalty_clause",
    "source_evidence",
    "confidence",
    "needs_human_review",
    "red_flags",
    "missing_fields",
    "extraction_notes"
  ],
  "properties": {
    "contract_id": {
      "type": "string",
      "description": "Mã hợp đồng, ví dụ: contract-001"
    },
    "effective_date": {
      "type": "string",
      "format": "date",
      "description": "Ngày hiệu lực, định dạng YYYY-MM-DD. null nếu không tìm thấy."
    },
    "expiry_date": {
      "type": "string",
      "format": "date",
      "description": "Ngày hết hạn, định dạng YYYY-MM-DD. null nếu không tìm thấy."
    },
    "penalty_clause": {
      "type": "string",
      "description": "Nội dung tóm tắt điều khoản phạt. Chuỗi rỗng nếu không có."
    },
    "penalty_amount": {
      "type": "string",
      "description": "Số tiền/mức phạt chi tiết. Chuỗi rỗng nếu không có."
    },
    "source_evidence": {
      "type": "array",
      "description": "Danh sách căn cứ nguồn cho các trường trích xuất",
      "items": {
        "type": "object",
        "required": ["field", "quote", "section"],
        "properties": {
          "field": {
            "type": "string",
            "description": "Tên trường JSON mà trích dẫn tham chiếu đến"
          },
          "quote": {
            "type": "string",
            "description": "Trích dẫn nguyên văn từ hợp đồng"
          },
          "section": {
            "type": "string",
            "description": "Điều khoản số mấy trong hợp đồng"
          }
        }
      }
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Mức chắc chắn tổng thể. Dựa trên căn cứ nguồn, không phải cảm tính."
    },
    "needs_human_review": {
      "type": "boolean",
      "description": "Bật true khi: thiếu trường, confidence < 0.7, mâu thuẫn, cờ đỏ, lỗi OCR"
    },
    "red_flags": {
      "type": "array",
      "description": "Danh sách cờ đỏ phát hiện được",
      "items": {
        "type": "string"
      }
    },
    "missing_fields": {
      "type": "array",
      "description": "Danh sách trường không tìm thấy trong hợp đồng",
      "items": {
        "type": "string"
      }
    },
    "extraction_notes": {
      "type": "string",
      "description": "Ghi chú bổ sung về quá trình trích xuất: lỗi OCR, mâu thuẫn, giải thích"
    }
  }
}
```

## Ví dụ JSON output hợp lệ

```json
{
  "contract_id": "contract-001",
  "effective_date": "2026-01-01",
  "expiry_date": "2026-12-31",
  "penalty_clause": "Phạt 1% giá trị hợp đồng hàng tháng cho mỗi 0.5% giảm hiệu suất, tối đa 10% giá trị hợp đồng hàng quý",
  "penalty_amount": "1% giá trị hợp đồng hàng tháng cho mỗi 0.5% giảm hiệu suất",
  "source_evidence": [
    {
      "field": "effective_date",
      "quote": "Hợp đồng có hiệu lực kể từ ngày 01 tháng 01 năm 2026",
      "section": "Điều 2"
    },
    {
      "field": "expiry_date",
      "quote": "Hợp đồng có thời hạn 12 (mười hai) tháng, hết hạn vào ngày 31 tháng 12 năm 2026",
      "section": "Điều 2"
    },
    {
      "field": "penalty_clause",
      "quote": "Phạt 1% giá trị hợp đồng hàng tháng cho mỗi 0.5% giảm hiệu suất. Tối đa phạt không quá 10% giá trị hợp đồng hàng quý.",
      "section": "Điều 4"
    }
  ],
  "confidence": 0.92,
  "needs_human_review": false,
  "red_flags": [],
  "missing_fields": [],
  "extraction_notes": "Hợp đồng đầy đủ, rõ ràng. Không phát hiện cờ đỏ."
}
```

## Ví dụ JSON output có cờ đỏ

```json
{
  "contract_id": "contract-003-risky",
  "effective_date": "2026-03-01",
  "expiry_date": "2027-02-28",
  "penalty_clause": "Phạt 5% giá trị hợp đồng hàng tháng cho mỗi giờ vượt, không giới hạn mức phạt tối đa",
  "penalty_amount": "5% giá trị hợp đồng hàng tháng cho mỗi giờ vượt quá SLA",
  "source_evidence": [
    {
      "field": "effective_date",
      "quote": "Hợp đồng có hiệu lực kể từ ngày 01 tháng 03 năm 2026",
      "section": "Điều 2"
    },
    {
      "field": "penalty_clause",
      "quote": "Phạt 5% giá trị hợp đồng hàng tháng cho mỗi giờ vượt. Không giới hạn mức phạt tối đa.",
      "section": "Điều 4"
    },
    {
      "field": "red_flag_auto_renew",
      "quote": "Hợp đồng sẽ tự động gia hạn thêm 12 tháng mà không cần thông báo trước trừ khi một bên thông báo bằng văn bản chấm dứt trước 15 ngày",
      "section": "Điều 2"
    }
  ],
  "confidence": 0.65,
  "needs_human_review": true,
  "red_flags": [
    "Tự gia hạn bất lợi: chỉ cần thông báo 15 ngày trước, rất dễ bị lỡ thời hạn chấm dứt",
    "Phạt không giới hạn: không có mức tối đa cho phạt vi phạm SLA",
    "Giới hạn trách nhiệm quá thấp: chỉ bằng 1 tháng giá trị hợp đồng với hợp đồng 1.8 tỷ"
  ],
  "missing_fields": [],
  "extraction_notes": "Phát hiện 3 cờ đỏ. Confidence thấp do nhiều rủi ro. Chuyển HITL."
}
```
