import argparse
import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_MODEL = "gemini-2.5-flash"


def load_dotenv(path):
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def image_mime(path):
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    return "application/octet-stream"


def extract_json(text):
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ValueError("Gemini response did not contain a JSON object.")
    return json.loads(match.group(0))


def call_gemini(model, api_key, image_path, expected_text, temperature, timeout):
    image_bytes = Path(image_path).read_bytes()
    encoded = base64.b64encode(image_bytes).decode("ascii")
    prompt = build_prompt(Path(image_path).name, expected_text)
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": image_mime(image_path),
                            "data": encoded,
                        }
                    },
                ],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model, safe='')}:generateContent?key={urllib.parse.quote(api_key)}"
    )
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "\n".join(part.get("text", "") for part in parts if part.get("text"))
    if not text:
        raise ValueError(f"Gemini returned no text for {image_path}")
    result = extract_json(text)
    result.setdefault("must_not_delete", True)
    return result


def build_prompt(image_name, expected_text):
    return f"""You are doing TYPO-ONLY QA for a rendered 16:9 Vietnamese presentation slide image.

Slide image: {image_name}

Reference text from source manifest. Use it only as a spelling and Vietnamese-diacritic reference, not as a strict content checklist:
{json.dumps(expected_text or {{}}, ensure_ascii=False, indent=2)}

Task:
1. Read visible Vietnamese text in the slide image using visual OCR.
2. Check only spelling, Vietnamese diacritics, and OCR/rendering noise.
3. Flag likely wrong or noisy Vietnamese letters/marks: a/ă/â, o/ô/ơ, u/ư, e/ê, d/đ, missing tone marks, extra tone marks, merged stacked accents, broken words, pseudo-letters, stray symbols inside words, or unreadable text.
4. Pay special attention to words that are often corrupted in generated slide images, such as "quyền", "đầu", "tự trị", "bán dẫn", "dữ liệu", "rủi ro", "bảo mật", "phê duyệt", "lãnh đạo", "hiệu suất".
5. Do not check content completeness, content meaning, factual accuracy, brand quality, layout, aesthetics, or whether the slide has extra/missing text.
6. Do not flag "extra pseudo-text" merely because expected_text is empty, incomplete, or does not list every visible sentence.
7. Only flag placeholder gibberish when visible text is clearly not real Vietnamese words or is unreadable.
8. Be conservative: Gemini visual OCR can be wrong, so use "Needs Human Review" only for suspected typo/OCR/diacritic issues.
9. Do not recommend deleting, omitting, moving aside, or reducing slides. QA is only a final typo decision report.

Return only valid JSON with this exact schema:
{{
  "status": "Pass | Needs Human Review",
  "score": 0,
  "confidence": "low | medium | high",
  "notes": "short Vietnamese or English rationale",
  "observed_text_issues": [
    {{
      "observed": "text as it appears in the image",
      "expected": "expected source text if known",
      "issue": "specific typo/diacritic/OCR rendering issue only",
      "confidence": "low | medium | high",
      "recommended_action": "Targeted Typo Fix | Human Verify | none"
    }}
  ],
  "visual_issues": [],
  "proposed_action": "none | Human Review | Targeted Typo Fix: ...",
  "must_not_delete": true
}}

Scoring guide for typo QA only: 18-20 no visible typo issue, 14-17 one uncertain suspected typo, 10-13 several suspected typo issues, below 10 unreadable/garbled text. Keep visual_issues empty unless the visual artifact directly makes text unreadable.
"""


def load_jobs(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data.get("jobs", [])


def slide_number(image_name):
    match = re.search(r"slide(\d+)", image_name)
    return int(match.group(1)) if match else 0


def write_markdown(report, output_path):
    lines = [
        "# Gemini image QA typo flags",
        "",
        "This report marks suspected issues only. Do not delete, omit, move aside, overwrite, regenerate, or fix slides from this report without explicit human approval.",
        "",
    ]
    flagged = [(name, item) for name, item in sorted(report.items(), key=lambda pair: slide_number(pair[0])) if item.get("status") != "Pass"]
    if not flagged:
        lines.append("No slides were flagged by Gemini QA.")
    for image_name, item in flagged:
        lines.append(f"## {image_name}")
        lines.append("")
        lines.append(f"- Status: {item.get('status', '')}")
        lines.append(f"- Score: {item.get('score', '')}")
        lines.append(f"- Confidence: {item.get('confidence', '')}")
        lines.append(f"- Proposed action: {item.get('proposed_action', '')}")
        notes = item.get("notes", "")
        if notes:
            lines.append(f"- Notes: {notes}")
        issues = item.get("observed_text_issues") or []
        for issue in issues:
            observed = issue.get("observed", "")
            expected = issue.get("expected", "")
            detail = issue.get("issue", "")
            confidence = issue.get("confidence", "")
            lines.append(f"- Typo/OCR suspect ({confidence}): observed `{observed}`; reference `{expected}`; {detail}")
        visual_issues = item.get("visual_issues") or []
        for issue in visual_issues:
            lines.append(f"- Visual issue: {issue}")
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run Gemini image QA over prepared UDDS slide QA jobs.")
    parser.add_argument("--jobs", required=True, help="Path to gemini_qa_jobs.json")
    parser.add_argument("--output", help="Path to gemini_qa_report.json. Defaults beside --jobs.")
    parser.add_argument("--flags-md", help="Path to markdown typo flags report. Defaults beside --jobs.")
    parser.add_argument("--env", default=".env", help="Path to .env containing GEMINI_API_KEY")
    parser.add_argument("--model", help="Gemini model. Defaults to GEMINI_QA_MODEL, MODEL, then gemini-2.5-flash.")
    parser.add_argument("--limit", type=int, help="Limit number of pending jobs for a smoke run")
    parser.add_argument("--start-slide", type=int, help="First slide number to process")
    parser.add_argument("--end-slide", type=int, help="Last slide number to process")
    parser.add_argument("--force", action="store_true", help="Re-run slides already present in the output report")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--sleep", type=float, default=0.25, help="Seconds to sleep between API calls")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    load_dotenv(args.env)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("[!] GEMINI_API_KEY is not set. Put it in .env or the environment.")
    model = args.model or os.environ.get("GEMINI_QA_MODEL") or os.environ.get("MODEL") or DEFAULT_MODEL
    jobs_path = Path(args.jobs)
    output_path = Path(args.output) if args.output else jobs_path.with_name("gemini_qa_report.json")
    flags_path = Path(args.flags_md) if args.flags_md else jobs_path.with_name("gemini_qa_typo_flags.md")
    report = {}
    if output_path.exists():
        report = json.loads(output_path.read_text(encoding="utf-8"))

    jobs = load_jobs(jobs_path)
    selected = []
    for job in jobs:
        number = slide_number(job.get("image", ""))
        if args.start_slide and number < args.start_slide:
            continue
        if args.end_slide and number > args.end_slide:
            continue
        if not args.force and job.get("image") in report:
            continue
        selected.append(job)
    if args.limit:
        selected = selected[: args.limit]

    for index, job in enumerate(selected, start=1):
        image_name = job["image"]
        print(f"[*] Gemini QA {index}/{len(selected)}: {image_name}")
        try:
            result = call_gemini(
                model=model,
                api_key=api_key,
                image_path=job["image_path"],
                expected_text=job.get("expected_text", {}),
                temperature=args.temperature,
                timeout=args.timeout,
            )
            report[image_name] = result
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            report[image_name] = {
                "status": "Needs Human Review",
                "score": 0,
                "confidence": "low",
                "notes": f"Gemini QA failed: {exc}",
                "observed_text_issues": [],
                "visual_issues": [],
                "proposed_action": "Human Review",
                "must_not_delete": True,
            }
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        write_markdown(report, flags_path)
        if args.sleep:
            time.sleep(args.sleep)

    print(f"[OK] Gemini QA report: {output_path.resolve()}")
    print(f"[OK] Typo flags:       {flags_path.resolve()}")
    print(f"[OK] Reviewed slides:  {len(report)}")


if __name__ == "__main__":
    main()
