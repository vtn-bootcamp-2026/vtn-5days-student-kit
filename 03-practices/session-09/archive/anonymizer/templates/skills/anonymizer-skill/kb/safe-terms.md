---
mo-ta: "Danh sach cac thuat ngu ky thuat, chi so SCADA, ten doanh nghiep KHONG duoc che giau"
trang-thai: active
phien-ban: v1.0
created-at: "2026-05-27 10:00 +07:00"
updated-at: "2026-05-27 10:00 +07:00"
---

# Safe Terms — Danh sách thuật ngữ KHÔNG được che giấu

> **Mục đích**: Ngăn chặn lọc nhầm (over-redaction). Các thuật ngữ dưới đây có vẻ giống PII nhưng KHÔNG phải.

## 1. Số đo vật lý SCADA

Các giá trị số thập phân trong ngữ cảnh đo lường kỹ thuật:
- `0.912.345.678 dB` — số đo công suất tín hiệu (decibel)
- `45.678 MHz` — tần số
- `12.345 ms` — độ trễ
- `99.97%` — tỷ lệ uptime

**Quy tắc nhận diện**: Số thập phân đi kèm đơn vị đo (dB, MHz, ms, %, GHz, km, V, A, W).

## 2. Mã serial thiết bị

Chuỗi số dạng mã tham chiếu thiết bị:
- `9876-5432-1012` — serial thiết bị viễn thông (12 chữ số có gạch ngang)
- `VTN-RTR-001` — mã thiết bị nội bộ

**Quy tắc nhận diện**: Dạng `xxxx-xxxx-xxxx` (4-4-4 có gạch ngang) hoặc có tiền tố thiết bị. Dù bỏ gạch ngang ra 12 chữ số giống CCCD → KHÔNG được che giấu.

## 3. Tên doanh nghiệp, tổ chức

Các tên có vẻ giống tên người nhưng là pháp nhân:
- `Viễn thông Hoàng Long` — tên doanh nghiệp đối tác
- `Công ty CP VTN` — tên pháp nhân
- `Tổ chuyên trách anhvan` — tên tổ kỹ thuật

**Quy tắc nhận diện**: Đi kèm từ chỉ tổ chức ("Công ty", "Viễn thông", "Tổ", "Phòng", "Ban", "Trung tâm").

## 4. Email tổ chức/kỹ thuật

Email không phải cá nhân mà là email chung của bộ phận:
- `anhvan-support@viettel.com.vn` — hòm thư tổ chuyên trách
- `noc@viettel.com.vn` — hòm thư NOC
- `support@viettel.com.vn` — hòm thư hỗ trợ

**Quy tắc nhận diện**: Prefix chứa dấu gạch ngang hoặc từ chức năng (`-support`, `noc`, `admin`, `info`, `helpdesk`).

## 5. Thuật ngữ kỹ thuật viễn thông

Các từ có dấu tiếng Việt trùng tên người:
- `định tuyến` — không phải tên "Tuyến"
- `báo cáo` — không phải tên "Cáo"
- `vận hành` — không phải tên "Hành"

## Cách sử dụng trong Anonymizer

```python
def is_safe_term(text, position, context):
    """
    Kiểm tra xem PII candidate có phải là safe term không.
    Trả về True nếu KHÔNG nên che giấu.
    """
    # 1. Kiểm tra đơn vị đo lường gần vị trí phát hiện
    # 2. Kiểm tra prefix thiết bị hoặc tổ chức
    # 3. Kiểm tra email chức năng
    # 4. Gửi context đến LLM để xác minh ngữ cảnh
    pass
```
