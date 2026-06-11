#!/usr/bin/env python3
"""
Figma Geometry Harness Gate — hifi_geometry

Validates high-fidelity Figma frame geometry against visual_spec specifications.
All configuration is read from workspace/ files; no page names, module names,
or Figma node IDs are hardcoded in this script.

Run:
    python scripts/figma_geometry_check.py --run-id run_001 --gate hifi_geometry

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
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
HARNESS_DIR = WORKSPACE / "harness"

PAGE_WIDTH = 360   # Fixed by hifi_generation_rules.md — not a design value
TOLERANCE_PX = 2   # Allowed position/gap tolerance in pixels


# ── Geometry model ────────────────────────────────────────────────────────────

@dataclass
class NodeGeom:
    node_id: str
    name: str
    x: float        # relative to parent
    y: float
    width: float
    height: float
    node_type: str = ""

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


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


def read_json(path: Path) -> tuple[Any | None, list[str]]:
    if not path.exists():
        return None, [f"missing file: {rel(path)}"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"invalid json: {rel(path)}: {exc}"]


def make_result(
    run_id: str,
    gate: str,
    status: str,
    errors: list[str],
    warnings: list[str],
    evidence_files: list[Path],
    upstream_gates: dict[str, str],
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "checked_by": "scripts/figma_geometry_check.py",
        "checked_at": now_iso(),
        "evidence_files": [rel(p) for p in evidence_files],
        "upstream_gates": upstream_gates,
        "blocking_errors": errors,
        "warnings": warnings,
    }


# ── Figma REST API ────────────────────────────────────────────────────────────

def _figma_token() -> str:
    token = os.environ.get("FIGMA_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "FAIL — Figma 认证失败\n"
            "  脚本读到的值：FIGMA_ACCESS_TOKEN 环境变量未设置\n"
            "  期望值：有效的 Figma Personal Access Token\n"
            "  解决方法：执行 export FIGMA_ACCESS_TOKEN=<your_token>，"
            "在 Figma → Settings → Account → Personal Access Tokens 中生成。"
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
            f"  脚本读到的值：HTTP {exc.code}，URL = {url}\n"
            f"  期望值：HTTP 200\n"
            f"  解决方法：检查 FIGMA_ACCESS_TOKEN 是否具有该文件的读取权限，"
            f"以及 figma_targets.md 中的 node-id 是否仍然有效。"
        ) from exc


def _node_to_geom(doc: dict[str, Any], parent_abs_x: float, parent_abs_y: float) -> NodeGeom:
    bb = doc.get("absoluteBoundingBox", {})
    return NodeGeom(
        node_id=doc.get("id", ""),
        name=doc.get("name", ""),
        x=bb.get("x", 0) - parent_abs_x,
        y=bb.get("y", 0) - parent_abs_y,
        width=bb.get("width", 0),
        height=bb.get("height", 0),
        node_type=doc.get("type", ""),
    )


def fetch_page_frames(file_key: str, page_id: str) -> list[NodeGeom]:
    """Return all direct FRAME children of a Figma page node."""
    encoded = page_id.replace(":", "-")
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={encoded}"
    data = _figma_get(url)
    nodes = data.get("nodes") or {}
    node_data = nodes.get(page_id) or nodes.get(encoded)
    if node_data is None:
        raise RuntimeError(
            f"FAIL — 无法读取高保真页面节点\n"
            f"  脚本读到的值：API 返回中未找到 page_id = {page_id}\n"
            f"  期望值：Figma 文件中存在该页面节点\n"
            f"  解决方法：确认 figma_targets.md 中 '高保真输出端' URL 的 node-id 正确，"
            f"且对应页面在 Figma 文件中未被删除。"
        )
    doc = node_data.get("document", {})
    parent_bb = doc.get("absoluteBoundingBox", {"x": 0, "y": 0})
    px, py = parent_bb.get("x", 0), parent_bb.get("y", 0)
    return [
        _node_to_geom(child, px, py)
        for child in doc.get("children", [])
        if child.get("type") == "FRAME" and "absoluteBoundingBox" in child
    ]


def fetch_children(file_key: str, node_id: str) -> list[NodeGeom]:
    """Return direct children of a node with coordinates relative to that node."""
    encoded = node_id.replace(":", "-")
    url = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={encoded}"
    data = _figma_get(url)
    nodes = data.get("nodes") or {}
    node_data = nodes.get(node_id) or nodes.get(encoded)
    if node_data is None:
        return []
    doc = node_data.get("document", {})
    parent_bb = doc.get("absoluteBoundingBox", {"x": 0, "y": 0})
    px, py = parent_bb.get("x", 0), parent_bb.get("y", 0)
    return [
        _node_to_geom(child, px, py)
        for child in doc.get("children", [])
        if "absoluteBoundingBox" in child
    ]


def find_horizontal_containers(
    file_key: str, node_id: str, depth: int = 0, max_depth: int = 5
) -> list[tuple[str, list[NodeGeom]]]:
    """Recursively find horizontal-layout containers. No name dependency."""
    if depth > max_depth:
        return []
    children = fetch_children(file_key, node_id)
    result: list[tuple[str, list[NodeGeom]]] = []
    if len(children) >= 2:
        x_span = max(c.x for c in children) - min(c.x for c in children)
        y_span = max(c.y for c in children) - min(c.y for c in children)
        if x_span > y_span:
            result.append((node_id, children))
    for child in children:
        result.extend(
            find_horizontal_containers(file_key, child.node_id, depth + 1, max_depth)
        )
    return result


# ── figma_targets.md parsing ──────────────────────────────────────────────────

def parse_figma_targets() -> dict[str, str]:
    """
    Returns {"file_key", "sample_frame_id", "hifi_page_id"}.
    All values read from workspace/figma_targets.md — no hardcoded IDs.
    """
    path = WORKSPACE / "figma_targets.md"
    if not path.exists():
        raise RuntimeError(
            f"FAIL — 配置文件缺失\n"
            f"  脚本读到的值：{rel(path)} 不存在\n"
            f"  期望值：包含采样端和高保真输出端 URL 的配置文件\n"
            f"  解决方法：确认 workspace/figma_targets.md 已创建并包含正确链接。"
        )
    text = path.read_text(encoding="utf-8")

    # file_key — extracted from any Figma design URL
    fk_m = re.search(r"figma\.com/design/([A-Za-z0-9_-]+)/", text)
    if not fk_m:
        raise RuntimeError(
            "FAIL — 无法解析 Figma file key\n"
            "  脚本读到的值：figma_targets.md 中未找到 figma.com/design/<key>/ 格式的 URL\n"
            "  期望值：至少一条 figma.com/design/... 链接\n"
            "  解决方法：检查 figma_targets.md 中的链接格式是否为完整 Figma URL。"
        )
    file_key = fk_m.group(1)

    # sample_frame_id — first priority-1 URL with node-id
    s_m = re.search(
        r"^\s*1\.\s+https://www\.figma\.com/design/[^?]+\?node-id=([0-9]+)-([0-9]+)",
        text, re.MULTILINE,
    )
    if not s_m:
        raise RuntimeError(
            "FAIL — 无法解析采样端 Frame ID\n"
            "  脚本读到的值：figma_targets.md 中未找到 priority 1 含 ?node-id=X-Y 的链接\n"
            "  期望格式：1. https://www.figma.com/design/...?node-id=XXX-YYY\n"
            "  解决方法：确认 figma_targets.md 的 '采样端链接' 区域有 '1. <url>' 格式的行，"
            "且 URL 包含 ?node-id= 参数。"
        )
    sample_frame_id = f"{s_m.group(1)}:{s_m.group(2)}"

    # hifi_page_id — from 高保真输出端 section URL
    h_m = re.search(
        r"高保真输出端.*?node-id=([0-9]+)-([0-9]+)",
        text, re.DOTALL,
    )
    if not h_m:
        raise RuntimeError(
            "FAIL — 无法解析高保真输出端 Page ID\n"
            "  脚本读到的值：figma_targets.md '高保真输出端' 区域未找到 ?node-id=X-Y\n"
            "  期望格式：figma文件链接：https://www.figma.com/design/...?node-id=XXX-YYY\n"
            "  解决方法：在 figma_targets.md 高保真输出端的链接中补充 ?node-id= 参数。"
        )
    hifi_page_id = f"{h_m.group(1)}:{h_m.group(2)}"

    return {
        "file_key": file_key,
        "sample_frame_id": sample_frame_id,
        "hifi_page_id": hifi_page_id,
    }


# ── visual_spec parsing ───────────────────────────────────────────────────────

def parse_visual_spec_geometry(visual_spec_dir: Path) -> tuple[dict[str, int], int | None]:
    """
    Parse gap and margin values from ## 页面级视觉属性 tables in visual_spec files.
    Returns (module_gaps, page_margin).
      module_gaps: {"top_nav→prompt_input_card": 24, ...}
      page_margin: 16 or None if not found
    """
    gap_re    = re.compile(r"\|\s*模块间距\s+(\S+)\s*[→\-]+\s*(\S+)\s*\|\s*(\d+)px")
    margin_re = re.compile(r"\|\s*左右页边距\s*\|\s*(\d+)px")

    module_gaps: dict[str, int] = {}
    page_margin: int | None = None

    for spec_file in sorted(visual_spec_dir.glob("*.md")):
        for line in spec_file.read_text(encoding="utf-8").splitlines():
            m = gap_re.search(line)
            if m:
                key = f"{m.group(1)}→{m.group(2)}"
                module_gaps[key] = int(m.group(3))
            m2 = margin_re.search(line)
            if m2 and page_margin is None:
                page_margin = int(m2.group(1))

    return module_gaps, page_margin


# ── Detection A: vertical gap chain ──────────────────────────────────────────

def check_vertical_gaps(
    file_key: str,
    hifi_frame_id: str,
    expected_gaps: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> None:
    children = fetch_children(file_key, hifi_frame_id)
    if not children:
        errors.append(
            "FAIL — 垂直间距检测无法执行\n"
            f"  脚本读到的值：高保真 Frame {hifi_frame_id} 无直接子节点\n"
            "  期望值：至少 1 个直接子模块\n"
            "  解决方法：确认 figma_targets.md 高保真输出端的 node-id 指向正确的 Frame，"
            "而不是空页面或页面根节点。"
        )
        return

    modules = sorted(children, key=lambda n: n.y)
    for i in range(len(modules) - 1):
        curr, nxt = modules[i], modules[i + 1]
        actual_gap = nxt.y - curr.bottom
        key = f"{curr.name}→{nxt.name}"
        expected = expected_gaps.get(key)

        if expected is None:
            existing = ", ".join(expected_gaps) or "（无记录）"
            errors.append(
                f"FAIL — 间距检测无法执行：visual_spec 未定义此模块对\n"
                f"  脚本读到的模块名：{curr.name} → {nxt.name}\n"
                f"  visual_spec 里存在的模块名：{existing}\n"
                f"  解决方法：检查高保真节点命名是否与 visual_spec 一致，"
                f"将节点名改为对应名称，或在 visual_spec ## 页面级视觉属性 表格中补充此模块对的间距定义。"
            )
            continue

        if abs(actual_gap - expected) > TOLERANCE_PX:
            errors.append(
                f"FAIL — 垂直间距不符：{key}\n"
                f"  脚本读到的值：gap = {actual_gap:.1f}px\n"
                f"  visual_spec 期望值：{expected}px（允许 ±{TOLERANCE_PX}px 容差）\n"
                f"  解决方法：将 {nxt.name}.y 调整为 {curr.bottom + expected:.0f}px，"
                f"或检查 {curr.name}.height 是否正确。"
            )


# ── Detection B: sibling collision ────────────────────────────────────────────

def check_sibling_collision(
    file_key: str,
    hifi_frame_id: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    h_containers = find_horizontal_containers(file_key, hifi_frame_id)
    if not h_containers:
        warnings.append("检测 B：未找到水平排列容器，跳过碰撞检测。")
        return

    for container_id, children in h_containers:
        sorted_c = sorted(children, key=lambda n: n.x)
        for i in range(len(sorted_c) - 1):
            left, right = sorted_c[i], sorted_c[i + 1]
            if left.right > right.x:
                overlap = left.right - right.x
                errors.append(
                    f"FAIL — 子节点碰撞（容器 {container_id}）\n"
                    f"  脚本读到的值：{left.name}.right = {left.right:.1f}px，"
                    f"{right.name}.x = {right.x:.1f}px，重叠量 = {overlap:.1f}px\n"
                    f"  期望值：相邻兄弟节点 right_edge ≤ next_left（重叠量 = 0px）\n"
                    f"  解决方法：将 {right.name} 向右移动至少 {overlap:.0f}px，"
                    f"或缩短 {left.name} 的宽度以消除重叠。"
                )


# ── Detection C: module margins ───────────────────────────────────────────────

def check_module_margins(
    file_key: str,
    hifi_frame_id: str,
    expected_margin: int | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    if expected_margin is None:
        errors.append(
            "FAIL — 边距检测无法执行：visual_spec 未定义左右页边距\n"
            "  脚本读到的值：workspace/visual_specs/ 中所有文件均未找到 '左右页边距' 行\n"
            "  期望格式（visual_spec ## 页面级视觉属性 表格）：| 左右页边距 | 16px | ... |\n"
            "  解决方法：在 visual_spec 的页面级视觉属性表格中补充左右页边距定义。"
        )
        return

    children = fetch_children(file_key, hifi_frame_id)
    for module in children:
        # Full-width modules (x=0, width≈PAGE_WIDTH) skip margin check
        if module.x == 0 and abs(module.width - PAGE_WIDTH) <= 1:
            continue

        left_margin  = module.x
        right_margin = PAGE_WIDTH - module.right

        if abs(left_margin - expected_margin) > TOLERANCE_PX:
            errors.append(
                f"FAIL — 左边距不符：{module.name}\n"
                f"  脚本读到的值：{module.name}.x = {left_margin:.1f}px\n"
                f"  visual_spec 期望值：左边距 = {expected_margin}px（允许 ±{TOLERANCE_PX}px 容差）\n"
                f"  解决方法：将 {module.name}.x 设为 {expected_margin}px。"
            )

        if abs(right_margin - expected_margin) > TOLERANCE_PX:
            errors.append(
                f"FAIL — 右边距不符：{module.name}\n"
                f"  脚本读到的值：{module.name} 右边距 = {right_margin:.1f}px "
                f"（x={module.x:.1f} + width={module.width:.1f} = {module.right:.1f}，"
                f"PAGE_WIDTH={PAGE_WIDTH}）\n"
                f"  visual_spec 期望值：右边距 = {expected_margin}px（允许 ±{TOLERANCE_PX}px 容差）\n"
                f"  解决方法：调整 {module.name} 的宽度使右边距 = {expected_margin}px，"
                f"即 width = {PAGE_WIDTH - expected_margin - module.x:.0f}px。"
            )

        if module.right > PAGE_WIDTH + 1:
            errors.append(
                f"FAIL — 横向溢出：{module.name}\n"
                f"  脚本读到的值：x + width = {module.x:.1f} + {module.width:.1f} "
                f"= {module.right:.1f}px\n"
                f"  期望值：x + width ≤ {PAGE_WIDTH}px（hifi_generation_rules.md 固定约束）\n"
                f"  解决方法：缩短 {module.name} 的宽度，使 x + width ≤ {PAGE_WIDTH}px。"
            )


# ── Upstream gate status ──────────────────────────────────────────────────────

def load_upstream_status(run_id: str) -> dict[str, str]:
    gate_path = HARNESS_DIR / f"{run_id}_hifi_generation_gate.json"
    if not gate_path.exists():
        return {"hifi_generation": "MISSING"}
    data, errs = read_json(gate_path)
    if errs:
        return {"hifi_generation": "INVALID"}
    return {"hifi_generation": data.get("status", "UNKNOWN")}


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Figma Geometry Harness Gate (hifi_geometry)"
    )
    parser.add_argument("--run-id", required=True, help="Run id, e.g. run_001")
    parser.add_argument("--gate", default="hifi_geometry")
    args = parser.parse_args()

    run_id = args.run_id
    gate   = args.gate
    errors:   list[str] = []
    warnings: list[str] = []
    evidence_files: list[Path] = [
        WORKSPACE / "figma_targets.md",
        *sorted((WORKSPACE / "visual_specs").glob("*.md")),
    ]
    output_path = HARNESS_DIR / f"{run_id}_{gate}_gate.json"

    # Check upstream gate
    upstream = load_upstream_status(run_id)
    if upstream.get("hifi_generation") != "PASS":
        gate_result = make_result(
            run_id, gate, "BLOCKED",
            [f"upstream gate hifi_generation is not PASS "
             f"(status: {upstream.get('hifi_generation')})"],
            warnings, evidence_files, upstream,
        )
        write_json(output_path, gate_result)
        print(f"BLOCKED — {output_path}")
        return 1

    # Parse figma_targets.md
    try:
        targets = parse_figma_targets()
    except RuntimeError as exc:
        errors.append(str(exc))
        write_json(output_path, make_result(run_id, gate, "FAIL", errors, warnings, evidence_files, upstream))
        print(f"FAIL — {output_path}")
        return 1

    file_key     = targets["file_key"]
    hifi_page_id = targets["hifi_page_id"]

    # Parse visual_spec for expected values
    expected_gaps, expected_margin = parse_visual_spec_geometry(WORKSPACE / "visual_specs")

    # Discover hifi frame from page children (page ID is in figma_targets.md;
    # specific frame ID is discovered at runtime via REST API)
    try:
        page_frames = fetch_page_frames(file_key, hifi_page_id)
    except RuntimeError as exc:
        errors.append(str(exc))
        write_json(output_path, make_result(run_id, gate, "FAIL", errors, warnings, evidence_files, upstream))
        print(f"FAIL — {output_path}")
        return 1

    if not page_frames:
        errors.append(
            "FAIL — 高保真页面无 Frame\n"
            f"  脚本读到的值：page {hifi_page_id} 下无 FRAME 类型子节点\n"
            "  期望值：至少 1 个高保真 Frame\n"
            "  解决方法：确认高保真生成已完成，且 Frame 位于正确的 Figma 页面下。"
        )
        write_json(output_path, make_result(run_id, gate, "FAIL", errors, warnings, evidence_files, upstream))
        print(f"FAIL — {output_path}")
        return 1

    if len(page_frames) > 1:
        warnings.append(
            f"高保真页面包含 {len(page_frames)} 个 Frame："
            f"{', '.join(f.name for f in page_frames)}。"
            f"使用第一个：{page_frames[0].name}（{page_frames[0].node_id}）。"
        )

    hifi_frame    = page_frames[0]
    hifi_frame_id = hifi_frame.node_id
    warnings.append(f"检测目标 Frame：'{hifi_frame.name}'（{hifi_frame_id}）")

    # Run three detections
    try:
        check_vertical_gaps(file_key, hifi_frame_id, expected_gaps, errors, warnings)
        check_sibling_collision(file_key, hifi_frame_id, errors, warnings)
        check_module_margins(file_key, hifi_frame_id, expected_margin, errors, warnings)
    except RuntimeError as exc:
        errors.append(
            f"FAIL — Figma REST API 调用失败\n"
            f"  脚本读到的值：异常信息 = {exc}\n"
            f"  期望值：成功从 Figma 获取节点几何数据\n"
            f"  解决方法：检查 FIGMA_ACCESS_TOKEN 是否正确，网络是否可用，"
            f"以及 figma_targets.md 中的 node-id 是否有效。"
        )

    status = "FAIL" if errors else "PASS"
    write_json(output_path, make_result(run_id, gate, status, errors, warnings, evidence_files, upstream))
    print(f"{status} — {output_path}")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
