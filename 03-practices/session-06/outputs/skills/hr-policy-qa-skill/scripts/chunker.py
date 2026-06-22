#!/usr/bin/env python3
"""
chunker.py — HR Policy Document Chunker for Agentic RAG Pipeline.

Reads HR policy markdown files from kb/hr-policies/, chunks them by H2 headings,
generates structured metadata, and optionally populates ChromaDB for vector retrieval.

Supports Vietnamese text. Falls back to in-memory storage when ChromaDB is unavailable.

Usage:
    python chunker.py --kb-dir ./kb/hr-policies --output ./kb/chunks.json
    python chunker.py --kb-dir ./kb/hr-policies --output ./kb/chunks.json --chroma
"""

import argparse
import json
import os
import re
import sys
import uuid
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

    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False


# ---------------------------------------------------------------------------
# Embedding model singleton
# ---------------------------------------------------------------------------

_EMBEDDING_MODEL = None
_EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def _get_embedding_model():
    """Lazily load the sentence-transformers model (singleton)."""
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        if not HAS_SENTENCE_TRANSFORMERS:
            return None
        _EMBEDDING_MODEL = SentenceTransformer(_EMBEDDING_MODEL_NAME)
    return _EMBEDDING_MODEL


def embed_texts(texts: list[str]) -> list[list[float]] | None:
    """Generate embeddings for a list of texts. Returns None if unavailable."""
    model = _get_embedding_model()
    if model is None:
        return None
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


# ---------------------------------------------------------------------------
# YAML frontmatter parser (no PyYAML dependency required)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse YAML frontmatter from markdown text.

    Returns (metadata_dict, body_text).
    Handles simple key: value pairs only (sufficient for HR policy docs).
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}, text

    frontmatter_str = match.group(1)
    body = text[match.end():]

    metadata: dict[str, str] = {}
    for line in frontmatter_str.strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip().strip("\"'")

    return metadata, body


# ---------------------------------------------------------------------------
# Core chunking functions
# ---------------------------------------------------------------------------

def load_policy_files(kb_dir: str) -> list[dict[str, Any]]:
    """Load all .md files from the knowledge base directory.

    Each file is parsed for YAML frontmatter. Returns a list of dicts with keys:
        filename, doc_id, metadata (frontmatter), content (body)
    """
    kb_path = Path(kb_dir).resolve()
    if not kb_path.exists():
        print(f"[chunker] Warning: directory not found: {kb_dir}")
        return []

    documents: list[dict[str, Any]] = []

    for md_file in sorted(kb_path.glob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        metadata, body = _parse_frontmatter(raw)

        # Derive doc_id from frontmatter or filename
        doc_id = metadata.get("doc_id", md_file.stem)

        documents.append({
            "filename": md_file.name,
            "doc_id": doc_id,
            "metadata": metadata,
            "content": body,
        })

    print(f"[chunker] Loaded {len(documents)} policy file(s) from {kb_dir}")
    return documents


def chunk_markdown_by_heading(
    content: str,
    max_words: int = 500,
    overlap_words: int = 50,
) -> list[dict[str, Any]]:
    """Split markdown content by H2 (##) headings.

    If a section exceeds *max_words*, it is further split with overlap.
    Each chunk is a dict with keys: section, content, chunk_index.
    """
    # Split by ## headings, keeping the heading text
    parts = re.split(r"(?=^##\s+)", content, flags=re.MULTILINE)

    chunks: list[dict[str, Any]] = []
    chunk_index = 0

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Extract section heading
        heading_match = re.match(r"^##\s+(.+?)(?:\n|$)", part)
        if heading_match:
            section_name = heading_match.group(1).strip()
            body = part[heading_match.end():].strip()
        else:
            # Content before the first H2 heading
            section_name = "Tổng quan"
            body = part.strip()

        if not body:
            continue

        words = body.split()
        if len(words) <= max_words:
            chunks.append({
                "section": section_name,
                "content": body,
                "chunk_index": chunk_index,
            })
            chunk_index += 1
        else:
            # Sub-split long sections with overlap
            start = 0
            while start < len(words):
                end = start + max_words
                sub_text = " ".join(words[start:end])
                chunks.append({
                    "section": section_name,
                    "content": sub_text,
                    "chunk_index": chunk_index,
                })
                chunk_index += 1
                start += max_words - overlap_words

    return chunks


def generate_metadata(
    chunk: dict[str, Any],
    doc_id: str,
    section: str,
) -> dict[str, Any]:
    """Generate 7-field metadata for a chunk.

    Fields: chunk_id, doc_id, section, version, status, access_level, word_count.
    Source metadata (version, status, access_level) falls back to sensible defaults.
    """
    chunk_id = str(uuid.uuid4())
    word_count = len(chunk["content"].split())

    return {
        "chunk_id": chunk_id,
        "doc_id": doc_id,
        "section": section,
        "version": chunk.get("version", "1.0"),
        "status": chunk.get("status", "active"),
        "access_level": chunk.get("access_level", "all"),
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# ChromaDB population
# ---------------------------------------------------------------------------

def populate_chromadb(
    chunks_with_metadata: list[dict[str, Any]],
    collection_name: str = "hr_policies",
    persist_dir: str | None = None,
) -> dict[str, Any]:
    """Populate ChromaDB with chunk embeddings. Falls back to in-memory dict.

    Returns a result dict with keys: method, collection_name, chunk_count, status.
    """
    result = {
        "method": "none",
        "collection_name": collection_name,
        "chunk_count": len(chunks_with_metadata),
        "status": "no_chunks",
    }

    if not chunks_with_metadata:
        return result

    texts = [c["content"] for c in chunks_with_metadata]
    metadatas = [
        {k: v for k, v in c.items() if k != "content"}
        for c in chunks_with_metadata
    ]
    ids = [c["chunk_id"] for c in chunks_with_metadata]

    # Attempt ChromaDB
    if HAS_CHROMADB:
        try:
            client = chromadb.Client()
            collection = client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "HR Policy chunks for Agentic RAG"},
            )

            # Generate embeddings if available
            embeddings = embed_texts(texts)

            if embeddings:
                collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas,
                    embeddings=embeddings,
                )
            else:
                # Let ChromaDB use its default embedding
                collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas,
                )

            result["method"] = "chromadb"
            result["status"] = "success"
            print(
                f"[chunker] ChromaDB: added {len(ids)} chunks to '{collection_name}'"
            )
            return result

        except Exception as exc:
            print(f"[chunker] ChromaDB error, falling back to dict: {exc}")

    # Fallback: store in a JSON-serialisable dict
    fallback_store = {
        "method": "in_memory_dict",
        "chunks": chunks_with_metadata,
    }
    result["method"] = "in_memory_dict"
    result["status"] = "success"
    print(f"[chunker] In-memory fallback: {len(ids)} chunks stored")
    return fallback_store


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(kb_dir: str, output_path: str | None = None) -> list[dict[str, Any]]:
    """Full chunking pipeline: load -> chunk -> metadata -> (optional) persist.

    Returns the list of chunks with full metadata and content.
    """
    documents = load_policy_files(kb_dir)
    if not documents:
        return []

    all_chunks: list[dict[str, Any]] = []

    for doc in documents:
        raw_chunks = chunk_markdown_by_heading(doc["content"])

        for raw_chunk in raw_chunks:
            meta = generate_metadata(
                chunk=raw_chunk,
                doc_id=doc["doc_id"],
                section=raw_chunk["section"],
            )
            # Merge: metadata fields + content
            chunk_record = {**meta, "content": raw_chunk["content"]}
            all_chunks.append(chunk_record)

    print(f"[chunker] Generated {len(all_chunks)} chunk(s) total")

    # Save to JSON if output path provided
    if output_path:
        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(all_chunks, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[chunker] Saved chunks to {output_path}")

    return all_chunks


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Chunk HR policy markdown files for RAG pipeline",
    )
    parser.add_argument(
        "--kb-dir",
        default="./kb/hr-policies",
        help="Directory containing HR policy .md files (default: ./kb/hr-policies)",
    )
    parser.add_argument(
        "--output",
        default="./kb/chunks.json",
        help="Output JSON path for chunks (default: ./kb/chunks.json)",
    )
    parser.add_argument(
        "--chroma",
        action="store_true",
        help="Also populate ChromaDB with chunk embeddings",
    )
    parser.add_argument(
        "--collection",
        default="hr_policies",
        help="ChromaDB collection name (default: hr_policies)",
    )

    args = parser.parse_args()

    chunks = run_pipeline(kb_dir=args.kb_dir, output_path=args.output)

    if args.chroma and chunks:
        populate_chromadb(chunks, collection_name=args.collection)

    if not chunks:
        print("[chunker] No chunks generated. Check --kb-dir path.")
        sys.exit(1)


if __name__ == "__main__":
    main()
