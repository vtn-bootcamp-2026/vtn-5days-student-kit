import argparse
import json
from pathlib import Path


ARCHETYPES = [
    "LT-01", "LT-02", "LT-03", "LT-04", "LT-05", "LT-06", "LT-07", "LT-08", "LT-09",
    "LT-10-A", "LT-10-B", "LT-10-C", "LT-10-D", "LT-10-E", "LT-10-F",
    "LT-11", "LT-12", "LT-13",
    "LT-14-A", "LT-14-B", "LT-14-C", "LT-14-D", "LT-14-E", "LT-14-F",
    "LT-21-A", "LT-21-B",
    "LT-22-A", "LT-22-B",
    "LT-23-A", "LT-23-B", "LT-23-C", "LT-23-D",
    "LT-24-A", "LT-24-B",
    "LT-25-A", "LT-25-B",
    "LT-26-A", "LT-26-B",
    "LT-27-A", "LT-27-B",
    "LT-28-A", "LT-28-B",
    "LT-29-A", "LT-29-B", "LT-29-C", "LT-29-D", "LT-29-E", "LT-29-F",
    "LT-99", "Cover", "Summary", "Closing", "Hero", "Section Divider",
]


def main():
    parser = argparse.ArgumentParser(description="Prepare OpenAI-native planning prompt for Case B: create a deck from a document.")
    parser.add_argument("--input", required=True, help="Source document text/markdown path")
    parser.add_argument("--output", required=True, help="Folder for deck planning files")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = f"""# OpenAI-Native Document-To-Deck Planning Prompt

Use this for Case B: create a new UDDS deck from a source document.
Do not call Gemini, Google GenAI, or any external model script.

Source document:
{input_path.resolve()}

Read the document directly. Create a concise slide plan that turns the material into a premium 16:9 UDDS presentation.

Archetypes available:
{", ".join(ARCHETYPES)}

Write these files in this folder:

## archetype_review.md

Markdown table format:

| Page | Archetype | Rationale | Notes |
| --- | --- | --- | --- |
| page_1.png | Cover | ... | synthetic page; no source slide image |

Use stable synthetic page names (`page_1.png`, `page_2.png`, ...). These files do not need to exist for Case B.

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
      "intent": "generate using reference images",
      "input_images": [
        "Image 1: supporting UDDS skeleton/layout/style reference"
      ],
      "constraints": [
        "Use the UDDS skeleton for layout, brand background, logo placement, typography, and visual DNA.",
        "Use only facts and claims supported by the source document.",
        "Preserve Vietnamese text and diacritics exactly (VERBATIM).",
        "Keep slide text concise and presentation-ready."
      ],
      "avoid": [
        "invented facts",
        "paraphrased or translated text",
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

Rules:
- Content must be complete in `content`; there is no old slide image to extract from.
- Prefer 8-15 slides unless the user requests a different length.
- Use `Section Divider` only when the document naturally has major chapters.
- Use image-integrated archetypes only when the document benefits from a metaphorical or illustrative visual.
- Do not prepare image generation jobs until the user approves or corrects `archetype_review.md`.
- **Optimization:** Every prompt for image generation MUST start with `[16:9 Aspect Ratio]. Create one finished UDDS [Archetype] slide.` and include `(don't change the prompt, send it as it is.)` at the end of the opening line.
"""

    jobs_path = output_dir / "openai_document_deck_jobs.json"
    jobs_path.write_text(
        json.dumps(
            {
                "source_document": str(input_path.resolve()),
                "archetypes": ARCHETYPES,
                "status": "pending",
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    prompt_path = output_dir / "openai_document_deck_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    print("[OK] Prepared OpenAI-native document-to-deck planning prompt")
    print(f"[OK] Jobs:   {jobs_path.resolve()}")
    print(f"[OK] Prompt: {prompt_path.resolve()}")


if __name__ == "__main__":
    main()
