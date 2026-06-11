# 00 Run Full Pipeline

## 任务

从 `workspace/PRD/` 中的当前 PRD 文件开始，自动完成：

```text
PRD
→ Intent
→ Intent Gate
→ Priority Map
→ Priority Gate
→ Layout Spec
→ Layout Gate
→ Wireframe Preflight Gate
→ Figma Wireframe
→ Structure Mapping
→ Structure Mapping Harness Check
→ Design System Extraction
→ Design System Harness Check
→ Visual Spec
→ Visual Spec Harness Check
→ Figma Hi-Fi
→ Hi-Fi Generation Harness Check
→ Design Layer Publishing
→ Backfill Harness Check
→ Layer Naming Harness Gate
→ Auto Layout Harness Gate
→ Layer Naming Harness Recheck
→ Run Record
```

自动执行边界：本入口从 PRD 自动执行到设计层交付完成。Wireframe、Hi-Fi 和设计层中间结果不等待人工检查；每个阶段必须执行对应 Harness Gate，Gate 失败或规则冲突时才停止并写入 run record。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/00_run_full_pipeline.md
execution/01_prd_to_intent.md
execution/02_intent_to_priority_map.md
execution/03_priority_map_to_layout_spec.md
execution/04_layout_spec_to_wireframe.md
execution/05_structure_mapping.md
execution/06_design_system_extraction.md
execution/07_visual_spec.md
execution/08_hifi_generation.md
execution/09_hifi_review_backfill.md
execution/10_layer_naming_normalization.md
execution/11_autolayout_backfill.md
execution/wireframe_construction_method.md
rules/intent_rules.md
rules/priority_rules.md
rules/layout_spec_rules.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/structure_mapping_rules.md
rules/design_system_rules.md
rules/visual_spec_rules.md
rules/hifi_generation_rules.md
rules/hifi_review_rules.md
rules/autolayout_rules.md
rules/harness_rules.md
```

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/figma_targets.md（采样端链接、线框图输出端、高保真输出端和设计层输出端）
页面范围：全部 / 指定页面
生成模式：typical_state / full_state
```

## 输出

```text
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/layout_specs/{page_id}.md
workspace/structure_mapping/
workspace/design_system/
workspace/visual_specs/{page_id}.md
Figma 中更新后的线框图 Frame
Figma 中更新后的高保真 Frame
Figma 中更新后的设计层 Frame
workspace/records/run_xxx.md
```

## 执行要求

1. 自动识别当前 PRD 文件和页面范围。
2. 全盘阅读 PRD，识别页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型。
3. 若 PRD 中存在原型图，所有后续阶段仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、可见文案、状态表达和 CTA 位置等界面表达与其他 PRD 内容或下游产物冲突时，作为最高优先级输入。
4. 按 Flow 01 生成 Intent，并执行 Intent Gate。
5. 按 Flow 02 生成 Priority Map，并执行 Priority Gate。
6. 按 Flow 03 生成 Layout Spec，并执行 Layout Gate。
7. 读取 `workspace/figma_targets.md`，确认采样端链接至少有一条 `数字. Figma链接`，并确认线框图输出端、高保真输出端和设计层输出端均已填写 figma文件链接与 Page 名称或 pageID；pageID 可选，缺失时按 Page 名称唯一解析。
8. 按 Flow 04 执行 Wireframe Preflight Gate。
9. 只有全部 Gate 通过，才生成 Figma Wireframe，并按 `rules/structure_preparation_rules.md` 保留后续组件、Token、Pattern 所需结构边界。
10. Wireframe 生成和校验通过后，不等待人工验收，继续执行 Flow 05 Structure Mapping。
11. 按 Flow 06 提取 Design System，按 Flow 07 生成 Visual Spec，按 Flow 08 生成 Figma Hi-Fi；每步完成后执行对应 Harness Check。
12. 按 Flow 09 执行自动 Design System Backfill 和 Design Layer Publishing：将通过 Harness 的高保真结果复制或同步到设计层输出端，并记录设计层 Frame ID。
13. 按 Flow 10 执行 Layer Naming Harness Gate，按 Flow 11 执行 Auto Layout Harness Gate，并执行 Layer Naming Harness Recheck。
14. 生成完成后新增 run record，记录输入、输出、Figma 采样端、线框图输出端、高保真输出端、设计层输出端、各阶段 Frame ID、Gate 结果、停止点和变更记录。
15. 任一 Gate 发现 PRD 冲突、关键遗漏、凭空新增、采样冲突无法裁定或 Figma 输出端不可解析时，停止后续步骤，并在 run record 或执行摘要中记录阻塞原因。
16. 每完成一个阶段产物后立即落盘；如果流程中断，必须在 run record 或执行摘要中记录最后成功阶段和恢复入口。
17. 恢复执行时，先读取最近一次相关 run record 和已存在产物，复用已通过 Gate 且未受上游修改影响的产物。
