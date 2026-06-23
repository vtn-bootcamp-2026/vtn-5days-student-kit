---
mo-ta: "Đáp án tham khảo cho BT1 — skill_design.md hoàn chỉnh cho skill review-contract. HV đối chiếu bài自己做 của mình."
trang-thai: active
phien-ban: v1.0
created-at: 2026-06-23 16:30 +07:00
---

# Skill Design — `review-contract` (EXAMPLE — đáp án tham khảo)

> Đây là một `skill_design.md` hoàn chỉnh, viết cho skill **review-contract**. HV làm BT1 xong mở file này ra đối chiếu. Ở BT2, `vibe-aiworkforce` sẽ đọc đúng file kiểu này để sinh ra gói skill.

---

## 0. Thông tin chung

- **Tên skill:** `review-contract`
- **Một câu mô tả:** Rà soát hợp đồng viễn thông — trích xuất điều khoản chính, phát hiện cờ đỏ rủi ro thương mại, xuất báo cáo có dẫn chứng và định tuyến HITL khi rủi ro cao.
- **Người dùng:** Nhân viên đội pháp lý viễn thông (non-tech).
- **Mỏ neo lý thuyết:** IPO + PDCA + Skill ≈ App (slide addendum S5).

---

## 1. Trigger — Kích hoạt khi nào?

- **Loại file đầu vào:** `.docx` (BT2); `.pdf`, `.xlsx` (sau BT3 improve).
- **Từ khóa người dùng nói:** "rà soát hợp đồng", "trích xuất điều khoản", "kiểm tra cờ đỏ", "contract review", "review contract".
- **Ngữ cảnh:** Người dùng gửi kèm 1 file hợp đồng và hỏi về điều khoản / rủi ro / SLA.

---

## 2. Input — Đầu vào là gì?

- **Dữ liệu chính:** 1 file hợp đồng `.docx` (synthetic, dạng theo Nghị định 30).
- **Dữ liệu phụ trợ (knowledge base):**
  - `kb/clause-library.md` — điều khoản mẫu thường gặp trong hợp đồng viễn thông.
  - `kb/red-flag-rules.md` — quy tắc phát hiện rủi ro thương mại/SLA/gia hạn.
- **Điều kiện đầu vào hợp lệ:** file tồn tại, không rỗng, ≥ 500 ký tự, tỷ lệ lỗi OCR < 5%.
- **Dữ liệu KHÔNG được phép:** hợp đồng thật của VTN, tên đối tác thật, MST/PII thật, số tiền thương mại thật.

---

## 3. Process — Xử lý như thế nào?

Theo vòng PDCA (Plan→Do→Check→Act):

1. **Intake (Plan/Do):** đọc `.docx` thành text, làm sạch ký tự nhiễu, kiểm tra hợp lệ → `scripts/intake.py --file <path>`.
2. **Extract (Do):** theo `schemas/contract-term.schema.json`, trích xuất các trường; **mỗi trường phải có `source_evidence` trích nguyên văn** từ hợp đồng. Đối chiếu `kb/clause-library.md`.
3. **Validate (Check):** so khớp fuzzy quote với văn bản gốc, hiệu chỉnh confidence theo số evidence thực tế, kiểm đủ trường bắt buộc → `scripts/validator.py --json <j> --source <txt>`. Nếu `adjusted_confidence < 0.7` → bật `needs_human_review`.
4. **Route (Act):** đối chiếu `kb/red-flag-rules.md`, ghi log CSV, rẽ 3 nhánh AUTO / HITL / REJECT, xuất báo cáo cờ đỏ → `scripts/router.py --json <j> --rules kb/red-flag-rules.md`.

- **Script gọi:** `scripts/intake.py`, `scripts/validator.py`, `scripts/router.py`.
- **Phân vai AI vs code:** AI (LLM) đọc hiểu + trích xuất; code (Python) kiểm schema, so khớp, định tuyến, ghi log — **không bắt LLM làm việc code làm chắc hơn**.

---

## 4. Output — Đầu ra là gì?

- **File output:**
  - `outputs/extracted-terms/<contract>.json` — kết quả trích xuất.
  - `outputs/reports/<contract>-red-flag.md` — báo cáo cờ đỏ (nếu có).
  - `outputs/execution-log.csv` — nhật ký 1 dòng/ca.
- **Schema đầu ra** (`schemas/contract-term.schema.json`), các trường:
  `contract_id`, `partner`, `effective_date`, `expiry_date`, `contract_value`, `sla`, `penalty_clause`, `renewal_clause`, `red_flags[]`, `source_evidence[]` (mỗi item: `quote`, `section`, `confidence`), `overall_confidence`, `needs_human_review`, `review_reason`, `status`.
- **Trạng thái kết thúc:** `auto_pass` | `needs_human_review` | `reject`.

---

## 5. Quality Gate — Do / Don't

**DO:**
- Mỗi điều khoản trích xuất phải có `source_evidence.quote` trích nguyên văn từ hợp đồng.
- Output khớp 100% JSON schema (kiểm bằng validator).
- `overall_confidence` tính từ số evidence thực tế + độ khớp fuzzy, không tự tin suông.
- Mọi ca rủi ro cao → `needs_human_review = true`.

**DON'T:**
- Không khẳng định điều khoản khi thiếu căn cứ / quote không khớp nguồn.
- Không tự đưa tư vấn pháp lý, không quyết định phạt/bồi thường.
- Không ghi PII thật (tên thật, MST thật, số tiền thật) vào output.
- Không tự thêm trường ngoài schema.

---

## 6. Human In the Loop (HITL)

- **Khi nào chuyển người duyệt:** red flag nghiêm trọng (SLA < 99%, tự động gia hạn, phạt > 10%), thiếu trường quan trọng, mâu thuẫn điều khoản, `confidence < 0.7`.
- **Người duyệt làm gì:** chốt kết luận pháp lý, quyết định phạt/bồi thường, ký duyệt.
- **AI vs Human:** AI trích xuất + cảnh báo + hạ confidence khi thiếu căn cứ; Human chốt rủi ro + quyết định thương mại.

---

## 7. Cấu trúc folder skill sẽ tạo ra

> Cùng cấu trúc với `outputs/contract-term-extractor/` đã có sẵn (tham chiếu). `vibe-aiworkforce` (BT2) sẽ sinh cấu trúc này.

```text
review-contract/
  SKILL.md
  skill.json
  schemas/
    contract-term.schema.json
  kb/
    clause-library.md
    red-flag-rules.md
  scripts/
    intake.py
    validator.py
    router.py
  data/
    contracts/              ← synthetic .docx (001..004)
    contracts-index.csv
  outputs/
    extracted-terms/
    reports/
    execution-log.csv
  tests/
    test-cases.md
    test-report.md
```

---

## 8. Test cases tối thiểu

| # | Ca | Kỳ vọng |
|---|----|---------|
| 1 | `contract-001.docx` (đầy đủ, bình thường) | `auto_pass`, đủ trường, mọi trường có evidence, confidence ≥ 0.8 |
| 2 | `contract-002.docx` (thiếu trường, lỗi OCR) | `needs_human_review`, flag thiếu trường, confidence < 0.7 |
| 3 | `contract-003-risky.docx` (3 cờ đỏ rõ) | `needs_human_review`, `red_flags[]` ≥ 3 (SLA / gia hạn / phạt) |
| 4 | `contract-004-telecom-sla.docx` (SLA 99.99%) | `auto_pass` nếu SLA đạt, flag nếu SLA < 99% |

> Tiêu chuẩn đạt: ≥ 3/4 ca pass đúng trạng thái.
