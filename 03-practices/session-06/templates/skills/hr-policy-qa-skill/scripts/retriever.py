#!/usr/bin/env python3
"""
retriever.py — Hybrid Retrieval Tool for HR Policy Agentic RAG.

Provides vector search via ChromaDB with automatic fallback to keyword-based
TF-IDF matching when ChromaDB is unavailable. Score normalisation and refusal
threshold ensure the Agent only receives high-quality context.

Supports Vietnamese text.

Usage:
    python retriever.py --query "Quy định nghỉ phép năm?" --top-k 3
    python retriever.py --query "Chính sách OT" --chunks ./kb/chunks.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


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


def _embed_query(query: str) -> list[float] | None:
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
# Main retrieval function
# ---------------------------------------------------------------------------

def retrieve_chunks(
    query: str,
    top_k: int = 3,
    chroma_collection=None,
    chunks_data: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Hybrid retrieval: try vector search, fallback to keyword.

    Returns a dict with keys:
        results  — list of scored chunks
        method   — "vector", "keyword", or "none"
        refused  — True if no results met the quality threshold
        query    — the original query
    """
    # Attempt vector search first
    if chroma_collection is not None:
        results = vector_search(query, chroma_collection, top_k)
        if results:
            return {
                "results": results,
                "method": "vector",
                "refused": False,
                "query": query,
            }

    # Fallback to keyword search
    if chunks_data:
        results = keyword_search(query, chunks_data, top_k)
        if results:
            return {
                "results": results,
                "method": "keyword",
                "refused": False,
                "query": query,
            }

    # Nothing found — refusal
    return {
        "results": [],
        "method": "none",
        "refused": True,
        "query": query,
    }


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
