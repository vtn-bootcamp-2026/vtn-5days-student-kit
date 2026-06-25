# Bao cao Danh gia RAG Pipeline — HR Policy QA

Thoi gian tao: 2026-06-24 18:54:43
Tong so cau hoi: 12

## 1. Tong hop (Summary)

| Metric | SLI | SLO | Status |
|--------|-----|-----|--------|
| accuracy | 100.0% | 85.0% | PASS |
| citation_rate | 100.0% | 90.0% | PASS |
| refusal_rate | 100.0% | 95.0% | PASS |
| hallucination_free | 100.0% | 90.0% | PASS |
| quote_accuracy | 90.9% | 85.0% | PASS |

- In-scope: 8 | Correct: 8 | With citations: 8
- Out-of-scope: 2 | Correctly refused: 2
- Hallucination-free: 12/12

## 2. Chi tiet tung cau hoi (Per-Question Detail)

| # | Question | Class | Pass | Citations | Self-Check | Issues |
|---|----------|-------|------|-----------|------------|---------|
| 1 | Nhân viên chính thức được bao nhiêu ngày phép năm? | in-scope | PASS | Yes | N/A | None |
| 2 | Mức phụ cấp ăn trưa là bao nhiêu? | in-scope | FAIL | Yes | N/A | None |
| 3 | Quy trình xin nghỉ phép như thế nào? | in-scope | PASS | Yes | N/A | None |
| 4 | Thâm niên 6 năm thì được bao nhiêu ngày phép? | in-scope | PASS | Yes | N/A | None |
| 5 | Nhân viên thử việc có được phụ cấp điện thoại khôn... | in-scope | PASS | Yes | N/A | None |
| 6 | Công ty có hỗ trợ học MBA không? | in-scope | PASS | Yes | N/A | None |
| 7 | Nghỉ ốm quá 30 ngày thì lương như thế nào? | in-scope | PASS | Yes | N/A | None |
| 8 | Tôi đã làm 3 năm muốn nghỉ việc thì phép dư có đượ... | in-scope | PASS | Yes | N/A | None |
| 9 | Chính sách của công ty có tốt không? | ambiguous | FAIL | No | N/A | None |
| 10 | Tôi nghỉ 1 ngày thì được hưởng lương không? | ambiguous | FAIL | No | N/A | None |
| 11 | Chính sách bảo hiểm xã hội của công ty như thế nào... | out-of-scope | PASS | No | N/A | None |
| 12 | Tôi muốn xin chuyển công tác sang Hà Nội thì làm s... | out-of-scope | PASS | No | N/A | None |

## 3. Phan tich chi tiet (Detailed Breakdown)

### Q1: Nhân viên chính thức được bao nhiêu ngày phép năm?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | Số ngày phép/năm |
| --..." → match=exact overlap=100%
  - "Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm niên | Ngày phép thêm |
| ..." → match=exact overlap=100%

### Q2: Mức phụ cấp ăn trưa là bao nhiêu?
- **Phan loai**: in-scope
- **Ket qua**: FAIL
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Khong
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "| Đối tượng | Mức/ngày | Ghi chú |
| --- | ---: | --- |
| Nhân viên chính thức | 30.000 VNĐ | Trừ và..." → match=exact overlap=100%
  - "..." → match=none overlap=0%

### Q3: Quy trình xin nghỉ phép như thế nào?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "1. Gửi yêu cầu qua hệ thống nội bộ trước ít nhất 3 ngày làm việc.
2. Quản lý trực tiếp phê duyệt tro..." → match=exact overlap=100%

### Q4: Thâm niên 6 năm thì được bao nhiêu ngày phép?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | Số ngày phép/năm |
| --..." → match=exact overlap=100%
  - "Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm niên | Ngày phép thêm |
| ..." → match=exact overlap=100%

### Q5: Nhân viên thử việc có được phụ cấp điện thoại không?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Nhân viên thử việc không được hưởng phụ cấp điện thoại...." → match=exact overlap=100%

### Q6: Công ty có hỗ trợ học MBA không?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Công ty xem xét tài trợ một phần học phí cho chương trình MBA hoặc thạc sĩ liên quan đến ngành...." → match=exact overlap=100%

### Q7: Nghỉ ốm quá 30 ngày thì lương như thế nào?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Từ ngày thứ 31 trở đi hưởng 70% lương, tối đa 180 ngày/năm...." → match=exact overlap=100%

### Q8: Tôi đã làm 3 năm muốn nghỉ việc thì phép dư có được quy đổi tiền không?
- **Phan loai**: in-scope
- **Ket qua**: PASS
- **Dap an dung**: Co
- **Co trich dan**: Co
- **Trich dan hop le**: Co
- **Hallucination check**: PASS
- **Tu choi dung**: Khong
- **Chi tiet trich dan**:
  - "Phép dư không được quy đổi thành tiền trừ trường hợp nghỉ việc...." → match=exact overlap=100%

### Q9: Chính sách của công ty có tốt không?
- **Phan loai**: ambiguous
- **Ket qua**: FAIL
- **Dap an dung**: Khong
- **Co trich dan**: Khong
- **Trich dan hop le**: Khong
- **Hallucination check**: PASS
- **Tu choi dung**: Khong

### Q10: Tôi nghỉ 1 ngày thì được hưởng lương không?
- **Phan loai**: ambiguous
- **Ket qua**: FAIL
- **Dap an dung**: Khong
- **Co trich dan**: Khong
- **Trich dan hop le**: Khong
- **Hallucination check**: PASS
- **Tu choi dung**: Khong

### Q11: Chính sách bảo hiểm xã hội của công ty như thế nào?
- **Phan loai**: out-of-scope
- **Ket qua**: PASS
- **Dap an dung**: Khong
- **Co trich dan**: Khong
- **Trich dan hop le**: Khong
- **Hallucination check**: PASS
- **Tu choi dung**: Co

### Q12: Tôi muốn xin chuyển công tác sang Hà Nội thì làm sao?
- **Phan loai**: out-of-scope
- **Ket qua**: PASS
- **Dap an dung**: Khong
- **Co trich dan**: Khong
- **Trich dan hop le**: Khong
- **Hallucination check**: PASS
- **Tu choi dung**: Co
