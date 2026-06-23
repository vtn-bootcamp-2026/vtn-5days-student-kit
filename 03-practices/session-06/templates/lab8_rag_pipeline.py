# -*- coding: utf-8 -*-
"""
lab8_rag_pipeline.py
Thực hành: Xây dựng hệ thống RAG hoàn chỉnh (End-to-End Pipeline) kết hợp mô hình sinh
"""

import os
import re
import sys
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, CrossEncoder
import chromadb

print("--- LAB 8: HỆ THỐNG RAG HOÀN CHỈNH (END-TO-END PIPELINE) ---")

# 1. Cấu hình Gemini API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CẢNH BÁO: Không tìm thấy GEMINI_API_KEY trong file .env!")
    print("Vui lòng lấy API Key và cập nhật vào file .env")
    sys.exit(1)

genai.configure(api_key=api_key)

# 2. Khởi tạo các mô hình & Database
print("\n[1/5] Đang khởi tạo các mô hình embedding, reranker và database...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
reranker = CrossEncoder('unicamp-dl/mt5-base-mmarco-v2')
chroma_client = chromadb.Client()

class CustomEmbeddingFunction:
    def __call__(self, input):
        return [emb.tolist() for emb in model.encode(input)]

collection = chroma_client.get_or_create_collection(
    name="vtn_travel_policies_final",
    embedding_function=CustomEmbeddingFunction()
)

# 3. Đọc dữ liệu tri thức chính sách công tác phí và nạp vào DB
kb_dir = "../synthetic-data/hr-policies"
chunks = []
metadatas = []
ids = []

for filename in os.listdir(kb_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(kb_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            clean_content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
            paragraphs = [p.strip() for p in clean_content.split("\n\n") if len(p.strip()) > 30]
            for i, p in enumerate(paragraphs):
                chunks.append(p)
                metadatas.append({"source": filename, "paragraph_idx": i})
                ids.append(f"{filename.replace('.md', '')}_{i}")

collection.add(documents=chunks, metadatas=metadatas, ids=ids)
print(f" -> Đã nạp thành công {len(chunks)} chunks tài liệu công tác phí.")

# 4. Hàm viết lại câu hỏi sử dụng LLM
def rewrite_query(user_query, chat_history=""):
    if not chat_history:
        return user_query
    prompt = f"""Hãy viết lại câu hỏi dưới đây của người dùng để làm rõ ý nghĩa các đại từ mơ hồ dựa trên lịch sử chat.
Chỉ trả về duy nhất câu hỏi đã được viết lại, không thêm lời giải thích nào khác.

Lịch sử chat:
{chat_history}

Câu hỏi: {user_query}

Câu hỏi viết lại:"""
    model_llm = genai.GenerativeModel("gemini-3.5-flash")
    response = model_llm.generate_content(prompt)
    return response.text.strip()

# 5. Hàm chạy toàn bộ quy trình RAG Pipeline
def run_rag_pipeline(user_query, chat_history=""):
    print(f"\n--- NHẬN TRUY VẤN: \"{user_query}\" ---")
    
    # Bước 1: Viết lại câu hỏi
    clean_query = rewrite_query(user_query, chat_history)
    if clean_query != user_query:
        print(f" -> [Rewriter] Câu hỏi đã được làm rõ thành: \"{clean_query}\"")
        
    # Bước 2: Truy xuất (Retrieval) thô - lấy top-4 kết quả
    print(" -> [Retriever] Đang thực hiện Vector Search lấy top-4 ứng viên...")
    results = collection.query(query_texts=[clean_query], n_results=4)
    retrieved_docs = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]
    
    # Bước 3: Xếp hạng lại (Reranking) - lấy top-2 kết quả tốt nhất
    print(" -> [Reranker] Đang chạy Cross-Encoder Reranking để chọn lọc top-2...")
    pairs = [[clean_query, doc] for doc in retrieved_docs]
    scores = reranker.predict(pairs)
    
    ranked_indices = np.argsort(scores)[::-1]
    final_docs = [retrieved_docs[idx] for idx in ranked_indices[:2]]
    final_metadatas = [retrieved_metadatas[idx] for idx in ranked_indices[:2]]
    
    print("\nChunks được chọn gửi vào ngữ cảnh:")
    for idx, doc in enumerate(final_docs):
         print(f"  + [{final_metadatas[idx]['source']}]: \"{doc[:80]}...\"")
         
    # Bước 4: Xây dựng Prompt ngữ cảnh (Context building)
    context = "\n\n".join([f"Tài liệu {m['source']}: {d}" for d, m in zip(final_docs, final_metadatas)])
    
    prompt = f"""Bạn là trợ lý giải đáp thắc mắc của phòng Tài chính VinaTel Network. 
Hãy trả lời câu hỏi của người dùng dưới đây bằng tiếng Việt, dựa HOÀN TOÀN vào NGỮ CẢNH được cung cấp.
Không phỏng đoán, không tự bịa đặt thông tin nằm ngoài ngữ cảnh.
Nếu thông tin trong ngữ cảnh không đủ để trả lời, hãy từ chối lịch sự và nói rõ là không có thông tin.

NGỮ CẢNH:
{context}

CÂU HỎI: {clean_query}

CÂU TRẢ LỜI:"""

    # Bước 5: Sinh câu trả lời (LLM Generation)
    print("\n -> [Generator] Đang gọi Gemini API để sinh câu trả lời...")
    model_llm = genai.GenerativeModel("gemini-3.5-flash")
    response = model_llm.generate_content(prompt)
    
    print("\n====== TRỢ LÝ PHẢN HỒI ======")
    print(response.text)
    print("=============================")

# --- CHẠY THỬ NGHIỆM HỆ THỐNG ---

# Ca kiểm thử 1: Câu hỏi trong phạm vi
run_rag_pipeline("Chuyên viên đi công tác Hải Phòng được thanh toán tiền khách sạn tối đa bao nhiêu")

# Ca kiểm thử 2: Câu hỏi mơ hồ cần làm rõ dựa trên hội thoại trước đó
history = """Người dùng: Tôi là Trưởng phòng tối ưu mạng đi công tác ở Hà Nội.
Trợ lý: Hạng vé máy bay tiêu chuẩn của Trưởng phòng là hạng Phổ thông (Economy)."""
run_rag_pipeline("Thế còn tiền phòng khách sạn của tôi là bao nhiêu?", history)

# Ca kiểm thử 3: Câu hỏi ngoài phạm vi (để kiểm tra hành vi từ chối và ảo giác)
run_rag_pipeline("Tôi đi công tác Singapore có được thanh toán tiền taxi không")

print("\n--- KẾT THÚC LAB 8 ---")
