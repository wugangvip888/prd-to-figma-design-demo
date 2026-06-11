#!/usr/bin/env python3
"""Generate machine-owned Harness Gate results for the PRD-to-Figma pipeline."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
HARNESS_DIR = WORKSPACE / "harness"
NODE_ID_RE = re.compile(r"^\d+:\d+$")
STYLE_ID_REF_RE = re.compile(r"style_id:\s*([a-z][a-z0-9_]*)")
GENERATED_NODE_ID_RE = re.compile(r"generated_node_id:\s*(\d+:\d+)")
STYLE_DECISION_LEVELS = {"component_match", "priority_sampling", "structure_fallback"}
VISUAL_AUDIT_STATES = {"value", "none", "conflict", "not_applicable"}
VISUAL_AUDIT_CONTAINER_KEYS = [
    "background_fill",
    "gradient",
    "border_stroke",
    "radius",
    "shadow_effects",
]

ORDERED_GATES = [
    "intent",
    "priority",
    "layout",
    "wireframe_preflight",
    "wireframe_color_check",
    "structure_mapping",
    "design_system",
    "visual_spec",
    "hifi_generation",
    "hifi_geometry",
    "backfill",
    "layer_naming",
    "auto_layout",
    "layer_naming_recheck",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_json(path: Path) -> tuple[Any | None, list[str]]:
    if not path.exists():
        return None, [f"missing file: {rel(path)}"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"invalid json: {rel(path)}:{exc.lineno}:{exc.colno} {exc.msg}"]


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def result(
    run_id: str,
    gate: str,
    status: str,
    evidence_files: list[Path],
    blocking_errors: list[str],
    warnings: list[str] | None = None,
    upstream_gates: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "checked_by": "scripts/harness_check.py",
        "checked_at": now_iso(),
        "evidence_files": [rel(path) for path in evidence_files],
        "upstream_gates": upstream_gates or {},
        "blocking_errors": blocking_errors,
        "warnings": warnings or [],
    }


def parse_sampling_targets() -> list[dict[str, Any]]:
    path = WORKSPACE / "figma_targets.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    targets: list[dict[str, Any]] = []
    for match in re.finditer(r"^\s*(\d+)\.\s+(https://www\.figma\.com/design/\S+)", text, re.MULTILINE):
        priority = int(match.group(1))
        url = match.group(2)
        node_match = re.search(r"node-id=([0-9]+)-([0-9]+)", url)
        node_id = f"{node_match.group(1)}:{node_match.group(2)}" if node_match else ""
        targets.append({"sample_priority": priority, "sample_url": url, "node_id": node_id})
    return sorted(targets, key=lambda item: item["sample_priority"])


def md_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.md") if path.name != ".gitkeep")


def parse_priority_modules(levels: set[str]) -> set[str]:
    modules: set[str] = set()
    for path in md_files(WORKSPACE / "priority_maps"):
        current_level = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            level_match = re.match(r"^##\s+(P[0-3])\s*$", line.strip())
            if level_match:
                current_level = level_match.group(1)
                continue
            module_match = re.match(r"^###\s+(.+?)\s*$", line.strip())
            if module_match and current_level in levels:
                modules.add(module_match.group(1).strip().strip("`"))
    return modules


def required_child_visual_audit_keys(mapping: dict[str, Any]) -> list[str]:
    child_types = mapping.get("target_child_types")
    if not isinstance(child_types, list):
        return []
    text = " ".join(str(item).lower() for item in child_types)
    required: list[str] = []
    if any(token in text for token in ["text", "label", "title", "value", "copy", "placeholder", "subtitle"]):
        required.append("text_color")
    if any(token in text for token in ["icon", "arrow"]):
        required.append("icon_color")
    if any(token in text for token in ["button", "tag", "chip", "tab", "cta", "action", "control", "selected", "unselected"]):
        required.append("foreground_color")
    return required


def validate_visual_audit_entry(entry: Any, prefix: str, errors: list[str]) -> None:
    if not isinstance(entry, dict):
        errors.append(f"{prefix} must be an object with state")
        return
    state = entry.get("state")
    if state not in VISUAL_AUDIT_STATES:
        errors.append(f"{prefix}.state missing or invalid")
        return
    if state == "value" and entry.get("value") in ("", None, [], {}):
        errors.append(f"{prefix}.value missing for state=value")
    if state == "conflict" and not (isinstance(entry.get("reason"), str) and entry["reason"].strip()):
        errors.append(f"{prefix}.reason missing for state=conflict")


def has_manual_pass(text: str) -> bool:
    return bool(re.search(r"\bGate result\s*:\s*PASS\b|Gate\s*结果\s*[:：]\s*PASS|结论\s*[:：]\s*PASS", text))


def _parse_yaml_frontmatter(text: str) -> dict[str, Any] | None:
    """Return parsed frontmatter dict if file starts with ---, else None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fm_text = text[3:end].strip()
    try:
        import yaml  # pyyaml
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "PyYAML is required to parse YAML frontmatter. "
            "Run: python -m pip install -r requirements.txt"
        ) from exc
    try:
        parsed = yaml.safe_load(fm_text) or {}
    except Exception as exc:
        raise RuntimeError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("YAML frontmatter must parse to a mapping object")
    return parsed


def check_intent(run_id: str) -> dict[str, Any]:
    evidence = [WORKSPACE / "PRD", WORKSPACE / "intents"]
    errors: list[str] = []
    warnings_list: list[str] = []
    prd_files = md_files(WORKSPACE / "PRD")
    intent_files = md_files(WORKSPACE / "intents")
    if not prd_files:
        errors.append("workspace/PRD contains no .md files")
    if not intent_files:
        errors.append("workspace/intents contains no .md files")
    required_fields = ["page_goal", "primary_action", "secondary_entries", "key_states", "hard_constraints"]
    source_markers = ["PRD", "source", "来源", "原文", "段落"]
    for path in intent_files:
        text = path.read_text(encoding="utf-8")
        fname = rel(path)
        if has_manual_pass(text):
            errors.append(f"{fname} contains manual Gate PASS")
        try:
            fm = _parse_yaml_frontmatter(text)
        except RuntimeError as exc:
            errors.append(f"{fname}: {exc}")
            continue
        if fm is not None:
            for field in required_fields:
                field_data = fm.get(field)
                if not isinstance(field_data, dict):
                    errors.append(f"{fname} intent field {field} missing or not a mapping")
                    continue
                for sub in ("value", "prd_source"):
                    val = field_data.get(sub)
                    if not isinstance(val, str) or not val.strip():
                        errors.append(f"{fname} intent field {field}.{sub} missing or empty")
        else:
            warnings_list.append(f"{fname} is not structured YAML frontmatter, falling back to keyword check")
            for field in required_fields:
                if field not in text:
                    errors.append(f"{fname} missing intent field: {field}")
            if not any(marker in text for marker in source_markers):
                errors.append(f"{fname} missing PRD source references")
    return result(run_id, "intent", "FAIL" if errors else "PASS", evidence, errors, warnings_list)


def check_priority(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [WORKSPACE / "priority_maps", WORKSPACE / "intents", WORKSPACE / "PRD"]
    if upstream.get("intent") != "PASS":
        return result(
            run_id,
            "priority",
            "BLOCKED",
            evidence,
            ["upstream gate intent is not PASS"],
            upstream_gates=upstream,
        )
    errors: list[str] = []
    files = md_files(WORKSPACE / "priority_maps")
    if not files:
        errors.append("workspace/priority_maps contains no .md files")
    for path in files:
        text = path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(path)} contains manual Gate PASS")
        for priority in ["P0", "P1"]:
            if priority not in text:
                errors.append(f"{rel(path)} missing {priority} section")
        for marker in ["PRD", "Intent", "page_goal", "primary_action", "hard_constraints"]:
            if marker not in text:
                errors.append(f"{rel(path)} missing trace marker: {marker}")
    return result(run_id, "priority", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_layout(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [WORKSPACE / "layout_specs", WORKSPACE / "priority_maps", WORKSPACE / "intents", WORKSPACE / "PRD"]
    required = ["intent", "priority"]
    blockers = [f"upstream gate {gate} is not PASS" for gate in required if upstream.get(gate) != "PASS"]
    if blockers:
        return result(run_id, "layout", "BLOCKED", evidence, blockers, upstream_gates=upstream)
    errors: list[str] = []
    files = md_files(WORKSPACE / "layout_specs")
    if not files:
        errors.append("workspace/layout_specs contains no .md files")
    for path in files:
        text = path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(path)} contains manual Gate PASS")
        for marker in ["frame_role", "parent", "children", "component_candidate", "component_reason"]:
            if marker not in text:
                errors.append(f"{rel(path)} missing layout marker: {marker}")
        for marker in ["PRD", "Intent", "Priority"]:
            if marker not in text:
                errors.append(f"{rel(path)} missing upstream trace marker: {marker}")
    return result(run_id, "layout", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_wireframe_preflight(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [WORKSPACE / "layout_specs", WORKSPACE / "records" / f"{run_id}_full_pipeline.md"]
    required = ["intent", "priority", "layout"]
    blockers = [f"upstream gate {gate} is not PASS" for gate in required if upstream.get(gate) != "PASS"]
    if blockers:
        return result(run_id, "wireframe_preflight", "BLOCKED", evidence, blockers, upstream_gates=upstream)
    errors: list[str] = []
    record_path = evidence[1]
    if not record_path.exists():
        errors.append(f"missing file: {rel(record_path)}")
    else:
        text = record_path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(record_path)} contains manual Gate PASS")
        for marker in ["Wireframe", "Layout Spec", "PRD", "Figma Wireframe Frame ID"]:
            if marker not in text:
                errors.append(f"{rel(record_path)} missing preflight evidence marker: {marker}")
        if not re.search(r"Figma Wireframe Frame ID[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(record_path)} Figma Wireframe Frame ID must be followed by a valid node id (format n:n)")
    return result(run_id, "wireframe_preflight", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_wireframe_color_check(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    color_check_path = WORKSPACE / "records" / f"{run_id}_wireframe_color_check.md"
    evidence = [color_check_path]
    if upstream.get("wireframe_preflight") != "PASS":
        return result(run_id, "wireframe_color_check", "BLOCKED", evidence,
                      ["upstream gate wireframe_preflight is not PASS"], upstream_gates=upstream)
    errors: list[str] = []
    if not color_check_path.exists():
        errors.append(f"missing file: {rel(color_check_path)}")
        return result(run_id, "wireframe_color_check", "FAIL", evidence, errors, upstream_gates=upstream)

    text = color_check_path.read_text(encoding="utf-8")
    if has_manual_pass(text):
        errors.append(f"{rel(color_check_path)} contains manual Gate PASS")

    # 必须包含颜色清单 section
    if "## 颜色自检清单" not in text:
        errors.append(f"{rel(color_check_path)} missing '## 颜色自检清单' section")
        return result(run_id, "wireframe_color_check", "FAIL", evidence, errors, upstream_gates=upstream)

    # 解析清单行：格式 "- <node_name> fill: r=<R>, g=<G>, b=<B>"
    # 允许可选的 ✓ 或其他后缀
    fill_re = re.compile(
        r"^\s*-\s+\S.*fill:\s*r=([\d.]+),\s*g=([\d.]+),\s*b=([\d.]+)",
        re.MULTILINE,
    )
    gradient_re = re.compile(r"^\s*-\s+\S.*fill:\s*GRADIENT", re.MULTILINE | re.IGNORECASE)

    # 渐变填充在线框图阶段禁止
    for m in gradient_re.finditer(text):
        errors.append(f"gradient fill detected (forbidden in wireframe): {m.group().strip()}")

    # 灰阶约束：|r-g| < 0.05 且 |r-b| < 0.05
    THRESHOLD = 0.05
    for m in fill_re.finditer(text):
        r, g, b = float(m.group(1)), float(m.group(2)), float(m.group(3))
        if abs(r - g) >= THRESHOLD or abs(r - b) >= THRESHOLD:
            errors.append(
                f"non-grayscale fill detected (|r-g|={abs(r-g):.3f}, |r-b|={abs(r-b):.3f}): {m.group().strip()}"
            )

    # 清单不能为空（至少有一条记录）
    if not fill_re.search(text) and not gradient_re.search(text):
        errors.append(f"{rel(color_check_path)} 颜色清单为空，未找到任何 fill 记录")

    return result(run_id, "wireframe_color_check", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_structure_mapping(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    page_map_path = WORKSPACE / "structure_mapping" / "page-structure-map.json"
    component_index_path = WORKSPACE / "structure_mapping" / "component-index.json"
    evidence = [page_map_path, component_index_path]
    if upstream.get("wireframe_color_check") != "PASS":
        return result(
            run_id,
            "structure_mapping",
            "BLOCKED",
            evidence,
            ["upstream gate wireframe_color_check is not PASS"],
            upstream_gates=upstream,
        )

    page_map, page_errors = read_json(page_map_path)
    component_index, component_errors = read_json(component_index_path)
    errors = page_errors + component_errors
    warnings: list[str] = []

    if errors:
        return result(run_id, "structure_mapping", "FAIL", evidence, errors, warnings, upstream_gates=upstream)

    source_lookup: dict[str, dict[str, Any]] = {}
    for idx, candidate in enumerate(page_map.get("source_frame_candidates", [])):
        prefix = f"source_frame_candidates[{idx}]"
        node_id = candidate.get("source_node_id")
        if not isinstance(node_id, str) or NODE_ID_RE.match(node_id) is None:
            errors.append(f"{prefix}.source_node_id missing or invalid")
            continue
        source_lookup[node_id] = candidate
        if not isinstance(candidate.get("sample_priority"), int):
            errors.append(f"{prefix}.sample_priority missing or invalid")
        if not isinstance(candidate.get("sample_url"), str) or "figma.com" not in candidate["sample_url"]:
            errors.append(f"{prefix}.sample_url missing or invalid")

    for idx, mapping in enumerate(page_map.get("module_mappings", [])):
        prefix = f"module_mappings[{idx}]"
        source_node_id = mapping.get("source_candidate")
        unmapped_reason = mapping.get("unmapped_reason")
        if source_node_id:
            if not isinstance(source_node_id, str) or NODE_ID_RE.match(source_node_id) is None:
                errors.append(f"{prefix}.source_candidate missing valid Figma node id")
            candidate = source_lookup.get(source_node_id, {})
            priority = mapping.get("sample_priority", candidate.get("sample_priority"))
            url = mapping.get("sample_url", candidate.get("sample_url"))
            if not isinstance(priority, int):
                errors.append(f"{prefix} missing sample_priority")
            if not isinstance(url, str) or "figma.com" not in url:
                errors.append(f"{prefix} missing sample_url")
            required_comparison_fields = [
                "source_node_type",
                "source_frame_role",
                "target_frame_role",
                "source_child_types",
                "target_child_types",
                "source_business_semantic",
                "target_business_semantic",
                "structural_basis",
            ]
            for field in required_comparison_fields:
                if field not in mapping or mapping[field] in ("", [], None):
                    errors.append(f"{prefix}.{field} missing")
        elif not unmapped_reason:
            errors.append(f"{prefix} must have source_candidate or unmapped_reason")

    components = component_index.get("components", [])
    if not isinstance(components, list) or not components:
        errors.append("component-index.json components missing or empty")
    for idx, component in enumerate(components if isinstance(components, list) else []):
        prefix = f"components[{idx}]"
        if not isinstance(component.get("source_node_id"), str) or NODE_ID_RE.match(component["source_node_id"]) is None:
            errors.append(f"{prefix}.source_node_id missing or invalid")
        if not isinstance(component.get("source_sample_priority"), int):
            errors.append(f"{prefix}.source_sample_priority missing or invalid")
        if not isinstance(component.get("source_sample_url"), str) or "figma.com" not in component["source_sample_url"]:
            errors.append(f"{prefix}.source_sample_url missing or invalid")
        for field in [
            "source_node_type",
            "source_frame_role",
            "target_frame_role",
            "source_child_types",
            "target_child_types",
            "source_business_semantic",
            "target_business_semantic",
        ]:
            if field not in component or component[field] in ("", [], None):
                errors.append(f"{prefix}.{field} missing")

    return result(run_id, "structure_mapping", "FAIL" if errors else "PASS", evidence, errors, warnings, upstream_gates=upstream)


def check_design_system(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [
        WORKSPACE / "design_system" / "raw-style-inventory.json",
        WORKSPACE / "design_system" / "design-system-draft.json",
        WORKSPACE / "design_system" / "design-system-review.md",
        WORKSPACE / "structure_mapping" / "page-structure-map.json",
        WORKSPACE / "priority_maps",
    ]
    if upstream.get("structure_mapping") != "PASS":
        return result(
            run_id,
            "design_system",
            "BLOCKED",
            evidence,
            ["upstream gate structure_mapping is not PASS"],
            upstream_gates=upstream,
        )

    raw, raw_errors = read_json(evidence[0])
    draft, draft_errors = read_json(evidence[1])
    page_map, page_map_errors = read_json(WORKSPACE / "structure_mapping" / "page-structure-map.json")
    errors = raw_errors + draft_errors + page_map_errors
    if not evidence[2].exists():
        errors.append(f"missing file: {rel(evidence[2])}")

    if errors:
        return result(run_id, "design_system", "FAIL", evidence, errors, upstream_gates=upstream)

    raw_items = raw.get("items") if isinstance(raw, dict) else None
    raw_ids: set[str] = set()
    raw_items_by_source: dict[str, list[dict[str, Any]]] = {}
    if not isinstance(raw_items, list) or not raw_items:
        errors.append("raw-style-inventory.json items missing or empty")
    else:
        for idx, item in enumerate(raw_items):
            prefix = f"items[{idx}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id:
                errors.append(f"{prefix}.id missing or invalid")
            else:
                raw_ids.add(item_id)
            source_node_id = item.get("source_node_id")
            if not isinstance(source_node_id, str) or NODE_ID_RE.match(source_node_id) is None:
                errors.append(f"{prefix}.source_node_id missing or invalid")
            else:
                raw_items_by_source.setdefault(source_node_id, []).append(item)
            if not isinstance(item.get("sample_priority"), int):
                errors.append(f"{prefix}.sample_priority missing or invalid")
            sample_url = item.get("sample_url")
            if not isinstance(sample_url, str) or "figma.com" not in sample_url:
                errors.append(f"{prefix}.sample_url missing or invalid")
            decision_level = item.get("decision_level")
            if decision_level not in STYLE_DECISION_LEVELS:
                errors.append(f"{prefix}.decision_level missing or invalid")
            decision_reason = item.get("decision_reason")
            if decision_reason is not None and (not isinstance(decision_reason, str) or not decision_reason.strip()):
                errors.append(f"{prefix}.decision_reason must be a non-empty string when present")

    sampling_targets = parse_sampling_targets()
    _ = sampling_targets  # retained for future use

    priority_modules = parse_priority_modules({"P0", "P1", "P2"})
    module_mappings = page_map.get("module_mappings") if isinstance(page_map, dict) else None
    if not isinstance(module_mappings, list):
        errors.append("page-structure-map.json module_mappings missing or invalid")
    else:
        for idx, mapping in enumerate(module_mappings):
            if not isinstance(mapping, dict):
                continue
            target_module = mapping.get("target_module")
            source_candidate = mapping.get("source_candidate")
            if target_module not in priority_modules or not source_candidate:
                continue
            if not isinstance(source_candidate, str) or NODE_ID_RE.match(source_candidate) is None:
                continue
            audit_items = [
                item for item in raw_items_by_source.get(source_candidate, [])
                if isinstance(item.get("visual_audit"), dict)
            ]
            audit_prefix = f"module_mappings[{idx}] target_module={target_module} source_candidate={source_candidate}"
            if not audit_items:
                errors.append(f"{audit_prefix} missing raw-style-inventory visual_audit item")
                continue
            for item in audit_items:
                visual_audit = item.get("visual_audit")
                container = visual_audit.get("container") if isinstance(visual_audit, dict) else None
                children = visual_audit.get("children") if isinstance(visual_audit, dict) else None
                item_prefix = f"items id={item.get('id')} visual_audit"
                if not isinstance(container, dict):
                    errors.append(f"{item_prefix}.container missing or invalid")
                else:
                    for key in VISUAL_AUDIT_CONTAINER_KEYS:
                        if key not in container:
                            errors.append(f"{item_prefix}.container.{key} missing")
                        else:
                            validate_visual_audit_entry(container[key], f"{item_prefix}.container.{key}", errors)
                required_child_keys = required_child_visual_audit_keys(mapping)
                if required_child_keys:
                    if not isinstance(children, dict):
                        errors.append(f"{item_prefix}.children missing or invalid")
                    else:
                        for key in required_child_keys:
                            if key not in children:
                                errors.append(f"{item_prefix}.children.{key} missing")
                            else:
                                validate_visual_audit_entry(children[key], f"{item_prefix}.children.{key}", errors)

    styles = draft.get("styles") if isinstance(draft, dict) else None
    if not isinstance(styles, dict) or not styles:
        errors.append("design-system-draft.json styles missing or empty")
    else:
        for style_id, style_value in styles.items():
            if not isinstance(style_id, str) or not style_id:
                errors.append("styles contains an empty or non-string style_id")
                continue
            if "." in style_id:
                errors.append(f"styles.{style_id} must not contain '.'")
            if not isinstance(style_value, dict):
                errors.append(f"styles.{style_id} must be an object with value and source_ref")
                continue
            if "value" not in style_value or style_value.get("value") in ("", None):
                errors.append(f"styles.{style_id}.value missing")
            source_ref = style_value.get("source_ref")
            if not isinstance(source_ref, str) or not source_ref:
                errors.append(f"styles.{style_id}.source_ref missing")
            elif source_ref not in raw_ids:
                errors.append(f"styles.{style_id}.source_ref cannot be found in raw-style-inventory.json items")

    return result(
        run_id,
        "design_system",
        "FAIL" if errors else "PASS",
        evidence,
        errors,
        upstream_gates=upstream,
    )


def check_visual_spec(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [
        WORKSPACE / "visual_specs",
        WORKSPACE / "layout_specs",
        WORKSPACE / "priority_maps",
        WORKSPACE / "design_system" / "design-system-draft.json",
    ]
    required = ["structure_mapping", "design_system"]
    blockers = [f"upstream gate {gate} is not PASS" for gate in required if upstream.get(gate) != "PASS"]
    if blockers:
        return result(run_id, "visual_spec", "BLOCKED", evidence, blockers, upstream_gates=upstream)

    errors: list[str] = []
    draft, draft_errors = read_json(WORKSPACE / "design_system" / "design-system-draft.json")
    raw, raw_errors = read_json(WORKSPACE / "design_system" / "raw-style-inventory.json")
    errors.extend(draft_errors)
    errors.extend(raw_errors)
    style_ids: set[str] = set()
    raw_ids: set[str] = set()
    if isinstance(draft, dict) and isinstance(draft.get("styles"), dict):
        style_ids = {key for key in draft["styles"] if isinstance(key, str)}
    if isinstance(raw, dict) and isinstance(raw.get("items"), list):
        raw_ids = {item.get("id") for item in raw["items"] if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if isinstance(draft, dict) and isinstance(draft.get("styles"), dict):
        for style_id, style_value in draft["styles"].items():
            if not isinstance(style_id, str) or not style_id.startswith("asset_"):
                continue
            if not isinstance(style_value, dict):
                errors.append(f"styles.{style_id} must be an object with source_ref")
                continue
            source_ref = style_value.get("source_ref")
            if not isinstance(source_ref, str) or not source_ref:
                errors.append(f"styles.{style_id}.source_ref missing")
            elif source_ref not in raw_ids:
                errors.append(f"styles.{style_id}.source_ref cannot be found in raw-style-inventory.json items")
    visual_files = sorted((WORKSPACE / "visual_specs").glob("*.md"))
    if not visual_files:
        errors.append("workspace/visual_specs contains no .md files")
    for path in visual_files:
        text = path.read_text(encoding="utf-8")
        for required_text in ["Design System", "Priority", "Layout Spec"]:
            if required_text not in text:
                errors.append(f"{rel(path)} missing upstream trace marker: {required_text}")
        for style_id in STYLE_ID_REF_RE.findall(text):
            if style_id not in style_ids:
                errors.append(f"{rel(path)} references undefined style_id: {style_id}")
        if "待人工确认" in text and not (WORKSPACE / "design_system" / "design-system-review.md").exists():
            errors.append(f"{rel(path)} has pending confirmation but design-system-review.md is missing")
    return result(run_id, "visual_spec", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_hifi_generation(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [
        WORKSPACE / "records" / f"{run_id}_full_pipeline.md",
        WORKSPACE / "visual_specs",
    ]
    required = ["structure_mapping", "design_system", "visual_spec"]
    blockers = [f"upstream gate {gate} is not PASS" for gate in required if upstream.get(gate) != "PASS"]
    if blockers:
        return result(run_id, "hifi_generation", "BLOCKED", evidence, blockers, upstream_gates=upstream)

    record_path = evidence[0]
    errors: list[str] = []
    warnings: list[str] = []
    draft, draft_errors = read_json(WORKSPACE / "design_system" / "design-system-draft.json")
    errors.extend(draft_errors)
    has_asset_style = False
    if isinstance(draft, dict) and isinstance(draft.get("styles"), dict):
        has_asset_style = any(isinstance(key, str) and key.startswith("asset_") for key in draft["styles"])
    if not record_path.exists():
        errors.append(f"missing file: {rel(record_path)}")
    else:
        text = record_path.read_text(encoding="utf-8")
        required_markers = [
            "Figma Hi-Fi Frame ID",
            "Visual Spec",
            "采样端",
            "资产",
        ]
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{rel(record_path)} missing Hi-Fi evidence marker: {marker}")
        if not re.search(r"Figma Hi-Fi Frame ID[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(record_path)} Figma Hi-Fi Frame ID must be followed by a valid node id (format n:n)")
        if not STYLE_ID_REF_RE.search(text):
            warnings.append(f"{rel(record_path)} contains no style_id color traceability records")
        if has_asset_style and not GENERATED_NODE_ID_RE.search(text):
            errors.append(f"{rel(record_path)} missing generated_node_id for asset style traceability")
    return result(run_id, "hifi_generation", "FAIL" if errors else "PASS", evidence, errors, warnings, upstream_gates=upstream)


def check_hifi_geometry(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    gate_json_path = HARNESS_DIR / f"{run_id}_hifi_geometry_gate.json"
    evidence = [gate_json_path]
    if upstream.get("hifi_generation") != "PASS":
        return result(
            run_id,
            "hifi_geometry",
            "BLOCKED",
            evidence,
            ["upstream gate hifi_generation is not PASS"],
            upstream_gates=upstream,
        )
    if not gate_json_path.exists():
        import subprocess, sys
        script = Path(__file__).parent / "figma_geometry_check.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--run-id", run_id, "--gate", "hifi_geometry"],
            capture_output=True, text=True
        )
        if proc.returncode != 0 or not gate_json_path.exists():
            return result(
                run_id, "hifi_geometry", "FAIL", [str(script)],
                [f"figma_geometry_check.py exited {proc.returncode}: {proc.stderr.strip()}"],
                upstream_gates=upstream,
            )
    data, read_errors = read_json(gate_json_path)
    if read_errors or not isinstance(data, dict):
        return result(
            run_id, "hifi_geometry", "FAIL", evidence,
            read_errors or ["geometry gate JSON is not a valid object"],
            upstream_gates=upstream,
        )
    status = data.get("status", "FAIL")
    blocking_errors = data.get("blocking_errors", [])
    warnings = data.get("warnings", [])
    return result(run_id, "hifi_geometry", status, evidence, blocking_errors, warnings, upstream_gates=upstream)


def check_backfill(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    evidence = [
        WORKSPACE / "records" / f"{run_id}_hifi_review_backfill.md",
        WORKSPACE / "records" / f"{run_id}_full_pipeline.md",
        WORKSPACE / "harness" / f"{run_id}_hifi_geometry_gate.json",
    ]
    if upstream.get("hifi_geometry") != "PASS":
        return result(
            run_id,
            "backfill",
            "BLOCKED",
            evidence,
            ["upstream gate hifi_geometry is not PASS"],
            upstream_gates=upstream,
        )
    errors: list[str] = []
    record_path = evidence[0]
    full_record_path = evidence[1]
    for path in [record_path, full_record_path]:
        if not path.exists():
            errors.append(f"missing file: {rel(path)}")
    if record_path.exists():
        text = record_path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(record_path)} contains manual Gate PASS")
        for marker in ["高保真 Frame", "设计层 Frame", "scope=single_page", "不写入 rules/"]:
            if marker not in text:
                errors.append(f"{rel(record_path)} missing backfill marker: {marker}")
        if not re.search(r"高保真 Frame[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(record_path)} missing valid Hi-Fi node id")
        if not re.search(r"设计层 Frame[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(record_path)} missing valid design layer node id")
    if full_record_path.exists():
        text = full_record_path.read_text(encoding="utf-8")
        if not re.search(r"Figma Hi-Fi Frame ID[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(full_record_path)} missing valid Figma Hi-Fi Frame ID")
        if not re.search(r"Figma 设计层 Frame ID[^\n]*?(\d+:\d+)", text):
            errors.append(f"{rel(full_record_path)} missing valid Figma design layer Frame ID")
    return result(run_id, "backfill", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def _check_layer_naming_common(run_id: str, gate: str, upstream: dict[str, str], required_upstream: str) -> dict[str, Any]:
    scan_path = WORKSPACE / "harness" / f"{run_id}_{gate}_scan.json"
    record_path = WORKSPACE / "records" / f"{run_id}_layer_naming.md"
    evidence = [scan_path, record_path]
    if upstream.get(required_upstream) != "PASS":
        return result(
            run_id,
            gate,
            "BLOCKED",
            evidence,
            [f"upstream gate {required_upstream} is not PASS"],
            upstream_gates=upstream,
        )
    errors: list[str] = []
    scan, scan_errors = read_json(scan_path)
    errors.extend(scan_errors)
    if not record_path.exists():
        errors.append(f"missing file: {rel(record_path)}")
    else:
        text = record_path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(record_path)} contains manual Gate PASS")
        for marker in ["默认 Figma 名称：0", "中文 frame-like 名称：0", "source_ 前缀：0"]:
            if marker not in text:
                errors.append(f"{rel(record_path)} missing naming marker: {marker}")
    if isinstance(scan, dict):
        for key in ["default_name_count", "chinese_frame_like_count", "source_prefix_count", "invalid_snake_case_count"]:
            val = scan.get(key)
            if not isinstance(val, int):
                errors.append(f"{rel(scan_path)}.{key} missing or invalid")
            elif val != 0:
                errors.append(f"{rel(scan_path)}.{key} must be 0, got {val}")
        if not scan.get("target_frame_ids"):
            errors.append(f"{rel(scan_path)}.target_frame_ids missing")
    return result(run_id, gate, "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_layer_naming(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    return _check_layer_naming_common(run_id, "layer_naming", upstream, "backfill")


def check_auto_layout(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    scan_path = WORKSPACE / "harness" / f"{run_id}_auto_layout_scan.json"
    record_path = WORKSPACE / "records" / f"{run_id}_autolayout_backfill.md"
    rules_path = ROOT / "rules" / "autolayout_rules.md"
    api_check_path = WORKSPACE / "harness" / f"{run_id}_autolayout_check.json"
    evidence = [scan_path, record_path, rules_path, api_check_path]
    if upstream.get("layer_naming") != "PASS":
        return result(
            run_id,
            "auto_layout",
            "BLOCKED",
            evidence,
            ["upstream gate layer_naming is not PASS"],
            upstream_gates=upstream,
        )
    errors: list[str] = []
    scan, scan_errors = read_json(scan_path)
    errors.extend(scan_errors)
    if not record_path.exists():
        errors.append(f"missing file: {rel(record_path)}")
    else:
        text = record_path.read_text(encoding="utf-8")
        if has_manual_pass(text):
            errors.append(f"{rel(record_path)} contains manual Gate PASS")
        required_markers = [
            "Auto Layout 结构调整边界",
            "metadata",
            "screenshot",
            "absolute positioning 扫描结果",
            "临时测试副本已删除",
        ]
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{rel(record_path)} missing auto layout marker: {marker}")
    if isinstance(scan, dict):
        for key in ["layout_none_count", "absolute_count", "temp_layer_count", "local_absolute_path_count"]:
            val = scan.get(key)
            if not isinstance(val, int):
                errors.append(f"{rel(scan_path)}.{key} missing or invalid")
            elif val != 0:
                errors.append(f"{rel(scan_path)}.{key} must be 0, got {val}")
        if scan.get("screenshot_checked") is not True:
            errors.append(f"{rel(scan_path)}.screenshot_checked must be true")
        if scan.get("stretch_test_deleted") is not True:
            errors.append(f"{rel(scan_path)}.stretch_test_deleted must be true")
        if not scan.get("target_frame_id"):
            errors.append(f"{rel(scan_path)}.target_frame_id missing")
    # --- Mechanical API check (figma_autolayout_check.py) ---
    # If the check JSON exists, read it and fail if failed_nodes is non-empty.
    # If it doesn't exist yet, emit a warning (not a hard error) so legacy runs
    # that predate the script are not retroactively broken; new runs should
    # always produce this file before running the gate.
    api_check, api_errors = read_json(api_check_path)
    if api_errors:
        errors.append(
            f"missing mechanical check file: {rel(api_check_path)} — "
            "run: python scripts/figma_autolayout_check.py --run-id "
            f"{run_id} --page-frame-id <page_frame_id>"
        )
    elif isinstance(api_check, dict):
        api_status = api_check.get("status", "FAIL")
        failed_nodes = api_check.get("failed_nodes", [])
        if api_status == "FAIL" or failed_nodes:
            for node in failed_nodes:
                errors.append(
                    f"layoutMode=NONE: [{node.get('depth', '?')}] "
                    f"{node.get('id', '?')}  {node.get('name', '?')}"
                )
            if not failed_nodes and api_status == "FAIL":
                api_error = api_check.get("error", "unknown error")
                errors.append(f"figma_autolayout_check.py reported FAIL: {api_error}")
    return result(run_id, "auto_layout", "FAIL" if errors else "PASS", evidence, errors, upstream_gates=upstream)


def check_layer_naming_recheck(run_id: str, upstream: dict[str, str]) -> dict[str, Any]:
    return _check_layer_naming_common(run_id, "layer_naming_recheck", upstream, "auto_layout")


CHECKERS = {
    "intent": check_intent,
    "priority": check_priority,
    "layout": check_layout,
    "wireframe_preflight": check_wireframe_preflight,
    "wireframe_color_check": check_wireframe_color_check,
    "structure_mapping": check_structure_mapping,
    "design_system": check_design_system,
    "visual_spec": check_visual_spec,
    "hifi_generation": check_hifi_generation,
    "hifi_geometry": check_hifi_geometry,
    "backfill": check_backfill,
    "layer_naming": check_layer_naming,
    "auto_layout": check_auto_layout,
    "layer_naming_recheck": check_layer_naming_recheck,
}


def run_gate(run_id: str, gate: str, statuses: dict[str, str]) -> dict[str, Any]:
    checker = CHECKERS[gate]
    if gate == "intent":
        gate_result = checker(run_id)
    else:
        gate_result = checker(run_id, dict(statuses))
    output_path = HARNESS_DIR / f"{run_id}_{gate}_gate.json"
    write_json(output_path, gate_result)
    statuses[gate] = gate_result["status"]
    return gate_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PRD-to-Figma Harness Gate checks.")
    parser.add_argument("--run-id", required=True, help="Run id, for example run_001")
    parser.add_argument("--gate", choices=ORDERED_GATES + ["all"], default="all")
    args = parser.parse_args()

    gates = ORDERED_GATES if args.gate == "all" else [args.gate]
    statuses: dict[str, str] = {}

    if args.gate != "all":
        gate_index = ORDERED_GATES.index(args.gate)
        for upstream_gate in ORDERED_GATES[:gate_index]:
            path = HARNESS_DIR / f"{args.run_id}_{upstream_gate}_gate.json"
            existing, errors = read_json(path)
            statuses[upstream_gate] = "MISSING" if errors else existing.get("status", "MISSING")

    results = [run_gate(args.run_id, gate, statuses) for gate in gates]
    summary = {
        "run_id": args.run_id,
        "checked_by": "scripts/harness_check.py",
        "checked_at": now_iso(),
        "statuses": {item["gate"]: item["status"] for item in results},
        "gate_files": [rel(HARNESS_DIR / f"{args.run_id}_{item['gate']}_gate.json") for item in results],
    }
    write_json(HARNESS_DIR / f"{args.run_id}_gate_summary.json", summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(item["status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
