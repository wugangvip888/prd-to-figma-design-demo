# Wireframe Construction Method

## 目标

本方法用于生成一套可直接支撑以下工作的结构化线框图骨架：

```text
真实设计稿绘制
Auto Layout 搭建
命名系统参考
组件候选识别
Token / Pattern 采样参考
AI 后续生成页面时的结构输入
```

## 输入

生成线框图时必须同时读取：

```text
workspace/PRD/{prd_file}.md
workspace/intents/{page_id}.md
workspace/priority_maps/{page_id}.md
workspace/layout_specs/{page_id}.md
rules/wireframe_rules.md
rules/structure_preparation_rules.md
rules/layout_spec_rules.md
```

判定顺序：

```text
PRD-原型图 > PRD正文业务规则 > rules > Intent > Priority Map > Layout Spec
```

解释：

```text
生成线框图前必须全盘阅读 PRD 内容，不得只读取下游产物或当前页面局部描述。
PRD-原型图包括【PRD-原型图】、页面原型图、线框图或 Markdown 字符原型。
必须全盘阅读 PRD，不得只读取 PRD-原型图或当前页面局部说明；PRD-原型图仅在页面结构、模块顺序、模块包含关系、可见文案、状态表达、CTA 位置和控件相对位置与其他 PRD 内容或下游产物冲突时优先。
PRD 正文业务规则是业务硬边界，不可违反。
rules 是生成与检查约束。
Intent 是页面目标与状态语义补充。
Priority Map 是页面元素权重依据。
Layout Spec 是页面结构依据。
当 PRD-原型图与 PRD 正文或下游产物冲突时，界面结构和可见表达遵循 PRD-原型图；业务逻辑、字段约束、校验规则、数据模型、埋点和后台流程遵循 PRD 正文，并写入 run record 或执行摘要。
Markdown 字符原型的右侧边框视觉对齐不作为布局准确性的判断依据；应读取其文本结构、模块层级、文案和相对顺序。
```

## 构造顺序

```text
1. 建立 Page Frame
2. 在 Page Frame 内建立所有 Module Frame
3. 在对应 Module Frame 内建立 Control Frame
4. 在对应 Control Frame 内放入 Element
5. 应用 P0/P1/P2/P3 层级表达
6. 执行单页自检
7. 执行跨页一致性检查
```

执行约束：

```text
必须先建父 Frame，再建子 Frame，最后放 Element。
每创建一个节点时必须立即设置正确 parent。
禁止先创建散落元素后再尝试归组。
禁止让文本、图标、矩形直接挂在 Page Frame 下，除非它们是页面级固定元素。
Wireframe 完成后必须验收图层树；如果存在大量散落 Text、Rectangle、Frame 1、Group 1，必须先整理，无法整理则记录为失败。
```

## Page Frame

统一命名：

```text
[page_number]_[page_name]_state_[state_value]
```

要求：

```text
必须保留真实页面编号。
必须显式写 state。
默认态必须写 state_default。
状态值必须是语义词，不允许位置词或临时词。
不允许中文、不允许无语义数字尾缀。
内容只包含当前页面当前状态。
```

示例：

```text
01_homepage_state_default
02_text_result_state_empty
07_doc_translation_state_uploading
```

## 页面身份与标题图层

执行要求：

```text
Page Frame 名称已经表达页面和状态身份，不再额外创建 page_title 图层。
顶部导航可见标题使用 nav_title。
顶部导航可见副标题使用 nav_subtitle。
页面主体中真实存在的内容标题使用 content_title 或具体模块语义名称。
不得同时使用 page_title 和 nav_title 表达同一标题。
不得同时使用 page_subtitle、subtitle_mode 或 nav_subtitle 表达同一副标题。
如果 page_subtitle 与 subtitle_mode 内容重复，删除重复项并统一收敛为 nav_subtitle。
```


## Page Frame 尺寸

标准线框图 Page Frame 固定使用：

```text
width: 360
height: 780
```

执行要求：

```text
同一批标准页面 Frame 必须保持 360 x 780。
PRD 中出现的设备基准、手机型号、pt 尺寸、倍率、安全区或适配说明，只作为业务与适配参考，不得覆盖标准 Page Frame 尺寸。
不得因为 PRD 写明 iPhone、Android、平板、桌面端、横屏或特殊容器规格，就改变标准线框图 Page Frame 尺寸。
如 PRD 明确要求非移动端或特殊容器，先在 Layout Spec 中记录为适配参考或待人工确认，但标准线框图、高保真图和设计层 Page Frame 仍使用 360 x 780，除非用户在当前执行中明确要求更改本项目标准尺寸。
```

## 页面区排布

默认页面区排布：

```text
排列方向：横向排列
顶边位置：y = 0
默认起点：x = 0
Frame 间距：40
默认 x 步进：400
默认尺寸：360 x 780
```

执行要求：

```text
所有标准页面 Frame 顶边对齐。
同一页面多状态相邻排列。
不同页面按页面编号或用户确认的页面顺序排列。
页面区不混入说明草图、组件参考内容或废弃 Frame。
组件参考区如需预留，必须与标准页面区分离，不得作为当前阶段正式输出。
```

## 系统 UI 与安全区

默认不生成：

```text
状态栏
灵动岛
刘海屏占位
Home Indicator
系统导航栏
安全区占位
设备外壳
```

只有 PRD 明确要求状态栏适配、灵动岛适配、系统 UI 避让、安全区表达或固定系统区域时，才允许表达。

允许表达时：

```text
必须先写入 Layout Spec 的页面级规则或模块描述。
在线框图中作为 P3 或页面结构约束处理。
不得作为装饰元素。
不得抢占 P0/P1 主任务层级。
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
```

## Module Frame

模块来自 Layout Spec 中的可见布局区块。

满足以下任一条件，必须成为 Module Frame：

```text
在 Layout Spec 中是独立模块。
在页面中承担明确功能分区。
后续设计稿中需要整体做 Auto Layout。
会被整体移动、替换、复用。
会作为组件、Token 或 Pattern 采样的结构上下文。
```

命名要求：

```text
使用 snake_case。
名称表达功能，不表达位置。
名称稳定，不带临时数字。
同语义模块跨页面尽量同名。
```

## Control Frame

满足以下任一条件，必须成为 Control Frame：

```text
可点击。
有“背景 + 图标/文字”组合。
是局部复用单元。
后续设计稿中需要单独调间距、对齐、状态。
会成为组件候选或组件内部结构。
```

控件命名优先使用：

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

禁止：

```text
source_read_icon_92
copy_icon_186
icon_left
button_top
group_12
```

## Element

以下对象可以作为 Element，不必单独成 Frame：

```text
纯文本占位。
单根分割线。
纯装饰矩形。
图标内部的小线段、小几何。
```

常用命名：

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

## 图标按钮结构

图标按钮使用：

```text
xxx_action
  icon_container
  xxx_icon
```

线框图阶段可见表达：

```text
icon_container = 灰色背景
xxx_icon = 中文功能说明文字
```

关键要求：

```text
icon_container 是图标控件唯一可见圆形。
父级 xxx_action 只作为结构容器，不再绘制圆形背景或圆形描边。
中文功能说明文字必须完整表达图标功能。
图层命名保持英文语义命名。
不允许双圆形表达。
```

## 文字按钮结构

文字按钮或带文字操作控件使用：

```text
xxx_button / xxx_action
xxx_cta
  button_bg（按实际需要）
  label
```

执行要求：

```text
按钮类控件包括 xxx_button、xxx_action 和 xxx_cta。
如果按钮或操作控件有可见文字，文字必须在按钮背景或按钮 Control Frame 的固定文字框内水平居中。
如果按钮或操作控件有可见文字，文字必须在按钮背景或按钮 Control Frame 的固定文字框内垂直居中。
按钮文字可以使用固定宽度文字框，但不得保持左对齐或顶部对齐。
不得用固定左边距模拟按钮文字位置。
图标 + 文字组合按钮允许文字相对图标偏移，但整体内容组仍必须在按钮容器内视觉居中。
校验按钮文字时，必须检查文字框内文字对齐方式为水平居中和垂直居中。
```

## 胶囊控件结构

胶囊控件使用：

```text
xxx_capsule
  capsule_bg
  label
  icon_container / icon（按实际需要）
```

胶囊控件必须作为 Control Frame，不得只用散落的矩形和文本表达。

## Tab 控件结构

Tab 控件使用：

```text
xxx_tabs
  selected_tab_label
  unselected_tab_label
  selected_indicator
```

执行要求：

```text
选中 Tab 文字使用 600 字重。
未选中 Tab 文字使用正常字重。
选中 Tab 底部必须有 10 x 4 黑色色块作为 selected_indicator。
selected_indicator 必须与选中 Tab 固定文字框在水平方向居中对齐。
选中态文字可以使用固定宽度文字框，但文字必须在该文字框内水平、垂直居中。
校验时必须同时检查 selected_indicator 是否对齐到固定文字框中心，以及选中文字是否在文字框内水平、垂直居中。
不使用方括号、按钮背景或胶囊背景表达普通 Tab 选中态。
```

## P0/P1/P2/P3 应用

```text
P0：最强线框层级，可用更明确边界、更大区域、更深灰阶表达。
P1：核心操作层级，可用标准控件尺寸和清晰边界表达。
P2：辅助层级，可用中灰、较弱边界或较小控件表达。
P3：弱层级，可用浅灰、占位线、弱边界或背景面表达。
```

同一控件类型在同一优先级下必须保持一致；不同优先级导致的视觉差异必须能从 Priority Map 中追溯。

## 自检顺序

```text
0. PRD 强约束：对应节点是否存在，可见内容是否表达约束。
1. 状态归属：当前 Frame 表达哪个页面、哪个状态。
2. 结构一致性：模块是否完整，是否有多余模块，是否符合四层结构。
3. 业务规则：PRD 强逻辑是否被满足。
4. 命名规则：Page、Module、Control、Element 命名是否符合 rules/wireframe_rules.md。
5. 复用一致性：同类控件、图标、灰阶、尺寸和命名是否一致。
6. 结构预备：组件候选、Token 采样父级和 Pattern 候选边界是否清晰。
```

如果 PRD 约束自检或状态归属无法确认，后续检查不得继续执行。
