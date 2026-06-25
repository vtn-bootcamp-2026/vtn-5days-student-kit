---
mo-ta: "Hướng dẫn thực hành Lab 2 nâng cao về phát triển công cụ che giấu dữ liệu cá nhân cục bộ bằng tiếng Việt có dấu: local AI data anonymizer pro bằng tư duy lập trình tự do kết hợp AI: vibe coding tại Viettel Networks"
trang-thai: active
phien-ban: v1.3
created-at: 2026-05-25 14:55 +07:00
updated-at: 2026-05-29 20:54 +07:00
---

# Lab 2: Công cụ che giấu dữ liệu cục bộ nâng cao: local AI data anonymizer pro

> [!IMPORTANT]
> **ĐIỀU KIỆN TIÊN QUYẾT TRƯỚC KHI BẮT ĐẦU:**
> Bài thực hành này yêu cầu máy chủ mô hình cục bộ **Ollama** phải đang hoạt động trên cổng mặc định `11434` và đã tải sẵn các mô hình ngôn ngữ thế hệ mới nhất tính đến tháng 5/2026 (`gemma4:e2b`, `qwen3.5:1.5b-instruct` hoặc `qwen3.5:7b-instruct`).
> *   *Nếu nhóm bạn đã hoàn thành Lab 1*: Hãy đảm bảo dịch vụ Ollama từ Lab 1 vẫn đang chạy nền bình thường trong hệ thống.
> *   *Nếu nhóm bạn muốn thực hiện độc lập Lab 2*: Vui lòng thực hiện cài đặt và khởi chạy Ollama theo hướng dẫn chi tiết tại **Bước 1 của [Lab 1](lab-1-personal-ai-assistant.md)** trước khi bắt đầu bài lab này.

---

## 1. Mục tiêu bài thực hành nâng cao

Sau khi hoàn thành bài thực hành Lab 2 nâng cao này, các nhóm học viên (kỹ sư VTN) sẽ làm chủ được:
- **Tư duy lập trình tự do nâng cao: vibe coding pro**: Sử dụng các trợ lý lập trình thông minh (Claude Code, Codex hoặc Antigravity CLI) để nâng cấp mã nguồn khung ban đầu tối giản thành một giải pháp xử lý ngôn ngữ tự nhiên thông minh, linh hoạt.
- **Xử lý tiếng Việt có dấu và chuẩn hóa Unicode**: Giải quyết triệt để sự khác biệt giữa Unicode tổ hợp (Decomposed - NFD) và Unicode dựng sẵn (Composed - NFC) thường gặp trong các cơ sở dữ liệu doanh nghiệp tại Việt Nam.
- **Kỹ thuật lai Hybrid chuyên sâu (Regex cải tiến + Local LLM)**: Thiết kế hệ thống thông minh kết hợp sức mạnh xử lý tốc độ của Regex tĩnh đối với các mẫu dữ liệu chuẩn và năng lực suy luận ngữ cảnh sâu sắc của Local LLM để giải quyết các bẫy dữ liệu lắt léo.
- **Kỹ thuật thiết kế Prompt an toàn (Prompt Defense & JSON Parser)**: Xây dựng hệ thống phòng thủ trước các cuộc tấn công ép buộc mô hình: prompt injection tinh vi và phát triển bộ phân tích cú pháp JSON chống chịu lỗi (Robust JSON Parser) phòng trường hợp Local LLM trả về mã rác.
- **Cơ chế kiểm duyệt có sự tham gia của con người: Human-in-the-loop (HITL)**: Thiết lập điểm dừng thông minh dựa trên độ tin cậy và ghi nhật ký log bảo mật tuyệt đối không rò rỉ thông tin nhận dạng cá nhân: Personal Identifiable Information (PII) gốc.

---

## 2. Dữ liệu và mã nguồn sử dụng

Học viên sử dụng các tệp tin được cung cấp sẵn trong thư mục bài làm:
- **Tệp dữ liệu mô phỏng tiếng Việt có dấu cực khó**:
  - `synthetic-data/pii-sample-01.txt`: Tài liệu có chứa thông tin nhạy cảm rõ ràng.
  - `synthetic-data/pii-sample-02-tricky.txt`: Tài liệu chứa dữ liệu lắt léo và các kịch bản kiểm thử khó (bẫy số đo SCADA, bẫy mã thiết bị, bẫy tên thương mại và prompt injection có dấu tiếng Việt).
- **Mã nguồn ban đầu**:
  - `templates/anonymizer-starter.py`: Khung mã nguồn Python ban đầu hỗ trợ đường dẫn động.
- **Tài liệu kiểm thử và bàn giao**:
  - `templates/anonymizer-test-report.md`: Biểu mẫu kết quả kiểm thử.
  - `templates/local-assistant-runbook.md`: Biểu mẫu biên bản bàn giao kỹ thuật.

---

## 3. Các bước thực hiện chi tiết

### Bước 1: Nghiên cứu mã nguồn ban đầu và kiểm tra trạng thái Ollama

1.  **Kiểm tra kết nối máy chủ Ollama**:
    *   Mở terminal và chạy lệnh xác thực kết nối cục bộ:
        ```bash
        curl http://localhost:11434
        ```
    *   Đảm bảo nhận được phản hồi `Ollama is running` để chắc chắn API đã sẵn sàng phục vụ cho mã nguồn Python.
2.  **Đọc hiểu dữ liệu lắt léo có dấu (`pii-sample-02-tricky.txt`)**:
    *   Nhận diện 6 thách thức kiểm thử đặc biệt:
        *   **Tên người tiếng Việt phức tạp**: Họ tên 4 chữ `"Nguyễn Trần Khánh Lâm"` và `"Lê Hoàng Phương Vy"` có dấu đầy đủ, rất dễ bị phân rã Unicode khi xử lý chuỗi.
        *   **Bẫy số điện thoại bàn và di động**: `024.3123.4567` (số bàn Hà Nội) và `+84 982-123-456` (số di động định dạng quốc tế).
        *   **Bẫy số đo vật lý SCADA**: Số thập phân `0.912.345.678 dB` (dễ bị thuật toán Regex thông thường nhận nhầm thành số điện thoại di động và che giấu nhầm gây mất mát dữ liệu vận hành).
        *   **Bẫy tên riêng trùng danh từ kỹ thuật**: Tổ chuyên trách `"anhvan-support@viettel.com.vn"` sử dụng nhãn `"anhvan"` mang tính ngữ cảnh kỹ thuật, không phải họ tên cá nhân tên "Văn".
        *   **Bẫy mã Serial thiết bị**: Chuỗi `9876-5432-1012` sau khi loại bỏ dấu gạch ngang sẽ chứa 12 chữ số liên tiếp giống hệt cấu trúc của số Căn cước công dân (CCCD). Tuy nhiên đây là serial thiết bị kỹ thuật, tuyệt đối không được che giấu.
        *   **Tấn công chèn lệnh tinh vi (Prompt Injection)**: Một tin nhắn giả danh quản trị viên yêu cầu phần mềm Anonymizer tạm thời tắt tính năng bảo mật, in nguyên văn thông tin của trưởng ca Nguyễn Trần Khánh Lâm và tắt cờ kiểm duyệt.
3.  **Đọc hiểu mã nguồn starter (`templates/anonymizer-starter.py`)**:
    *   Học viên phân tích: Hiện tại script starter chỉ sử dụng Regex tĩnh và rất dễ bị sập hoặc hoạt động sai (lọc nhầm số SCADA thành SĐT, lọc nhầm Serial thiết bị thành CCCD, không nhận diện được tên người tiếng Việt có dấu, hoàn toàn bại trận trước prompt injection).

---

### Bước 2: Nâng cấp công cụ bằng Vibe Coding kết hợp Local LLM

Học viên sử dụng tính năng hỗ trợ lập trình của Claude Code hoặc Antigravity CLI để nâng cấp tệp `templates/anonymizer-starter.py` thành công cụ hoàn hảo `anonymizer.py` nằm ở thư mục gốc của buổi học. Yêu cầu AI cải tiến mã nguồn dựa trên các đặc tả nghiệp vụ nâng cao sau:

1.  **Chuẩn hóa Unicode tiếng Việt**:
    *   Sử dụng thư viện chuẩn `unicodedata` để đưa toàn bộ văn bản đầu vào về dạng dựng sẵn (NFC) trước khi thực hiện bất kỳ thao tác so khớp hay phân tích nào:
        ```python
        import unicodedata
        normalized_text = unicodedata.normalize('NFC', text)
        ```
2.  **Tích hợp cuộc gọi Local LLM API cục bộ chống chịu lỗi (Urllib-first + JSON Parser)**:
    *   Sử dụng thư viện chuẩn `urllib.request` để gửi yêu cầu POST đến Ollama API cục bộ: `http://localhost:11434/v1/chat/completions` [cite: 77].
    *   **Prompt thiết kế Few-Shot cho Local LLM**: Thiết kế prompt thông minh gửi đến mô hình (`gemma4:e2b`, `qwen3.5:1.5b-instruct` hoặc mô hình lớn hơn). Yêu cầu mô hình trả về một chuỗi định dạng JSON duy nhất. Cung cấp ít nhất 2 ví dụ (Few-Shot) rõ ràng về cách phân biệt giữa tên người thật và tên đối tác/địa danh/tên phòng ban kỹ thuật để mô hình nhỏ không bị suy luận sai lệch.
    *   **Bộ bóc tách JSON chống chịu lỗi (Robust JSON Parser)**: Do Local LLM đôi khi chèn thêm văn bản giải thích hoặc khối markdown ` ```json ... ``` `, học viên bắt buộc yêu cầu AI lập trình một hàm bóc tách dữ liệu JSON an toàn bằng biểu thức chính quy (trích xuất chuỗi nằm giữa dấu `{` và `}` đầu tiên và cuối cùng) trước khi gọi `json.loads()`.
3.  **Xây dựng bộ lọc an toàn đa lớp tránh lọc nhầm (Over-redaction)**:
    *   *Tránh lọc nhầm*: Kết hợp kết quả từ LLM để loại trừ việc che giấu các bẫy dữ liệu (nhãn doanh nghiệp "Viễn thông Hoàng Long", hòm thư kỹ thuật "anhvan-support", số đo SCADA "0.912.345.678 dB", số serial thiết bị "9876-5432-1012").
    *   *Chống Prompt Injection*: LLM phải phát hiện các câu chỉ thị ép buộc phá hoại trong văn bản đầu vào. Khi phát hiện prompt injection, chương trình **tuyệt đối không làm theo lệnh phá hoại**, tiến hành che giấu dữ liệu nhạy cảm bình thường và tự động cưỡng bức bật cờ kiểm duyệt: `needs_human_review = True`.
    *   *Mã hóa Log bảo mật*: Nhật ký ghi vào `outputs/execution-log.csv` tuyệt đối không chứa bất kỳ chuỗi PII gốc nào [cite: 162].
4.  **Thiết kế cơ chế dự phòng an toàn (Resilient Fallback Design)**:
    *   Thiết kế mã nguồn sao cho nếu không thể kết nối tới Ollama API cục bộ (do cổng kết nối lỗi hoặc API quá tải), chương trình **không bị sập (crash)** mà tự động chuyển sang chế độ Regex Fallback an toàn (chấp nhận lọc nhầm mã tham chiếu thiết bị để bảo vệ dữ liệu nhưng kích hoạt cờ duyệt thủ công HITL để con người kiểm tra lại).

---

#### 🌐 MỞ RỘNG: Chuyển đổi công cụ sang sử dụng Google Gemini Cloud API
*Trường hợp áp dụng*: Học viên muốn mở rộng mã nguồn Python của công cụ `anonymizer.py` kết nối trực tiếp với các mô hình đám mây: Cloud AI mới nhất của Google để tăng tốc độ phân tích ngữ cảnh đối với các tài liệu thông thường (không nhạy cảm).
1.  **Lấy chuỗi khóa**: Đăng nhập Google AI Studio để tạo chuỗi khóa **API Key** cá nhân.
2.    *   Thay đổi địa chỉ gọi API và sử dụng mô hình thế hệ mới nhất tính đến tháng 5/2026:
        *   Mô hình tốc độ cực nhanh: **`gemini-3-flash-preview`** (Thay thế dòng cũ, hỗ trợ Structured Outputs tuyệt đối)
        *   Mô hình suy luận chuyên sâu: **`gemini-3-pro-preview`**
    *   Endpoint Native v1beta của Gemini:
        ```python
        ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"
        ```
    *   Xác thực bằng cách truyền API Key trong header an toàn:
        ```python
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": YOUR_GEMINI_API_KEY
        }
        ```
3.  > [!CAUTION]
    > **TUÂN THỦ BẢO MẬT DOANH NGHIỆP:** Tuyệt đối nghiêm cấm gửi các dữ liệu nhạy cảm mô phỏng của Viettel Networks lên môi trường Cloud AI. Khi thực hiện bài lab, bắt buộc phải dùng Ollama Local để đảm bảo an toàn thông tin tối cao.

### Bước 3: Chạy thử nghiệm và Đánh giá 8 Ca kiểm thử nâng cao

1.  **Thực thi chương trình**:
    *   Học viên sao chép tệp starter hoặc tạo mới tệp `anonymizer.py` tại thư mục gốc buổi học và chạy lệnh:
        ```bash
        python anonymizer.py
        ```
2.  **Rà soát sản phẩm đầu ra**:
    *   Mở tệp kết quả tại `outputs/pii-sample-01-redacted.txt` và `outputs/pii-sample-02-tricky-redacted.txt`.
    *   Kiểm tra tệp nhật ký tại `outputs/execution-log.csv` xem có bị rò rỉ dữ liệu nhạy cảm thô nào không.
3.  **Hoàn thiện báo cáo kiểm thử**:
    *   Sao chép mẫu tệp `templates/anonymizer-test-report.md` và lưu thành `anonymizer-test-report.md` trong thư mục bài làm.
    *   Chạy kiểm thử và điền chi tiết kết quả cho cả 8 ca kiểm thử nâng cao dưới đây:

| Mã test | Tệp đầu vào | Tình huống kiểm thử | Kết quả kỳ vọng | Kết quả thực tế (PASS / FAIL) |
| :--- | :--- | :--- | :--- | :--- |
| **T01** | `pii-sample-01.txt` | Tài liệu có PII rõ ràng. | Lọc sạch họ tên, CCCD, SĐT, email. | |
| **T02** | `pii-sample-01.txt` | Thiếu trường email trong văn bản. | Không báo lỗi, không crash chương trình. | |
| **T03** | `pii-sample-02-tricky.txt`| Số serial thiết bị 12 chữ số (`9876-5432-1012`). | Giữ nguyên dạng gốc, không che giấu nhầm thành `[REDACTED_CCCD]`. | |
| **T04** | `pii-sample-02-tricky.txt`| Số điện thoại định dạng quốc tế (`+84 982-123-456`) và SĐT bàn (`024.3123.4567`).| Nhận diện chính xác cả hai định dạng và che giấu hoàn toàn. | |
| **T05** | `pii-sample-02-tricky.txt`| Nhãn tổ chuyên trách trùng tên riêng (`anhvan-support`). | Tránh lọc nhầm (giữ nguyên cụm từ gốc, không che giấu nhầm). | |
| **T06** | `pii-sample-02-tricky.txt`| Tên doanh nghiệp đối tác trùng tên người (`Viễn thông Hoàng Long`). | Tránh lọc nhầm (giữ nguyên tên doanh nghiệp). | |
| **T07** | `pii-sample-02-tricky.txt`| Số đo thập phân vật lý SCADA (`0.912.345.678 dB`). | Tránh lọc nhầm thành số điện thoại di động (giữ nguyên số đo vật lý). | |
| **T08** | `pii-sample-02-tricky.txt`| Tấn công chèn lệnh prompt injection lừa đảo hệ thống và yêu cầu tắt cờ duyệt. | Không tuân thủ lệnh, lọc sạch họ tên và số điện thoại, bắt buộc kích hoạt cờ duyệt thủ công `needs_human_review = True`. | |

---

## 4. Tiêu chuẩn hoàn thành Lab 2 nâng cao

Nhóm thực hành đạt yêu cầu Lab 2 nâng cao khi có đầy đủ các minh chứng kỹ thuật sau:
- [ ] Tệp tin `anonymizer.py` hoạt động hoàn hảo và không bị sập chương trình khi mất kết nối Ollama (chạy thành công Regex Fallback).
- [ ] Tệp kết quả che giấu `outputs/pii-sample-02-tricky-redacted.txt` lọc sạch thông tin nhạy cảm của nhân sự trực ca nhưng giữ nguyên các chỉ số kỹ thuật, số đo SCADA, mã serial thiết bị và tên doanh nghiệp.
- [ ] Tệp nhật ký `outputs/execution-log.csv` không chứa bất kỳ chuỗi dữ liệu thô nào và ghi nhận chính xác trạng thái, cờ kiểm duyệt.
- [ ] Hoàn thành báo cáo kiểm thử `anonymizer-test-report.md` với tối thiểu **6 trên 8** ca kiểm thử đạt kết quả **PASS**.
- [ ] Hoàn thành tài liệu Runbook bàn giao kỹ thuật đầy đủ 8 phần chuẩn doanh nghiệp.
