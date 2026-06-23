---
mo-ta: bao cao co do do mau cho contract-003-risky
trang-thai: active
phien-ban: v1.0
created-at: 2026-05-26 16:00 +07:00
updated-at: 2026-05-26 16:00 +07:00
---

# Báo cáo cờ đỏ: Red-flag report mẫu

## Thông tin hợp đồng

| Trường | Giá trị |
| --- | --- |
| Mã hợp đồng | HD-VH-2026-003 |
| Loại | Dịch vụ vận hành và bảo trì hệ thống mạng |
| Giá trị | 1.800.000.000 VNĐ |
| Bên A | Công ty Cổ phần Viễn thông Mô phỏng (VTN-Sim) |
| Bên B | Công ty TNHH Dịch vụ Kỹ thuật Demo |
| Confidence | 0.65 |
| Cần xem xét | **CÓ** — needs_human_review = true |

## Tổng hợp cờ đỏ

| STT | Cờ đỏ | Mức độ | Điều khoản |
| --- | --- | --- | --- |
| 1 | Tự gia hạn với thời hạn thông báo quá ngắn | CAO | Điều 2 |
| 2 | Phạt vi phạm không giới hạn mức tối đa | CAO | Điều 4 |
| 3 | Giới hạn trách nhiệm quá thấp so với giá trị hợp đồng | CAO | Điều 5 |

---

## Chi tiết từng cờ đỏ

### Red Flag 1: Tự gia hạn với thời hạn thông báo quá ngắn

**Trích dẫn nguồn:**
> "Hợp đồng sẽ tự động gia hạn thêm 12 tháng mà không cần thông báo trước trừ khi một bên thông báo bằng văn bản chấm dứt trước 15 ngày so với ngày hết hạn."
> — Điều 2, HD-VH-2026-003

**Phân tích:**
- Thời hạn thông báo chấm dứt chỉ **15 ngày** — quá ngắn so với thông lệ 30-90 ngày trong ngành viễn thông.
- Hợp đồng trị giá **1.8 tỷ VNĐ/năm** — rủi ro tài chính lớn nếu lỡ deadline.
- Thông lệ ngành: hợp đồng O&M hệ thống mạng thường yêu cầu notice period 60-90 ngày để đảm bảo chuyển giao và tính liên tục dịch vụ.

**Hành động đề xuất:**
1. Đề xuất tăng notice period lên tối thiểu **60 ngày**.
2. Thêm điều kiện: gia hạn chỉ khi hai bên đồng ý bằng văn bản.
3. Nếu giữ auto-renewal: thêm điều khoản review hiệu suất trước khi gia hạn.

---

### Red Flag 2: Phạt vi phạm không giới hạn mức tối đa

**Trích dẫn nguồn:**
> "Phạt 5% giá trị hợp đồng hàng tháng cho mỗi giờ vượt. Không giới hạn mức phạt tối đa."
> — Điều 4, HD-VH-2026-003

**Phân tích:**
- Phạt **5% giá trị hợp đồng hàng tháng** (7.500.000 VNĐ) cho mỗi giờ vượt SLA.
- **Không có trần phạt** — nếu sự cố kéo dài 48 giờ: phạt = 48 × 7.5 triệu = **360 triệu VNĐ**, tương đương 20% giá trị hợp đồng.
- So sánh: contract-001 (truyền dẫn) có trần phạt 10%/quý — thông lệ hơn trong ngành.

**Hành động đề xuất:**
1. Đặt trần phạt tối đa — đề xuất **10-15% giá trị hợp đồng hàng tháng**.
2. Hoặc giới hạn tổng phạt không quá **giá trị hợp đồng 1 quý** (450 triệu).
3. Thêm quy định: phạt trừ vào hóa đơn tháng tiếp theo, không yêu cầu thanh toán riêng.

---

### Red Flag 3: Giới hạn trách nhiệm quá thấp

**Trích dẫn nguồn:**
> "Tổng trách nhiệm bồi thường của Bên B trong mọi trường hợp không vượt quá giá trị hợp đồng của 01 (một) tháng."
> — Điều 5, HD-VH-2026-003

**Phân tích:**
- Giới hạn trách nhiệm = **150.000.000 VNĐ** (1 tháng).
- Giá trị hợp đồng = **1.800.000.000 VNĐ** (12 tháng).
- Tỷ lệ trách nhiệm/giá trị = **8.3%** — quá thấp.
- Kịch bản rủi ro: nếu nhà cung cấp gây sự cố mạng lan rộng, thiệt hại cho doanh nghiệp viễn thông có thể vượt xa 150 triệu (mất doanh thu, đền bù khách hàng, uy tín).
- Đặc thù viễn thông: thời gian ngừng dịch vụ mạng tính bằng phút, không phải giờ. Mỗi phút downtime có thể ảnh hưởng hàng nghìn khách hàng.

**Hành động đề xuất:**
1. Đề xuất tăng giới hạn trách nhiệm lên tối thiểu **50% giá trị hợp đồng** (900 triệu).
2. Hoặc tách riêng: trách nhiệm trực tiếp (100% giá trị hợp đồng) vs. gián tiếp (1 tháng).
3. Bổ sung: loại trừ trách nhiệm cho thiệt hại gián tiếp là hợp lý, nhưng giới hạn tổng thể quá thấp.

---

## Kiến nghị tổng thể

| Ưu tiên | Hành động | Người phụ trách |
| --- | --- | --- |
| KHẨN CẤP | Đàm phán lại 3 cờ đỏ trước khi ký | Giám đốc + Pháp chế |
| CAO | Bổ sung điều khoản giải quyết tranh chấp (hiện đang thiếu) | Pháp chế |
| CAO | Yêu cầu Bên B cung cấp chứng nhận bảo hiểm trước khi ký | Nhân sự hợp đồng |
| TRUNG BÌNH | So sánh với điều khoản chuẩn hợp đồng O&M mạng nội bộ | Kỹ thuật mạng |

**Kết luận:** Hợp đồng có **3 cờ đỏ mức CAO** và **1 trường thiếu** (giải quyết tranh chấp). Khuyến nghị **không ký** ở dạng hiện tại. Cần đàm phán lại các điều khoản 2, 4, 5 và bổ sung điều khoản giải quyết tranh chấp.
