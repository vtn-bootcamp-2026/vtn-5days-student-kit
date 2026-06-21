#!/usr/bin/env python3
"""
PII Validator — Kiểm tra output không rò rỉ PII gốc.
Chạy sau anonymizer.py để xác minh chất lượng.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any


def validate_output(original_path: Path, redacted_path: Path) -> dict[str, Any]:
    """So sánh file gốc và file đã redacted, tìm PII bị rò rỉ."""
    if not original_path.exists() or not redacted_path.exists():
        return {"error": "Input or output file missing", "leaked_pii": []}

    original = unicodedata.normalize("NFC", original_path.read_text(encoding="utf-8"))
    redacted = unicodedata.normalize("NFC", redacted_path.read_text(encoding="utf-8"))

    # Tìm PII trong redacted output (không nên có)
    pii_patterns = {
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(03|05|07|08|09)\d{8}\b"),
        "cccd": re.compile(r"\b\d{12}\b"),
        "ip": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    }

    leaked = []
    for pii_type, pattern in pii_patterns.items():
        for match in pattern.finditer(redacted):
            matched = match.group()
            # Kiểm tra có phải placeholder không
            if "[REDACTED" not in matched:
                leaked.append({
                    "type": pii_type,
                    "value": matched[:5] + "...",  # Chỉ hiển thị 5 ký tự đầu
                    "position": match.start(),
                })

    # Kiểm tra placeholder count
    placeholders = re.findall(r"\[REDACTED_\w+\]", redacted)

    return {
        "leaked_pii": leaked,
        "placeholder_count": len(placeholders),
        "placeholder_types": list(set(placeholders)),
        "is_clean": len(leaked) == 0,
    }


def validate_log(log_path: Path) -> dict[str, Any]:
    """Kiểm tra log không chứa PII gốc."""
    if not log_path.exists():
        return {"error": "Log file not found", "pii_in_log": []}

    log_content = log_path.read_text(encoding="utf-8")

    # Tìm PII pattern trong log
    pii_patterns = {
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(03|05|07|08|09)\d{8}\b"),
        "cccd": re.compile(r"\b\d{12}\b"),
    }

    pii_in_log = []
    for pii_type, pattern in pii_patterns.items():
        for match in pattern.finditer(log_content):
            pii_in_log.append({
                "type": pii_type,
                "position": match.start(),
            })

    return {
        "pii_in_log": pii_in_log,
        "is_clean": len(pii_in_log) == 0,
    }


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent.parent.parent

    # Validate pii-sample-01
    result1 = validate_output(
        base_dir / "synthetic-data/pii-sample-01.txt",
        base_dir / "outputs/pii-sample-01-redacted.txt",
    )
    print(f"Sample 01: {'CLEAN' if result1['is_clean'] else 'LEAKED'} — {result1['placeholder_count']} placeholders")

    # Validate pii-sample-02-tricky (if exists)
    tricky_path = base_dir / "synthetic-data/pii-sample-02-tricky.txt"
    if tricky_path.exists():
        result2 = validate_output(
            tricky_path,
            base_dir / "outputs/pii-sample-02-tricky-redacted.txt",
        )
        print(f"Sample 02 (tricky): {'CLEAN' if result2['is_clean'] else 'LEAKED'} — {result2['placeholder_count']} placeholders")

    # Validate log
    log_result = validate_log(base_dir / "outputs/execution-log.csv")
    print(f"Log: {'CLEAN' if log_result['is_clean'] else 'PII DETECTED IN LOG'}")


if __name__ == "__main__":
    main()
