# Design System Rules

## 目标

从采样源 Figma 文件中读取当前线框图所需的样式证据，
生成可追溯的按需样式清单，供 Visual Spec 和高保真生成阶段引用。

不建立完整的全局 token 体系。只采集线框图实际用到的样式。

## 总体原则

按需采样：线框图用到什么组件或样式，就去采样源里找对应的值。
不需要的不采。不得因"体系完整性"采集线框图未用到的样式。

页面或界面背景属于页面 Frame 的基础视觉属性。即使线框图未显式绘制背景色，只要当前页面需要生成高保真页面背景，且采样源中存在同页面、同模块族或高相似页面的明确背景色 / 背景渐变，必须从采样源读取并记录为页面背景 style_id；不得因线框图没有背景色标注而退回默认白色或临场自造颜色。

Design System 采集阶段必须扫描采样源 Frame 的所有直接子节点，识别背景类图层（name 包含 background、bg、gradient、page 关键词），为每个背景类图层建立独立 style_id 并写入 Visual Spec，不得因线框图未显式绘制背景而跳过。

采样源是设计系统分区文件，不是单一页面截图。
分区文件不存在"整体主色"或"品牌色"的概念。
不得从分区文件推断、归纳或命名任何全局语义色。

## 采集前提

采样源 Figma 文件可能结构不规范，不得默认存在可靠的 Auto Layout、instance、component、variant、命名或父子层级。

源文件不规范不等于不能复用：

```text
能复用视觉结构就复用。
源文件结构不规范的部分，在目标稿中按目标项目的图层命名、父子层级和可编辑结构整理。
不得因为源文件命名或层级不规范，就默认降级为手工重绘。
```

可稳定采集项：

```text
fill / stroke
fontSize / fontWeight / lineHeight
cornerRadius
strokeWeight
effects / opacity
gradientStops / gradientTransform
image paint
width / height
asset URL / node ID（图片资产、图标资产、装饰资产）
padding / gap / spacing（来自 Structure Mapping spacing_evidence 的可追溯间距数值）
模块级纵向间距：相邻模块之间的 y 坐标差值（下模块 y - 上模块底部 y），必须从采样源实际节点坐标计算，
  写入 design-system-draft.json 的 spacing_* 条目，不得估算。
页面左右边距：采样源页面内容模块的实际 x 坐标，作为页面安全边距基准。
```

这些值可直接从节点属性读取，不依赖源文件结构规范；只要节点可访问，就可以写入确定值。

需谨慎采集项：

```text
父子间距、padding、gap、alignment
constraints、variant 关系
component props、instance override
组件状态关系
```

如果源文件没有可靠结构支撑：

```text
可以记录视觉观测值，但必须标注 unverified。
不得写成已确认 token。
必须进入 design-system-review.md。
高保真阶段只能作为参考，不能作为硬规则。
```

## 复用分级

### 核心倾向

```text
采样源是本项目的设计资产库，复用是默认行为，重建是例外。

判定为 Level 3（重建）时，必须逐条写出三个维度均无法匹配的具体原因。
无法提供原因，强制降回 Level 2。

不得把 Level 1 / Level 2 的 source_candidate 仅当作 token 参考后手工重绘。
```

### 候选源发现规则（三维判定前置步骤）

```text
在进入三维判定框架之前，必须先完成候选源发现，确定旧文件中的 source_candidate 节点。
候选源发现采用以下匹配优先级，从大模块到小组件逐层执行。

#### 匹配优先级（三个维度，优先级从高到低）

1. 内部结构（最高权重）
   判断依据：目标模块的内部元素类型及其位置关系，与旧文件节点是否一致。
   示例：目标为「标题行 + 横排图标操作行」，旧文件中找结构相同的节点。

2. 语义（次高权重）
   判断依据：模块的职责类型（导航栏、卡片列表、输入区、CTA 按钮等）是否与旧文件节点的功能角色一致。

3. 页面位置（仅作否定过滤，不参与正向评分）
   页面位置相同不得作为正向加分依据。
   仅用于排除：若内部结构和语义均无法匹配，且位置明显不符（如顶部导航栏 vs 底部操作区），可作为否定过滤依据排除候选。

#### 匹配等级规则

- 三项全部符合：最优候选，直接进入三维判定。
- 两项符合：权重从高到低排列（内部结构 > 语义 > 页面位置），优先选择高权重维度命中的候选。
- 一项符合：权重同上，仅在无两项以上候选时使用。
- 零项符合：无候选，直接进入 Level 3 采样组装。

#### 执行层级顺序（从大到小）

1. 先在旧文件中搜索与目标模块匹配的 Module 级节点。
2. 若无 Module 级匹配，搜索 Control 级（按钮、Tab、输入框等）。
3. 若无 Control 级匹配，搜索 Element 级（文字节点、图标节点、色块等）。

找到候选后，再进入三维判定框架确定复用级别（Level 1/2/3）。
不得跳过候选发现直接进入 Level 3 重建。
```

### 三维判定框架

复用判定基于以下三个维度，判定顺序从大到小：先模块级，再组件级，再叶子节点。上层判定通过后，下层子组件默认继承，不重新降级。

#### 维度 A：结构组成模式（判定入口）

```text
从外到内描述模块由哪些结构层组成，顺序和层级关系对上即匹配。
不依赖位置、不依赖名称、不依赖业务内容。

判定方式：
  自行描述当前模块的结构层顺序，与采样源对比，层级顺序一致即判定匹配。
  无需查表，无需预录入。

示例（不构成封闭列表）：
  [标题层 + 内容输入层 + 底部操作层] = [标题层 + 内容输入层 + 底部操作层] ✓
  [横排多选一控件 + 选中指示层] = [横排多选一控件 + 选中指示层] ✓
  不论标题文字长短、输入区是文本框还是图片上传、底部是1个还是2个按钮

容差规则：
  采样源比线框图多出的纯装饰层（背景色块、渐变覆盖层、分割线、阴影层）
  不计入结构组成对比，不影响匹配判定。

维度 A 不满足 → 直接 Level 3，必须写明原因。
维度 A 满足 → 进入 Level 判定。
```

#### 维度 B：Action 类型

```text
忽略具体业务含义，只看 action 类型是否相同。

action 类型（不构成封闭列表）：
  switch_view     切换视图/选项（Tab、Segmented Control）
  trigger_action  触发独立操作（按钮、图标操作行）
  input_content   输入内容（输入框、上传区）
  display_info    展示信息（卡片、列表项、标题区）
  toggle_state    开关/勾选状态（switch、checkbox）
  navigate        页面跳转（导航入口、返回）

示例：
  「幻灯片/剧情切换 Tab」= 「历史/浏览切换 Tab」→ 均为 switch_view ✓
  「编辑/拷贝图标行」= 「收藏/分享图标行」→ 均为 trigger_action ✓
```

#### 维度 C：视觉结构模式

```text
忽略内容语义，只看形态类型和交互职责是否相同。

形态类型示例（不构成封闭列表）：
  tab-bar           横排标签 + 切换态
  icon-action-row   横排图标 + 点击触发
  card-list         纵向/横向卡片列表
  input-card        输入区容器
  capsule-param     胶囊形参数选择项
  cta-button        主操作按钮
  section-header    模块标题行

两个维度都对上（形态类型 + 交互职责），判定视觉结构模式相同。
```

### 复用级别判定

```text
【前提】维度 A（结构组成模式）对上，进入以下判定：

Level 1 — clone 后只做替换
  触发条件（满足维度 B 或维度 C 任意一条）：
    B：action 类型相同
    C：形态类型 + 交互职责相同
  允许操作：文案替换、图片/imageHash 替换、颜色 token 替换、图标资产替换
  不需要移动、增删、重排任何功能节点

Level 2 — clone 后修改
  触发条件：
    维度 B 或 C 部分匹配，但形态类型对上、槽位数量或排列方向需要调整
    （如横排变纵排、2项变3项）
    clone 后需要移动、增删或重排功能节点
  执行方式：先删再补再改，不得乱序

Level 3 — 重建
  触发条件：维度 A/B/C 均无法匹配
  必须逐条写出三个维度无法匹配的具体原因，否则强制降回 Level 2
```

### 继承规则

```text
上层模块判定为 Level 1/2 后，其子组件默认继承复用判定，不重新降级。
只有子组件的功能节点发生增减时，才在子组件层单独标注 Level 2，不影响上层判定。
子组件局部视觉结构差异（装饰层增删、背景形状替换、图片填充替换）不触发降级。
```

### 视觉增强豁免条款

```text
以下变化属于视觉层增强，不改变结构角色，不触发降级：
- 纯文字 action → 图标 + 文字组合 action
- 纯色块 → 图片填充
- 无装饰层 → 增加背景形状 / 描边 / 阴影
- 单图标 → 图标 + 角标组合
- tab 胶囊样 ↔ tab 下划线样 ↔ tab 填色块样
- checkbox ↔ switch
- text action ↔ icon action ↔ icon + text action
```

### 采样优先级

```text
同一复用等级中有多个候选源时，按 figma_targets.md 的优先级选择。
优先级相同则按书写顺序选择。
如果高优先级源不可访问、缺失必要结构或存在冲突，才降级到后续采样源，并记录原因。
```

### Level 1/2 复用执行约束

#### 文案替换后的布局重算

```text
复用组件替换文案后，必须以目标文案的实际显示宽度为基准重新计算布局。
保留源组件中相同语义元素之间的间距关系，反推直接容器和相关父级 Frame 的尺寸。
不得在目标文案宽度变化后，机械保留源文本框、容器或父级 Frame 的固定宽度，
导致裁切、重叠或溢出。
重算时不得使用人工估算 gap。
必须从源组件同语义节点的实际 x / y / width / height 计算水平和垂直间距，
再将该间距用于目标节点重排。
```

#### 内容延展方向

```text
目标文案必须完整展示，不得裁切、压缩到不可读或与其他元素重叠。
容器尺寸根据文本 / 元素组的对齐锚点延展：
- 左对齐：优先向右延展
- 右对齐：优先向左延展
- 居中对齐：优先向左右对称延展，并保持中心锚点不变
若延展会超出父级容器或安全边距，应在父级允许范围内重新计算位置和尺寸。
```

#### 文本组对齐继承

```text
同一卡片、列表项、按钮、入口或表单控件内，若标题、主文本、说明、tag、状态文本构成同一文本组，
从属文本默认继承主文本的水平对齐锚点。
除非源文件明确表现为独立对象，例如角标、badge、价格、计数器、状态点或独立操作入口。
```

#### 状态样式作用边界

```text
状态样式属于具体控件状态，不得迁移到父级容器、保护层、页面背景或无状态语义节点。
```

#### 图标 / 符号继承

```text
Level 1/2 复用时，icon、符号、装饰图形、状态图形应优先原样继承源节点。
不得根据语义自行替换为未采样的新图标。
如目标确实需要替换但找不到采样源对应节点：
- 若复用源中已有 icon / 符号节点，优先保留源节点，记录语义不完全匹配。
- 若目标结构明确要求必须有 icon，且源中没有可用节点，可使用 Unicode 或「icon」文字作为 review 占位。
- 占位只能作为 review 中间态，不得作为最终高保真交付结果。
- 不得为了等价视觉表达从纯 text action 自行新增 icon。
- 图标节点的尺寸、颜色、视觉样式优先继承源节点。
- 位置应按源组件中相同语义元素之间的间距关系重新计算，
  不得因文案替换造成图标与文字重叠或间距失真。
- 记录到 design-system-review.md 等待人工替换或补充项目图标库来源。
```

#### 替换文案后的同步检查

```text
替换文案后，不得只修改 text.characters。
必须同步检查并更新，横向和纵向都要覆盖：
- 文本宽度变化时：重算同行兄弟元素位置和父级宽度
- 文本高度变化时：重算下方兄弟元素 y 值；必要时重算直接父级高度
- 必要时同步更新背景 shape 尺寸
- 同步检查上一级容器内的排列位置
- 保留源组件相同语义元素之间的水平和垂直间距关系

若父级高度固定，优先在父级内部重新分配位置。
无法容纳时记录到 design-system-review.md，不得让元素重叠。

检查目标是：目标文案完整展示，元素不重叠，源组件相同语义元素间距关系被保留。
```

#### 父级尺寸不可直接更改

```text
以下情况不得随文案变化直接更改源组件或目标组件的父级尺寸：
- 源组件或目标组件在 Visual Spec / Wireframe 中已定义固定 width / height。
- Auto Layout 设置为 Fixed Width / Fixed Height，且该固定尺寸是组件视觉结构的一部分。
- 父级容器在当前页面结构中是固定尺寸，子元素依赖 Fill、constraints 或对齐锚点贴合父级边界。
- 调整父级尺寸会破坏页面栅格、模块边界、安全边距或同级组件排列。

当父级尺寸不可直接更改时：
- 不得通过扩大父级来掩盖文本溢出或重叠。
- 必须优先在父级内部重排、换行、调整兄弟元素位置或减少无关留白。
- 若仍无法容纳目标文案，记录到 design-system-review.md，等待人工确认。
```

#### 横向溢出处理

```text
当子元素横向排布后超出父级容器或页面安全边距时，
必须先判断该区域是否为明确的横向滚动 / 横滑容器。

若是横向滚动 / 横滑容器：
- 必须在 Wireframe、Layout Spec 或 Visual Spec 中有明确横滑 / 横向滚动标注。
- 没有明确标注时，默认视为非横滑容器处理。
- 允许内部滚动内容宽度超过父级可视宽度。
- 父级 Frame 必须保持在页面安全边距内。
- 超出的只能是内部滚动内容，不得扩大父级 Frame 突破安全边距。

若不是横向滚动 / 横滑容器：
- 不得横向超出父级容器或页面安全边距。
- 必须通过换行、分行、压缩间距到源规则允许范围内、或减少单行数量解决。
- 不得通过扩大父级 Frame 或突破页面边距解决。
- 不得压缩字段名、字段值、按钮文案、标题等业务文本节点的实际显示宽度。
- 必须先保证业务文本完整展示，再通过调整兄弟元素位置、背景 shape 宽度、换行或分行解决。
```

### 等价视觉表达替换

以下情况不自动降低匹配等级：

```text
text action -> icon + text action
icon + text action -> text action
text tab -> pill tab / underline tab
checkbox -> switch
dropdown text -> text + chevron
```

必须满足：

```text
1. 交互对象一致。
2. 触发动作一致。
3. 状态语义不变。
4. 没有新增业务入口。
5. 没有删除必要入口。
6. 没有迁移源组件文案。
7. 新增图标必须能在采样源中找到同语义或等价语义节点，
   或来自已确认的项目图标库 / design-system-draft.json 资产记录。
   若找不到来源，保持 text action，不得新增图标。
```

只有无法判断是否改变业务语义时，才进入人工确认。

### Level 3：低相似或无匹配，采样组装

没有完全匹配或高相似组件时，才进入 Level 3。

执行顺序：

```text
1. 先找相似父级 Frame：
   采集页面边距、模块间距、容器背景、圆角、描边、投影、padding、gap。
   padding / gap / alignment 若源文件无可靠 Auto Layout 支撑，
   只能作为当前页面局部视觉观测值，标注 unverified，
   不得写成确定 token 或通用规则。

2. 再按子级语义找相似子组件：
   采集标题、正文、按钮、输入区、卡片、标签、图标等局部样式。

3. 最后使用 design-system-draft.json 中已有 style_id / token 组装。
   若 design-system-draft.json 尚无对应 style_id，
   必须先从第 1 步和第 2 步的采集结果中生成新的按需 style_id，
   写入 raw-style-inventory.json 和 design-system-draft.json，
   建立 style_id -> source_ref -> source_node_id 的追溯链，
   再用于 Visual Spec 和 Hi-Fi 组装。
   不得跳过写入步骤直接重绘。
```

### 间距冲突仲裁规则

```text
本规则适用于 Level 2 和 Level 3 场景。Level 1 直接复用不涉及间距冲突。

当从不同来源采集到的间距值发生冲突时，按以下规则仲裁：

#### 规则一：层级高的覆盖层级低的

父容器的 padding 优先于子组件的内边距。
示例：模块 padding = 16px，子组件内部采集到的 padding = 24px，取 16px。
原因：父容器 padding 是结构性约束，决定内容与背景边界的整体视觉关系；子组件内边距是局部视觉属性，不得突破父级结构边界。

#### 规则二：同级冲突以 width × height 更大的组件为准

同级两个组件采集到的间距值冲突时，以 width × height 乘积更大的组件所属采样值为准。
width × height 必须从采样源节点实际属性计算，不得凭视觉估算。
若两个节点面积完全相同，取采样优先级链中优先级更高的来源（见 figma_targets.md）。

#### 冲突记录要求

每次触发仲裁规则，必须在 run record 中写出：
- 冲突的两个来源节点 ID 及各自的间距值
- 适用的仲裁规则（规则一 / 规则二）
- 最终采用的值及来源节点 ID
```

约束：

```text
不得凭空创造颜色、圆角、阴影、字号、行高或间距层级。
不得因为视觉相似继承源组件业务内容。
不得迁移目标 PRD 未定义的模块、状态、按钮、字段或入口。
```

核心原则：

```text
先复用，再修改，最后才组装。
能直接采用源组件时，不应手工重绘。
能修改后复用时，不应只采 token 重建。
只有低相似或无匹配时，才使用父级规范 + 子级语义 + token/style_id 组装。
业务结构和文案以 PRD / Wireframe 为准。
视觉结构和样式优先来自采样源。
源文件不规范时，目标稿负责规范化，而不是放弃复用。
```

## JSON 追溯链

raw-style-inventory.json 使用顶层 items 数组，每条包含：
id、property、value、source_node_id（格式 n:n）、sample_priority、sample_url、
decision_level（只允许 component_match / priority_sampling / structure_fallback）。
decision_reason 可选；如果存在，必须是非空字符串。
凡 Structure Mapping 中有 source_candidate 的 P0/P1/P2 模块，raw-style-inventory.json 必须对该 source_candidate 写入 visual_audit 四态记录。主容器必须逐项记录 container.background_fill、container.gradient、container.border_stroke、container.radius、container.shadow_effects；子元素颜色按目标结构需要记录 children.text_color、children.icon_color、children.foreground_color。每项只能使用 value、none、conflict、not_applicable 四态之一；value 必须附具体值，conflict 必须附冲突原因。

design-system-draft.json：
styles 必填，每条 style_id 必须有 value 和 source_ref，
source_ref 必须指向 raw-style-inventory.items 中存在的 id。
components 可选，只记录线框图实际用到且 Visual Spec 需要引用的组件关系。
style_id 只能使用局部描述名，例如 color_page_bg、radius_card、spacing_card_padding。
禁止 color.primary.action、font.page.title 等全局语义 token 命名。

追溯链：style_id -> source_ref -> raw-style-inventory.items.id -> source_node_id + sample_url

凡 Structure Mapping 的 `asset_mappings` 中有可复用资产节点，必须在 `raw-style-inventory.json` 和 `design-system-draft.json` 中建立对应 `asset_*` 条目，包含采样端节点 ID、资产 URL 和复用方式；缺少 `asset_*` 条目判定为遗漏，不得进入 Visual Spec。凡 Structure Mapping 的 `spacing_evidence` 中有可追溯间距数值，必须在 `design-system-draft.json` 中建立对应 `spacing_*` 条目；缺少 `spacing_*` 条目判定为遗漏，不得进入 Visual Spec。

## Harness 要求

1. raw-style-inventory.items 每条必须有 source_node_id、sample_url、sample_priority、decision_level。
2. decision_level 只允许 component_match、priority_sampling、structure_fallback。

decision_level 枚举值与复用分级的对应关系：
- component_match：对应 Level 1 直接复用 / Level 2 修改后复用
- priority_sampling：对应 Level 3 中按采样优先级取得的局部样式
- structure_fallback：对应 Level 3 中无明确组件匹配时的父级 / 子级结构采样

3. design-system-draft.json 每个 style_id 必须有 source_ref，且能在 items.id 中找到。
4. Visual Spec 中引用的每个 style_id 必须存在于 design-system-draft.json.styles。
5. 页面整体视觉权重不得倒置。Visual Spec 必须为 P0/P1/P2/P3 模块标注关键强调 style_id，包括文字层级、文字颜色、容器背景、按钮 / CTA 样式、描边、投影或尺寸中的相关项。P0 的关键强调 style_id 不得与 P3 完全相同；如无法区分，写入 design-system-review.md。允许共享基础结构类 style_id，例如页面背景、通用圆角、基础间距、基础分割线。
6. 不得新增业务内容。等价视觉替换允许，但必须标注业务属性、触发动作、选项含义未变。
7. 禁止 color.primary.action、font.page.title 等全局语义 token 命名。
8. 不得采集线框图未用到的样式。
9. 不得把单页特殊样式提升为通用规则。
10. Design System Gate 以 Structure Mapping 中的 source_candidate 与 Priority Map 中的 P0/P1/P2 为检查范围，对 raw-style-inventory.json 的 visual_audit 执行硬检查；缺项、四态非法、value 无具体值或 conflict 无原因均判定为 FAIL。

## 禁止事项

不得建立完整、全局、可复用的 token 命名体系。
不得使用全局语义 token 命名。
不得推断品牌主色、主色调、色相家族等全局概念。
不得把 AI 推测值写入 raw-style-inventory.json。
不得采集线框图未用到的样式。
不得把单页特殊样式直接提升为通用规则。
