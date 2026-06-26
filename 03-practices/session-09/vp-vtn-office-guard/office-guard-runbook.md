---
mo-ta: "Biên bản bàn giao 'Vệ sĩ văn phòng VTN' — cho nhóm non-tech"
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-26 08:35 +07:00
updated-at: 2026-06-26 08:35 +07:00
---

# Biên bản bàn giao — Vệ sĩ văn phòng VTN

## Công cụ làm gì (1 câu)
Che giấu thông tin cá nhân trong tài liệu văn phòng VTN và cản lệnh giả danh hệ thống, chạy hoàn toàn trong Antigravity tại máy người dùng — không cần API ngoài.

## Cách chạy (3 bước, không cần biết code)
1. Mở Antigravity tại thư mục `03-practice/session-09/`.
2. Dán lần lượt các prompt trong `lab.md` (Part A → D) — Antigravity tự dựng & nâng cấp Skill.
3. Chạy: `python vp-vtn-office-guard/scripts/anonymizer.py` → xem kết quả trong `outputs/`.

## Cấu trúc Skill Package bàn giao
```
vp-vtn-office-guard/
├── SKILL.md            ← vai trò, quy trình, giới hạn, an toàn
├── skill.json          ← cấu hình & cổng chất lượng
├── kb/
│   ├── pii-categories.md   ← loại PII cần ẩn
│   └── safe-terms.md       ← thuật ngữ KHÔNG được ẩn nhầm
├── scripts/
│   ├── anonymizer.py       ← ẩn danh PII
│   └── hook.py             ← chặn thao tác nguy hiểm
└── outputs/
    ├── vp-vtn-ban-giao-ca-redacted.txt
    └── execution-log.csv
```

## Kiểm tra nhanh sau bàn giao
- [x] Mở `outputs/vp-vtn-ban-giao-ca-redacted.txt` — PII đã ẩn, mã phiếu/tiền còn nguyên.
- [x] Mở `outputs/execution-log.csv` — không có PII gốc.
- [x] Email mục 2 bị vô hiệu hoá + cờ rà soát bật.
- [x] Bảng kiểm tuân thủ đạt ≥ 7/8.

## Hạn chế đã biết
- Tên người được nhận diện qua ngữ cảnh trong Antigravity; nếu văn bản quá tối nghĩa, hệ thống GIỮ NGUYÊN + bật cờ rà soát thay vì đoán bừa (an toàn hơn).
