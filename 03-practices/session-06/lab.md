---
mo-ta: hướng dẫn thực hành chi tiết buổi học RAG cơ bản: Basic RAG
trang-thai: active
phien-ban: v1.6
created-at: 2026-06-17 20:05 +07:00
updated-at: 2026-06-17 21:00 +07:00
---
# Hướng dẫn thực hành: RAG cơ bản (Basic RAG)

> **Mỏ neo Slide bài giảng:** Tương ứng với slide **Hiểu RAG từ gốc** (tài liệu [rag-basic.pdf](../../../01-slides/rag-basic.pdf)).

## 1. Mục tiêu bài thực hành

Hoàn thành bài thực hành này, học viên sẽ nắm được:

- **Biểu diễn số hóa văn bản:** Hiểu cách máy tính biểu diễn từ ngữ và câu dưới dạng các mảng số: vectors.
- **Trích xuất đặc trưng ngữ nghĩa:** Sử dụng thư viện `sentence-transformers` chuyển đổi câu tiếng Việt thành các vector đặc trưng ngữ nghĩa: sentence embeddings.
- **Tính toán khoảng cách ngữ nghĩa:** Tự lập trình công thức tính độ tương đồng cosine: cosine similarity để đo mức độ gần gũi về mặt ý nghĩa giữa các câu trong không gian vector: vector space.
- **Tìm kiếm lai: Hybrid search:** Kết hợp kết quả tìm kiếm theo từ khóa: keyword search và tìm kiếm theo ngữ nghĩa: vector search.
- **Xếp hạng lại: Reranking:** Sử dụng Cross-Encoder để tinh lọc kết quả tìm kiếm có độ liên quan cao nhất.
- **Viết lại câu hỏi: Question rewriting:** Xử lý các câu hỏi mơ hồ, thiếu ngữ cảnh trước khi truy xuất.
- **Xây dựng hệ thống RAG cơ bản:** Tự tay lập trình trọn vẹn quy trình nạp tri thức: ingestion pipeline và quy trình truy vấn: query pipeline kết hợp mô hình ngôn ngữ lớn để trả lời dựa trên tài liệu.

## 2. Bối cảnh và dữ liệu sử dụng

Bài thực hành này giúp bạn tiếp cận công nghệ truy xuất tăng cường: retrieval-augmented generation (RAG) từ gốc rễ toán học và lập trình đơn giản trước khi nâng cấp lên các kiến trúc tác nhân: Agentic RAG phức tạp.

Dữ liệu thực hành là 3 tài liệu quy định công tác phí và tạm ứng hành chính mô phỏng (synthetic data) của **VinaTel Network** nằm tại thư mục `synthetic-data/hr-policies/`:

- `policy-travel-allowance.md`: Định mức phụ cấp lưu trú và đi lại.
- `policy-hotel-limit.md`: Định mức tiền phòng khách sạn tối đa theo chức danh.
- `policy-advance-process.md`: Quy trình và thủ tục tạm ứng, hoàn ứng công tác phí.

Học viên sẽ thực hiện các bài Lab theo từng bước bằng cách chạy trực tiếp các file Python độc lập trong thư mục `templates/` thông qua PowerShell.

## 3. Phân bổ thời lượng buổi học (4 giờ - 240 phút)

Để học viên dễ tiếp cận và thực hành sâu, mỗi bài Lab đều cung cấp sẵn **định dạng dữ liệu, kịch bản hội thoại và mã nguồn mẫu cụ thể** để học viên làm theo mà không cần tự suy nghĩ kịch bản từ đầu.

| Phần             | Thời lượng | Nội dung                                                                                                                                                                                                             | Hoạt động chính                                                                                                                                                                                                                                                                                                                |
| ----------------- | ------------: | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phần 1** |      30 phút | Lý thuyết tổng quan từ slide                                                                                                                                                                                      | Giảng giải lý thuyết 6 module từ slide                                                                                                                                                                                                                                                                                        |
| **Phần 2** |      45 phút | **Lab 1:** Biểu diễn Vector Bag-of-Words (20 phút)`<br>`**Lab 2:** Trích xuất Sentence Embedding (25 phút)                                                                                        | - Thực thi mã nguồn thô.`<br>`- **Thử thách 1:** Thêm câu đồng nghĩa/trái nghĩa được cung cấp sẵn vào code, chạy lại và ghi nhận kết quả.`<br>`- Nhận xét về kích thước vector.                                                                                                           |
| **Phần 3** |      25 phút | **Lab 3:** Tính toán Cosine Similarity                                                                                                                                                                        | -**Thử thách 2:** Thay thế hàm tính cosine bằng đoạn mã tính thủ công (được cung cấp sẵn).`<br>`- **Thí nghiệm 1:** Tính ma trận tương đồng cho 4 câu có sẵn, giải thích lý do số điểm biến động.                                                                               |
| **Phần 4** |      40 phút | **Lab 4:** Hybrid Search (15 phút)`<br>`**Lab 5:** Reranking bằng Cross-Encoder (15 phút)`<br>`**Lab 6:** Question Rewriting bằng LLM (10 phút)                                            | -**Thí nghiệm 2:** Thực hiện 3 lần chạy với $\alpha = 0.0$, $\alpha = 1.0$, $\alpha = 0.5$ có sẵn.`<br>`- **Thử thách 3:** Dán kịch bản chat bẫy có sẵn vào code để xem kết quả viết lại câu hỏi.                                                                                    |
| **Phần 5** |      50 phút | **Lab 7:** Ingestion Pipeline & ChromaDB (15 phút)`<br>`**Lab 8:** Query Pipeline & LLM Generation (35 phút)                                                                                          | -**Thử thách 4:** Tạo và dán nội dung chính sách làm thêm giờ có sẵn vào file mới, chạy lại Ingestion.`<br>`- **Thử thách 5:** Dán Prompt hệ thống cải tiến có sẵn vào code để chặn hoàn toàn ảo giác cho câu hỏi Singapore.                                                     |
| **Phần 6** |      50 phút | **Lab 9:** Đánh giá chất lượng RAG (RAG Triad) (25 phút)`<br>`**Lab 10:** Xử lý lỗi kỹ thuật kinh điển (15 phút)`<br>`**Lab 11:** So sánh hiệu năng Local vs Cloud (10 phút) | -**Thử thách 6:** Chạy đánh giá RAG Triad tự động bằng LLM-as-a-judge.`<br>`- **Thử thách 7:** Chuẩn đoán và sửa lỗi mã hóa UTF-8, chunk size và API quota trên Windows.`<br>`- **Thử thách 8:** Chạy script benchmark đo lường sự khác biệt giữa Local và Cloud embedding. |

---

## 4. Hướng dẫn chi tiết từng bước thực hành (Step-by-Step)

Mở PowerShell tại máy tính của bạn và di chuyển vào thư mục bài thực hành:

```powershell
cd "c:\Users\DELL\Documents\4. Presentations & Training\VTN\vtn-ai-builders-bootcamp-2026\03-practice\day-02\session-rag-basic"
```

---

### Phần 1: Lý thuyết tổng quan (30 phút)

Học viên nghe giảng viên đi nhanh qua các slide lý thuyết trong [rag-basic.pdf](../../../01-slides/rag-basic.pdf) để nắm được các khái niệm cơ bản.

---

### Phần 2: Vector và Embedding (60 phút)

#### Lab 1: Biểu diễn văn bản dưới dạng Vector Bag-of-Words (30 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ TỦ GỬI ĐỒ SIÊU THỊ):**
> Hãy hình dung việc chuyển đổi chữ thành Vector giống như xếp đồng xu vào chiếc **tủ gửi đồ siêu thị gồm 20 ngăn**. Mỗi ngăn tủ được dán nhãn duy nhất một từ trong từ điển (sắp xếp theo thứ tự A-Z).
> Khi máy tính đọc câu *"Tôi muốn tạm ứng tiền đi công tác"*, nó đi dọc 20 ngăn tủ và thả 1 đồng xu vào các ngăn tương ứng với các từ xuất hiện trong câu (như ngăn `công`, `tạm`, `ứng`, `tiền`...).
> Vector của câu chính là **mảng ghi nhận số lượng đồng xu trong 20 ngăn tủ** đó: `[0, 1, 0, 0, 0, 1...]`.

* **Bước 1: Chạy mã nguồn mẫu (5 phút)**
  Chạy file [lab1_bag_of_words.py](templates/lab1_bag_of_words.py):

  ```powershell
  python templates/lab1_bag_of_words.py
  ```

  *Quan sát:* Nhìn vào danh sách từ điển và các vector `[0, 1, 0...]` được in ra trên terminal.
* **Bước 2: Thực hiện Thử thách 1 - Sửa đổi mã nguồn (15 phút)**
  Mở file `templates/lab1_bag_of_words.py` bằng trình soạn thảo. Tìm danh sách `documents` ở dòng 10 và **sửa đổi bằng cách thêm vào 2 câu cụ thể dưới đây**:

  - Dòng thêm mới 1 (Câu 4 - đồng nghĩa nhưng khác chữ): `"Cho em xin ứng trước tiền công tác phí"`
  - Dòng thêm mới 2 (Câu 5 - trái nghĩa nhưng trùng chữ): `"Tôi không muốn tạm ứng tiền đi công tác"`

  *Đoạn mã sau khi sửa đổi:*

  ```python
  documents = [
      "Tôi muốn tạm ứng tiền đi công tác",
      "Quy trình tạm ứng công tác phí của công ty",
      "Tôi muốn mua máy tính mới cho phòng họp",
      "Cho em xin ứng trước tiền công tác phí",
      "Tôi không muốn tạm ứng tiền đi công tác"
  ]
  ```

  Lưu file và chạy lại trên terminal:

  ```powershell
  python templates/lab1_bag_of_words.py
  ```

  *Quan sát:* Từ điển lúc này phình to từ 20 từ lên bao nhiêu từ? Hãy xem vector của câu 4 và câu 5.
* **Bước 3: Thảo luận phản tư tại lớp (10 phút)**

  - Tại sao câu đồng nghĩa (câu 4) có ý nghĩa y hệt câu 1 nhưng vector của nó lại hầu như toàn số 0 ở các vị trí trùng khớp của câu 1?
  - Tại sao câu trái nghĩa (câu 5) có ý nghĩa ngược lại hoàn toàn nhưng vector lại trùng khớp đến 90% với câu 1?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi 1 (Vấn đề đồng nghĩa khác từ):** Nếu hai câu có ý nghĩa y hệt nhau nhưng dùng từ ngữ khác nhau (ví dụ: *"Cho em xin ứng trước tiền công tác phí"* và *"Tôi muốn tạm ứng tiền đi công tác"*), vector Bag-of-Words của chúng có độ trùng khớp thế nào?
> * **Gợi ý 1:** Hầu như không trùng nhau (chỉ số tương đồng cực thấp) vì từ điển ghi nhận các từ viết khác nhau là các chiều độc lập. Điều này khiến máy tính không hiểu hai câu có chung ý nghĩa.
> * **Hỏi 2 (Vấn đề trái nghĩa trùng từ):** Nếu câu 1 là *"Tôi muốn tạm ứng tiền đi công tác"* và câu 2 là *"Tôi không muốn tạm ứng tiền đi công tác"*, biểu diễn Bag-of-Words của chúng giống nhau bao nhiêu %? Tại sao điều này nguy hiểm cho hệ thống AI của VinaTel Network?
> * **Gợi ý 2:** Giống nhau đến hơn 90% (chỉ lệch duy nhất chữ "không"). Nếu RAG tìm tài liệu dựa trên đếm chữ thô, nó sẽ coi hai câu này là gần như giống hệt nhau, dẫn đến việc lấy sai quy định hoặc phản hồi sai nghiêm trọng ý định của người hỏi.

#### Lab 2: Trích xuất Sentence Embedding ngữ nghĩa (30 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ DẤU VÂN TAY Ý NGHĨA):**
> Thay vì đếm chữ thô sơ, mô hình ngôn ngữ (Embedding Model) sẽ dịch nghĩa của cả câu thành một **dấu vân tay kỹ thuật số gồm 384 thông số số thực**. Những câu có ý nghĩa gần nhau sẽ được xếp vào các vùng tọa độ gần nhau trong "không gian ngữ nghĩa" đa chiều.

* **Bước 1: Chạy mã nguồn mẫu (10 phút)**
  Chạy file [lab2_sentence_embedding.py](templates/lab2_sentence_embedding.py):
  ```powershell
  python templates/lab2_sentence_embedding.py
  ```

  *Quan sát:* Chờ mô hình tải về máy tính (khoảng 1-2 phút). Nhìn vào kích thước vector (luôn là 384 chiều) và các giá trị số thực rất nhỏ in ra.
* **Bước 2: Thực hiện Thử thách 2 (10 phút)**
  Mở file `templates/lab2_sentence_embedding.py`. Thay thế danh sách `sentences` bằng 4 câu có độ dài khác nhau cực kỳ rõ rệt dưới đây:
  ```python
  sentences = [
      "Tôi muốn tạm ứng tiền đi công tác",
      "Đi công tác",
      "Định mức tiền phòng khách sạn tối đa của cấp Trưởng phòng tại Hà Nội là một triệu hai trăm nghìn đồng một đêm",
      "Tạm ứng"
  ]
  ```

  Lưu file và chạy lại trên terminal.
* **Bước 3: Thảo luận nhóm (10 phút)**
  Hãy quan sát kích thước vector (shape) của câu cực ngắn ("Tạm ứng" - 2 từ) và câu cực dài (22 từ). Có phải tất cả đều có kích thước cố định là 384 chiều hay không? Tại sao việc cố định kích thước này lại quan trọng đối với máy tính?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Tại sao mô hình embedding MiniLM lại luôn trả về vector có kích thước cố định là 384 số thực, bất kể câu hỏi dài 2 chữ hay dài 30 chữ?
> * **Gợi ý:** Việc cố định kích thước vector giúp máy tính thực hiện các phép toán so sánh hình học (như tính khoảng cách Cosine hoặc Euclid) một cách đồng nhất và cực kỳ nhanh chóng. Nếu số chiều bị biến động theo độ dài câu, máy tính sẽ không thể so khớp các câu với nhau được.

---

### Phần 3: Lab 3 - Tính toán khoảng cách và độ tương đồng Cosine (40 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ CHIẾC LA BÀN ĐO GÓC Ý NGHĨA):**
> Để đo xem hai câu có "cùng ý nghĩa" hay không, máy tính dùng toán học đo góc lệch giữa 2 vector của chúng trong không gian.
>
> - **Góc cực nhỏ (hai vector chỉ cùng hướng):** Cosine Similarity gần bằng **1.0 (100% giống nhau)**.
> - **Góc vuông (hai vector không liên quan):** Cosine Similarity gần bằng **0.0 (không liên quan)**.

* **Bước 1: Chạy mã nguồn mẫu (5 phút)**
  Chạy file [lab3_cosine_similarity.py](templates/lab3_cosine_similarity.py):
  ```powershell
  python templates/lab3_cosine_similarity.py
  ```
* **Bước 2: Thực hiện Thử thách 3 - Thay thế thuật toán tính toán (20 phút)**
  Mở file `templates/lab3_cosine_similarity.py`. Tìm hàm `calculate_cosine_similarity(v1, v2)`.
  Hãy **thay thế toàn bộ nội dung hàm này bằng đoạn mã lập trình thủ công** dưới đây để hiểu rõ công thức toán học tính độ tương đồng cosine:
  ```python
  def calculate_cosine_similarity(v1, v2):
      # 1. Tính tích vô hướng (dot product)
      dot_product = sum(a * b for a, b in zip(v1, v2))

      # 2. Tính độ dài vector 1 (norm v1)
      norm_v1 = sum(a ** 2 for a in v1) ** 0.5

      # 3. Tính độ dài vector 2 (norm v2)
      norm_v2 = sum(b ** 2 for b in v2) ** 0.5

      # 4. Trả về điểm tương đồng cosine
      if norm_v1 == 0 or norm_v2 == 0:
          return 0.0
      return float(dot_product / (norm_v1 * norm_v2))
  ```

  Lưu file và chạy lại trên terminal. Đảm bảo điểm số in ra hoàn toàn trùng khớp với kết quả trước đó.
* **Bước 3: Làm thí nghiệm đối chiếu (15 phút)**
  Hãy so sánh điểm tương đồng của câu 1 với câu đồng nghĩa *"Thủ tục xin ứng trước công tác phí như thế nào"*. Có phải điểm số đạt mức rất cao (>0.75) mặc dù hai câu dùng từ ngữ khác nhau hay không? Giải thích sự vượt trội của phương pháp này so với Bag-of-Words ở Lab 1.

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Nếu hai câu có vector chỉ về hai hướng vuông góc 90 độ trong không gian ngữ nghĩa, thì độ tương đồng Cosine bằng bao nhiêu? Về mặt ý nghĩa, điều này thể hiện quan hệ gì?
> * **Gợi ý:** Độ tương đồng Cosine sẽ bằng 0.0. Về mặt ngữ nghĩa, điều này thể hiện hai câu hoàn toàn độc lập và không liên quan gì đến nhau (ví dụ: *"Hôm nay trời đẹp"* và *"Quy chế tạm ứng công tác phí"*).

---

### Phần 4: Các kỹ thuật tối ưu RAG (50 phút)

#### Lab 4: Tìm kiếm lai (Hybrid Search) (15 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ LƯỚI VÀ CUNG TÊN):**
>
> - **Vector Search giống như tấm lưới:** Quét và bắt tất cả những ý nghĩa tương đồng.
> - **Keyword Search giống như mũi tên:** Bắn trúng đích các từ khóa chính xác như tên riêng, địa danh (như "Hải Phòng").
>   **Hybrid Search** kết hợp cả hai theo tỷ lệ trọng số $\alpha$.

* **Chạy và làm Thí nghiệm đối chiếu tham số $\alpha$ (15 phút):**
  Chạy file [lab4_hybrid_search.py](templates/lab4_hybrid_search.py):
  ```powershell
  python templates/lab4_hybrid_search.py
  ```

  *Thực hiện thí nghiệm:* Mở file. Tìm dòng gọi hàm `hybrid_search` ở cuối file. Hãy thay đổi tham số `alpha` và chạy lại 3 lần ghi nhận kết quả:- **Lần 1 với `alpha = 1.0` (Chỉ dùng Vector Search):** Điểm số của Tài liệu 2 (chứa từ khóa "Hải Phòng") là bao nhiêu?
  - **Lần 2 với `alpha = 0.0` (Chỉ dùng Keyword Search):** Điểm số của Tài liệu 2 là bao nhiêu?
  - **Lần 3 với `alpha = 0.5` (Cân bằng):** Điểm số của Tài liệu 2 thay đổi như thế nào? Điểm số này giúp đưa Tài liệu 2 lên vị trí số 1 trong kết quả tìm kiếm ra sao?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Trong trường hợp nào ta nên thiết lập $\alpha = 0.0$ (chỉ tìm theo từ khóa) và trường hợp nào nên đặt $\alpha = 1.0$ (chỉ tìm theo vector ngữ nghĩa)?
> * **Gợi ý:** Ta đặt $\alpha = 0.0$ khi người dùng muốn tra cứu các từ khóa chính xác tuyệt đối như tên riêng, mã số tài liệu, mã hóa đơn (ví dụ: *"POL-ALLOW-001"*). Ngược lại, đặt $\alpha = 1.0$ khi người dùng hỏi các câu hỏi diễn đạt tự do bằng ngôn từ khác nhau nhưng hướng tới cùng một ý nghĩa ngữ nghĩa (ví dụ: *"Thủ tục xin tiền đi công tác"*).

#### Lab 5: Reranking bằng Cross-Encoder (20 phút)

* **Chạy và quan sát sự thay đổi thứ hạng (20 phút):**
  Chạy file [lab5_reranking.py](templates/lab5_reranking.py):
  ```powershell
  python templates/lab5_reranking.py
  ```

  *Quan sát:* Đối chiếu thứ tự ưu tiên của 4 tài liệu trước khi rerank (điểm Cosine) và sau khi rerank (điểm Rerank).
  Hãy ghi nhận sự thay đổi thứ hạng của tài liệu: *"Vé máy bay hạng thương gia Business Class chỉ dành cho cấp Giám đốc và Phó Giám đốc"* đối với câu hỏi *"Giám đốc đi máy bay được thanh toán thế nào"*. Có phải nó đã được đẩy lên hạng 1 với điểm số vượt trội hay không?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Tại sao không dùng Cross-Encoder (Reranker) để tìm kiếm ngay từ đầu trên hàng triệu văn bản, mà phải qua bước Vector Search (Bi-Encoder) trước để lọc ra top 4 rồi mới chạy Reranking?
> * **Gợi ý:** Vì mô hình Cross-Encoder so sánh cặp câu hỏi và tài liệu đồng thời nên tính toán rất nặng và chậm. Nếu quét hàng triệu tài liệu bằng Cross-Encoder, hệ thống sẽ bị treo hoặc phản hồi sau nhiều phút. Do đó, quy trình tối ưu là dùng Vector Search để "vớt nhanh" top 10-20 ứng viên trong vài mili-giây, sau đó dùng Cross-Encoder để "đọc kỹ" và xếp hạng lại.

#### Lab 6: Question Rewriting bằng LLM (15 phút)

* **Chạy và Thử thách viết lại (15 phút):**
  Chạy file [lab6_question_rewriting.py](templates/lab6_question_rewriting.py):
  ```powershell
  python templates/lab6_question_rewriting.py
  ```

  *Quan sát:* Xem cách mô hình tự động chuyển câu hỏi *"Thế còn Hải Phòng thì được bao nhiêu?"* thành *"Mức phụ cấp lưu trú khi đi công tác tại Hải Phòng là bao nhiêu?"* nhờ đọc hiểu lịch sử hội thoại.

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Điều gì sẽ xảy ra với quy trình Vector Search nếu không có bước viết lại câu hỏi (Question Rewriting) khi học viên hỏi *"Thế còn Hải Phòng?"*?
> * **Gợi ý:** Vector search sẽ tìm kiếm ngữ nghĩa cho chính xác cụm từ *"Thế còn Hải Phòng?"*. Kết quả trả về sẽ là các tài liệu mô tả về địa danh Hải Phòng hoặc các đoạn không liên quan, chứ không thể tìm ra quy định phụ cấp công tác phí của Hải Phòng vì câu hỏi bị thiếu hoàn toàn chủ ngữ và ngữ cảnh.

---

### Phần 5: Xây dựng RAG hoàn chỉnh (60 phút)

#### Lab 7: Quy trình nạp tri thức - Ingestion Pipeline & ChromaDB (20 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ THỦ THƯ XẾP SÁCH):**
> Quy trình nạp tri thức giống như cách người thủ thư sắp xếp sách vào thư viện: cắt nhỏ sách thành đoạn ngắn để dễ tìm (Chunking), dán nhãn tên file (Metadata), quét mã số tọa độ ý nghĩa (Embedding) và xếp vào database (ChromaDB).

* **Thực hiện và Thử thách nạp tri thức mới (20 phút):**
  Chạy file [lab7_ingestion_chromadb.py](templates/lab7_ingestion_chromadb.py):
  ```powershell
  python templates/lab7_ingestion_chromadb.py
  ```

  *Thực hiện thử thách:*1. Vào thư mục `synthetic-data/hr-policies/`. Tạo một file mới bằng text editor đặt tên là `policy-overtime.md`.
  2. **Dán toàn bộ nội dung chính sách làm thêm giờ có sẵn dưới đây vào file đó và lưu lại**:
     ```markdown
     ---
     doc_id: POL-OVERTIME-001
     title: Quy định làm thêm giờ và phụ cấp ngoài giờ
     version: v1.0
     effective_date: 2026-03-01
     owner: Ban Nhân sự
     access_level: public
     status: active
     ---
     # Quy định làm thêm giờ và phụ cấp ngoài giờ

     Cán bộ nhân viên làm việc ngoài giờ hành chính hoặc trong các ngày nghỉ lễ sẽ được hưởng phụ cấp làm thêm giờ bằng 300% mức lương ngày bình thường.
     ```
  3. Chạy lại file `lab7_ingestion_chromadb.py` trên terminal. Quan sát xem số lượng chunks đã tăng lên từ bao nhiêu thành bao nhiêu.

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Điều gì sẽ xảy ra nếu ta nạp dữ liệu chính sách mới vào ChromaDB nhưng lại quên gắn siêu dữ liệu (Metadata) cho từng đoạn?
> * **Gợi ý:** Nếu thiếu Metadata, khi hệ thống truy xuất được các đoạn văn bản (chunks) liên quan, nó sẽ không thể chỉ ra được đoạn đó trích từ file tài liệu nào (như `policy-hotel-limit.md` hay `policy-travel-allowance.md`). Điều này khiến trợ lý RAG không thể thực hiện trích nguồn dẫn chứng hợp lệ, làm giảm uy tín của câu trả lời.

#### Lab 8: Quy trình truy vấn - Query Pipeline & LLM Generation (40 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ KỲ THI MỞ SÁCH - OPEN-BOOK EXAM):**
> RAG giải quyết hiện tượng ảo giác bằng cách tổ chức kỳ thi mở sách cho LLM: RAG tìm 2 trang tài liệu liên quan nhất rồi đưa cho LLM và ra lệnh: *"Chỉ trả lời dựa vào đây, cấm tự ý bịa đặt."*

* **Bước 1: Chạy thử nghiệm hệ thống (10 phút)**
  Chạy file [lab8_rag_pipeline.py](templates/lab8_rag_pipeline.py):
  ```powershell
  python templates/lab8_rag_pipeline.py
  ```

  *Quan sát:*- Ca test 1: Trả lời đúng mức trần khách sạn cho chuyên viên đi Hải Phòng (700k/đêm) dựa vào file `policy-hotel-limit.md`.
  - Ca test 3: Câu hỏi bẫy về Singapore (thông tin không có trong tài liệu). Trợ lý RAG cơ bản vẫn cố tìm các đoạn tài liệu tương tự (về đi lại trong nước) đưa vào context khiến LLM bị lừa và trả lời sai lệch (ảo giác).
* **Bước 2: Thực hiện Thử thách 5 - Khắc phục ảo giác (20 phút)**
  Mở file `templates/lab8_rag_pipeline.py`. Tìm biến `prompt` ở dòng 95. Hãy **thay đổi toàn bộ prompt hệ thống bằng đoạn mã có sẵn dưới đây** để thắt chặt quy luật phòng vệ, bắt LLM phải từ chối khi thiếu thông tin:
  ```python
  prompt = f"""Bạn là trợ lý giải đáp thắc mắc của phòng Tài chính VinaTel Network.
  ```

Nhiệm vụ của bạn là trả lời câu hỏi dựa HOÀN TOÀN vào NGỮ CẢNH được cung cấp dưới đây.

NGỮ CẢNH:
{context}

Yêu cầu nghiêm ngặt:

1. Chỉ trả lời các thông tin có bằng chứng trực tiếp từ NGỮ CẢNH trên.
2. Nếu câu hỏi yêu cầu thông tin về một địa điểm hoặc nội dung không hề xuất hiện trong NGỮ CẢNH (ví dụ: đi nước ngoài, đi Singapore), bạn KHÔNG được phỏng đoán hay áp dụng định mức trong nước để trả lời.
3. Trong trường hợp thiếu thông tin hoặc câu hỏi ngoài phạm vi ngữ cảnh, hãy trả lời chính xác câu sau và không thêm gì khác: "Kho tri thức hiện tại chưa có thông tin về nội dung này. Vui lòng liên hệ phòng Tài chính để được hỗ trợ."

CÂU HỎI: {clean_query}

CÂU TRẢ LỜI:"""
    ```
    Lưu file và chạy lại `python templates/lab8_rag_pipeline.py` trên terminal. Quan sát câu trả lời cho ca test đi Singapore. Có phải trợ lý đã từ chối an toàn thay vì bịa đặt số liệu hay không?

* **Bước 3: Thảo luận tổng kết Phần 5 (10 phút)**
  - Việc từ chối an toàn có lợi ích gì cho doanh nghiệp so với việc cố gắng trả lời?
  - RAG cơ bản còn những điểm yếu gì trước tấn công prompt injection hoặc tài liệu hết hiệu lực? (Chuẩn bị hành trang cho buổi học Agentic RAG).

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Tại sao một Prompt hệ thống (System Prompt) có quy tắc phòng vệ chặt chẽ lại quan trọng hơn việc chọn một mô hình ngôn ngữ lớn hơn để phòng chống ảo giác?
> * **Gợi ý:** Dù mô hình ngôn ngữ lớn đến đâu, nếu không được rào ranh giới nghiêm ngặt trong prompt, nó vẫn sẽ cố suy diễn và đoán mò dựa trên dữ liệu học máy chung để trả lời người dùng. Prompt phòng vệ chính là "lớp bảo vệ pháp lý" ép buộc mô hình phải từ chối khi thiếu bằng chứng thực tế trong ngữ cảnh được cung cấp.

---

### Phần 6: RAG nâng cao - Advanced RAG (50 phút)

#### Lab 9: Đánh giá chất lượng RAG bằng phương pháp RAG Triad (LLM-as-a-judge) (25 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ HỘI ĐỒNG GIÁM KHẢO ĐỘC LẬP):**
> Đánh giá RAG Triad giống như việc bạn mời một **hội đồng gồm 3 vị giám khảo độc lập** đến chấm điểm bài thi mở sách của trợ lý AI:
>
> 1. **Giám khảo 1 (chấm Context Relevance):** Kiểm tra xem trang sách mà thủ thư tìm ra có thực sự chứa nội dung câu hỏi yêu cầu không.
> 2. **Giám khảo 2 (chấm Groundedness):** So sánh câu trả lời của trợ lý với trang sách mở ra để xem trợ lý có tự bịa thêm thông tin nào không (ảo giác).
> 3. **Giám khảo 3 (chấm Answer Relevance):** Đọc câu hỏi và câu trả lời của trợ lý để xem trợ lý có trả lời đi thẳng vào trọng tâm câu hỏi hay nói vòng vo, lạc đề.

* **Bước 1: Chạy mã nguồn mẫu (10 phút)**
  Chạy file [lab9_evaluation.py](templates/lab9_evaluation.py):

  ```powershell
  python templates/lab9_evaluation.py
  ```

  *Quan sát:* Nhìn vào kết quả chấm điểm của 3 ca kiểm thử in ra trên terminal.

  - Ca 1 (Lý tưởng) đạt điểm bao nhiêu?
  - Ca 2 (Bị ảo giác đi Singapore) bị kéo tụt điểm Groundedness xuống bao nhiêu?
  - Ca 3 (Truy xuất sai ngữ cảnh xăng xe thay vì tiền phòng) bị kéo tụt điểm Context Relevance xuống bao nhiêu?
* **Bước 2: Thực hiện Thử thách 6 (10 phút)**
  Mở file `templates/lab9_evaluation.py`. Tìm ca đánh giá thứ 2 (dòng 142) và quan sát câu trả lời bị ảo giác: `"Có, khi anh/chị đi công tác tại Singapore, anh/chị sẽ được thanh toán tiền taxi tối đa là 500.000 VNĐ/ngày..."`.

  Hãy **thay thế câu trả lời bị ảo giác này bằng câu trả lời từ chối an toàn** đã được học ở Lab 8:

  ```python
  case_hallucination_response = "Kho tri thức hiện tại chưa có thông tin về nội dung này. Vui lòng liên hệ phòng Tài chính để được hỗ trợ."
  ```

  Lưu file và chạy lại trên terminal. Quan sát điểm số Groundedness và Answer Relevance của Ca 2 thay đổi như thế nào. Giải thích tại sao điểm Groundedness lúc này lại tăng vọt lên 5/5.
* **Bước 3: Thảo luận nhóm (5 phút)**
  Tại sao phương pháp sử dụng LLM làm giám khảo (LLM-as-a-judge) lại cực kỳ hữu ích cho doanh nghiệp khi cần đánh giá tự động hàng ngàn cuộc hội thoại của khách hàng với trợ lý AI?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Trong 3 tiêu chí của RAG Triad (Context Relevance, Groundedness, Answer Relevance), tiêu chí nào trực tiếp giúp phát hiện và ngăn chặn hiện tượng trợ lý AI tự bịa đặt thông tin (ảo giác)?
> * **Gợi ý:** Tiêu chí **Groundedness (Tính xác thực / Đỡ ảo giác)**. Tiêu chí này so sánh câu trả lời của AI với ngữ cảnh được cung cấp. Nếu câu trả lời chứa thông tin không có trong ngữ cảnh, điểm số sẽ bị kéo tụt xuống, giúp quản trị viên phát hiện lỗi lập tức.

#### Lab 10: Chuẩn đoán và xử lý các lỗi kỹ thuật kinh điển trong RAG (15 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ BẮT BỆNH HỆ THỐNG):**
> Xây dựng hệ thống RAG giống như lắp ráp một chiếc xe máy. Nếu bạn đổ sai nhiên liệu (sai mã hóa đọc file), chỉnh xích quá căng (chunk size quá nhỏ làm đứt đoạn ý nghĩa), hoặc hết xăng giữa đường (lỗi cạn hạn ngạch API/mất mạng), xe sẽ không chạy được.

* **Bước 1: Chạy mã nguồn mô phỏng lỗi (5 phút)**
  Chạy file [lab10_troubleshooting.py](templates/lab10_troubleshooting.py):
  ```powershell
  python templates/lab10_troubleshooting.py
  ```

  *Quan sát:* Đọc kỹ 3 lỗi in ra trên terminal:- **Lỗi 1 (Mã hóa):** Hiển thị những ký tự tiếng Việt bị lỗi kỳ lạ (Mojibake) hoặc báo lỗi chương trình bị dừng.
  - **Lỗi 2 (Phân đoạn):** Thấy rõ việc cắt nhỏ 15 ký tự làm số tiền `1.500.000 VNĐ` bị cắt đôi thành 2 đoạn độc lập, không còn ý nghĩa.
  - **Lỗi 3 (API/Mạng):** Bắt ngoại lệ báo lỗi kết nối hoặc sai khóa API Key.
* **Bước 2: Thực hiện Thử thách 7 (5 phút)**
  Hãy mở file `templates/lab10_troubleshooting.py`. Tìm phần mô phỏng lỗi API (dòng 68). Đổi biến `fake_api_key` thành khóa API thực tế lấy từ `.env`:
  ```python
  # Sửa dòng này để dùng API key đúng
  fake_api_key = os.getenv("GEMINI_API_KEY")
  ```

  Lưu file và chạy lại. Đảm bảo chương trình gọi API thành công và in ra lời chào tiếng Việt bình thường.
* **Bước 3: Thảo luận nhanh (5 phút)**
  Khi thiết kế ứng dụng RAG thực tế cho nhân viên công ty sử dụng, lập trình viên cần xử lý ngoại lệ (`try-except`) như thế nào để hệ thống không bị sập hoàn toàn khi mạng internet bị chập chờn?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Làm thế nào giảng viên giúp học viên phát hiện nhanh lỗi Unicode cp1252 trên Windows mà không cần chạy toàn bộ ứng dụng RAG?
> * **Gợi ý:** Chỉ cần mở đọc thử một dòng của file chính sách có tiếng Việt mà không truyền tham số `encoding='utf-8'`. Windows sẽ ném ra lỗi `UnicodeDecodeError` hoặc in ra các ký tự Mojibake lỗi, từ đó giúp học viên hiểu sự cần thiết của encoding.

#### Lab 11: So sánh hiệu năng Local vs Cloud Embedding (10 phút)

> [!NOTE]
> **DIỄN GIẢI TRỰC QUAN (ẨN DỤ XE MÁY VS MÁY BAY):**
>
> - **Mô hình Local giống như chiếc xe máy cá nhân:** Bạn có thể đi bất cứ lúc nào (offline), không cần xin phép/mua vé, hoàn toàn miễn phí hành trình, cực kỳ cơ động và nhanh chóng cho quãng đường ngắn. Nhưng nó chở được rất ít đồ (số chiều nhỏ - 384 chiều, hiểu ngữ nghĩa đơn giản).
> - **Mô hình Cloud giống như chiếc máy bay:** Chở được khối lượng đồ khổng lồ (số chiều lớn - 768 chiều, hiểu sâu sắc nhiều sắc thái ngôn ngữ). Nhưng bạn phải mua vé (tốn phí API), phụ thuộc vào lịch bay và thời tiết (đường truyền mạng internet, độ trễ kết nối).

* **Bước 1: Chạy mã nguồn đo đạc (5 phút)**
  Chạy file [lab11_benchmarking.py](templates/lab11_benchmarking.py):
  ```powershell
  python templates/lab11_benchmarking.py
  ```

  *Quan sát:* Nhìn vào bảng kết quả so sánh (Benchmark Table) hiển thị trên terminal. Ghi lại:- Tổng thời gian xử lý của Local và Cloud khác nhau bao nhiêu lần?
  - Số chiều vector (Dimension) của Local và Cloud lệch nhau thế nào?
* **Bước 2: Thử thách 8 và Thảo luận tổng kết toàn buổi học (5 phút)**
  Dựa trên bảng so sánh vừa chạy:
  - Nếu bạn cần xây dựng một ứng dụng RAG tra cứu văn bản pháp luật vô cùng phức tạp cho ban Giám đốc, cần độ chính xác ngữ nghĩa tuyệt đối, bạn sẽ chọn giải pháp nào?
  - Nếu bạn cần xây dựng một ứng dụng RAG chạy trên điện thoại di động của nhân viên kỹ thuật đi hiện trường (nơi sóng 3G/4G chập chờn), bạn sẽ chọn mô hình Local hay Cloud Embedding? Tại sao?

> [!TIP]
> **CÂU HỎI TƯƠNG TÁC DÀNH CHO GIẢNG VIÊN (INSTRUCTOR CHECKPOINT):**
>
> * **Hỏi:** Tại sao Local Embedding mặc dù chạy hoàn toàn offline trên CPU máy tính cá nhân thô sơ vẫn cho thời gian phản hồi (latency) cực kỳ nhanh so với Cloud Embedding (chỉ khoảng 0.03 giây/câu)?
> * **Gợi ý:** Vì mô hình local MiniLM cực kỳ nhẹ (chỉ khoảng vài chục triệu tham số), và quan trọng nhất là nó không tốn thời gian truyền dữ liệu qua mạng internet (network round-trip time) cũng như thời gian xếp hàng chờ đợi trên máy chủ đám mây.

---

### Thảo luận tổng kết cuối buổi học (10 phút)

Học viên và giảng viên cùng thảo luận 3 câu hỏi lớn:

1. RAG cơ bản giúp chúng ta kiểm soát câu trả lời của mô hình ngôn ngữ lớn (LLM) tốt hơn so với việc hỏi trực tiếp LLM như thế nào?
2. Tại sao việc chia nhỏ tài liệu (Chunking) và chọn kích thước chunk phù hợp lại quyết định trực tiếp đến sự thành bại của Vector Search?
3. Tại sao trong môi trường doanh nghiệp thực tế, việc thiết lập các prompt phòng vệ chống ảo giác (giống như Lab 8 và Lab 9) lại quan trọng hơn việc bắt mô hình phải trả lời bằng mọi giá?
