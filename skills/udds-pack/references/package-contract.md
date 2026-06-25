# UDDS Pack Contract

`udds-pack` is the shared resource pack for UDDS workflow skills.

## Contains

- `assets/core/`: layout definitions, spacing, typography, and layout skeletons
- `assets/themes/`: theme folders and brand assets
- `assets/tokens/`: primitive token files
- `assets/schemas/`: canonical schemas
- `scripts/`: deterministic utilities called by workflow skills
- `references/layout-skeleton-selection-guide.md`: designer-facing guide for choosing a layout skeleton by slide intent, content density, image/text relationship, and moodboard structural archetype

## Does Not Contain

- user-facing end-to-end slide workflows
- generated decks, generated slide images, QA reports, run logs, `outputs/`, or `reports/`
- workflow-specific orchestration such as triage -> redesign -> QA -> assemble

## Workflow Skill Requirements

Workflow skills must resolve the pack before running any pipeline step. Preferred resolution order:

1. `package.ref.json` beside the workflow skill
2. sibling `../udds-pack`
3. legacy repo-root `core/`, `themes/`, and `tokens/` only outside strict portable validation

Strict portable validation must not rely on legacy root resources.

Low-level production utilities may live in `scripts/` when they perform one deterministic operation from explicit inputs to explicit outputs. The workflow skill remains responsible for deciding when to call them.

## Layout Skeleton Role

Layout skeletons are geometry references only. They define zones, anchors, hierarchy, safe areas, and reading flow. Visual style authority always comes from the selected theme and moodboard, not from the core skeleton image.

When a workflow or designer needs to choose a skeleton, first consult `references/layout-skeleton-selection-guide.md`, then resolve the corresponding PNG under `assets/core/layout-skeletons/` or the selected theme's `assets/themes/<theme-id>/03_Moodboards/<moodboard>/` folder. Machine-readable core zones live under `assets/core/layout-definitions.json`.
