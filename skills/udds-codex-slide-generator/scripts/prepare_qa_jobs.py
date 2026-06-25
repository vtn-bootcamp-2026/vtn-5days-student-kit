import argparse
import json
from pathlib import Path


def natural_key(path):
    digits = "".join(ch for ch in path.stem if ch.isdigit())
    return int(digits or 0)


def main():
    parser = argparse.ArgumentParser(description="Prepare Gemini image QA jobs for generated UDDS slide images.")
    parser.add_argument("--input", required=True, help="Folder containing slide*_redesigned images")
    parser.add_argument("--output", help="Folder for QA job files. Defaults to --input")
    parser.add_argument("--manifest", help="Optional deck_manifest.json with expected slide text")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output) if args.output else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_items = load_manifest(args.manifest) if args.manifest else {}

    slides = sorted(
        list(input_dir.glob("slide*_redesigned.jpg")) + list(input_dir.glob("slide*_redesigned.png")),
        key=natural_key,
    )
    jobs = [
        {
            "image": slide.name,
            "image_path": str(slide.resolve()),
            "expected_text": manifest_items.get(natural_key(slide), {}),
            "status": "pending",
        }
        for slide in slides
    ]

    jobs_path = output_dir / "gemini_qa_jobs.json"
    jobs_path.write_text(json.dumps({"jobs": jobs}, indent=2, ensure_ascii=False), encoding="utf-8")

    prompt = """# Gemini Image UDDS QA Prompt

Use Gemini image understanding for every `image_path` in `gemini_qa_jobs.json`.
Read the rendered slide image and write a typo/OCR decision report. Use `expected_text` only as a spelling and Vietnamese-diacritic reference, not as a strict content-completeness checklist.

For each slide, inspect:
- Vietnamese spelling and diacritics only: wrong/missing/noisy tone marks; a/ă/â, o/ô/ơ, u/ư, e/ê, d/đ; broken stacked marks; malformed words such as `quyền`, `đầu`, `tự trị`, `bán dẫn`, `dữ liệu`.
- OCR/text rendering noise: pseudo-letters, merged accents, stray symbols inside Vietnamese words, unreadable or distorted text.
- Do not judge whether the slide has extra/missing content unless the visible text is clearly placeholder gibberish or unreadable.
- Do not score brand, layout, aesthetics, or content strategy in typo QA.

Write `gemini_qa_report.json` in this folder as a findings report only. Gemini visual OCR can be wrong, especially for Vietnamese diacritics and dense slide text, so do not treat this file as approval to edit generated slides.

Use this shape:

{
  "slide1_redesigned.jpg": {
    "status": "Pass",
    "score": 16,
    "confidence": "high",
    "notes": "Short rationale.",
    "observed_text_issues": [],
    "proposed_action": "none",
    "must_not_delete": true
  },
  "slide2_redesigned.jpg": {
    "status": "Needs Human Review",
    "score": 11,
    "confidence": "medium",
    "notes": "Short rationale.",
    "observed_text_issues": [],
    "proposed_action": "Aesthetic Tweak: increase whitespace and improve title hierarchy"
  },
  "slide3_redesigned.jpg": {
    "status": "Needs Human Review",
    "score": 6,
    "confidence": "low",
    "notes": "Short rationale.",
    "observed_text_issues": [
      {
        "observed": "Text as you think it appears on the image.",
        "expected": "Expected source text from the manifest, if known.",
        "issue": "Possible garbled Vietnamese text in the body."
      }
    ],
    "proposed_action": "Targeted Typo Fix: correct the observed text only after human approval",
    "must_not_delete": true
  }
}

Use `Pass` when no visible Vietnamese spelling/diacritic/OCR rendering issue is detected.
Use `Needs Human Review` only for suspected typo/OCR/diacritic issues. Put the recommended typo review/fix in `proposed_action`, not in `status`.
Never run, request, or imply automatic fixes from `gemini_qa_report.json`. The human must approve the proposed action before any targeted fix, tweak, or regeneration job is prepared.
Never delete, omit, move aside, or reduce slides after QA. QA marks issues; it does not change the 64-slide set.
"""
    prompt_path = output_dir / "gemini_qa_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    print(f"[OK] Prepared {len(jobs)} Gemini image QA job(s)")
    print(f"[OK] Jobs:   {jobs_path.resolve()}")
    print(f"[OK] Prompt: {prompt_path.resolve()}")


def load_manifest(manifest_path):
    path = Path(manifest_path)
    if not path.exists():
        raise SystemExit(f"[!] Manifest not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        items = data.get("slides") or data.get("items") or []
    else:
        items = data
    expected = {}
    for index, item in enumerate(items, start=1):
        content = item.get("content", {}) if isinstance(item, dict) else {}
        expected[index] = flatten_text_fields(content)
    return expected


def flatten_text_fields(value, prefix="content"):
    fields = {}
    if isinstance(value, str):
        text = value.strip()
        if text:
            fields[prefix] = text
    elif isinstance(value, list):
        for index, item in enumerate(value, start=1):
            fields.update(flatten_text_fields(item, f"{prefix}[{index}]"))
    elif isinstance(value, dict):
        for key, item in value.items():
            fields.update(flatten_text_fields(item, f"{prefix}.{key}"))
    return fields


if __name__ == "__main__":
    main()
