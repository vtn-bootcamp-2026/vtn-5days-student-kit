---
mo-ta: "Biểu mẫu mô tả chi tiết đặc tả thiết kế và cấu hình 3 agent nội bộ của nhóm thực hành"
trang-thai: active
phien-ban: v1.1
created-at: 2026-05-25 10:41 +07:00
updated-at: 2026-05-25 13:40 +07:00
---

# Bản đặc tả tác tử nội bộ: Agent specification

## 1. Thông tin chung của nhóm

| Trường thông tin | Nội dung chi tiết |
| :--- | :--- |
| **Mã nhóm thực hành** | *Ví dụ: Nhóm 03 - Vận hành mạng truyền dẫn* |
| **Hệ thống nền sử dụng** | *OpenClaw v1.4.0 / Hermes Agent v0.14.0 (Chọn một)* |
| **Mô hình ngôn ngữ cục bộ** | *Ví dụ: qwen3.5:7b-instruct hoặc gemma4:e2b* |
| **Thành viên & Phân vai** | *Ví dụ: Nguyễn Văn A (Hệ thống), Trần Thị B (Lập trình)...* |

---

## 2. Đặc tả Agent 1: Trợ lý tri thức vận hành mạng: tri-thuc-noi-bo

*Mô tả: Tác tử tra cứu tài liệu nội bộ, không có quyền thực thi, chỉ cung cấp thông tin đã được kiểm chứng.*

| Hạng mục cấu hình | Nội dung thiết lập của nhóm |
| :--- | :--- |
| **Tên định danh Agent** | `tri-thuc-noi-bo` |
| **Mô hình kết nối** | *Ví dụ: qwen3.5:7b-instruct hoặc gemma4:e2b* |
| **Môi trường thư mục làm việc** | Chỉ đọc: read-only thư mục `/docs/simulated/` |
| **Các công cụ được cấp quyền** | Chỉ được dùng các chức năng đọc tệp: read_file. **Nghiêm cấm** ghi tệp và chạy shell. |
| **Cơ chế enforce kỹ thuật** | `SOUL.md` + `pre_tool_call hook` chặn `write_file`, `patch`, `terminal`, `process`, `execute_code`; giới hạn thao tác đọc trong thư mục tài liệu mô phỏng (Docker sandbox + volume `:ro` là tùy chọn nâng cao). |
| **System Prompt chi tiết (Soul)** | *Dán đoạn System Prompt thực tế nhóm đã nạp vào tệp cấu hình của agent tại đây. Phải thể hiện rõ ràng ràng buộc về nguồn trích dẫn và cách phản hồi khi thiếu thông tin.* |
| **Hàng rào an toàn: guardrails** | Không bao giờ tự suy diễn cấu hình thiết bị. Không dùng kiến thức ngoài tài liệu cung cấp. |
| **Điểm chốt con người: HITL criteria** | Câu hỏi yêu cầu thay đổi cấu hình thực tế, hỏi về thông tin hạ tầng thật, hoặc hỏi ngoài phạm vi tài liệu mô phỏng. |

---

## 3. Đặc tả Agent 2: Trợ lý soạn thảo báo cáo ca trực: soan-thao-noi-dung

*Mô tả: Tác tử hỗ trợ viết lại, định dạng email/thông báo kỹ thuật từ các ghi chép thô, loại bỏ IP thật.*

| Hạng mục cấu hình | Nội dung thiết lập của nhóm |
| :--- | :--- |
| **Tên định danh Agent** | `soan-thao-noi-dung` |
| **Mô hình kết nối** | *Khuyến nghị dùng mô hình suy luận tốt hơn (ví dụ: qwen3.5:7b-instruct)* |
| **Môi trường thư mục làm việc** | Quyền ghi vào thư mục cách ly: sandbox `/drafts/` |
| **Các công cụ được cấp quyền** | Đọc tệp: read_file, viết tệp: write_file (giới hạn trong thư mục `/drafts/`). Chặn chạy shell. |
| **Cơ chế enforce kỹ thuật** | `SOUL.md` + `pre_tool_call hook` chặn shell; chỉ cho phép ghi file vào thư mục `/drafts/` (hoặc `~/vtn-lab/drafts/`) thông qua hook kiểm tra đường dẫn. |
| **System Prompt chi tiết (Soul)** | *Dán đoạn System Prompt thực tế nhóm đã dùng tại đây. Phải thể hiện cơ chế che giấu IP công cộng thật và chèn cảnh báo in đậm khi thiếu dữ kiện.* |
| **Hàng rào an toàn: guardrails** | Không tự thêm số liệu kỹ thuật giả định. Không để lộ IP công cộng thật. |
| **Điểm chốt con người: HITL criteria** | Báo cáo sự cố nghiêm trọng có liên quan đến cam kết chất lượng dịch vụ: SLA, báo cáo tài chính, hoặc chia sẻ thông tin cho đối tác ngoài VTN. |

---

## 4. Đặc tả Agent 3: Trợ lý checklist vận hành kỹ thuật: checklist-van-hanh

*Mô tả: Tác tử phân tích yêu cầu công việc và lập kế hoạch thực hiện an toàn qua 5 bước suy luận.*

| Hạng mục cấu hình | Nội dung thiết lập của nhóm |
| :--- | :--- |
| **Tên định danh Agent** | `checklist-van-hanh` |
| **Mô hình kết nối** | *Ví dụ: qwen3.5:7b-instruct hoặc gemma4:e2b* |
| **Môi trường thư mục làm việc** | Thư mục dự án cục bộ của nhóm. |
| **Các công cụ được cấp quyền** | Cho phép sử dụng các công cụ tìm kiếm và tự động ghi nhớ/tạo kỹ năng (Hermes Auto-Skill generation) nếu có. |
| **Cơ chế enforce kỹ thuật** | `SOUL.md` + hook chặn các lệnh nguy hiểm; mọi bước chuyển giao từ Pre-checks sang Execution bắt buộc phải được đánh dấu nhãn [ĐIỂM DỪNG CHỜ PHÊ DUYỆT]. |
| **System Prompt chi tiết (Soul)** | *Dán đoạn System Prompt thực tế nhóm đã dùng tại đây. Phải mô tả rõ cấu trúc 5 phần bắt buộc (Pre-checks, Execution, Post-checks, Stop & Rollback, HITL Approval).* |
| **Hàng rào an toàn: guardrails** | Không đề xuất các lệnh mang tính phá hoại hệ thống (ví dụ: format, delete) mà không có chốt phê duyệt thủ công. |
| **Điểm chốt con người: HITL criteria** | Mọi bước chuyển đổi từ kiểm tra (Pre-checks) sang thực hiện cấu hình (Execution) bắt buộc phải có nhãn [ĐIỂM DỪNG CHỜ PHÊ DUYỆT]. |

---

## 5. Nhật ký kết quả chạy thử (Bắt buộc chạy tối thiểu 6 ca)

*Lưu ý: Học viên thực hiện reset bộ nhớ hệ thống (Memory Clear Protocol) trước khi thực hiện các bài chạy thử độc lập.*

| Tên Agent | Prompt kiểm thử đầu vào | Nội dung phản hồi của Agent (Tóm tắt) | Đánh giá an toàn (Pass / Fail) | Ghi chú kỹ thuật (Lỗi gặp phải / Cách cải tiến Prompt) |
| :--- | :--- | :--- | :--- | :--- |
| `tri-thuc-noi-bo` | | | | |
| `tri-thuc-noi-bo` | | | | |
| `soan-thao-noi-dung`| | | | |
| `soan-thao-noi-dung`| | | | |
| `checklist-van-hanh`| | | | |
| `checklist-van-hanh`| | | | |
