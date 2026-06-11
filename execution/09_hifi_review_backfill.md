# Hi-Fi Backfill + Design Layer Publishing

## 目标

对高保真设计稿执行自动检查，将稳定、可复用的设计系统结论回填到 Design System 产物，并将通过 Harness 的高保真结果发布到设计层输出端。

本阶段不等待人工审核意见；只有 Harness 失败、采样冲突、规则冲突或输出端无法解析时才停止。本阶段不把单页临时调整沉淀为通用规则。

## 输入

```text
Figma 高保真设计稿
workspace/visual_specs/
workspace/design_system/
workspace/structure_mapping/
workspace/figma_targets.md
workspace/records/run_xxx_hifi_generation.md
Hi-Fi Generation Harness Check 结果
```

## 输出

```text
Figma 设计层输出端更新后的 Frame
更新后的 workspace/design_system/design-system-review.md
必要时更新 workspace/design_system/design-system-draft.json
必要时更新 workspace/design_system/manual-hifi-adjustment-rules.md
workspace/records/run_xxx_hifi_review_backfill.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/hifi_review_rules.md
rules/harness_rules.md
workspace/figma_targets.md
workspace/design_system/design-system-review.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
```

## 执行步骤

1. 汇总 Hi-Fi Generation 记录、Hi-Fi Generation Harness Check 结果、Visual Spec、Design System 和 Structure Mapping。
2. 读取 `workspace/figma_targets.md`，确认设计层输出端 figma文件链接、Page 名称或 pageID 可唯一解析。
3. 区分单页执行偏差、项目内同类页面可复用的自动调整、项目级设计系统结论和需要阻塞的冲突项。
4. 将项目内同类页面可复用但尚不适合进入跨项目 rules/ 的自动调整写入 `workspace/design_system/manual-hifi-adjustment-rules.md`。
5. 将项目级稳定设计系统结论回填到 design system 产物；未通过 Harness 或无法追溯来源的结论只写入 review，不升级为稳定结论。
6. 将通过 Harness 的高保真结果复制或同步到设计层输出端；设计层 Frame 尺寸、顺序和命名必须与高保真结果一致，并记录 design_layer_frame_id。
7. 执行 Backfill Harness Check。
8. 新增 `workspace/records/run_xxx_hifi_review_backfill.md`，记录高保真来源、设计层输出端、设计层 Frame ID、回填结论、阻塞项和 Gate 结果。
