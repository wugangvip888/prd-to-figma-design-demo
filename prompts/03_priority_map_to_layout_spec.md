# 03 Priority Map to Layout Spec

## 任务

读取 PRD、Intent 和 Priority Map，生成 Layout Spec。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/03_priority_map_to_layout_spec.md
rules/layout_spec_rules.md
rules/harness_rules.md
```

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
```

## 输出

```text
workspace/layout_specs/{page_id}.md
```

## 执行要求

1. 全盘阅读 PRD，识别当前页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型，同时参考 Intent 和 Priority Map。
2. 若 PRD 中存在原型图，仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、模块包含关系、可见文案、状态表达和 CTA 位置与正文概述、Intent 或 Priority Map 冲突时，作为最高优先级输入。
3. 将 Priority Map 中的元素组织为可见布局模块。
4. 每个模块必须标注 P0/P1/P2/P3。
5. 每个模块必须写清关键内容、frame_role、parent、children、component_candidate、component_reason 和 PRD 约束。
6. parent/children 必须形成可映射到 Figma 的 Frame 树，不得存在孤立模块、循环引用或无语义命名。
7. 如原型图与正文、Intent 或 Priority Map 冲突，按 `rules/layout_spec_rules.md` 的冲突处理规则标记。
8. 不写高保真视觉样式。
9. 按 `rules/harness_rules.md` 执行 Layout Gate。
