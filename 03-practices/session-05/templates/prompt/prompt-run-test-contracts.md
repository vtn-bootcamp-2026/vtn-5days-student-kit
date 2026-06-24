---
mo-ta: Lời nhắc kích hoạt skill review-contract chạy thử nghiệm trên các hợp đồng mẫu
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 22:45 +07:00
updated-at: 2026-06-23 22:45 +07:00
---

# Lời nhắc chạy thử nghiệm kĩ năng (BT2.5)

Đặt các file hợp đồng mẫu từ `synthetic-data/contracts/` vào thư mục `review-contract/data/contracts/`. Sau đó, sử dụng các câu lệnh dưới đây để yêu cầu Agent thực hiện rà soát.

## Ca 1: Kiểm thử với hợp đồng bình thường (`contract-001.docx`)

```text
Rà soát hợp đồng `review-contract/data/contracts/contract-001.docx` và trích xuất điều khoản.
```

## Ca 2: Kiểm thử với hợp đồng thiếu thông tin (`contract-002.docx`)

```text
Rà soát hợp đồng `review-contract/data/contracts/contract-002.docx` và trích xuất điều khoản.
```

## Ca 3: Kiểm thử với hợp đồng chứa các điều khoản rủi ro (`contract-003-risky.docx`)

```text
Rà soát hợp đồng `review-contract/data/contracts/contract-003-risky.docx` và phát hiện cờ đỏ rủi ro.
```
