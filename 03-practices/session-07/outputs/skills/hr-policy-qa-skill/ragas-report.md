# RAGAS Report — Session 07 Lab D2 (GV demo)

> **Mục đích:** GV show cho HV kết quả RAGAS (industry-standard RAG metrics) để đối chiếu với SLI/SLO custom. **HV không tự chạy** (tiết kiệm thời gian + token LLM-judge).

## Thông số chạy
- **LLM-judge:** GLM `glm-4.5-air` (z.ai, OpenAI-compatible)
- **Embeddings:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Dataset:** 4 câu đại diện (in-scope direct + cross-ref + out-of-scope) từ `answers-glm.json`; `contexts` = citation quotes thật.
- **Run:** `max_workers=1` (GLM latency 120–160s/call), 16/16 step, ~32 phút, 1 job TimeoutError → NaN.

## Kết quả 4 metric

| Metric | Score | Đo gì | Đọc kết quả |
|---|---:|---|---|
| **Faithfulness** | 0.61 | Câu trả lời có bịa ngoài context không | 61% câu trả lời trung thành với context — còn ~39% mang thông tin ngoài context (hallucination nhẹ) |
| **Answer Relevancy** | 0.55 | Câu trả lời có sát câu hỏi không | 55% — một số câu trả lời lan man / thừa thông tin |
| **Context Precision** | 0.38 | Top-k context có chứa đoạn cần không | 38% — retrieval thỉnh thoảng đưa chunk không liên quan lên top |
| **Context Recall** | 0.33 | Có thiếu context cần không | 33% — retrieval còn bỏ sót đoạn cần thiết cho đáp án |

## Đối chiếu RAGAS vs SLI/SLO custom (Lab D1)

| Khía cạnh | SLI/SLO custom | RAGAS |
|---|---|---|
| Citation rate | 100% ✅ | — |
| Cross-check verbatim | 90.9% ✅ | faithfulness 0.61 (bắt hallucination tinh hơn) |
| Accuracy (source match) | 100% ✅ | context_recall 0.33 (retrieval còn hụt) |
| Phù hợp enterprise deterministic | ✅ | ◐ (LLM-judge, tốn token) |

**Kết luận:** SLI/SLO custom đo đúng nhu cầu doanh nghiệp (citation, refusal, verbatim). RAGAS **bổ sung** góc nhìn industry-standard: phát hiện retrieval còn yếu (context_precision/recall thấp) — gợi ý cải thiện retriever (Lab A hybrid + RRF đã partially giải quyết). Nên chạy cả hai; RAGAS cho GV demo, SLI cho HV thực hành.

## Reproduce (GV only)
```bash
python3 -m venv ragas-venv && source ragas-venv/bin/activate
pip install ragas langchain-huggingface sentence-transformers
# stub langchain_community.chat_models.vertexai nếu ragas 0.4.x import lỗi
export GLM_API_KEY=<key>
python run_ragas.py  # ~30+ phút, GLM judge chậm
```
