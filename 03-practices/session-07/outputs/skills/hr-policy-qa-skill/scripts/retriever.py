#!/usr/bin/env python3
"""
retriever.py — Hybrid Retrieval Tool for HR Policy Agentic RAG (Lab A hoàn chỉnh).

Hybrid thật sự: vector (ChromaDB, nghĩa) + BM25 (SQLite-FTS5, từ khóa), ghép bằng
RRF (Reciprocal Rank Fusion). Fallback tự động:
  - ChromaDB thiếu        -> chỉ BM25
  - SQLite-FTS5 tắt       -> rank_bm25 (thuần Python)
  - Cả hai rỗng            -> refused

Supports Vietnamese text.

Usage:
    python retriever.py --query "Quy định nghỉ phép năm?" --top-k 3
    python retriever.py --query "Chính sách OT" --chunks ./kb/chunks.json
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Optional, Union


# ---------------------------------------------------------------------------
# Optional dependency guards
# ---------------------------------------------------------------------------

try:
    import chromadb

    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False

try:
    from sentence_transformers import SentenceTransformer

    _MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    _EMBEDDING_MODEL = SentenceTransformer(_MODEL_NAME)
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    _EMBEDDING_MODEL = None

# rank_bm25: fallback thuần Python khi SQLite-FTS5 không bật
try:
    from rank_bm25 import BM25Okapi

    HAS_RANK_BM25 = True
except ImportError:
    HAS_RANK_BM25 = False


def _fts5_available() -> bool:
    """Kiểm tra build SQLite hiện tại có bật FTS5 không."""
    try:
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
        conn.close()
        return True
    except sqlite3.OperationalError:
        return False


HAS_FTS5 = _fts5_available()


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Score normalisation ranges
VECTOR_SCORE_MIN = 0.3
VECTOR_SCORE_MAX = 0.8
KEYWORD_SCORE_MIN = 0.0
KEYWORD_SCORE_MAX = 0.5

# Refusal thresholds
VECTOR_REFUSAL_THRESHOLD = 0.3
KEYWORD_REFUSAL_THRESHOLD = 0.01

# RRF (Reciprocal Rank Fusion) — Lab A bước A2
RRF_K = 60  # hằng số chuẩn, k≈60 (Cormack et al., 2009)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalise_vector_score(distance: float) -> float:
    """Normalise ChromaDB distance to a 0.3-0.8 relevance score.

    Formula: 1 / (1 + distance), clamped to [0.3, 0.8].
    """
    raw = 1.0 / (1.0 + distance)
    return max(VECTOR_SCORE_MIN, min(VECTOR_SCORE_MAX, raw))


def _normalise_keyword_score(raw: float) -> float:
    """Clamp keyword TF-IDF score to [0.0, 0.5]."""
    return max(KEYWORD_SCORE_MIN, min(KEYWORD_SCORE_MAX, raw))


def _embed_query(query: str) -> Optional[list[float]]:
    """Generate embedding for a single query string."""
    if _EMBEDDING_MODEL is None:
        return None
    return _EMBEDDING_MODEL.encode([query], show_progress_bar=False)[0].tolist()


def _load_chunks_from_file(path: str) -> list[dict[str, Any]]:
    """Load chunks from a JSON file produced by chunker.py."""
    p = Path(path).resolve()
    if not p.exists():
        # Fallback to look relative to this script: ../kb/chunks.json
        script_dir = Path(__file__).resolve().parent
        alt_path = (script_dir / ".." / "kb" / "chunks.json").resolve()
        if alt_path.exists():
            p = alt_path
        else:
            print(f"[retriever] Chunks file not found: {path}")
            return []
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Vector search
# ---------------------------------------------------------------------------

def vector_search(
    query: str,
    collection=None,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Search ChromaDB collection using vector similarity.

    Returns list of result dicts: {chunk_id, content, metadata, score, method}.
    Returns empty list if ChromaDB or embeddings unavailable.
    """
    if not HAS_CHROMADB or collection is None:
        return []

    query_embedding = _embed_query(query)
    if query_embedding is None:
        return []

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
    except Exception as exc:
        print(f"[retriever] Vector search error: {exc}")
        return []

    if not results or not results.get("documents"):
        return []

    formatted: list[dict[str, Any]] = []
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(documents, metadatas, distances):
        score = _normalise_vector_score(dist)
        # Apply refusal threshold
        if score < VECTOR_REFUSAL_THRESHOLD:
            continue
        formatted.append({
            "chunk_id": meta.get("chunk_id", "unknown"),
            "content": doc,
            "metadata": meta,
            "score": score,
            "method": "vector",
        })

    return formatted


# ---------------------------------------------------------------------------
# Keyword search (TF-IDF fallback)
# ---------------------------------------------------------------------------

def _simple_tfidf(query: str, document: str) -> float:
    """Compute a simple TF-IDF-like score between query and document.

    Uses word overlap with inverse document frequency weighting.
    No external library required.
    """
    # Tokenise (simple whitespace + lower, works for Vietnamese)
    query_terms = set(query.lower().split())
    doc_terms = document.lower().split()

    if not doc_terms or not query_terms:
        return 0.0

    doc_len = len(doc_terms)
    score = 0.0

    for term in query_terms:
        tf = doc_terms.count(term) / doc_len
        # IDF approximation: boost rare terms slightly
        if tf > 0:
            score += tf * (1.0 / (1.0 + tf))

    return score


def keyword_search(
    query: str,
    chunks_data: list[dict[str, Any]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Keyword-based search using simple TF-IDF matching.

    Returns list of result dicts: {chunk_id, content, metadata, score, method}.
    """
    if not chunks_data:
        return []

    scored: list[tuple[float, dict[str, Any]]] = []

    for chunk in chunks_data:
        content = chunk.get("content", "")
        raw_score = _simple_tfidf(query, content)
        score = _normalise_keyword_score(raw_score)

        if score >= KEYWORD_REFUSAL_THRESHOLD:
            scored.append((score, chunk))

    # Sort descending by score
    scored.sort(key=lambda x: x[0], reverse=True)

    results: list[dict[str, Any]] = []
    for score, chunk in scored[:top_k]:
        results.append({
            "chunk_id": chunk.get("chunk_id", "unknown"),
            "content": chunk.get("content", ""),
            "metadata": {
                k: v
                for k, v in chunk.items()
                if k not in ("content",)
            },
            "score": round(score, 4),
            "method": "keyword",
        })

    return results


# ---------------------------------------------------------------------------
# BM25 search (SQLite-FTS5, fallback rank_bm25) — Lab A bước A1
# ---------------------------------------------------------------------------

_FTS_CACHE: dict[str, tuple] = {}  # db_path -> (conn,) | (bm25_index, chunk_ids)


def _tokenize(text: str) -> list[str]:
    """Tokenizer nhẹ cho tiếng Việt: giữ chữ/ số/ dấu, bỏ dấu câu."""
    return re.findall(r"[0-9A-Za-zÀ-ỹ]+", text.lower())


def _fts_match_query(query: str) -> str:
    """Chuyển query tự do sang cú pháp FTS5 MATCH an toàn (token OR token)."""
    tokens = _tokenize(query)
    if not tokens:
        return ""
    return " OR ".join(tokens)


def build_fts_index(chunks: list[dict[str, Any]], db_path: str = "kb/fts5.db"):
    """Tạo index BM25 từ chunks.

    Ưu tiên SQLite-FTS5 (built-in, nhanh). Nếu build SQLite không bật FTS5
    -> fallback `rank_bm25` (BM25Okapi, thuần Python). Trả về một "index handle"
    mà `bm25_search` biết cách dùng: (conn, "fts5") hoặc (bm25, "rank_bm25").
    """
    if db_path in _FTS_CACHE:
        return _FTS_CACHE[db_path]

    # Đảm bảo thư mục cha tồn tại
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    if HAS_FTS5:
        conn = sqlite3.connect(db_path)
        conn.execute("DROP TABLE IF EXISTS policy_fts")
        conn.execute(
            "CREATE VIRTUAL TABLE policy_fts USING fts5"
            "(content, doc_id UNINDEXED, section UNINDEXED, chunk_id UNINDEXED)"
        )
        for c in chunks:
            conn.execute(
                "INSERT INTO policy_fts(content, doc_id, section, chunk_id) VALUES (?,?,?,?)",
                (c.get("content", ""), c.get("doc_id", ""), c.get("section", ""), c.get("chunk_id", "")),
            )
        conn.commit()
        handle = (conn, "fts5")
    elif HAS_RANK_BM25:
        corpus_tokens = [_tokenize(c.get("content", "")) for c in chunks]
        bm25 = BM25Okapi(corpus_tokens)
        handle = (bm25, "rank_bm25", chunks)
    else:
        # Fallback cuối: TF-IDF (dùng keyword_search)
        handle = (None, "none")

    _FTS_CACHE[db_path] = handle
    return handle


def bm25_search(index_handle, query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Tìm top-k chunk theo BM25. `index_handle` từ `build_fts_index`.

    bm25() của SQLite trả score (càng âm càng liên quan) -> ta giữ nguyên để sort,
    rồi chuẩn hóa về [0,1] theo rank để RRF dùng.
    """
    if index_handle is None:
        return []
    backend = index_handle[1]

    if backend == "fts5":
        conn = index_handle[0]
        match = _fts_match_query(query)
        if not match:
            return []
        rows = conn.execute(
            "SELECT chunk_id, doc_id, section, content, bm25(policy_fts) AS score "
            "FROM policy_fts WHERE policy_fts MATCH ? ORDER BY score LIMIT ?",
            (match, top_k),
        ).fetchall()
        ranked = [
            {"chunk_id": r[0], "doc_id": r[1], "section": r[2], "content": r[3], "_raw": r[4]}
            for r in rows
        ]
    elif backend == "rank_bm25":
        bm25, chunks = index_handle[0], index_handle[2]
        scores = bm25.get_scores(_tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]
        ranked = [
            {
                "chunk_id": chunks[i].get("chunk_id", ""),
                "doc_id": chunks[i].get("doc_id", ""),
                "section": chunks[i].get("section", ""),
                "content": chunks[i].get("content", ""),
                "_raw": float(scores[i]),
            }
            for i in order
            if scores[i] > 0
        ]
    else:
        return []

    # Chuẩn hóa score về [0,1] theo rank (rank 1 = 1.0) — chỉ để hiển thị/báo cáo
    for rank, hit in enumerate(ranked, start=1):
        hit["bm25_rank"] = rank
        hit["bm25_score"] = round(1.0 / rank, 4)
    return ranked


# ---------------------------------------------------------------------------
# RRF (Reciprocal Rank Fusion) — Lab A bước A2
# ---------------------------------------------------------------------------

def rrf_fuse(
    vector_hits: list[dict[str, Any]],
    bm25_hits: list[dict[str, Any]],
    k: int = RRF_K,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Ghép 2 ranked list bằng RRF — không cần chuẩn hóa điểm giữa 2 hệ.

    score(d) = Σ 1 / (k + rank_i(d))
    """
    scores: dict[str, float] = {}
    payload: dict[str, dict[str, Any]] = {}

    def _norm(hit: dict[str, Any]) -> dict[str, Any]:
        """Chuẩn hóa hit (vector có nested metadata, bm25 flat) về cùng dạng flat."""
        meta = hit.get("metadata", {})
        return {
            "chunk_id": hit.get("chunk_id") or meta.get("chunk_id", ""),
            "doc_id": hit.get("doc_id") or meta.get("doc_id", ""),
            "section": hit.get("section") or meta.get("section", ""),
            "content": hit.get("content", ""),
        }

    for rank, hit in enumerate(vector_hits, start=1):
        cid = _norm(hit)["chunk_id"]
        if not cid:
            continue
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
        payload.setdefault(cid, _norm(hit))

    for rank, hit in enumerate(bm25_hits, start=1):
        cid = _norm(hit)["chunk_id"]
        if not cid:
            continue
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
        payload.setdefault(cid, _norm(hit))

    ordered = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    fused: list[dict[str, Any]] = []
    for cid, score in ordered:
        item = dict(payload[cid])
        item["chunk_id"] = cid
        item["score"] = round(score, 4)
        item["rrf_score"] = round(score, 4)
        fused.append(item)
    return fused


# ---------------------------------------------------------------------------
# Main retrieval function — HYBRID (vector + BM25 -> RRF)
# ---------------------------------------------------------------------------

def retrieve_chunks(
    query: str,
    top_k: int = 3,
    chroma_collection=None,
    chunks_data: Optional[list[dict[str, Any]]] = None,
    fts_db_path: str = "kb/fts5.db",
) -> dict[str, Any]:
    """Hybrid retrieval thật: vector (nghĩa) + BM25 (từ khóa) -> RRF.

    Chiến lược:
      1. vector_search (ChromaDB) nếu có collection.
      2. bm25_search (FTS5 / rank_bm25) nếu có chunks_data.
      3. RRF fuse 2 ranked list -> top_k.
      4. Nếu chỉ 1 phía có kết quả -> dùng suất đó (vector-only hoặc bm25-only).
      5. Nếu cả hai rỗng -> refused.

    Returns dict: results, method ("hybrid"|"vector"|"bm25"|"none"),
                  refused, query.
    """
    vector_hits = vector_search(query, chroma_collection, top_k) if chroma_collection is not None else []
    bm25_hits = []
    if chunks_data:
        index_handle = build_fts_index(chunks_data, fts_db_path)
        if index_handle[1] == "none":
            # FTS5 + rank_bm25 đều thiếu -> dùng keyword TF-IDF cũ
            bm25_hits = keyword_search(query, chunks_data, top_k)
        else:
            bm25_hits = bm25_search(index_handle, query, top_k)

    # RRF fuse khi CẢ hai phía đều có kết quả
    if vector_hits and bm25_hits:
        fused = rrf_fuse(vector_hits, bm25_hits, k=RRF_K, top_k=top_k)
        # chuẩn hóa định dạng kết quả
        results = []
        for r in fused:
            meta = {k: v for k, v in r.items() if k not in ("content", "_raw", "score", "rrf_score")}
            results.append({
                "chunk_id": r.get("chunk_id", "unknown"),
                "content": r.get("content", ""),
                "metadata": meta,
                "score": r.get("rrf_score", 0),
                "method": "hybrid",
            })
        return {"results": results, "method": "hybrid", "refused": False, "query": query}

    # Chỉ vector
    if vector_hits:
        return {"results": vector_hits, "method": "vector", "refused": False, "query": query}

    # Chỉ BM25
    if bm25_hits:
        results = []
        for r in bm25_hits:
            meta = {k: v for k, v in r.items() if k not in ("content", "_raw", "score", "bm25_score", "bm25_rank")}
            results.append({
                "chunk_id": r.get("chunk_id", "unknown"),
                "content": r.get("content", ""),
                "metadata": meta,
                "score": r.get("bm25_score", 0),
                "method": "bm25",
            })
        return {"results": results, "method": "bm25", "refused": False, "query": query}

    # Cả hai rỗng -> refused
    return {"results": [], "method": "none", "refused": True, "query": query}


# ---------------------------------------------------------------------------
# Formatting for Agent consumption
# ---------------------------------------------------------------------------

def format_retrieval_results(retrieval: dict[str, Any]) -> str:
    """Format retrieval results into a clean string for Agent context.

    Includes method, chunk count, and each chunk with its score.
    """
    method = retrieval.get("method", "none")
    refused = retrieval.get("refused", False)
    results = retrieval.get("results", [])
    query = retrieval.get("query", "")

    if refused or not results:
        return (
            f"Không tìm thấy thông tin liên quan cho: \"{query}\"\n"
            f"Phương pháp: {method} | Kết quả: 0 | Gợi ý: từ chối trả lời (out-of-scope)."
        )

    lines = [
        f"Kết quả truy xuất cho: \"{query}\"",
        f"Phương pháp: {method} | Số chunks: {len(results)}",
        "---",
    ]

    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        content = r.get("content", "")
        chunk_id = r.get("chunk_id", "?")
        meta = r.get("metadata", {})
        doc_id = meta.get("doc_id", "?")
        section = meta.get("section", "?")

        lines.append(f"[Chunk {i}] doc_id={doc_id} | section={section} | score={score:.3f}")
        lines.append(content[:500])
        if len(content) > 500:
            lines.append("... (đã cắt ngắn)")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Hybrid retrieval tool for HR Policy RAG pipeline",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Câu hỏi cần truy xuất (Vietnamese supported)",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Số kết quả trả về (default: 3)",
    )
    parser.add_argument(
        "--chunks",
        default="./kb/chunks.json",
        help="Đường dẫn file chunks JSON (default: ./kb/chunks.json)",
    )
    parser.add_argument(
        "--collection",
        default="hr_policies",
        help="Tên ChromaDB collection (default: hr_policies)",
    )

    args = parser.parse_args()

    # Try to connect to ChromaDB
    chroma_collection = None
    if HAS_CHROMADB:
        try:
            client = chromadb.Client()
            chroma_collection = client.get_or_create_collection(args.collection)
        except Exception as exc:
            print(f"[retriever] ChromaDB unavailable ({exc}), using keyword fallback.")

    # Load chunks data for keyword fallback
    chunks_data = _load_chunks_from_file(args.chunks)

    # Retrieve
    result = retrieve_chunks(
        query=args.query,
        top_k=args.top_k,
        chroma_collection=chroma_collection,
        chunks_data=chunks_data,
    )

    # Output
    formatted = format_retrieval_results(result)
    print(formatted)

    # Also output raw JSON for programmatic use
    print("\n--- RAW JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
