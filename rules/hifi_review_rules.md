# Hi-Fi Backfill Rules

## 目标

定义高保真自动检查、设计层发布和设计系统回填规则。

## 回填原则

```text
单页临时调整只记录在 run record 或 visual_spec。
项目内可复用的稳定结论可回填到 workspace/design_system/。
项目内同类页面可复用、但尚不适合进入跨项目 rules/ 的高保真自动调整，必须记录到 workspace/design_system/manual-hifi-adjustment-rules.md。
跨项目可复用的判断方法才可回填到 rules/。
自动检查结论必须记录来源、影响范围、Harness 证据和是否需要重跑。
```

## 截图视觉对比回填规则

```text
截图视觉对比结论必须先判断偏差类型，再决定回填位置。

结构正确但单页视觉偏离：
优先修正当前页面 Hi-Fi 或 workspace/visual_specs/{page_id}.md，只记录到 run record；不得直接升级为项目级设计系统规则。

多页面重复出现的视觉偏离：
视为 Design System 草案缺口或表达不足，进入 workspace/design_system/design-system-review.md；只有来源可追溯且通过 Harness 的结论才可更新 design-system-draft.json。

Visual Spec 未明确导致的执行偏差：
先回补对应页面 Visual Spec，再重跑 Hi-Fi；不得只在高保真稿中临场修正。

设计系统与采样源截图明显冲突：
必须标注冲突来源、影响范围和阻塞项；冲突解决前不得覆盖既有 Design System 结论。

截图视觉对比只能沉淀判断方法，不能把单张截图中的页面事实、业务文案、临时模块位置或一次性风格偏好写入 rules/。
```

## 禁止事项

```text
不得把一次性页面事实沉淀为通用规则。
不得覆盖未经影响评估的 design system 结论。
不得跳过 Backfill Harness Check。
```
