# -*- coding: utf-8 -*-
"""
lab7_ingestion_chromadb.py
Thực hành: Quy trình nạp tri thức (Ingestion Pipeline) & cơ sở dữ liệu vector ChromaDB
"""

import os
import re
import sys
from sentence_transformers import SentenceTransformer

print("--- LAB 7: INGESTION PIPELINE & CHROMADB ---")

# Đảm bảo ChromaDB đã được cài đặt
try:
    import chromadb
except ImportError:
    print("Lỗi: Hãy cài đặt chromadb bằng lệnh: pip install chromadb")
    sys.exit(1)

# 1. Đọc và chia nhỏ tài liệu chính sách công tác phí mô phỏng
kb_dir = "../synthetic-data/hr-policies"
print(f"\n1. Đang quét thư mục tài liệu tri thức: {kb_dir}...")

if not os.path.exists(kb_dir):
    print(f"Lỗi: Thư mục {kb_dir} không tồn tại. Hãy chắc chắn bạn chạy đúng thư mục làm việc!")
    sys.exit(1)

chunks = []
metadatas = []
ids = []
chunk_count = 0

for filename in os.listdir(kb_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(kb_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Loại bỏ frontmatter YAML bằng Regex
            clean_content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
            
            # Tách nội dung thành các đoạn văn đơn giản dựa trên 2 dấu xuống dòng (\n\n)
            paragraphs = [p.strip() for p in clean_content.split("\n\n") if len(p.strip()) > 30]
            
            for i, p in enumerate(paragraphs):
                chunks.append(p)
                metadatas.append({
                    "source": filename,
                    "paragraph_idx": i
                })
                ids.append(f"{filename.replace('.md', '')}_chunk_{i}")
                chunk_count += 1

print(f" -> Đã đọc và phân mảnh thành công {chunk_count} đoạn văn (chunks) tri thức.")

# 2. Khởi tạo ChromaDB Client (Dạng In-Memory tạm thời để thực hành)
print("\n2. Đang khởi tạo cơ sở dữ liệu vector ChromaDB...")
chroma_client = chromadb.Client()

# Tải mô hình embedding
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Định nghĩa hàm sinh vector embedding tương thích với ChromaDB
class CustomEmbeddingFunction:
    def __call__(self, input):
        # Trả về danh sách các list float đại diện cho vector
        return [emb.tolist() for emb in model.encode(input)]

# Tạo collection và gán embedding function
collection = chroma_client.get_or_create_collection(
    name="vtn_travel_policies",
    embedding_function=CustomEmbeddingFunction()
)

# 3. Nạp tài liệu vào DB
print("\n3. Đang đẩy các chunks và sinh embedding lưu vào database...")
collection.add(
    documents=chunks,
    metadatas=metadatas,
    ids=ids
)
print(" -> Hoàn tất! Dữ liệu đã được lưu trữ thành công và sẵn sàng để truy vấn.")

# Thử truy vấn kiểm tra nhanh
test_query = "Hà Nội được phụ cấp ăn uống bao nhiêu"
print(f"\n[Test thử Vector Search] Câu hỏi: '{test_query}'")
results = collection.query(query_texts=[test_query], n_results=1)

print("\nKết quả truy xuất tốt nhất:")
print(f" ID: {results['ids'][0][0]}")
print(f" Nguồn: {results['metadatas'][0][0]['source']}")
print(f" Nội dung: \"{results['documents'][0][0]}\"")

print("\n--- KẾT THÚC LAB 7 ---")
