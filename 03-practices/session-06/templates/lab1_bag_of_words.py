# -*- coding: utf-8 -*-
"""
lab1_bag_of_words.py
Thực hành: Biểu diễn văn bản dưới dạng Vector đếm từ (Bag-of-Words)
"""

print("--- LAB 1: BIỂU DIỄN VECTOR BAG-OF-WORDS ---")

# 1. Định nghĩa các câu mẫu liên quan đến công tác phí
documents = [
    "Tôi muốn tạm ứng tiền đi công tác",
    "Quy trình tạm ứng công tác phí của công ty",
    "Tôi muốn mua máy tính mới cho phòng họp"
]

# 2. Xây dựng từ điển (Vocabulary) chứa toàn bộ các từ duy nhất
vocab = set()
for doc in documents:
    # Chuyển về chữ thường và tách từ theo khoảng trắng
    words = doc.lower().split()
    vocab.update(words)

# Chuyển set thành danh sách đã sắp xếp để cố định chỉ số (index)
vocab_list = sorted(list(vocab))

print("\nTừ điển (Vocabulary):")
print(vocab_list)
print(f"Tổng số từ trong từ điển: {len(vocab_list)} từ")

# 3. Chuyển đổi các câu văn bản thành vector đếm từ
vectors = []
for doc in documents:
    words = doc.lower().split()
    # Khởi tạo vector toàn số 0 có độ dài bằng từ điển
    vector = [0] * len(vocab_list)
    for word in words:
        if word in vocab_list:
            idx = vocab_list.index(word)
            vector[idx] += 1
    vectors.append(vector)

# 4. In kết quả biểu diễn số hóa của mỗi câu
print("\nKết quả số hóa các câu thành Vector:")
for i, doc in enumerate(documents):
    print(f"\nCâu: \"{doc}\"")
    print(f"Vector: {vectors[i]}")

print("\n--- KẾT THÚC LAB 1 ---")
