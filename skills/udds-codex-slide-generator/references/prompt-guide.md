# UDDS `$imagegen` Prompt Guide

This guide defines how `prepare_image_tool_jobs.py` should shape prompts for the Codex `$imagegen` built-in `image_gen` workflow.

The old Gemini workflow treated the Python script as the image-generation runtime. This fork does not. The script only prepares job manifests and prompt files. The Codex agent then:

1. Reads `image_tool_jobs.json`.
2. Loads every local `input_images[].path` with `view_image`.
3. Calls built-in `image_gen` once for each slide job.
4. Selects the best `$CODEX_HOME/generated_images/...` output.
5. Records that output with `record_image_tool_result.py`.

## Recording Safety

Record each slide immediately after its own built-in `image_gen` call. Do not run multiple unrelated batches, leave all outputs in the shared `$CODEX_HOME/generated_images/...` pool, and later guess which generated file belongs to which job.

`record_image_tool_result.py` records hashes and source metadata, but it cannot infer visual intent from a filename alone. The agent must preserve the one-job-at-a-time chain:

1. Read job prompt.
2. Load only that job's input images.
3. Call built-in `image_gen`.
4. Inspect/select that job's output.
5. Record that output before moving to another job or batch.

If several Codex sessions are generating slides in parallel, use separate output folders and separate `image_tool_jobs.json` manifests. Never share one manifest between simultaneous recorders unless the recorder lock is active and each session records only its own just-created image.

Acceptable same-deck parallelism:

- Chat A owns `slide1`-`slide10`.
- Chat B owns `slide11`-`slide20`.
- Chat C owns `slide21`-`slide30`.
- Each chat calls built-in `image_gen` and immediately records only its assigned `job-id`s.
- No chat records a generated image created by another chat unless the user explicitly transfers ownership and verifies the file.

Unsafe same-deck parallelism:

- All chats generate several slides first, then later pick files from the shared `$CODEX_HOME/generated_images/...` directory.
- Two chats work on the same `job-id`.
- One chat reuses another chat's generated source path for a different slide.
- Multiple chats write to the same output file after it is already marked complete.

Targeted fixes after a batch:

- If the user says slide 5 has a typo and slide 9 has a color issue, switch to Targeted Slide Fix Mode.
- Process slide 5 fully first: prepare fix job, call built-in `image_gen`, record the result, and QA it.
- Then process slide 9 the same way.
- Keep the prompt minimal and preserve everything except the requested typo/color/artifact fix.
- Do not rerun the whole batch for localized fixes.

Do not include Gemini-specific API concepts in prompts or instructions, such as `response_modalities`, `thinking_config`, model IDs, SDK retries, or inline byte parts.

## Shared Prompt Shape

Each generated prompt should follow the `$imagegen` shared schema:

- `Use case: productivity-visual`
- `Asset type: 16:9 presentation slide image`
- `Intent: edit` when a source/current slide exists
- `Intent: generate using reference images` when only the skeleton and manifest content exist
- `Input images:` with clear roles for source/current slide and UDDS skeleton
- `Primary request:` one finished UDDS slide image
- `Composition/framing:` 16:9 full-bleed presentation canvas
- `Style/medium:` premium agency-grade business presentation visual
- `Text handling:` preserve Vietnamese text and diacritics exactly
- `Constraints:` skeleton controls layout, background, brand, logo placement, typography, and visual DNA
- `Constraints:` always include an explicit official logo reference path and require exact logo copy (no redraw/substitute)
- `Avoid:` garbled Vietnamese, extra captions, process labels, third-party visual marks, distorted logos, unreadable text, non-16:9 output

## Two Production Cases

### Case A: Redesign From Old PDF

Goal: preserve the useful content and intent of an existing deck while replacing its visual system with a selected UDDS theme and moodboard.

Manifest implications:

- `page` points to a real `page_N.png` extracted from the old PDF/deck.
- `imagegen.intent` is usually `edit`.
- `imagegen.input_images` should include the source page as Image 1 and UDDS skeleton as Image 2.
- `imagegen.input_images` should also include the official logo asset as a dedicated reference image.
- Constraints should mention preserving Vietnamese text, preserving important diagrams/photos when appropriate, and sanitizing old non-brand visuals.

### Case B: Create Design From Document

Goal: convert a source document/article/brief into a new slide deck, not redesign an old slide image.

Manifest implications:

- `page` can be a synthetic stable name such as `page_1.png`; no corresponding source image is required.
- `imagegen.intent` is usually `generate using reference images`.
- `imagegen.input_images` should usually include only the UDDS skeleton/layout reference.
- For strict brand compliance, also include the official logo asset and require exact logo geometry/text.
- Content must be fully represented in `content`; do not rely on an old slide image for text extraction.
- Constraints should emphasize concise slide writing, exact Vietnamese rendering, layout fit, and no invented facts.

## Manifest Contract

Every `deck_manifest.json` item should include an `imagegen` block. `prepare_image_tool_jobs.py` reads this block and uses it to override the default prompt headers.

```json
{
  "page": "page_1.png",
  "archetype": "LT-01",
  "content": {
    "eyebrow": "SECTION",
    "title": "Slide title",
    "subtitle": "",
    "bullets": ["Point 1", "Point 2"]
  },
  "imagegen": {
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
  }
}
```

Keep slide text in `content`. Use `imagegen` only for generation instructions and per-slide overrides.

## Scenario 1: Text-Only Sanitization

**Applied to:** LT-01 to LT-09, Summary, Closing without custom imagery.

### Strategy

Treat the source slide as a content reference only. The skeleton is the visual authority.

### Prompt Logic

- Source/current slide role: extract Vietnamese text and content hierarchy.
- Skeleton role: layout, brand background, logo placement, typography, and visual DNA.
- Visual rule: do not carry over source backgrounds, random shapes, old branding, or non-brand artifacts.
- Text rule: render only `content_to_display`; delete skeleton placeholder text when no matching content exists.

## Scenario 2: Image-Integrated Redesign

**Applied to:** LT-10 series, LT-11 to LT-14, Hero.

### Strategy

Preserve the useful subject matter from the source image, but rebuild the slide using the UDDS skeleton and theme.

### Prompt Logic

- Source/current slide role: extract Vietnamese text and identify useful photographic or illustrative content.
- Skeleton role: define where imagery and text should sit.
- Visual rule: blend useful source imagery into the designated visual zone.
- Sanitization rule: keep the central subject matter, but do not preserve old backgrounds, unwanted branding graphics, or third-party visual marks.
- Balance rule: do not let image content overpower the text zone.

## Scenario 3: Complex Preservation

**Applied to:** LT-99.

### Strategy

Preserve the source slide's complex layout and information structure while applying UDDS brand atmosphere.

### Prompt Logic

- Source/current slide role: preserve text, layout, diagrams, and relationships as faithfully as possible.
- Skeleton role: provide brand mood, background style, accent colors, and logo placement.
- Visual rule: improve finish without changing meaning, order, data, or diagram structure.
- Text rule: preserve all visible text verbatim unless the manifest explicitly provides optimized replacement content.

## Scenario 4: QA Tweak

**Applied to:** slides with a human-approved `Aesthetic Tweak:` action. QA findings alone are not approval.

### Strategy

Use the current generated slide as the edit target. Polish aesthetics without changing text or content.

### Prompt Logic

- Current generated slide role: edit target.
- Skeleton role: brand/style reference.
- Tweak rule: apply only the QA instruction.
- Preservation rule: keep Vietnamese text, diagrams, key imagery, and slide meaning intact.
- HITL rule: first present the QA finding to the user with observed text, expected text, confidence, and proposed action; prepare this job only after explicit approval or a matching `qa_approved_actions.json` entry.

## Scenario 5: Regenerate

**Applied to:** slides with a human-approved `Regenerate:` action. QA findings alone are not approval.

### Strategy

Start over from source content and skeleton because the generated slide failed technically.

### Prompt Logic

- Source/current slide role: content reference, if available.
- Skeleton role: authoritative layout and brand reference.
- Failure rule: explicitly fix the QA failure in `Regenerate: ...`.
- Density rule: if failure is caused by cramped text or garbled Vietnamese, reduce `deck_manifest.json` first, then regenerate.
- HITL rule: do not delete, move aside, overwrite, or regenerate a slide until the user approves the specific slide and action.

## Terminology

Use safe, neutral visual-production language:

- Prefer: `visual sanitization`, `unwanted branding graphics`, `third-party visual marks`, `third-party artifacts`, `source artifacts`.
- Avoid in generation prompts: `remove watermark`, specific third-party product logo deletion, `copyright`, or adversarial phrasing.

QA documents may mention visual marks descriptively, but image-generation prompts should stay focused on creating a clean UDDS slide rather than removing protected marks.
