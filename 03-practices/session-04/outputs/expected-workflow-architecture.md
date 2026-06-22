---
mo-ta: Mo ta kien truc quy trinh lam viec AI hoan chinh va cac nhanh re dieu kien cho hoc vien doi chieu
trang-thai: active
phien-ban: v1.2
created-at: 2026-05-23 15:15 +07:00
updated-at: 2026-05-23 15:50 +07:00
---

# Kiến trúc quy trình làm việc AI phân loại sự cố thông minh hoàn chỉnh

Tài liệu này mô tả chi tiết sơ đồ kiến trúc luồng dữ liệu đầu-cuối (<span class="pill-academic">kiến trúc đầu-cuối: end-to-end architecture</span>) của hệ thống tự động hóa xử lý yêu cầu sự cố công nghệ thông tin sử dụng trí tuệ nhân tạo. Học viên sử dụng sơ đồ này làm đích đến để đối chiếu và lắp ghép các cấu phần trên <span class="pill-academic">công cụ tự động hóa quy trình: n8n</span>.

> [!TIP]
> **ĐÁP ÁN BÀI LAB:** Ban tổ chức cung cấp sẵn tệp cấu trúc quy trình hoàn chỉnh (đáp án quy trình n8n) tại liên kết tương đối: [smart-ticket-triage-solution-workflow.json](smart-ticket-triage-solution-workflow.json). Giảng viên sử dụng tệp này để đối chiếu kết quả, hoặc học viên có thể dùng để nhập trực tiếp (import) vào n8n của mình nhằm tự kiểm chứng sau buổi học.

---

## 1. Sơ đồ quy trình thực tế trên n8n: n8n Workflow Screenshot

Dưới đây là hình ảnh chụp màn hình giao diện cấu trúc quy trình thực tế được thiết lập và kiểm thử thành công trên n8n của chuyên gia:

![Sơ đồ quy trình n8n hoàn chỉnh mẫu](screenshots/smart-ticket-triage-screenshot.jpg)

---

## 2. Sơ đồ luồng xử lý dữ liệu logic: Mermaid Flowchart

Dưới đây là sơ đồ luồng tổng thể từ khâu tiếp nhận dữ liệu, tiền kiểm tra lọc lỗi cục bộ, gọi mô hình trí tuệ nhân tạo (LLM), lọc dữ liệu nhạy cảm, rẽ nhánh điều kiện và kết thúc ở các cổng đầu ra tương ứng:

```mermaid
graph TD
    %% Định nghĩa phong cách thiết kế
    classDef startNode fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef processNode fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1;
    classDef aiNode fill:#EDE7F6,stroke:#4527A0,stroke-width:2px,color:#4A148C;
    classDef conditionNode fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px,color:#E65100;
    classDef errorNode fill:#FFEBEE,stroke:#C62828,stroke-width:2px,color:#B71C1C;
    classDef successNode fill:#F1F8E9,stroke:#558B2F,stroke-width:2px,color:#33691E;

    %% Luồng xử lý chính
    A[Manual / Schedule Trigger] --> B[Read Google Sheets: input]
    B --> C[Filter: Only workflow_status == 'New']
    
    C --> D{"Pre-checking Rules"}:::conditionNode
    
    %% Nhánh tiền kiểm tra lỗi
    D -- "Empty / Empty spaces" --> E[Assign: Missing_Data]:::errorNode
    D -- "Description < 10 chars" --> F[Assign: Format_Error]:::errorNode
    E --> G[Log to execution_log: Fallback]:::processNode
    F --> G
    
    %% Nhánh dữ liệu hợp lệ
    D -- "Valid Description" --> H[LLM Node: Generate JSON]:::aiNode
    H --> I[Code Node: Clean JSON wrapper]:::processNode
    I --> J[Code Node: Mask Sensitive Password PII]:::processNode
    
    J --> K{"Switch Node: Evaluate confidence & requirements"}:::conditionNode
    
    %% Nhánh phân phối của Switch
    K -- "confidence >= 80 AND human_review == false" --> L[Auto Route Branch]:::successNode
    K -- "confidence < 80 OR human_review == true OR category == 'Unknown'" --> M[Human Review Queue Branch]:::conditionNode
    K -- "LLM output invalid category / Parse error" --> N[Fallback Branch]:::errorNode
    
    %% Cổng xử lý đầu ra & Ghi nhật ký
    L --> O[Google Sheets: Append to execution_log Success]:::processNode
    
    M --> P[Google Sheets: Append to review_queue HITL]:::processNode
    P --> Q[Google Sheets: Append to execution_log Pending]:::processNode
    
    N --> R[Google Sheets: Append to execution_log Failed]:::processNode
    
    %% Định dạng phong cách cho các khối
    class A startNode;
    class B,C,G,I,J,O,P,Q,R processNode;
    class H aiNode;
    class D,K conditionNode;
    class E,F,N errorNode;
    class L,M successNode;
```

---

## 2. Đặc tả các cổng rẽ nhánh đầu ra: Branching specifications

Quy trình sử dụng một nút rẽ nhánh điều kiện (<span class="pill-academic">nút rẽ nhánh điều kiện: Switch node</span>) để phân phối dữ liệu dựa trên kết quả đầu ra của mô hình AI:

### A. Nhánh tự động định tuyến (Auto Route Branch)
* **Điều kiện kích hoạt:** 
  $$\text{ai\_confidence} \ge 80 \quad \text{AND} \quad \text{human\_review\_required} == \text{false}$$
* **Hành động hệ thống:** Định tuyến tự động phiếu sự cố đến các hàng chờ chuyên môn tương ứng (Hardware, Software, Network) và gửi thông báo tự động.
* **Mẫu ghi log:** Ghi nhận cột `branch_taken` là `Auto_Route` và trạng thái `final_status` là `Success`.

### B. Nhánh con người duyệt (Human Review Queue Branch)
* **Điều kiện kích hoạt:** 
  $$\text{ai\_confidence} < 80 \quad \text{OR} \quad \text{human\_review\_required} == \text{true} \quad \text{OR} \quad \text{ai\_category} == \text{"Unknown"}$$
* **Hành động hệ thống:** Tạm dừng quy trình tự động, chuyển yêu cầu sự cố sang trang bảng tính duyệt thủ công `review_queue` cho nhân viên kỹ thuật xử lý thủ công.
* **Mẫu ghi log:** Ghi nhận cột `branch_taken` là `Human_Review` và trạng thái `final_status` là `Pending_Human_Review`.

### C. Nhánh xử lý lỗi dự phòng (Fallback Branch)
* **Điều kiện kích hoạt:** Khi xảy ra lỗi phân tích cú pháp JSON ở bước trước, AI trả về kết quả lỗi định dạng, hoặc phân loại nằm ngoài 3 nhóm quy định.
* **Hành động hệ thống:** Báo động lỗi hệ thống, dừng an toàn yêu cầu sự cố và gán nhãn xử lý khẩn cấp.
* **Mẫu ghi log:** Ghi nhận cột `branch_taken` là `Fallback`, lưu mã lỗi tương ứng (ví dụ: `JSON_PARSE_ERROR`) và gán trạng thái `final_status` là `Failed`.
