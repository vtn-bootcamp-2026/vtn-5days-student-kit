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
import concurrent.futures
import json
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

try:
    from rank_bm25 import BM25Okapi
    HAS_RANK_BM25 = True
except ImportError:
    HAS_RANK_BM25 = False



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


def build_fts_index(chunks: list[dict[str, Any]], db_path: str = "kb/fts5.db") -> Any:
    """Build keyword search index using SQLite FTS5 or fallback to rank_bm25."""
    if db_path != ":memory:":
        if db_path == "kb/fts5.db":
            script_dir = Path(__file__).resolve().parent
            db_path = str((script_dir / ".." / "kb" / "fts5.db").resolve())
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    has_fts5 = False
    try:
        # Check SQLite FTS5 support dynamically
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE VIRTUAL TABLE test USING fts5(content);")
        has_fts5 = True
    except Exception:
        has_fts5 = False

    if has_fts5:
        try:
            import sqlite3
            conn = sqlite3.connect(db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS chunks_fts;")
            cursor.execute("""
                CREATE VIRTUAL TABLE chunks_fts USING fts5(
                    chunk_id,
                    doc_id,
                    section,
                    content
                );
            """)
            for chunk in chunks:
                cursor.execute(
                    "INSERT INTO chunks_fts (chunk_id, doc_id, section, content) VALUES (?, ?, ?, ?);",
                    (
                        chunk.get("chunk_id", ""),
                        chunk.get("doc_id", ""),
                        chunk.get("section", ""),
                        chunk.get("content", "")
                    )
                )
            conn.commit()
            return {"type": "fts5", "connection": conn, "db_path": db_path}
        except Exception as e:
            print(f"[retriever] Error building SQLite FTS5 index: {e}. Falling back to rank_bm25.")
    
    # Fallback to rank_bm25
    if HAS_RANK_BM25:
        tokenized_corpus = [c.get("content", "").lower().split() for c in chunks]
        bm25 = BM25Okapi(tokenized_corpus)
        return {"type": "rank_bm25", "index": bm25, "chunks": chunks}
    
    # Ultimate fallback to simple TF-IDF (which operates directly on raw chunks)
    return {"type": "simple_tfidf", "chunks": chunks}


def bm25_search(
    conn_or_index: Any,
    query: str,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Search for query using BM25.
    
    Supports SQLite FTS5 (if conn_or_index type is 'fts5' or is a sqlite3.Connection),
    or rank_bm25 (if type is 'rank_bm25'),
    or simple_tfidf (if type is 'simple_tfidf').
    
    Returns list of result dicts: {chunk_id, content, metadata, score, method}.
    Scores are normalised to [0, 1].
    """
    if not conn_or_index:
        return []
    
    # Check index type
    is_fts5 = False
    conn = None
    if isinstance(conn_or_index, sqlite3.Connection):
        conn = conn_or_index
        is_fts5 = True
    elif isinstance(conn_or_index, dict) and conn_or_index.get("type") == "fts5":
        conn = conn_or_index["connection"]
        is_fts5 = True

    # 1. SQLite FTS5 Search
    if is_fts5 and conn is not None:
        import re
        words = re.findall(r'\w+', query.lower())
        if not words:
            return []
        # Safe escaping by double quoting each word and joining with OR
        fts_query = " OR ".join(f'"{w}"' for w in words)
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT chunk_id, doc_id, section, content, bm25(chunks_fts)
                FROM chunks_fts
                WHERE chunks_fts MATCH ?
                ORDER BY bm25(chunks_fts) ASC
                LIMIT ?;
            """, (fts_query, top_k))
            rows = cursor.fetchall()
            
            if not rows:
                return []
            
            raw_results = []
            for row in rows:
                chunk_id, doc_id, section, content, raw_score = row
                raw_results.append({
                    "chunk_id": chunk_id,
                    "content": content,
                    "metadata": {
                        "doc_id": doc_id,
                        "section": section,
                    },
                    "raw_score": raw_score,
                })
            
            # Normalise negative BM25 score to [0, 1] range: y_i = max(0, -raw_score), norm = y_i / max_y
            y_vals = [max(0.0, -r["raw_score"]) for r in raw_results]
            max_y = max(y_vals) if y_vals else 0.0
            
            results = []
            for r, y in zip(raw_results, y_vals):
                norm_score = (y / max_y) if max_y > 0 else 0.0
                if norm_score < KEYWORD_REFUSAL_THRESHOLD:
                    continue
                results.append({
                    "chunk_id": r["chunk_id"],
                    "content": r["content"],
                    "metadata": r["metadata"],
                    "score": round(norm_score, 4),
                    "method": "bm25_fts5",
                })
            return results
        except Exception as e:
            print(f"[retriever] SQLite FTS5 search error: {e}")
            return []

    # 2. rank_bm25 Search
    elif isinstance(conn_or_index, dict) and conn_or_index.get("type") == "rank_bm25":
        bm25_obj = conn_or_index["index"]
        chunks = conn_or_index["chunks"]
        
        tokenized_query = query.lower().split()
        if not tokenized_query:
            return []
            
        raw_scores = bm25_obj.get_scores(tokenized_query)
        scored_chunks = []
        for idx, score in enumerate(raw_scores):
            if score > 0:
                scored_chunks.append((score, chunks[idx]))
                
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_chunks = scored_chunks[:top_k]
        
        if not top_chunks:
            return []
            
        max_score = max(x[0] for x in top_chunks) if top_chunks else 0.0
        
        results = []
        for score, chunk in top_chunks:
            norm_score = (score / max_score) if max_score > 0 else 0.0
            if norm_score < KEYWORD_REFUSAL_THRESHOLD:
                continue
            results.append({
                "chunk_id": chunk.get("chunk_id", "unknown"),
                "content": chunk.get("content", ""),
                "metadata": {
                    k: v
                    for k, v in chunk.items()
                    if k not in ("content",)
                },
                "score": round(norm_score, 4),
                "method": "bm25_library",
            })
        return results

    # 3. simple_tfidf fallback search
    elif isinstance(conn_or_index, dict) and conn_or_index.get("type") == "simple_tfidf":
        chunks = conn_or_index["chunks"]
        return keyword_search(query, chunks, top_k)
        
    return []


def rrf_fuse(
    vector_hits: list[dict[str, Any]],
    bm25_hits: list[dict[str, Any]],
    k: int = 60,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Reciprocal Rank Fusion (RRF) to combine vector and keyword search results.
    
    Formula: score(d) = sum(1 / (k + rank_i(d)))
    """
    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, dict[str, Any]] = {}
    
    # Process vector hits
    for rank, hit in enumerate(vector_hits, start=1):
        chunk_id = hit["chunk_id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))
        chunk_map[chunk_id] = hit

    # Process bm25 hits
    for rank, hit in enumerate(bm25_hits, start=1):
        chunk_id = hit["chunk_id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + (1.0 / (k + rank))
        if chunk_id not in chunk_map:
            chunk_map[chunk_id] = hit
            
    # Sort chunks by RRF score descending
    sorted_chunks = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)
    
    fused_results: list[dict[str, Any]] = []
    for cid in sorted_chunks[:top_k]:
        hit = chunk_map[cid]
        fused_results.append({
            "chunk_id": cid,
            "content": hit["content"],
            "metadata": hit.get("metadata", {}),
            "score": round(rrf_scores[cid], 6),
            "method": "hybrid_rrf",
        })
        
    return fused_results


# ---------------------------------------------------------------------------
# Main retrieval function
# ---------------------------------------------------------------------------

def retrieve_chunks(
    query: str,
    top_k: int = 3,
    chroma_collection=None,
    chunks_data: Optional[list[dict[str, Any]]] = None,
    fts_index: Optional[Any] = None,
) -> dict[str, Any]:
    """Hybrid retrieval: runs vector search and SQLite-FTS5/BM25 keyword search in parallel,
    then applies Reciprocal Rank Fusion (RRF) to merge and rank results.

    Returns a dict with keys:
        results  — list of scored chunks
        method   — "hybrid", "vector", "keyword", or "none"
        refused  — True if no results met the quality threshold
        query    — the original query
    """
    # 1. Build FTS index dynamically if not provided but chunks_data is present
    created_fts_dynamically = False
    if fts_index is None and chunks_data:
        fts_index = build_fts_index(chunks_data)
        created_fts_dynamically = True

    # 2. Run searches in parallel
    vector_hits = []
    bm25_hits = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        if chroma_collection is not None:
            futures["vector"] = executor.submit(vector_search, query, chroma_collection, top_k)
        if fts_index is not None:
            futures["bm25"] = executor.submit(bm25_search, fts_index, query, top_k)

        # Wait and extract results
        if "vector" in futures:
            try:
                vector_hits = futures["vector"].result()
            except Exception as exc:
                print(f"[retriever] Vector search thread error: {exc}")
        if "bm25" in futures:
            try:
                bm25_hits = futures["bm25"].result()
            except Exception as exc:
                print(f"[retriever] BM25 search thread error: {exc}")

    # 3. Clean up FTS connection if created dynamically to avoid file locks
    if created_fts_dynamically and isinstance(fts_index, dict) and fts_index.get("type") == "fts5":
        try:
            fts_index["connection"].close()
        except Exception:
            pass

    # 4. Fuse results using RRF
    fused_results = rrf_fuse(vector_hits, bm25_hits, k=60, top_k=top_k)

    # 5. Return results or refuse if empty
    if fused_results:
        # Determine effective method
        if vector_hits and bm25_hits:
            method = "hybrid"
        elif vector_hits:
            method = "vector"
        else:
            method = "keyword"

        return {
            "results": fused_results,
            "method": method,
            "refused": False,
            "query": query,
        }

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

    # Try to connect to ChromaDB using persistent client
    chroma_collection = None
    if HAS_CHROMADB:
        try:
            client = chromadb.PersistentClient(path="kb/chroma_db")
            chroma_collection = client.get_or_create_collection(args.collection)
        except Exception as exc:
            print(f"[retriever] ChromaDB unavailable ({exc}), using keyword fallback.")

    # Load chunks data for keyword fallback
    chunks_data = _load_chunks_from_file(args.chunks)

    # Build FTS index
    fts_index = build_fts_index(chunks_data) if chunks_data else None

    # Retrieve
    result = retrieve_chunks(
        query=args.query,
        top_k=args.top_k,
        chroma_collection=chroma_collection,
        chunks_data=chunks_data,
        fts_index=fts_index,
    )

    # Clean up FTS connection in main CLI
    if fts_index and fts_index.get("type") == "fts5":
        try:
            fts_index["connection"].close()
        except Exception:
            pass

    # Output
    formatted = format_retrieval_results(result)
    print(formatted)

    # Also output raw JSON for programmatic use
    print("\n--- RAW JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
