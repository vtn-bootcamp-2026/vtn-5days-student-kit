# Quy trình mẫu (as-is) — Tổng hợp báo cáo nhân sự hằng tuần

> Dùng cho lab S2: vẽ hiện trạng → ESIA → Mermaid. Quy trình thủ công hiện tại (mô phỏng).

## Bối cảnh
Phòng HCNS tổng hợp báo cáo nhân sự hằng tuần cho Giám đốc. Hiện làm thủ công.

## Các bước hiện tại (as-is)
1. Nhân viên HCNS nhắn nhủ (Zalo/email) đôn đốc 5 phòng gửi báo cáo nhân sự tuần. *(thủ công, dễ quên)*
2. 5 phòng soạn báo cáo theo **format riêng** (Word/Excel khác cấu trúc), gửi lại qua email.
3. Nhân viên HCNS mở từng file, **copy-paste số liệu** vào 1 file Excel tổng.
4. Tính lại tay các cột tổng (số NV hiện tại, nghỉ việc, tuyển mới, biến động).
5. Vẽ biểu đồ trong Excel, chụp ảnh, dán vào báo cáo Word.
6. Soạn email đính kèm báo cáo, gửi Giám đốc.
7. Lưu file vào thư mục (tên file không chuẩn).

## Điểm nghẽn / lỗi lặp
- Bước 1: quên đôn đốc → nộp trễ.
- Bước 2: format không đồng nhất → bước 3 tốn thời gian.
- Bước 3-4: copy-paste sai số, tính nhẩm lỗi.
- Bước 7: tên file lộn xộn, khó tìm lại.

## Gợi ý ESIA
- Eliminate: bước nhắn nhủ đôn đốc → tự động nhắc.
- Simplify: đồng nhất template báo cáo 5 phòng.
- Integrate: gom email/Sheet về 1 nguồn.
- Automate: AI chuẩn hóa + tổng hợp + xuất báo cáo chuẩn (→ chính là lab S4).
