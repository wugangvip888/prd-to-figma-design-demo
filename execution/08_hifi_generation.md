# Hi-Fi Generation

## 目标

根据 Visual Spec 在 Figma 中生成 360 x 780 的高保真设计稿。

本阶段负责执行，不负责临场改写 PRD、Layout Spec、Structure Mapping 或 Design System 结论。

## 输入

```text
Figma 线框图 Page
workspace/visual_specs/{page_id}.md
workspace/design_system/
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
workspace/structure_mapping/
workspace/figma_targets.md
高保真输出端 figma文件链接与 Page 名称或 pageID
```

## 输出

```text
Figma 高保真设计稿
workspace/records/run_xxx_hifi_generation.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/hifi_generation_rules.md
rules/autolayout_rules.md
rules/visual_spec_rules.md
rules/harness_rules.md
workspace/visual_specs/{page_id}.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
```

## 执行步骤

1. 读取并校验 Figma 线框图 Page，确认当前已审核线框图 Frame 数量、顺序、命名、尺寸、模块结构和可见内容。
2. 读取 PRD、PRD 补充 run record、Intent、Priority Map、Layout Spec、Visual Spec、Structure Mapping 和 Design System 产物。
3. 如存在 `workspace/design_system/manual-hifi-adjustment-rules.md`，读取项目级手动调整规则；其只约束当前项目同类页面，不得覆盖 PRD、Wireframe 或 Visual Spec 的业务结构。
4. 读取 `workspace/figma_targets.md`，确认高保真输出端 figma文件链接、Page 名称或 pageID、页面范围和覆盖策略。
5. 按 `workspace/figma_targets.md` 中采样端链接的数字优先级升序读取 Figma 采样来源；同一数字内链接权重相同，按书写顺序读取；仅当前一层级不可访问、内容不足或无法覆盖当前模块时，才降级读取后续数字层级，并记录降级原因。
6. 如果线框图、PRD / PRD 补充记录、Intent、Priority Map、Layout Spec、Visual Spec、项目级手动调整规则或采样来源发生冲突，停止并列出冲突项，等待人工定夺。
7. 按 360 x 780 Page Frame 生成高保真页面；高保真 Page Frame 必须与线框图 Frame 一一对应，名称保持一致。
8. 使用 Visual Spec 指定的组件、Pattern、style_id、Auto Layout 和视觉权重；但不得改变线框图业务结构。
9. 执行 Hi-Fi Generation Harness Check，并输出 `wireframe_frame_id -> hifi_frame_id -> 审核结果` 对照表。
10. 新增 `workspace/records/run_xxx_hifi_generation.md`。

## Harness Check 必查项

```text
高保真 Frame 数量是否等于当前线框图 Frame 数量。
高保真 Frame 顺序和命名是否与线框图一致。
每个 Frame 是否保持 360 x 780。
是否完整显示线框图已有模块、按钮、状态、可见文案和 CTA。
是否新增线框图没有的业务模块、按钮、状态或可见文案。
是否完整继承线框图已有可见文案，且未改写、润色、缩写、扩写、翻译或替换。
是否把采样稿、旧界面或采样端 Figma 来源页面整体复制、整体移植或整体替换到当前设计稿；如存在，判定为严重生成偏差。
是否因视觉采样改写目标稿已有文案、功能架构、业务状态或交互语义；如存在，必须恢复目标稿原内容。
是否存在文本控件到同语义图标控件的等价视觉表达替换；如存在，必须确认功能语义不变且未新增业务入口。
是否恢复已删除的爆款视频复刻功能或旧 14 页范围。
P0/P1/P2/P3 视觉层级是否符合 Priority Map。
页面标题、模块标题、正文、辅助说明、按钮文案和状态提示是否根据业务语义使用了不同的字体、字号、字重和颜色。
Hi-Fi 使用的颜色值是否能在 run record 或 Visual Spec 中找到对应的 style_id 追溯记录（格式：颜色值 -> style_id -> source_ref）。
按钮、Tab、Segmented Control、Chip、标签、参数项、上传入口等有背景容器的控件，其文字是否完整位于背景容器内，且 X/Y 双轴居中。
采样来源是否按优先级执行，降级是否记录原因。
图层结构和命名是否可继续编辑。
如存在 `manual-hifi-adjustment-rules.md`，是否已执行其中适用于当前页面的项目级手动调整规则。
```
