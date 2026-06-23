---
mo-ta: Tài liệu hướng dẫn thực hành n8n tự động hóa văn phòng với AI Gemini cho nhân viên Viettel Network
trang-thai: active
phien-ban: v1.6
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-23 08:15 +07:00
---

# TÀI LIỆU THỰC HÀNH n8n — VIETTEL NETWORK

### Tự động hóa công việc văn phòng với n8n + AI Gemini

> **Giảng viên:** Th.S Nguyễn Minh Cường
> **Đối tượng:** Nhân viên văn phòng Viettel Network
> **Mạch học:** 3 bài tăng dần độ khó — từ cơ bản thuần (chỉ dùng Google Sheets), nâng cao tích hợp đa dịch vụ (Sheets + Gmail), đến AI sinh nội dung + quy trình duyệt.

Mỗi workflow đều theo kiến trúc xương sống **Trigger → Node xử lý → Action**, và xoay quanh nhóm node cốt lõi đã học (Triggers · Data Transform · Flow Control · Integration & AI).

---

## Chuẩn bị chung (làm 1 lần trước khi vào 3 bài)

| Hạng mục | Ghi chú |
|---|---|
| Tài khoản n8n | Bản cloud hoặc self-hosted đều được |
| Credential **Google Sheets** | Kết nối tài khoản Google (OAuth2) |
| Credential **Gmail** | Kết nối tài khoản Google (OAuth2) — dùng cho Bài 2 & 3 |
| Credential **Google Gemini** | Loại "Google Gemini (PaLM) API"; lấy API key tại Google AI Studio — dùng cho Bài 3 |
| File Google Sheet mẫu | Tải file `.xlsx` kèm theo → **Upload lên Google Drive → mở bằng Google Sheets** (n8n nói chuyện với Google Sheets online, không đọc file tĩnh) |

**Quy tắc vàng về bảo mật (áp dụng cả 3 bài):** API key luôn để trong *credential* của n8n, không nhúng thẳng vào luồng. Với hành động quan trọng (gửi email), giữ nguyên tắc **human-in-the-loop** — AI soạn, con người duyệt và bấm gửi.

---

## Bài 1: Nhắc việc tồn đọng & ghi nhật ký qua Google Sheets

**File:** `flow1_nhac_viec_sheets.json` · `ggsheet1_nhac_viec.xlsx`

**Mục tiêu sư phạm:** nắm trọn cơ chế tự động hóa cơ bản *chưa cần AI* — máy tự chạy theo lịch, tự lọc dữ liệu và tự động cập nhật ghi sổ trực tuyến trên Google Sheets.

**Bối cảnh:** mỗi sáng hệ thống tự động đọc bảng công việc, lọc ra các việc chưa hoàn thành, tự động soạn thảo nội dung nhắc nhở cá nhân hóa và lưu vào nhật ký nhắc việc trên Google Sheets.

**Sơ đồ luồng:**

```
Lịch 8h sáng → Đọc CongViec → IF (chưa hoàn thành) → Soạn nội dung nhắc → Ghi vào bảng NhacViec
```

**Cấu trúc Google Sheet:**

- Tab **CongViec** (người nhập): `Tên công việc` · `Người phụ trách` · `Trạng thái` · `Hạn chót` · `Email`
- Tab **NhacViec** (hệ thống ghi): `Nội dung nhắc` · `Người phụ trách` · `Ngày nhắc`

**Node sử dụng:** Schedule Trigger (Triggers) · Google Sheets Read/Append (Integration) · IF (Flow Control) · Edit Fields (Data Transform).

**Điểm dạy:** Cơ chế làm việc cơ bản với Google Sheets (đọc dữ liệu từ một tab, xử lý điều kiện, chuyển đổi và ghi đè/thêm mới sang tab khác), giúp học viên làm quen với kiến trúc tự động hóa **Trigger → Node xử lý → Action**.

---

## Bài 2: Nhắc việc tồn đọng & gửi email tự động qua Google Sheets và Gmail

**File:** `flow2_nhac_viec_gmail.json` · `ggsheet1_nhac_viec.xlsx`

**Mục tiêu sư phạm:** kết hợp đa hành động và gửi email tự động — làm quen với việc xử lý song song hai nhánh hành động từ cùng một nguồn dữ liệu (vừa ghi nhật ký vào Google Sheets, vừa gửi email nhắc nhở qua Gmail).

**Bối cảnh:** mỗi sáng hệ thống tự động quét danh sách công việc chưa hoàn thành, soạn thảo nội dung nhắc nhở cá nhân hóa và thực hiện đồng thời việc ghi nhận nhật ký nhắc nhở vào Google Sheets và gửi email trực tiếp cho người phụ trách qua Gmail.

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

**Điểm dạy:** Sau bước soạn nội dung nhắc, luồng **tách thành hai nhánh song song** để thực hiện đồng thời hai tác vụ: ghi nhật ký nhắc nhở vào Google Sheets và gửi email thông báo trực tiếp cho người phụ trách qua Gmail từ cùng một nguồn dữ liệu ban đầu. Điều này minh họa trực quan cho tư duy "một nguồn dữ liệu, nhiều hành động xử lý song song".

---

## Bài 3: Trợ lý AI soạn thảo email & quy trình duyệt

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

## Tổng kết — bản đồ kỹ năng

| Bài | Vai trò của AI | Khái niệm cốt lõi |
|---|---|---|
| 1 | (chưa dùng AI) | Cơ chế Trigger–Action, làm việc với Google Sheets |
| 2 | (chưa dùng AI) | Tách nhánh song song, tích hợp đa dịch vụ (Sheets + Gmail) |
| 3 | Sinh nội dung hoàn chỉnh | Prompt định hướng + human-in-the-loop |

## Lưu ý kỹ thuật thường gặp

**Lỗi 429 — "The service is receiving too many requests"**
Gemini bị gọi quá nhiều lần một lúc (thường do bảng nhiều dòng + API key miễn phí hạn mức thấp). Cách xử lý:

1. Bật **Retry On Fail** cho node Gemini (Settings → Max Tries 4–5, Wait 5000ms) — đã cấu hình sẵn trong file Bài 3.
2. Nếu xử lý nhiều dòng: bọc node AI trong **Loop Over Items** (mỗi lần 1 dòng) + nối **Wait** vài giây.
3. Triển khai thật quy mô lớn: bật billing cho project Google Cloud để nâng hạn mức.

**Hai cách gọi Gemini**

- Node **"Message a model"** (Gemini gốc): kéo-thả, dễ dạy; đọc kết quả ở `content.parts[0].text`. Có cổng "Tools" để trống — vô hại, là chỗ gắn công cụ nâng cao (AI Agent).
- Node **HTTP Request**: gọi thẳng API; đọc kết quả ở `candidates[0].content.parts[0].text`. Không có cổng Tools.
- Cả hai đều soạn/được việc như nhau vì cùng gọi một model.

## Danh sách file đính kèm

- `flow1_nhac_viec_sheets.json` + `ggsheet1_nhac_viec.xlsx`
- `flow2_nhac_viec_gmail.json` + `ggsheet1_nhac_viec.xlsx`
- `flow3a_soan_nhap.json` + `flow3b_gui_email.json` + `ggsheet3_soan_thao.xlsx`

---
*Tài liệu phục vụ đào tạo nội bộ — Alobase × Viettel Network.*
