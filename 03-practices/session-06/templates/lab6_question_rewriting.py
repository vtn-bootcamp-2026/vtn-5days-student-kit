# -*- coding: utf-8 -*-
"""
lab6_question_rewriting.py
Thực hành: Viết lại câu hỏi (Question Rewriting) xử lý câu hỏi mơ hồ bằng LLM
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

print("--- LAB 6: THỰC HÀNH QUESTION REWRITING ---")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env hoặc biến môi trường!")
    print("Vui lòng lấy API Key từ https://aistudio.google.com và điền vào file .env")
    sys.exit(1)

genai.configure(api_key=api_key)

def rewrite_query(user_query, chat_history=""):
    """
    Sử dụng Gemini API để viết lại câu hỏi mơ hồ của người dùng dựa trên ngữ cảnh lịch sử chat.
    """
    prompt = f"""Bạn là bộ phận xử lý truy vấn thông minh của hệ thống RAG doanh nghiệp.
Nhiệm vụ của bạn là viết lại câu hỏi của người dùng để làm rõ ý nghĩa của các đại từ chỉ định hoặc từ ngữ mơ hồ (như "cái đó", "bao nhiêu", "ở đâu", "ai") dựa trên lịch sử hội thoại trước đó.
Mục tiêu là giúp hệ thống truy xuất tài liệu chính xác hơn.
Chỉ trả về duy nhất CÂU HỎI ĐÃ ĐƯỢC VIẾT LẠI rõ nghĩa, KHÔNG thêm bất kỳ bình luận hay từ giải thích nào khác.

Lịch sử hội thoại trước đó:
{chat_history}

Câu hỏi mơ hồ hiện tại của người dùng: {user_query}

Câu hỏi rõ nghĩa viết lại:"""
    
    model = genai.GenerativeModel("gemini-3.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Kịch bản 1: Mơ hồ về đối tượng và loại phụ cấp
history_1 = """Người dùng: Tôi muốn hỏi về mức phụ cấp lưu trú khi đi công tác Hà Nội.
Trợ lý: Theo chính sách, mức phụ cấp lưu trú tại Hà Nội (Vùng I) là 350.000 VNĐ/ngày."""
query_1 = "Thế còn Hải Phòng thì được bao nhiêu?"

print(f"\n--- Kịch bản 1 ---")
print(f"Lịch sử chat:\n{history_1}")
print(f"Câu hỏi mơ hồ: \"{query_1}\"")
rewritten_1 = rewrite_query(query_1, history_1)
print(f"-> Câu hỏi viết lại rõ nghĩa: \"{rewritten_1}\"")

# Kịch bản 2: Mơ hồ về đại từ chỉ định "cái này" và thời gian
history_2 = """Người dùng: Cho tôi hỏi về thời hạn nộp hồ sơ hoàn ứng công tác phí.
Trợ lý: Bạn cần nộp đầy đủ hồ sơ hoàn ứng trong vòng 7 ngày làm việc kể từ khi kết thúc chuyến công tác."""
query_2 = "Nếu nộp muộn cái này thì bị làm sao?"

print(f"\n--- Kịch bản 2 ---")
print(f"Lịch sử chat:\n{history_2}")
print(f"Câu hỏi mơ hồ: \"{query_2}\"")
rewritten_2 = rewrite_query(query_2, history_2)
print(f"-> Câu hỏi viết lại rõ nghĩa: \"{rewritten_2}\"")

print("\n--- KẾT THÚC LAB 6 ---")
