# -*- coding: utf-8 -*-
"""
lab2_sentence_embedding.py
Thực hành: Trích xuất đặc trưng câu (Sentence Embedding) dùng mô hình pre-trained
"""

import sys

print("--- LAB 2: TRÍCH XUẤT SENTENCE EMBEDDING ---")

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Lỗi: Thư viện 'sentence-transformers' chưa được cài đặt!")
    print("Vui lòng chạy lệnh sau trên terminal để cài đặt:")
    print("pip install sentence-transformers")
    sys.exit(1)

# 1. Tải mô hình embedding
model_name = 'all-MiniLM-L6-v2'
print(f"\nĐang tải mô hình embedding '{model_name}' (Vui lòng chờ)...")
model = SentenceTransformer(model_name)
print("Đã tải mô hình thành công!")

# 2. Định nghĩa các câu cần trích xuất vector ngữ nghĩa
sentences = [
    "Tôi muốn tạm ứng tiền đi công tác",
    "Quy trình tạm ứng công tác phí của công ty",
    "Tôi muốn mua máy tính mới cho phòng họp",
    "Thủ tục xin ứng trước công tác phí như thế nào"
]

# 3. Tiến hành trích xuất vector embedding
print("\nĐang sinh embedding cho các câu mẫu...")
embeddings = model.encode(sentences)

# 4. In thông tin kích thước và giá trị số thực của vector
for i, sentence in enumerate(sentences):
    print(f"\nCâu: \"{sentence}\"")
    print(f"Kích thước Vector (Số chiều): {embeddings[i].shape}")
    print(f"5 giá trị số thực đầu tiên: {embeddings[i][:]}...")

print("\n--- KẾT THÚC LAB 2 ---")
