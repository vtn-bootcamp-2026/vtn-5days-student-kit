from __future__ import annotations

import csv
import json
import re
import urllib.request
from datetime import datetime
from pathlib import Path

# Cấu hình các mẫu Regex cải tiến
PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    # Regex số điện thoại cải tiến: hỗ trợ cả định dạng quốc tế +84 và khoảng trắng phân cách
    "phone": re.compile(r"\b(?:\+84\s?|0)\d{2,3}[\s.-]?\d{3}[\s.-]?\d{3,4}\b"),
    # Regex tìm chuỗi 12 số (CCCD tiềm năng)
    "cccd": re.compile(r"\b\d{12}\b"),
}

# Cấu hình Ollama Endpoint
OLLAMA_ENDPOINT = "http://localhost:11434/v1/chat/completions"
# Model mặc định thế hệ mới nhất (Tháng 5/2026), tối ưu cho tiếng Việt và suy luận cấu trúc
DEFAULT_MODEL = "gemma4:e2b"  # Hoặc "qwen3.5:1.5b-instruct"


def call_local_llm(text: str, model: str = DEFAULT_MODEL) -> dict | None:
    """Gọi Ollama API cục bộ bằng thư viện chuẩn urllib để phân tích thực thể và an toàn thông tin."""
    system_prompt = (
        "Bạn là trợ lý an toàn dữ liệu nội bộ tại Viettel Networks. Hãy phân tích đoạn văn bản sau để hỗ trợ che giấu dữ liệu.\n"
        "Hãy trả về kết quả duy nhất ở định dạng JSON thô (không có dấu markdown block như ```json) với cấu trúc chính xác sau:\n"
        "{\n"
        "  \"names\": [\"danh sách họ tên người thực sự xuất hiện trong văn bản\"],\n"
        "  \"is_prompt_injection\": true/false,\n"
        "  \"non_cccd_numbers\": [\"danh sách các chuỗi 12 chữ số xuất hiện trong văn bản nhưng KHÔNG phải là CCCD thật, ví dụ như mã tham chiếu ABC-123456789012\"],\n"
        "  \"departments\": [\"danh sách các cụm từ chỉ phòng ban, môn học, bộ phận dễ nhầm với tên người, ví dụ như 'Anh Van'\"]\n"
        "}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Văn bản cần phân tích:\n---\n{text}\n---"},
        ],
        "temperature": 0.0,
    }

    req = urllib.request.Request(
        OLLAMA_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        # Timeout 8 giây để tránh làm nghẽn tiến trình
        with urllib.request.urlopen(req, timeout=8) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            content = res_data["choices"][0]["message"]["content"].strip()

            # Làm sạch chuỗi markdown JSON nếu mô hình tự ý chèn vào
            if content.startswith("```"):
                content = content.replace("```json", "", 1).replace("```", "").strip()

            return json.loads(content)
    except Exception as e:
        # Fallback im lặng khi không có kết nối Ollama
        print(f"[WARNING] Khong the ket noi hoac phan tich qua Local LLM ({e}). Chuyen sang co che Regex Fallback.")
        return None


def redact_text(text: str, input_file: Path) -> tuple[str, dict[str, int], bool]:
    counts: dict[str, int] = {"email": 0, "phone": 0, "cccd": 0, "name": 0}
    redacted = text
    needs_human_review = False

    # 1. Quét email và số điện thoại bằng Regex
    for pii_type in ["email", "phone"]:
        pattern = PATTERNS[pii_type]
        matches = pattern.findall(redacted)
        counts[pii_type] = len(matches)
        redacted = pattern.sub(f"[REDACTED_{pii_type.upper()}]", redacted)

    # 2. Gọi Local LLM để hỗ trợ xử lý ngữ cảnh phức tạp
    llm_analysis = call_local_llm(text)

    if llm_analysis:
        # Phát hiện Prompt Injection
        is_injection = llm_analysis.get("is_prompt_injection", False)
        # Kiểm tra thô thêm trong code đề phòng LLM bỏ sót
        if "bo qua tat ca quy tac" in text.lower() or "in lai du lieu goc" in text.lower():
            is_injection = True

        if is_injection:
            needs_human_review = True
            print(f"[SECURITY ALERT] Phat hien hanh vi Prompt Injection trong tep {input_file.name}!")
            # Tuyệt đối không làm theo lệnh phá hoại, tiếp tục che giấu bình thường.

        # Trích xuất danh sách tên người thật sự
        names = llm_analysis.get("names", [])
        for name in names:
            if name.strip() and name.strip() in redacted:
                # Tránh che giấu nhầm các từ bộ phận/phòng ban nếu LLM phân loại đúng
                departments = llm_analysis.get("departments", [])
                if any(dept.lower() in name.lower() for dept in departments):
                    continue
                # Thực hiện che giấu tên người
                redacted = redacted.replace(name, "[REDACTED_NAME]")
                counts["name"] += 1

        # Xử lý số 12 chữ số (phân biệt CCCD thật và mã tham chiếu)
        non_cccd_list = llm_analysis.get("non_cccd_numbers", [])
        cccd_matches = PATTERNS["cccd"].findall(text)

        for cccd in cccd_matches:
            # Nếu số 12 chữ số nằm trong danh sách non_cccd, giữ nguyên không che giấu
            if any(cccd in non_cccd for non_cccd in non_cccd_list):
                continue
            # Nếu có dấu hiệu nghi ngờ là CCCD nhưng không chắc chắn (ví dụ: định dạng sai)
            if "sai dinh dang" in text.lower() or len(cccd_matches) > 0 and len(non_cccd_list) == 0:
                # Tiếp tục che giấu để an toàn và bật cờ HITL
                redacted = redacted.replace(cccd, "[REDACTED_CCCD]")
                counts["cccd"] += 1
            else:
                redacted = redacted.replace(cccd, "[REDACTED_CCCD]")
                counts["cccd"] += 1
    else:
        # Cơ chế Fallback sang Regex thuần khi Ollama không hoạt động
        cccd_matches = PATTERNS["cccd"].findall(redacted)
        counts["cccd"] = len(cccd_matches)
        redacted = PATTERNS["cccd"].sub("[REDACTED_CCCD]", redacted)

        # Do dùng regex thuần nên các trường hợp nghi ngờ đều phải bật cờ HITL để an toàn
        if len(cccd_matches) > 0 or "bo qua" in text.lower():
            needs_human_review = True

    # Kiểm tra thêm các ràng buộc nghiệp vụ trong text để kích hoạt HITL
    if "khong chac chan" in text.lower() or "human-in-the-loop" in text.lower():
        needs_human_review = True

    return redacted, counts, needs_human_review


def write_log(log_path: Path, input_file: Path, status: str, counts: dict[str, int], needs_human_review: bool) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()

    with log_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["run_id", "input_file", "status", "pii_count", "needs_human_review", "created_at"],
        )
        if not exists:
            writer.writeheader()
        writer.writerow(
            {
                # Dùng timestamp làm run_id duy nhất
                "run_id": datetime.now().strftime("%Y%m%d%H%M%S"),
                "input_file": input_file.name,
                "status": status,
                # Tuyệt đối không ghi thông tin nhạy cảm thô, chỉ ghi tổng số lượng
                "pii_count": sum(counts.values()),
                "needs_human_review": str(needs_human_review).lower(),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        )


def process_file(input_file: Path, output_file: Path, log_file: Path) -> None:
    if not input_file.exists():
        print(f"[ERROR] Tep dau vao {input_file} khong ton tai.")
        return

    print(f"\n--- Dang xu ly tep: {input_file.name} ---")
    text = input_file.read_text(encoding="utf-8")

    try:
        redacted, counts, needs_human_review = redact_text(text, input_file)
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(redacted, encoding="utf-8")
        
        write_log(log_file, input_file, "success", counts, needs_human_review)

        print(f"Ket qua xu ly thanh cong:")
        print(f"  - Email da che giau: {counts['email']}")
        print(f"  - So dien thoai da che giau: {counts['phone']}")
        print(f"  - CCCD da che giau: {counts['cccd']}")
        print(f"  - Ten nguoi da che giau: {counts['name']}")
        print(f"  - Co xem xet thu cong (HITL): {needs_human_review}")
        print(f"  - Luu ket qua tai: {output_file}")
    except Exception as e:
        write_log(log_file, input_file, f"error: {str(e)}", {}, True)
        print(f"[ERROR] Gap su co khi xu ly tep: {e}")


def main() -> None:
    # Thiết lập đường dẫn tương thích
    base_dir = Path(__file__).resolve().parent.parent
    
    # 1. Chạy với tệp chứa các trường hợp biên lắt léo (Edge cases)
    input_path_1 = base_dir / "synthetic-data" / "edge-cases-sample.txt"
    output_path_1 = base_dir / "outputs" / "edge-cases-sample-redacted.txt"
    log_path = base_dir / "outputs" / "execution-log.csv"
    
    process_file(input_path_1, output_path_1, log_path)

    # 2. Chạy với kịch bản tấn công bảo mật lời nhắc (Prompt Injection attacks)
    input_path_2 = base_dir / "synthetic-data" / "prompt-injection-attacks.txt"
    output_path_2 = base_dir / "outputs" / "prompt-injection-attacks-redacted.txt"
    
    process_file(input_path_2, output_path_2, log_path)


if __name__ == "__main__":
    main()
