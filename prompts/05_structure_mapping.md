# 05 Structure Mapping

## 任务

读取 Wireframe、采样端 Figma 来源和上游业务产物，建立结构映射，输出 Structure Mapping 产物并执行 Structure Mapping Harness Check。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/05_structure_mapping.md
rules/structure_mapping_rules.md
rules/structure_preparation_rules.md
rules/harness_rules.md
```

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/layout_specs/{page_id}.md
workspace/figma_targets.md
线框图输出端 figma文件链接与 Page 名称或 pageID
采样端链接优先级列表
本次映射页面范围
```

## 输出

```text
workspace/structure_mapping/component-index.json
workspace/structure_mapping/page-structure-map.json
workspace/structure_mapping/mapping-review.md
workspace/records/run_xxx_structure_mapping.md
```

## 执行要求

1. 读取 Wireframe 前必须确认其保留 Page Frame → Module Frame → Control Frame → Element 层级。
2. 读取采样端 Figma 来源时，按 `workspace/figma_targets.md` 中采样端链接的数字优先级升序读取；同一数字内链接权重相同，按书写顺序读取；仅当前一层级不足以支撑目标界面结构、组件、状态或样式判断时，才降级读取后续数字层级。
3. 如存在大量散落 Text、Rectangle、Frame 1、Group 1，停止本阶段并回到 Wireframe 整理。
4. 按 module_* 和 control_* 边界建立结构映射，不得从散落节点或纯视觉组合中生成组件候选。
5. 组件候选只能来自稳定的 Module Frame 或 Control Frame。
6. 按 `rules/harness_rules.md` 执行 Structure Mapping Harness Check。
