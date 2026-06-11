# Visual Spec

## 目标

将 PRD、Intent、Priority Map、Layout Spec、Wireframe、Structure Mapping 和 Design System 草案转成每个页面的高保真设计指令。

Visual Spec 是 Hi-Fi Generation 的直接依据；08 阶段只执行本阶段决策，不临场新增核心设计规则。

## 输入

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/layout_specs/{page_id}.md
workspace/structure_mapping/
workspace/design_system/
Figma Wireframe
```

## 输出

```text
workspace/visual_specs/{page_id}.md
workspace/records/run_xxx_visual_spec.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/visual_spec_rules.md
rules/harness_rules.md
```

## 执行步骤

1. 读取业务输入、结构映射和设计系统草案。
2. 按页面生成高保真设计指令。
3. 明确每个模块使用的 component、pattern、style_id 和视觉权重表达。
4. 根据 PRD、Intent、Layout Spec 和 Priority Map，明确页面标题、模块标题、正文、辅助说明、按钮文案、状态提示分别使用的字体、字号、字重、颜色、间距和状态样式。所有引用的 style_id 必须以 `style_id: xxx` 格式写入，且必须存在于 design-system-draft.json.styles。
5. 标注无法由设计系统覆盖的新增结构、样式选用冲突和人工确认项。
6. 执行 Visual Spec Harness Check。
7. 新增 `workspace/records/run_xxx_visual_spec.md`。
