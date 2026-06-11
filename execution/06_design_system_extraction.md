# Design System Extraction

## 目标

从采样端 Figma 来源和 Structure Mapping 结果中提取当前模块可复用的设计系统草案。

本阶段输出真实样式清单、AI 归纳草案和人工审核清单；未经审核的草案不得视为最终设计系统。

## 输入

```text
workspace/structure_mapping/component-index.json
workspace/structure_mapping/page-structure-map.json
workspace/structure_mapping/mapping-review.md
workspace/figma_targets.md
采样端链接优先级列表
```

## 输出

```text
workspace/design_system/raw-style-inventory.json
workspace/design_system/design-system-draft.json
workspace/design_system/design-system-review.md
workspace/records/run_xxx_design_system_extraction.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/design_system_rules.md
rules/harness_rules.md
workspace/structure_mapping/component-index.json
workspace/structure_mapping/page-structure-map.json
workspace/structure_mapping/mapping-review.md
```

## 执行步骤

1. 读取 Structure Mapping 产物和 `workspace/figma_targets.md` 中采样端链接优先级列表；数字越小优先级越高，同一数字内链接权重相同。
2. 按采样端链接优先级升序采集样式证据；仅当前一层级缺少目标界面所需组件、状态、样式或布局证据时，才降级读取后续数字层级，并记录降级来源和原因。
3. 采集真实样式、Auto Layout、尺寸、间距、圆角、描边、阴影、字号和层级结构，写入 `raw-style-inventory.json`。
4. 按线框图实际用到的样式生成按需样式草案，写入 `design-system-draft.json`。每条样式用 style_id 命名（如 color_page_bg、radius_card），必须有 source_ref 指向 raw-style-inventory.items.id。不得归纳线框图未用到的样式，禁止使用全局语义 token 命名。
5. 结合 Priority Map 和 Layout Spec，在 `design-system-review.md` 中标注哪些样式对应高优先级模块，供 Visual Spec 参考。不得在 draft 中硬编码权重分级。
6. 将低置信度归纳、样式冲突、组件边界不清、业务语义不匹配和需要人工确认项写入 `design-system-review.md`。
7. 执行 Design System Harness Check。
8. 新增 `workspace/records/run_xxx_design_system_extraction.md`，记录采样优先级、采样链接、降级原因、冲突项和人工确认项。
