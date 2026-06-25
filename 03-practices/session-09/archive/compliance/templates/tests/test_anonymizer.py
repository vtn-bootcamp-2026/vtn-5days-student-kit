# ==============================================================================
# BỘ KIỂM THỬ TỰ ĐỘNG CAPSTONE - MINI TOOL ANONYMIZER (10 TEST CASES)
# Chạy kiểm thử bằng cách thực thi lệnh: pytest tests/ hoặc pytest capstone_project/tests/
# ==============================================================================

import sys
import pytest
from pathlib import Path

# Định vị thư mục src nằm ở session-06-compliance-capstone/src
# Cả templates/tests/ và capstone_project/tests/ đều cách session-06 hai cấp thư mục cha
session_dir = Path(__file__).resolve().parents[2]
src_dir = session_dir / "src"

sys.path.insert(0, str(src_dir))

try:
    from anonymizer import anonymize_text
except ImportError as e:
    print(f"[ERROR] Không thể import anonymize_text từ {src_dir}: {e}")
    sys.exit(1)

# Định nghĩa 10 ca kiểm thử như trong Checkpoint A1/A2
TEST_CASES = [
    # Nhóm 1: Bình thường (TC-01 đến TC-03) - Phải che giấu chính xác PII
    ("TC-01", "Vui lòng gửi hợp đồng đến nguyenvana@gmail.com", "[REDACTED_EMAIL]"),
    ("TC-02", "Liên hệ tôi qua số 0912345678 nhé", "[REDACTED_PHONE]"),
    ("TC-03", "Căn cước công dân số 079201001234", "[REDACTED_CCCD]"),
    
    # Nhóm 2: Lỗi định dạng (TC-04 đến TC-06) - Không được ẩn nhầm thông tin không chuẩn
    ("TC-04", "Gửi cho nguyenvana.gmail.com giúp tôi", "nguyenvana.gmail.com"),
    ("TC-05", "Gọi cho tôi số 0912345678910", "0912345678910"),
    ("TC-06", "CCCD số 079abc01234xyz", "079abc01234xyz"),
    
    # Nhóm 3: Thiếu dữ liệu (TC-07, TC-08) - Xử lý mượt, không crash
    ("TC-07", "", ""),
    ("TC-08", "Hôm nay thời tiết đẹp quá", "Hôm nay thời tiết đẹp quá"),
    
    # Nhóm 4: Vượt phạm vi & Ngữ cảnh (TC-09, TC-10)
    ("TC-09", "KH Trần Văn B, email tranb@yahoo.com, SĐT 0987654321, CCCD 079201005678", "redact_multiple"),
    ("TC-10", "Email là viết tắt của Electronic Mail", "Email"),
]

@pytest.mark.parametrize("case_id, input_text, expected_outcome", TEST_CASES)
def test_anonymizer_cases(case_id, input_text, expected_outcome):
    output = anonymize_text(input_text)
    
    if case_id in ["TC-01", "TC-02", "TC-03"]:
        # Phải chứa nhãn che giấu
        assert expected_outcome in output, f"{case_id} thất bại: Không che giấu thành công {expected_outcome}."
        
    elif case_id in ["TC-04", "TC-05", "TC-06", "TC-08", "TC-10"]:
        # Không được che giấu nhầm, giữ nguyên dữ liệu gốc
        assert expected_outcome in output, f"{case_id} thất bại: Dữ liệu bị thay đổi sai lệch."
        assert "[REDACTED_" not in output, f"{case_id} thất bại: Bị che giấu nhầm."
        
    elif case_id == "TC-07":
        # Chuỗi rỗng phải trả về rỗng
        assert output == "", f"{case_id} thất bại: Đầu ra không rỗng."
        
    elif case_id == "TC-09":
        # Phải che ít nhất 3 trường PII nhạy cảm trong câu phức
        redacted_count = output.count("[REDACTED_")
        assert redacted_count >= 3, f"{case_id} thất bại: Số lượng trường bị che giấu quá ít ({redacted_count}/3)."
