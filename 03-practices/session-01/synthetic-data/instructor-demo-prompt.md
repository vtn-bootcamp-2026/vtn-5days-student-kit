---
mo-ta: Hướng dẫn prompt mẫu nâng cao và kết quả đầu ra dự kiến của prompt phân tích, làm sạch dữ liệu log NOC giả lập cho giảng viên thị phạm tại lớp.
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-26 11:00 +07:00
updated-at: 2026-05-26 11:27 +07:00
---

# Demo dẫn nhập của giảng viên - phân tích & lọc PII log NOC 100+ dòng

Tài liệu này chứa prompt mẫu nâng cao, dữ liệu log NOC giả lập và kết quả đầu ra dự kiến tương ứng dành cho giảng viên thực hiện **Phần A: Demo dẫn nhập** tại lớp.

## 1. Prompt thị phạm (dành cho giảng viên)

Giảng viên copy toàn bộ nội dung prompt dưới đây dán vào Antigravity IDE hoặc công cụ tương đương khi thực hiện demo:

```text
Bạn là một Chuyên gia Vận hành NOC (NOC L2/L3 Specialist). 
Tôi cung cấp cho bạn một file dữ liệu NOC gồm hơn 100 cảnh báo giả lập dưới dạng CSV bên dưới.

Nhiệm vụ của bạn:
1. Lọc và làm sạch (Sanitize/Mask) toàn bộ thông tin cá nhân nhạy cảm (PII) như Tên người liên hệ, Số điện thoại, Email xuất hiện trong cột `summary`. Hãy thay thế chúng bằng nhãn "[REDACTED_PII]".
2. Phân loại số lượng cảnh báo theo từng loại thiết bị (device_type) dưới dạng bảng thống kê (Switch, Router, Firewall, Server, UPS, Base-station).
3. Trích xuất toàn bộ các cảnh báo ở mức "critical" (nguy kịch) còn đang mở ("open"), dịch nội dung lỗi sang tiếng Việt dễ hiểu và đề xuất hành động khắc phục nhanh (HITL - Human-in-the-loop).
4. Do các cảnh báo nguy kịch đang mở (critical & open) có thể không chứa PII nhạy cảm, hãy chủ động bổ sung một bảng đối chiếu minh họa kết quả làm sạch PII thực tế trên một số dòng log tiêu biểu có chứa PII từ dữ liệu đầu vào. Để bảo mật tuyệt đối, thông tin nhạy cảm ở cột "Dữ liệu trước khi lọc" trong bảng minh họa này phải được chủ động làm mờ một phần bằng các ký tự ẩn (ví dụ: Nguyen Van A -> Ngu*** A, 0987654321 -> 098*****21).
5. Lưu toàn bộ báo cáo phân tích và làm sạch dữ liệu cảnh báo NOC ở trên dưới dạng một tập tin Markdown tại đường dẫn tương đối: "outputs/noc-alert-sanitized-report.md".

Ràng buộc an toàn:
- Tuyệt đối không để lộ bất kỳ thông tin số điện thoại hay email cá nhân nào ở đầu ra.
- Chỉ sử dụng dữ liệu được cung cấp, không tự suy đoán hoặc vẽ thêm lỗi ngoài dữ liệu.
- Phản hồi hoàn toàn bằng tiếng Việt, trình bày Markdown sạch sẽ, chuyên nghiệp.

Dữ liệu log NOC mô phỏng:
"""
[GIẢNG VIÊN COPY NỘI DUNG TỪ TỆP synthetic-data/sample-noc-alerts.csv VÀ DÁN VÀO ĐÂY]
"""
```

## 2. Dữ liệu mẫu (20 dòng đầu tiên để test nhanh)

Nếu giảng viên muốn test nhanh hoặc chạy thử trong môi trường giới hạn token, có thể copy đoạn dữ liệu 20 dòng mẫu chứa PII dưới đây:

```csv
alert_id,timestamp,site_code,device_type,severity,summary,status
ALERT-001,2026-05-01 08:02:00,TEST_SITE_018,server,high,database query latency spike in performance test [Contact: Nguyen Van A (0987654321)],open
ALERT-002,2026-05-01 21:16:00,TEST_SITE_009,switch,low,interface flap in synthetic log,open
ALERT-003,2026-05-01 23:59:00,TEST_SITE_026,server,high,unauthorized login attempt simulated in audit log,resolved
ALERT-004,2026-05-01 21:35:00,TEST_SITE_010,server,low,disk space low on simulated system drive,in-progress
ALERT-005,2026-05-01 22:56:00,TEST_SITE_004,firewall,high,session table capacity warning (simulated),in-progress
ALERT-006,2026-05-02 01:25:00,TEST_SITE_010,base-station,low,RF module communication failure in lab environment,in-progress
ALERT-007,2026-05-01 10:31:00,TEST_SITE_018,ups,high,communication failure with network card in test,open
ALERT-008,2026-05-01 21:37:00,TEST_SITE_027,base-station,low,power backup warning in training scenario,resolved
ALERT-009,2026-05-01 21:52:00,TEST_SITE_012,base-station,high,RF module communication failure in lab environment [Assigned to: Nguyen Hoang E (0912345678)],open
ALERT-010,2026-05-01 15:21:00,TEST_SITE_022,ups,medium,communication failure with network card in test,resolved
ALERT-011,2026-05-01 11:56:00,TEST_SITE_008,ups,low,bypass mode activated for maintenance demo,resolved
ALERT-012,2026-05-01 09:50:00,TEST_SITE_023,router,medium,packet loss above simulated threshold on uplink,in-progress
ALERT-013,2026-05-01 18:03:00,TEST_SITE_020,firewall,medium,high memory usage alert on training cluster [Contact: Nguyen Van A (0987654321)],in-progress
ALERT-014,2026-05-01 14:22:00,TEST_SITE_020,server,medium,disk space low on simulated system drive,in-progress
ALERT-015,2026-05-01 11:50:00,TEST_SITE_026,firewall,medium,session table capacity warning (simulated),open
ALERT-016,2026-05-01 21:54:00,TEST_SITE_005,router,low,packet loss above simulated threshold on uplink,resolved
ALERT-017,2026-05-01 16:32:00,TEST_SITE_011,ups,critical,communication failure with network card in test,in-progress
ALERT-018,2026-05-01 17:53:00,TEST_SITE_019,base-station,low,RF module communication failure in lab environment,open
ALERT-019,2026-05-01 09:24:00,TEST_SITE_010,firewall,medium,security policy update failed in sandbox,resolved
ALERT-020,2026-05-02 02:45:00,TEST_SITE_006,server,medium,unauthorized login attempt simulated in audit log,in-progress
```

## 3. Kết quả đầu ra kỳ vọng của prompt thị phạm (dành cho giảng viên)

Dưới đây là kết quả đầu ra chuẩn hóa (output) kỳ vọng của mô hình ngôn ngữ lớn khi chạy prompt thị phạm ở trên với toàn bộ dữ liệu 115 cảnh báo NOC:

---

### Báo cáo phân tích và làm sạch dữ liệu cảnh báo NOC

> [!NOTE]
> Báo cáo này được thực hiện bởi Chuyên gia Vận hành NOC (NOC L2/L3 Specialist) dựa trên dữ liệu log giả lập được cung cấp từ tập tin [sample-noc-alerts.csv](../synthetic-data/sample-noc-alerts.csv).

---

#### 1. Làm sạch thông tin cá nhân nhạy cảm: PII sanitization

Toàn bộ thông tin cá nhân nhạy cảm (PII) như tên người liên hệ, số điện thoại và email xuất hiện trong trường mô tả lỗi (`summary`) đã được lọc sạch và thay thế hoàn toàn bằng nhãn an toàn `[REDACTED_PII]` nhằm tuân thủ quy chuẩn an toàn thông tin của VTN.

##### Cú pháp chuyển đổi tổng quát cho các mẫu dữ liệu:
- **Thông tin liên hệ dạng số điện thoại:** `[Contact: [Tên người liên hệ] ([Số điện thoại])]` $\rightarrow$ `[Contact: [REDACTED_PII]]`
- **Thông tin liên hệ dạng email:** `[Contact: [Tên người liên hệ] ([Địa chỉ email])]` $\rightarrow$ `[Contact: [REDACTED_PII]]`
- **Ghi chú vận hành trạm:** `[Operator notes: contact engineer [Tên kỹ sư] at [Địa chỉ email] if alert persists]` $\rightarrow$ `[Operator notes: contact [REDACTED_PII] if alert persists]`
- **Thông tin sở hữu phiếu sự cố:** `[Ticket owner: [Tên người sở hữu] - [Địa chỉ email]]` $\rightarrow$ `[Ticket owner: [REDACTED_PII]]`

---

#### 2. Thống kê cảnh báo theo loại thiết bị: device type

Tổng cộng có **115 cảnh báo** được ghi nhận và phân loại chi tiết theo từng loại thiết bị như sau:

| Loại thiết bị | Tên tiếng Anh | Số lượng cảnh báo | Tỷ lệ (%) |
| :--- | :--- | :---: | :---: |
| máy chủ | server | 23 | 20.0% |
| trạm phát sóng vô tuyến | base-station | 19 | 16.5% |
| thiết bị chuyển mạch | switch | 18 | 15.7% |
| tường lửa | firewall | 18 | 15.7% |
| bộ lưu điện | UPS | 22 | 19.1% |
| thiết bị định tuyến | router | 15 | 13.0% |
| **Tổng cộng** | | **115** | **100%** |

---

#### 3. Danh sách cảnh báo nguy kịch: critical còn đang mở: open

Qua rà soát hệ thống, có **03 cảnh báo** thuộc mức độ nghiêm trọng nguy kịch: `critical` và đang ở trạng thái chưa xử lý: `open`. Trong 3 cảnh báo này, trường mô tả lỗi gốc không chứa thông tin cá nhân PII nên nội dung sau khi làm sạch trùng khớp với nội dung gốc. 

Chi tiết thông tin sự cố, bản dịch nghĩa tiếng Việt và đề xuất hành động khắc phục nhanh (quy trình có sự tham gia của con người: Human-in-the-loop (HITL)):

##### 🚨 Cảnh báo ALERT-040
- **Mã trạm:** `TEST_SITE_034`
- **Thời gian xảy ra:** `2026-05-01 23:56:00`
- **Loại thiết bị:** Trạm phát sóng vô tuyến: base-station
- **Mô tả gốc (đã khử PII):** `"power backup warning in training scenario"`
- **Dịch nghĩa tiếng Việt:** Cảnh báo nguồn điện dự phòng (máy phát điện hoặc hệ thống ắc quy phụ) gặp sự cố hoặc đang phải chạy ở chế độ dự phòng trong kịch bản diễn tập.
- **Hành động khắc phục đề xuất (HITL):**
  1. Liên hệ ngay với đội ngũ kỹ thuật trực ca tại trạm `TEST_SITE_034` để kiểm tra trực quan tủ nguồn, máy phát điện và hệ thống ắc quy phụ.
  2. Xác minh trạng thái của bộ chuyển nguồn tự động: ATS (automatic transfer switch).
  3. Kiểm tra xem có xảy ra sự cố mất nguồn điện lưới hay không để phối hợp với điện lực địa phương nếu cần.

##### 🚨 Cảnh báo ALERT-058
- **Mã trạm:** `TEST_SITE_013`
- **Thời gian xảy ra:** `2026-05-01 19:41:00`
- **Loại thiết bị:** Trạm phát sóng vô tuyến: base-station
- **Mô tả gốc (đã khử PII):** `"RF module communication failure in lab environment"`
- **Dịch nghĩa tiếng Việt:** Lỗi mất kết nối truyền thông ở mô-đun vô tuyến: RF module trong môi trường phòng thí nghiệm.
- **Hành động khắc phục đề xuất (HITL):**
  1. Yêu cầu kỹ sư vận hành phòng lab kiểm tra kết nối vật lý của cáp tín hiệu RF và cáp quang feeder nối đến mô-đun.
  2. Đo đạc và kiểm tra nguồn cấp điện đầu vào cho mô-đun vô tuyến.
  3. Tiến hành khởi động lại mềm (soft reset) thiết bị qua bảng điều khiển quản trị; nếu không thành công, thực hiện khởi động lại cứng (hard reboot) bằng cách ngắt nguồn vật lý.

##### 🚨 Cảnh báo ALERT-081
- **Mã trạm:** `TEST_SITE_020`
- **Thời gian xảy ra:** `2026-05-01 13:48:00`
- **Loại thiết bị:** Thiết bị chuyển mạch: switch
- **Mô tả gốc (đã khử PII):** `"high broadcast traffic detected in lab subnet"`
- **Dịch nghĩa tiếng Việt:** Phát hiện lưu lượng gói tin quảng bá: broadcast traffic vượt ngưỡng cho phép ở mức nguy hiểm trong phân mạng phòng thí nghiệm.
- **Hành động khắc phục đề xuất (HITL):**
  1. Kiểm tra cấu hình và rà soát tô-pô mạng trên thiết bị chuyển mạch: switch tại trạm `TEST_SITE_020` để phát hiện hiện tượng vòng lặp mạng: loop mạng (do giao thức Spanning Tree Protocol - STP bị lỗi hoặc cấu hình sai).
  2. Rà soát danh sách các cổng đang có lưu lượng tăng đột biến để xác định nguồn phát quảng bá (ví dụ: máy trạm bị nhiễm mã độc hoặc thiết bị lỗi phần cứng liên tục gửi gói tin lỗi).
  3. Tạm thời kích hoạt tính năng kiểm soát bão quảng bá: storm control trên các cổng liên quan để cô lập lưu lượng lỗi và bảo vệ tài nguyên hệ thống.

---

#### 4. Minh họa kết quả làm sạch PII thực tế trên một số dòng log tiêu biểu

Để chứng minh thuật toán làm sạch PII hoạt động hiệu quả trên dữ liệu thực tế của tập tin [sample-noc-alerts.csv](../synthetic-data/sample-noc-alerts.csv), dưới đây là bảng đối chiếu trước và sau khi làm sạch của một số bản ghi tiêu biểu trong log hệ thống (Dữ liệu gốc dưới đây đã được chúng tôi chủ động làm mờ một phần để bảo mật tuyệt đối trước khi đưa vào bảng đối chiếu):

| Mã cảnh báo | Dữ liệu gốc (Đã che mờ bảo mật) | Dữ liệu sau khi làm sạch (Kết quả thực tế) |
| :---: | :--- | :--- |
| **ALERT-001** | `database query latency spike in performance test [Contact: Ngu*** A (098*****21)]` | `database query latency spike in performance test [Contact: [REDACTED_PII]]` |
| **ALERT-009** | `RF module communication failure in lab environment [Assigned to: Ngu*** E (091*****78)]` | `RF module communication failure in lab environment [Assigned to: [REDACTED_PII]]` |
| **ALERT-023** | `database query latency spike in performance test [Contact: Tr*** B (tr***@vtn.com.vn)]` | `database query latency spike in performance test [Contact: [REDACTED_PII]]` |
| **ALERT-043** | `spanning tree topology change detected [Operator notes: contact engineer L*** C at l***@vtn.vn if alert persists]` | `spanning tree topology change detected [Operator notes: contact [REDACTED_PII] if alert persists]` |
| **ALERT-070** | `session table capacity warning (simulated) [Ticket owner: Ph*** D - p***@vtn.com.vn]` | `session table capacity warning (simulated) [Ticket owner: [REDACTED_PII]]` |
