# -*- coding: utf-8 -*-
"""
lab5_reranking.py
Thực hành: Xếp hạng lại (Reranking) sử dụng Cross-Encoder để tối ưu kết quả
"""

import sys
import numpy as np

print("--- LAB 5: THỰC HÀNH RERANKING ---")

# 1. Định nghĩa cẩm nang công tác phí giả lập
documents = [
    "Quy định Vùng I gồm Hà Nội và TP Hồ Chí Minh hưởng phụ cấp lưu trú là 350.000 VNĐ một ngày.",
    "Quy định Vùng II gồm Đà Nẵng và Hải Phòng hưởng phụ cấp lưu trú là 300.000 VNĐ một ngày.",
    "Vé máy bay hạng thương gia Business Class chỉ dành cho cấp Giám đốc và Phó Giám đốc.",
    "Thời hạn nộp hồ sơ thanh toán hoàn ứng công tác phí là 7 ngày làm việc kể từ khi kết thúc chuyến đi."
]

try:
    from sentence_transformers import CrossEncoder, SentenceTransformer
except ImportError:
    print("Lỗi: Hãy cài đặt sentence-transformers!")
    sys.exit(1)

# Tải model Bi-Encoder (dùng để tìm kiếm nhanh) và Cross-Encoder (dùng để Rerank chính xác)
print("\nĐang tải mô hình Cross-Encoder (Vui lòng chờ)...")
# Sử dụng model cross-encoder siêu nhỏ, đa ngôn ngữ hoặc tương thích tiếng Việt tốt
reranker = CrossEncoder('BAAI/bge-reranker-base')
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Đã tải xong các mô hình!")

query = "Giám đốc đi máy bay được thanh toán thế nào"

# Bước 1: Chạy Vector search để lấy top-3 ứng viên thô
print("\nBước 1: Chạy Vector search thô...")
q_emb = model.encode(query)
d_embs = model.encode(documents)
vector_scores = [float(np.dot(q_emb, d_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(d_emb))) for d_emb in d_embs]

print("Kết quả điểm tương đồng Cosine:")
for i, score in enumerate(vector_scores):
    print(f" - Tài liệu {i+1}: {score:.4f}")

# Bước 2: Rerank top ứng viên bằng Cross-Encoder
print("\nBước 2: Chạy Cross-Encoder Reranking...")
pairs = [[query, doc] for doc in documents]
rerank_scores = reranker.predict(pairs)

print("Kết quả điểm Rerank (Cross-Encoder):")
for i, score in enumerate(rerank_scores):
    print(f" - Tài liệu {i+1}: {score:.4f}")

# Sắp xếp kết quả theo điểm Rerank
ranked_indices = np.argsort(rerank_scores)[::-1]
print("\nThứ tự tài liệu ưu tiên sau khi Rerank:")
for rank, idx in enumerate(ranked_indices):
    print(f" Hạng {rank+1}: Tài liệu {idx+1} (Điểm: {rerank_scores[idx]:.4f}) -> \"{documents[idx][:60]}...\"")

print("\n--- KẾT THÚC LAB 5 ---")
