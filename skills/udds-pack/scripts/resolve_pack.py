from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[4]


def default_pack_root() -> Path:
    return Path(__file__).resolve().parents[1]


def is_valid_pack(path: Path) -> bool:
    return all(
        [
            (path / "SKILL.md").exists(),
            (path / "assets" / "core" / "layout-definitions.json").exists(),
            (path / "assets" / "core" / "layout-skeletons").exists(),
            (path / "assets" / "tokens" / "primitives.json").exists(),
            (path / "assets" / "schemas" / "theme.schema.json").exists(),
            any((path / "assets" / "themes").glob("*/theme.json"))
            if (path / "assets" / "themes").exists()
            else False,
        ]
    )


def legacy_root_is_valid(path: Path) -> bool:
    return all((path / name).exists() for name in ("core", "themes", "tokens"))


def resolve_from_package_ref(skill_dir: Path) -> Path | None:
    ref_path = skill_dir / "package.ref.json"
    if not ref_path.exists():
        return None
    data = json.loads(ref_path.read_text(encoding="utf-8"))
    pack_value = data.get("pack")
    if not pack_value:
        return None
    return (skill_dir / pack_value).resolve()


def resolve_pack(skill_dir: Path | None, strict_pack: bool) -> tuple[Path | None, str]:
    candidates: list[tuple[Path, str]] = []

    if skill_dir is not None:
        ref_candidate = resolve_from_package_ref(skill_dir)
        if ref_candidate is not None:
            candidates.append((ref_candidate, "package.ref.json"))
        candidates.append(((skill_dir.parent / "udds-pack").resolve(), "sibling ../udds-pack"))

    candidates.append((default_pack_root().resolve(), "current resolve_pack.py location"))

    for candidate, source in candidates:
        if is_valid_pack(candidate):
            return candidate, source

    if not strict_pack:
        repo_root = repo_root_from_script()
        if legacy_root_is_valid(repo_root):
            return repo_root, "legacy repo-root resources"

    return None, "no valid UDDS pack found"


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve UDDS shared resource pack")
    parser.add_argument("--from-skill", type=Path, help="Workflow skill directory")
    parser.add_argument("--strict-pack", action="store_true")
    args = parser.parse_args()

    skill_dir = args.from_skill.resolve() if args.from_skill else None
    pack, source = resolve_pack(skill_dir, args.strict_pack)
    if pack is None:
        print(f"[FAIL] {source}")
        return 1

    print(f"[PASS] UDDS pack resolved via {source}: {pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
