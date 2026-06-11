# PRD to Intent

## 目标

从 PRD 为每个页面生成 Intent。

## 输入

```text
workspace/PRD/{prd_file}.md
```

## 执行前请读取

```text
docs/workflow.md
rules/intent_rules.md
rules/harness_rules.md
```

## 输出

```text
workspace/intents/{page_id}.md
```

## 执行步骤

1. 全盘阅读 PRD，识别页面名称、页面数量、页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型。
2. 若 PRD 中存在原型图，仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、可见文案、关键状态和 CTA 判断与正文概述冲突时，作为最高优先级输入。
3. 针对每个页面提取页面目标、用户首要任务、主操作、次要入口、关键状态和 PRD 硬约束。
4. 如原型图与正文冲突，按 `rules/intent_rules.md` 的冲突处理规则标记。
5. 按 `rules/intent_rules.md` 的固定字段生成 Intent。
6. 执行 PRD → Intent 强约束自检。
7. 按 `rules/harness_rules.md` 执行 Intent Gate。
8. 写入 `workspace/intents/`。
