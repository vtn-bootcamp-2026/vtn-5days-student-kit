from __future__ import annotations

import json
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def is_valid_pack(path: Path) -> bool:
    return all(
        [
            (path / "SKILL.md").exists(),
            (path / "assets" / "core" / "layout-definitions.json").exists(),
            (path / "assets" / "core" / "layout-skeletons").exists(),
            (path / "assets" / "tokens" / "primitives.json").exists(),
            (path / "assets" / "schemas" / "theme.schema.json").exists(),
            (path / "assets" / "themes").exists(),
        ]
    )


def resolve_pack_root(strict: bool = False) -> Path | None:
    root = skill_root()
    ref_path = root / "package.ref.json"
    if ref_path.exists():
        data = json.loads(ref_path.read_text(encoding="utf-8"))
        pack_value = data.get("pack")
        if pack_value:
            candidate = (root / pack_value).resolve()
            if is_valid_pack(candidate):
                return candidate

    sibling = (root.parent / "udds-pack").resolve()
    if is_valid_pack(sibling):
        return sibling

    if strict:
        return None
    return None


def assets_root(strict: bool = False) -> Path:
    pack = resolve_pack_root(strict=strict)
    if pack is not None:
        return pack / "assets"
    return repo_root()


def core_path(*parts: str) -> Path:
    return assets_root() / "core" / Path(*parts)


def themes_path(*parts: str) -> Path:
    return assets_root() / "themes" / Path(*parts)


def tokens_path(*parts: str) -> Path:
    return assets_root() / "tokens" / Path(*parts)


def schemas_path(*parts: str) -> Path:
    return assets_root() / "schemas" / Path(*parts)


def pack_script_path(script_name: str) -> Path | None:
    pack = resolve_pack_root()
    if pack is None:
        return None
    path = pack / "scripts" / script_name
    return path if path.exists() else None
