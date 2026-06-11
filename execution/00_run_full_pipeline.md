# Run Full Pipeline

## 目标

用一次执行完成从 PRD 到 Figma Wireframe、Structure Mapping、Design System、Visual Spec、Figma Hi-Fi、设计层、Layer Naming 和 Auto Layout 的端到端自动生成。Wireframe、Hi-Fi 和设计层中间结果不等待人工检查；只有 Harness Gate 失败、规则冲突或 Figma 输出端无法解析时才停止。

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/figma_targets.md（采样端链接、线框图输出端、高保真输出端和设计层输出端）
页面范围：全部 / 指定页面
生成模式：typical_state / full_state
```

## 执行前请读取

```text
docs/workflow.md
rules/intent_rules.md
rules/priority_rules.md
rules/layout_spec_rules.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/harness_rules.md
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

## 执行步骤

1. 检查 `workspace/PRD/` 中是否存在当前 PRD 文件。
2. 检查 `workspace/figma_targets.md` 中是否填写采样端链接、线框图输出端、高保真输出端和设计层输出端；采样端链接至少包含一条 `数字. Figma链接`，输出端必须包含 figma文件链接与 Page 名称或 pageID；pageID 可选，缺失时按 Page 名称唯一解析。
3. 全盘阅读 PRD，识别页面范围、页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型；如果用户未指定页面范围，默认处理全部页面。
4. 若 PRD 中存在原型图，所有后续阶段仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、可见文案、状态表达和 CTA 位置等界面表达与其他 PRD 内容或下游产物冲突时，作为最高优先级输入。
5. 对每个页面执行 Flow 01，生成 `workspace/intents/{page_id}.md`。
6. 执行 `python3 scripts/harness_check.py --run-id {run_id} --gate intent`；只有 `workspace/harness/{run_id}_intent_gate.json.status` 为 `PASS` 才能继续。
7. 对通过 Intent Gate 的页面执行 Flow 02，生成 `workspace/priority_maps/{page_id}.md`。
8. 执行 `python3 scripts/harness_check.py --run-id {run_id} --gate priority`；只有 `workspace/harness/{run_id}_priority_gate.json.status` 为 `PASS` 才能继续。
9. 对通过 Priority Gate 的页面执行 Flow 03，生成 `workspace/layout_specs/{page_id}.md`。
10. 执行 `python3 scripts/harness_check.py --run-id {run_id} --gate layout`；只有 `workspace/harness/{run_id}_layout_gate.json.status` 为 `PASS` 才能继续。
11. 执行 `python3 scripts/harness_check.py --run-id {run_id} --gate wireframe_preflight`；只有 `workspace/harness/{run_id}_wireframe_preflight_gate.json.status` 为 `PASS` 才能进入 Figma Wireframe 生成。
12. 只有通过 Wireframe Preflight Gate 的页面，才进入 Figma Wireframe 生成。
13. 按 `execution/wireframe_construction_method.md` 和 `rules/structure_preparation_rules.md` 生成 Figma Frame，保留后续组件、Token、Pattern 所需结构边界。
14. Figma Wireframe 生成和校验通过后，不等待人工验收，继续执行 Flow 05。
15. 执行 Flow 05 Structure Mapping，输出结构映射产物后必须执行 `python3 scripts/harness_check.py --run-id {run_id} --gate structure_mapping`；只有 `workspace/harness/{run_id}_structure_mapping_gate.json.status` 为 `PASS` 才能继续。
16. 执行 Flow 06 Design System Extraction，输出 Design System 产物后必须执行 `python3 scripts/harness_check.py --run-id {run_id} --gate design_system`；只有 `workspace/harness/{run_id}_design_system_gate.json.status` 为 `PASS` 才能继续。
17. 执行 Flow 07 Visual Spec，输出高保真设计指令后必须执行 `python3 scripts/harness_check.py --run-id {run_id} --gate visual_spec`；只有 `workspace/harness/{run_id}_visual_spec_gate.json.status` 为 `PASS` 才能继续。
18. 执行 Flow 08 Hi-Fi Generation，生成 Figma 高保真后必须执行 `python3 scripts/harness_check.py --run-id {run_id} --gate hifi_generation`；只有 `workspace/harness/{run_id}_hifi_generation_gate.json.status` 为 `PASS` 才能继续。
19. 执行 Flow 09 自动 Design System Backfill 和 Design Layer Publishing，将通过 Harness 的高保真结果复制或同步到设计层输出端，并执行 Backfill Harness Check；Backfill Gate 不得绕过上游 `hifi_generation` gate json。
20. 执行 Flow 10 Layer Naming Normalization，通过 Layer Naming Harness Gate 后继续；Layer Naming Gate 结论必须写入结构化 gate json，不能只写入 run record。
21. 执行 Flow 11 Auto Layout Backfill，通过 Auto Layout Harness Gate 后执行 Layer Naming Harness Recheck；Auto Layout Gate 结论必须写入结构化 gate json，不能只写入 run record。
22. 重跑时默认覆盖当前页面的 Intent、Priority Map、Layout Spec、Structure Mapping、Design System、Visual Spec、线框图输出端、高保真输出端和设计层输出端对应内容；只有用户明确要求保留旧版时才新建副本或追加版本。
23. 每完成一个阶段产物后立即落盘，避免中断后丢失进度。
24. 新增 `workspace/records/run_xxx.md`，记录输入、页面范围、Gate 结果、Figma 采样端、线框图输出端、高保真输出端、设计层输出端、Frame ID、停止点和变更；Gate 结果必须从 `workspace/harness/{run_id}_*_gate.json` 汇总，禁止手写 PASS。
25. 如果流程中断，尽可能写入或补写 run record，记录最后成功阶段、已生成文件、阻塞原因和恢复入口。

## 停止条件

```text
PRD 文件不存在。
线框图输出端 figma文件链接为空，或 Page 名称 / pageID 无法唯一解析。
采样端链接为空或不符合 `数字. Figma链接` 格式。
高保真输出端 figma文件链接为空，或 Page 名称 / pageID 无法唯一解析。
设计层输出端 figma文件链接为空，或 Page 名称 / pageID 无法唯一解析。
PRD 与下游产物发生冲突。
关键页面、关键状态或 PRD 硬约束遗漏。
下游产物凭空新增 PRD 未定义的核心业务能力。
Layout Spec 不足以生成一个页面状态一个 Frame 的线框图。
任一 Harness Gate 失败且无法在当前流程内自动修正。
缺少当前阶段对应的 workspace/harness/{run_id}_{gate}_gate.json。
上游 Gate 不是 PASS。
run record 中的 Gate 结果与 gate json 冲突。
```

## Run Record 必填字段

```text
run_id：
执行时间：
PRD 输入：
页面范围：
生成模式：
Figma 线框图输出端：
Figma 高保真输出端：
Figma 设计层输出端：
Figma 采样端：
Intent 输出：
Priority Map 输出：
Layout Spec 输出：
Structure Mapping 输出：
Design System 输出：
Visual Spec 输出：
Gate 结果：
Gate 结果来源：workspace/harness/{run_id}_*_gate.json
Figma Wireframe Frame ID：
Figma Hi-Fi Frame ID：
Figma 设计层 Frame ID：
Frame 名称：
停止点：端到端流程完成 / Gate 失败阶段
自动修正记录：
```

## 断点续跑字段

```text
执行状态：running / blocked / completed
最后成功阶段：
已生成产物：
未完成阶段：
阻塞原因：
恢复入口：
是否可复用已生成产物：
需要重跑的范围：
```

## 恢复策略

```text
恢复执行时，先读取最近一次相关 run record。
检查 workspace/intents、workspace/priority_maps、workspace/layout_specs、workspace/structure_mapping、workspace/design_system、workspace/visual_specs 中已存在的产物。
已通过 Gate 且未受上游修改影响的产物可以复用。
如果 PRD 或上游产物发生变化，受影响的下游产物必须重新生成。
恢复 Wireframe 生成前，必须重新执行 Wireframe Preflight Gate。
恢复到 Wireframe 之后不等待人工验收；若 Wireframe Gate 通过，继续执行后续阶段。
```

## 重跑策略

```text
Intent、Priority Map、Layout Spec、Structure Mapping、Design System、Visual Spec：默认覆盖当前最新产物。
Figma Wireframe：默认覆盖 `workspace/figma_targets.md` 中线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Figma Hi-Fi：默认覆盖高保真输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Figma 设计层：默认覆盖设计层输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Run Record：不得覆盖旧记录，每次执行必须新增 run_xxx.md。
旧版线框图、高保真和设计层：仅当用户明确要求保留时，才在 Figma 中新建副本或追加版本。
```
