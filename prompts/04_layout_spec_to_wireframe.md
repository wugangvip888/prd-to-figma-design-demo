# 04 Layout Spec to Wireframe

## 任务

读取 PRD、Intent、Priority Map 和已确认的 Layout Spec，先执行 Wireframe Preflight Gate，再根据 `workspace/figma_targets.md` 中线框图输出端的 figma文件链接、Page 名称或 pageID 生成线框图 Frame。

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
execution/04_layout_spec_to_wireframe.md
execution/wireframe_construction_method.md
rules/layout_spec_rules.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/harness_rules.md
```

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
重跑策略：默认覆盖线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容
```

## 输出

```text
Figma 中更新后的线框图 Frame
新 Frame ID
workspace/records/run_xxx.md
```

## 执行要求

1. 默认覆盖 `workspace/figma_targets.md` 中线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容；只有用户明确要求保留旧版时，才新建副本或追加版本。
2. 读取 `workspace/figma_targets.md`，确认线框图输出端 figma文件链接和 Page 名称；pageID 可选。
3. 全盘阅读 PRD，识别当前页面正文说明和【PRD-原型图】/页面原型图/线框图/Markdown 字符原型，同时读取 Intent、Priority Map 和 Layout Spec。
4. 若 PRD 中存在原型图，仍必须全盘阅读 PRD；【PRD-原型图】仅在页面结构、模块顺序、模块包含关系、可见文案、状态表达、CTA 位置和控件相对位置与正文概述、Intent、Priority Map 或 Layout Spec 冲突时，作为最高优先级输入。
5. 生成前按 `rules/harness_rules.md` 执行 Wireframe Preflight Gate。
6. 通过 Preflight 后，严格按 Layout Spec 的 Frame 树规划构造：先创建 Page Frame，再创建 Module Frame，再创建 Control Frame，最后放入 Element。
7. 每创建一个节点时必须立即设置正确 parent，禁止先创建散落元素后再尝试归组。
8. 按 P0/P1/P2/P3 表达信息层级。
9. 如原型图与正文、Intent、Priority Map 或 Layout Spec 冲突，按 `rules/wireframe_rules.md` 的冲突处理规则写入 run record 或执行摘要。
10. 可见文案必须来自 PRD、PRD 原型图或已确认 Layout Spec，不得自行改写、润色、缩写、扩写、翻译或替换。
11. 按 `rules/structure_preparation_rules.md` 保留组件候选、Token 采样父级和 Pattern 候选所需结构边界。
12. 检查一个 Frame 是否只表达一个页面状态。
13. 检查 Figma 图层树是否符合 Page Frame → Module Frame → Control Frame → Element，是否存在散落 Text、Rectangle、Frame 1、Group 1；不符合时先整理，无法整理则记录为失败。
14. 输出线框图输出端 figma文件链接、Page 名称、解析到的 pageID、新 Frame ID、生成结果摘要，并新增 Wireframe 后变更记录。
