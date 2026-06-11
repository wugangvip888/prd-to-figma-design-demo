# Priority Map to Layout Spec

## 目标

将页面 Intent 和 Priority Map 转成可生成线框图的 Layout Spec。

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
```

## 执行前请读取

```text
rules/priority_rules.md
rules/layout_spec_rules.md
rules/harness_rules.md
```

## 输出

```text
workspace/layout_specs/{page_id}.md
```

## 执行步骤

1. 全盘阅读 PRD，识别当前页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型，同时读取 Intent 和 Priority Map。
2. 若 PRD 中存在原型图，仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、模块包含关系、可见文案、状态表达和 CTA 位置与正文概述、Intent 或 Priority Map 冲突时，作为最高优先级输入。
3. 将 P0/P1/P2/P3 元素组织为可见布局模块。
4. 为每个模块写入模块 ID、权重、位置或属性、关键内容描述、frame_role、parent、children、component_candidate、component_reason 和 PRD 约束。
5. 确认 parent/children 形成可映射到 Figma 的 Frame 树，不存在孤立模块、循环引用或无语义命名。
6. 如原型图与正文、Intent 或 Priority Map 冲突，按 `rules/layout_spec_rules.md` 的冲突处理规则标记。
7. 检查 Priority Map 中的元素是否被覆盖或明确排除。
8. 检查 Layout Spec 是否足以生成 Figma 线框图。
9. 按 `rules/harness_rules.md` 执行 Layout Gate。
