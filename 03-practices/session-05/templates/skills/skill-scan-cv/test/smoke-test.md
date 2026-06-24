# Kịch bản kiểm thử: smoke-test

Tài liệu này hướng dẫn cách kiểm thử nhanh kỹ năng `skill-scan-cv` trên môi trường local.

---

## 1. Thiết lập trước khi test

Đảm bảo các file sau đã nằm đúng cấu trúc thư mục:
- Cấu hình: `skill.json`
- Quy tắc: `kb/evaluation-rubrics.md`, `kb/red-flag-rules.md`
- Schema: `schema/evaluation.schema.json`
- Scripts: `scripts/intake.py`, `scripts/validator.py`, `scripts/router.py`
- Dữ liệu mẫu: `synthetic-data/cv-sample.md`

Đồng thời tạo thư mục chứa đầu ra nếu chưa có:
```bash
mkdir -p output/skill-scan-cv/outputs
```

---

## 2. Các bước chạy kiểm thử tự động

### Bước 1: Chạy kiểm tra Intake
Chạy script intake để kiểm tra tính hợp lệ của tệp CV đầu vào:
```bash
python scripts/intake.py --file synthetic-data/cv-sample.md --json
```
**Kết quả kỳ vọng:** Xuất ra JSON có `"valid": true` và `"needs_human_review": false` (hoặc `true` tùy thuộc vào độ dài/OCR).

### Bước 2: Giả lập kết quả trích xuất và chạy Validator
Tạo một file JSON giả lập kết quả trích xuất của AI tại `output/skill-scan-cv/outputs/extracted-cv.json` với nội dung sau:
```json
{
  "candidate_name": "Nguyễn Văn A",
  "contact_info": {
    "email": "candidate.a@example.com",
    "phone": "0901234567"
  },
  "experience_years": 4,
  "education": "Cử nhân Khoa học Máy tính",
  "skills": ["Python", "SQL", "JavaScript", "Django", "FastAPI", "Git", "Docker"],
  "suitability_score": 85,
  "matched_criteria": [
    "Cử nhân Khoa học Máy tính",
    "Kinh nghiệm làm việc với Python và Django",
    "Có kỹ năng làm việc nhóm Agile/Scrum"
  ],
  "missing_criteria": [
    "Kinh nghiệm làm việc với các hệ thống Cloud lớn"
  ],
  "red_flags": [],
  "status": "auto_pass",
  "evidence": [
    {
      "claim": "Cử nhân Khoa học Máy tính",
      "verbatim_quote": "Cử nhân Khoa học Máy tính - Trường Đại học Công nghệ",
      "source": "cv-sample.md",
      "location": "Phần Học vấn"
    },
    {
      "claim": "Kinh nghiệm làm việc Python",
      "verbatim_quote": "Phát triển hệ thống quản lý dữ liệu lớn bằng Python và Django.",
      "source": "cv-sample.md",
      "location": "Phần Kinh nghiệm"
    }
  ],
  "confidence_score": 0.9,
  "need_review": false
}
```

Sau đó chạy script validator để kiểm chứng:
```bash
python scripts/validator.py --json output/skill-scan-cv/outputs/extracted-cv.json --source synthetic-data/cv-sample.md
```
**Kết quả kỳ vọng:** Xuất ra JSON validation có `"valid": true` và không có lỗi nào trong mảng `issues`.

### Bước 3: Định tuyến hồ sơ và ghi log
Chạy script router để xác định trạng thái hồ sơ ứng viên và sinh báo cáo:
```bash
python scripts/router.py \
  --json output/skill-scan-cv/outputs/extracted-cv.json \
  --log output/skill-scan-cv/outputs/execution-log.csv \
  --report output/skill-scan-cv/outputs/report-nguyen-van-a.md
```
**Kết quả kỳ vọng:** 
- Xuất ra màn hình thông tin định tuyến dạng JSON (`"route": "auto_pass"` hoặc `"needs_human_review"`).
- Ghi một dòng log vào `output/skill-scan-cv/outputs/execution-log.csv`.
- Sinh tệp báo cáo chi tiết tại `output/skill-scan-cv/outputs/report-nguyen-van-a.md`.
