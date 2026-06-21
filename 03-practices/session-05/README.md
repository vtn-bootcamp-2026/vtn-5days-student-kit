---
mo-ta: mục tiêu và đầu ra buổi thực hành RAG cơ bản: Basic RAG
trang-thai: active
phien-ban: v1.1
created-at: 2026-06-17 20:00 +07:00
updated-at: 2026-06-17 20:25 +07:00
---

# Thực hành: RAG cơ bản (Basic RAG)

Buổi học này giới thiệu về kiến trúc tìm kiếm tăng cường: retrieval-augmented generation (RAG) ở mức cơ bản: Basic RAG, giúp học viên hiểu rõ cách thức hoạt động từ tìm kiếm từ khóa truyền thống đến tìm kiếm theo ngữ nghĩa: semantic search và tích hợp mô hình ngôn ngữ lớn để trả lời dựa trên tài liệu.

## 1. Mục tiêu buổi thực hành

Hoàn thành buổi thực hành này, học viên sẽ:

- **Hiểu rõ hạn chế của tìm kiếm từ khóa:** Nhận diện sự khác biệt giữa tìm kiếm từ khóa: keyword search và tìm kiếm ngữ nghĩa dùng vector.
- **Xây dựng quy trình nạp tri thức: Ingestion pipeline:** Tự viết script chia nhỏ tài liệu: chunking, tạo vector đại diện: embedding bằng mô hình ngôn ngữ và nạp vào cơ sở dữ liệu vector: vector database (ChromaDB).
- **Xây dựng quy trình truy vấn: Query pipeline:** Thực hiện tìm kiếm vector: vector search, kết hợp ngữ cảnh: context building và gọi mô hình ngôn ngữ lớn: LLM (Gemini API) để sinh câu trả lời có căn cứ.
- **Đánh giá và phản tư:** Thử nghiệm với các câu hỏi thực tế để nhận diện hiện tượng ảo giác: hallucination và trích dẫn giả của mô hình khi chưa được kiểm soát.

## 2. Tài nguyên học tập

- **Slide bài giảng lý thuyết:** [rag-basic.pdf](../../../01-slides/rag-basic.pdf)
- **Hướng dẫn thực hành chi tiết:** [lab.md](lab.md)
- **Danh sách kiểm tra hoàn thành:** [self-checklist.md](self-checklist.md)
- **Kho tri thức thực hành:** Tài liệu quy định công tác phí mô phỏng trong thư mục [synthetic-data/hr-policies/](synthetic-data/hr-policies/).
- **Mã nguồn mẫu:** Các file script mẫu trong thư mục [templates/](templates/).

## 3. Bản đồ thời gian buổi học (4 giờ)

| Phần | Thời lượng | Hoạt động | Sản phẩm cần đạt |
| --- | --- | --- | --- |
| **Phần 1** | 30 phút | Lý thuyết tổng quan từ slide | Nắm vững lý thuyết 6 module trong slide |
| **Phần 2** | 60 phút | Lab 1: Biểu diễn Vector Bag-of-Words<br>Lab 2: Trích xuất Sentence Embedding | Chuyển đổi thành công câu thành vector đếm từ và vector embedding |
| **Phần 3** | 40 phút | Lab 3: Tính toán Cosine Similarity | Code công thức cosine và vẽ biểu đồ ma trận tương đồng |
| **Phần 4** | 50 phút | Lab 4: Hybrid Search<br>Lab 5: Reranking<br>Lab 6: Question Rewriting | Hiểu và chạy thử 3 cơ chế tối ưu tìm kiếm và xử lý câu hỏi |
| **Phần 5** | 60 phút | Lab 7: Ingestion pipeline<br>Lab 8: Query pipeline | Script truy vấn và gọi LLM sinh câu trả lời có căn cứ |
