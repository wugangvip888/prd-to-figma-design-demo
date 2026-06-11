# Wireframe Rules

## 目标

线框图必须是一套可支撑后续工作的结构化骨架，而不只是视觉草图。

后续可支撑对象：

```text
真实设计稿绘制
Auto Layout 搭建
命名系统参考
组件候选识别
Token / Pattern 采样参考
AI 后续生成页面时的结构输入
```

## 输出单位

```text
一个页面在一个具体状态下的完整 Frame。
```

## 字体处理规则

```text
线框图阶段不处理最终字体设计。
所有新建文字节点默认使用 Figma 可用的 Inter。
不得主动加载、匹配、替换或修复字体。
不得因为字体缺失、字体权限、字体不可加载或字体不一致而重试。
线框图字体只服务结构可读性，不表达最终品牌字体。
最终字体由人工在流程完成后统一替换。
```

## PRD-原型图优先级

```text
生成线框图前必须全盘阅读 PRD 内容，不得只读取 Intent、Priority Map、Layout Spec 或当前页面正文。
若 PRD 中存在【PRD-原型图】、页面原型图、线框图或 Markdown 字符原型，仍必须全盘阅读 PRD，不得只读取原型图或只读取局部说明；原型图仅在界面结构和可见表达与其他 PRD 内容或下游产物冲突时，作为线框图生成的最高优先级输入。
【PRD-原型图】在页面结构、模块顺序、模块包含关系、可见文案、状态表达、CTA 位置、页面内主次层级和控件相对位置上优先于正文概述、Intent、Priority Map 和 Layout Spec。
当【PRD-原型图】与 PRD 正文、Intent、Priority Map 或 Layout Spec 冲突时，页面结构、模块顺序、可见文案、状态表达和 CTA 位置优先遵循【PRD-原型图】；业务逻辑、字段约束、校验规则、数据模型、埋点和后台流程优先遵循 PRD 正文，并在 run record 或执行摘要中标记冲突。
Markdown 字符原型的右侧边框视觉对齐不作为布局准确性的判断依据；应读取其文本结构、模块层级、文案和相对顺序。
```

## 可见文案保护规则

```text
线框图中的可见文案必须以 PRD、PRD 原型图或已确认 Layout Spec 为准。
不得自行改写、润色、缩写、扩写、翻译或替换 PRD 中的展示文案。
不得用自己的概括文案替代 PRD 中已有的按钮文案、标题、状态文案、说明文案或占位文案。
如果 PRD 文案存在歧义、缺失或冲突，必须记录为待确认，不得自行补写最终文案。
图标内部说明文字只用于线框图功能表达，不作为最终业务文案；但普通可见文本必须严格继承 PRD / Layout Spec。
```

规则：

```text
一个 Frame 只表达一个页面状态。
不把多个页面状态压进同一个 Frame。
不把流程说明混入页面 Frame。
不把组件状态展示混入页面 Frame。
需要作为后续设计、命名、组件、Token 或 Pattern 参考的页面级状态，必须拆成独立 Frame。
仅用于流程理解的状态集合，只能作为说明草图，不得进入标准线框图输入区。
```

## Page Frame 命名规则

统一格式：

```text
[page_number]_[page_name]_state_[state_value]
```

要求：

```text
必须保留真实页面编号。
必须显式写 state。
默认态必须写 state_default。
状态值必须是语义词，不允许位置词、临时词或无意义数字。
不允许中文命名。
不允许无语义数字尾缀。
```

示例：

```text
01_homepage_state_default
02_text_result_state_empty
07_doc_translation_state_uploading
```

禁止：

```text
首页
homepage_1
page_left
02_text_result_default
frame_12
```

## Figma Frame 层级规则

线框图必须使用稳定的 Figma Frame 层级，不得把页面元素散落在 Page Frame 下。

强制层级：

```text
Page Frame
  Module Frame
    Control Frame
      Element
```

要求：

```text
Page Frame 只能直接包含 Module Frame，少量页面级固定元素除外。
Module Frame 只能承载一个业务区块，不得混放多个无关模块。
Control Frame 用于承载可复用控件组合，例如 Tab、输入框组合、上传卡片、参数组、CTA 区。
Element 是最小可见对象，例如文本、图标、分隔线、占位矩形。
不允许大量文本、图标、矩形直接散落在 Page Frame 下。
不允许把所有内容放进一个无语义大 Frame。
不允许用视觉位置代替语义层级。
```

Figma MCP 操作顺序：

```text
生成 Figma Wireframe 时必须先建父 Frame，再建子 Frame，最后放 Element。
1. 创建 Page Frame。
2. 在 Page Frame 内创建所有 Module Frame。
3. 在对应 Module Frame 内创建 Control Frame。
4. 在对应 Control Frame 内创建 Element。
5. 每创建一个节点时，必须立即设置正确 parent，不能依赖后续整理。
6. 禁止先创建散落元素后再尝试归组。
7. 禁止让文本、图标、矩形直接挂在 Page Frame 下，除非它们是页面级固定元素。
```

图层树验收：

```text
生成完成后必须检查 Figma 图层树。
Page Frame 下是否主要只有 module_*。
module_* 下是否主要只有 control_* 或必要的模块级 element。
control_* 下是否包含对应文本、图标、形状等 element。
是否存在大量散落的 Text、Rectangle、Frame 1、Group 1。
若存在散落节点，必须重新整理；无法整理时记录为失败并写入 run record 或执行摘要。
```

## Figma Frame 命名规则

Module Frame 命名：

```text
module_[module_id]
```

Control Frame 命名：

```text
control_[control_id]
```

Element 命名：

```text
[element_type]_[semantic_name]
```

常用 element_type：

```text
text
label
icon
image
shape
divider
button_text
placeholder
progress
badge
```

命名必须满足：

```text
英文 snake_case。
表达业务语义。
不使用中文。
不使用无语义数字尾缀。
不使用纯位置词，例如 top、left、right、bottom、center。
同类控件跨页面命名保持一致。
```

禁止命名：

```text
Frame 1
Group 23
Rectangle 8
Text 12
left_card
top_area
box_1
按钮1
```

## 页面身份与标题图层规则

```text
Page Frame 名称负责表达页面和状态身份。
顶部导航可见标题使用 nav_title。
顶部导航可见副标题使用 nav_subtitle。
页面主体中真实存在的内容标题可使用 content_title 或具体模块语义命名。
不得额外生成通用 page_title 图层。
不得同时使用 page_title 和 nav_title 表达同一标题。
不得同时使用 page_subtitle、subtitle_mode 或 nav_subtitle 表达同一副标题。
```

说明：

```text
如果标题属于顶部导航，统一命名为 nav_title。
如果副标题属于顶部导航，统一命名为 nav_subtitle。
如果标题属于模块内容，命名应跟随模块语义，例如 outline_title_label、sheet_title。
如果页面身份已由 Page Frame 名称表达，不再创建额外标题图层。
同一可见副标题只能保留一个语义图层；如果 page_subtitle 与 subtitle_mode 内容重复，删除重复项并统一收敛为 nav_subtitle。
```


## Page Frame 尺寸规则

标准线框图 Page Frame 固定使用：

```text
width: 360
height: 780
```

规则：

```text
同一批标准页面 Frame 必须保持 360 x 780。
PRD 中出现的设备基准、手机型号、pt 尺寸、倍率、安全区或适配说明，只作为业务与适配参考，不得覆盖标准 Page Frame 尺寸。
不得因为 PRD 写明 iPhone、Android、平板、桌面端、横屏或特殊容器规格，就改变标准线框图 Page Frame 尺寸。
如 PRD 明确要求非移动端或特殊容器，应在 Layout Spec 中记录为适配参考或待人工确认，但标准线框图、高保真图和设计层 Page Frame 仍使用 360 x 780，除非用户在当前执行中明确要求更改本项目标准尺寸。
线框图尺寸用于结构表达和后续设计衔接，不代表最终设备适配断点或真实设备物理尺寸。
```

## 页面区排布规则

标准页面区只放可作为后续设计、命名、组件、Token 或 Pattern 输入的独立页面 Frame。

默认排布：

```text
排列方向：横向排列
顶边位置：y = 0
默认起点：x = 0
Frame 间距：40
默认 x 步进：400
默认尺寸：360 x 780
```

规则：

```text
所有标准页面 Frame 顶边必须对齐。
同一页面多状态必须相邻排列。
不同页面按页面编号或用户确认的页面顺序排列。
页面区不混入说明草图。
页面区不混入组件参考内容。
页面区不混入废弃 Frame。
组件参考区如需预留，必须与标准页面区分离，不得作为当前阶段正式输出。
```

## 系统 UI 与安全区规则

默认线框图不主动生成以下系统 UI 或占位：

```text
状态栏
灵动岛
刘海屏占位
Home Indicator
系统导航栏
安全区占位
设备外壳
```

例外：

```text
只有 PRD 明确要求状态栏适配、灵动岛适配、系统 UI 避让、安全区表达或固定系统区域时，才允许在线框图中表达。
允许表达时，必须在 Layout Spec 中写明依据，并在线框图中作为 P3 或页面结构约束处理。
系统 UI / 安全区表达不得成为装饰元素，不得抢占 P0/P1 主任务层级。
```

## 页面内部层级

页面内部按 4 层组织：

```text
Page Frame
  Module Frame
    Control Frame
      Element
```

解释：

```text
Page Frame：页面状态容器。
Module Frame：页面级功能模块或稳定功能分区。
Control Frame：可交互控件或稳定局部结构。
Element：文本、描边、图形、占位内容。
```

禁止跳层乱放：

```text
页面下直接散放按钮和图标。
控件元素没有父级容器。
同类控件结构深度不一致。
把页面级模块伪装成普通 group。
```

## 哪些对象必须成为 Frame

### 必须是 Page Frame

```text
每个页面状态。
```

### 必须是 Module Frame

满足以下任一条件：

```text
在 Layout Spec 中是独立模块。
在页面中承担明确功能分区。
后续设计稿中需要整体做 Auto Layout。
会被整体移动、替换、复用。
会作为组件、Token 或 Pattern 采样的结构上下文。
```

### 必须是 Control Frame

满足以下任一条件：

```text
可点击。
有“背景 + 图标/文字”组合。
是局部复用单元。
后续设计稿中需要单独调间距、对齐、状态。
会成为组件候选或组件内部结构。
```

### 不必单独成 Frame

```text
纯文本占位。
单根分割线。
纯装饰矩形。
图标内部的小线段、小几何。
```

这些对象应放进所属控件或模块内部。

## Module 命名规则

模块使用：

```text
snake_case
```

要求：

```text
名称表达功能，不表达位置。
名称稳定，不带临时数字。
同语义模块跨页面尽量同名。
优先表达结构归属，例如 input_actions 优于 quick_actions。
```

禁止：

```text
left_area
module_1
top_group
box_23
```

## Control 命名规则

控件优先使用以下格式：

```text
[semantic_name]_action
[semantic_name]_button
[semantic_name]_cta
[semantic_name]_icon
[semantic_name]_capsule
[semantic_name]_tab
[semantic_name]_card
[semantic_name]_input
```

补充容器类控件后缀（Flutter Widget 语义对应）：

```text
[semantic_name]_list       （ListView：垂直或水平列表容器）
[semantic_name]_scroll     （SingleChildScrollView：可滚动内容区容器）
[semantic_name]_carousel   （PageView / 横向 ListView：横向滚动卡片组）
[semantic_name]_grid       （GridView：网格容器）
[semantic_name]_cell       （GridView 单元格）
[semantic_name]_wrap       （Wrap：流式换行容器）
[semantic_name]_stack      （Stack：层叠定位容器，内部不开 Auto Layout）
[semantic_name]_sheet      （BottomSheet：底部弹出层）
[semantic_name]_modal      （Dialog：模态弹层）
[semantic_name]_popup      （PopupMenuButton：弹出层）
[semantic_name]_menu       （MenuAnchor / DropdownMenu：菜单容器）
[semantic_name]_drawer     （Drawer：侧滑抽屉）
[semantic_name]_bottom_nav （BottomNavigationBar：底部导航栏）
[semantic_name]_dropdown   （DropdownButton：下拉选择控件）
[semantic_name]_slider     （Slider：滑块控件）
[semantic_name]_checkbox   （Checkbox：勾选框控件）
[semantic_name]_radio      （Radio：单选框控件）
[semantic_name]_field      （TextField / TextFormField：表单输入框）
[semantic_name]_tap / [semantic_name]_hit  （GestureDetector / InkWell：手势热区，透明交互层）
[semantic_name]_safe       （SafeArea：屏幕安全区容器）
```

要求：

```text
优先使用语义词，不使用坐标词。
同一控件跨页面复用时尽量保持同名。
控件名称必须能对应 PRD、Intent、Priority Map 或 Layout Spec 中的功能语义。
```

禁止：

```text
source_read_icon_92
copy_icon_186
icon_left
button_top
group_12
```

## Element 命名规则

常用元素命名：

```text
label
value
placeholder
helper_text
divider
container_bg
button_bg
capsule_bg
icon_container
```

补充 Element 层命名后缀（Flutter Widget 语义对应）：

```text
[semantic_name]_img / [semantic_name]_image  （Image：图片资源位）
[semantic_name]_avatar   （CircleAvatar：头像图片）
[semantic_name]_overlay  （Stack 浮层：浮层遮罩，不开 Auto Layout）
[semantic_name]_layer    （Stack 子图层：独立图层，不开 Auto Layout）
[semantic_name]_clip / [semantic_name]_mask  （ClipRRect / ClipPath：裁剪或遮罩层，不开 Auto Layout）
[semantic_name]_blur     （BackdropFilter：模糊效果层，不开 Auto Layout）
[semantic_name]_decor    （DecoratedBox：装饰容器，不开 Auto Layout）
[semantic_name]_banner   （Banner：横幅占位块）
```

要求：

```text
Element 命名表达元素角色，不表达坐标。
胶囊控件内部优先使用 capsule_bg、label、icon、icon_container。
按钮控件内部优先使用 button_bg、label、icon_container、xxx_icon。
```

### 命名后缀与 Auto Layout 对应规则

必须开 Auto Layout 的后缀：

```text
_row / _col / _list / _scroll / _wrap / _carousel /
_grid / _cell / _sheet / _modal / _menu / _drawer /
_bottom_nav / _field / _safe
```

禁止开 Auto Layout 的后缀：

```text
_stack / _overlay / _layer / _clip / _mask /
_blur / _decor / _bg / _background / _surface /
_gradient / _icon / _img / _image / _avatar
```

## 文字节点尺寸约束规则

默认不对文字节点设置固定宽高。只有满足以下条件之一，才允许设置固定尺寸：

```text
1. Tab 文字节点：同一 Tab 控件内所有 Tab 项（选中态与未选中态）的文字框宽度必须统一，
   高度固定，确保 selected_indicator 能对齐到每个 Tab 文字框的水平中心。

2. 占据特定区域的展示型文本：文字节点的父容器有明确宽度语义（如输入框、正文展示区），
   该文字节点的宽度从结构关系推导（= 父容器宽度 - 内边距），不得使用硬编码绝对值。
   高度允许自适应内容（textAutoResize = HEIGHT 或 WIDTH_AND_HEIGHT）。
```

不得将以下文字节点设置固定尺寸：

```text
导航标题、按钮文案、参数标签、参数值、卡片标题、卡片标签、区块标题、图标说明文字等。
这类节点跟随内容自适应，强行限制尺寸会导致内容截断或影响后续 Auto Layout 回填校验。
```

## 文字按钮标准结构

文字按钮或带文字操作控件使用：

```text
xxx_button / xxx_action
xxx_cta
  button_bg（按实际需要）
  label
```

要求：

```text
按钮类控件包括 xxx_button、xxx_action 和 xxx_cta。
如果按钮或操作控件有可见文字，文字必须在按钮背景或按钮 Control Frame 的固定文字框内水平居中。
如果按钮或操作控件有可见文字，文字必须在按钮背景或按钮 Control Frame 的固定文字框内垂直居中。
按钮文字可以使用固定宽度文字框，但不得保持左对齐或顶部对齐。
不得用固定左边距模拟按钮文字位置，除非该按钮同时包含图标且 PRD 或 Layout Spec 明确要求图标 + 文字组合。
只有图标 + 文字组合按钮允许文字相对图标偏移；整体内容组仍必须在按钮容器内视觉居中。
校验按钮文字时，必须检查文字框内文字对齐方式为水平居中和垂直居中。
```

## 图标按钮标准结构

图标按钮使用：

```text
xxx_action
  icon_container
  xxx_icon
```

线框图阶段图标按钮的可见表达：

```text
icon_container = 灰色背景
xxx_icon = 中文功能说明文字
```

要求：

```text
icon_container 必须可见，使用灰色背景表达图标背景容器。
icon_container 必须是单个圆形背景，宽高相等，圆角为宽高的一半。
icon_container 是图标控件唯一可见圆形；父级 xxx_action Frame 只作为结构容器，不得再绘制圆形背景或圆形描边。
xxx_icon 的实际显示内容必须是中文功能说明文字。
中文功能说明文字必须完整表达图标功能，不使用英文缩写、英文占位或无语义符号。
图标说明文字以 PRD 中的功能描述为准，例如返回、朗读、复制、切换、上传入口、语音输入。
图层命名仍保持英文语义命名，例如 back_icon、read_icon、copy_icon、swap_icon。
不允许同一套线框图中并存“有 icon_container 的图标”和“没有 icon_container 的图标”。
不允许双圆形表达方式；同一图标控件内只能有一个圆形图标背景。
关闭/删除类熟悉图标允许使用居中的 x 形笔画表达，不需要再用“关闭”文字占位；x 形两条笔画必须在 icon_container 中心对齐。
```

## 可见文案与交互说明

线框图只展示用户可见的业务文案、控件文案和必要标题，不展示给设计/研发看的模块说明。

```text
不得把 mode_tabs_label、creation_input_card_label 这类模块说明作为可见 Text 输出。
不得展示“← 横滑 →”“上滑”“点击后跳转”等交互说明文字；交互信息应写入 Layout Spec 或 run record，而不是放进 Figma 画面。
如果区块本身需要标题，可以保留业务标题，例如“灵感示例”，但不能拼接交互提示。
```

## 图片资源位表达

图片、视频、角色头像、三视图、灵感示例卡等资源位必须使用图片占位结构表达。

```text
image_resource / xxx_thumb
  image_resource_icon
  label（如有标题）
```

要求：

```text
资源位不得只用纯色矩形或纯文字表达。
inspiration_card 必须是图片在上、标题在下，整体高度必须明显高于 param 控件。
character_cards_list_thumb 必须包含 image_resource_icon。
角色三视图必须拆成标题、正面/侧面/背面 Tab、图片展示区，不得混成一个文本块。
```

## 参数与进度表达

```text
param 控件如果代表可选择/可展开参数，右侧必须使用下箭头，而不是左箭头或右箭头。
param 控件如果已被人工确认为“仅展示当前参数”，不得在单个参数项上显示箭头；应在参数模块右侧提供统一“编辑”入口，并在 Layout Spec 中注明点击后进入功能选择弹窗编辑。
上传中状态必须同时展示进度文字和进度条；进度条至少包含 upload_progress_track 与 upload_progress_fill。
上传中状态不显示新增上传入口，避免同一附件上传过程中重复添加文件。
上传成功状态如果需要继续处理附件，应区分删除与替换两个动作。
上传成功状态如果支持多个文档，必须按列表自上而下展示；每项左侧为文件图标和文档名称，右侧为删除和替换两个图标。
上传失败状态应展示失败文案和单一恢复动作；若人工确认文案为“上传失败，请重新上传。”，左侧显示文件图标和文档名称，右侧只显示重新上传图标。
```

## 功能范围删减表达

```text
如果人工确认某一期不上某个功能，必须先在 run record 记录范围变更，再从 Intent、Priority Map、Layout Spec 和 Figma Wireframe 中移除对应页面、入口和可见文案。
已下线/本期不上功能不得仅在 Figma 隐藏；必须避免后续按上游产物重跑时重新生成。
```

## 胶囊控件标准结构

胶囊控件使用：

```text
xxx_capsule
  capsule_bg
  label
  icon_container / icon（按实际需要）
```

要求：

```text
胶囊控件必须是 Control Frame。
胶囊控件内部只允许使用 capsule_bg、label、icon_container、icon 这类语义元素命名。
如果胶囊包含下拉、切换、关闭等操作图标，必须按图标按钮或图标元素规则命名。
```

## Tab 控件标准表达

Tab 控件使用：

```text
xxx_tabs
  selected_tab_label
  unselected_tab_label
  selected_indicator
```

线框图阶段可见表达：

```text
选中 Tab：文字字重 600，底部显示黑色色块。
未选中 Tab：文字正常字重。
selected_indicator：width = 10，height = 4，fill = black。
selected_indicator 必须在选中 Tab 固定文字框的水平中心线上对齐。
```

要求：

```text
不得使用方括号表达选中状态，例如 [ AI漫剧生成 ]。
不得用大面积背景块、胶囊背景或灰色按钮样式表达普通 Tab 选中态。
选中态必须由文字字重和 selected_indicator 共同表达。
选中态文字可以使用固定宽度文字框，但文字必须在该文字框内水平、垂直居中。
选中态文字与 selected_indicator 必须作为一个垂直组合处理，二者按固定文字框在水平方向居中对齐。
校验 selected_indicator 时，必须同时校验文字框内文字对齐方式为水平居中和垂直居中。
如果 PRD 明确要求胶囊式子 Tab，才按胶囊控件规则处理；否则按 Tab 控件标准表达。
```

## P0/P1/P2/P3 到线框图表达

```text
P0：最强线框层级，可用更明确边界、更大区域、更深灰阶表达。
P1：核心操作层级，可用标准控件尺寸和清晰边界表达。
P2：辅助层级，可用中灰、较弱边界或较小控件表达。
P3：弱层级，可用浅灰、占位线、弱边界或背景面表达。
```

执行要求：

```text
同一控件类型在同一优先级下应保持一致。
不同优先级导致的尺寸、灰阶或边界差异必须能从 P0/P1/P2/P3 解释。
P0/P1/P2/P3 只表达信息层级、主次关系、操作优先级和状态强弱，不表达最终品牌视觉。
Priority Map = 权重判断。
Wireframe = 权重可视化，通过灰阶、边界、尺寸和显著性表达信息层级。
Hi-Fi = 最终视觉设计，不直接继承线框图灰阶；最终颜色、样式和组件状态必须来自 Design System、Visual Spec 或采样源。
```

## 禁止事项

```text
不得引入品牌色、渐变、阴影、营销风格或最终 UI 风格。
不得把所有模块处理成同一尺寸和同一灰阶。
不得新增 Layout Spec 未要求的导航、图标或操作入口。
不得新增 PRD、Intent、Priority Map 和 Layout Spec 均无法追溯的核心业务能力。
不得用无语义图层名、数字尾缀或位置词替代功能命名。
不得把状态集合草图作为高保真设计、命名系统、组件、Token 或 Pattern 采样输入。
```

## 自检顺序

```text
0. PRD 约束自检：节点是否存在，可见内容是否表达约束。
1. 状态归属：当前 Frame 表达哪个页面、哪个具体状态。
2. 结构一致性：模块是否完整，是否有多余模块，是否符合四层结构。
3. 业务规则：PRD 中的强逻辑约束是否被满足。
4. 命名规则：Page、Module、Control、Element 命名是否符合规则。
5. 复用一致性：跨 Frame 的同类控件、图标、灰阶、尺寸和命名是否一致。
```

命名正确不等于表达正确，必须同时验证画布可见内容。

## FRAME 包裹规范

```text
凡有子元素组合关系的地方必须用 FRAME 包裹，不得散放在父容器里。

包裹原则（按优先级）：
1. 语义优先：一个功能单元对应一个 FRAME
2. 结构其次：有横向或纵向排列关系的子元素必须有父级 FRAME

覆盖范围：从最小组合单元到页面级别，层层都要有 FRAME。
此规范是 Auto Layout 回填阶段能够正确执行的前提条件。
```
