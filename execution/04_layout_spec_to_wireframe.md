# Layout Spec to Wireframe

## 目标

读取 PRD、Intent、Priority Map 和 Layout Spec，先完成 Wireframe Preflight Gate，再在 Figma 中生成线框图。

## 输入

```text
workspace/layout_specs/{page_id}.md
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/figma_targets.md
线框图输出端 figma文件链接
线框图输出端 Page 名称或 pageID
本次生成页面范围
生成模式：typical_state / full_state
```

## 执行前请读取

```text
rules/layout_spec_rules.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/harness_rules.md
execution/wireframe_construction_method.md
```

## 输出

```text
Figma 中更新后的线框图 Frame
新 Frame ID
workspace/records/run_xxx.md
```

## 执行步骤

1. 读取 Layout Spec、wireframe_rules、structure_preparation_rules 和 wireframe_construction_method。
2. 读取 `workspace/figma_targets.md`，确认线框图输出端 figma文件链接和 Page 名称；pageID 可选。
3. 全盘阅读 PRD，识别当前页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型，同时读取 Intent 和 Priority Map，按 `rules/harness_rules.md` 执行 Wireframe Preflight Gate。
4. 若 PRD 中存在原型图，仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、模块包含关系、可见文案、状态表达、CTA 位置和控件相对位置与正文概述、Intent、Priority Map 或 Layout Spec 冲突时，作为最高优先级输入。
5. 默认覆盖线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容；只有用户明确要求保留旧版时，才新建副本或追加版本。
6. 严格按 Layout Spec 的 Frame 树规划建立线框图：先创建 Page Frame，再在 Page Frame 内创建 Module Frame，再在对应 Module Frame 内创建 Control Frame，最后在对应 Control Frame 内放入 Element。
7. 每创建一个节点时必须立即设置正确 parent，禁止先创建散落元素后再尝试归组。
8. 按 P0/P1/P2/P3 表达灰阶、尺寸、边界强弱和显著性。
9. 检查一个 Frame 是否只表达一个页面状态。
10. 检查 PRD 强约束是否在画布可见内容中被表达。
11. 检查线框图可见文案是否来自 PRD、PRD 原型图或已确认 Layout Spec；不得自行改写、润色、缩写、扩写、翻译或替换。
12. 如原型图与正文、Intent、Priority Map 或 Layout Spec 冲突，按 `rules/wireframe_rules.md` 的冲突处理规则写入 run record 或执行摘要。
13. 按 `rules/structure_preparation_rules.md` 检查组件候选、Token 采样父级和 Pattern 候选边界。
14. 检查 Figma 图层树是否符合 Page Frame → Module Frame → Control Frame → Element，是否存在散落 Text、Rectangle、Frame 1、Group 1；不符合时先整理，无法整理则记录为失败。
15. 输出线框图输出端 figma文件链接、Page 名称、解析到的 pageID 和新 Frame ID，并新增 run record。

## Run Record 变更字段

```text
变更对象：
变更前：
变更后：
变更原因：
依据来源：PRD / Intent / Priority Map / Layout Spec / 人工审核
是否影响上游文件：
是否沉淀为通用规则：
```

## Run Record Figma 字段

```text
线框图输出端 figma文件链接：
线框图输出端 Page 名称：
线框图输出端 pageID（如已解析）：
生成模式：
新 Frame ID：
Frame 名称：
```

## 重跑策略

```text
Figma Wireframe：默认覆盖线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Run Record：不得覆盖旧记录，每次执行必须新增 run_xxx.md。
旧版线框图：仅当用户明确要求保留时，才在 Figma 中新建副本或追加版本。
```
