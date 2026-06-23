---
mo-ta: "Template IPO (Input–Process–Output) để mô tả một skill trước khi build. Track A BT1."
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 16:30 +07:00
---

# Skill Design — <TÊN SKILL>

> Điền từng mục. Mọi mục có chữ `<...>` phải thay bằng nội dung cụ thể của skill bạn định build.
> Mục đích của file này: là **đầu vào** cho skill `vibe-aiworkforce` (BT2) — AI đọc file này rồi sinh ra gói skill.
> Cấu trúc IPO = **Input → Process → Output**, bổ sung **Trigger / Quality Gate / HITL / Folder**.

---

## 0. Thông tin chung

- **Tên skill:** `<vi-du: review-contract>`
- **Một câu mô tả:** `<Skill này dùng để làm gì — vd: "Rà soát hợp đồng viễn thông, trích xuất điều khoản, phát hiện cờ đỏ">`
- **Người dùng:** `<ai dùng — vd: nhân viên đội pháp lý viễn thông>`
- **Mỏ neo lý thuyết:** IPO + PDCA + Skill ≈ App (xem slide addendum S5).

---

## 1. Trigger — Kích hoạt khi nào?

Skill sẽ tự nạp khi gặp đúng tín hiệu. Liệt kê:

- **Loại file đầu vào:** `<vd: .docx, .pdf, .xlsx, .txt>`
- **Từ khóa người dùng nói:** `<vd: "rà soát hợp đồng", "trích xuất điều khoản", "kiểm tra cờ đỏ", "contract review">`
- **Ngữ cảnh:** `<vd: khi người dùng gửi kèm 1 file hợp đồng và hỏi về rủi ro/điều khoản>`

> Nguyên tắc: trigger càng cụ thể, AI càng ít nạp nhầm skill.

---

## 2. Input — Đầu vào là gì?

- **Dữ liệu chính:** `<vd: 1 file hợp đồng .docx>`
- **Dữ liệu phụ trợ (knowledge base):** `<vd: kb/clause-library.md (điều khoản mẫu), kb/red-flag-rules.md (quy tắc cờ đỏ)>`
- **Điều kiện đầu vào hợp lệ:** `<vd: file tồn tại, không rỗng, độ dài tối thiểu, tỷ lệ lỗi OCR < ngưỡng>`
- **Dữ liệu KHÔNG được phép:** `<vd: hợp đồng thật của VTN, PII thật, số tiền thương mại thật>`

---

## 3. Process — Xử lý như thế nào?

Mô tả các bước AI/scripts thực hiện (theo vòng PDCA: Plan→Do→Check→Act):

1. **Intake (tiền xử lý):** `<đọc file, làm sạch, kiểm tra hợp lệ — chạy scripts/intake.py>`
2. **Extract (trích xuất):** `<theo schemas/<name>.schema.json, mỗi trường phải có source_evidence trích nguyên văn>`
3. **Validate (tự kiểm):** `<so khớp quote với văn bản gốc, hiệu chỉnh confidence — chạy scripts/validator.py>`
4. **Route (định tuyến):** `<đối chiếu red-flag-rules, rẽ AUTO / HITL / REJECT — chạy scripts/router.py>`

- **Script gọi:** `<liệt kê scripts/*.py mà skill được phép chạy>`
- **Công cụ AI dùng:** `<vd: LLM đọc hiểu + trích xuất; code (Python) kiểm chứng>`

---

## 4. Output — Đầu ra là gì?

- **File output:** `<vd: outputs/extracted-terms/<contract>.json + outputs/reports/<contract>-red-flag.md>`
- **Schema đầu ra:** `<vd: schemas/contract-term.schema.json — các trường: contract_id, partner, effective_date, sla, penalty, red_flags[], source_evidence[], confidence, needs_human_review>`
- **Trạng thái kết thúc:** `<vd: auto_pass / needs_human_review / reject>`

---

## 5. Quality Gate — Do / Don't

**DO (bắt buộc):**
- `<vd: Mỗi điều khoản trích xuất phải có source_evidence trích nguyên văn>`
- `<vd: Output phải khớp 100% JSON schema>`
- `<vd: Confidence phản ánh số evidence thực tế, không tự tin suông>`

**DON'T (cấm):**
- `<vd: Không khẳng định điều khoản khi thiếu căn cứ>`
- `<vd: Không tự đưa tư vấn pháp lý / quyết định phạt>`
- `<vd: Không ghi PII thật vào output>`

---

## 6. Human In the Loop (HITL)

- **Khi nào chuyển người duyệt:** `<vd: red flag nghiêm trọng, thiếu trường quan trọng, mâu thuẫn điều khoản, confidence < 0.7>`
- **Người duyệt làm gì:** `<vd: chốt kết luận pháp lý, quyết định phạt/bồi thường>`
- **AI làm gì vs Human làm gì:** `<AI trích xuất + cảnh báo; Human chốt rủi ro + quyết định>`

---

## 7. Cấu trúc folder skill sẽ tạo ra

> Tham chiếu cấu trúc chuẩn (xem `outputs/contract-term-extractor/` có sẵn). Vibe-aiworkforce (BT2) sẽ sinh cấu trúc này từ file design.

```text
<skill-name>/
  SKILL.md                  ← Bản đồ chỉ dẫn cho Agent (sinh từ §1–§6)
  skill.json                ← Metadata + triggers + permissions
  schemas/
    <output>.schema.json    ← Lược đồ đầu ra (từ §4)
  kb/
    clause-library.md       ← Điều khoản mẫu (từ §2)
    red-flag-rules.md       ← Quy tắc cờ đỏ (từ §3 route)
  scripts/
    intake.py               ← §3 bước 1
    validator.py            ← §3 bước 3
    router.py               ← §3 bước 4
  data/
    contracts/              ← Synthetic contracts (input test)
  outputs/
    extracted-terms/        ← JSON output
    reports/                ← Báo cáo cờ đỏ
    execution-log.csv       ← Nhật ký vận hành
  tests/
    test-cases.md
    test-report.md
```

---

## 8. Test cases tối thiểu

| # | Ca | Kỳ vọng |
|---|----|---------|
| 1 | Hợp đồng đầy đủ bình thường | auto_pass, đủ trường, có evidence |
| 2 | Hợp đồng thiếu trường | needs_human_review, flag thiếu trường |
| 3 | Hợp đồng có cờ đỏ | needs_human_review, red_flags[] không rỗng |
