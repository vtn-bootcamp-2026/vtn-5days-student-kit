import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from udds_paths import core_path, pack_script_path, resolve_pack_root, themes_path, tokens_path


def natural_page_number(page_name):
    digits = "".join(ch for ch in Path(page_name).stem if ch.isdigit())
    return int(digits or 0)


def page_token(page_name):
    stem = Path(page_name).stem
    if stem.startswith("page_"):
        return stem[len("page_") :]
    return stem


def canonical_archetype(archetype):
    text = str(archetype or "").strip()
    upper = text.upper()

    lt_match = re.search(r"\bLT-\d{2}(?:-[A-F])?\b", upper)
    if lt_match:
        return lt_match.group(0)

    if "SECTION" in upper and "DIVIDER" in upper:
        return "SECTION DIVIDER"
    if "SUMMARY" in upper:
        return "SUMMARY"
    if "CLOSING" in upper:
        return "CLOSING"
    if "COVER" in upper:
        return "COVER"
    if "HERO" in upper:
        return "HERO"

    return upper


def run_theme_validation():
    script_path = pack_script_path("validate_themes.py") or Path(__file__).with_name("validate_themes.py")
    if not script_path.exists():
        raise FileNotFoundError(f"Theme validator not found: {script_path}")
        
    print(f"[*] Triggering Deep Theme Validation Gate...")
    pack_root = resolve_pack_root()
    command = [sys.executable, str(script_path)]
    if pack_root is not None and script_path == pack_script_path("validate_themes.py"):
        command.extend(["--pack", str(pack_root)])
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError("Theme validation failed. Fix theme files before preparing jobs.")


def load_json(path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def qa_approval_for(output_dir, image_name, proposed_status):
    approval_path = Path(output_dir) / "qa_approved_actions.json"
    approvals = load_json(approval_path, {})
    state = approvals.get(image_name, {}) if isinstance(approvals, dict) else {}
    if not isinstance(state, dict):
        return None
    if not state.get("approved"):
        return None

    approved_status = str(state.get("status") or state.get("action") or "").strip()
    if approved_status and approved_status != proposed_status:
        raise RuntimeError(
            f"QA approval mismatch for {image_name}: approved '{approved_status}' but qa.json proposes '{proposed_status}'."
        )
    return state


def ensure_qa_hitl_approval(output_dir, image_name, proposed_status):
    approval = qa_approval_for(output_dir, image_name, proposed_status)
    if approval is not None:
        return
    approval_path = Path(output_dir) / "qa_approved_actions.json"
    raise RuntimeError(
        "QA-driven tweak/regenerate requires human approval before preparing image jobs. "
        f"Review the finding for {image_name}, then create {approval_path} with "
        f'{{"{image_name}": {{"approved": true, "status": "{proposed_status}"}}}} '
        "or run an explicit --fix-slide command after user approval."
    )


def load_review(review_file, page_filter=None):
    mappings = []
    with open(review_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.startswith("| page_"):
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 2:
                continue
            page_name, archetype = parts[0], parts[1]
            if page_filter and page_name != page_filter:
                continue
            mappings.append({"page": page_name, "archetype": archetype})
    return sorted(mappings, key=lambda item: natural_page_number(item["page"]))


def load_manifest(input_folder):
    manifest_path = Path(input_folder) / "deck_manifest.json"
    manifest = {}
    for item in load_json(manifest_path, []):
        if "page" in item:
            manifest[item["page"]] = item
    return manifest


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def default_imagegen_metadata(has_original, is_tweak_mode=False, is_regenerate_mode=False):
    if is_tweak_mode:
        intent = "aesthetic_tweak"
    elif is_regenerate_mode:
        intent = "regenerate"
    elif has_original:
        intent = "edit"
    else:
        intent = "generate using reference images"

    input_images = []
    if has_original:
        if is_tweak_mode:
            input_images.append("Image 1: current generated slide to polish")
        else:
            input_images.append("Image 1: edit/content target source slide")
        input_images.append("Image 2: supporting LT skeleton/layout geometry reference")
    else:
        input_images.append("Image 1: supporting LT skeleton/layout geometry reference")

    return {
        "use_case": "productivity-visual",
        "asset_type": "16:9 presentation slide image",
        "intent": intent,
        "input_images": input_images,
        "constraints": [
            "Use the provided LT skeleton for layout geometry only: zones, anchors, hierarchy, flow direction, safe areas, and logo position.",
            "Use the selected theme and moodboard as the only visual-style authority: palette, background, typography mood, illustration style, texture, lighting, and decorative motifs.",
            "Do not copy colors, backgrounds, textures, illustration style, effects, or accent treatments from core LT skeletons.",
            "Preserve Vietnamese text and diacritics exactly.",
            "Render only content_to_display and delete unmatched skeleton placeholders.",
        ],
        "avoid": [
            "garbled Vietnamese",
            "extra captions",
            "process labels",
            "third-party visual marks",
            "distorted brand marks",
            "unreadable small text",
            "non-16:9 output",
        ],
    }


def hex_luminance(color):
    if not isinstance(color, str):
        return None
    value = color.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        return None
    try:
        r = int(value[0:2], 16) / 255
        g = int(value[2:4], 16) / 255
        b = int(value[4:6], 16) / 255
    except ValueError:
        return None

    def linear(channel):
        if channel <= 0.03928:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    return 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)


def background_is_light(colors):
    luminance = hex_luminance(colors.get("background-primary") if isinstance(colors, dict) else None)
    if luminance is None:
        return False
    return luminance > 0.55


def get_official_logo_path(theme, colors=None):
    logo_dir = themes_path(theme, "02_Logos")
    if background_is_light(colors or {}):
        candidates = [
            logo_dir / "und_logo_transparent_for_light_bg.png",
            logo_dir / "Uncle Dao White Background.png",
            logo_dir / "logo-white-bg.png",
            logo_dir / "logo.png",
        ]
    else:
        candidates = [
            logo_dir / "und_logo_transparent_for_dark_bg.png",
            logo_dir / "Uncle Dao Black Background.png",
            logo_dir / "logo-black-bg.png",
            logo_dir / "logo.png",
        ]
    candidates.extend(
        [
            themes_path(theme, "02_Logos", "Primary", "logo.png"),
            themes_path(theme, "02_Logos", "trainocate-logo-orange-bg.jpg"),
            themes_path(theme, "02_Logos", "trainocate-logo-white-bg.jpg"),
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    if logo_dir.exists():
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            found = sorted(logo_dir.glob(ext))
            if found:
                return found[0]
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            found = sorted(logo_dir.rglob(ext))
            if found:
                return found[0]
    return None


def merge_imagegen_metadata(defaults, overrides):
    if not isinstance(overrides, dict):
        return defaults

    merged = dict(defaults)
    for key in ["use_case", "asset_type", "intent"]:
        if overrides.get(key):
            merged[key] = str(overrides[key])

    for key in ["input_images", "constraints", "avoid"]:
        override_items = as_list(overrides.get(key))
        if override_items:
            combined = list(merged.get(key, []))
            for item in override_items:
                if item not in combined:
                    combined.append(item)
            merged[key] = combined

    return merged


def normalize_skeleton_authority_text(value: str) -> str:
    replacements = {
        "supporting brand skeleton/layout/style reference": "supporting LT skeleton/layout geometry reference",
        "supporting UDDS skeleton/layout/style reference": "supporting LT skeleton/layout geometry reference",
        "supporting brand skeleton/layout/visual reference": "supporting LT skeleton/layout geometry reference",
        "supporting UDDS skeleton/layout/visual reference": "supporting LT skeleton/layout geometry reference",
        "Use the UDDS skeleton for layout, brand background, logo placement, typography, and visual DNA.": (
            "Use the LT skeleton for layout geometry only: zones, anchors, hierarchy, flow direction, safe areas, and logo position."
        ),
        "Use the provided skeleton for layout, brand background, typography, and visual DNA.": (
            "Use the LT skeleton for layout geometry only: zones, anchors, hierarchy, flow direction, safe areas, and logo position."
        ),
    }
    text = str(value)
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def normalize_imagegen_metadata(metadata):
    normalized = dict(metadata)
    for key in ["input_images", "constraints", "avoid"]:
        normalized[key] = [normalize_skeleton_authority_text(item) for item in as_list(normalized.get(key))]
    return normalized


def resolve_token(value, primitives):
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        return primitives.get(value[1:-1], value)
    return value


def load_theme_context(theme, moodboard):
    primitives = {}
    primitives_path = tokens_path("primitives.json")
    if primitives_path.exists():
        data = load_json(primitives_path, {})
        primitives.update(data.get("colors", {}))
        primitives.update(data.get("typography", {}))

    theme_path = themes_path(theme, "theme.json")
    if not theme_path.exists():
        theme_path = tokens_path(f"theme-{theme}.json")

    theme_data = load_json(theme_path, {})
    base_data = theme_data.get("base", theme_data)

    colors = {}
    for key, value in base_data.get("colors", {}).items():
        resolved = value
        for _ in range(3):
            next_value = resolve_token(resolved, primitives)
            if next_value == resolved:
                break
            resolved = next_value
        colors[key] = resolved

    mood_key = moodboard.lower().replace("-", "_").replace(" ", "_")
    mood_data = theme_data.get("moods", {}).get(mood_key, {})

    typography = base_data.get("typography", {})
    return {
        "theme": theme,
        "moodboard": moodboard,
        "colors": colors,
        "aesthetic": mood_data.get(
            "prompt_aesthetic",
            theme_data.get("prompt_aesthetic", "Premium agency-grade minimalist presentation"),
        ),
        "font_heading": typography.get("font-heading", "Montserrat"),
        "font_body": typography.get("font-body", "Open Sans"),
        "title_size": typography.get("title-size", "54pt"),
    }


def get_skeleton_path(archetype, theme, moodboard):
    skeleton_dir = core_path("layout-skeletons")
    normalized = canonical_archetype(archetype)

    matches = list(skeleton_dir.glob(f"{normalized}*.png"))
    if matches:
        return matches[0]

    mood_dirs = [
        themes_path(theme, "03_Moodboards", moodboard),
        themes_path(theme, "03-Moodboards", moodboard),
    ]
    for theme_mood_dir in mood_dirs:
        if theme_mood_dir.exists():
            motif_matches = list(theme_mood_dir.glob(f"*{archetype}*.png"))
            if motif_matches:
                return motif_matches[0]
            motif_matches = list(theme_mood_dir.glob(f"*{normalized}*.png"))
            if motif_matches:
                return motif_matches[0]
            normalized_archetype = "".join(ch for ch in archetype.lower() if ch.isalnum())
            for motif in theme_mood_dir.glob("*.png"):
                normalized_name = "".join(ch for ch in motif.stem.lower() if ch.isalnum())
                if normalized_archetype in normalized_name:
                    return motif

    return skeleton_dir / "LT-10-C-Full-Image-With-Overlay-Text.png"


def get_skeleton_path_strict(archetype, theme, moodboard):
    """
    Resolve skeleton path for an archetype without allowing fallback.
    Returns Path if found; otherwise returns None.
    """
    skeleton_dir = core_path("layout-skeletons")
    normalized = canonical_archetype(archetype)

    # 1) Direct core skeleton match by normalized archetype.
    matches = list(skeleton_dir.glob(f"{normalized}*.png"))
    if matches:
        return matches[0]

    # 2) Theme moodboard motif match.
    mood_dirs = [
        themes_path(theme, "03_Moodboards", moodboard),
        themes_path(theme, "03-Moodboards", moodboard),
    ]
    for theme_mood_dir in mood_dirs:
        if theme_mood_dir.exists():
            motif_matches = list(theme_mood_dir.glob(f"*{archetype}*.png"))
            if motif_matches:
                return motif_matches[0]
            motif_matches = list(theme_mood_dir.glob(f"*{normalized}*.png"))
            if motif_matches:
                return motif_matches[0]
            normalized_archetype = "".join(ch for ch in archetype.lower() if ch.isalnum())
            for motif in theme_mood_dir.glob("*.png"):
                normalized_name = "".join(ch for ch in motif.stem.lower() if ch.isalnum())
                if normalized_archetype in normalized_name:
                    return motif

    return None


def validate_required_skeletons(mappings, theme, moodboard):
    """
    Validate all archetypes in review mappings can resolve to a concrete skeleton
    without fallback. Raise error early so users can fix layout naming/resources.
    """
    missing = []
    for item in mappings:
        archetype = item["archetype"]
        resolved = get_skeleton_path_strict(archetype, theme, moodboard)
        if not resolved or not resolved.exists():
            missing.append((item["page"], archetype))

    if missing:
        lines = [
            "Layout validation failed: missing skeleton for one or more slides.",
            "Fix archetype labels/resources before preparing jobs.",
            "",
            "Missing mappings:",
        ]
        lines.extend([f"- {page}: {arch}" for page, arch in missing])
        raise RuntimeError("\n".join(lines))


def get_spatial_blueprint(archetype):
    arch = canonical_archetype(archetype)
    if arch in ["COVER", "CLOSING", "SECTION DIVIDER"]:
        return (
            "Minimalist centered layout. All core typography (title, subtitle) is vertically and horizontally centered on the 16:9 canvas, "
            "creating a premium focal point. Large title on top, followed by subtitle below. No left/right column splits."
        )
    elif arch == "SUMMARY":
        return (
            "Executive summary layout. Top band contains a concise title and section label. The body is organized into 3 to 4 balanced recap blocks "
            "or takeaway rows, with clear hierarchy from headline to short supporting text. Keep generous whitespace and avoid decorative image dominance."
        )
    elif arch == "LT-01":
        return (
            "Agenda layout. Top-left or top-center title area, followed by a vertically stacked numbered agenda list in the main body. "
            "Each agenda item has one clear row with consistent spacing, optional small index markers, and no multi-column fragmentation."
        )
    elif arch == "LT-05":
        return (
            "Framework/model layout. Central model zone contains the main framework diagram, matrix, loop, pyramid, or model blocks. "
            "Supporting labels sit around the model with clean connector alignment. Preserve a single visual system and avoid scattering unrelated cards."
        )
    elif arch == "LT-09":
        return (
            "Action plan layout. Main body is structured as sequential steps or a timeline from left to right or top to bottom. "
            "Each step has a short action title, compact detail text, and an aligned marker. Emphasize progression and execution order."
        )
    elif arch == "LT-11":
        return (
            "Zen statement layout. One dominant statement sits in the visual center with ample empty space around it. "
            "Secondary text, if present, is small and subordinate. No grids, dense bullets, or competing content blocks."
        )
    elif arch == "LT-12":
        return (
            "Editorial spread layout. Magazine-like composition with a large headline, short deck text, and one strong supporting visual or pull quote. "
            "Use asymmetry intentionally: one dominant text column and one spacious visual or accent zone."
        )
    elif arch == "LT-13":
        return (
            "Dual dialogue layout. Two opposing or complementary voices are placed in balanced left and right zones. "
            "Each side has its own speaker/header and concise content block, separated by a strong vertical boundary or central comparison axis."
        )
    elif arch == "LT-03":
        return (
            "Premium 3-column grid layout. The 16:9 canvas is divided horizontally into 3 equal columns. "
            "Column 1 (left), Column 2 (middle), and Column 3 (right) each contain a distinct block of text aligned precisely under its respective header. "
            "Strict vertical alignment. No horizontal overlapping between columns."
        )
    elif arch in ["LT-02", "LT-06", "LT-07", "LT-08"]:
        return (
            "Premium 2-column split layout. The 16:9 canvas is divided horizontally into 2 equal columns. "
            "Left column has a title and a block of text, right column has a corresponding block of text or content. "
            "Strict vertical alignment. Clean visual separation between the left and right halves."
        )
    elif arch == "LT-04":
        return (
            "Premium 2x2 quadrant grid layout. The 16:9 canvas is divided into 4 equal quadrants (top-left, top-right, bottom-left, bottom-right). "
            "Each quadrant is a neat bento cell containing a short title and content block, strictly aligned both vertically and horizontally."
        )
    elif arch in ["LT-10-A", "LT-14-A", "LT-29-A"]:
        return (
            "Image-left text-right split layout. The left 45-50% of the canvas is reserved for the primary image or illustration. "
            "The right 50-55% contains the title and concise text stack. Keep a hard spatial boundary so text never enters the image zone."
        )
    elif arch in ["LT-10-B", "LT-14-B", "LT-29-B"]:
        return (
            "Text-left image-right split layout. The left 50-55% of the canvas is reserved for title and body text. "
            "The right 45-50% contains the primary image or illustration. Keep typography aligned to a single vertical axis."
        )
    elif arch in ["LT-10-C", "LT-14-C", "LT-29-C", "HERO"]:
        return (
            "Full-bleed image with overlay text layout. The entire 16:9 canvas may use a photographic or illustrative background, "
            "but all text must sit inside a deliberate high-contrast safe zone with overlay treatment. Preserve readability above all else."
        )
    elif arch in ["LT-10-D", "LT-14-D", "LT-29-D"]:
        return (
            "Split-screen visual layout. The 16:9 canvas is divided 50/50: the left 50% zone is dedicated exclusively to clean, high-contrast typography, "
            "while the right 50% zone contains the high-end illustrative or photographic brand image. Strict boundary preservation—no text overlaps "
            "the image zone, and no image details leak into the text zone."
        )
    elif arch in ["LT-10-E", "LT-14-E", "LT-29-E"]:
        return (
            "Top-image bottom-text layout. The upper 50-60% of the canvas is reserved for the primary image or visual field. "
            "The lower 40-50% contains title and supporting text in a clean horizontal text band."
        )
    elif arch in ["LT-10-F", "LT-14-F", "LT-29-F"]:
        return (
            "Top-text bottom-image layout. The upper 35-45% contains the title and concise message. "
            "The lower 55-65% is reserved for the primary image, banner, or visual field. Maintain clear separation between text and image."
        )
    elif arch in ["LT-21-A", "LT-21-B"]:
        return (
            "Bootcamp roadmap layout. Arrange modules, days, or milestones along a clear path or timeline with sequential markers. "
            "Use consistent milestone spacing and keep the roadmap readable as a learning journey."
        )
    elif arch in ["LT-22-A", "LT-22-B"]:
        return (
            "Workflow steps layout. Present process steps in a connected flow with arrows, lanes, or numbered blocks. "
            "Each step must have a compact label and a consistent visual container, emphasizing operational order."
        )
    elif arch in ["LT-23-A", "LT-23-B", "LT-23-C", "LT-23-D"]:
        return (
            "Guardrails checklist layout. Use a clear checklist structure with aligned check markers, short rule titles, and concise explanations. "
            "Group related guardrails into readable rows or columns without turning the slide into dense prose."
        )
    elif arch in ["LT-24-A", "LT-24-B"]:
        return (
            "Lab activity layout. Structure the slide around hands-on activity blocks: objective, task, materials, and expected output. "
            "Use clear zones so participants can scan instructions quickly during a workshop."
        )
    elif arch in ["LT-25-A", "LT-25-B"]:
        return (
            "Use case card layout. Present one or more use cases as compact cards with title, scenario, value, and action. "
            "Cards must share dimensions, spacing, and hierarchy for quick comparison."
        )
    elif arch in ["LT-26-A", "LT-26-B"]:
        return (
            "Prompt comparison layout. Use a side-by-side before/after or weak/strong comparison structure. "
            "Keep prompt examples in distinct text boxes with clear labels and visible contrast between the two versions."
        )
    elif arch in ["LT-27-A", "LT-27-B"]:
        return (
            "Rubric matrix layout. Use a table or matrix with criteria on one axis and scoring levels or evaluation notes on the other. "
            "Maintain strict row and column alignment so the matrix remains legible."
        )
    elif arch in ["LT-28-A", "LT-28-B"]:
        return (
            "Code terminal layout. Reserve the main body for a terminal or code panel with monospaced content, command blocks, or output snippets. "
            "Surrounding explanatory text must be secondary and must not overlap the code panel."
        )
    elif arch == "LT-99":
        return (
            "Verbatim coordinate-preserved layout. The spatial distribution, visual components, text boxes, and complex graphic elements are "
            "positioned precisely as shown in the source Image 1. Respect all absolute coordinates."
        )
    else:
        return (
            "Clean structured presentation layout. Top section contains the slide category/eyebrow and main slide title. "
            "The body section organizes content cleanly using the brand's layout grid to maximize white space and readability."
        )


def build_prompt(item, input_folder, output_folder, manifest, theme_context, tweak_instruction=None, regenerate_instruction=None, logo_mode="optional", quality="medium"):
    page_name = item["page"]
    archetype = item["archetype"]
    skeleton_path = get_skeleton_path(archetype, theme_context["theme"], theme_context["moodboard"])
    token = page_token(page_name)
    output_path = Path(output_folder) / f"slide{token}_redesigned.jpg"
    original_path = output_path if tweak_instruction else Path(input_folder) / page_name
    has_original = original_path.exists()
    logo_path = get_official_logo_path(theme_context["theme"], theme_context["colors"])

    page_content = manifest.get(page_name, {})
    content_data = page_content.get("content", {})
    imagegen_data = page_content.get("imagegen", {})
    eyebrow = content_data.get("eyebrow", "").strip() if isinstance(content_data, dict) else ""

    archetype_key = canonical_archetype(archetype)
    is_complex_preservation = archetype_key == "LT-99"
    is_image_integrated = archetype_key.startswith("LT-10") or archetype_key.startswith("LT-14") or archetype_key == "HERO"
    is_tweak_mode = bool(tweak_instruction)
    is_regenerate_mode = bool(regenerate_instruction)

    if is_tweak_mode:
        image_1_role = "CURRENT DESIGN: technically correct slide that needs aesthetic polishing only."
    elif is_regenerate_mode:
        image_1_role = "Source slide: extract content again and regenerate from scratch because the previous output failed QA."
    elif is_complex_preservation:
        image_1_role = "TOTAL PRESERVATION: preserve all text, layout, and graphics from Image 1."
    elif is_image_integrated:
        image_1_role = "Source slide: extract Vietnamese text and the main photographic/illustrative content; remove third-party branding."
    else:
        image_1_role = "Source slide: use only for Vietnamese text extraction; ignore backgrounds, artifacts, and non-brand logos."

    if is_complex_preservation and has_original:
        cleanup_instruction = "Preserve Image 1 content and layout. Use Image 2 only for layout geometry if needed; apply visual style from the selected theme and moodboard."
    else:
        cleanup_instruction = (
            "Delete dummy skeleton text unless it has exact matching content in content_to_display. "
            "Explicitly remove placeholders like KEY MESSAGE, SUMMARY, CLOSING, SECTION LABEL, PRESENTATION, and TAKEAWAY when unmatched."
        )

    if archetype_key in ["COVER", "CLOSING", "SUMMARY", "SECTION DIVIDER"]:
        eyebrow_instruction = "Delete all skeleton placeholder text. Use only content_to_display."
    elif eyebrow:
        eyebrow_instruction = f"Replace the section placeholder with this exact text: {eyebrow}"
    else:
        eyebrow_instruction = "Delete section placeholders such as SECTION LABEL, PRESENTATION, or TAKEAWAY."

    if is_tweak_mode:
        visual_instruction = (
            f"AESTHETIC POLISH (Change + Preserve + Physics):\n"
            f"1. CHANGE: {tweak_instruction}.\n"
            f"2. PRESERVE: Keep all Vietnamese text, core composition, and brand colors exactly as in Image 1.\n"
            f"3. PHYSICS: Ensure natural lighting and shadows at the modified areas."
        )
    elif is_regenerate_mode:
        visual_instruction = f"Regenerate from scratch and fix this QA failure: {regenerate_instruction}."
    elif is_complex_preservation:
        visual_instruction = "Render Image 1 faithfully while applying the selected theme and moodboard. Use Image 2 only for layout geometry, not for colors or style."
    elif is_image_integrated:
        visual_instruction = "Spatial Balancing: Seamlessly blend the photographic/illustrative content into its designated zone while keeping the text zones clean and legible. Ensure both coexist without overlapping."
    else:
        visual_instruction = "Strict Geometry Matching: follow the LT skeleton geometry precisely, but do not copy its colors, background, decorative treatments, or visual style. Theme and moodboard are the visual authority."

    imagegen_metadata = merge_imagegen_metadata(
        default_imagegen_metadata(has_original, is_tweak_mode, is_regenerate_mode),
        imagegen_data,
    )
    imagegen_metadata = normalize_imagegen_metadata(imagegen_metadata)
    imagegen_metadata["quality"] = quality
    include_logo_reference = logo_mode != "forbidden" and logo_path and logo_path.exists()
    logo_image_number = 3 if has_original else 2
    if include_logo_reference:
        logo_image_label = f"Image {logo_image_number}: official brand logo reference from udds-pack/assets/themes/{theme_context['theme']}/02_Logos"
        if logo_image_label not in imagegen_metadata["input_images"]:
            imagegen_metadata["input_images"].append(logo_image_label)

    if logo_mode == "required" and logo_path:
        logo_requirement_text = (
            f"Brand logo requirement: copy the logo exactly from Image {logo_image_number}, the official logo reference file: {str(logo_path.resolve())}. "
            "If any other logo is present, remove it and replace with the exact reference logo.\n"
        )
        logo_rule = {
            "reference_path": str(logo_path.resolve()),
            "reference_image": f"Image {logo_image_number}",
            "rule": "Use the official logo from the separate reference image exactly. Do not redraw, re-letter, restyle, or substitute.",
            "placement": "top-right logo block consistent with skeleton",
        }
    elif logo_mode == "forbidden":
        logo_requirement_text = "Brand logo requirement: do not render any logo on the slide.\n"
        logo_rule = {"rule": "Do not use logo. Remove or hide logo placeholders if present."}
    elif include_logo_reference:
        logo_requirement_text = (
            f"Brand logo requirement: use Image {logo_image_number} as the official logo reference when the slide requires a logo; "
            "do not invent, redraw, distort, or substitute brand marks.\n"
        )
        logo_rule = {
            "reference_path": str(logo_path.resolve()),
            "reference_image": f"Image {logo_image_number}",
            "rule": "Logo is optional, but any rendered logo must come from the separate official logo reference image exactly.",
            "placement": "follow the logo placement in the skeleton/template",
        }
    else:
        logo_requirement_text = (
            "Brand logo requirement: keep logo behavior consistent with skeleton/template; "
            "do not invent or distort any brand marks.\n"
        )
        logo_rule = {
            "rule": "Logo is optional. If present in skeleton or source, keep it clean and undistorted; otherwise do not force-add."
        }

    input_roles = {}
    if has_original:
        input_roles["Image 1"] = image_1_role
        input_roles["Image 2"] = f"LT skeleton for {archetype}; use for layout geometry only. Do not copy colors, background, texture, effects, or illustration style from this image."
    else:
        input_roles["Image 1"] = f"LT skeleton for {archetype}; use for layout geometry only. Do not copy colors, background, texture, effects, or illustration style from this image."
    if include_logo_reference:
        input_roles[f"Image {logo_image_number}"] = "official brand logo reference; use only for exact logo shape, lettering, and color."

    prompt_config = {
        "output": "single 16:9 presentation slide image",
        "task_type": "aesthetic_tweak" if is_tweak_mode else ("regenerate_failed_slide" if is_regenerate_mode else ("image_redesign" if has_original else "text_to_presentation_slide")),
        "archetype": archetype,
        "imagegen": imagegen_metadata,
        "input_roles": input_roles,
        "content_to_display": content_data if (not is_complex_preservation or not has_original) else "Use all text from Image 1 verbatim.",
        "visual_dna": {
            "aesthetic": theme_context["aesthetic"],
            "color_palette": theme_context["colors"],
            "visual_authority_rule": "The selected theme and moodboard are the only visual-style authority. Core LT skeletons provide geometry only.",
            "layout_geometry_rule": "Follow the LT skeleton for zones, anchors, hierarchy, flow direction, safe areas, and logo position only.",
            "background_rule": "Use the selected theme and moodboard for the background. Do not copy the LT skeleton background if it conflicts with the moodboard.",
            "accent_rule": "Use only theme and moodboard accent colors. Do not inherit any accent treatment from core LT skeletons.",
            "spatial_layout_blueprint": get_spatial_blueprint(archetype),
        },
        "brand_logo": logo_rule,
        "typography": {
            "heading_font": f"{theme_context['font_heading']} ({theme_context['title_size']}, bold)",
            "body_font": theme_context["font_body"],
            "text_rendering": "VERBATIM: Preserve all Vietnamese text and diacritics exactly as provided. Do not translate, paraphrase, or add extra text. Every character must be accurate.",
        },
        "surgical_tasks": {
            "eyebrow_action": eyebrow_instruction,
            "cleanup": cleanup_instruction,
            "visual_sanitization": visual_instruction,
        },
        "avoid": imagegen_metadata["avoid"],
    }

    slide_title = ""
    if isinstance(content_data, dict):
        title_field = content_data.get("title", content_data.get("heading", content_data.get("headline", "")))
        if title_field:
            if isinstance(title_field, list):
                slide_title = " ".join(str(x) for x in title_field)
            else:
                slide_title = str(title_field)
    slide_title = slide_title.strip()

    brand_name = theme_context["theme"].replace("-", " ").title()
    aesthetic_short = theme_context["aesthetic"].split(".")[0].strip()
    title_context = f' containing verbatim Vietnamese text: "{slide_title}"' if slide_title else ""
    leading_phrase = f"[16:9 Slide]. Premium {archetype} presentation slide in \"{brand_name}\" style ({aesthetic_short}){title_context}. (don't change the prompt, send it as it is.)"

    constraints = "; ".join(imagegen_metadata["constraints"])
    avoid = "; ".join(imagegen_metadata["avoid"])

    prompt = (
        f"{leading_phrase}\n"
        f"Intent: {imagegen_metadata['intent']}\n"
        f"Quality: {quality}\n"
        f"Asset type: {imagegen_metadata['asset_type']}\n"
        f"Use case: {imagegen_metadata['use_case']}\n"
        f"Input images: {'; '.join(imagegen_metadata['input_images'])}\n"
        "Primary request: create one finished presentation slide image from the provided source content, using the LT skeleton as layout geometry only.\n"
        f"Composition/framing: 16:9 landscape slide, full-bleed canvas. Spatial layout blueprint: {get_spatial_blueprint(archetype)}. Respect all layout anchors.\n"
        "Visual authority: theme and moodboard define palette, background, typography mood, illustration style, texture, lighting, and decorative motifs. Do not inherit visual style from core LT skeletons.\n"
        "Style/medium: premium agency-grade business presentation visual, clean brand system, polished editorial lighting from the selected theme and moodboard.\n"
        "Text handling: RENDER EXACT TEXT provided in the JSON configuration. Preserve all Vietnamese diacritics exactly; no translation or added labels.\n"
        f"{logo_requirement_text}"
        f"Constraints: {constraints}\n"
        f"Avoid: {avoid}\n\n"
        "Detailed slide configuration:\n"
        f"{json.dumps(prompt_config, indent=2, ensure_ascii=False)}\n"
    )

    inputs = []
    if has_original:
        role = "Image 1 - current generated slide to polish" if is_tweak_mode else "Image 1 - source/current slide"
        inputs.append({"path": str(original_path.resolve()), "role": role})
    skeleton_role = "Image 2 - LT layout geometry reference" if has_original else "Image 1 - LT layout geometry reference"
    inputs.append({"path": str(skeleton_path.resolve()), "role": skeleton_role})
    if include_logo_reference:
        inputs.append({"path": str(logo_path.resolve()), "role": f"Image {logo_image_number} - official logo reference"})

    return {
        "id": f"slide{token}",
        "page": page_name,
        "archetype": archetype,
        "prompt": prompt,
        "prompt_path": "",
        "input_images": inputs,
        "output_path": str(output_path.resolve()),
        "status": "pending",
    }


def build_targeted_fix_job(output_folder, slide_number, fix_type, fix_instruction, quality="medium"):
    output_dir = Path(output_folder)
    current_path = output_dir / f"slide{slide_number}_redesigned.jpg"
    source_path = output_dir / f"slide{slide_number}_redesigned_to-be_fixed.jpg"

    if current_path.exists() and not source_path.exists():
        current_path.rename(source_path)
    elif not source_path.exists():
        raise FileNotFoundError(
            f"Cannot find '{current_path.name}' or '{source_path.name}' in {output_dir}."
        )

    if fix_type == "typo":
        prompt = "\n".join(
            [
                "[16:9 Aspect Ratio]. Edit Image A with a minimal typo/OCR text fix.",
                "(don't change the prompt, send it as it is.)",
                "",
                "Dùng Image A làm ảnh gốc.",
                "Giữ nguyên toàn bộ bố cục, màu sắc, font, icon, hình minh họa, hiệu ứng, texture, bóng đổ và nội dung slide.",
                "Chỉ sửa lỗi typo trong phần chữ, đặc biệt lỗi sai dấu tiếng Việt, thiếu dấu, nhiễu dấu, nhầm ký tự hoặc chữ bị méo.",
                "Render lại chữ rõ ràng, sắc nét, đúng chính tả, và hòa hợp tự nhiên với vùng chữ gốc.",
                "Không tự ý thay đổi nội dung khác, không thiết kế lại slide.",
                "",
                "REQUESTED TYPO FIX:",
                fix_instruction,
                "",
                "VISUAL INTEGRATION RULES:",
                "- Inpaint the corrected text into the original text area so it looks native to the slide, not pasted on top.",
                "- Match the exact original text color, opacity, gradient or material treatment, anti-aliasing, edge sharpness, and contrast.",
                "- Match the exact font size, font style, weight, line height, letter spacing, word spacing, alignment, and text box boundaries.",
                "- Preserve the original baseline, x-height, cap height, kerning rhythm, indentation, wrapping, and surrounding whitespace.",
                "- Preserve the local background, shadows, highlights, outlines, glow, perspective, depth, and any texture behind or on the text.",
                "- Do not move nearby text, icons, separators, illustrations, or layout anchors while fixing the typo.",
                "",
                "VIETNAMESE TEXT RENDERING RULES:",
                "- Render the corrected text VERBATIM. Do not translate, paraphrase, add words, remove words, or create pseudo-text.",
                "- Match the surrounding typography exactly: font family category, weight, size, style, color, casing, tracking, baseline, perspective, texture, and shadow.",
                "- Do not switch serif/sans-serif styles. Do not force ALL CAPS unless the surrounding text already uses ALL CAPS.",
                "- Preserve Vietnamese sentence case. Do not convert Vietnamese headings to Initial Caps.",
                "- For Vietnamese diacritics, keep all marks clean and recognizable: circumflex accent, breve accent, horn accent, acute accent, grave accent, hook accent, tilde accent, and dot under the letter.",
                "- For stacked Vietnamese marks, keep the vowel modifier and tone mark visually distinct with a small gap so they do not merge.",
                "- Preserve every unrelated Vietnamese word and diacritic exactly as it appears in Image A.",
                "",
                "OUTPUT:",
                f"- Write a clean 16:9 JPG slide suitable to replace slide{slide_number}_redesigned.jpg.",
                f"- Quality: {quality}.",
            ]
        )
    else:
        fix_rules = {
            "color": "Only adjust the specified color issue. Preserve text, layout, illustration, and composition exactly.",
            "minor_artifact": "Only remove or repair the specified minor artifact. Preserve text, layout, colors, and composition exactly.",
        }

        prompt = "\n".join(
            [
                "[16:9 Aspect Ratio]. Edit the provided slide image with a minimal targeted fix.",
                "(don't change the prompt, send it as it is.)",
                "",
                "Use Image 1 as the only reference and edit target.",
                "",
                "REQUESTED FIX:",
                fix_instruction,
                "",
                "PRESERVE:",
                "- Preserve the slide exactly except for the requested fix.",
                "- Do not change layout, composition, typography hierarchy, illustration style, or unrelated colors.",
                "- Do not rewrite, translate, paraphrase, or reflow unrelated Vietnamese text.",
                f"- {fix_rules[fix_type]}",
                "",
                "OUTPUT:",
                f"- Write a clean 16:9 JPG slide suitable to replace slide{slide_number}_redesigned.jpg.",
                f"- Quality: {quality}.",
            ]
        )

    return {
        "id": f"slide{slide_number}_targeted_fix",
        "page": f"slide{slide_number}_redesigned.jpg",
        "archetype": "Targeted Fix",
        "prompt": prompt,
        "prompt_path": "",
        "input_images": [
            {
                "path": str(source_path.resolve()),
                "role": "Image 1 - current generated slide to fix",
            }
        ],
        "output_path": str(current_path.resolve()),
        "status": "pending",
        "task_type": f"targeted_{fix_type}_fix",
    }



def main():
    parser = argparse.ArgumentParser(description="Prepare slide redesign jobs for Codex $imagegen built-in image_gen.")
    parser.add_argument("--input", help="Folder containing page_*.png and deck_manifest.json")
    parser.add_argument("--review", help="Path to archetype_review.md")
    parser.add_argument("--output", required=True, help="Folder where final redesigned slide images should be recorded")
    parser.add_argument("--theme", default="uncle-dao")
    parser.add_argument("--moodboard", default="Board-Strategy")
    parser.add_argument("--logo-mode", choices=["required", "forbidden", "optional"], default="optional")
    parser.add_argument("--page")
    parser.add_argument("--force", action="store_true", help="Force re-prepare jobs even if output image already exists; old output will be removed.")
    parser.add_argument("--quality", choices=["low", "medium", "high"], default="medium", help="Image generation quality (low/medium/high)")
    parser.add_argument("--fix-slide", type=int, help="Prepare a targeted fix job for slide[n]_redesigned.jpg.")
    parser.add_argument("--fix-type", choices=["typo", "color", "minor_artifact"], default="typo")
    parser.add_argument("--fix", help="Targeted fix instruction. Required with --fix-slide.")
    args = parser.parse_args()

    output_dir = Path(args.output)
    prompts_dir = output_dir / "image_tool_prompts"
    output_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    if args.fix_slide is not None:
        if not args.fix:
            parser.error("--fix is required with --fix-slide")
        job = build_targeted_fix_job(args.output, args.fix_slide, args.fix_type, args.fix, args.quality)
        prompt_path = prompts_dir / f"{job['id']}.md"
        prompt_path.write_text(job["prompt"], encoding="utf-8")
        job["prompt_path"] = str(prompt_path.resolve())
        del job["prompt"]
        manifest_path = output_dir / "image_tool_jobs.json"
        manifest_path.write_text(json.dumps({"jobs": [job]}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] Prepared targeted slide fix job")
        print(f"[OK] Source:   {(output_dir / f'slide{args.fix_slide}_redesigned_to-be_fixed.jpg').resolve()}")
        print(f"[OK] Output:   {(output_dir / f'slide{args.fix_slide}_redesigned.jpg').resolve()}")
        print(f"[OK] Manifest: {manifest_path.resolve()}")
        print(f"[OK] Prompt:   {prompt_path.resolve()}")
        return

    if not args.input or not args.review:
        parser.error("--input and --review are required unless --fix-slide is used")

    run_theme_validation()

    manifest = load_manifest(args.input)
    theme_context = load_theme_context(args.theme, args.moodboard)
    mappings = load_review(args.review, args.page)
    validate_required_skeletons(mappings, args.theme, args.moodboard)

    qa_state = load_json(output_dir / "qa.json", {})
    jobs = []
    for item in mappings:
        token = page_token(item["page"])
        image_name = f"slide{token}_redesigned.jpg"
        existing_output = output_dir / image_name

        tweak_instruction = None
        regenerate_instruction = None
        state = qa_state.get(image_name, {})
        if isinstance(state, dict) and state.get("status", "").startswith("Aesthetic Tweak:"):
            proposed_status = state["status"].strip()
            ensure_qa_hitl_approval(output_dir, image_name, proposed_status)
            tweak_instruction = proposed_status.replace("Aesthetic Tweak:", "").strip()
        elif isinstance(state, dict) and state.get("status", "").startswith("Regenerate:"):
            proposed_status = state["status"].strip()
            ensure_qa_hitl_approval(output_dir, image_name, proposed_status)
            regenerate_instruction = proposed_status.replace("Regenerate:", "").strip()

        if args.force and existing_output.exists():
            existing_output.unlink()

        if existing_output.exists() and not args.force and not tweak_instruction and not regenerate_instruction:
            continue

        job = build_prompt(
            item,
            args.input,
            args.output,
            manifest,
            theme_context,
            tweak_instruction,
            regenerate_instruction,
            args.logo_mode,
            args.quality,
        )
        prompt_path = prompts_dir / f"{job['id']}_{item['archetype'].replace(' ', '_')}.md"
        prompt_path.write_text(job["prompt"], encoding="utf-8")
        job["prompt_path"] = str(prompt_path.resolve())
        del job["prompt"]
        jobs.append(job)

    manifest_path = output_dir / "image_tool_jobs.json"
    manifest_path.write_text(json.dumps({"jobs": jobs}, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[OK] Prepared image_tool job(s)")
    print(f"[OK] Manifest: {manifest_path.resolve()}")
    print(f"[OK] Prompts:  {prompts_dir.resolve()}")


if __name__ == "__main__":
    main()
