# Structure Mapping

## 目标

将已生成的 Figma Wireframe 与采样端 Figma 来源结构建立映射，为后续 Design System Extraction 和 Visual Spec 提供结构依据。

本阶段只做结构映射和复用判断，不生成最终组件库、不抽取最终 Token、不绘制高保真设计稿。

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/layout_specs/{page_id}.md
workspace/figma_targets.md
线框图输出端 figma文件链接与 Page 名称或 pageID
采样端链接优先级列表
本次映射页面范围
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/structure_mapping_rules.md
rules/harness_rules.md
workspace/figma_targets.md
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 输出

```text
workspace/structure_mapping/component-index.json
workspace/structure_mapping/page-structure-map.json
workspace/structure_mapping/mapping-review.md
workspace/records/run_xxx_structure_mapping.md
```

## 执行步骤

1. 读取 PRD、Intent、Priority Map、Layout Spec 和最近一次 Wireframe run record。
2. 读取 `workspace/figma_targets.md`，确认线框图输出端 figma文件链接、Page 名称或 pageID，以及采样端链接优先级列表；采样端每行使用 `数字. Figma链接` 格式，数字表示采样优先级。
3. 按采样端链接的数字优先级升序读取 Figma 来源结构；同一数字内链接权重相同，按书写顺序读取；采样链接可以指向 Figma 文件、Page、Section、Frame 或具体节点。
4. 将线框图输出端 Page 名称或 pageID 唯一解析到的 Wireframe 与采样端 Figma 来源按优先级对齐；仅当前一层级内容不足以支撑目标界面结构、组件、状态或样式判断时，才降级读取后续数字层级，并记录降级原因。
5. 检查 Wireframe 是否保留 Page Frame → Module Frame → Control Frame → Element 层级；如存在大量散落节点，停止本阶段并回到 Wireframe 整理。
6. 按页面逐一建立 Wireframe Page Frame 与采样端 Figma 来源 Frame 的候选映射。
7. 按 Module Frame、Control Frame、Element 层级建立结构映射，不因视觉相似直接合并业务语义不同的结构。
8. 识别跨页面或页面内重复出现的组件候选，写入 `component-index.json`；组件候选只能来自稳定的 Module Frame 或 Control Frame。
9. 记录页面级、模块级、控件级映射关系，写入 `page-structure-map.json`。
10. 对无法映射、低置信度映射、疑似复用但证据不足的项写入 `mapping-review.md`。
11. 按 `rules/structure_mapping_rules.md` 和 `rules/harness_rules.md` 执行 Structure Mapping Harness Check。
12. 新增 `workspace/records/run_xxx_structure_mapping.md`，记录输入、输出、Figma 采样来源、采样优先级、采样链接、降级原因、映射范围、审核点和阻塞项。

## component-index.json 内容要求

```text
component_candidate_id：组件候选 ID
source：采样端 Figma 来源 Frame / Node
source_sample_priority：采样优先级数字
source_sample_url：采样链接
wireframe_usage：线框图使用页面和模块
structure_signature：结构特征
reuse_reason：复用依据
differences：与线框图结构差异
confidence：high / medium / low
review_required：true / false
```

## page-structure-map.json 内容要求

```text
page_id：页面 ID
wireframe_frame：线框图 Page Frame 信息
source_frame_candidates：采样端候选 Frame
module_mappings：模块级映射列表
control_mappings：控件级映射列表
unmapped_wireframe_nodes：线框图未映射结构
unmapped_source_nodes：采样端未使用结构
mapping_confidence：high / medium / low
review_required：true / false
```

## mapping-review.md 内容要求

```text
本次映射范围
高置信度复用项
中低置信度复用项
未映射线框图结构
未使用采样端结构
需要人工确认的问题
是否影响后续 Design System Extraction
是否需要回补 Wireframe / Layout Spec
```

## Structure Mapping Harness Check

进入 06 Design System Extraction 前必须检查：

```text
线框图 Page Frame 是否全部被处理。
线框图是否保留 Page Frame → Module Frame → Control Frame → Element 层级，且不存在大量散落节点。
P0/P1/P2 关键模块是否有明确映射或明确未映射原因。
组件候选是否有旧 Figma 结构依据。
低置信度映射是否进入 mapping-review.md。
是否没有把视觉相似误判为同一组件。
是否没有把采样端 Figma 来源中无关结构强行映射到新页面。
是否没有生成最终组件库、最终 Token 或高保真设计结论。
```

如果 Harness Check 未通过，停止进入 06，并在 run record 中记录阻塞原因和下一步恢复入口。

## 重跑策略

```text
Structure Mapping 产物：默认覆盖 workspace/structure_mapping/ 中同名文件。
Run Record：不得覆盖旧记录，每次执行必须新增 run_xxx_structure_mapping.md。
采样端 Figma 来源范围变化：必须重新执行本阶段。
Wireframe、Layout Spec 或 PRD 变化：必须检查是否影响已有映射，受影响页面必须重新映射。
```
