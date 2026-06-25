# Báo cáo Đánh giá RAG Pipeline — HR Policy QA

Thời gian tạo: 2026-06-25 13:50:40
Tổng số câu hỏi: 24

## 1. Tổng hợp (Summary)

| Metric             | SLI    | SLO   | Status |
| ------------------ | ------ | ----- | ------ |
| accuracy           | 72.2%  | 85.0% | FAIL   |
| citation_rate      | 100.0% | 90.0% | PASS   |
| refusal_rate       | 100.0% | 95.0% | PASS   |
| hallucination_free | 100.0% | 90.0% | PASS   |
| quote_accuracy     | 100.0% | 85.0% | PASS   |
|                    |        |       |        |

- In-scope: 18 | Correct: 13 | With citations: 18
- Out-of-scope: 4 | Correctly refused: 4
- Hallucination-free: 24/24

## 2. Chi tiết từng câu hỏi (Per-Question Detail)

| #  | Question                                                             | Class        | Pass | Citations | Self-Check | Issues |
| -- | -------------------------------------------------------------------- | ------------ | ---- | --------- | ---------- | ------ |
| 1  | Nhân viên chính thức được bao nhiêu ngày phép năm?        | in-scope     | PASS | Yes       | N/A        | None   |
| 2  | Mức phụ cấp ăn trưa là bao nhiêu?                             | in-scope     | PASS | Yes       | N/A        | None   |
| 3  | Quy trình xin nghỉ phép như thế nào?                           | in-scope     | PASS | Yes       | N/A        | None   |
| 4  | Thâm niên 6 năm thì được bao nhiêu ngày phép?              | in-scope     | PASS | Yes       | N/A        | None   |
| 5  | Nhân viên thử việc có được phụ cấp điện thoại khôn...  | in-scope     | PASS | Yes       | N/A        | None   |
| 6  | Công ty có hỗ trợ học MBA không?                               | in-scope     | PASS | Yes       | N/A        | None   |
| 7  | Nghỉ ốm quá 30 ngày thì lương như thế nào?                 | in-scope     | PASS | Yes       | N/A        | None   |
| 8  | Tôi đã làm 3 năm muốn nghỉ việc thì phép dư có đượ... | in-scope     | PASS | Yes       | N/A        | None   |
| 9  | Chính sách của công ty có tốt không?                          | ambiguous    | FAIL | Yes       | N/A        | None   |
| 10 | Tôi nghỉ 1 ngày thì được hưởng lương không?              | ambiguous    | FAIL | Yes       | N/A        | None   |
| 11 | Chính sách bảo hiểm xã hội của công ty như thế nào...     | out-of-scope | PASS | No        | N/A        | None   |
| 12 | Tôi muốn xin chuyển công tác sang Hà Nội thì làm s...       | out-of-scope | PASS | No        | N/A        | None   |
| 13 | Theo chính sách Viettel Network nhân viên chính th...           | in-scope     | PASS | Yes       | N/A        | None   |
| 14 | Theo chính sách Viettel Network nghỉ ốm quá 30 ngà...          | in-scope     | PASS | Yes       | N/A        | None   |
| 15 | Theo chính sách Viettel Network nhân viên thử việc...          | in-scope     | PASS | Yes       | N/A        | None   |
| 16 | Theo chính sách Viettel Network nhân viên thâm niê...          | in-scope     | PASS | Yes       | N/A        | None   |
| 17 | Theo chính sách Viettel Network công ty có hỗ trợ ...          | in-scope     | PASS | Yes       | N/A        | None   |
| 18 | Theo Bộ luật Lao động 2019 người làm việc đủ 12 th...      | in-scope     | FAIL | Yes       | N/A        | None   |
| 19 | Theo Bộ luật Lao động 2019 thời gian thử việc tối ...        | in-scope     | FAIL | Yes       | N/A        | None   |
| 20 | Theo Bộ luật Lao động 2019 nữ lao động nghỉ thai s...        | in-scope     | FAIL | Yes       | N/A        | None   |
| 21 | Theo luật nghỉ ốm hưởng bảo hiểm xã hội bao nhiêu ...      | in-scope     | FAIL | Yes       | N/A        | None   |
| 22 | Theo Bộ luật Lao động nghỉ phép năm được hưởng bao...    | in-scope     | FAIL | Yes       | N/A        | None   |
| 23 | Viettel Network có chính sách cho vay mua nhà khôn...           | out-of-scope | PASS | No        | N/A        | None   |
| 24 | Tôi muốn xin chuyển công tác sang Hà Nội thì làm s...       | out-of-scope | PASS | No        | N/A        | None   |

## 3. Phân tích chi tiết (Detailed Breakdown)

### Q1: Nhân viên chính thức được bao nhiêu ngày phép năm?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

### Q2: Mức phụ cấp ăn trưa là bao nhiêu?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

- "# Chính sách phụ cấp ăn trưa, đi lại và điện thoại

*(Tài liệu mô phỏng — không phải chính sách thật..." → match=exact overlap=100%

- "### 2.1 Mức thưởng

| Thâm niên | Mức thưởng                       | Thời điểm chi trả |
| ----------- | ----------------------------------- | --------------------- |
| 5 năm      | 1 t..." → match=exact overlap=100% |                       |

### Q3: Quy trình xin nghỉ phép như thế nào?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Thời gian nghỉ
- Thai sản thông thường: 6 tháng.
- Sinh đôi trở lên: thêm 1 tháng cho mỗi b..." → match=exact overlap=100%

### Q4: Thâm niên 6 năm thì được bao nhiêu ngày phép?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

- "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

### Q5: Nhân viên thử việc có được phụ cấp điện thoại không?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 3.1 Mức phụ cấp

| Cấp bậc                 |                      Mức/tháng | Ghi chú |
| ------------------------- | -------------------------------: | -------- |
| Trưởng phòng trở lên | ..." → match=exact overlap=100% |          |

- "# Chính sách phụ cấp ăn trưa, đi lại và điện thoại

*(Tài liệu mô phỏng — không phải chính sách thật..." → match=exact overlap=100%

- "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

### Q6: Công ty có hỗ trợ học MBA không?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 4.1 Hỗ trợ học MBA, thạc sĩ
- Công ty xem xét tài trợ một phần học phí cho chương trình MBA hoặ..." → match=exact overlap=100%

  - "### 2.1 Bước thực hiện

1. Nhân viên gửi yêu cầu đào tạo qua hệ thống nội bộ trước ít nhất 14 ngày.
   ..." → match=exact overlap=100%

- "### 1.1 Ngân sách hàng năm
- Mỗi nhân viên chính thức được ngân sách đào tạo: 5.000.000 VNĐ/năm.
- ..." → match=exact overlap=100%

### Q7: Nghỉ ốm quá 30 ngày thì lương như thế nào?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Thời gian nghỉ
- Thai sản thông thường: 6 tháng.
- Sinh đôi trở lên: thêm 1 tháng cho mỗi b..." → match=exact overlap=100%

  - "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

### Q8: Tôi đã làm 3 năm muốn nghỉ việc thì phép dư có được quy đổi tiền không?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

### Q9: Chính sách của công ty có tốt không?

- **Phân loại**: ambiguous
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 4.1 Hỗ trợ học MBA, thạc sĩ
- Công ty xem xét tài trợ một phần học phí cho chương trình MBA hoặ..." → match=exact overlap=100%

  - "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Cam kết làm việc

Khi công ty tài trợ khóa đào tạo chi phí trên 10.000.000 VNĐ hoặc bằng cấp..." → match=exact overlap=100%

### Q10: Tôi nghỉ 1 ngày thì được hưởng lương không?

- **Phân loại**: ambiguous
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Thời gian nghỉ
- Thai sản thông thường: 6 tháng.
- Sinh đôi trở lên: thêm 1 tháng cho mỗi b..." → match=exact overlap=100%

  - "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

### Q11: Chính sách bảo hiểm xã hội của công ty như thế nào?

- **Phân loại**: out-of-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Không
- **Có trích dẫn**: Không
- **Trích dẫn hợp lệ**: Không
- **Hallucination check**: PASS
- **Từ chối đúng**: Có

### Q12: Tôi muốn xin chuyển công tác sang Hà Nội thì làm sao?

- **Phân loại**: out-of-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Không
- **Có trích dẫn**: Không
- **Trích dẫn hợp lệ**: Không
- **Hallucination check**: PASS
- **Từ chối đúng**: Có

### Q13: Theo chính sách Viettel Network nhân viên chính thức được bao nhiêu ngày phép năm theo thâm niên?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

- "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

### Q14: Theo chính sách Viettel Network nghỉ ốm quá 30 ngày thì lương tính thế nào?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 3.1 Thời gian nghỉ
- Thai sản thông thường: 6 tháng.
- Sinh đôi trở lên: thêm 1 tháng cho mỗi b..." → match=exact overlap=100%

  - "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

### Q15: Theo chính sách Viettel Network nhân viên thử việc có được phụ cấp điện thoại không?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 3.1 Mức phụ cấp

| Cấp bậc                 |                      Mức/tháng | Ghi chú |
| ------------------------- | -------------------------------: | -------- |
| Trưởng phòng trở lên | ..." → match=exact overlap=100% |          |

- "# Chính sách phụ cấp ăn trưa, đi lại và điện thoại

*(Tài liệu mô phỏng — không phải chính sách thật..." → match=exact overlap=100%

- "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

### Q16: Theo chính sách Viettel Network nhân viên thâm niên 6 năm được bao nhiêu ngày phép?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

- "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

### Q17: Theo chính sách Viettel Network công ty có hỗ trợ học MBA không?

- **Phân loại**: in-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Có
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 4.1 Hỗ trợ học MBA, thạc sĩ
- Công ty xem xét tài trợ một phần học phí cho chương trình MBA hoặ..." → match=exact overlap=100%

  - "### 2.1 Bước thực hiện

1. Nhân viên gửi yêu cầu đào tạo qua hệ thống nội bộ trước ít nhất 14 ngày.
   ..." → match=exact overlap=100%

- "### 1.1 Ngân sách hàng năm
- Mỗi nhân viên chính thức được ngân sách đào tạo: 5.000.000 VNĐ/năm.
- ..." → match=exact overlap=100%

### Q18: Theo Bộ luật Lao động 2019 người làm việc đủ 12 tháng được nghỉ phép năm bao nhiêu ngày?

- **Phân loại**: in-scope
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 2.1 Mức thưởng

| Thâm niên | Mức thưởng                       | Thời điểm chi trả |
| ----------- | ----------------------------------- | --------------------- |
| 5 năm      | 1 t..." → match=exact overlap=100% |                       |

- "### 3.1 Nghỉ phép thêm

Nhân viên ở bậc thâm niên 3 trở lên (5 năm+) được thêm ngày phép:

| Thâm ni..." → match=exact overlap=100%

### Q19: Theo Bộ luật Lao động 2019 thời gian thử việc tối đa cho lao động có bằng đại học là bao lâu?

- **Phân loại**: in-scope
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 2.1 Mức thưởng

| Thâm niên | Mức thưởng                       | Thời điểm chi trả |
| ----------- | ----------------------------------- | --------------------- |
| 5 năm      | 1 t..." → match=exact overlap=100% |                       |

- "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

- "### 4.1 Hỗ trợ học MBA, thạc sĩ
- Công ty xem xét tài trợ một phần học phí cho chương trình MBA hoặ..." → match=exact overlap=100%

### Q20: Theo Bộ luật Lao động 2019 nữ lao động nghỉ thai sản được bao nhiêu tháng?

- **Phân loại**: in-scope
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

- "### 2.1 Mức thưởng

| Thâm niên | Mức thưởng                       | Thời điểm chi trả |
| ----------- | ----------------------------------- | --------------------- |
| 5 năm      | 1 t..." → match=exact overlap=100% |                       |

- "### 3.1 Thời gian nghỉ
- Thai sản thông thường: 6 tháng.
- Sinh đôi trở lên: thêm 1 tháng cho mỗi b..." → match=exact overlap=100%

### Q21: Theo luật nghỉ ốm hưởng bảo hiểm xã hội bao nhiêu phần trăm lương?

- **Phân loại**: in-scope
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:

  - "### 2.1 Điều kiện
- Nghỉ ốm hưởng nguyên lương trong 30 ngày đầu mỗi năm.
- Từ ngày thứ 31 trở đi h..." → match=exact overlap=100%

  - "### 1.1 Mức phụ cấp

| Đối tượng                                             | Mức/ngày | Ghi chú |
| --------------------------------------------------------- | ---------: | -------- |
| Nhân viên chính thức ..." → match=exact overlap=100% |            |          |

- "### 5.1 Buổi chia sẻ kiến thức
- Mỗi bộ phận tổ chức ít nhất 1 buổi chia sẻ kiến thức hàng quý.
- D..." → match=exact overlap=100%

### Q22: Theo Bộ luật Lao động nghỉ phép năm được hưởng bao nhiêu phần trăm lương?

- **Phân loại**: in-scope
- **Kết quả**: FAIL
- **Đáp án đúng**: Không
- **Có trích dẫn**: Có
- **Trích dẫn hợp lệ**: Có
- **Hallucination check**: PASS
- **Từ chối đúng**: Không
- **Chi tiết trích dẫn**:
  - "### 2.1 Mức thưởng

| Thâm niên | Mức thưởng                       | Thời điểm chi trả |
| ----------- | ----------------------------------- | --------------------- |
| 5 năm      | 1 t..." → match=exact overlap=100% |                       |

- "### 1.1 Số ngày phép

Nhân viên chính thức được hưởng ngày phép năm theo thâm niên:

| Thâm niên | S..." → match=exact overlap=100%

- "### 1.1 Phân loại

| Bậc   | Thâm niên | Mô tả                                         |
| ------ | ----------- | ----------------------------------------------- |
| Bậc 1 | 1-3 năm    | Mới gia nhập ..." → match=exact overlap=100% |

### Q23: Viettel Network có chính sách cho vay mua nhà không?

- **Phân loại**: out-of-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Không
- **Có trích dẫn**: Không
- **Trích dẫn hợp lệ**: Không
- **Hallucination check**: PASS
- **Từ chối đúng**: Có

### Q24: Tôi muốn xin chuyển công tác sang Hà Nội thì làm sao?

- **Phân loại**: out-of-scope
- **Kết quả**: PASS
- **Đáp án đúng**: Không
- **Có trích dẫn**: Không
- **Trích dẫn hợp lệ**: Không
- **Hallucination check**: PASS
- **Từ chối đúng**: Có
