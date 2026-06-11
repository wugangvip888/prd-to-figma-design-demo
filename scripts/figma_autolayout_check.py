#!/usr/bin/env python3
"""
Figma Auto Layout Harness Gate — auto_layout

机械检测设计层 page_frame 内所有节点是否已正确设置 Auto Layout。
通过 Figma REST API 递归拉取节点数据，不依赖 AI 自我报告。

Run:
    python scripts/figma_autolayout_check.py --run-id run_001 --page-frame-id 1594:886

Output:
    workspace/harness/run_001_autolayout_check.json

Requires:
    FIGMA_ACCESS_TOKEN environment variable (Figma personal access token)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
HARNESS_DIR = WORKSPACE / "harness"

# 节点类型：仅这些类型的节点才进入检查逻辑
CHECKABLE_TYPES = {"FRAME", "GROUP"}

# 子节点全为纯 Element 类型时，跳过该节点（无需 Auto Layout）
ELEMENT_ONLY_TYPES = {"TEXT", "VECTOR", "RECTANGLE", "ELLIPSE", "IMAGE", "BOOLEAN_OPERATION", "LINE", "STAR", "POLYGON"}

# 名称以这些后缀结尾的节点跳过（背景/装饰层/图标资产）
# 与 wireframe_rules.md "禁止开 Auto Layout 的后缀" 保持一致
SKIP_NAME_SUFFIXES = {
    "_bg", "_background", "_surface", "_gradient",
    "_overlay", "_layer", "_clip", "_mask", "_blur", "_decor",
    "_icon",
}


# ── Utilities ─────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ── Figma REST API ─────────────────────────────────────────────────────────────

def _figma_token() -> str:
    token = os.environ.get("FIGMA_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "FAIL — Figma 认证失败\n"
            "  FIGMA_ACCESS_TOKEN 环境变量未设置\n"
            "  解决方法：执行 export FIGMA_ACCESS_TOKEN=<your_token>"
        )
    return token


def _figma_get(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"X-Figma-Token": _figma_token()})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"FAIL — Figma REST API HTTP 错误\n"
            f"  HTTP {exc.code}，URL = {url}\n"
            f"  解决方法：检查 FIGMA_ACCESS_TOKEN 权限及 node-id 是否有效"
        ) from exc


def fetch_subtree(file_key: str, node_id: str) -> dict[str, Any] | None:
    """
    Fetch the full subtree of a node via /v1/files/:key/nodes?ids=:id&depth=999.
    Returns the 'document' dict, or None on error.
    """
    encoded = node_id.replace(":", "-")
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={encoded}"
    data = _figma_get(url)
    nodes = data.get("nodes") or {}
    node_data = nodes.get(node_id) or nodes.get(encoded)
    if node_data is None:
        return None
    return node_data.get("document")


# ── figma_targets.md parsing ──────────────────────────────────────────────────

def parse_file_key() -> str:
    path = WORKSPACE / "figma_targets.md"
    if not path.exists():
        raise RuntimeError(f"missing file: {rel(path)}")
    text = path.read_text(encoding="utf-8")
    m = re.search(r"figma\.com/design/([A-Za-z0-9_-]+)/", text)
    if not m:
        raise RuntimeError("Cannot parse Figma file key from figma_targets.md")
    return m.group(1)


# ── Skip logic ────────────────────────────────────────────────────────────────

def _has_skip_suffix(name: str) -> bool:
    name_lower = name.lower()
    return any(name_lower.endswith(sfx) for sfx in SKIP_NAME_SUFFIXES)


def _children_are_all_elements(children: list[dict[str, Any]]) -> bool:
    """Return True if all children are pure element types (no FRAME/GROUP)."""
    if not children:
        return True
    return all(c.get("type", "") in ELEMENT_ONLY_TYPES for c in children)


def _should_skip(node: dict[str, Any]) -> bool:
    """
    Return True if this node should be excluded from the Auto Layout check.

    Skip conditions (any one is sufficient):
    1. type is not FRAME or GROUP
    2. no children (leaf node)
    3. all children are pure element types (TEXT / VECTOR / RECTANGLE / ELLIPSE / IMAGE)
    4. node name ends with a suffix in SKIP_NAME_SUFFIXES
    """
    node_type = node.get("type", "")
    if node_type not in CHECKABLE_TYPES:
        return True

    children = node.get("children", [])
    if not children:
        return True

    if _children_are_all_elements(children):
        return True

    if _has_skip_suffix(node.get("name", "")):
        return True

    return False


# ── Recursive traversal ───────────────────────────────────────────────────────

def _traverse(
    node: dict[str, Any],
    depth: int,
    checked: list[dict[str, Any]],
    failed: list[dict[str, Any]],
    skipped_count: list[int],
) -> None:
    """
    Recursively traverse the subtree rooted at `node`.
    - Nodes that pass the skip filter are checked for layoutMode != NONE.
    - Skipped nodes are counted but not checked.
    - All children are traversed regardless of whether the parent was skipped.
    """
    if depth > 0:  # depth 0 = page_frame itself, always skip (it's the root container)
        if _should_skip(node):
            skipped_count[0] += 1
        else:
            layout_mode = node.get("layoutMode", "NONE")
            entry = {
                "id": node.get("id", ""),
                "name": node.get("name", ""),
                "depth": depth,
                "layoutMode": layout_mode,
            }
            checked.append(entry)
            if layout_mode == "NONE":
                failed.append(entry)

    for child in node.get("children", []):
        _traverse(child, depth + 1, checked, failed, skipped_count)


# ── Main check ────────────────────────────────────────────────────────────────

def run_check(run_id: str, page_frame_id: str) -> dict[str, Any]:
    """
    Fetch page_frame subtree, traverse, and return the check result dict.
    Writes output to workspace/harness/run_XXX_autolayout_check.json.
    """
    output_path = HARNESS_DIR / f"{run_id}_autolayout_check.json"

    try:
        file_key = parse_file_key()
    except RuntimeError as exc:
        result = {
            "run_id": run_id,
            "gate": "auto_layout",
            "status": "FAIL",
            "checked_by": "scripts/figma_autolayout_check.py",
            "checked_at": now_iso(),
            "page_frame_id": page_frame_id,
            "error": str(exc),
            "checked_count": 0,
            "skipped_count": 0,
            "failed_nodes": [],
        }
        write_json(output_path, result)
        return result

    try:
        doc = fetch_subtree(file_key, page_frame_id)
    except RuntimeError as exc:
        result = {
            "run_id": run_id,
            "gate": "auto_layout",
            "status": "FAIL",
            "checked_by": "scripts/figma_autolayout_check.py",
            "checked_at": now_iso(),
            "page_frame_id": page_frame_id,
            "error": str(exc),
            "checked_count": 0,
            "skipped_count": 0,
            "failed_nodes": [],
        }
        write_json(output_path, result)
        return result

    if doc is None:
        result = {
            "run_id": run_id,
            "gate": "auto_layout",
            "status": "FAIL",
            "checked_by": "scripts/figma_autolayout_check.py",
            "checked_at": now_iso(),
            "page_frame_id": page_frame_id,
            "error": f"Node {page_frame_id} not found in Figma file",
            "checked_count": 0,
            "skipped_count": 0,
            "failed_nodes": [],
        }
        write_json(output_path, result)
        return result

    checked: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    skipped_count = [0]  # mutable container for pass-by-reference

    _traverse(doc, depth=0, checked=checked, failed=failed, skipped_count=skipped_count)

    status = "FAIL" if failed else "PASS"
    result = {
        "run_id": run_id,
        "gate": "auto_layout",
        "status": status,
        "checked_by": "scripts/figma_autolayout_check.py",
        "checked_at": now_iso(),
        "page_frame_id": page_frame_id,
        "file_key": file_key,
        "checked_count": len(checked),
        "skipped_count": skipped_count[0],
        "failed_nodes": failed,
    }
    write_json(output_path, result)
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Figma Auto Layout Gate — mechanical check via Figma REST API"
    )
    parser.add_argument("--run-id", required=True, help="Run id, e.g. run_001")
    parser.add_argument(
        "--page-frame-id",
        required=True,
        help="Figma node ID of the page_frame to scan, e.g. 1594:886",
    )
    args = parser.parse_args()

    result = run_check(args.run_id, args.page_frame_id)
    output_path = HARNESS_DIR / f"{args.run_id}_autolayout_check.json"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n{'PASS' if result['status'] == 'PASS' else 'FAIL'} — {rel(output_path)}")
    print(
        f"checked={result['checked_count']}  "
        f"skipped={result['skipped_count']}  "
        f"failed={len(result['failed_nodes'])}"
    )

    if result["failed_nodes"]:
        print("\nFailed nodes (layoutMode=NONE):")
        for node in result["failed_nodes"]:
            print(f"  [{node['depth']}] {node['id']}  {node['name']}")

    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
