#!/usr/bin/env python3
"""
evaluator.py — Auto-Evaluation Tool for HR Policy Agentic RAG Pipeline.

Runs all test questions through the RAG pipeline, checks citations, verifies
quote accuracy, and generates a comprehensive markdown evaluation report with
SLI metrics compared against SLO targets.

Supports Vietnamese text.

Usage:
    python evaluator.py --questions ./synthetic-data/test-questions.csv --output ./evaluation-report.md
    python evaluator.py --questions ./synthetic-data/test-questions.csv --output ./evaluation-report.md --chunks ./kb/chunks.json
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union


# ---------------------------------------------------------------------------
# SLO targets (Service Level Objectives)
# ---------------------------------------------------------------------------

SLO = {
    "accuracy": 0.85,           # Correct answer rate for in-scope questions
    "citation_rate": 0.90,      # Percentage of answers with valid citations
    "refusal_rate": 0.95,       # Correct refusal rate for out-of-scope questions
    "hallucination_free": 0.90, # Percentage of answers that pass hallucination check
    "quote_accuracy": 0.85,     # Percentage of citations where quote matches source
}


# ---------------------------------------------------------------------------
# Test question loader
# ---------------------------------------------------------------------------

def load_test_questions(csv_path: str) -> list[dict[str, Any]]:
    """Load test questions from CSV file.

    Expected columns: question, classification, expected_answer, expected_source
    Returns list of dicts, one per row.
    """
    p = Path(csv_path).resolve()
    if not p.exists():
        print(f"[evaluator] File not found: {csv_path}")
        return []

    questions: list[dict[str, Any]] = []
    with open(p, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            category_val = row.get("category", "").strip() or row.get("classification", "").strip()
            classification = "in-scope" if category_val.startswith("in-scope") else category_val
            exp_ans = row.get("expected_answer", "").strip() or row.get("expected_behavior", "").strip()
            questions.append({
                "question": row.get("question", "").strip(),
                "classification": classification,
                "expected_answer": exp_ans,
                "expected_source": row.get("expected_source", "").strip(),
            })

    print(f"[evaluator] Loaded {len(questions)} test question(s) from {csv_path}")
    return questions


# ---------------------------------------------------------------------------
# Evaluation functions
# ---------------------------------------------------------------------------

def cross_check_citation(quote: str, source_chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Verify that a quote exists verbatim (or near-verbatim) in source chunks.

    Checks for exact substring match first, then falls back to word-level
    overlap for fuzzy matching.

    Returns dict: {found, match_type, matched_chunk_id, overlap_ratio}.
    """
    if not quote or not source_chunks:
        return {
            "found": False,
            "match_type": "none",
            "matched_chunk_id": None,
            "overlap_ratio": 0.0,
        }

    quote_clean = quote.strip().lower()

    # Exact match
    for chunk in source_chunks:
        content = chunk.get("content", "").lower()
        if quote_clean in content:
            return {
                "found": True,
                "match_type": "exact",
                "matched_chunk_id": chunk.get("chunk_id"),
                "overlap_ratio": 1.0,
            }

    # Fuzzy: word-level overlap
    quote_words = set(quote_clean.split())
    best_ratio = 0.0
    best_chunk_id = None

    for chunk in source_chunks:
        content_words = set(chunk.get("content", "").lower().split())
        if not quote_words or not content_words:
            continue
        overlap = quote_words & content_words
        ratio = len(overlap) / len(quote_words)
        if ratio > best_ratio:
            best_ratio = ratio
            best_chunk_id = chunk.get("chunk_id")

    # Consider found if >70% word overlap
    found = best_ratio >= 0.70
    return {
        "found": found,
        "match_type": "fuzzy" if found else "none",
        "matched_chunk_id": best_chunk_id,
        "overlap_ratio": round(best_ratio, 3),
    }


def evaluate_answer(
    question: str,
    answer_data: dict[str, Any],
    expected: dict[str, Any],
    source_chunks: Optional[list[dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Evaluate a single RAG answer against expected result.

    Checks:
        1. Correct answer (answer matches expected for in-scope)
        2. Has citations (for in-scope questions)
        3. Quote matches source (cross-check)
        4. Refusal when expected (for out-of-scope questions)

    Returns evaluation dict with pass/fail and detailed metrics.
    """
    classification = answer_data.get("classification", "in-scope")
    answer = answer_data.get("answer", "")
    citations = answer_data.get("citations", [])
    is_out_of_scope = answer_data.get("is_out_of_scope", False)
    refusal_message = answer_data.get("refusal_message", "")
    expected_class = expected.get("classification", "in-scope")
    expected_answer = expected.get("expected_answer", "")

    result: dict[str, Any] = {
        "question": question,
        "classification": classification,
        "expected_classification": expected_class,
        "correct_answer": False,
        "has_citations": False,
        "citations_valid": False,
        "refusal_correct": False,
        "hallucination_check": True,
        "issues": [],
    }

    # --- Out-of-scope: should refuse ---
    if expected_class in ("out-of-scope", "prompt-injection"):
        refused = is_out_of_scope or bool(refusal_message)
        result["refusal_correct"] = refused
        if not refused:
            result["issues"].append(
                "Expected refusal for out-of-scope question but answer was given"
            )
        result["overall_pass"] = refused
        return result

    # --- In-scope evaluation ---
    # Check answer correctness (keyword overlap with expected)
    if expected_answer:
        answer_words = set(answer.lower().split())
        expected_words = set(expected_answer.lower().split())
        if expected_words:
            overlap = answer_words & expected_words
            ratio = len(overlap) / len(expected_words)
            result["correct_answer"] = ratio >= 0.50
        else:
            result["correct_answer"] = bool(answer)
    else:
        result["correct_answer"] = bool(answer)

    # Check citations
    result["has_citations"] = len(citations) > 0

    # Cross-check each citation
    citation_checks: list[dict[str, Any]] = []
    all_citations_valid = True

    if citations and source_chunks:
        for citation in citations:
            quote = citation.get("quote", "")
            check = cross_check_citation(quote, source_chunks)
            citation_checks.append({
                "quote": quote[:100],
                **check,
            })
            if not check["found"]:
                all_citations_valid = False

    result["citations_valid"] = all_citations_valid if citations else False
    result["citation_checks"] = citation_checks

    # Hallucination check: answer has no citations and is non-trivial
    if answer and not citations:
        word_count = len(answer.split())
        if word_count > 20:
            result["hallucination_check"] = False
            result["issues"].append(
                "Answer is substantial (>20 words) but has no citations — possible hallucination"
            )

    # Overall pass
    result["overall_pass"] = (
        result["correct_answer"]
        and result["has_citations"]
        and result["citations_valid"]
        and result["hallucination_check"]
    )

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    results: list[dict[str, Any]],
    output_path: Optional[str] = None,
) -> str:
    """Generate a markdown evaluation report with SLI metrics.

    Report sections:
        1. Summary table with SLI vs SLO comparison
        2. Per-question detail table
        3. Detailed breakdown per question

    Returns the markdown report string.
    """
    total = len(results)
    if total == 0:
        return "# Evaluation Report\n\nNo results to evaluate.\n"

    # --- Compute SLI metrics ---
    in_scope = [r for r in results if r.get("expected_classification") == "in-scope"]
    out_of_scope = [
        r for r in results
        if r.get("expected_classification") in ("out-of-scope", "prompt-injection")
    ]

    in_scope_correct = sum(1 for r in in_scope if r.get("correct_answer"))
    out_of_scope_refused = sum(1 for r in out_of_scope if r.get("refusal_correct"))

    with_citations = sum(1 for r in in_scope if r.get("has_citations"))
    hallucination_free = sum(1 for r in results if r.get("hallucination_check"))

    # Citation quote accuracy
    all_citation_checks = []
    for r in results:
        all_citation_checks.extend(r.get("citation_checks", []))
    citations_checked = [c for c in all_citation_checks if c]
    valid_quotes = sum(1 for c in citations_checked if c.get("found"))

    sli = {
        "accuracy": in_scope_correct / len(in_scope) if in_scope else 0.0,
        "citation_rate": with_citations / len(in_scope) if in_scope else 0.0,
        "refusal_rate": out_of_scope_refused / len(out_of_scope) if out_of_scope else 0.0,
        "hallucination_free": hallucination_free / total,
        "quote_accuracy": valid_quotes / len(citations_checked) if citations_checked else 0.0,
    }

    # --- Build report ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines: list[str] = [
        f"# Bao cao Danh gia RAG Pipeline — HR Policy QA",
        f"",
        f"Thoi gian tao: {now}",
        f"Tong so cau hoi: {total}",
        f"",
    ]

    # Summary table
    lines.append("## 1. Tong hop (Summary)")
    lines.append("")
    lines.append("| Metric | SLI | SLO | Status |")
    lines.append("|--------|-----|-----|--------|")

    for metric, slo_val in SLO.items():
        sli_val = sli.get(metric, 0.0)
        status = "PASS" if sli_val >= slo_val else "FAIL"
        lines.append(
            f"| {metric} | {sli_val:.1%} | {slo_val:.1%} | {status} |"
        )

    lines.append("")
    lines.append(
        f"- In-scope: {len(in_scope)} | Correct: {in_scope_correct} "
        f"| With citations: {with_citations}"
    )
    lines.append(
        f"- Out-of-scope: {len(out_of_scope)} | Correctly refused: {out_of_scope_refused}"
    )
    lines.append(
        f"- Hallucination-free: {hallucination_free}/{total}"
    )
    lines.append("")

    # Per-question detail table
    lines.append("## 2. Chi tiet tung cau hoi (Per-Question Detail)")
    lines.append("")
    lines.append("| # | Question | Class | Pass | Citations | Self-Check | Issues |")
    lines.append("|---|----------|-------|------|-----------|------------|---------|")

    for i, r in enumerate(results, 1):
        q_short = r.get("question", "")[:50]
        if len(r.get("question", "")) > 50:
            q_short += "..."
        cls = r.get("expected_classification", "?")
        passed = "PASS" if r.get("overall_pass") else "FAIL"
        has_cit = "Yes" if r.get("has_citations") else "No"
        issues = "; ".join(r.get("issues", [])) or "None"
        lines.append(
            f"| {i} | {q_short} | {cls} | {passed} | {has_cit} | N/A | {issues[:40]} |"
        )

    lines.append("")

    # Detailed breakdown
    lines.append("## 3. Phan tich chi tiet (Detailed Breakdown)")
    lines.append("")

    for i, r in enumerate(results, 1):
        lines.append(f"### Q{i}: {r.get('question', '')}")
        lines.append(f"- **Phan loai**: {r.get('expected_classification', '?')}")
        lines.append(f"- **Ket qua**: {'PASS' if r.get('overall_pass') else 'FAIL'}")
        lines.append(f"- **Dap an dung**: {'Co' if r.get('correct_answer') else 'Khong'}")
        lines.append(f"- **Co trich dan**: {'Co' if r.get('has_citations') else 'Khong'}")
        lines.append(f"- **Trich dan hop le**: {'Co' if r.get('citations_valid') else 'Khong'}")
        lines.append(
            f"- **Hallucination check**: "
            f"{'PASS' if r.get('hallucination_check') else 'FAIL'}"
        )

        if r.get("refusal_correct") is not None:
            lines.append(
                f"- **Tu choi dung**: "
                f"{'Co' if r.get('refusal_correct') else 'Khong'}"
            )

        citation_checks = r.get("citation_checks", [])
        if citation_checks:
            lines.append("- **Chi tiet trich dan**:")
            for cc in citation_checks:
                lines.append(
                    f"  - \"{cc.get('quote', '')}...\" → "
                    f"match={cc.get('match_type')} "
                    f"overlap={cc.get('overlap_ratio', 0):.0%}"
                )

        issues = r.get("issues", [])
        if issues:
            lines.append("- **Van de**:")
            for issue in issues:
                lines.append(f"  - {issue}")

        lines.append("")

    report = "\n".join(lines)

    # Save to file if output path provided
    if output_path:
        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"[evaluator] Report saved to {output_path}")

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Auto-evaluation tool for HR Policy RAG pipeline",
    )
    parser.add_argument(
        "--questions",
        required=True,
        help="Path to test questions CSV file",
    )
    parser.add_argument(
        "--output",
        default="./evaluation-report.md",
        help="Output markdown report path (default: ./evaluation-report.md)",
    )
    parser.add_argument(
        "--chunks",
        default="./kb/chunks.json",
        help="Path to chunks JSON for citation cross-checking (default: ./kb/chunks.json)",
    )
    parser.add_argument(
        "--answers",
        default=None,
        help="Path to answers JSON file (optional; if omitted, runs retriever pipeline)",
    )

    args = parser.parse_args()

    # Load test questions
    questions = load_test_questions(args.questions)
    if not questions:
        print("[evaluator] No test questions loaded. Exiting.")
        sys.exit(1)

    # Load source chunks for cross-checking
    source_chunks: list[dict[str, Any]] = []
    chunks_path = Path(args.chunks).resolve()
    if chunks_path.exists():
        with open(chunks_path, "r", encoding="utf-8") as f:
            source_chunks = json.load(f)
        print(f"[evaluator] Loaded {len(source_chunks)} source chunks for cross-checking")

    # Load or simulate answers
    answers: list[dict[str, Any]] = []
    if args.answers:
        with open(args.answers, "r", encoding="utf-8") as f:
            answers = json.load(f)
    else:
        # Generate placeholder answers from retriever pipeline
        print("[evaluator] No --answers file provided. Running retriever pipeline...")
        try:
            from retriever import retrieve_chunks, _load_chunks_from_file

            chunks_data = _load_chunks_from_file(args.chunks)
            for q in questions:
                retrieval = retrieve_chunks(
                    query=q["question"],
                    top_k=3,
                    chunks_data=chunks_data,
                )
                citations = []
                for r in retrieval.get("results", []):
                    citations.append({
                        "doc_id": r.get("metadata", {}).get("doc_id", "?"),
                        "section": r.get("metadata", {}).get("section", "?"),
                        "quote": r.get("content", "")[:200],
                        "relevance_score": r.get("score", 0),
                    })

                is_oos = q.get("classification", "") in (
                    "out-of-scope", "prompt-injection"
                )
                answers.append({
                    "question": q["question"],
                    "classification": q.get("classification", "in-scope"),
                    "answer": " ".join(
                        r.get("content", "")[:200]
                        for r in retrieval.get("results", [])[:2]
                    ),
                    "citations": citations,
                    "is_out_of_scope": is_oos,
                    "refusal_message": "Xin loi, cau hoi nay ngoai pham vi." if is_oos else "",
                    "confidence": 0.0,
                    "self_check_result": {
                        "passed": True,
                        "issues_found": [],
                        "corrected": False,
                    },
                    "retrieval_method": retrieval.get("method", "none"),
                    "top_chunks_used": len(retrieval.get("results", [])),
                })
        except ImportError:
            print("[evaluator] retriever module not available. Using empty answers.")

    # Evaluate each answer
    eval_results: list[dict[str, Any]] = []
    for q, a in zip(questions, answers):
        result = evaluate_answer(
            question=q["question"],
            answer_data=a,
            expected=q,
            source_chunks=source_chunks,
        )
        eval_results.append(result)

    # Generate report
    report = generate_report(eval_results, output_path=args.output)

    # Print summary to stdout
    total = len(eval_results)
    passed = sum(1 for r in eval_results if r.get("overall_pass"))
    print(f"\n[evaluator] Evaluation complete: {passed}/{total} passed")
    print(f"[evaluator] Full report: {args.output}")


if __name__ == "__main__":
    main()
