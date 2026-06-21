---
mo-ta: Tài liệu hướng dẫn thực hành n8n tự động hóa văn phòng với AI Gemini cho nhân viên Viettel Network
trang-thai: active
phien-ban: v1.5
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-22 00:30 +07:00
---

# TÀI LIỆU THỰC HÀNH n8n — VIETTEL NETWORK

### Tự động hóa công việc văn phòng với n8n + AI Gemini

> **Giảng viên:** Th.S Nguyễn Minh Cường
> **Đối tượng:** Nhân viên văn phòng Viettel Network
> **Mạch học:** 3 bài tăng dần độ khó — từ cơ chế thuần, đến AI phân loại, đến AI sinh nội dung + quy trình duyệt.

Mỗi workflow đều theo kiến trúc xương sống **Trigger → Node xử lý → Action**, và xoay quanh nhóm node cốt lõi đã học (Triggers · Data Transform · Flow Control · Integration & AI).

---

## CHUẨN BỊ CHUNG (làm 1 lần trước khi vào 3 bài)

| Hạng mục | Ghi chú |
|---|---|
| Tài khoản n8n | Bản cloud hoặc self-hosted đều được |
| Credential **Google Sheets** | Kết nối tài khoản Google (OAuth2) |
| Credential **Gmail** | Kết nối tài khoản Google (OAuth2) — dùng cho Bài 1 & 3 |
| Credential **Google Gemini** | Loại "Google Gemini (PaLM) API"; lấy API key tại Google AI Studio — dùng cho Bài 2 & 3 |
| File Google Sheet mẫu | Tải file `.xlsx` kèm theo → **Upload lên Google Drive → mở bằng Google Sheets** (n8n nói chuyện với Google Sheets online, không đọc file tĩnh) |

**Quy tắc vàng về bảo mật (áp dụng cả 3 bài):** API key luôn để trong *credential* của n8n, không nhúng thẳng vào luồng. Với hành động quan trọng (gửi email), giữ nguyên tắc **human-in-the-loop** — AI soạn, con người duyệt và bấm gửi.

---

## BÀI 1 — NHẮC VIỆC TỒN ĐỌNG & GỬI EMAIL TỰ ĐỘNG

**File:** `flow1_nhac_viec.json` · `ggsheet1_nhac_viec.xlsx`

**Mục tiêu sư phạm:** nắm trọn cơ chế tự động hóa *chưa cần AI* — máy tự chạy theo lịch, tự lọc, tự ghi sổ và tự gửi nhắc.

**Bối cảnh:** mỗi sáng hệ thống đọc bảng công việc, lọc ra việc chưa hoàn thành, ghi vào sổ nhắc và gửi email tới đúng người phụ trách.

**Sơ đồ luồng:**

```
Lịch 8h sáng → Đọc CongViec → IF (chưa hoàn thành) → Soạn nội dung nhắc
                                                          ├─→ Ghi vào bảng NhacViec
                                                          └─→ Gửi email nhắc (Gmail)
```

**Cấu trúc Google Sheet:**

- Tab **CongViec** (người nhập): `Tên công việc` · `Người phụ trách` · `Trạng thái` · `Hạn chót` · `Email`
- Tab **NhacViec** (hệ thống ghi): `Nội dung nhắc` · `Người phụ trách` · `Ngày nhắc`

**Node sử dụng:** Schedule Trigger (Triggers) · Google Sheets Read/Append (Integration) · IF (Flow Control) · Edit Fields (Data Transform) · Gmail (Integration).

**Điểm dạy:** sau bước soạn nội dung, luồng **tách hai nhánh song song** từ cùng một nguồn dữ liệu (một nhánh ghi sổ, một nhánh gửi mail) — minh họa tư duy "một dữ liệu, nhiều hành động".

---

## BÀI 2 — TRỢ LÝ AI PHÂN LOẠI PHẢN ÁNH

**File:** `flow2_phan_loai.json` · `ggsheet2_phan_anh.xlsx`

**Mục tiêu sư phạm:** lần đầu đưa AI vào luồng — vai trò **đọc – hiểu – gán nhãn**. Cùng một cột phản ánh viết tự do, AI tự điền các cột kết quả có cấu trúc.

**Bối cảnh:** nhân viên gửi phản ánh nội bộ bằng ngôn ngữ tự nhiên; Gemini đọc và phân loại nhóm, đánh giá mức độ, tóm tắt một câu.

**Sơ đồ luồng:**

```
Bấm chạy thử → Đọc PhanAnh → IF (chưa phân loại) → Gemini phân tích → Tách kết quả AI → Ghi kết quả vào Sheet
```

**Cấu trúc Google Sheet — tab PhanAnh:**

- Người nhập: `Nội dung phản ánh`
- AI điền: `Phân loại` (Hạ tầng mạng / Nhân sự / Hành chính / CNTT / Khác) · `Mức độ` (Thấp / Trung bình / Cao) · `Tóm tắt`

**Vai trò AI nổi bật:** ép Gemini trả về **JSON có cấu trúc** thay vì văn bản tự do — đây chính là minh họa sống cho khái niệm *Output Parser*.

**Node sử dụng:** Manual Trigger (Triggers) · Google Sheets Read/Update (Integration) · IF (Flow Control) · Gemini (Integration & AI) · Edit Fields (Data Transform).

**Điểm dạy:** bước IF "chỉ xử lý dòng chưa phân loại" giúp chạy lại nhiều lần mà không tốn lượt gọi AI cho dòng đã xử lý.

---

## BÀI 3 — TRỢ LÝ AI SOẠN THẢO EMAIL + QUY TRÌNH DUYỆT

**File:** `flow3a_soan_nhap.json` · `flow3b_gui_email.json` · `ggsheet3_soan_thao.xlsx`

**Mục tiêu sư phạm:** vai trò AI cao nhất — **sinh nội dung** — kết hợp quy trình **con người duyệt** trước khi gửi. Vì có bước chờ người, luồng tách làm hai: 3A soạn & tạo nháp, 3B gửi sau khi duyệt. Cột **"Duyệt gửi"** trong Sheet đóng vai trò "nút phê duyệt".

**Sơ đồ luồng 3A — Soạn & tạo nháp:**

```
Bấm soạn nháp → Đọc SoanThao → IF (chưa xử lý) → Gemini soạn thảo (jsonOutput) → Tách nháp
                                                                                    ├─→ Tạo email nháp (Gmail Draft)
                                                                                    └─→ Ghi nháp vào Sheet (Trạng thái = "Chờ duyệt")
```

**→ Con người mở Sheet, đọc/sửa nội dung, gõ chữ `Gửi` vào cột "Duyệt gửi" cho dòng nào ưng.**

**Sơ đồ luồng 3B — Gửi sau khi duyệt:**

```
Bấm gửi → Đọc dòng đã duyệt → IF (Duyệt gửi = "Gửi" VÀ chưa "Đã gửi") → Gửi email (Gmail) → Đánh dấu "Đã gửi" + giờ gửi
```

**Cấu trúc Google Sheet — tab SoanThao:**

- Người nhập: `Loại văn bản` · `Người nhận` · `Email người nhận` · `Ý chính` · `Giọng văn`
- AI / hệ thống điền: `Tiêu đề` · `Nội dung hoàn chỉnh` · `Trạng thái` · `Ngày gửi`
- Con người gõ tay: `Duyệt gửi`

**Vai trò AI nổi bật:** từ vài gạch đầu dòng + cột "Loại văn bản"/"Giọng văn", Gemini soạn ra email hoàn chỉnh. *Đổi 2 ô định hướng là ra văn bản khác hẳn* — dạy được cả bài về Prompt (chữ **P** trong PCTF).

**Node sử dụng:** Manual Trigger (Triggers) · Google Sheets Read/Update (Integration) · IF (Flow Control) · Gemini "Message a model" (Integration & AI) · Edit Fields (Data Transform) · Gmail Draft & Send (Integration).

---

## TỔNG KẾT — BẢN ĐỒ KỸ NĂNG

| Bài | Vai trò của AI | Khái niệm cốt lõi |
|---|---|---|
| 1 | (chưa dùng AI) | Cơ chế Trigger–Action, tách nhánh song song |
| 2 | Đọc – phân loại – gán nhãn | Output có cấu trúc (JSON) |
| 3 | Sinh nội dung hoàn chỉnh | Prompt định hướng + human-in-the-loop |

## LƯU Ý KỸ THUẬT THƯỜNG GẶP

**Lỗi 429 — "The service is receiving too many requests"**
Gemini bị gọi quá nhiều lần một lúc (thường do bảng nhiều dòng + API key miễn phí hạn mức thấp). Cách xử lý:

1. Bật **Retry On Fail** cho node Gemini (Settings → Max Tries 4–5, Wait 5000ms) — đã cấu hình sẵn trong file Bài 3.
2. Nếu xử lý nhiều dòng: bọc node AI trong **Loop Over Items** (mỗi lần 1 dòng) + nối **Wait** vài giây.
3. Triển khai thật quy mô lớn: bật billing cho project Google Cloud để nâng hạn mức.

**Hai cách gọi Gemini**

- Node **"Message a model"** (Gemini gốc): kéo-thả, dễ dạy; đọc kết quả ở `content.parts[0].text`. Có cổng "Tools" để trống — vô hại, là chỗ gắn công cụ nâng cao (AI Agent).
- Node **HTTP Request**: gọi thẳng API; đọc kết quả ở `candidates[0].content.parts[0].text`. Không có cổng Tools.
- Cả hai đều soạn/được việc như nhau vì cùng gọi một model.

## DANH SÁCH FILE ĐÍNH KÈM

- `flow1_nhac_viec.json` + `ggsheet1_nhac_viec.xlsx`
- `flow2_phan_loai.json` + `ggsheet2_phan_anh.xlsx`
- `flow3a_soan_nhap.json` + `flow3b_gui_email.json` + `ggsheet3_soan_thao.xlsx`

---
*Tài liệu phục vụ đào tạo nội bộ — Alobase × Viettel Network.*
