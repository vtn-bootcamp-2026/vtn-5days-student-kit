---
mo-ta: tai lieu mo ta danh muc case studies va dinh huong lua chon bai toan AI thuc chien
trang-thai: active
phien-ban: v1.3
created-at: 2026-05-17 13:37 +07:00
updated-at: 2026-05-25 18:45 +07:00
---

# Báo cáo Nghiên cứu: Chiến lược Lựa chọn Bài toán AI Thực chiến cho Lực lượng Nòng cốt VTN

**Tuyên bố Khước từ Trách nhiệm (Safety Disclaimer):** Bất kỳ đầu ra nào do AI tạo ra liên quan đến hợp đồng pháp lý, chính sách nhân sự (HR) hoặc cấu hình mạng lõi được đề cập trong báo cáo và khóa học này chỉ dành cho mục đích học tập, thí điểm và mô phỏng. Mọi kết quả do AI sinh ra bắt buộc phải trải qua quá trình xác minh nghiêm ngặt bởi con người (Human-in-the-loop) trước khi đưa ra quyết định hoặc thực thi trong bất kỳ môi trường vận hành thực tế nào của doanh nghiệp.

* Tác nhân AI (AI agents) và quy trình làm việc AI (AI workflows) đang chuyển dịch từ khái niệm lý thuyết sang các công cụ tự động hóa doanh nghiệp thực tiễn với tác động kinh tế khổng lồ.
* Sự thành bại của một chương trình đào tạo AI thực chiến phụ thuộc vào việc lựa chọn đúng bài toán ngay từ Buổi 1, đảm bảo tính khả thi trong phạm vi thời lượng hạn chế.
* Bài toán lý tưởng phải nhỏ gọn, có tính lặp lại cao, sở hữu đầu vào/đầu ra rõ ràng và tuân thủ các nguyên tắc an toàn dữ liệu khắt khe của Khung quản lý rủi ro.
* Nhóm 12 bài toán được đề xuất trong báo cáo này cân bằng giữa vận hành kỹ thuật viễn thông và hỗ trợ quản trị nội bộ, hoàn toàn khả thi để thực hành trên dữ liệu tổng hợp (synthetic data) độc lập với mạng thật.

Trong bối cảnh công nghệ năm 2026, trí tuệ nhân tạo không chỉ dừng lại ở các công cụ trò chuyện đơn lẻ (chatbots) mà đã tiến hóa thành lực lượng lao động AI đa tác nhân (multi-agent AI workforce). Mô hình này sử dụng các tác nhân được điều phối (orchestrator agents) có khả năng truy xuất dữ liệu, suy luận và thực thi nhiệm vụ liền mạch trong các quy trình nghiệp vụ phức tạp từ nhân sự đến chuỗi cung ứng [cite: 1, 2, 3]. Đặc biệt trong lĩnh vực viễn thông, theo phân tích của McKinsey, AI tạo sinh và tự động hóa mạng có khả năng thúc đẩy tỷ suất lợi nhuận (EBITDA) của các nhà mạng tăng thêm 3-4% trong vòng hai năm tới, đồng thời tiết kiệm đến 10% chi phí đầu tư hạ tầng (CAPEX) [cite: 4, 5]. 

Đối với lực lượng nòng cốt tại Viettel Networks (VTN), việc tích hợp AI vào quy trình làm việc đòi hỏi một cách tiếp cận thận trọng, dựa trên tri thức khả thi tối thiểu (Minimum Viable Knowledge - MVK). Báo cáo này cung cấp một khung đánh giá và danh mục 12 bài toán AI thực chiến chuyên sâu, được thiết kế đặc biệt để triển khai xuyên suốt 6 buổi học. Các giải pháp này ưu tiên sử dụng Mô hình ngôn ngữ lớn (Large Language Model - LLM) kết hợp Truy xuất tăng cường (Retrieval-Augmented Generation - RAG) và Tự động hóa bằng AI (AI automation) nhằm giải quyết những nút thắt cục bộ trong cả khối kỹ thuật lẫn khối hỗ trợ. Bằng cách áp dụng các nguyên lý cốt lõi từ Khung Quản lý Rủi ro AI của Viện Tiêu chuẩn và Công nghệ Quốc gia Hoa Kỳ (NIST AI RMF 2024), mọi bài toán đều được thiết kế để đảm bảo tuân thủ tuyệt đối các tiêu chuẩn bảo mật dữ liệu, ngăn ngừa ảo giác (hallucination) và kiểm soát rủi ro hệ thống [cite: 6, 7].

## Phần 1. Tóm tắt điều hành

Sự chuyển dịch của AI đánh dấu một bước ngoặt chiến lược: các tổ chức viễn thông không còn chỉ tìm kiếm một mô hình LLM thông minh, mà họ cần các mạng lưới tác nhân AI (AI agents) có khả năng tự động hóa quy trình nghiệp vụ IT và mạng viễn thông (Artificial Intelligence for IT Operations - AIOps) một cách an toàn [cite: 1, 8]. Việc ứng dụng AIOps có thể giúp giảm thiểu chi phí vận hành, giảm đến 40% Thời gian trung bình để xử lý sự cố (Mean Time to Resolution - MTTR) và tăng mức độ tự động hóa lên 30% [cite: 8, 9]. Do đó, Buổi 1 của khóa học "AI thực chiến cho nhân sự nòng cốt VTN" mang tính chất quyết định, đóng vai trò là la bàn định hướng cho toàn bộ 5 buổi học tiếp theo. 

Việc tập trung vào "chọn đúng bài toán" thay vì "trình diễn công cụ" xuất phát từ nguyên tắc cốt lõi: công cụ AI có thể lỗi thời hoặc thay đổi, nhưng năng lực phân tích quy trình và thiết kế giải pháp an toàn là giá trị vĩnh cửu. Để giải quyết triệt để vấn đề này, báo cáo đề xuất trực tiếp **Danh mục 12 bài toán thực chiến**, chia đều cho khối Kỹ thuật và khối Hỗ trợ doanh nghiệp:
1. Tự động tóm tắt và phân nhóm cụm cảnh báo NOC.
2. Trợ lý tạo bản nháp kịch bản cấu hình thiết bị mạng.
3. Trợ lý RAG tra cứu nhanh cẩm nang xử lý sự cố trạm BTS.
4. Công cụ tự động đối chiếu báo cáo chất lượng mạng.
5. Trợ lý tiền kiểm tra rủi ro cấu hình mạng.
6. Công cụ chuẩn hóa thuật ngữ tài liệu kỹ thuật đa Vendor.
7. Trợ lý ảo giải đáp chính sách nhân sự (HR).
8. Công cụ trích xuất và đối chiếu điều khoản hợp đồng nội bộ.
9. Trợ lý phân tích và viết báo cáo sản lượng tự động.
10. Công cụ tự động phân loại và định tuyến ticket nội bộ.
11. Trợ lý ảo điều phối quy trình Onboarding nhân sự mới.
12. Công cụ phân tích cảm xúc từ khảo sát phản hồi nội bộ.

**Khuyến nghị các bài toán mẫu ưu tiên theo lịch 6 buổi hiện hành:**
Để tối ưu hóa việc truyền đạt, giảng viên nên bám theo chuỗi: Buổi 1 chọn bài toán và phạm vi thí điểm, Buổi 2 thiết kế quy trình làm việc AI với xử lý lỗi và HITL, Buổi 3 thiết kế tác nhân AI có chuẩn đầu ra và tự kiểm, Buổi 4 xây kho tri thức/RAG có trích dẫn nguồn, Buổi 5 tạo công cụ nhỏ chạy local, Buổi 6 kiểm thử tuân thủ và đóng gói triển khai.
*   **Bài toán 10 (Định tuyến Ticket IT):** Bài mẫu chính cho Buổi 2, trực quan hóa quy trình rẽ nhánh, logging và cơ chế con người trong vòng lặp [cite: 12].
*   **Bài toán 8 (Trích xuất Hợp đồng):** Bài mẫu chính cho Buổi 3, phù hợp để luyện thiết kế tác nhân AI, JSON schema, self-check và bộ test cases.
*   **Bài toán 7 (Trợ lý giải đáp chính sách nhân sự):** Bài mẫu chính cho Buổi 4, minh họa sức mạnh của hệ thống RAG doanh nghiệp và quy tắc trích dẫn nguồn [cite: 10].

**Kết luận nền tảng về Dữ liệu và An toàn:**
Việc thiết kế bài toán phải tuân thủ nghiêm ngặt Khung quản lý rủi ro NIST AI RMF, lấy 4 trụ cột Quản trị (Govern), Lập bản đồ (Map), Đo lường (Measure) và Quản lý (Manage) làm kim chỉ nam [cite: 6]. Mọi bài toán trong khóa học **bắt buộc phải sử dụng 100% dữ liệu mô phỏng (synthetic data)** và thiết lập cơ chế "Con người trong vòng lặp" (Human-in-the-loop). Điều này giúp học viên hình thành tư duy "xây được, thử được, kiểm được" mà không xâm phạm cấu trúc dữ liệu thực, từ đó tự tin nhân rộng mô hình an toàn về đơn vị sau khóa học.

```json
{
  "concept": "A matrix plotting the 12 proposed AI use cases based on their feasibility for a 6-session classroom environment versus their expected business value to VTN. This directly visualizes the strategic selection process outlined in Section 4.",
  "reasoning_for_value": "While the text and tables provide detailed scoring, a visual quadrant matrix instantly communicates to instructors and students which use cases represent 'Quick Wins' (high feasibility, high value) versus those that are more complex. This helps steer teams toward successful project selection in Session 1.",
  "title": "Ma trận Lựa chọn Bài toán: Tính khả thi trong Lớp học và Giá trị Kỳ vọng",
  "visual_type": "Scatter Plot / Quadrant Matrix",
  "generation_method": "CODE",
  "justification_of_choice": "A 2D scatter plot configured as a 4-quadrant matrix is the optimal way to compare multiple entities across two distinct scoring dimensions (Feasibility vs. Value). A bar chart would require multiple grouped bars and lose the clear 'Quick Win' visual grouping. A radar chart would be cluttered with 12 entities.",
  "caption": "Phân bổ 12 bài toán đề xuất theo điểm số Khả thi và Giá trị kỳ vọng. Các bài toán nằm ở góc trên bên phải đại diện cho những lựa chọn tối ưu nhất để thực hành xuyên suốt khóa học 6 buổi.",
  "data_specification": {
    "source_snippets_ids": [],
    "data_structure": "A JSON array of objects representing the 12 Use Cases, containing keys: 'id' (1-12), 'name' (Short name of the use case), 'feasibility' (score 1-5), 'value' (score 1-5), and 'group' (Kỹ thuật or Hỗ trợ). Data sourced from the comparative table in Section 4.",
    "mapping": "X-axis = 'feasibility' (Tính khả thi, scale 1-5). Y-axis = 'value' (Giá trị kỳ vọng, scale 1-5). Points are colored by 'group' (e.g., Blue for Kỹ thuật, Orange for Hỗ trợ). The plot area is divided into four quadrants by lines at X=3 and Y=3. Point labels show the 'id'."
  },
  "design_and_interaction": {
    "layout": "A square plot area with X and Y axes ranging from 1 to 5. Clearly labeled quadrants (e.g., Top-Right: 'Ưu tiên Cao / Quick Wins'). A legend indicating the color mapping for technical vs. support groups.",
    "aesthetics": {
      "style": "Professional & Corporate",
      "color_palette": "Background: #FFFFFF. X/Y Axes and Gridlines: #CCCCCC. Kỹ thuật dots: #1A73E8 (Google Blue). Hỗ trợ dots: #FA903E (Tangerine). Text labels: #111111.",
      "additional_details": "Use large, clear dots with the number ID inside or immediately adjacent. Provide a tooltip on hover for full details."
    },
    "interactivity": "Hovering over a data point reveals a tooltip with the full 'name' of the use case, its exact 'feasibility' score, and its 'value' score.",
    "animation": "Static visual with no animation."
  }
}
```

## Phần 2. Nguyên tắc chọn bài toán cho VTN

Để đảm bảo các dự án thực hành không bị "sa lầy" vào các rào cản kỹ thuật phi thực tế, một khung đánh giá đa chiều là công cụ bắt buộc. Khung này giúp giảng viên và học viên VTN sàng lọc, định lượng và quyết định bài toán nào xứng đáng được đầu tư thời gian trong 24 giờ của khóa học, bám sát các nguyên tắc rủi ro của NIST AI RMF [cite: 13].

Dưới đây là 11 tiêu chí đánh giá cốt lõi, được chấm theo thang điểm từ 1 (Rất thấp/Rất kém) đến 5 (Rất cao/Rất xuất sắc).

1. **Mức độ lặp lại của tác vụ:** Tác vụ có thường xuyên xảy ra trong thực tế không? (1 = Hiếm khi, 5 = Diễn ra hàng ngày, hàng giờ). Các tác vụ lặp lại mang lại Tỷ suất hoàn vốn (Return on Investment - ROI) cao nhất khi tự động hóa [cite: 1].
2. **Độ rõ của đầu vào:** Dữ liệu cấp cho AI có cấu trúc hoặc định dạng nhất quán không? (1 = Rất lộn xộn, vô định hình, 5 = Dữ liệu có trường rõ ràng, văn bản chuẩn).
3. **Độ rõ của đầu ra:** Kết quả cần đạt được có thể mô tả bằng một biểu mẫu hoặc danh sách kiểm tra cụ thể không? (1 = Mơ hồ, tùy cảm hứng, 5 = Có mẫu báo cáo hoặc định dạng JSON/bảng biểu cố định).
4. **Khả năng dùng dữ liệu mô phỏng hoặc tổng hợp (synthetic data):** Có thể dễ dàng tạo ra dữ liệu giả giống thật mà không lộ thông tin nhạy cảm của VTN không? (1 = Không thể giả lập, bắt buộc dùng mạng thật, 5 = Dễ dàng tạo hàng trăm mẫu giả lập trong vài phút) [cite: 14].
5. **Mức độ rủi ro (Điểm đảo ngược):** Nếu AI làm sai, hậu quả có nghiêm trọng không? (1 = Hậu quả thảm họa/gây sập mạng, 5 = Sai sót chỉ ở mức nháp, con người duyệt lại sẽ phát hiện ngay).
6. **Khả năng đo hiệu quả:** Có thể chứng minh được số giờ tiết kiệm hoặc tỷ lệ lỗi giảm đi không? (1 = Rất khó đo, 5 = Có thể tính ra ngay số phút/giờ tiết kiệm trên mỗi tác vụ).
7. **Khả năng làm trong lớp:** Mức độ phức tạp kỹ thuật có phù hợp để hoàn thành phiên bản gốc (prototype) trong vài giờ thực hành không? (1 = Cần code phức tạp, 5 = Có thể làm bằng nền tảng no-code/low-code hoặc AI coding tool như n8n, Antigravity, Claude Code, Codex).
8. **Khả năng phát triển xuyên suốt 6 buổi:** Bài toán có thể chia nhỏ thành các chặng (Chọn phạm vi -> Quy trình -> Tác nhân -> Kho tri thức/RAG -> Công cụ nhỏ -> Đóng gói) không? (1 = Quá đơn giản, làm 1 buổi là xong, 5 = Đủ độ sâu để đắp thêm tính năng qua từng buổi).
9. **Khả năng mở rộng sau khóa:** Sau khi thí điểm thành công, đơn vị có thể nhân rộng để xử lý hàng ngàn yêu cầu không? (1 = Chỉ dùng được cho 1 người, 5 = Áp dụng toàn công ty).
10. **Mức độ cần con người trong vòng lặp (Human-in-the-loop - HITL):** Bài toán có điểm dừng để con người kiểm duyệt trước khi hành động không? (1 = Tự động hoàn toàn đầy rủi ro, 5 = Thiết kế sẵn bước xác nhận phê duyệt bởi chuyên viên) [cite: 15, 16].
11. **Mức độ phù hợp với kiến trúc RAG/AI workflow:** Bài toán có cần truy xuất tài liệu nội bộ và chạy qua nhiều bước xử lý không? (1 = Chỉ cần hỏi ChatGPT là ra, 5 = Bắt buộc phải có kho tri thức riêng và công cụ luồng).

Khung tiêu chí này đóng vai trò như một bộ lọc an toàn, ngăn chặn việc lựa chọn các bài toán quá tham vọng hoặc vi phạm nguyên tắc bảo mật. Bằng cách cộng điểm, giảng viên có thể nhanh chóng hướng dẫn học viên điều chỉnh phạm vi (scope) của bài toán về mức "vừa sức" cho khóa học 6 buổi.

## Phần 3. Danh mục 12 bài toán đề xuất

Sau quá trình rà soát các xu hướng ứng dụng AI trong quản trị vận hành viễn thông (AIOps) và tự động hóa doanh nghiệp đa tác nhân (multi-agent workflows) [cite: 3, 17], danh sách 12 bài toán sau đây được tuyển chọn. Danh sách được chia đều: 6 bài toán cho nhóm kỹ thuật (đặc thù mạng viễn thông) và 6 bài toán cho nhóm hỗ trợ doanh nghiệp. Tất cả đều tuân thủ nghiêm ngặt nguyên tắc chỉ dùng dữ liệu mô phỏng.

### 3.1. Phân tích và Tóm tắt Cảnh báo NOC (Nhóm Kỹ thuật)

Trong trung tâm điều hành mạng (NOC), các kỹ sư thường xuyên bị "ngập" trong hàng ngàn cảnh báo hệ thống, dẫn đến hiện tượng mệt mỏi vì cảnh báo (alert fatigue) [cite: 11, 18]. Việc tích hợp AIOps vào khâu này là xu hướng tất yếu của các nhà mạng viễn thông toàn cầu để giảm thiểu sức lao động thủ công [cite: 19, 20].

- **1. Tên bài toán:** Tự động tóm tắt và phân nhóm cụm cảnh báo NOC (NOC Alert Summarization).
- **2. Nhóm lĩnh vực phù hợp:** Vận hành mạng, NOC, xử lý sự cố.
- **3. Vai trò học viên phù hợp:** Kỹ sư NOC, chuyên viên giám sát cấp 1 (Tier 1).
- **4. Vấn đề công việc cần giải quyết:** Hàng loạt cảnh báo rác và cảnh báo trùng lặp từ nhiều hệ thống đổ về khiến kỹ sư mất nhiều thời gian đọc hiểu và tìm ra nguyên nhân gốc.
- **5. Vì sao bài toán này phù hợp với VTN:** Giảm Thời gian trung bình để xử lý sự cố (MTTR) là ưu tiên hàng đầu của bất kỳ nhà mạng nào. Việc tóm tắt cảnh báo bằng AI giúp kỹ sư nắm bắt bức tranh toàn cảnh nhanh chóng [cite: 8, 16].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Phân tích một tệp tin chứa 50-100 dòng log/cảnh báo thô, nhóm chúng lại theo mức độ nghiêm trọng và xuất ra 1 đoạn tóm tắt 3 ý chính.
- **7. Đầu vào mô phỏng cần chuẩn bị:** File CSV/Excel chứa các dòng log giả lập có cấu trúc trường: Thời gian, Thiết bị, Mức độ, Mã lỗi.
- **8. Đầu ra kỳ vọng:** Một phiếu tóm tắt sự cố (Incident Briefing) ghi rõ: Vấn đề chính là gì, Ảnh hưởng đến dịch vụ nào, Khuyến nghị hành động tiếp theo.
- **9. Dạng giải pháp phù hợp:** Tác nhân AI kết hợp Quy trình làm việc AI.
- **10. Phần có thể làm trong Buổi 1:** Xác định định dạng log đầu vào, thiết kế mẫu Phiếu tóm tắt đầu ra và định hình luồng xử lý.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế quy trình xử lý log có logging, nhánh lỗi và HITL. Buổi 3: Xây tác nhân AI đọc log, xuất JSON và tự kiểm. Buổi 4: Bổ sung kho tri thức mã lỗi giả lập/RAG có trích dẫn nguồn. Buổi 5: Tạo công cụ nhỏ chạy local để nạp file và sinh phiếu tóm tắt. Buổi 6: Kiểm thử tuân thủ và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI nhóm đúng các lỗi thuộc về cùng một thiết bị mô phỏng và không sinh ra thông tin ảo.
- **13. Rủi ro chính và cách kiểm soát:** Rủi ro bỏ sót cảnh báo chí mạng (False negative). Kiểm soát: Cấu hình bộ quy tắc luật cứng (hard-rule) chạy song song với AI.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Thời gian trung bình để lập phiếu sự cố (Ticket creation time) giảm từ 15 phút xuống 3 phút.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 5
- **18. Điểm rủi ro:** 4 (Chỉ đưa ra gợi ý, con người vẫn quyết định cuối cùng).

### 3.2. Trợ lý Sinh Kịch bản Cấu hình Thiết bị (Nhóm Kỹ thuật)

Cấu hình thiết bị định tuyến hoặc chuyển mạch là thao tác lặp lại nhưng yêu cầu độ chính xác cao. Trợ lý AI có thể đóng vai trò như một chuyên gia biên soạn nháp kịch bản [cite: 21].

- **1. Tên bài toán:** Trợ lý tạo bản nháp kịch bản cấu hình thiết bị mạng (Config Script Drafter).
- **2. Nhóm lĩnh vực phù hợp:** Cấu hình mạng, thay đổi kỹ thuật, kỹ sư triển khai.
- **3. Vai trò học viên phù hợp:** Kỹ sư cấu hình, nhân viên triển khai hiện trường.
- **4. Vấn đề công việc cần giải quyết:** Tốn thời gian viết lại các kịch bản cấu hình cơ bản cho nhiều thiết bị khác nhau, dễ sai sót cú pháp.
- **5. Vì sao bài toán này phù hợp với VTN:** Viễn thông vận hành khối lượng thiết bị đa dạng. Tự động sinh mã cấu hình giảm thiểu lỗi do thao tác thủ công.
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Nhập một yêu cầu bằng ngôn ngữ tự nhiên, AI trả về đoạn mã lệnh Command Line Interface (CLI) tương ứng.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Danh sách các lệnh mẫu (Command Reference) của một hãng thiết bị mạng giả định.
- **8. Đầu ra kỳ vọng:** File văn bản chứa đoạn mã lệnh CLI sạch, kèm theo một dòng giải thích logic.
- **9. Dạng giải pháp phù hợp:** Tác nhân AI dựa trên Kho tri thức (RAG).
- **10. Phần có thể làm trong Buổi 1:** Xác định giới hạn lệnh hỗ trợ, chuẩn hóa yêu cầu đầu vào.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng tiếp nhận yêu cầu, kiểm lỗi và điểm duyệt kỹ sư. Buổi 3: Dạy tác nhân AI trích xuất cú pháp theo JSON schema và self-check. Buổi 4: Bổ sung kho tri thức chứa file lệnh mẫu/RAG có trích dẫn. Buổi 5: Xây công cụ nhỏ dạng form nhập liệu. Buổi 6: Kiểm thử nguy cơ tấn công lời nhắc (prompt injection) và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI không bao giờ bịa ra một cú pháp lệnh không có trong Kho tri thức.
- **13. Rủi ro chính và cách kiểm soát:** Mã lệnh sai có thể làm sập thiết bị. Kiểm soát: Đóng gói chặt bằng lời nhắc hệ thống (system prompt), bắt buộc kỹ sư phải xem và thao tác dán (copy-paste) thủ công.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Thời gian tạo một kịch bản Yêu cầu thay đổi (Change Request - CR) chuẩn giảm từ 15 phút xuống 2 phút.
- **15. Điểm khả thi:** 4
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 4
- **18. Điểm rủi ro:** 3 (Bắt buộc phải áp dụng Human-in-the-loop).

### 3.3. Tra cứu Quy trình Vận hành Chuẩn Hiện trường (Nhóm Kỹ thuật)

Kỹ sư hiện trường thường gặp khó khăn khi phải tra cứu Quy trình Vận hành Chuẩn (Standard Operating Procedure - SOP) dày hàng trăm trang giữa lúc đang xử lý sự cố tại trạm BTS [cite: 22].

- **1. Tên bài toán:** Trợ lý RAG tra cứu nhanh cẩm nang xử lý sự cố trạm BTS (Field Ops RAG Assistant).
- **2. Nhóm lĩnh vực phù hợp:** Vận hành hiện trường, bảo trì, quản lý tài sản.
- **3. Vai trò học viên phù hợp:** Kỹ sư hiện trường, chuyên viên hỗ trợ tuyến đầu.
- **4. Vấn đề công việc cần giải quyết:** Tốc độ tìm kiếm tài liệu SOP trên thiết bị di động chậm, khó tra cứu đúng lỗi phần cứng.
- **5. Vì sao bài toán này phù hợp với VTN:** Số hóa năng lực và tài liệu lưu trữ, tăng cường độ chính xác khi thay thế thiết bị trên quy mô lớn.
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Đưa 3 tài liệu PDF hướng dẫn xử lý lỗi phần cứng (mô phỏng) vào cơ sở dữ liệu véc-tơ. Đặt câu hỏi và AI trích xuất đúng quy trình 3 bước kèm số trang tài liệu.
- **7. Đầu vào mô phỏng cần chuẩn bị:** 3-5 file PDF mô tả cách khắc phục sự cố nguồn điện, module quang ảo.
- **8. Đầu ra kỳ vọng:** Câu trả lời ngắn gọn, trích dẫn chính xác nguồn tài liệu nào, trang bao nhiêu.
- **9. Dạng giải pháp phù hợp:** Kho tri thức (Knowledge Base) và Trợ lý AI cá nhân.
- **10. Phần có thể làm trong Buổi 1:** Phân loại tài liệu hiện trường và đặt kỳ vọng về hành vi từ chối trả lời nếu thiếu thông tin.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng hỏi-đáp có xử lý câu hỏi ngoài phạm vi và HITL. Buổi 3: Dựng tác nhân AI với chuẩn đầu ra, self-check và refusal rule. Buổi 4: Phân mảnh tài liệu (chunking), dựng RAG và trích dẫn nguồn. Buổi 5: Tạo công cụ nhỏ để tra cứu local. Buổi 6: Kiểm thử bằng các câu hỏi "bẫy" và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** Độ chính xác 100% trong việc trích dẫn nguồn. Tỷ lệ tự suy diễn là 0%.
- **13. Rủi ro chính và cách kiểm soát:** AI suy diễn sai thông số dòng điện gây nguy hiểm. Kiểm soát: Yêu cầu mọi tham số phần cứng phải được bôi đậm và đối chiếu nguồn.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Tỷ lệ giải quyết sự cố ngay lần đầu (First Time Fix Rate) tăng từ 60% lên 85%.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 5
- **18. Điểm rủi ro:** 4.

### 3.4. Đối chiếu Báo cáo Chất lượng Mạng (Nhóm Kỹ thuật)

Đánh giá Chất lượng Dịch vụ (Quality of Service - QoS) cần đối chiếu nhiều file báo cáo định kỳ.

- **1. Tên bài toán:** Công cụ tự động đối chiếu và cảnh báo độ lệch chuẩn QoS (QoS Report Validator).
- **2. Nhóm lĩnh vực phù hợp:** Chất lượng dịch vụ, tối ưu mạng.
- **3. Vai trò học viên phù hợp:** Kỹ sư tối ưu, chuyên gia đánh giá chất lượng.
- **4. Vấn đề công việc cần giải quyết:** Mất hàng giờ để so sánh báo cáo Chỉ số đo lường hiệu quả công việc (Key Performance Indicators - KPIs) của tuần này với tuần trước.
- **5. Vì sao bài toán này phù hợp với VTN:** Quản lý chất lượng mạng ở quy mô lớn yêu cầu giám sát tự động hóa [cite: 23].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Đọc 2 file báo cáo giả lập, so sánh các chỉ số (Tốc độ tải, Tỷ lệ rớt cuộc gọi), sinh ra báo cáo chỉ ra các trạm bị suy giảm.
- **7. Đầu vào mô phỏng cần chuẩn bị:** 2 bảng dữ liệu CSV với các cột: Tên Trạm (giả), KPI_1, KPI_2.
- **8. Đầu ra kỳ vọng:** File cảnh báo: "Danh sách 3 trạm suy giảm mạnh nhất", giải thích ngắn gọn bằng lời văn.
- **9. Dạng giải pháp phù hợp:** Luồng tự động hóa (Workflow) + Công cụ nhỏ.
- **10. Phần có thể làm trong Buổi 1:** Khảo sát định dạng file báo cáo và xác định công thức logic.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế workflow đọc file, xử lý lỗi định dạng và logging. Buổi 3: Xây Agent đọc số liệu, xuất JSON/bảng và tự kiểm. Buổi 4: Bổ sung tài liệu quy tắc KPI/RAG nếu cần trích dẫn công thức. Buổi 5: Tạo công cụ nhỏ chạy local để sinh báo cáo. Buổi 6: Rà soát lỗi đọc số và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI lấy đúng số liệu toán học từ 2 bảng, không làm tròn sai.
- **13. Rủi ro chính và cách kiểm soát:** LLM thường yếu về toán học. Kiểm soát: Dùng AI để viết mã Python (Vibe coding) thực hiện phép tính [cite: 24].
- **14. Chỉ số đo hiệu quả sau thí điểm:** Thời gian hoàn thành báo cáo đối chiếu hàng tuần giảm từ 4 giờ xuống 30 phút.
- **15. Điểm khả thi:** 4
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 3
- **18. Điểm rủi ro:** 5.

### 3.5. Nhận diện Rủi ro Thay đổi Cấu hình (Nhóm Kỹ thuật)

Trước khi thực hiện một Yêu cầu thay đổi (Change Request - CR), chuyên gia phải rà soát lịch sử xem thay đổi tương tự từng gây lỗi chưa.

- **1. Tên bài toán:** Trợ lý tiền kiểm tra rủi ro cấu hình mạng (CR Risk Predictor).
- **2. Nhóm lĩnh vực phù hợp:** Quản lý thay đổi, An toàn thông tin.
- **3. Vai trò học viên phù hợp:** Người phê duyệt CR, quản trị viên hệ thống.
- **4. Vấn đề công việc cần giải quyết:** Việc thiếu đánh giá rủi ro xuyên suốt các silo thông tin dễ dẫn đến lỗi cấu hình dây chuyền.
- **5. Vì sao bài toán này phù hợp với VTN:** Đảm bảo độ ổn định của mạng viễn thông bằng cách gợi nhớ "ký ức tổ chức" từ các kho log sự cố cũ.
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Nhập một mô tả thay đổi. AI tìm trong kho dữ liệu sự cố quá khứ xem có sự cố nào liên quan không và cảnh báo.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Dữ liệu mô phỏng về 20-30 sự cố cũ, trong đó có gài 1-2 sự cố do nâng cấp cấu hình.
- **8. Đầu ra kỳ vọng:** Thẻ đánh giá rủi ro (Risk Scorecard): Xanh/Vàng/Đỏ kèm lý do.
- **9. Dạng giải pháp phù hợp:** Tác nhân AI truy xuất kho tri thức (RAG).
- **10. Phần có thể làm trong Buổi 1:** Phân loại cấu trúc một phiếu CR và định nghĩa rủi ro.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng đọc phiếu CR/ticket, nhánh rủi ro và HITL. Buổi 3: Xây tác nhân đánh giá rủi ro với JSON schema và self-check. Buổi 4: Cấu trúc hóa kho lịch sử/RAG có căn cứ nguồn. Buổi 5: Tạo công cụ nhỏ hỗ trợ phê duyệt. Buổi 6: Đánh giá độ hội tụ và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI phát hiện chính xác 80% trường hợp CR có từ khóa rủi ro tương đồng.
- **13. Rủi ro chính và cách kiểm soát:** Cảnh báo giả (False positive) khiến mọi thay đổi đều bị chặn. Kiểm soát: Cảnh báo chỉ mang tính tham khảo.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Tỷ lệ thay đổi gây sự cố (Change Failure Rate) giảm 25% [cite: 25].
- **15. Điểm khả thi:** 4
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 4
- **18. Điểm rủi ro:** 4.

### 3.6. Chuẩn hóa Tài liệu Kỹ thuật Đa Vendor (Nhóm Kỹ thuật)

Mỗi nhà cung cấp hạ tầng viễn thông sử dụng một bộ thuật ngữ tài liệu khác nhau.

- **1. Tên bài toán:** Công cụ chuẩn hóa thuật ngữ tài liệu kỹ thuật (Multi-vendor Doc Normalizer).
- **2. Nhóm lĩnh vực phù hợp:** Quản lý tri thức, tích hợp hệ thống.
- **3. Vai trò học viên phù hợp:** Kỹ sư thiết kế, quản lý hợp đồng vendor.
- **4. Vấn đề công việc cần giải quyết:** Tốn thời gian đào tạo nhân viên hiểu các định dạng thuật ngữ khác nhau.
- **5. Vì sao bài toán này phù hợp với VTN:** Viettel sở hữu mạng lưới đa vendor rất lớn. LLM xuất sắc trong dịch thuật chuyên ngành [cite: 23, 26].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Nhập tài liệu mô phỏng của Vendor A, AI trích xuất các thông số và gán vào một Template chuẩn của VTN.
- **7. Đầu vào mô phỏng cần chuẩn bị:** 5 file tài liệu hướng dẫn cấu hình (mô phỏng) của 2 vendor khác nhau dùng thuật ngữ khác nhau.
- **8. Đầu ra kỳ vọng:** File JSON hoặc Word theo cấu trúc chuẩn.
- **9. Dạng giải pháp phù hợp:** Công cụ nhỏ (Mini tool).
- **10. Phần có thể làm trong Buổi 1:** Liệt kê các thuật ngữ tương đương.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng tải file, kiểm lỗi định dạng và logging. Buổi 3: Xây Agent "Biên dịch" với output schema và self-check. Buổi 4: Nạp từ điển thuật ngữ vào KB/RAG để trích dẫn. Buổi 5: Tích hợp công cụ kiểm lỗi local. Buổi 6: Nghiệm thu khả năng ánh xạ và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** Chuyển đổi chính xác 100% thuật ngữ đã có trong từ điển gốc.
- **13. Rủi ro chính và cách kiểm soát:** Dịch sai thuật ngữ kỹ thuật. Kiểm soát: Chuyên gia con người bắt buộc rà soát bản dịch.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Số giờ tiết kiệm được khi chuẩn hóa tài liệu mới đạt mức 12 giờ cho mỗi bộ tài liệu 100 trang.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 3
- **18. Điểm rủi ro:** 5.

### 3.7. Trợ lý Trả lời Chính sách Nhân sự (Nhóm Hỗ trợ)

Nhân viên liên tục hỏi Phòng Nhân sự (HR) về ngày phép, chế độ phụ cấp ca kíp. Việc ứng dụng RAG vào quản trị tri thức nhân sự là một "Quick Win" điển hình [cite: 27, 28].

- **1. Tên bài toán:** Trợ lý ảo giải đáp chính sách nhân sự (HR Policy Q&A Agent).
- **2. Nhóm lĩnh vực phù hợp:** Nhân sự, Hành chính.
- **3. Vai trò học viên phù hợp:** Chuyên viên nhân sự, truyền thông nội bộ.
- **4. Vấn đề công việc cần giải quyết:** HR quá tải vì phải trả lời lặp đi lặp lại những câu hỏi đã có sẵn trong quy chế [cite: 29, 30].
- **5. Vì sao bài toán này phù hợp với VTN:** Doanh nghiệp quy mô lớn có tài liệu quy chế phức tạp. AI hỗ trợ tìm kiếm ngữ nghĩa cực kỳ hiệu quả [cite: 31].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Đưa 1 file PDF "Sổ tay nhân sự mô phỏng" vào hệ thống. Trợ lý trả lời đúng quy định số ngày phép, cách tính lương làm thêm.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Sổ tay nhân viên mô phỏng.
- **8. Đầu ra kỳ vọng:** Phản hồi chat, kèm link trích dẫn đến đúng trang tài liệu.
- **9. Dạng giải pháp phù hợp:** Kho tri thức + Tác nhân AI.
- **10. Phần có thể làm trong Buổi 1:** Viết danh sách 20 câu hỏi thường gặp nhất (FAQ).
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng tiếp nhận câu hỏi, logging và chuyển chuyên viên thật khi thiếu căn cứ. Buổi 3: Lập chỉ dẫn giọng điệu, chuẩn đầu ra và rule tự kiểm. Buổi 4: Xây kho tri thức RAG có trích dẫn nguồn. Buổi 5: Tạo công cụ nhỏ để hỏi đáp và theo dõi lịch sử. Buổi 6: Kiểm tra bảo mật thông tin và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI biết từ chối trả lời nếu câu hỏi vượt quá quy chế đã nạp.
- **13. Rủi ro chính và cách kiểm soát:** AI hướng dẫn sai luật lao động. Kiểm soát: Cảnh báo tĩnh "Đây là tư vấn tự động tham khảo".
- **14. Chỉ số đo hiệu quả sau thí điểm:** Lượng ticket/email hỏi HR về thủ tục hành chính lặp lại giảm 60%.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 5
- **18. Điểm rủi ro:** 4.

### 3.8. Rà soát Dữ liệu Hợp đồng Pháp lý (Nhóm Hỗ trợ)

Ban Pháp chế/Mua sắm thường phải đọc các hợp đồng dài hàng chục trang để tìm kiếm các điều khoản phạt.

- **1. Tên bài toán:** Công cụ trích xuất và đối chiếu điều khoản hợp đồng nội bộ (Contract Term Extractor).
- **2. Nhóm lĩnh vực phù hợp:** Pháp lý, Mua sắm, Kế toán.
- **3. Vai trò học viên phù hợp:** Chuyên viên pháp lý, cán bộ phòng mua sắm.
- **4. Vấn đề công việc cần giải quyết:** Tốn nhiều công sức để rà soát thủ công nhằm đảm bảo hợp đồng đối tác không lệch chuẩn [cite: 28, 32].
- **5. Vì sao bài toán này phù hợp với VTN:** Giảm thiểu rủi ro pháp lý và thời gian trình ký trong chuỗi cung ứng khổng lồ [cite: 3].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Nạp 2 file hợp đồng mẫu. AI tự động trích xuất: Ngày hết hạn, Giá trị hợp đồng, Mức phạt vi phạm (%).
- **7. Đầu vào mô phỏng cần chuẩn bị:** Hợp đồng giả định có gài sẵn một số điều khoản rủi ro.
- **8. Đầu ra kỳ vọng:** Bảng tính (Excel/CSV) liệt kê các trường thông tin quan trọng.
- **9. Dạng giải pháp phù hợp:** Quy trình làm việc AI + Tác nhân trích xuất.
- **10. Phần có thể làm trong Buổi 1:** Xác định đúng 5-7 trường dữ liệu bắt buộc.
- **11. Cách phát triển trong Buổi 3 khi dùng làm bài mẫu:** Trong cùng 1 session 4 giờ, gom đủ các phần: thiết kế workflow nạp hợp đồng, logging, nhánh lỗi định dạng và HITL; dạy Agent dùng output JSON, self-check và test cases; bổ sung kho điều khoản mẫu/RAG mini có trích dẫn nguồn; tạo logic rẽ nhánh cảnh báo cờ đỏ; rà soát lỗi đọc sót (False Negative) và đóng gói artifact.
- **12. Tiêu chí nghiệm thu tối thiểu:** Xuất ra đúng định dạng JSON/Bảng mà không chèn thêm ký tự văn tự do.
- **13. Rủi ro chính và cách kiểm soát:** Rò rỉ thông tin nhạy cảm. Kiểm soát: Thực hành hoàn toàn trên hợp đồng mẫu (Template) tải từ Internet đã được tùy biến [cite: 33].
- **14. Chỉ số đo hiệu quả sau thí điểm:** Thời gian rà soát ban đầu của một hợp đồng chuẩn giảm từ 45 phút xuống còn 5 phút.
- **15. Điểm khả thi:** 4
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 4
- **18. Điểm rủi ro:** 3 (Bảo mật dữ liệu là rủi ro cao nhất).

### 3.9. Báo cáo Doanh thu/Sản lượng (Nhóm Hỗ trợ)

Cán bộ báo cáo phải tổng hợp số liệu kinh doanh hàng ngày để viết email gửi lãnh đạo.

- **1. Tên bài toán:** Trợ lý phân tích và viết báo cáo sản lượng tự động (Automated Daily Reporting).
- **2. Nhóm lĩnh vực phù hợp:** Báo cáo quản trị, Kế toán, Bán hàng.
- **3. Vai trò học viên phù hợp:** Chuyên viên phân tích dữ liệu, cán bộ tổng hợp.
- **4. Vấn đề công việc cần giải quyết:** Mất thời gian "nhào nặn" số liệu lặp đi lặp lại.
- **5. Vì sao bài toán này phù hợp với VTN:** Quản lý bằng số liệu là văn hóa Viettel. LLM sinh bình luận giúp báo cáo nhanh và sắc bén hơn [cite: 28, 34].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Luồng tự động đọc CSV số liệu, tính toán tăng/giảm và sinh ra email tóm tắt nguyên nhân biến động.
- **7. Đầu vào mô phỏng cần chuẩn bị:** 1 file CSV giả lập số liệu kinh doanh.
- **8. Đầu ra kỳ vọng:** Một đoạn văn bản báo cáo tóm tắt rõ ràng.
- **9. Dạng giải pháp phù hợp:** Luồng tự động hóa bằng AI (AI Workflow).
- **10. Phần có thể làm trong Buổi 1:** Thiết kế cấu trúc (Template) của báo cáo mục tiêu.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế workflow đọc CSV, kiểm lỗi số liệu và logging. Buổi 3: Dạy Agent nhận xét số liệu theo schema và self-check. Buổi 4: Bổ sung tài liệu quy tắc tính toán/RAG nếu cần căn cứ. Buổi 5: Tạo công cụ truy vấn (Chat với CSV) chạy local. Buổi 6: Kiểm soát ảo giác toán học và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** AI chép chính xác số từ CSV vào báo cáo, không bịa ra số liệu không tồn tại.
- **13. Rủi ro chính và cách kiểm soát:** LLM tính toán sai tỷ lệ phần trăm. Kiểm soát: Hệ thống truyền lệnh tính toán bằng Code thay vì LLM nội suy.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Tiết kiệm 45 phút khởi tạo báo cáo định kỳ mỗi buổi sáng.
- **15. Điểm khả thi:** 4
- **16. Điểm giá trị kỳ vọng:** 5
- **17. Điểm phù hợp để làm bài mẫu:** 4
- **18. Điểm rủi ro:** 5.

### 3.10. Định tuyến Ticket Nội bộ (Nhóm Hỗ trợ)

Ticket báo lỗi nội bộ thường bị dồn ứ ở khâu phân loại thủ công [cite: 35, 36]. Hệ thống đa tác nhân (multi-agent) cực kỳ phù hợp để thay thế khâu "gác cổng" này [cite: 12].

- **1. Tên bài toán:** Công cụ tự động phân loại và định tuyến ticket nội bộ (Smart Ticket Triage).
- **2. Nhóm lĩnh vực phù hợp:** Hỗ trợ CNTT nội bộ, Tổng hợp.
- **3. Vai trò học viên phù hợp:** Quản trị viên hệ thống, nhân viên hỗ trợ CNTT.
- **4. Vấn đề công việc cần giải quyết:** Trễ hạn Cam kết Chất lượng Dịch vụ (Service Level Agreement - SLA) xử lý vì ticket nằm chờ phân loại.
- **5. Vì sao bài toán này phù hợp với VTN:** Quy mô nhân sự lớn dẫn đến lượng ticket khổng lồ. Việc gán nhãn tự động tăng tốc luồng xử lý.
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Đọc nội dung phàn nàn tự do, AI tự động gán nhãn: Nhóm lỗi, Mức ưu tiên, Gán cho đội nào.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Danh sách 50 ticket mô phỏng.
- **8. Đầu ra kỳ vọng:** Bảng tính đã được thêm các cột Nhãn (Tags) chính xác.
- **9. Dạng giải pháp phù hợp:** Luồng làm việc AI tích hợp phân tích ngữ nghĩa.
- **10. Phần có thể làm trong Buổi 1:** Lập danh mục (Taxonomy) các loại lỗi.
- **11. Cách phát triển tiếp:** Buổi 2: Dựng workflow Smart Ticket Triage định tuyến theo điểm tin cậy (confidence score), có logging, nhánh Unknown và HITL. Buổi 3: Xây Agent "Người gác cổng" với output JSON và self-check. Buổi 4: Bổ sung KB/RAG cho chính sách phân loại nếu cần trích dẫn. Buổi 5: Tạo công cụ nhỏ tự sinh phản hồi ban đầu. Buổi 6: Đóng gói và nghiệm thu.
- **12. Tiêu chí nghiệm thu tối thiểu:** Độ chính xác phân loại tự động đạt trên 85% trên tập dữ liệu thử nghiệm.
- **13. Rủi ro chính và cách kiểm soát:** Phân loại nhầm khiến ticket bị trôi. Kiểm soát: Bắt buộc duy trì luồng "Chưa rõ" (Unknown) cho con người xử lý.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Thời gian ticket chờ phân loại giảm từ 2 giờ xuống 30 giây.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 5
- **18. Điểm rủi ro:** 5.

### 3.11. Sinh Tự động Lịch trình Onboarding (Nhóm Hỗ trợ)

Quá trình tiếp nhận nhân sự mới đòi hỏi phối hợp với IT, Hành chính và Quản lý. Sự phối hợp đa nền tảng này cần các tác nhân điều phối (orchestrator agent) để đảm bảo đồng bộ [cite: 3].

- **1. Tên bài toán:** Trợ lý ảo điều phối quy trình Onboarding nhân sự mới (Onboarding Automation Workflow).
- **2. Nhóm lĩnh vực phù hợp:** Nhân sự, Đào tạo nội bộ.
- **3. Vai trò học viên phù hợp:** Chuyên viên nhân sự.
- **4. Vấn đề công việc cần giải quyết:** Trải nghiệm nhân viên mới bị ảnh hưởng do quá trình cấp email, xếp chỗ chậm trễ [cite: 29].
- **5. Vì sao bài toán này phù hợp với VTN:** Chuẩn hóa quy trình tạo ra hình ảnh doanh nghiệp chuyên nghiệp [cite: 24].
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Nhập thông tin nhân sự. AI tự động sinh ra: Email chào mừng, Danh sách kiểm tra công việc cho IT, Kịch bản giới thiệu.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Dữ liệu mô phỏng của 3 nhân viên mới trúng tuyển.
- **8. Đầu ra kỳ vọng:** Tập tin văn bản/email được cá nhân hóa cho từng phòng ban.
- **9. Dạng giải pháp phù hợp:** Luồng tự động hóa + Tác nhân AI.
- **10. Phần có thể làm trong Buổi 1:** Vẽ lại quy trình Onboarding và đánh dấu nút thắt.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng tích hợp Form, logging và điểm duyệt HR. Buổi 3: Dạy Agent viết email theo schema và self-check. Buổi 4: Tạo kho tri thức "Khung năng lực"/RAG có trích dẫn. Buổi 5: Xây công cụ nhắc nhở chạy local. Buổi 6: End-to-end testing và đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** Nội dung email sinh ra không sáo rỗng, đúng định dạng và đề xuất tài liệu chuẩn.
- **13. Rủi ro chính và cách kiểm soát:** Nhầm lẫn thông tin cá nhân. Kiểm soát: Cơ chế gắn thẻ (tags mapping) chặt chẽ trong luồng tự động hóa.
- **14. Chỉ số đo hiệu quả sau thí điểm:** Tốc độ hoàn thiện hồ sơ và thủ tục hành chính cho nhân viên mới giảm từ 3 ngày xuống 4 giờ.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 4
- **18. Điểm rủi ro:** 5.

### 3.12. Phân tích Cảm xúc Khảo sát Nội bộ (Nhóm Hỗ trợ)

Phần câu hỏi mở (Open-ended questions) trong khảo sát chứa nhiều giá trị nhưng tốn quá nhiều thời gian đọc thủ công.

- **1. Tên bài toán:** Công cụ phân tích cảm xúc và tổng hợp từ khóa khảo sát (Feedback Sentiment Analyzer).
- **2. Nhóm lĩnh vực phù hợp:** Đào tạo nội bộ, Quản lý chất lượng.
- **3. Vai trò học viên phù hợp:** Chuyên viên đào tạo, truyền thông nội bộ.
- **4. Vấn đề công việc cần giải quyết:** Bỏ qua hàng ngàn dòng phản hồi text vì không có công cụ phân tích tự động [cite: 37].
- **5. Vì sao bài toán này phù hợp với VTN:** Lắng nghe tiếng nói nội bộ là nền tảng của Kaizen. LLM thấu hiểu ngữ cảnh xuất sắc.
- **6. Phạm vi tối thiểu có thể làm trong khóa:** Đọc 100 câu nhận xét. AI gán nhãn Tích cực/Tiêu cực/Trung tính và tổng hợp ý chính.
- **7. Đầu vào mô phỏng cần chuẩn bị:** Bảng CSV chứa 100 phản hồi giả định.
- **8. Đầu ra kỳ vọng:** Báo cáo text chỉ ra tỷ lệ cảm xúc, xu hướng chính.
- **9. Dạng giải pháp phù hợp:** Quy trình làm việc AI (xử lý hàng loạt).
- **10. Phần có thể làm trong Buổi 1:** Định nghĩa thang đo cảm xúc nội bộ.
- **11. Cách phát triển tiếp:** Buổi 2: Thiết kế luồng quét CSV, logging và nhánh duyệt phản hồi nhạy cảm. Buổi 3: Dạy Agent trích xuất (Extraction) theo schema và self-check. Buổi 4: Bổ sung từ điển từ lóng/KB để giải thích căn cứ phân loại. Buổi 5: Tạo công cụ nhỏ tự động phân loại luồng cảnh báo. Buổi 6: Đóng gói.
- **12. Tiêu chí nghiệm thu tối thiểu:** Nhận diện đúng mỉa mai (Sarcasm) trong văn cảnh cơ bản, tổng hợp đúng 3 ý chính.
- **13. Rủi ro chính và cách kiểm soát:** Phân tích sai cảm xúc dẫn đến bỏ lọt khủng hoảng nội bộ. Kiểm soát: Cảnh báo tự tin (Confidence score) [cite: 36, 38].
- **14. Chỉ số đo hiệu quả sau thí điểm:** Số giờ tiết kiệm được khi làm báo cáo hậu kiểm (Post-mortem report) giảm từ 8 giờ xuống 1 giờ.
- **15. Điểm khả thi:** 5
- **16. Điểm giá trị kỳ vọng:** 4
- **17. Điểm phù hợp để làm bài mẫu:** 3
- **18. Điểm rủi ro:** 5.

## Phần 4. So sánh và Xếp hạng 12 Bài toán

Nhằm giúp Ban tổ chức và giảng viên có cái nhìn toàn cảnh, bảng phân tích ma trận sau đây đối chiếu 12 bài toán qua lăng kính của tính thực chiến.

| Tên Bài toán | Khả thi trong lớp | Dễ tạo dữ liệu ảo | Phát triển xuyên 6 buổi | Giá trị với VTN | Hợp Nhóm Kỹ thuật | Hợp Nhóm Hỗ trợ | Rủi ro (1-5, 5 là an toàn) | Khả năng làm Bài mẫu | Khả năng nhân rộng |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1. NOC Alert Summarization | Tốt | Tốt | Xuất sắc | Xuất sắc | Rất hợp | Không | 4 | Xuất sắc | Rất cao |
| 2. Config Script Drafter | Khá | Tốt | Tốt | Cao | Rất hợp | Không | 3 | Tốt | Trung bình |
| 3. Field Ops RAG | Xuất sắc | Xuất sắc | Tốt | Cao | Rất hợp | Không | 4 | Xuất sắc | Rất cao |
| 4. QoS Report Validator | Khá | Tốt | Trung bình | Cao | Rất hợp | Không | 5 | Trung bình | Cao |
| 5. CR Risk Predictor | Khá | Trung bình | Tốt | Rất cao | Rất hợp | Cân nhắc | 4 | Tốt | Cao |
| 6. Doc Normalizer | Xuất sắc | Xuất sắc | Trung bình | Cao | Rất hợp | Khá hợp | 5 | Trung bình | Cao |
| 7. HR Policy Q&A | Xuất sắc | Xuất sắc | Xuất sắc | Cao | Không | Rất hợp | 4 | Xuất sắc | Rất cao |
| 8. Contract Term Extractor | Khá | Khá | Tốt | Rất cao | Không | Rất hợp | 3 | Tốt | Rất cao |
| 9. Daily Reporting | Tốt | Tốt | Tốt | Cao | Cân nhắc | Rất hợp | 5 | Tốt | Cao |
| 10. Smart Ticket Triage | Xuất sắc | Xuất sắc | Xuất sắc | Cao | Khá hợp | Rất hợp | 5 | Xuất sắc | Rất cao |
| 11. Onboarding Workflow | Xuất sắc | Xuất sắc | Tốt | Cao | Không | Rất hợp | 5 | Tốt | Cao |
| 12. Sentiment Analyzer | Xuất sắc | Xuất sắc | Trung bình | Cao | Không | Rất hợp | 5 | Trung bình | Cao |

Dựa trên bảng so sánh và phân tích chuyên sâu về quy trình tự động hóa tại doanh nghiệp [cite: 1, 17, 39], chiến lược phân nhóm lựa chọn như sau:

**1. Ba bài toán nên ưu tiên dùng làm bài mẫu theo từng session chính:**
*   **Phân loại định tuyến Ticket (Bài 10):** Bài mẫu cho Buổi 2 về quy trình làm việc AI, rẽ nhánh, logging, xử lý lỗi và HITL [cite: 12, 38].
*   **Trích xuất dữ liệu hợp đồng pháp lý (Bài 8):** Bài mẫu cho Buổi 3 về tác nhân AI, chuẩn đầu ra JSON, prompt boundary, self-check và test cases.
*   **Trợ lý giải đáp chính sách nhân sự (Bài 7):** Bài mẫu cho Buổi 4 về nền tảng RAG, trích dẫn nguồn, từ chối khi thiếu căn cứ và kiểm soát ảo giác [cite: 10].

**2. Ba bài toán phù hợp nhất cho nhóm kỹ thuật:**
*   Tóm tắt cảnh báo NOC (Bài 1)
*   Trợ lý RAG tra cứu cẩm trạm hiện trường (Bài 3)
*   Nhận diện rủi ro thay đổi cấu hình CR (Bài 5)

**3. Ba bài toán phù hợp nhất cho nhóm hỗ trợ:**
*   Phân loại định tuyến Ticket IT (Bài 10)
*   Trích xuất dữ liệu hợp đồng pháp lý (Bài 8)
*   Sinh tự động lịch trình Onboarding (Bài 11)

**4. Ba bài toán dễ làm nhất cho nhóm học viên mới bắt đầu (không nền tảng lập trình):**
*   Trợ lý giải đáp chính sách nhân sự (Bài 7 - RAG thuần)
*   Phân tích cảm xúc khảo sát (Bài 12 - Phân loại thuần)
*   Dịch thuật chuẩn hóa tài liệu (Bài 6 - Chuyển đổi định dạng thuần)

**5. Ba bài toán có giá trị quản trị cao nhất nếu phát triển tiếp sau khóa học:**
*   Nhận diện rủi ro cấu hình CR (Bài 5): Có thể cứu hệ thống khỏi các thảm họa downtime nghiêm trọng [cite: 40].
*   Trích xuất dữ liệu hợp đồng (Bài 8): Quản trị rủi ro pháp lý và kiểm soát phạt vi phạm rất hiệu quả [cite: 32].
*   Tóm tắt cảnh báo NOC (Bài 1): Đẩy nhanh quá trình hiện thực hóa mục tiêu AIOps mạng lõi và tiết kiệm hàng ngàn giờ lao động định kỳ [cite: 8, 41, 42].

## Phần 5. Gợi ý Dữ liệu Mô phỏng

Tuân thủ AI (AI Compliance) và bảo vệ Dữ liệu Định danh Cá nhân (Personally Identifiable Information - PII) là quy tắc bất khả xâm phạm. Dưới đây là phương pháp tạo lập dữ liệu tổng hợp (synthetic data) chi tiết cho từng bài toán cụ thể để đảm bảo an toàn vận hành [cite: 6, 33].

### 5.1. Bài toán Tóm tắt Cảnh báo NOC
1. **Loại tài liệu:** Tập tin CSV hoặc file log văn bản.
2. **Số lượng mẫu tối thiểu:** 50 - 100 dòng log sự cố.
3. **Cấu trúc dữ liệu gợi ý:** Gồm các cột `[Timestamp]`, `[Node_Name]`, `[Error_Code]`, `[Severity_Level]`, và `[Message_Description]`.
4. **Những trường dữ liệu cần tránh:** Không sử dụng dải IP thật, tên trạm hoặc tên thiết bị thật (hostname) đang vận hành trong mạng VTN. Tuyệt đối không dùng thông tin tọa độ GPS có thực.
5. **Cách làm dữ liệu đủ giống thực tế:** Sử dụng LLM tạo sinh (như ChatGPT hoặc Gemini) với câu lệnh: "Tạo một danh sách giả lập 50 dòng log hệ thống định tuyến, trong đó mô phỏng một sự cố rớt kết nối Giao thức định tuyến liên mạng (Border Gateway Protocol - BGP) và Giao thức định tuyến nội mạng (Open Shortest Path First - OSPF) lặp lại liên tục do lỗi card quang ảo của hãng X".

### 5.2. Bài toán Trợ lý Cấu hình Thiết bị
1. **Loại tài liệu:** Tập tin văn bản (TXT) chứa cú pháp câu lệnh (Command Reference).
2. **Số lượng mẫu tối thiểu:** Danh sách từ 15 đến 20 câu lệnh chuẩn của một hãng.
3. **Cấu trúc dữ liệu gợi ý:** `[Command_Syntax]`, `[Variables]`, `[Expected_Result]`.
4. **Những trường dữ liệu cần tránh:** Tránh đưa chuỗi mật khẩu quản trị mạng nội bộ thực tế, khóa mã hóa (encryption keys), hay chuỗi chứng chỉ SSL thật.
5. **Cách làm dữ liệu đủ giống thực tế:** Dịch và điều chỉnh một phần nhỏ cẩm nang hướng dẫn cấu hình thiết bị nguồn mở (như Open vSwitch) hoặc dùng một ngôn ngữ cấu hình hư cấu (VD: ViettelOS giả lập) với các quy tắc do người dùng tự đặt ra.

### 5.3. Bài toán Tra cứu Cẩm nang BTS
1. **Loại tài liệu:** Tài liệu PDF nhiều trang dạng sổ tay kỹ thuật.
2. **Số lượng mẫu tối thiểu:** 3 tài liệu PDF, mỗi tài liệu 10-15 trang.
3. **Cấu trúc dữ liệu gợi ý:** Chia làm các chương mục rõ ràng: "Triệu chứng", "Mã lỗi trên đèn LED", "Các bước khắc phục 1-2-3", "Tham số kỹ thuật".
4. **Những trường dữ liệu cần tránh:** Tránh ghi rõ tần số vô tuyến nội bộ mật, sơ đồ đấu nối trạm lõi nhạy cảm hoặc quy trình bảo vệ vật lý trạm.
5. **Cách làm dữ liệu đủ giống thực tế:** Tải các tài liệu bảo trì điện tử dân dụng hoặc tài liệu thiết bị viễn thông công cộng, sau đó đổi tên thiết bị thành mã thiết bị giả lập "BTS-VXX-2026" và điều chỉnh một số thông số cường độ dòng điện ảo.

### 5.4. Bài toán Đối chiếu Báo cáo QoS
1. **Loại tài liệu:** Tập tin bảng tính Excel (XLSX) hoặc CSV.
2. **Số lượng mẫu tối thiểu:** 2 tập tin báo cáo tượng trưng cho Tuần 1 và Tuần 2, mỗi file khoảng 30 hàng.
3. **Cấu trúc dữ liệu gợi ý:** `[Khu_vực]`, `[Mã_trạm_mô_phỏng]`, `[Tỉ_lệ_rớt_cuộc_gọi_%]`, `[Tốc_độ_tải_xuống_Mbps]`.
4. **Những trường dữ liệu cần tránh:** Lưu lượng thực tế, số liệu doanh thu thực trên mỗi trạm, tọa độ địa lý.
5. **Cách làm dữ liệu đủ giống thực tế:** Sử dụng hàm ngẫu nhiên của Excel (RANDBETWEEN) để sinh các con số KPI bình thường ở đa số trạm, và chủ động cấu hình 3 trạm có sự tụt giảm hiệu suất đột biến (VD: Tốc độ tải giảm 50%) để làm "bẫy" cho AI nhận diện.

### 5.5. Bài toán Dự báo Rủi ro CR
1. **Loại tài liệu:** Phiếu mô tả sự cố (Post-mortem incident reports).
2. **Số lượng mẫu tối thiểu:** 20 phiếu sự cố lưu trữ dạng Word hoặc JSON.
3. **Cấu trúc dữ liệu gợi ý:** `[Mã_Sự_cố]`, `[Mô_tả_CR_Gây_lỗi]`, `[Thiệt_hại_ước_tính]`, `[Nguyên_nhân_gốc]`.
4. **Những trường dữ liệu cần tránh:** Tránh cung cấp thông tin lỗ hổng bảo mật Zero-day chưa được vá của mạng lưới, hoặc tên kỹ sư phê duyệt thực tế trong quá khứ.
5. **Cách làm dữ liệu đủ giống thực tế:** Tạo dữ liệu mô phỏng bằng cách viết kịch bản giả tưởng về việc thay đổi thông số phần cứng A vô tình làm sập phần mềm B.

### 5.6. Bài toán Chuẩn hóa Tài liệu Đa Vendor
1. **Loại tài liệu:** Tệp Word (DOCX) mô tả thông số mạng.
2. **Số lượng mẫu tối thiểu:** 4 mẫu tài liệu ngắn gọn của hai Vendor "X" và "Y".
3. **Cấu trúc dữ liệu gợi ý:** Các đoạn văn chứa các từ khóa đặc thù (eNodeB vs Base Station).
4. **Những trường dữ liệu cần tránh:** Giá mua thiết bị bí mật trong hợp đồng đấu thầu, hoặc kiến trúc lõi độc quyền chưa công bố.
5. **Cách làm dữ liệu đủ giống thực tế:** Chỉ tập trung vào một tập con nhỏ của ngôn ngữ viễn thông (tầm 20 từ khóa) để minh họa quy trình từ điển ánh xạ (mapping dictionary).

### 5.7. Bài toán Trợ lý Chính sách Nhân sự
1. **Loại tài liệu:** Sổ tay nhân viên định dạng PDF hoặc TXT.
2. **Số lượng mẫu tối thiểu:** 1 tài liệu tổng hợp khoảng 20 trang.
3. **Cấu trúc dữ liệu gợi ý:** Các điều khoản quy định về thời gian làm việc, bảo hiểm y tế, quy trình xin nghỉ phép thường niên, phụ cấp làm thêm giờ.
4. **Những trường dữ liệu cần tránh:** Tuyệt đối không nạp bảng lương thưởng thực tế, cơ chế KPI cá nhân, hoặc dữ liệu PII của bất kỳ nhân viên nào.
5. **Cách làm dữ liệu đủ giống thực tế:** Lấy khung Bộ Luật Lao động Việt Nam hiện hành, bổ sung các chính sách hư cấu nhưng có logic chặt chẽ (VD: Phụ cấp đi lại vùng sâu vùng xa cấp độ 2 là 500,000 VND).

### 5.8. Bài toán Trích xuất Hợp đồng
1. **Loại tài liệu:** Hợp đồng thương mại mẫu (PDF định dạng scan hoặc Word).
2. **Số lượng mẫu tối thiểu:** 3-5 mẫu hợp đồng.
3. **Cấu trúc dữ liệu gợi ý:** Điều khoản thanh toán, điều khoản bồi thường, thời hạn hợp đồng, nghĩa vụ các bên.
4. **Những trường dữ liệu cần tránh:** Tên doanh nghiệp đối tác có thật, dấu mộc thật, số tiền đấu thầu thực tế hoặc mã số thuế thực.
5. **Cách làm dữ liệu đủ giống thực tế:** Sử dụng các mẫu hợp đồng trống công khai trên thư viện pháp luật, điền tên "Công ty Viễn thông A" và "Nhà cung cấp B", thay đổi ngẫu nhiên tỷ lệ phạt hợp đồng (5%, 8%, 15%) để tạo đa dạng kiểm thử.

### 5.9. Bài toán Báo cáo Sản lượng Hàng ngày
1. **Loại tài liệu:** Bảng dữ liệu định dạng CSV.
2. **Số lượng mẫu tối thiểu:** 1-2 bảng tính chứa 30 hàng đại diện cho các nhóm chi nhánh.
3. **Cấu trúc dữ liệu gợi ý:** `[Tên_Chi_nhánh_Mô_phỏng]`, `[Doanh_thu_Ngày_T-1]`, `[Doanh_thu_Ngày_T]`, `[Mục_tiêu_Tháng]`.
4. **Những trường dữ liệu cần tránh:** Doanh thu kinh doanh thực của từng tỉnh thành, cơ sở dữ liệu khách hàng.
5. **Cách làm dữ liệu đủ giống thực tế:** Khởi tạo dữ liệu trên file Excel bằng các hàm random số học mô phỏng cho chuỗi doanh thu ảo, gài một chi nhánh tụt doanh thu 30% để AI có dữ liệu để bình luận.

### 5.10. Bài toán Định tuyến Ticket IT
1. **Loại tài liệu:** Tập tin văn bản thô hoặc JSON chứa danh sách phàn nàn.
2. **Số lượng mẫu tối thiểu:** 50 ticket mô phỏng.
3. **Cấu trúc dữ liệu gợi ý:** `[Ticket_ID]`, `[User_Input_Text]`, `[Timestamp]`.
4. **Những trường dữ liệu cần tránh:** Thông tin mật khẩu của người dùng, phàn nàn nhắc đến tên thật hoặc lỗi cá nhân nhạy cảm.
5. **Cách làm dữ liệu đủ giống thực tế:** Sử dụng các nền tảng mở như Reddit hay diễn đàn IT, sao chép các lời phàn nàn phổ thông như "Màn hình bị sọc", "Không in được", "Mất kết nối WiFi", sau đó dịch qua tiếng Việt và chuẩn hóa giọng văn công sở.

### 5.11. Bài toán Quy trình Onboarding
1. **Loại tài liệu:** Biểu mẫu điền thông tin nhân sự dạng JSON hoặc CSV.
2. **Số lượng mẫu tối thiểu:** Thông tin của 3 hồ sơ nhân sự giả định vào 3 vị trí khác nhau.
3. **Cấu trúc dữ liệu gợi ý:** `[Tên_Nhân_Viên]`, `[Vị_Trí_Tuyển_Dụng]`, `[Ngày_Bắt_Đầu]`, `[Phòng_Ban]`.
4. **Những trường dữ liệu cần tránh:** Số CMND/CCCD, số tài khoản ngân hàng, ảnh chụp chân dung thực tế.
5. **Cách làm dữ liệu đủ giống thực tế:** Tạo thông tin hoàn toàn hư cấu như "Nguyễn Văn A - Kỹ sư DevOps", "Trần Thị B - Chuyên viên Marketing", đảm bảo luồng điều phối (orchestrator agent) nhận diện và sinh ra email kịch bản riêng biệt tương ứng cho các nhánh kỹ thuật và hỗ trợ [cite: 3].

### 5.12. Bài toán Phân tích Cảm xúc
1. **Loại tài liệu:** Danh sách nhận xét đánh giá định dạng CSV.
2. **Số lượng mẫu tối thiểu:** 100 dòng phản hồi bằng tiếng Việt.
3. **Cấu trúc dữ liệu gợi ý:** `[Feedback_ID]`, `[Topic: Căng tin / Mạng nội bộ / Khóa học]`, `[Review_Text]`.
4. **Những trường dữ liệu cần tránh:** Phản hồi chứa từ ngữ bôi nhọ cá nhân cụ thể, đánh giá hiệu suất trực tiếp của một lãnh đạo thực tế.
5. **Cách làm dữ liệu đủ giống thực tế:** Yêu cầu một LLM sinh ra 100 câu nhận xét ảo (VD: 40 câu tích cực, 40 câu tiêu cực, 20 câu trung lập). Chỉ định rõ LLM sử dụng ngôn ngữ tự nhiên công sở, gài thêm một vài câu châm biếm nghệ thuật (Sarcasm) để thử thách kỹ năng phân tích sâu của công cụ AI.

## Phần 6. Khuyến nghị cho Giảng viên 

Buổi 1 là buổi "định âm" cho toàn khóa. Thành công của 5 buổi còn lại phụ thuộc 80% vào việc giảng viên dẫn dắt lớp chọn được đúng bài toán. Sự chuyển dịch tư duy từ việc "Dùng AI để làm hộ mọi thứ" sang "Thiết kế hệ sinh thái Đa tác nhân (Multi-agent AI ecosystem) phối hợp cùng con người trong quy trình nghiệp vụ" là điều kiện tiên quyết [cite: 3, 22, 43].

Khuyến nghị cách điều phối Buổi 1:

**1. Cách giới thiệu danh mục bài toán:**
Không liệt kê cả 12 bài toán một cách khô khan. Giảng viên nên dùng phương pháp kể chuyện (storytelling), vẽ lên bảng 2 trục: Trục ngang là Quy trình Kỹ thuật (Mạng), Trục dọc là Quy trình Doanh nghiệp (Nội bộ). Đính các bài toán vào giao điểm của luồng công việc. Nhấn mạnh việc các bài toán này là những "viên gạch nhỏ" (micro-use cases) để xây dựng kiến trúc tự động hóa diện rộng (orchestration layer) sau này [cite: 3].

**2. Cách giúp học viên chọn bài toán vừa sức:**
Yêu cầu học viên chấm điểm theo khung 11 tiêu chí (ở Phần 2) đối với chính ý tưởng của nhóm mình. Nếu tổng điểm ở các tiêu chí cốt lõi (Độ rõ đầu ra, Tính lặp lại) quá thấp, giảng viên phải phủ quyết ngay lập tức. Hãy hỏi: *"Bạn có thể tạo ra 50 mẫu dữ liệu giả trong 15 phút tới không?"*. Nếu học viên ngần ngại, hãy ép họ chuyển sang chọn 1 trong 12 bài toán đã chuẩn bị sẵn ở trên.

**3. Cách tránh bài toán quá lớn, quá mơ hồ hoặc quá rủi ro:**
Phải thiết lập lan can an toàn (guardrails) cực kỳ cứng rắn ngay Buổi 1 [cite: 6, 33]. Cấm các từ khóa mĩ miều như: "AI tối ưu toàn mạng", "Trợ lý vạn năng", "Tự động sửa mọi lỗi thiết bị". Đóng khung lại bằng cụm từ: "Trợ lý thu thập log", "Trợ lý dịch tài liệu", "Trợ lý báo cáo nháp". Yêu cầu học viên cam kết luôn có bước "Chuyên viên xác nhận" (HITL) trong mọi thiết kế kiến trúc [cite: 16, 38, 44].

**4. Cách chọn bài mẫu theo từng buổi thực hành:**
Giảng viên nên bám theo bộ bài mẫu chính thức thay vì ép một bài toán duy nhất chạy xuyên suốt toàn khóa. Buổi 2 dùng **Bài toán 10 (Smart Ticket Triage)** để demo workflow, logging, error handling và HITL. Buổi 3 dùng **Bài toán 8 (Contract Term Extractor)** để demo tác nhân AI, JSON schema, prompt boundary và self-check. Buổi 4 dùng **Bài toán 7 (HR Policy Q&A)** để demo kho tri thức/RAG và trích dẫn nguồn. Buổi 5 và Buổi 6 tập trung công cụ nhỏ chạy local, kiểm thử tuân thủ và đóng gói triển khai.

**5. Cách phân nhóm học viên theo lĩnh vực kỹ thuật và hỗ trợ:**
Sàng lọc danh sách 100 học viên trước giờ lên lớp. Ghép nhóm 4-6 người có cùng chuyên môn hoặc làm cùng một luồng quy trình (VD: Nhóm xử lý CR, Nhóm Hỗ trợ IT). Không nên ghép một kỹ sư cấu hình lõi với một chuyên viên nhân sự vào chung một nhóm làm dự án, vì họ sẽ mất thời gian thỏa hiệp về dữ liệu đầu vào.

**6. Cách chốt phạm vi tối thiểu (Minimum Viable Product - MVP):**
Cuối Buổi 1, mỗi nhóm phải nộp lên hệ thống: 1 cái tên dự án, 1 mô tả đầu vào (kèm ví dụ dữ liệu giả), và 1 định nghĩa về cấu trúc dữ liệu đầu ra cực kỳ chi tiết. Giảng viên ký duyệt "hợp đồng" MVP này với các nhóm. Nếu học viên làm đúng và đủ MVP đó trong 5 buổi sau là coi như hoàn thành khóa học. Mọi ý tưởng phát triển tính năng phức tạp sẽ được đưa vào "Danh mục mở rộng đa tác nhân" để tiếp tục triển khai trong chiến dịch 30/90 ngày sau khóa học [cite: 3, 17].

**Sources:**
1. [vellum.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG6eTYQl3jKuMi-dSHJwjlc4-ko19-cPWokbIQFxxUX0dy7ymP2ezk0EebfDVP9Qg1yTUrFXIVVqGQLw7GLLue1bKgAy42Yns5Ona7ngIPkJDgvVw51iLec59KFie9LptJHXEizR65P5fYT3VZiCds3YvR-ikQ7c-UuSss=)
2. [infovista.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYwJNy66pWrzfgNJlMx03Bg5oY17tuPnF8FBqTuUxHuKPfckYWspXujgqVlOrkrnY72x7zc0Hi-7TbPy80im9DMopwd-cRU6uUV9oKFxooNBl9NYT4ZfjmGKJPhkdOZusyfR-2NHEP_53WArmpi1ZsPwutiA==)
3. [deloitte.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEI8DMGeIf0neLXl84X9OzPVXPorKq50uDwXWHLl1Yz8-VXnzMKAqXDlCPGWjL4rDfU7oAM4aI9aqT9R4Br5wjD5oJvUOcHYHrJSoxnErughenVCAJs2cJPHe7Bd6XKEWh2nAa5pHVaBpBU9TCgMopwsf272FXEln63rEAHGf3qJuW00-ZX-hFhVGincbXYRmtXl_TP4Wapu45d0plhLuZOtfCYIxTblUkaWmKieKIM)
4. [cloudfresh.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHKb-Bj2njzIX4-MwTmpFoEto6f_CRFd4R-lHcNiFLdjgaOPyFE2vQJIz2-ShwZG-AiO84Bg2CzVwN6F0LkPYdx9zZN_xLF5leyJcsbN0bhGfC8jHWqSHDC2M3WnmVpRrj4dQ==)
5. [ibm.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbAy0DWvn-Y4y9orgx94yzRt3IGA4MQzViYhhaGEBcANmeYfbmMKh0lvc0utH59Pqy8w88HADFQ6GNY19t_dA01ajKOA4IAz89KNwv5--WkjxF_NgavpGIMjEI85aOPKVCtY1V9E1nu5-KmUtUmQ==)
6. [modulos.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHGmknrabSAXek1ebLdmXWq9_RkogGsfJvFfXd_W3AOfjME5_IrpfdPS9wabKNbSi0sKWu4iPVgSIZGQKppL6ioOarOjuQDWczYWgTLZARf3r1Z-14M7eXVKmpA4tPlnXNz_y4n_NOb3c0h0Q7NUg==)
7. [nist.gov](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETSyR4rsLkQyOrhC6CtvFG7FbI9UnxgE-vlI6wUunDC7g8NccfI_U-tDW-GmfJy5BfH9tOpx-ub-oVN-Q5WS0fzq9v0dGRioucVYrJz61zB6vCvV-yW8qfVxfqxOBbqGThaz4PuLlzP48eQw==)
8. [amasol.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGJYYFEZi4m15g2pIG-hho-ZHou4rS33dwSsIoafsT0Njv3zFLaagTrh6sCSfNYqzAofsS5R4glf8_vM41npMPrvncdaxoE5T_bWz2Qaxjz3VYqgn2aYdBPP69t1ax26HXqey5AKBTRCwEweF3OEudIVyhqmUA5Bu3jry-90tyF2NwpK3sbDgvnmuldHkK378vbIvrETOFLxYfbQKVrbQ==)
9. [bigpanda.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF4u_MeQSQiSpWYARz1rqADzpdE5I0fKe7FOHNO1uHm1kL4X4s7YdmXmLtqkv7LGEarIsy71MVqKdt7vSII6TYj7fjVEyBFV7DRTf1P-nyzvTnPzO00tsQHIekJdSnV8O-IUzsb)
10. [evidentlyai.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHEkW52PSkbfV64kK_ZIatfdGpii2h96690T8pFy9oC5b6mFT7MFXwZTu1gbKg48s6VLkXDBPS6PQnV27FN150tXTftrYtUj6tFfMFmP707O6sZchfPnbjQrgvLDAz4fYjx3Q==)
11. [logicmonitor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZbVKp-dEX50RLJoKzLhrA0SyP_T2XfvwmHoSc31huYkEPWkrbEUdB7g01_Vjcr09_ByQ9GG5lDGUhcYrp-UsnpoIv7vBa7CbiJBw7JXPZx7BeJrctX_CMrM68DZajuJy9AtGloBu8wKniP4xrNA==)
12. [getstream.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5FI9DUaSAyBXG4OWi98aiQot2Ht_fjR3AerbY4IHr3RoZMsiU9XuFBW1c94fUAPR_Fu2jWBppNkDgYNyPrhs-vC88IPL1tFvX5gq3XyWa6Z2thc-umKPsX2xk3sb7536LNIckJvlaqg==)
13. [diligent.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF9Dz99rQzi4kSq4KXkp7TSVwYENcF7SZfQpNtCJfxG42HrBfBpf24QOzNfE_f9FYWVDDDb7s-aq64EyD7ncnhlXXR8FhveuVQpGPALMU3hMNN21xPzbFdQyOs_aFgY5yCJfiSGYP-AFxDWCxLufKA6qGrPQTVlQrjkT7UukW0=)
14. [lumenalta.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEvnVJIFDxMT0AElwsLhWLWoXWvzgR3Tc8RIijoegLwQwI778q7GkMtN3pIpvlJuq1pe85ACyVJ2K7HstCmukfmHCuQNNOyAaHtow6_MduGDhwH6rjWAozcVsYVAlKNC9zFtUhEU7Ds6wa8qQKgTD_ksWR0Nc-hBrg=)
15. [tonic.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGb0QKwmpIsGxREaADItYqbMA6BCOHU20Kj2Gtb63BsFrfAkhVMOFSiXCsYUSMWw_MRr9T3_LoH_kAfnIL5OlENAYL04JS_QVnFoTcJNLR6WlE6YHUYWY44KyZWAVq6XPvXn5o7_315a5RD7DzqawBjE7c6zeYwvw5uk_NqLq_KtZQI)
16. [nvidia.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYxm13zp9wIArl6afOVlbEdsJUE1LXbQPGpPrV-HfqhHz3LcOaZCsLOO_KKSfprmGNxl3hy76ha-7iSAT5Zs9LflevqXCIl7Q-d6GCGQLr23Knj05C3AR87JfGN99zK4Bpnk_8Tl0ksWI9xvxPs62r6WBE69kN)
17. [deloitte.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGad--eZM33WsVtw4veeqoDZ__udieDCI6-hatJ5QGjJLk-Vc1tbzJ3dt3R3PJUXPOBg_CKhQ26jbLdtJKK3D92s6dlH5SSTI5ujcz02av2YjTVSoa3l6EKEjwx8FXqWV6peH5DDBsjLPJ4CuvIUgw7QgkAopYuPg8djOXoK028PzjphvweF3eqE8A6OW-H5-96fWbqrTM37SdwfT8LsVX3oybLVt0=)
18. [softwaremind.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFPMQbpDmi4Gxltc4VMTICaFEviC-h0u9TAl_qFeIc1HPjSJIlSoxXQkrpbPgCEswZssczs6MSFJYdJ1P3CV4MSR51dj-GSifAx4bjnQcrSlflA1KADLpcucKacgQSQ6zsoenb3QXh9NQaVEUu1mOxhKy4JuPA0njVMQWnif1lkjAyEzlDQoHzo)
19. [gartner.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwv0VOUt1unMCVtwxmZPM15CGWigg-bbnp0j1J_zChbl8IhPfGX-SvZsysgcMlhZ68zQ0OOscNhzP0veptn6MzQI5w4bPdMt760lf_uugTbB5Fvo2c74UAn-hHCxFHSUoe)
20. [mindtitan.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQ65tK1xzqvwROWP8A8JhqRItYrsACzJHDty3Mf5SbVacSRMTQe4f3jNTzt3ctHynxZdNLYbA3MKCQ0oI28HAJ7ZYu-0IiBeOnXSl5HiSHgiME9hn9Q0XnKi-N226nXQtsPjTSq9OVbaz3gmo-lEaPrHzWGuCoKtuG8Np7LbqLb9IGgmXWszm0ns71SUSqijatYg8o)
21. [dtskill.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYePVtBMVlHtyYCwCMeAYwgpfaJ6NyR3B9aqJTfDAAPoo7D1PIpJUDhqDP8xAEKP9oUkZtRoLmiQTptyLBK9MLbL6X7dRv4X1fJHc7Ug0MBCmnt4hLQkMK3tOdkWw4xyubi-6czZZc3GWgyQCLR0_3-uo=)
22. [rcrwireless.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFv8nWglPYXsmX900aV188pqbQb4BjigheuEeh9Old1lewEw7PFbkoqm3P7bnYvkpipchsVBd2Zlhrb0WF4VJrJECD5bM9SiTnqpYRf3Yfl4x81vHlFjBj8HecyZRMF1K19J3JejmEd5pzllpZeVaKrYg==)
23. [ibm.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGzwxle49ccHnr7TACwdfGARLIuEEXUxk4fTa-3iFxm4Y0yO-uS_u1CHqQDGQbNjJtDo9e4pT27Kc9eUl4EM4FJPEuYHxg2yFDloP0C9A9dqVbsDr7Vwt-ftndADQuHxHEXS0CpmOavn3kCgDjVXuoPwu3q3RGsD1g8pg==)
24. [aihr.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG9wXejIU67X6Ocpfremd4QkM7iFLlJySbHCOsnTIbIpwADbHuPcGeNkHHGrFmkQNPIn8nIEJt1tyX54MoDswNeqJ0ZR5A0AxrHA9TBF22WhvYuv-Bd60crv3UFPgC_7TCQhAw=)
25. [articsledge.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFKi03CiQk6PnN22v8n18nom_iE_0_wZsvsDZyr3UueHLjIbzBN7uMQjZdkTrUWf3mzHxw3ZMub15StpkyFbxqhclZQu1szSQ6pPeBjm77Vpgt7WtUdmlRd3zaNkdqzQrPYgJSlgoCHyCwt5Q==)
26. [glean.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGuo-NAnK0QHN2XDXuNJxPXRgAj9SxGXvYbuAvfE1yvy63Mn2BWLotv4QBL_oXJ0wdfHCjENTCbMrMrp4rJZUxP5__77yAqZrZsnW2H2256svyWJdNpG5Csf3TWWMSyV53FZNAmNatsQvz0C9BWmMQ2f-1kliMDmYk=)
27. [indigo.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtoW7SSG1oPHanfT3kfqdpRDpi5Bq_R8I7HqThE_zPiD8euyARlJMN2qs0nGb_388u5amsSnRPFtj9Tc-F7nmir4QFFK0G44SfvK0RRFIztY8mGeHDDZCnKm3LihUZanrm4LV9Svg4MADfgP2kdQ==)
28. [meilisearch.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGK7ZGAL0DSEfd80pGTJnn9qCIaIwyO5LqWNwgwklZtaK3A3xFYvUomnblYy94ZEkK-Z8gEdD6xmcwHpa8tM0CsNep53MUke6jD6Sl-RCfZfEYw43Z47aHxRtPrSBk9AR6YMtQT7yM=)
29. [automationedge.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGI9oISFvfsOvPiW5_6HP08trA40RHBkAEidM6IhR99xhkrKce_ymmJf_Z90ByCSFwa4owpfGLePjwSWg4knZ3midsMWCCL30sf5heVCQkg0zI2hwVlDrzJqo5IWDqo9CMYCOKOk_VvPE1GC_YjA09PDLc=)
30. [talentia-software.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGwOLXDhzJF-Y6jJ2E-bUz9tSYjpIjrcct_F9vCFAjYqf-44yVRELhzYN9jaTO4N5gUqow5CKeRquqP2NBornoptZXy-RqgXarUqZtCGm4rqUUOFpLqq3p8rSKzs3T1stqvaOlw1fTbYO4-0erUrp-knrPN5aI=)
31. [nsight-inc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGbVaAkBVL6ytsa0WNZ1CIJ1cQfd_hQ7o5tQx5ZpTHzaiec6LxbFzuoYWmzl2c2iyCubvjCtHxRfcTWohGaYsl6B2gdwKGJG_ruWVNUdRKHWk5CHeGn56G-AQ3nShod-x17Hg==)
32. [gartner.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGqhfhdJEri3m_e0vzcImwooFnAGJnd7oVqSRr-nMS2u37xagxVkvxaObcaIlBURUpoPd64Pw3RjHQKqf9ECSv8Pvrl2Hc8_dzQAU2v9aQfrvVgFJNbGw_H6rv6_HMfPHUWq2Bw9gCoNgRFtA0oHS6pSUX76hfLAFr64L684awqMQmUo2XS5PuDX7icxIp66kWVKvUrdW26RwKIGosfur52zCQjvFwVGSCKH_5UAKLxSTl79CuD9qIh5HlWq9xgsiGZ)
33. [agatsoftware.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGDzkgvLxIaGgkYNEB7ONMo63QHRGlAEZRFK3IBEDTTh7Yg1Uw1dxVaiwtyKnVQLJGvC9fK-hIlcNw3TJrgQoRkem21X63raVPruu2jfkc63RL-MwFsxMqPWb6oH_gSU1OLctnSdYW4pZMd8jyTQ36pYe0iYSNF)
34. [qontak.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEK_wjJ1nkwsewOzgGIgjbNarE4ZSPmqHOjwabIQ2MDJrGxCo-_BI756GDdw6SxSxikkXc_bsvyQfosNBu1XA8Pt6hzRmc0RHU4BK-umr99QO-sgCumzcRBjwS2bCP-p1CNNprMMM6Qo9hJFpBb_WRSNHheIbxxN30VhAT3L4pFbw==)
35. [jitterbit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEcMLkCjJidwyG8wu2TdRzDmtXBM-UKuyJEW9ey8TFMCTG2Y7slh_C9j-PmtHv5Jd4nNAWQuRPe_o0pehbNRhUOWkvjO3ItgB9EsF23tSHwEvB_H7lOxZVBe_-RJSdcOkuL-kJfb6S4CUAewdpq0Mh3f4fdi9cm5glWp9QI)
36. [zingtree.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQ0K9CCKY4Sl9jnpJbpaxhe8a_XBYr9bBYRLtNmG6ZppglnKTw3AFxENx8viVdDz9vDLcphp7OjUunfH5TNAkUEN2A9rKZbUsyt5xwC1FYUzTJPps4zyMHrMmEMLFTq_WzVKrCALtGHpmSxVEDIN5ndz1vaQJyH2zHBCYbgcU=)
37. [addvaluemachine.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNHpOt07QPzjgUh0rtAAviR9Rq73yv33qM3lWWdBkXweM5On2ZvjOaw-Db5MS7jMHZJF2Kq3ta2NIx1XX0ndLNQeHlba6k8xkBiU8qn-kSHKouq7Hmn5K-41pn9jtTJNppp9AWOuA0hc_Fp6bFm8CsXb5HZqkTX8_p7FWJBw_zBzbKXA==)
38. [pipefy.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFXOSH6waUIEUy3ax4vMVoI5_cMOZw8UK1xyY_6_AqWYMQXWxlxclvxMxAK7JezyRcu-GLbFncITSM3MJ1sV-eU_kVK9sbjOHe8aUonQKKi34vXVWS9zEjnF5WHtVat)
39. [nuroblox.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEy5LNVcN10TgCzqJ2CORJ79Bg2s_7_5v-gKxhDM78aQqvl1DSxMRIm-rPsQstMmdzb097vDrBEQ0LWlvhpYhKXN9l4hTQePmn8p7SMYvpfucaPeRYkEcSwvIJxdzc2R45zfHujkbSjDYn4-SlxNo9sR1sk0kbtAJ_s1I87)
40. [jadeglobal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEClzHpTOnL2I_ibmZl6bm8_XbOXL-9oXwSqHxueoSE3rJKNbHvygCr5vKqNvQKCocWUUwjwgoenpQbTznfniwgxvAssd2KJeMe9fb7Y0DLER-TofoUvahtkCAoF4z5CPm9rpEVsWdYy1plGsxlFn0rCzVgqSJNAAo_2Rc72Uf5358fMCbx)
41. [telecomblogs.in](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGozSpMAFOXydxZWkGSPbeegh6Wdt8SC342uXGL6Ug-TaFYqoQ9bsYl6Yvr-lrTg-gH6QwiSUwb5KzZd6m4rT5hO7OJYmPkT9CBWVQRFF-h6q5MhQzenuA2AtJzbKdFSdgLVPtSfIV8lQW_cY4_XU5DTG6P4cMwi1pl34r70iGGSQWF9NWVf4jP)
42. [circles.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpLa3_qQsaOjq9aAlFTlN8eJ69HSBOJssPeMXqiHtuiCaoTvi5_HmEMYuUdkBoGV2eZv-_aFLMPcWqlHL0VgMXu2iYKZB_7AVBuIxJvOMjBhQX-7dBzQRc9cRwhSlpGg7Lpi6v)
43. [deloitte.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEofAQ-h08qbJhG0X6aPJU3CXx6A-I1uzA9VP6phLV3YlbS-O7lPk6OOYcf17GEx-YyEYyyQJASjk21WttKUZh2l1KZ6g0fLSKRYXPBMod6KLV8ck_u00lgW86sM25poZwBgqQsm4UFTreJ9obyh2RW9uVDK9JEXZR-A4AGViQgSXsP3kyls683bEvMMM4LqIF_gzeNQZg_2dDPHs6ddCQhKTo=)
44. [deloitte.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGVBLP9qA7R_W9iduVKOhJxEnNIvR2_z5v8MP8w39BtnKFQmj-uMQoqe3AHd0a-HHltJlsAbhdlTUNlqEu-sh1FFASqCk1IHGsaoaV4gXyeSyYHiSViPWT07RYPLWB_PlD8B4034jkN-m9Wx3Fe5SK2OGa19lOv8zx6Sw==)
