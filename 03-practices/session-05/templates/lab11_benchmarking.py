# -*- coding: utf-8 -*-
"""
lab11_benchmarking.py
Thực hành: So sánh hiệu năng (Benchmarking) mô hình Embedding Cục bộ (Local) và Đám mây (Cloud)
"""

import os
import sys
import time
import google.generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

print("--- LAB 11: SO SÁNH HIỆU NĂNG LOCAL VS CLOUD EMBEDDING ---")

# 1. Cấu hình Gemini API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CẢNH BÁO: Không tìm thấy GEMINI_API_KEY trong file .env!")
    print("Vui lòng lấy API Key và cập nhật vào file .env")
    sys.exit(1)

genai.configure(api_key=api_key)

# 2. Chuẩn bị tập dữ liệu thử nghiệm (10 câu hỏi/mệnh đề thực tế về công tác phí)
test_sentences = [
    "Quy định tạm ứng công tác phí cho nhân viên như thế nào?",
    "Hạn mức phòng khách sạn tối đa của Trưởng phòng tại Hà Nội là bao nhiêu?",
    "Mức phụ cấp đi lại vùng 1 được thanh toán thế nào?",
    "Làm sao để thanh quyết toán tiền vé máy bay sau khi đi công tác về?",
    "Chuyên viên đi công tác Hải Phòng được ở khách sạn tối đa mấy tiền?",
    "Phó giám đốc đi công tác có được thanh toán vé thương gia không?",
    "Thời hạn nộp hồ sơ thanh toán công tác phí là bao nhiêu ngày kể từ khi về?",
    "Trường hợp mất hóa đơn taxi có được hoàn tiền công tác phí không?",
    "Quy trình duyệt tạm ứng tiền phòng của phòng Tài chính VinaTel Network.",
    "Tôi đi công tác từ Đà Nẵng ra Hà Nội bằng tàu hỏa thì tính phụ cấp thế nào?"
]

print(f"👉 Chuẩn bị danh sách {len(test_sentences)} câu test mẫu.")

# 3. Chạy thử nghiệm với Local Embedding (MiniLM)
print("\n[1/2] Đang tải mô hình Local Embedding (paraphrase-multilingual-MiniLM-L12-v2)...")
start_init_local = time.time()
local_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
end_init_local = time.time()
local_init_time = end_init_local - start_init_local
print(f" -> Thời gian khởi tạo/tải mô hình local: {local_init_time:.4f} giây")

print(" -> Đang sinh vector embedding cho 10 câu mẫu...")
start_run_local = time.time()
local_embeddings = local_model.encode(test_sentences)
end_run_local = time.time()
local_run_time = end_run_local - start_run_local
local_dim = len(local_embeddings[0])

# 4. Chạy thử nghiệm với Cloud Embedding (Gemini text-embedding-004)
print("\n[2/2] Đang kết nối mô hình Cloud Embedding (Gemini text-embedding-004)...")
print(" -> Đang sinh vector embedding cho 10 câu mẫu...")

start_run_cloud = time.time()
try:
    cloud_result = genai.embed_content(
        model="models/text-embedding-004",
        content=test_sentences,
        task_type="retrieval_document"
    )
    cloud_embeddings = cloud_result['embedding']
    end_run_cloud = time.time()
    cloud_run_time = end_run_cloud - start_run_cloud
    cloud_dim = len(cloud_embeddings[0])
    cloud_success = True
except Exception as e:
    print(f"⚠️ Lỗi khi gọi Cloud Embedding: {str(e)}")
    cloud_success = False
    cloud_run_time = 0
    cloud_dim = "N/A"

# 5. In bảng so sánh kết quả trực quan
print("\n" + "="*70)
print("             BẢNG SO SÁNH HIỆU NĂNG EMBEDDING (BENCHMARK)")
print("="*70)
print(f"{'Tiêu chí':<28} | {'Local Model (MiniLM)':<20} | {'Cloud Model (Gemini)':<20}")
print("-"*70)
print(f"{'Tên mô hình':<28} | {'multilingual-MiniLM':<20} | {'text-embedding-004':<20}")
print(f"{'Số chiều Vector (Dimension)':<28} | {local_dim:<20} | {cloud_dim:<20}")
print(f"{'Yêu cầu kết nối Mạng':<28} | {'Không (Offline)':<20} | {'Có (Online)':<20}")
print(f"{'Tổng thời gian sinh 10 câu':<28} | {local_run_time:.4f} giây | {cloud_run_time:.4f} giây" if cloud_success else f"{'Tổng thời gian sinh 10 câu':<28} | {local_run_time:.4f} giây | {'Lỗi kết nối':<20}")
print(f"{'Thời gian TB mỗi câu':<28} | {local_run_time/10:.4f} giây | {cloud_run_time/10:.4f} giây" if cloud_success else f"{'Thời gian TB mỗi câu':<28} | {local_run_time/10:.4f} giây | {'N/A':<20}")
print("="*70)

print("\n👉 NHẬN XÉT DÀNH CHO HỌC VIÊN:")
print("1. Số chiều Vector (Dimension):")
print("   - Mô hình Local (MiniLM) chỉ có 384 chiều, giúp tiết kiệm bộ nhớ lưu trữ và tốc độ so khớp khoảng cách cực nhanh.")
print("   - Mô hình Cloud (Gemini) có tới 768 chiều (hoặc hơn), giữ được nhiều sắc thái ngữ nghĩa phức tạp của tiếng Việt hơn.")
print("2. Tốc độ thực thi (Latency):")
print("   - Mô hình Local xử lý hoàn toàn trên CPU/GPU của máy học viên, không tốn thời gian truyền dữ liệu qua mạng nên có độ trễ cực thấp.")
print("   - Mô hình Cloud phụ thuộc vào đường truyền Internet và độ trễ phản hồi từ máy chủ Google, nên tổng thời gian xử lý thường cao hơn.")
print("3. Kịch bản áp dụng thực tế:")
print("   - Chọn Local Embedding: Khi cần làm các ứng dụng nhỏ chạy offline, bảo mật dữ liệu nội bộ không được gửi lên đám mây, hoặc tài nguyên phần cứng hạn chế.")
print("   - Chọn Cloud Embedding: Khi cần độ chính xác ngữ nghĩa cực cao đối với lượng lớn tài liệu học thuật phức tạp và hệ thống đã được triển khai lên cloud.")

print("\n--- KẾT THÚC LAB 11 ---")
