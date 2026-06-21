# -*- coding: utf-8 -*-
"""
lab9_evaluation.py
Thực hành: Đánh giá chất lượng RAG bằng phương pháp RAG Triad (LLM-as-a-judge)
"""

import os
import sys
import re
import google.generativeai as genai
from dotenv import load_dotenv

print("--- LAB 9: ĐÁNH GIÁ RAG BẰNG PHƯƠNG PHÁP RAG TRIAD ---")

# 1. Cấu hình Gemini API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CẢNH BÁO: Không tìm thấy GEMINI_API_KEY trong file .env!")
    print("Vui lòng lấy API Key và cập nhật vào file .env")
    sys.exit(1)

genai.configure(api_key=api_key)
model_llm = genai.GenerativeModel("gemini-3.5-flash")

# 2. Định nghĩa các hàm đánh giá (LLM-as-a-judge)
def evaluate_metric(metric_name, prompt):
    try:
        response = model_llm.generate_content(prompt)
        text = response.text.strip()
        
        # Trích xuất điểm số (1-5) từ kết quả phản hồi của LLM
        score_match = re.search(r"Điểm:\s*([1-5])", text)
        score = int(score_match.group(1)) if score_match else "N/A"
        
        # Trích xuất lý do
        reason_match = re.search(r"Lý do:\s*(.*)", text, re.DOTALL)
        reason = reason_match.group(1).strip() if reason_match else text
        
        return score, reason
    except Exception as e:
        return "N/A", f"Lỗi gọi API: {str(e)}"

def evaluate_context_relevance(query, context):
    """
    1. Context Relevance: Đo lường xem Ngữ cảnh được truy xuất có liên quan đến Câu hỏi hay không.
    """
    prompt = f"""Bạn là một kiểm định viên hệ thống AI độc lập. Hãy đánh giá tiêu chí:
TIÊU CHÍ: Sự liên quan của Ngữ cảnh (Context Relevance)
Nhiệm vụ: Đánh giá xem thông tin trong "NGỮ CẢNH" được truy xuất có chứa thông tin hữu ích và liên quan trực tiếp để trả lời "CÂU HỎI" hay không.

Thang điểm từ 1 đến 5:
- 1: Hoàn toàn không liên quan, không có từ khóa hay ý nghĩa nào giúp ích.
- 3: Có liên quan một phần, chứa một số thông tin hữu ích nhưng thiếu nhiều chi tiết quan trọng.
- 5: Hoàn toàn liên quan, chứa đầy đủ thông tin để trả lời câu hỏi một cách trọn vẹn.

CÂU HỎI: {query}
NGỮ CẢNH: {context}

Hãy trả về phản hồi chính xác theo cấu trúc sau (không viết thêm gì khác):
Điểm: [Điểm số từ 1 đến 5]
Lý do: [Viết 1-2 câu giải thích ngắn gọn bằng tiếng Việt]"""
    return evaluate_metric("Context Relevance", prompt)

def evaluate_groundedness(context, response):
    """
    2. Groundedness (Faithfulness): Đo lường xem Câu trả lời có hoàn toàn dựa vào Ngữ cảnh hay không (Tránh ảo giác).
    """
    prompt = f"""Bạn là một kiểm định viên hệ thống AI độc lập. Hãy đánh giá tiêu chí:
TIÊU CHÍ: Tính xác thực / Không ảo giác (Groundedness / Faithfulness)
Nhiệm vụ: Đánh giá xem mọi thông tin khẳng định trong "CÂU TRẢ LỜI" có được suy ra hoặc trực tiếp hỗ trợ bởi "NGỮ CẢNH" hay không.

Thang điểm từ 1 đến 5:
- 1: Hoàn toàn ảo giác. Câu trả lời đưa ra thông tin không hề có trong ngữ cảnh hoặc mâu thuẫn hoàn toàn.
- 3: Bị ảo giác một phần. Câu trả lời có dựa vào ngữ cảnh nhưng tự thêm thắt một số thông tin quan trọng mà ngữ cảnh không nói tới.
- 5: Hoàn toàn xác thực. 100% thông tin trong câu trả lời đều có thể tìm thấy chứng cứ rõ ràng trong ngữ cảnh.

NGỮ CẢNH: {context}
CÂU TRẢ LỜI: {response}

Hãy trả về phản hồi chính xác theo cấu trúc sau (không viết thêm gì khác):
Điểm: [Điểm số từ 1 đến 5]
Lý do: [Viết 1-2 câu giải thích ngắn gọn bằng tiếng Việt]"""
    return evaluate_metric("Groundedness", prompt)

def evaluate_answer_relevance(query, response):
    """
    3. Answer Relevance: Đo lường xem Câu trả lời có giải quyết trực tiếp Câu hỏi hay không.
    """
    prompt = f"""Bạn là một kiểm định viên hệ thống AI độc lập. Hãy đánh giá tiêu chí:
TIÊU CHÍ: Sự liên quan của Câu trả lời (Answer Relevance)
Nhiệm vụ: Đánh giá xem "CÂU TRẢ LỜI" có đi thẳng vào trọng tâm và giải quyết được "CÂU HỎI" của người dùng hay không (không xét đến tính đúng sai của thông tin, chỉ xét độ khớp mục tiêu của câu hỏi).

Thang điểm từ 1 đến 5:
- 1: Lạc đề hoàn toàn. Trả lời một chủ đề khác không liên quan đến câu hỏi.
- 3: Trả lời đúng một phần, hoặc nói vòng vo dài dòng nhưng cuối cùng chưa giải quyết triệt để câu hỏi.
- 5: Trực tiếp, rõ ràng, giải quyết hoàn chỉnh 100% mục tiêu của câu hỏi.

CÂU HỎI: {query}
CÂU TRẢ LỜI: {response}

Hãy trả về phản hồi chính xác theo cấu trúc sau (không viết thêm gì khác):
Điểm: [Điểm số từ 1 đến 5]
Lý do: [Viết 1-2 câu giải thích ngắn gọn bằng tiếng Việt]"""
    return evaluate_metric("Answer Relevance", prompt)

# 3. Hàm in báo cáo RAG Triad trực quan
def report_rag_triad(case_name, query, context, response):
    print(f"\n=========================================")
    print(f" CA ĐÁNH GIÁ: {case_name}")
    print(f"=========================================")
    print(f"• Câu hỏi: \"{query}\"")
    print(f"• Ngữ cảnh: \"{context[:120]}...\"")
    print(f"• Câu trả lời: \"{response[:120]}...\"")
    print("\n--- ĐANG CHẤM ĐIỂM BẰNG LLM-AS-A-JUDGE (RAG TRIAD) ---")
    
    c_rel_score, c_rel_reason = evaluate_context_relevance(query, context)
    g_score, g_reason = evaluate_groundedness(context, response)
    a_rel_score, a_rel_reason = evaluate_answer_relevance(query, response)
    
    print(f"\n[1] CONTEXT RELEVANCE (Sự liên quan ngữ cảnh) : {c_rel_score}/5")
    print(f"    ↳ Lý do: {c_rel_reason}")
    print(f"[2] GROUNDEDNESS (Tính xác thực / Đỡ ảo giác)  : {g_score}/5")
    print(f"    ↳ Lý do: {g_reason}")
    print(f"[3] ANSWER RELEVANCE (Sự liên quan câu trả lời): {a_rel_score}/5")
    print(f"    ↳ Lý do: {a_rel_reason}")
    
    # Tính điểm trung bình RAG Triad
    try:
        avg_score = (float(c_rel_score) + float(g_score) + float(a_rel_score)) / 3
        print(f"\n=> ĐIỂM TRUNG BÌNH RAG TRIAD: {avg_score:.2f}/5.00")
        if avg_score >= 4.0:
            print("🌟 ĐÁNH GIÁ CHUNG: ĐẠT TIÊU CHUẨN CHẤT LƯỢNG CAO!")
        elif avg_score >= 2.5:
            print("⚠️ ĐÁNH GIÁ CHUNG: CẦN CẢI THIỆN (Có lỗi nhẹ hoặc thông tin chưa tối ưu)")
        else:
            print("❌ ĐÁNH GIÁ CHUNG: KHÔNG ĐẠT (Bị ảo giác nghiêm trọng hoặc lạc đề)")
    except:
         print("\n=> ĐIỂM TRUNG BÌNH RAG TRIAD: Không thể tính toán do có lỗi chấm điểm.")

# --- CHẠY THỬ CÁC CA ĐIỂN HÌNH ---

# Ca 1: Luồng RAG Lý tưởng (Đầy đủ thông tin, không ảo giác, trả lời đúng)
case_ideal_query = "Tôi là Chuyên viên đi công tác Hải Phòng thì tiền phòng tối đa là bao nhiêu?"
case_ideal_context = "Tài liệu policy-hotel-limit.md: Chức danh Chuyên viên/Nhân viên đi công tác tại các Thành phố trực thuộc Trung ương (như Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng, Cần Thơ) có định mức phòng khách sạn tối đa là 1.000.000 VNĐ/ngày."
case_ideal_response = "Chào anh/chị, theo quy định về định mức khách sạn, đối với chức danh Chuyên viên đi công tác tại Hải Phòng (là thành phố trực thuộc Trung ương), mức thanh toán tiền khách sạn tối đa là 1.000.000 VNĐ/ngày."

report_rag_triad("1. Ca RAG Lý Tưởng", case_ideal_query, case_ideal_context, case_ideal_response)

# Ca 2: Luồng RAG bị Ảo giác (Groundedness kém - Do LLM tự bịa thông tin đi Singapore)
case_hallucination_query = "Tôi đi công tác Singapore có được thanh toán tiền taxi không?"
case_hallucination_context = "Tài liệu policy-travel-allowance.md: Phụ cấp đi lại nội bộ vùng chỉ áp dụng khi cán bộ nhân viên di chuyển công tác trong lãnh thổ Việt Nam. Quy định này không đề cập đến định mức công tác nước ngoài."
# Câu trả lời bịa đặt thêm định mức 500.000 VNĐ tại Singapore
case_hallucination_response = "Có, khi anh/chị đi công tác tại Singapore, anh/chị sẽ được thanh toán tiền taxi tối đa là 500.000 VNĐ/ngày dựa trên hóa đơn thực tế."

report_rag_triad("2. Ca RAG Bị Ảo Giác (Lỗi Groundedness)", case_hallucination_query, case_hallucination_context, case_hallucination_response)

# Ca 3: Luồng RAG bị Truy xuất sai ngữ cảnh (Context Relevance kém)
case_wrong_retrieval_query = "Trưởng phòng đi công tác tại Hà Nội được phụ cấp tiền phòng bao nhiêu?"
# Hệ thống truy xuất sai thông tin về phụ cấp đi lại bằng xe máy thay vì tiền phòng khách sạn
case_wrong_retrieval_context = "Tài liệu policy-travel-allowance.md: Trường hợp cán bộ nhân viên sử dụng phương tiện cá nhân (xe máy) đi công tác sẽ được thanh toán phụ cấp xăng xe với mức 3.000 VNĐ/km dựa trên số km thực tế và phê duyệt của quản lý."
case_wrong_retrieval_response = "Hệ thống không tìm thấy quy định phụ cấp tiền phòng khách sạn cho Trưởng phòng đi công tác tại Hà Nội trong ngữ cảnh được truy xuất."

report_rag_triad("3. Ca RAG Truy Xuất Sai Ngữ Cảnh (Lỗi Context Relevance)", case_wrong_retrieval_query, case_wrong_retrieval_context, case_wrong_retrieval_response)

print("\n--- KẾT THÚC LAB 9 ---")
