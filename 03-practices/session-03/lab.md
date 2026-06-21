---
mo-ta: Hướng dẫn thực hành chi tiết cho học viên về tự động hóa văn phòng sử dụng n8n và trợ lý AI Gemini
trang-thai: active
phien-ban: v5.4
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-06-22 00:30 +07:00
---

# Hướng dẫn thực hành Session 3: Tự động hóa công việc văn phòng với n8n và AI Gemini

Tài liệu này cung cấp hướng dẫn thực hành từng bước chi tiết giúp học viên xây dựng và làm chủ các <span class="pill-academic">quy trình làm việc AI: AI workflow</span> từ cơ bản đến nâng cao trên nền tảng n8n, kết hợp sức mạnh phân tích và sinh nội dung của mô hình ngôn ngữ lớn Google Gemini.

---

## 1. Mục tiêu bài thực hành: Lab objectives

Sau khi hoàn thành các bài thực hành trong Session này, học viên có khả năng:
* Hiểu rõ và áp dụng thành thạo kiến trúc xương sống **Trigger → Node xử lý → Action** trong tự động hóa quy trình.
* Sử dụng thành thạo các nhóm node cốt lõi trong n8n bao gồm: Triggers, Data Transform, Flow Control, và Integration & AI.
* Kết nối và làm việc trực tuyến với dữ liệu bảng tính Google Sheets và dịch vụ thư điện tử Gmail thông qua cơ chế <span class="pill-academic">thông tin xác thực: credentials</span> chuẩn hóa.
* Tích hợp mô hình Google Gemini để giải quyết 2 bài toán thực chiến: phân loại dữ liệu phi cấu trúc (ép đầu ra dạng JSON có cấu trúc) và sinh nội dung thư điện tử cá nhân hóa.
* Thiết lập quy trình có kiểm soát của con người, đảm bảo an toàn thông tin trước khi thực hiện hành động nhạy cảm thông qua cơ chế <span class="pill-academic">con người phê duyệt: human-in-the-loop</span>.

---

## 2. Chuẩn bị môi trường: Environment setup

Học viên cần hoàn thành các bước chuẩn bị sau trước khi bắt đầu thực hành các bài tập:

1. **Tài khoản n8n:** Đăng nhập vào tài khoản n8n của bạn (có thể sử dụng bản cloud hoặc bản cài đặt self-hosted).
2. **Khóa API Google Gemini:** Truy cập Google AI Studio, tạo một <span class="pill-academic">khóa giao diện lập trình ứng dụng: API key</span> mới và lưu trữ bảo mật.
3. **Chuẩn bị dữ liệu bảng tính trên Google Drive:**
   * Tải các tệp Excel mẫu từ thư mục `synthetic-data/` về máy tính của bạn:
     * `ggsheet1_nhac_viec.xlsx` (Bài 1)
     * `ggsheet2_phan_anh.xlsx` (Bài 2)
     * `ggsheet3_soan_thao.xlsx` (Bài 3)
   * Tải các tệp này lên Google Drive cá nhân của bạn.
   * Mở từng tệp bằng **Google Sheets** trực tuyến để chuyển đổi chúng thành định dạng bảng tính Google Sheets hoạt động (n8n kết nối thông qua API trực tuyến, không làm việc trực tiếp với các tệp tin tĩnh trên máy).

---

## 3. Bài 1: Nhắc việc tồn đọng & gửi email tự động

### 3.1. Bối cảnh & Mục tiêu
Thiết lập một luồng tự động hóa hoàn toàn không sử dụng AI. Hệ thống sẽ tự động quét bảng theo dõi công việc vào khung giờ cố định mỗi sáng, lọc ra các công việc chưa hoàn thành, biên tập nội dung nhắc nhở, sau đó vừa ghi nhận nhật ký nhắc việc vừa gửi email cảnh báo trực tiếp đến người phụ trách.

* **Tệp dữ liệu sử dụng:** `ggsheet1_nhac_viec.xlsx` (đã chuyển thành Google Sheets).
* **Đầu ra mong muốn:** File quy trình `flow1_nhac_viec.json` chạy thành công.

### 3.2. Sơ đồ luồng thiết kế
```
Schedule Trigger (8h sáng) → Đọc CongViec → IF (Chưa hoàn thành) → Soạn nội dung nhắc
                                                                        ├─→ Ghi vào bảng NhacViec (Sheets)
                                                                        └─→ Gửi email nhắc (Gmail)
```

### 3.3. Các bước thực hiện chi tiết
1. **Bước 1: Thiết lập phương thức kích hoạt:**
   * Thêm node **Schedule Trigger** vào canvas.
   * Cấu hình trigger chạy định kỳ hàng ngày (Trigger Interval = Daily) vào lúc **08:00 AM**.
2. **Bước 2: Đọc bảng dữ liệu công việc:**
   * Thêm node **Google Sheets** (chọn action **Read**).
   * Tạo credential kết nối với tài khoản Google của bạn thông qua OAuth2.
   * Chọn bảng tính `ggsheet1_nhac_viec` và chỉ định Tab dữ liệu là **CongViec**.
3. **Bước 3: Lọc công việc chưa hoàn thành:**
   * Thêm nút rẽ nhánh điều kiện: **IF node**.
   * Cấu hình điều kiện lọc: Nếu cột `Trạng thái` **không bằng (is not equal to)** giá trị `Hoàn thành`.
4. **Bước 4: Soạn thảo nội dung nhắc việc:**
   * Thêm node **Edit Fields** (Data Transform) ở nhánh True của node IF.
   * Tạo trường dữ liệu mới tên là `noi_dung_nhac` với công thức kết hợp dữ liệu:
     `Việc '{{ $json.["Tên công việc"] }}' do {{ $json.["Người phụ trách"] }} phụ trách hiện chưa hoàn thành. Hạn chót: {{ $json.["Hạn chót"] }}.`
5. **Bước 5: Tách nhánh hành động song song:**
   * **Nhánh 1 (Ghi sổ nhắc việc):** Kéo kết nối từ node Edit Fields sang một node **Google Sheets** mới (chọn action **Append**). Kết nối với tab **NhacViec** để ghi nhận nhật ký gồm: `Nội dung nhắc`, `Người phụ trách`, và ngày nhắc (dùng hàm lấy ngày hiện tại).
   * **Nhánh 2 (Gửi email nhắc việc):** Kéo một đường kết nối khác từ node Edit Fields sang node **Gmail** (chọn action **Send Email**). Cấu hình gửi thư tới địa chỉ email của người phụ trách, tiêu đề thư là `[Nhắc việc] Dự án công việc tồn đọng`, phần nội dung thư nhúng trường dữ liệu `noi_dung_nhac` vừa soạn thảo.

> [!TIP]
> **TƯ DUY THIẾT KẾ SONG SONG:** Việc tách song song hai nhánh hành động từ một node Edit Fields giúp bạn thực hiện nhiều thao tác khác nhau (ghi nhật ký hệ thống và gửi thông báo trực tiếp) mà không cần phải nhân bản dữ liệu hay gọi đọc Sheets nhiều lần.

---

## 4. Bài 2: Trợ lý AI phân loại phản ánh

### 4.1. Bối cảnh & Mục tiêu
Sử dụng mô hình AI Gemini đóng vai trò trợ lý thông minh để đọc, hiểu và gán nhãn cho các ý kiến phản ánh nội bộ được gửi lên dưới dạng ngôn ngữ tự nhiên. AI sẽ phân loại phản ánh vào các nhóm cụ thể, đánh giá mức độ khẩn cấp và viết tóm tắt ngắn gọn, sau đó ghi trực tiếp kết quả này vào các cột tương ứng trên sheet.

* **Tệp dữ liệu sử dụng:** `ggsheet2_phan_anh.xlsx` (chuyển thành Google Sheets).
* **Đầu ra mong muốn:** File quy trình `flow2_phan_loai.json` chạy thành công.

### 4.2. Sơ đồ luồng thiết kế
```
Manual Trigger → Đọc PhanAnh → IF (Chưa phân loại) → Gemini phân tích → Tách kết quả AI → Ghi kết quả vào Sheet
```

### 4.3. Các bước thực hiện chi tiết
1. **Bước 1: Tạo trigger chạy thử:** Thêm node **Manual Trigger** để bạn chủ động bấm chạy thử nghiệm luồng từ giao diện thiết kế.
2. **Bước 2: Đọc dữ liệu phản ánh:** Thêm node **Google Sheets (Read)** kết nối tới tab **PhanAnh**.
3. **Bước 3: Lọc dòng chưa phân loại:** Thêm node **IF** để kiểm tra xem cột `Phân loại` hoặc `Mức độ` có bị rỗng hay không. Bước này giúp hệ thống chỉ xử lý những dòng phản ánh mới tinh, tránh gọi API Gemini lặp lại cho các dòng cũ đã được gán nhãn xong xuôi.
4. **Bước 4: Gọi mô hình AI Gemini phân tích:**
   * Thêm node **Google Gemini** (chọn action **Message a model**).
   * Cấu hình credential: Nhập API key Google Gemini của bạn.
   * Viết prompt chi tiết yêu cầu mô hình phân tích cột `Nội dung phản ánh` và trả về thông tin dưới dạng JSON có cấu trúc chứa đúng 3 khóa: `category` (Hạ tầng mạng / Nhân sự / Hành chính / CNTT / Khác), `priority` (Thấp / Trung bình / Cao), và `summary` (tóm tắt sự cố trong 1 câu).
5. **Bước 5: Trích xuất và định dạng JSON:**
   * Sử dụng tính năng ép kiểu phản hồi thành JSON của node Gemini (<span class="pill-academic">trình phân tích cú pháp đầu ra: output parser</span>).
   * Thêm node **Edit Fields** để trích xuất 3 trường dữ liệu trên từ kết quả phản hồi của AI.
6. **Bước 6: Ghi kết quả cập nhật lại Sheets:**
   * Thêm node **Google Sheets (Update)** để điền ngược lại các kết quả đã được cấu trúc hóa vào 3 cột tương ứng trên dòng dữ liệu gốc: `Phân loại`, `Mức độ`, và `Tóm tắt`.

---

## 5. Bài 3: Trợ lý AI soạn thảo email & quy trình duyệt

### 5.1. Bối cảnh & Mục tiêu
Sử dụng trợ lý AI ở cấp độ cao nhất — sinh nội dung email cá nhân hóa dựa trên vài ý chính đầu vào. Tuy nhiên, để đảm bảo tính chuẩn mực và an toàn thông tin, quy trình áp dụng mô hình <span class="pill-academic">con người phê duyệt: human-in-the-loop</span>. Quy trình được tách làm 2 phần:
* **Luồng 3A:** AI đọc yêu cầu từ sheet, soạn email mẫu, tạo bản nháp trên Gmail (Gmail Draft) và cập nhật sheet ở trạng thái "Chờ duyệt".
* **Luồng 3B:** Con người kiểm tra nội dung và duyệt trên Sheet bằng cách gõ "Gửi". Luồng 3B quét và tự động gửi email đi, chuyển trạng thái sang "Đã gửi".

* **Tệp dữ liệu sử dụng:** `ggsheet3_soan_thao.xlsx` (chuyển thành Google Sheets).
* **Đầu ra mong muốn:** File quy trình `flow3a_soan_nhap.json` và `flow3b_gui_email.json` chạy thành công.

### 5.2. Sơ đồ luồng thiết kế

**Luồng 3A — Soạn & tạo nháp:**
```
Bấm soạn nháp → Đọc SoanThao → IF (Chưa xử lý) → Gemini soạn thảo (JSON Output) → Tách nháp
                                                                                     ├─→ Tạo email nháp (Gmail Draft)
                                                                                     └─→ Ghi nháp vào Sheet (Trạng thái = "Chờ duyệt")
```

*Sau khi Luồng 3A chạy xong, con người mở Google Sheets, kiểm tra và chỉnh sửa nội dung, gõ chữ `Gửi` vào cột "Duyệt gửi" để phê duyệt.*

**Luồng 3B — Gửi sau khi duyệt:**
```
Bấm gửi → Đọc dòng đã duyệt → IF (Duyệt gửi = "Gửi" VÀ chưa "Đã gửi") → Gửi email (Gmail) → Đánh dấu "Đã gửi" + ghi nhận giờ gửi
```

### 5.3. Các bước thực hiện chi tiết
#### Thiết lập Luồng 3A:
1. **Đọc yêu cầu soạn thảo:** Thêm node **Google Sheets (Read)** kết nối tới tab **SoanThao**.
2. **Lọc dòng mới:** Dùng node **IF** kiểm tra xem cột `Trạng thái` có đang để trống hay không (chỉ xử lý các yêu cầu soạn thảo mới tinh).
3. **Soạn thảo email bằng AI:** Thêm node **Google Gemini**. Thiết lập Prompt hướng dẫn AI đóng vai trò thư ký chuyên nghiệp soạn thảo email hoàn chỉnh dựa trên các cột đầu vào: `Loại văn bản`, `Người nhận`, `Ý chính`, và `Giọng văn`.
4. **Tạo email nháp trên Gmail:** Thêm node **Gmail** (chọn action **Create Draft**). Nhập địa chỉ người nhận từ cột `Email người nhận`, tiêu đề và nội dung email lấy trực tiếp từ kết quả soạn thảo của Gemini.
5. **Cập nhật trạng thái chờ duyệt:** Thêm node **Google Sheets (Update)** để ghi lại tiêu đề, nội dung email hoàn chỉnh do AI viết vào sheet, đồng thời cập nhật cột `Trạng thái` thành `Chờ duyệt`.

#### Thiết lập Luồng 3B:
1. **Đọc dòng đã phê duyệt:** Thêm node **Google Sheets (Read)** để đọc lại toàn bộ tab **SoanThao**.
2. **Kiểm tra điều kiện duyệt:** Thêm node **IF** cấu hình điều kiện kép: Cột `Duyệt gửi` bằng giá trị `Gửi` **VÀ** cột `Trạng thái` không bằng `Đã gửi`.
3. **Thực hiện gửi email:** Thêm node **Gmail** (chọn action **Send Email**). Sử dụng nội dung email đã được phê duyệt/chỉnh sửa trên sheet để gửi đi.
4. **Đóng hồ sơ trạng thái:** Cập nhật cột `Trạng thái` thành `Đã gửi` và điền ngày giờ gửi vào cột `Ngày gửi` thông qua node **Google Sheets (Update)**.

---

## 6. Lỗi thường gặp và cách xử lý: Common errors & Trouble cards

<div class="trouble-card">
<h4>Thẻ xử lý lỗi số 1: Lỗi nghẽn hạn mức gọi API (Gemini API Quota 429)</h4>
<p><b>Triệu chứng:</b> Khi xử lý bảng dữ liệu có số lượng dòng lớn, node Gemini báo lỗi <code>The service is receiving too many requests</code> (lỗi vượt hạn mức 429 của tài khoản API miễn phí).</p>
<p><b>Cách khắc phục:</b>
1. Mở phần cấu hình (Settings) của node Gemini, kích hoạt tính năng <b>Retry On Fail</b>. Cấu hình số lần thử lại (Max Tries) từ 4-5 lần và khoảng thời gian chờ giữa các lần thử (Wait Between Tries) là 5000ms.
2. Nếu xử lý bảng dữ liệu cực lớn, hãy bọc node Gemini bên trong nút lặp qua các phần tử: <b>Loop Over Items</b> (thiết lập Batch Size = 1) kết hợp với một node <b>Wait</b> chờ khoảng 2-3 giây sau mỗi vòng lặp trước khi gửi request tiếp theo.</p>
</div>

<div class="trouble-card">
<h4>Thẻ xử lý lỗi số 2: Lỗi định dạng JSON trả về từ AI (Markdown JSON wrapper)</h4>
<p><b>Triệu chứng:</b> Trình phân tích cú pháp báo lỗi không thể đọc dữ liệu do Gemini trả về chuỗi JSON bị bọc trong cú pháp Markdown (ví dụ: <code>```json {"category": "CNTT"} ```</code>) thay vì chuỗi JSON thô.</p>
<p><b>Cách khắc phục:</b>
Thêm một node <b>Code</b> chạy JavaScript trung gian ngay sau node Gemini để làm sạch chuỗi văn bản trước khi phân tích cú pháp bằng đoạn mã sau:</p>
<pre><code class="language-javascript">let rawText = $input.item.json.ai_response; // Thay bằng tên biến chứa kết quả của bạn
rawText = rawText.replace(/```json/g, "").replace(/```/g, "").trim();
return { json: JSON.parse(rawText) };
</code></pre>
</div>

<div class="trouble-card">
<h4>Thẻ xử lý lỗi số 3: Lỗi mất thông tin định danh dòng gốc (Context loss)</h4>
<p><b>Triệu chứng:</b> Sau khi đi qua các node trung gian biến đổi dữ liệu (như node Gemini hoặc Code), các thông tin định danh gốc của dòng như chỉ số dòng <code>row_number</code> bị biến mất, khiến node Google Sheets (Update) phía sau không xác định được dòng cần ghi đè kết quả.</p>
<p><b>Cách khắc phục:</b>
Sử dụng tính năng ghim dữ liệu: <b>data pinning</b> (bấm biểu tượng ghim hoặc nhấn phím tắt <code>P</code>) ở node Google Sheets đầu tiên để cố định dữ liệu mẫu trong quá trình thiết kế, giúp các node phía sau luôn tham chiếu chính xác đến cấu trúc dữ liệu ban đầu bao gồm cả thông tin dòng gốc.</p>
</div>

---

## 7. Bài tập nâng cao: Advanced challenges

* **Thử thách 1 (Tích hợp Telegram cảnh báo):** Ở Bài 1, hãy nghiên cứu kết nối thêm node **Telegram** song song với nhánh Gmail để khi phát hiện công việc trễ hạn, hệ thống vừa gửi email vừa gửi một tin nhắn cảnh báo nhanh vào nhóm chat Telegram của đội ngũ.
* **Thử thách 2 (Tự động dịch thuật email):** Ở Bài 3, hãy bổ sung thêm cột `Ngôn ngữ` trong sheet yêu cầu soạn thảo. Thiết lập prompt của Gemini sao cho nếu cột ngôn ngữ yêu cầu là `Tiếng Anh`, AI sẽ tự động soạn thảo email hoàn chỉnh bằng tiếng Anh tương ứng với nội dung ý chính tiếng Việt được cung cấp.

---

## 8. Tiêu chí đánh giá bài thực hành: Definition of Done

Bài thực hành được coi là hoàn thành xuất sắc khi đáp ứng đủ các tiêu chí sau:
- [ ] Cả 3 quy trình workflow (`flow1_nhac_viec.json`, `flow2_phan_loai.json`, `flow3a_soan_nhap.json` và `flow3b_gui_email.json`) được xuất thành công dưới dạng tệp tin JSON và tải lên thư mục lưu trữ bài làm.
- [ ] Quy trình Bài 1 gửi email nhắc việc chính xác đến đúng địa chỉ hòm thư và ghi nhận thành công nhật trình nhắc vào sheet `NhacViec`.
- [ ] Quy trình Bài 2 phân loại chính xác các phản ánh mẫu vào các nhóm và cập nhật đầy đủ thông tin phân loại, mức độ, tóm tắt dạng JSON có cấu trúc vào sheet trực tuyến.
- [ ] Quy trình Bài 3A tạo được email nháp trên Gmail của học viên, cập nhật đúng trạng thái "Chờ duyệt". Quy trình Bài 3B chỉ gửi email đi khi học viên gõ chữ "Gửi" vào cột phê duyệt trên sheet.
- [ ] Toàn bộ các API key bảo mật đều được cấu hình trong phần credentials của n8n, tuyệt đối không được viết trực tiếp (hardcode) vào ô nhập prompt hoặc mã nguồn JavaScript.
