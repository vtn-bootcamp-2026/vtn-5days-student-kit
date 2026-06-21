# Mermaid Starter — Template sơ đồ workflow cho non-tech

> Dùng khi HV yếu Mermaid (F4). Copy template gần nhất → điền → dán vào mermaid.live hoặc Antigravity.

## 1. Tuyến tính (as-is đơn giản nhất)

```mermaid
flowchart TD
  A[Bắt đầu: nhận yêu cầu] --> B[Xử lý bước 1]
  B --> C[Xử lý bước 2]
  C --> D[Lưu / gửi kết quả]
  D --> E[Kết thúc]
```

## 2. Có rẽ nhánh (to-be có AI/tự động)

```mermaid
flowchart TD
  A[Nhận input] --> B{Loại?}
  B -->|Dễ| C[Auto: AI xử lý]
  B -->|Khó| D[HITL: người duyệt]
  B -->|Không rõ| E[Unknown: dừng + log]
  C --> F[Xuất kết quả]
  D --> F
  E --> G[Báo lỗi]
```

## 3. Theo vai trò (swimlane)

```mermaid
flowchart LR
  subgraph VP[Văn phòng]
    A1[Nhận] --> A2[Phân loại]
  end
  subgraph KT[Kế toán]
    K1[Duyệt chi]
  end
  A2 --> K1
  K1 --> OUT[Xuất]
```

## Lỗi cú pháp thường gặp

| Lỗi | Sửa |
|---|---|
| Node id trùng | mỗi id duy nhất (A, B, C...) |
| Nhãn có ký tự đặc biệt | bọc `[...]` hoặc `(...)` |
| `-->` viết thành `->` | phải `-->` (2 dấu) |
| Subgraph thiếu `end` | mỗi `subgraph` cần 1 `end` |

> Mẹo: dán vào **mermaid.live** xem lỗi ngay; sửa đến khi render.
