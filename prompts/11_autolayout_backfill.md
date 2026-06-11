# 11 Auto Layout Backfill

## 任务

为已确认的 Figma 高保真静态稿补齐 Auto Layout、constraints 和 layout sizing，并执行 Auto Layout Harness Gate。

本流程以保持原静态稿视觉结果为最高优先级，不重新设计页面。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/11_autolayout_backfill.md
rules/autolayout_rules.md
rules/hifi_generation_rules.md
rules/harness_rules.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 前置条件

```text
Layer Naming Harness Gate 必须已通过。
目标 Figma 范围必须明确。
静态稿关键节点 x / y / width / height 必须可读取。
```

## 放行要求

```text
必须通过 Auto Layout Harness Gate。
Auto Layout 修改后必须执行 Layer Naming Harness Recheck。
未通过 Auto Layout Harness Gate，不得进入交付。
未通过 Layer Naming Harness Recheck，回到 execution/10_layer_naming_normalization.md 修正命名。
```
