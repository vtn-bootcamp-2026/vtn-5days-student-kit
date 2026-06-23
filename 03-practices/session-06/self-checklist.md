---
mo-ta: danh sách kiểm tra hoàn thành buổi thực hành RAG cơ bản: Basic RAG
trang-thai: active
phien-ban: v1.3
created-at: 2026-06-17 20:10 +07:00
updated-at: 2026-06-18 09:15 +07:00
---

# Danh sách kiểm tra hoàn thành bài thực hành RAG cơ bản (Basic RAG checklist)

Học viên sử dụng checklist này để tự đánh giá kết quả thực hành của nhóm sau buổi học.

## 1. Môi trường và thư viện

- [ ] Đã chạy lệnh cài đặt thành công các thư viện Python: `sentence-transformers`, `chromadb`, `google-generativeai`, `python-dotenv`, `numpy`.
- [ ] Đã tạo file `.env` chứa khóa `GEMINI_API_KEY` hợp lệ tại thư mục làm việc.

## 2. Các bài Lab cơ bản (Lab 1 - Lab 3)

- [ ] **Lab 1 (Bag-of-Words):** Chạy thành công file `lab1_bag_of_words.py` và in ra được vector đếm của 3 câu mẫu.
- [ ] **Lab 2 (Embedding):** Chạy thành công file `lab2_sentence_embedding.py` và in ra được kích thước vector 384 chiều của mô hình embedding.
- [ ] **Lab 3 (Cosine Similarity):** Chạy thành công file `lab3_cosine_similarity.py` và hiểu vì sao hai câu đồng nghĩa nhưng khác chữ vẫn có điểm tương đồng cao.

## 3. Các kỹ thuật tối ưu hóa RAG (Lab 4 - Lab 6)

- [ ] **Lab 4 (Hybrid Search):** Chạy thành công file `lab4_hybrid_search.py` kết hợp điểm Vector search và Keyword search.
- [ ] **Lab 5 (Reranking):** Chạy thành công file `lab5_reranking.py` sử dụng Cross-Encoder để xếp hạng lại độ liên quan của các chunks đối với câu hỏi.
- [ ] **Lab 6 (Question Rewriting):** Chạy thành công file `lab6_question_rewriting.py` gọi Gemini API viết lại các câu hỏi chứa đại từ chỉ định mơ hồ.

## 4. Quy trình RAG hoàn chỉnh (Lab 7 - Lab 8)

- [ ] **Lab 7 (Ingestion Pipeline):** Chạy thành công file `lab7_ingestion_chromadb.py` để phân mảnh 3 file tài liệu công tác phí và nạp vào database ChromaDB.
- [ ] **Lab 8 (Query Pipeline):** Chạy thành công file `lab8_rag_pipeline.py` tích hợp toàn trình, trả lời đúng định mức tiền phòng của Trưởng phòng/Chuyên viên đi công tác.
- [ ] **Phân tích ảo giác:** Chạy thử câu hỏi về công tác đi Singapore và quan sát, giải thích được hiện tượng ảo giác của luồng RAG cơ bản khi thiếu dữ liệu nguồn.

## 5. RAG nâng cao (Lab 9 - Lab 11)

- [ ] **Lab 9 (Evaluation - RAG Triad):** Chạy thành công file `lab9_evaluation.py` tự động chấm điểm 3 tiêu chí Context Relevance, Groundedness và Answer Relevance cho 3 ca RAG điển hình.
- [ ] **Lab 10 (Troubleshooting):** Chạy thành công file `lab10_troubleshooting.py` để quan sát, chuẩn đoán và hiểu rõ cách xử lý 3 lỗi kinh điển: lỗi UTF-8 trên Windows, lỗi phân đoạn quá nhỏ và lỗi cạn hạn mức API Quota.
- [ ] **Lab 11 (Benchmarking):** Chạy thành công file `lab11_benchmarking.py` so sánh kích thước vector và tốc độ thực thi (latency) giữa mô hình cục bộ (Local MiniLM) và mô hình đám mây (Cloud Gemini).
