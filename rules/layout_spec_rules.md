# Layout Spec Rules

## 格式

每个模块使用以下格式：

```text
[module_id]        P0/P1/P2/P3 / 位置或属性
                   关键内容描述
                   frame_role：module / control / element
                   parent：page / module_id / control_id
                   children：child_id_1, child_id_2, child_id_3
                   component_candidate：true / false
                   component_reason：重复出现 / 可复用控件 / 状态变体 / 跨页面共用 / 业务独立单元 / none
                   PRD约束：xxx
```

## 模块规则

```text
生成 Layout Spec 前必须全盘阅读 PRD 内容，不得只读取当前页面正文、Intent 或 Priority Map。
若 PRD 中存在【PRD-原型图】、页面原型图、线框图或 Markdown 字符原型，仍必须全盘阅读 PRD，不得只读取原型图或只读取局部说明；原型图仅在页面结构和可见表达与正文概述、Intent 或 Priority Map 冲突时，作为 Layout Spec 的最高优先级输入。
【PRD-原型图】在页面结构、模块顺序、模块包含关系、可见文案、状态表达、CTA 位置和页面内主次层级上优先于正文概述、Intent 和 Priority Map。
Layout Spec 必须同时参考 PRD、Intent 和 Priority Map。
每个模块必须对应一个可见布局区块。
模块 ID 使用 snake_case。
模块命名表达功能，不表达位置。
交互规则是模块属性，不应伪装成独立布局模块。
模块数量保持精简，能合并的合并。
每个模块必须继承 Priority Map 中的 P0/P1/P2/P3 分级。
当【PRD-原型图】与 PRD 正文、Intent 或 Priority Map 冲突时，页面结构、模块顺序、可见文案、状态表达和 CTA 位置优先遵循【PRD-原型图】；业务逻辑、字段约束、校验规则、数据模型、埋点和后台流程优先遵循 PRD 正文，并在 Layout Spec 中标记冲突。
```

## Frame 结构规划规则

```text
Layout Spec 不只描述页面布局，还必须规划后续 Figma Wireframe 的 Frame 结构。
每个可见模块必须明确 frame_role、parent、children、component_candidate 和 component_reason。
frame_role 只能使用 page、module、control、element。
page 仅用于页面根 Frame，不作为普通模块条目重复输出。
module 表示页面中的主要业务模块或区块。
control 表示模块内可复用或可独立操作的控件组合。
element 表示文本、图标、线、占位图、按钮文字等不可再拆的基础元素。
parent 必须指向 page、已存在 module_id 或已存在 control_id。
children 必须列出直接子级 ID；无子级时写 none。
Layout Spec 中的模块 ID 必须能直接映射为 Wireframe Frame 名称，不允许使用临时名、位置名或无语义数字。
```

组件候选标记规则：

```text
只有满足以下任一条件，才允许标记 component_candidate：true。
同类结构在多个页面或多个状态中重复出现。
是独立控件组合，例如 Tab、上传卡片、参数选择器、底部操作栏。
有明确状态变体，例如 default、uploading、success、disabled、selected。
后续可能进入设计系统或组件库。
component_candidate 只表示候选，不表示当前阶段创建正式组件。
```

## 描述规则

```text
描述应服务线框图生成，避免高保真视觉细节。
关键状态必须写清楚，例如空态、加载态、键盘态、禁用态。
页面级约束只有影响线框图表达时才写入 Layout Spec。
标准线框图、高保真图和设计层 Page Frame 尺寸固定为 360 x 780；PRD 中的设备基准、手机型号、pt 尺寸、倍率、安全区或适配说明只能作为适配参考记录，不得作为覆盖标准画布尺寸的依据。
界面展示文案以 PRD 为准，不自行改写、缩写或翻译。
```

## 固定/悬浮模块标注规则（强制）

```text
凡 PRD 中标注为「贴底」「悬浮」「固定」「fixed」「sticky」「底部操作栏」「底部 CTA」的模块，
Layout Spec 必须同时写入以下两个属性，缺一不可：

position：fixed_bottom / fixed_top / overlay
  （fixed_bottom = 贴底悬浮，fixed_top = 贴顶悬浮，overlay = 浮层）

z_order：最高层
  （明确标注该模块在当前页面状态的 Z 轴最上层，所有普通内容模块不得覆盖）

缺少这两个属性的 fixed/悬浮模块视为 Layout Spec 不完整，
下游 Visual Spec 和 hifi_generation 阶段无法正确识别 Z 轴约束，
导致内容模块覆盖悬浮层的结构错误。
```

## 自检

```text
PRD 强约束是否进入模块描述。
Intent 的视觉重心是否映射为 P0/P1 模块。
Priority Map 中的元素是否都被覆盖或明确排除。
每个可见模块是否具备 frame_role、parent、children、component_candidate 和 component_reason。
parent/children 是否形成清晰树结构，且无孤立模块、循环引用或无语义层级。
Layout Spec 是否足以生成一个页面状态一个 Frame 的线框图。
PRD 中标注为贴底/悬浮/固定/sticky 的模块，是否已写入 position（fixed_bottom/fixed_top/overlay）和 z_order（最高层）两个属性。
```
