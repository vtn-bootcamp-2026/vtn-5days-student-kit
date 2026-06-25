---
mo-ta: Prompt yêu cầu Antigravity nâng cấp retriever.py lên cơ chế truy xuất lai (hybrid retrieval) vector + SQLite-FTS5 BM25 + RRF
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-25 07:15 +07:00
updated-at: 2026-06-25 07:15 +07:00
---

# Prompt 4: Hiện thực hóa truy xuất lai (Hybrid retrieval)

Sao chép toàn bộ nội dung trong khung dưới đây và gửi cho trợ lý ảo Antigravity:

```markdown
Chào Antigravity, tôi muốn thực hiện Lab A để nâng cấp bộ công cụ truy xuất của chúng tôi thành cơ chế truy xuất lai (truy xuất lai: hybrid retrieval) thực sự. Hãy giúp tôi chỉnh sửa và hoàn thiện tệp mã nguồn bộ truy xuất: retriever tại:
`outputs/skills/hr-policy-qa-skill/scripts/retriever.py`

Hãy thực hiện các yêu cầu sau:
1. Sao chép tệp mẫu `templates/skills/hr-policy-qa-skill/scripts/retriever.py` sang thư mục đích `outputs/skills/hr-policy-qa-skill/scripts/retriever.py` (nếu chưa có).
2. Viết thêm hàm xây dựng chỉ mục tìm kiếm từ khóa `build_fts_index(chunks, db_path="kb/fts5.db")` sử dụng tính năng bảng ảo FTS5 (bảng ảo FTS5: FTS5 virtual table) tích hợp sẵn của SQLite để đánh chỉ mục các trường `content`, `doc_id`, `section`, `chunk_id`. Hỗ trợ cơ chế dự phòng: fallback sử dụng thư viện `rank_bm25` (thuần Python) nếu môi trường không hỗ trợ extension FTS5 của SQLite.
3. Viết thêm hàm tìm kiếm từ khóa `bm25_search(conn_or_index, query, top_k=3)` trả về danh sách các chunk phù hợp nhất được chấm điểm bằng giải thuật BM25 của SQLite (hàm `bm25()`) hoặc `rank_bm25` và chuẩn hóa điểm số về khoảng [0, 1].
4. Viết thêm hàm trộn danh sách xếp hạng `rrf_fuse(vector_hits, bm25_hits, k=60, top_k=3)` áp dụng công thức ghép xếp hạng đảo chiều (ghép xếp hạng đảo chiều: Reciprocal Rank Fusion - RRF) để kết hợp kết quả tìm kiếm ngữ nghĩa (semantic search) từ ChromaDB và tìm kiếm từ khóa (keyword search) từ BM25 mà không cần chuẩn hóa điểm trực tiếp:
   `score(d) = Σ (1 / (k + rank_i(d)))`
5. Cập nhật hàm truy xuất chính `retrieve_chunks()` để thực hiện chạy song song cả tìm kiếm vector và tìm kiếm từ khóa BM25, sau đó áp dụng hàm `rrf_fuse` để chọn ra top-k chunk có điểm RRF cao nhất. Nếu cả hai phương pháp đều không trả về kết quả đạt yêu cầu, đánh dấu trường `refused: True` trong kết quả trả về.
6. Hiển thị phần code thay đổi dưới dạng khối mã khác biệt: diff block để tôi phê duyệt.
```
