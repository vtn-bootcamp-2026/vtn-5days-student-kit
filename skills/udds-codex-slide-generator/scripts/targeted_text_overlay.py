import argparse
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


DEFAULT_FONT_DIR = Path("C:/Windows/Fonts")
FONT_MAP = {
    "regular": DEFAULT_FONT_DIR / "arial.ttf",
    "bold": DEFAULT_FONT_DIR / "arialbd.ttf",
    "italic": DEFAULT_FONT_DIR / "ariali.ttf",
    "bold_italic": DEFAULT_FONT_DIR / "arialbi.ttf",
}


def parse_box(value):
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox must be x1,y1,x2,y2")
    x1, y1, x2, y2 = parts
    if x2 <= x1 or y2 <= y1:
        raise argparse.ArgumentTypeError("bbox requires x2 > x1 and y2 > y1")
    return (x1, y1, x2, y2)


def parse_color(value):
    try:
        return ImageColor.getrgb(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid color: {value}") from exc


def slide_paths(output_dir, slide_token):
    current = output_dir / f"slide{slide_token}_redesigned.jpg"
    backup = output_dir / f"slide{slide_token}_redesigned_to-be_fixed.jpg"
    return current, backup


def ensure_backup(current, backup, overwrite_backup=False):
    if not current.exists() and not backup.exists():
        raise FileNotFoundError(f"Cannot find {current} or {backup}")
    if current.exists() and (overwrite_backup or not backup.exists()):
        backup.write_bytes(current.read_bytes())
    return backup if backup.exists() else current


def auto_background(img, bbox, sample_bbox=None, blur_radius=5):
    x1, y1, x2, y2 = bbox
    if sample_bbox:
        sx1, sy1, sx2, sy2 = sample_bbox
        patch = img.crop((sx1, sy1, sx2, sy2)).resize((x2 - x1, y2 - y1))
        return patch.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Pick a flat color from bbox corners to avoid sampling old text strokes.
    inset = 3
    points = [
        (x1 + inset, y1 + inset),
        (x2 - inset - 1, y1 + inset),
        (x1 + inset, y2 - inset - 1),
        (x2 - inset - 1, y2 - inset - 1),
    ]
    colors = [img.getpixel(point) for point in points]
    median = tuple(sorted(channel)[len(channel) // 2] for channel in zip(*colors))
    return Image.new("RGB", (x2 - x1, y2 - y1), median)


def load_font(style, size, font_path=None):
    path = Path(font_path) if font_path else FONT_MAP[style]
    if not path.exists():
        raise FileNotFoundError(f"Font not found: {path}")
    return ImageFont.truetype(str(path), size)


def draw_multiline(draw, xy, text, font, fill, line_spacing, align="left", width=None):
    x, y = xy
    for line in text.splitlines():
        line_x = x
        if align == "center" and width is not None:
            text_bbox = draw.textbbox((x, y), line, font=font)
            line_x = x + max(0, (width - (text_bbox[2] - text_bbox[0])) // 2)
        draw.text((line_x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line or "Ag", font=font)
        y += (bbox[3] - bbox[1]) + line_spacing


def main():
    parser = argparse.ArgumentParser(
        description="Patch a rendered slide by covering a bbox and overlaying corrected text."
    )
    parser.add_argument("--output", required=True, help="Folder containing slide<TOKEN>_redesigned.jpg")
    parser.add_argument("--slide-token", required=True, help="Slide token such as 2D, 6, 50B")
    parser.add_argument("--bbox", required=True, type=parse_box, help="Text region x1,y1,x2,y2")
    parser.add_argument("--text", required=True, help="Replacement text. Use \\n for line breaks.")
    parser.add_argument("--font-size", type=int, required=True)
    parser.add_argument("--font-style", choices=sorted(FONT_MAP.keys()), default="regular")
    parser.add_argument("--font-path", help="Optional explicit .ttf/.otf font path")
    parser.add_argument("--text-color", type=parse_color, default=(32, 32, 32))
    parser.add_argument(
        "--background",
        default="auto",
        help="auto or a CSS/hex color such as #fdfdfc or #12191d",
    )
    parser.add_argument("--sample-bbox", type=parse_box, help="Clean texture sample x1,y1,x2,y2")
    parser.add_argument("--padding-x", type=int, default=0)
    parser.add_argument("--padding-y", type=int, default=0)
    parser.add_argument("--line-spacing", type=int, default=4)
    parser.add_argument("--align", choices=["left", "center"], default="left")
    parser.add_argument("--from-current", action="store_true", help="Patch from current image instead of backup")
    parser.add_argument("--overwrite-backup", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output)
    current, backup = slide_paths(output_dir, args.slide_token)
    source = current if args.from_current else ensure_backup(current, backup, args.overwrite_backup)

    img = Image.open(source).convert("RGB")
    x1, y1, x2, y2 = args.bbox
    if args.background == "auto":
        patch = auto_background(img, args.bbox, args.sample_bbox)
    else:
        patch = Image.new("RGB", (x2 - x1, y2 - y1), parse_color(args.background))
    img.paste(patch, args.bbox)

    draw = ImageDraw.Draw(img)
    font = load_font(args.font_style, args.font_size, args.font_path)
    text = args.text.replace("\\n", "\n")
    draw_multiline(
        draw,
        (x1 + args.padding_x, y1 + args.padding_y),
        text,
        font,
        args.text_color,
        args.line_spacing,
        args.align,
        (x2 - x1) - (args.padding_x * 2),
    )

    if not args.dry_run:
        img.save(current, quality=95, subsampling=0)
    print(f"[OK] Source: {source.resolve()}")
    print(f"[OK] Output: {current.resolve()}")
    print(f"[OK] BBox: {args.bbox}")


if __name__ == "__main__":
    main()
