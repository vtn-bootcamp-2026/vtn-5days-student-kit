---
name: udds-pack
description: Use when resolving, validating, or maintaining shared UDDS resources such as core layouts, themes, tokens, schemas, and shared maintenance scripts.
---

# UDDS Pack

This is a shared resource/dependency skill, not a production workflow.

Use it only to resolve, validate, or maintain shared UDDS resources. Do not use this skill directly to generate slides, redesign decks, run QA loops, or assemble a complete presentation workflow.

For production slide work, use one of:

- `udds-codex-slide-generator`
- `udds-slide-generator`

For the resource contract, read `references/package-contract.md`.

For designer-facing layout skeleton selection, read `references/layout-skeleton-selection-guide.md`. Use it to map slide intent to either a core `LT-*` skeleton or the active moodboard's structural archetype before production workflows attach skeleton images as geometry references.

## Theme Asset Naming Contract

Use these conventions for every theme under `assets/themes/<theme-id>/`:

- Asset section directories use `NN_Title`, because the numeric prefix controls display order:
  - `01_Guidelines`
  - `02_Logos`
  - `03_Moodboards`
- Moodboard directories under `03_Moodboards/` use `Title-Kebab` as the filesystem/display name:
  - `Board-Strategy`
  - `Human-Centered-AI`
  - `Technical-Blueprint`
  - `Liberal-Reflective`
  - `Sketchnote-Illustration`
- Mood keys in `theme.json` use the normalized `snake_case` equivalent:
  - `Board-Strategy` -> `board_strategy`
  - `Human-Centered-AI` -> `human_centered_ai`
  - `Technical-Blueprint` -> `technical_blueprint`
  - `Liberal-Reflective` -> `liberal_reflective`
  - `Sketchnote-Illustration` -> `sketchnote_illustration`
- Tools must normalize moodboard names before lookup. Do not compare raw folder names directly with `theme.json` keys.
- Do not add `-Moodboard` suffix to moodboard directory names. The parent directory already defines the asset type.

Run the deep theme validator after changing theme assets:

```powershell
python ".agents/skills/udds-pack/scripts/validate_themes.py" --pack ".agents/skills/udds-pack"
```

