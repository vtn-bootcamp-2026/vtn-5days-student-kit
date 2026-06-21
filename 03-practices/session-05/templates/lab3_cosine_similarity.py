# -*- coding: utf-8 -*-
"""
lab3_cosine_similarity.py
Thực hành: Tính toán độ tương đồng Cosine (Cosine Similarity) đo khoảng cách ngữ nghĩa
"""

import sys
import numpy as np

print("--- LAB 3: TÍNH TOÁN ĐỘ TƯƠNG ĐỒNG COSINE ---")

# Định nghĩa hàm tính toán cosine similarity sử dụng numpy
def calculate_cosine_similarity(v1, v2):
    """
    Tính độ tương đồng cosine giữa 2 vector.
    Công thức: (A . B) / (||A|| * ||B||)
    """
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(dot_product / (norm_v1 * norm_v2))

# Đảm bảo đã cài sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Lỗi: Hãy chạy cài đặt sentence-transformers trước!")
    sys.exit(1)

# 1. Tải model và sinh embedding
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

sentences = [
    "Tôi muốn tạm ứng tiền đi công tác",
    "Quy trình tạm ứng công tác phí của công ty",
    "Tôi muốn mua máy tính mới cho phòng họp",
    "Thủ tục xin ứng trước công tác phí như thế nào"
]

print("\nĐang sinh vector embedding...")
embeddings = model.encode(sentences)

# 2. Tính toán độ tương đồng giữa câu 0 ("Tôi muốn tạm ứng tiền đi công tác") và các câu khác
print("\nTính toán độ tương đồng ngữ nghĩa:")
sim_0_1 = calculate_cosine_similarity(embeddings[0], embeddings[1])
sim_0_2 = calculate_cosine_similarity(embeddings[0], embeddings[2])
sim_0_3 = calculate_cosine_similarity(embeddings[0], embeddings[3])

print(f"\nCâu gốc: \"{sentences[0]}\"")
print(f" -> So với: \"{sentences[1]}\"")
print(f"    Độ tương đồng Cosine: {sim_0_1:.4f} (Độ tương đồng cao, cùng chủ đề tạm ứng)")

print(f"\n -> So với: \"{sentences[3]}\"")
print(f"    Độ tương đồng Cosine: {sim_0_3:.4f} (Độ tương đồng rất cao, do đồng nghĩa mặc dù khác từ chữ)")

print(f"\n -> So với: \"{sentences[2]}\"")
print(f"    Độ tương đồng Cosine: {sim_0_2:.4f} (Độ tương đồng thấp, khác chủ đề)")

print("\n--- KẾT THÚC LAB 3 ---")
