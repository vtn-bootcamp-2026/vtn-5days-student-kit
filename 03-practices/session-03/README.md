---
mo-ta: Mục tiêu và đầu ra của Session 3 tự động hóa công việc văn phòng với n8n và AI Gemini
trang-thai: active
phien-ban: v2.2
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-22 00:30 +07:00
---

# Session 3: Tự động hóa công việc văn phòng với n8n và AI Gemini

## Mục tiêu

Làm quen và làm chủ các nút cơ bản của n8n và tích hợp mô hình ngôn ngữ lớn (Google Gemini) để xây dựng luồng tự động hóa công việc văn phòng thông qua 3 bài thực hành từ cơ bản đến nâng cao.

## Đầu vào

- Dữ liệu bảng tính Google Sheets: `ggsheet1_nhac_viec.xlsx`, `ggsheet2_phan_anh.xlsx`, `ggsheet3_soan_thao.xlsx` (được tải lên Google Drive và mở dưới dạng Google Sheets trực tuyến).
- Tài khoản n8n (bản đám mây: cloud hoặc tự lưu trữ: self-hosted).
- <span class="pill-academic">Thông tin xác thực: credentials</span> của Google Sheets, Gmail, và Google Gemini API key.

## Đầu ra

- Quy trình Bài 1: `flow1_nhac_viec.json` chạy tự động nhắc việc tồn đọng và gửi email.
- Quy trình Bài 2: `flow2_phan_loai.json` sử dụng AI để đọc, hiểu và gán nhãn phản ánh thành JSON có cấu trúc.
- Quy trình Bài 3: `flow3a_soan_nhap.json` (soạn thảo và tạo nháp email) và `flow3b_gui_email.json` (gửi sau khi duyệt với cơ chế <span class="pill-academic">con người phê duyệt: human-in-the-loop</span>).

## Phân công

Học viên làm việc độc lập hoặc theo nhóm dưới sự hướng dẫn của giảng viên và trợ giảng để thiết lập tài khoản, kết nối API và kéo thả xây dựng quy trình trên n8n.

## Checklist

Đối chiếu yêu cầu hoàn thành và các hướng dẫn chi tiết trong tệp [lab.md](lab.md) và danh sách kiểm tra trong [checklist.md](checklist.md).
