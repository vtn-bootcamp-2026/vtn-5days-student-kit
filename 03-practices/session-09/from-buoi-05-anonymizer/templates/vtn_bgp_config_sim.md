---
mo-ta: "Tài liệu cấu hình BGP mô phỏng dành cho bài thực hành Lab 1 tại VTN"
trang-thai: active
phien-ban: v1.0
created-at: "2026-06-15 06:10 +07:00"
updated-at: "2026-06-15 06:10 +07:00"
---

# Tài liệu mô phỏng: cấu hình BGP cơ bản tại VTN

## 1. Mục đích
Tài liệu này mô tả khái niệm cơ bản về BGP và quy trình cấu hình mô phỏng dành cho bài lab đào tạo. Không dùng cho hệ thống thật.

## 2. BGP là gì
BGP, Border Gateway Protocol, là giao thức định tuyến dùng để trao đổi thông tin định tuyến giữa các hệ tự trị, Autonomous System, trên mạng diện rộng.

## 3. Quy trình cấu hình BGP mô phỏng
1. Kiểm tra trạng thái router trước thay đổi.
2. Xác định số AS nội bộ và AS láng giềng.
3. Khai báo tiến trình BGP mô phỏng.
4. Khai báo neighbor mô phỏng.
5. Kiểm tra trạng thái phiên BGP.
6. Ghi log kết quả kiểm tra.

## 4. Điều kiện dừng
Nếu phiên BGP không lên trạng thái Established trong thời gian kiểm thử, dừng thao tác và chuyển cho kỹ sư vận hành bậc 2.

## 5. Lưu ý an toàn
Không áp dụng trực tiếp nội dung này lên thiết bị thật.
