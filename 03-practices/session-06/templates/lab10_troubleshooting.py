# -*- coding: utf-8 -*-
"""
lab10_troubleshooting.py
Thực hành: Chuẩn đoán và xử lý 3 lỗi kỹ thuật kinh điển trong RAG
"""

import os
import sys

print("--- LAB 10: CHUẨN ĐOÁN VÀ XỬ LÝ LỖI KỸ THUẬT KINH ĐIỂN ---")

# --- LỖI 1: LỖI MÃ HÓA UTF-8 TRÊN WINDOWS (UnicodeDecodeError / Ký tự lỗi) ---
def simulate_encoding_issue():
    print("\n-------------------------------------------------------------")
    print("[MÔ PHỎNG LỖI 1] Lỗi mã hóa đọc file tiếng Việt trên Windows")
    print("-------------------------------------------------------------")
    policy_file = "../synthetic-data/hr-policies/policy-hotel-limit.md"
    
    # Giả lập lỗi: Đọc không có encoding='utf-8'
    print("❌ Thử nghiệm 1.1: Đọc file KHÔNG chỉ định encoding (Windows mặc định):")
    try:
        # Sử dụng encoding mặc định của hệ thống (trên Windows thường là cp1252 hoặc gbk)
        # Để mô phỏng chân thực, ta thử mở bằng cp1252
        with open(policy_file, "r", encoding="cp1252") as f:
            content = f.read()
            print(" -> Đọc thành công nhưng nội dung bị lỗi font chữ (Mojibake):")
            print(f"    Xem thử 3 dòng đầu: \n\"\"\"\n{content[:150]}\n\"\"\"")
    except UnicodeDecodeError as e:
        print(f" -> Xảy ra lỗi UnicodeDecodeError ngay lập tức: {str(e)}")
        print("    (Đây là lỗi cực kỳ phổ biến khi chạy Python trên Windows 11!)")

    print("\n✅ Giải pháp sửa lỗi: Luôn chỉ định encoding='utf-8' khi mở file:")
    try:
        with open(policy_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(" -> Đọc thành công và hiển thị tiếng Việt chuẩn xác:")
            print(f"    Xem thử 3 dòng đầu: \n\"\"\"\n{content[:150]}\n\"\"\"")
    except Exception as e:
        print(f" -> Vẫn xảy ra lỗi: {str(e)}")


# --- LỖI 2: CHUNK SIZE QUÁ NHỎ LÀM MẤT NGỮ NGHĨA HOÀN TOÀN ---
def simulate_chunk_size_issue():
    print("\n-------------------------------------------------------------")
    print("[MÔ PHỎNG LỖI 2] Lỗi phân đoạn (Chunking) quá nhỏ làm mất ngữ nghĩa")
    print("-------------------------------------------------------------")
    
    original_text = "Chức danh Trưởng phòng đi công tác tại Hà Nội được thanh toán tối đa 1.500.000 VNĐ/ngày tiền phòng."
    print(f"Văn bản quy định gốc:\n  \"{original_text}\"")
    
    # Trường hợp 1: Phân đoạn quá nhỏ (ví dụ: chunk_size = 15 ký tự)
    print("\n❌ Thử nghiệm 2.1: Phân đoạn quá nhỏ (15 ký tự):")
    small_chunks = [original_text[i:i+15] for i in range(0, len(original_text), 15)]
    for idx, chunk in enumerate(small_chunks):
        print(f"  Chunk #{idx}: \"{chunk}\"")
    
    print(" 👉 Nhận xét: Các chunk bị cắt vụn (ví dụ: '1.500.00' và '0 VNĐ/ngày').")
    print("    Không một chunk nào còn giữ đủ ý nghĩa 'Trưởng phòng được bao nhiêu tiền' để vector search tìm kiếm chính xác.")

    # Trường hợp 2: Phân đoạn hợp lý (theo dấu câu hoặc độ dài lớn hơn, ví dụ: chunk_size = 100 ký tự)
    print("\n✅ Thử nghiệm 2.2: Phân đoạn hợp lý (bao trọn ý nghĩa câu):")
    proper_chunks = [original_text] # Ở đây câu ngắn nên giữ nguyên 1 chunk là tối ưu nhất
    for idx, chunk in enumerate(proper_chunks):
        print(f"  Chunk #{idx}: \"{chunk}\"")
    print(" 👉 Nhận xét: Chunk giữ nguyên toàn bộ mệnh đề, số tiền và địa danh đi kèm.")


# --- LỖI 3: LỖI CẠN QUOTA / SAI API KEY / LỖI MẠNG KHI GỌI LLM ---
def simulate_api_quota_issue():
    print("\n-------------------------------------------------------------")
    print("[MÔ PHỎNG LỖI 3] Lỗi API Key hoặc Cạn hạn mức (Quota) cuộc gọi")
    print("-------------------------------------------------------------")
    
    import google.generativeai as genai
    
    # Cố tình sử dụng API Key sai để kích hoạt lỗi
    fake_api_key = "AIzaSyFakeKey_ThisIsWrongForSure_12345"
    print(f"❌ Thử nghiệm 3.1: Gọi Gemini API với API Key sai: \"{fake_api_key}\"")
    
    try:
        # Cấu hình API key sai tạm thời
        genai.configure(api_key=fake_api_key)
        model_llm = genai.GenerativeModel("gemini-3.5-flash")
        print(" -> Đang gửi yêu cầu sinh nội dung...")
        response = model_llm.generate_content("Xin chào")
        print(response.text)
    except Exception as e:
        print("🔴 BẮT ĐƯỢC LỖI GỌI API:")
        print(f"    {str(e)}")
        print("\n✅ Hướng dẫn khắc phục cho học viên:")
        print("    1. Kiểm tra lại xem file '.env' đã được tạo ở thư mục gốc của bài thực hành chưa.")
        print("    2. Đảm bảo biến 'GEMINI_API_KEY' trong file '.env' khớp chính xác với Key được cấp phát.")
        print("    3. Kiểm tra kết nối mạng Internet (không chặn proxy/VPN).")
        print("    4. Nếu lỗi 429 hoặc Quota Exceeded: Tài khoản đã hết hạn mức chạy thử miễn phí.")


# Chạy toàn bộ các ca mô phỏng lỗi
simulate_encoding_issue()
simulate_chunk_size_issue()
simulate_api_quota_issue()

print("\n--- KẾT THÚC LAB 10 ---")
