# Use Case Chi Tiết: NetSaveAI — Chatbot RAG cho Vận Hành Mạng Viễn Thông

---

## 1. Bối Cảnh & Vấn Đề

### Môi trường thực tế

Một nhà mạng viễn thông (Viettel, VNPT, MobiFone...) vận hành hàng trăm thiết bị mạng lõi:

- **PS Core**: GGSN, SGSN, MME, vEPC
- **IP/Transport**: BRAS, Router lõi, MPLS
- **VAS/IT**: AAA, DNS, SMSC, HSS, PCRF

### Vấn đề tồn tại

```
Kỹ sư trực đêm nhận alert: "Node GGHL14 có dấu hiệu lỗi"
  ↓
Phải tìm trong hàng trăm file Excel/PDF/Word:
  - PA (Physical Architecture) — cấu trúc node
  - MOP (Method of Procedure) — quy trình thao tác
  - Checklist vận hành
  - Hướng dẫn xử lý sự cố
  ↓
Mất 15–30 phút chỉ để tìm đúng file + đúng sheet + đúng bước
  ↓
Áp lực cao, dễ sai sót → ảnh hưởng hàng triệu thuê bao
```

**Tài liệu đặc thù của ngành:**

- Cực kỳ chuyên biệt: tên node, lệnh CLI, IP address nội bộ
- Cập nhật thường xuyên theo mỗi đợt nâng cấp
- Không thể dùng ChatGPT thông thường vì dữ liệu **nội bộ, bảo mật**

---

## 2. Actors (Người Dùng)

| Actor | Vai Trò | Nhu Cầu Chính |
|---|---|---|
| **Kỹ sư trực vận hành** | Xử lý sự cố 24/7 | Tìm quy trình nhanh, chính xác, không sai bước |
| **Kỹ sư thực hiện thay đổi** | Cutover, nâng cấp, bảo trì | Đọc đúng MOP, đúng lệnh, đúng thứ tự |
| **Trưởng ca / Giám sát** | Review quy trình trước khi thực hiện | Xác nhận nhanh các bước quan trọng |
| **Kỹ sư mới** | Học việc, chưa quen tài liệu | Hỏi được câu hỏi cơ bản mà không mất thời gian mentor |
| **Admin hệ thống** | Quản lý tài liệu, cấu hình RAG | Upload tài liệu mới, cấu hình routing |

---

## 3. Use Cases Chính

---

### UC-01: Hỏi Quy Trình Cô Lập Node

**Tình huống:** Node GGHL14 (GGSN) có nguy cơ sập, cần cô lập khỏi mạng trước khi xử lý.

```
Kỹ sư gõ: "Quy trình cô lập dịch vụ 4G của node SGHL04"
```

**Luồng hệ thống:**

```
1. Query Analyzer phát hiện:
   - node_type = GGSN
   - scenario  = co_lap
   - node_name = SGHL04
   - service   = 4G  ← must_contain = ["dịch vụ 4G"]

2. Routing: GGSN × co_lap → PA_GGSN_UCTT.xlsx

3. Hybrid Search trong PA_GGSN_UCTT.xlsx:
   - BM25 match: "dịch vụ 4G", "SGHL04", "cô lập"
   - FAISS match: ngữ nghĩa gần với "isolation procedure"
   - Filter: must_contain "dịch vụ 4G" → loại row 3G

4. Trả về: Hàng 21 (SGHL04 4G) với điểm cao nhất
           KHÔNG trả về hàng 38 (SGHL04 3G)

5. LLM tổng hợp: liệt kê đúng thứ tự các bước cô lập
```

**Kết quả trả về cho kỹ sư:**

```
Quy trình cô lập dịch vụ 4G node SGHL04:
1. Đăng nhập vào SGHL04: ssh admin@10.60.107.8
2. Kiểm tra trạng thái hiện tại: show service 4G status
3. Drain traffic: set service 4G drain enable
4. Xác nhận traffic = 0: watch -n5 show counters 4G
5. Isolate: set node SGHL04 service 4G out-of-service
6. Notify NOC: gửi ticket #INC-XXXX

Nguồn: PA_GGSN_UCTT.xlsx, sheet "Cô Lập", hàng 21 (độ liên quan: 0.89)
⬇️ Tải xuống: PA_GGSN_UCTT.xlsx
```

---

### UC-02: Hỏi Quy Trình Cutover

**Tình huống:** Bảo trì định kỳ, cần chuyển traffic từ BRAS PEKH01 sang PEKH02.

```
Kỹ sư gõ: "Cắt chuyển traffic BRAS PEKH01 sang PEKH02"
```

**Điểm đặc biệt:** Cutover có thứ tự bước rất nghiêm ngặt — sai thứ tự → outage.

**Hệ thống đảm bảo:**

- System prompt yêu cầu LLM *"liệt kê ĐÚNG THỨ TỰ như trong tài liệu"*
- *"Dùng ĐÚNG lệnh có trong tài liệu, KHÔNG tự thay bằng lệnh tương đương"*
- *"KHÔNG tự thêm bước không có trong tài liệu"*

---

### UC-03: Hỏi Kiến Thức Tổng Quát

**Tình huống:** Kỹ sư mới muốn hiểu cấu trúc.

```
Kỹ sư gõ: "Các node GGSN hiện tại đang phục vụ những dịch vụ gì?"
```

**Luồng:** Không có scenario cụ thể → search toàn bộ KB → tổng hợp từ nhiều chunk.

---

### UC-04: Upload Tài Liệu Mới (Admin)

**Tình huống:** Sau đợt nâng cấp, PA được cập nhật.

```
Admin thực hiện:
1. Tab 📁 Tài Liệu → Upload PA_GGSN_v2.xlsx
2. Chọn Profile: PA_GGSN_Profile
3. Lập chỉ mục → ~30 giây
4. Vector store cập nhật tự động
5. Chat ngay lập tức phản ánh tài liệu mới
```

> **Không cần:** restart app, không cần developer.

---

### UC-05: Debug Khi Kết Quả Sai (Admin/Senior)

**Tình huống:** Chatbot trả lời sai, cần tìm nguyên nhân.

```
Admin vào Tab 🔍 Debug:
- Nhập lại câu hỏi
- Xem:  node_type=[GGSN]              ✅
        scenario=[co_lap]             ✅
        source_files=[PA_GGSN.xlsx]   ✅
        must_contain=["dịch vụ 4G"]   ✅
        Retrieved chunks: hàng 21 score=0.89 ✅

→ Kết quả đúng. Vấn đề có thể do LLM tóm tắt sai
→ Điều chỉnh system_prompt
```

---

## 4. Luồng Tổng Thể (End-to-End)

```
┌─────────────────────────────────────────────────────────┐
│                    THỜI GIAN CHUẨN BỊ                   │
│                                                         │
│  Admin upload tài liệu (PA/MOP/Checklist)               │
│         ↓                                               │
│  Cấu hình: Node Types, Scenarios, Routing, Profile      │
│         ↓                                               │
│  Vector Store sẵn sàng                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    THỜI GIAN VẬN HÀNH                   │
│                                                         │
│  Kỹ sư đặt câu hỏi bằng ngôn ngữ tự nhiên (tiếng Việt) │
│         ↓                                               │
│  Hệ thống tự hiểu: node nào, thao tác gì, loại gì      │
│         ↓                                               │
│  Tìm đúng tài liệu, đúng hàng, đúng quy trình          │
│         ↓                                               │
│  LLM trình bày rõ ràng, có nguồn, có nút download      │
│         ↓                                               │
│  Kỹ sư thực hiện đúng, nhanh, an toàn                  │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Giá Trị Mang Lại

| Chỉ Số | Trước | Sau |
|---|---|---|
| Thời gian tìm tài liệu | 15–30 phút | **< 30 giây** |
| Rủi ro sai quy trình | Cao (tìm nhầm file/sheet) | **Thấp** (trích dẫn chính xác đến hàng) |
| Onboarding kỹ sư mới | 3–6 tháng học tài liệu | **Hỏi trực tiếp được ngay** |
| Cập nhật tài liệu | Dev phải re-index thủ công | **Admin tự upload, tự động** |
| Bảo mật dữ liệu | Phụ thuộc ChatGPT bên ngoài | **Chạy hoàn toàn nội bộ, offline** |

---

## 6. Điểm Khác Biệt So Với RAG Thông Thường

| Vấn Đề Đặc Thù | Giải Pháp Trong NetSaveAI |
|---|---|
| Nhiều node cùng tên prefix (SGHL04 có cả 4G và 3G) | `must_contain` filter theo loại dịch vụ |
| Tên node viết tắt chuyên biệt (GGHL14, PEKH01) | Regex pattern nhận diện tên node + name_prefix matching |
| 1 file Excel có nhiều loại node | Profile YAML + key_columns để phân biệt |
| Câu hỏi tiếng Việt có dấu → BM25 kém | Synonym expansion ("cô lập" → "isolate tách loại khỏi") |
| Tài liệu nội bộ tuyệt mật | Chạy hoàn toàn offline, không gửi data ra ngoài |
