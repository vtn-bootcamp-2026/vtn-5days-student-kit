---
mo-ta: "Prompt B — Concept 1: Ẩn danh PII (Anonymizer) cho học viên non-tech"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 08:00 +07:00
updated-at: 2026-06-26 08:00 +07:00
---

# Prompt B: Concept 1 — Ẩn danh PII (Anonymizer)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```text
BỐI CẢNH:
Tiếp tục "Vệ sĩ văn phòng VTN". File dữ liệu mẫu:
- synthetic-data/vp-vtn-ban-giao-ca.txt (bản ghi bàn giao ca, có PII + 1 email Injection).
- synthetic-data/vp-vtn-ban-giao-ca-redacted-mau.txt (kết quả đúng để so sánh).
Cơ sở tri thức: kb/pii-categories.md (loại PII cần ẩn), kb/safe-terms.md (KHÔNG được ẩn).

CHỈ DẪN:
Dựa trên templates/office-guard-starter.py, tạo vp-vtn-office-guard/scripts/anonymizer.py
sao cho khi chạy với đầu vào là vp-vtn-ban-giao-ca.txt thì:
1. Ẩn: email→[REDACTED_EMAIL], SĐT→[REDACTED_PHONE], CCCD→[REDACTED_CCCD].
2. Ẩn tên người (nhân viên + khách)→[REDACTED_NAME], dùng ngữ cảnh tiếng Việt (chỉ tên người, KHÔNG phải tên bộ phận).
3. GIỮ NGUYÊN: mã phiếu TK-..., số tiền ... VNĐ, mã phiên #CSKH-..., tên "Trung tâm CSKH", tổng đài 1800.8123.
4. Ghi kết quả ra outputs/vp-vtn-ban-giao-ca-redacted.txt.
5. Ghi outputs/execution-log.csv chỉ chứa: run_id, input_file, pii_count, needs_human_review, created_at (KHÔNG chứa PII gốc).
Sau đó CHẠY script và cho tôi xem diff so với file mẫu redacted.

TIÊU CHUẨN ĐẦU RA:
- Tệp outputs/vp-vtn-ban-giao-ca-redacted.txt gần giống file -redacted-mau.txt.
- outputs/execution-log.csv sạch PII.
- Báo cáo: đã ẩn bao nhiêu PII mỗi loại, có che nhầm mã phiếu/tiền không.
```

**Kết quả kỳ vọng:** Văn bản đã ẩn — họ tên/email/SĐT/CCCD thành nhãn; mã phiếu `TK-2026-001`, tiền `350.000 VNĐ`, "Trung tâm CSKH" còn nguyên.
