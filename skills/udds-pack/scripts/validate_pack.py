from __future__ import annotations

import argparse
import sys
from pathlib import Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def pack_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def has_skeleton_images(path: Path) -> bool:
    return path.exists() and any(path.glob("*.png"))


def validate_pack(pack_root: Path) -> list[str]:
    errors: list[str] = []
    required_files = [
        pack_root / "SKILL.md",
        pack_root / "assets" / "core" / "layout-definitions.json",
        pack_root / "assets" / "tokens" / "primitives.json",
        pack_root / "assets" / "schemas" / "theme.schema.json",
        pack_root / "references" / "package-contract.md",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"missing required file: {path}")

    skeleton_dir = pack_root / "assets" / "core" / "layout-skeletons"
    if not has_skeleton_images(skeleton_dir):
        errors.append(f"missing skeleton images under: {skeleton_dir}")

    theme_root = pack_root / "assets" / "themes"
    theme_files = list(theme_root.glob("*/theme.json")) if theme_root.exists() else []
    if not theme_files:
        errors.append(f"missing theme.json files under: {theme_root}")

    for forbidden_name in ("outputs", "reports"):
        forbidden = pack_root / forbidden_name
        if forbidden.exists():
            errors.append(f"generated artifact directory must not be inside pack: {forbidden}")

    return errors


def legacy_root_has_resources(repo_root: Path) -> bool:
    return all((repo_root / name).exists() for name in ("core", "themes", "tokens"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate UDDS shared resource pack")
    parser.add_argument("--pack", type=Path, default=pack_root_from_script())
    parser.add_argument(
        "--strict-pack",
        action="store_true",
        help="Validate only the pack assets; never treat legacy repo-root resources as sufficient.",
    )
    args = parser.parse_args()

    pack_root = args.pack.resolve()
    errors = validate_pack(pack_root)

    if args.strict_pack and legacy_root_has_resources(repo_root_from_script()):
        print("[strict-pack] legacy repo-root resources detected but ignored by strict validation")

    if errors:
        print("[FAIL] UDDS pack validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"[PASS] UDDS pack validation passed: {pack_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
