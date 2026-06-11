#!/usr/bin/env python3
"""Clean generated workspace outputs while keeping project inputs and rules."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"

GENERATED_DIRS = [
    WORKSPACE / "intents",
    WORKSPACE / "priority_maps",
    WORKSPACE / "layout_specs",
    WORKSPACE / "structure_mapping",
    WORKSPACE / "design_system",
    WORKSPACE / "visual_specs",
    WORKSPACE / "harness",
    WORKSPACE / "records",
]

KEEP_FILES = {
    ROOT / "docs" / "harness-backlog.md",
}


def should_keep(path: Path) -> bool:
    if path.name == ".gitkeep":
        return True
    return path in KEEP_FILES


def collect_targets() -> list[Path]:
    targets: list[Path] = []
    for directory in GENERATED_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.iterdir()):
            if path.is_file() and not should_keep(path):
                targets.append(path)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Remove generated workspace outputs before a clean pipeline rerun. "
            "Keeps rules, prompts, scripts, workspace/PRD, workspace/figma_targets.md, "
            ".gitkeep files, workspace/archive, and docs/harness-backlog.md."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete files. Without this flag, only prints what would be removed.",
    )
    args = parser.parse_args()

    targets = collect_targets()
    action = "Deleting" if args.apply else "Would delete"
    if not targets:
        print("No generated workspace output files found.")
        return 0

    for path in targets:
        print(f"{action}: {path.relative_to(ROOT)}")
        if args.apply:
            path.unlink()

    if not args.apply:
        print("\nDry run only. Re-run with --apply to delete these files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
