import argparse
import json
from pathlib import Path


ARCHETYPES = [
    "LT-01", "LT-02", "LT-03", "LT-04", "LT-05", "LT-06", "LT-07", "LT-08", "LT-09",
    "LT-10-A", "LT-10-B", "LT-10-C", "LT-10-D", "LT-10-E", "LT-10-F",
    "LT-11", "LT-12", "LT-13",
    "LT-14-A", "LT-14-B", "LT-14-C", "LT-14-D", "LT-14-E", "LT-14-F",
    "LT-99", "Cover", "Summary", "Closing", "Hero", "Section Divider",
]


def natural_key(path):
    digits = "".join(ch for ch in path.stem if ch.isdigit())
    return int(digits or 0)


def main():
    parser = argparse.ArgumentParser(description="Prepare OpenAI-native visual triage jobs for Case A: redesign from old PDF/deck page images.")
    parser.add_argument("--input", required=True, help="Folder containing page_*.png slide images from an old PDF/deck")
    parser.add_argument("--output", help="Folder for triage job files. Defaults to --input")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output) if args.output else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = sorted(input_dir.glob("page_*.png"), key=natural_key)
    jobs = []
    for page in pages:
        jobs.append({
            "page": page.name,
            "image_path": str(page.resolve()),
            "status": "pending",
        })

    jobs_path = output_dir / "openai_triage_jobs.json"
    jobs_path.write_text(json.dumps({"jobs": jobs, "archetypes": ARCHETYPES}, indent=2, ensure_ascii=False), encoding="utf-8")

    prompt = f"""# OpenAI-Native UDDS Triage Prompt

Use Codex visual reasoning with `view_image` for every `image_path` in `openai_triage_jobs.json`.
Do not call Gemini, Google GenAI, or any external model script.

This prompt is for Case A: redesign from an old PDF/deck. For Case B, create design from a document, do not use this triage script; read the document directly and author `archetype_review.md` plus `deck_manifest.json`.

For each old slide page:
1. Load the local image with `view_image`.
2. Classify it into exactly one UDDS archetype from this list:
{", ".join(ARCHETYPES)}
3. Extract visible text faithfully, preserving Vietnamese diacritics.
4. Keep dense text concise for redesign: prefer 3-5 short bullets in the manifest when possible.

First write this file in the same folder:

## archetype_review.md

Markdown table format:

| Page | Archetype | Rationale | Notes |
| --- | --- | --- | --- |
| page_1.png | Cover | ... | ... |

After the user approves or corrects `archetype_review.md`, write this file:

## deck_manifest.json

JSON list format:

[
  {{
    "page": "page_1.png",
    "archetype": "Cover",
    "content": {{
      "eyebrow": "",
      "title": "",
      "subtitle": "",
      "bullets": []
    }},
    "imagegen": {{
      "use_case": "productivity-visual",
      "asset_type": "16:9 presentation slide image",
      "intent": "edit",
      "input_images": [
        "Image 1: edit/content target source slide",
        "Image 2: supporting UDDS skeleton/layout/style reference"
      ],
      "constraints": [
        "Use the UDDS skeleton for layout, brand background, logo placement, typography, and visual DNA.",
        "Preserve Vietnamese text and diacritics exactly.",
        "Render only content_to_display and delete unmatched skeleton placeholders."
      ],
      "avoid": [
        "garbled Vietnamese",
        "extra captions",
        "process labels",
        "third-party visual marks",
        "distorted logos",
        "unreadable small text",
        "non-16:9 output"
      ]
    }}
  }}
]

Set `imagegen.intent` per slide:
- Use `"edit"` for Case A because the source page image exists and should ground the redesign.
- Use `"generate using reference images"` only for Case B text-to-slide items or pages without a source image.
- Use `"aesthetic_tweak"` only for QA tweak jobs, not initial triage.
- Use `"regenerate"` only when QA later marks the slide for regeneration.

You may add slide-specific constraints when needed, for example `"Preserve the source diagram structure exactly"` for LT-99 or `"Keep the main photo subject but rebuild the surrounding layout"` for image-integrated archetypes.

Do not prepare image generation jobs until the user has explicitly approved or corrected `archetype_review.md`.
"""
    prompt_path = output_dir / "openai_triage_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    print(f"[OK] Prepared {len(jobs)} OpenAI-native triage job(s)")
    print(f"[OK] Jobs:   {jobs_path.resolve()}")
    print(f"[OK] Prompt: {prompt_path.resolve()}")


if __name__ == "__main__":
    main()
