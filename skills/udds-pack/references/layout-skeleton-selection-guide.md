# Layout Skeleton Selection Guide

Use this guide when a designer or workflow has a slide concept and needs to choose the closest UDDS layout skeleton.

Layout skeletons define geometry only: zones, reading order, visual hierarchy, safe areas, and content balance. They are not visual-style authority. Color, typography feel, illustration style, texture, photography treatment, and decorative accents must come from the selected theme and moodboard.

## Selection Workflow

1. Identify the slide intent: orient, state one idea, compare, explain a model, show evidence, quote, tell a case, drive action, teach an activity, or present a visual scene.
2. Estimate content density: single message, 2 columns, 3 points, table/matrix, process, code, image-led, or mixed image/text.
3. Pick the narrowest matching skeleton family from the catalog below. For cover, hero, section divider, summary, and closing slides, check the active moodboard's structural archetype files before using a generic named layout.
4. Choose the variant that matches image placement and reading direction.
5. Reduce content before changing skeletons if text does not fit the chosen geometry.

## Core Narrative Skeletons

| Skeleton | Intent | Best for | Avoid when |
| --- | --- | --- | --- |
| `LT-01 Agenda` | Orient the audience | Section agenda, workshop modules, session roadmap summary | The slide needs persuasion or visual drama |
| `LT-02 One insight` | Make one strong point | Key thesis, executive insight, principle, provocative claim | There are more than 1-2 supporting ideas |
| `LT-03 Three-point` | Present balanced pillars | Three lessons, three risks, three capabilities, three choices | Points have unequal weight or need sequencing |
| `LT-04 Two-column comparison` | Compare two sides | Before/after, human/AI, current/future, pros/cons | More than two categories are needed |
| `LT-05 Framework or model` | Explain a system | 2x2, flywheel, stack, map, architecture, governance model | The slide is mostly proof, example, or activity steps |
| `LT-06 Data or chart` | Show evidence | Chart, KPI, scorecard, metric trend, quantitative argument | Data is not the main message |
| `LT-07 Quote` | Pause on a voice | Expert quote, reflective transition, principle statement | The quote needs many annotations |
| `LT-08 Case study` | Tell context plus result | Mini case, customer story, problem/result, local example | The case has many chronological steps |
| `LT-09 Action plan` | Convert insight into steps | Next actions, operating checklist, rollout plan | Steps need a full workflow diagram |

## Image-Led Skeletons

Use `LT-10-*` for general image-led slides and `LT-14-*` when the design direction is more editorial, reflective, or liberal-arts oriented. Use `LT-29-*` for bootcamp/training image slides that need stronger instructional structure.

| Skeleton | Image relationship | Best for |
| --- | --- | --- |
| `LT-10-A` / `LT-14-A` / `LT-29-A` | Image left, text right | Visual example first, then explanation |
| `LT-10-B` / `LT-14-B` / `LT-29-B` | Text left, image right | Claim first, then supporting visual |
| `LT-10-C` / `LT-14-C` / `LT-29-C` | Full image with overlay | Hero moment, scene, emotional beat, strong visual metaphor |
| `LT-10-D` / `LT-14-D` / `LT-29-D` | Split or centered image plus text | Two visual states, paired screenshots, process snapshot |
| `LT-10-E` / `LT-14-E` / `LT-29-E` | Top image, bottom text | Wide scene with takeaway beneath |
| `LT-10-F` / `LT-14-F` / `LT-29-F` | Top text, bottom image | Explanation first, visual evidence beneath |

## Editorial And Reflective Skeletons

| Skeleton | Intent | Best for |
| --- | --- | --- |
| `LT-11 Zen Statement` | Minimal reflective statement | Closing thought, philosophical pause, single-line principle |
| `LT-12 Editorial Spread` | Magazine-like argument | Thought leadership, article excerpt, premium narrative slide |
| `LT-13 Dual Dialogue` | Two voices in tension | Debate, tradeoff, opposing beliefs, old model vs new model |

## Training And Workshop Skeletons

| Skeleton | Intent | Best for |
| --- | --- | --- |
| `LT-21 Bootcamp Roadmap` | Show learning path | Multi-day roadmap, module sequence, capability ladder |
| `LT-22 Workflow Steps` | Show process flow | Agent workflow, operating loop, handoff sequence, pipeline |
| `LT-23 Guardrails Checklist` | Show governance boundaries | Do/don't, risk controls, approval gates, policy guardrails |
| `LT-24 Lab Activity` | Direct hands-on work | Exercise brief, mission objective, participant instructions |
| `LT-25 Use Case Card` | Package reusable examples | Use case portfolio, customer scenario, project card set |
| `LT-26 Prompt Compare` | Contrast quality | Weak vs strong prompt, before/after instruction, critique slide |
| `LT-27 Rubric Matrix` | Evaluate across criteria | Scoring table, capability matrix, assessment rubric |
| `LT-28 Code Terminal` | Show technical artifact | Code, CLI output, API payload, debugging walkthrough |

## Moodboard Structural Archetypes

Every moodboard can provide five branded structural archetypes under `assets/themes/<theme-id>/03_Moodboards/<moodboard>/`. These are not core `LT-*` skeletons. They are moodboard-specific geometry and visual-direction references for deck rhythm.

Use the active moodboard's own files when the slide is a cover, hero, section divider, summary, or closing slide. The filename prefix varies by moodboard, but the archetype numbers and roles stay stable:

| Archetype | Role | Best for | Use instead of |
| --- | --- | --- | --- |
| `*-01-Cover` | Open the deck | Course title, audience, session identity, main promise, partner/client context | Generic `Cover` when a moodboard-specific cover exists |
| `*-02-Hero` | Create a strong thesis or module moment | Big idea, major concept, visual anchor, session-level learning promise | Generic `Hero` when a moodboard-specific hero exists |
| `*-03-Section-Divider` | Separate deck sections | Module breaks, agenda chapters, lab/theory transitions, section reset moments | Generic `Section Divider` when a moodboard-specific divider exists |
| `*-04-Summary` | Consolidate learning | Key takeaways, recap, operating checklist summary, end-of-module synthesis | Generic `Summary` when a moodboard-specific summary exists |
| `*-05-Closing` | Close with action and confidence | Final message, next steps, learner commitment, handoff to practice or follow-up resources | Generic `Closing` when a moodboard-specific closing exists |

Examples from current moodboards include `BS-01-Cover` through `BS-05-Closing` in `uncle-dao/Board-Strategy`, `HC-01-Cover` through `HC-05-Closing` in `uncle-dao/Human-Centered-AI`, and `TC-01-Cover` through `TC-05-Closing` in `trainocate/bootcamp-training`. Treat the prefix as moodboard-specific, not as the archetype contract.

## Special Skeletons

| Skeleton | Use when | Notes |
| --- | --- | --- |
| `LT-99 Complex Preservation` | Redesigning a dense source slide where preserving relationships matters more than simplifying into a standard archetype | Use sparingly. Prefer reducing content first when the slide can be expressed with a clearer skeleton. |
| `Cover`, `Hero`, `Section Divider`, `Summary`, `Closing` | The workflow uses named non-`LT` layout definitions for deck structure | These appear in `layout-definitions.json`; use them for deck-level rhythm rather than ordinary content slides. If the active moodboard provides matching `*-01` through `*-05` structural archetypes, prefer the moodboard files for that branded deck. |

## Variant Rules

- `A/B` variants usually mirror image or content placement. Choose based on reading order and where the strongest visual anchor belongs.
- `C` variants usually favor full-image or overlay treatment. Use only when the image can carry the slide.
- `D/E/F` variants support mixed image/text emphasis. Use them when both visual evidence and explanatory text are required.
- If the selected theme or moodboard conflicts with a core skeleton's colors or decorative treatment, keep the geometry and replace the styling with the theme/moodboard direction.
- If a designer has already created a polished composition, use the skeleton only to name the closest geometry family and to validate spacing, hierarchy, and safe areas.
