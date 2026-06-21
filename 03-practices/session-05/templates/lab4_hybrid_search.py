# -*- coding: utf-8 -*-
"""
lab4_hybrid_search.py
Thực hành: Kết hợp Vector Search và Keyword Search (Hybrid Search)
"""

import numpy as np
from sentence_transformers import SentenceTransformer

print("--- LAB 4: THỰC HÀNH HYBRID SEARCH ---")

# 1. Định nghĩa cẩm nang công tác phí giả lập làm tri thức
documents = [
    "Quy định Vùng I gồm Hà Nội và TP Hồ Chí Minh hưởng phụ cấp lưu trú là 350.000 VNĐ một ngày.",
    "Quy định Vùng II gồm Đà Nẵng và Hải Phòng hưởng phụ cấp lưu trú là 300.000 VNĐ một ngày.",
    "Vé máy bay hạng thương gia Business Class chỉ dành cho cấp Giám đốc và Phó Giám đốc.",
    "Thời hạn nộp hồ sơ thanh toán hoàn ứng công tác phí là 7 ngày làm việc kể từ khi kết thúc chuyến đi."
]

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
doc_embeddings = model.encode(documents)

# Phép toán tính cosine similarity
def cosine_sim(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# 2. Hàm tìm kiếm từ khóa đơn giản (Jaccard similarity)
def keyword_search(query, docs):
    query_words = set(query.lower().split())
    scores = []
    for doc in docs:
        doc_words = set(doc.lower().split())
        intersection = query_words.intersection(doc_words)
        union = query_words.union(doc_words)
        score = len(intersection) / len(union) if len(union) > 0 else 0
        scores.append(score)
    return np.array(scores)

# 3. Hàm tìm kiếm ngữ nghĩa (Vector search)
def vector_search(query, doc_embs):
    q_emb = model.encode(query)
    scores = [cosine_sim(q_emb, d_emb) for d_emb in doc_embs]
    return np.array(scores)

# 4. Tìm kiếm lai (Hybrid Search)
def hybrid_search(query, docs, doc_embs, alpha=0.5):
    k_scores = keyword_search(query, docs)
    v_scores = vector_search(query, doc_embs)
    
    # Chuẩn hóa điểm về khoảng [0, 1] trước khi cộng
    k_min, k_max = k_scores.min(), k_scores.max()
    v_min, v_max = v_scores.min(), v_scores.max()
    
    k_norm = (k_scores - k_min) / (k_max - k_min + 1e-9) if k_max != k_min else k_scores
    v_norm = (v_scores - v_min) / (v_max - v_min + 1e-9) if v_max != v_min else v_scores
    
    # Cộng chéo có trọng số alpha
    hybrid_scores = alpha * v_norm + (1 - alpha) * k_norm
    return hybrid_scores, k_norm, v_norm

# Thử nghiệm truy vấn
query = "Hải Phòng được phụ cấp bao nhiêu"
h_scores, k_scores, v_scores = hybrid_search(query, documents, doc_embeddings, alpha=0.5)

print(f"\nCâu hỏi: \"{query}\"")
print("\nKết quả so sánh điểm số:")
for idx, doc in enumerate(documents):
    print(f"\nTài liệu {idx+1}: \"{doc[:50]}...\"")
    print(f" -> Điểm Keyword normalized: {k_scores[idx]:.4f}")
    print(f" -> Điểm Vector normalized: {v_scores[idx]:.4f}")
    print(f" -> Điểm Hybrid (alpha=0.5): {h_scores[idx]:.4f}")

print("\n--- KẾT THÚC LAB 4 ---")
