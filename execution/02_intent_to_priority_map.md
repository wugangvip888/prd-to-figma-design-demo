# Intent to Priority Map

## 目标

基于 Intent 生成页面元素权重排序。

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
```

## 执行前请读取

```text
rules/intent_rules.md
rules/priority_rules.md
rules/harness_rules.md
```

## 输出

```text
workspace/priority_maps/{page_id}.md
```

## 执行步骤

1. 读取目标页面 Intent。
2. 回查 PRD 中当前页面的硬约束。
3. 列出页面可见元素、操作入口、状态反馈和背景/占位元素。
4. 按 P0/P1/P2/P3 分级并写明原因。
5. 检查 P0 是否对应 Intent 的视觉重心和首要动作。
6. 按 `rules/harness_rules.md` 执行 Priority Gate。
