# 02 Intent to Priority Map

## 任务

读取页面 Intent，并生成页面元素权重排序。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/02_intent_to_priority_map.md
rules/priority_rules.md
rules/harness_rules.md
```

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
```

## 输出

```text
workspace/priority_maps/{page_id}.md
```

## 执行要求

1. 从 Intent 中识别页面目标、视觉重心和主要操作。
2. 从 PRD 中补充必须出现的页面元素和硬约束。
3. 将元素分为 P0/P1/P2/P3。
4. 每个元素必须写明分级原因。
5. 按 `rules/harness_rules.md` 执行 Priority Gate。
