# Visual Spec Rules

## 目标

定义 Visual Spec 的生成规则，确保高保真设计指令同时服从业务结构和设计系统。

## 基本原则

```text
已审核 Wireframe > PRD / PRD 补充记录 > Intent > Priority Map > Layout Spec > Structure Mapping > Design System > Visual Spec
Visual Spec 必须完整承接已审核线框图的页面数量、模块结构、可见文案、状态表达、CTA 位置和控件相对位置。
Visual Spec 必须解释 P0/P1/P2/P3 如何转成视觉层级。
Visual Spec 必须指定使用哪些 component、pattern、style_id 或 layout rule。
Design System 无法覆盖的新增设计必须标注原因和人工确认点。
采样端 Figma 来源 / Design System 的视觉采样必须按 rules/hifi_generation_rules.md 中的采样端链接优先级执行。
采样端 Figma 来源 / Design System 只提供视觉体系依据，不提供目标页面的业务结构；不得把采样源中存在、但已审核 Wireframe / Visual Spec 未定义的 Tab、按钮、状态、模块或交互控件写入目标页面。
Visual Spec 必须承接 Design System 中的组件匹配、优先级采样和结构兜底结论；当目标组件存在相似采样组件时，必须明确使用哪个采样组件的视觉属性；当不存在相似组件时，必须说明使用哪个相似 Frame 或哪些 style_id 推导。
如果 Design System 已采集页面背景 style_id，Visual Spec 必须把该 style_id 写入对应 Page Frame 或页面背景层；线框图未显式绘制背景色不构成忽略采样背景的理由。
Visual Spec 必须先判断目标页面与采样源页面是否结构同构；只有明确同构时，才允许把旧稿模块位置、高度和整页骨架写入高保真生成规格。若不同构或不明确，Visual Spec 只能写入旧稿设计规范、相似 Frame 规则或 style_id 兜底，不得要求高保真强套旧稿骨架。
Visual Spec 不得依赖人工点名某个具体 Figma 节点后才继承视觉。凡 Structure Mapping 已为目标 P0/P1/P2 模块或控件写出 source_candidate，且 mapping_type 为 component_inheritance 或 frame_level_inference，Visual Spec 必须自动读取该 source_candidate 的视觉属性，并逐项说明继承 / 不继承结论。
```

## 设计系统选用规则

```text
Visual Spec 必须根据 PRD、Intent、Layout Spec、Structure Mapping、Design System 和 Priority Map，为每个模块明确样式选用原因。

每个页面至少明确：
1. 页面主目标对应的 P0 元素，以及使用的主强调样式。
2. 模块标题、主要输入区、核心内容卡片对应的 P1 / P2 样式。
3. 辅助说明、状态补充、计数器、弱提示对应的 P3 样式。
4. 错误、成功、上传中、生成中、禁用、选中等状态对应的状态色、图标、描边或提示样式。
5. 标题字体、正文/内容字体、辅助解释字体、按钮字体之间的字号、字重和颜色差异。
6. 每个主要模块的视觉依据来源：组件匹配 / 优先级采样 / 结构兜底。
7. 结构同构判断结论：同构 / 不同构 / 不明确；并说明是否允许继承旧稿整页骨架。
8. 对按钮、Tab、Segmented Control、Chip、标签、参数项、上传入口等有背景容器的控件，明确采样源 padding / gap / 高度 / 圆角，并说明当前 PRD 文案放入后如何保证文字完整位于背景容器内且 X/Y 双轴居中。
9. 对 Structure Mapping 已匹配 source_candidate 的 P0/P1/P2 模块或控件，必须逐项列出背景、描边、圆角、阴影、内边距、尺寸比例、字号层级、颜色层级和视觉权重的继承结果；若任一项不继承，必须写出具体冲突来源、影响范围和人工确认依据。
10. 对 Structure Mapping 已匹配 source_candidate 的每个模块或控件，必须先从采样端节点读取其所有直接子节点列表（包括文字节点、图标节点、装饰节点、背景 shape），逐一列出子节点名称、类型和 Design System 对应 asset_id 或 style_id，再声明每个子节点继承或不继承；不得跳过任何采样端已存在的子节点；漏写任何子节点类型（尤其是装饰图片、图标资产、笔触装饰），判定为遗漏，Visual Spec 不得通过 Harness Check。

不得把所有文字、按钮、卡片、状态统一套用同一种样式；必须体现业务优先级和信息层级。
```

## 字体表达边界

```text
Visual Spec 可描述字号、字重、行高、颜色和层级。
Visual Spec 不要求生成阶段加载、匹配或替换特定字体 family。
字体 family 不作为 Hi-Fi 生成阻塞项。
最终字体由人工在流程完成后统一替换。
```

## 禁止事项

```text
不得在 Visual Spec 中新增 PRD 未定义的核心业务能力。
不得在 Visual Spec 中新增线框图没有的业务模块、按钮、状态或可见文案。
不得遗漏线框图已有的模块、按钮、状态或可见文案。
不得绕过 Structure Mapping 直接临场选择采样端结构。
不得把采样源页面里的额外内容模块、Tab、操作入口或状态控件当成设计系统样式迁移到目标页面。
不得把低置信度 Design System 结论当成强规则。
不得脱离 PRD、Intent、Spec 和 Priority Map 机械套用 Design System 样式。
不得在 Structure Mapping 已存在 source_candidate 时只写“参考结构”“继承比例”“style_id 兜底”等笼统结论；必须明确该 source_candidate 的视觉属性是否被采用。未逐项说明的 Visual Spec 不得通过 Harness。
不得引用 design-system-draft.json 未定义的 style_id 或颜色值。
不得使用全局语义 token 命名（含点号的 token 名）。
不得把采样源中线框图未定义的业务入口、按钮、状态或文案写入 Visual Spec；业务结构以 Layout Spec 和 Wireframe 为唯一依据。
允许行为不变的等价视觉替换，但必须标注行为一致。
```

## Visual Spec 坐标合法性校验（强制）

```text
Visual Spec 输出前，对每个模块的所有直接子节点执行以下数学校验：

  子节点 x + 子节点 width ≤ 父容器实测 width
  （父容器 width 必须从 use_figma/get_node 实际读取，禁止假定为 360 或任何固定值）

任何子节点不满足上述条件，该模块 Visual Spec 判定为 FAIL，
禁止进入 Flow 08，必须先修正坐标后重新输出。

对存在"同义控件"的模块（两个节点表达同一语义入口），
必须在 Visual Spec 中明确标注：保留哪一套节点 ID、删除哪一套节点 ID。
未标注删除项的同义控件对，视为 Visual Spec 不完整，同样判定 FAIL。
```

## TEXT 节点属性显式记录规则（强制）

```text
Visual Spec 中所有 TEXT 节点的属性必须使用属性名显式记录，
不得用中文描述词或自然语言代替属性名。

禁止写法示例（不合规）：
  - 居中
  - 左对齐
  - 加粗
  - 14号字

必须写法示例（合规）：
  - textAlignHorizontal: CENTER
  - textAlignHorizontal: LEFT
  - fontName: { family: "Inter", style: "Bold" }
  - fontSize: 14

适用属性包括但不限于：
  textAlignHorizontal、textAlignVertical、textAutoResize、
  fontName（family + style）、fontSize、lineHeight、
  letterSpacing、fills（颜色）、layoutSizingHorizontal

违反此规则的 TEXT 节点记录视为属性不完整，Flow 08 执行时
不得假设默认值，必须重新读取采样源后补全记录。
```

## 多元素横向排列模块的排列规范

```text
默认使用 layoutWrap = WRAP，由内容宽度自然决定折行。
禁止使用固定行数分组（row_1 / row_2 等中间层）模拟换行。
仅当 spec 明确声明"固定N行"或"横向滚动"时，
才可以使用对应的结构，否则一律 WRAP。
```

## 模块标题与内容的层级规范

```text
模块标题（section_label，区块标签）禁止与内容子元素平级放在同一容器内。
正确结构：模块容器使用 layoutMode = VERTICAL（纵向自动布局），
标题作为第一个子节点，内容区域作为第二个子节点。
```
