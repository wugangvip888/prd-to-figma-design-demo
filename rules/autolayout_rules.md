# Auto Layout Rules

本文档定义为已有 Figma 高保真静态稿补 Auto Layout 时的执行规则。

## 适用范围

```text
适用于已有人工作图或已确认高保真静态稿的 Auto Layout 整理。
目标是提升开发交付结构、拉伸适配和可维护性，不是重新设计页面。
```

## 最高优先级

```text
1. 不改变原静态稿视觉效果。
2. 不删除、替换或重建用户已有界面元素，除非用户明确要求。
3. 不改变字体、字重、字形、文字节点字体属性或将图形标题替换为文字标题。
4. 不为了套用 Auto Layout 改动已有图层的位置、尺寸、间距或层级视觉结果。
5. 如果 Auto Layout 适配目标与静态视觉保持存在冲突，必须先说明冲突、影响范围、可选方案和结构调整收益，等待人工确认后再执行。
```

## 允许操作

```text
允许调整 Frame 的 Auto Layout 属性、constraints、layout sizing 和 clipping。
允许把散落但语义一致的图层归入同一个 Frame。
允许将装饰层设为不参与布局计算，前提是不改变视觉位置。
允许重命名无语义图层，但不得改变业务语义。
```

## 禁止操作

```text
不得删除原始图形、图标、图片、装饰、文字或业务节点。
不得用新建文字替换已有图形标题。
不得用新建图形替换已有文字标题。
不得改字体来解决渲染、加载或权限问题。
Auto Layout 阶段不处理字体 family；已有文字节点保留当前字体属性。
不得因为 Auto Layout 默认 gap、padding 或对齐方式而改变静态图的视觉位置。
不得用 constraints 或子节点坐标模拟排列效果替代 Auto Layout；设置 Auto Layout 必须通过 Plugin API 设置父级节点 layoutMode = "HORIZONTAL" 或 "VERTICAL"。
不得为了制作 Auto Layout 而擅自新增空白占位 Frame，例如 spacer、padding frame、hidden bucket。
不得新增无业务语义或仅为撑开布局的结构层。
允许自动执行背景层与内容层拆分、为表达已有排列关系新增有业务语义的 wrapper/container、调整父子层级，前提是不改变业务内容、可见文案、样式、尺寸、间距、Z 轴顺序和视觉结果。
如果结构调整会改变业务模块边界、Z 轴业务语义、可见内容归属，或必须新增空白占位 Frame，必须先列出结构调整方案并等待人工确认；未确认前不得执行。
复杂结构如果用 Auto Layout 会导致空白占位层、破坏原始视觉位置或改变业务归属，必须先说明保留普通 Frame + constraints 与结构调整两种方案的影响，不得自行裁定。
不得把不可见的样式源节点留在 Auto Layout 普通流里撑高父级。
不得把为了 Auto Layout 流程而新建、复制、迁移、隐藏的临时图层留在交付结构中；制作完成后必须自动删除。
Auto Layout 交付节点及其业务/装饰子节点默认禁止使用 Figma absolute positioning（layoutPositioning=ABSOLUTE）。
不得用 absolute positioning 来“保视觉位置”；必须优先通过 wrapper、padding、gap、Auto Layout 普通流、固定尺寸或语义容器表达结构。
只有当前任务或项目规则明确允许的背景层、覆盖层或特殊浮层才可以使用 absolute positioning，并必须在 run record 中记录节点、原因和允许来源。
当背景节点无法作为 Auto Layout 普通子项存在且不能使用 absolute positioning 时，允许把背景视觉属性转移到父 frame fill，但必须满足：背景节点原本就在该父 frame 内部，且视觉范围与该父 frame 边界一致，或明确只属于该父 frame 自身背景。
如果背景节点在目标 frame 外部，或覆盖多个模块、整页、遮罩、跨层级区域，则不得合并到局部 frame；应保留为页面级或模块级独立背景结构。
背景视觉属性转移后，不得把被流程隐藏的背景来源节点留在交付结构中；如该节点已不再承载业务/装饰交付语义，制作完成后必须删除，并在 run record 中记录来源节点、迁移目标和删除原因。
页面级背景必须纳入尺寸拉伸适配检查：如果背景在视觉上属于页面宽度或整屏区域，必须设置 horizontal stretch 或等效约束，使其跟随页面宽度变化。
不得只验证内容区和 fixed CTA 的拉伸；页面级背景、顶部渐变、整屏底色、遮罩背景都必须在临时拉伸副本中单独检查。
```

## Auto Layout 覆盖范围

```text
以 Flutter 布局需求为准，Page Frame 内部到 Element 上一层，所有直接子节点之间存在横向或纵向排列关系的 FRAME 都必须设置 layoutMode，包括 Page 内 Module 排列、Module 内 Control 排列、Control 内 Element 排列。
顶部导航栏按"顶部导航栏 Auto Layout 判定"节执行，属于例外。
背景层处理规则（完整版）：
情况 1：背景层与内容层在不同父 FRAME 下（背景独立）
背景层用普通 Frame + constraints，不做 Auto Layout。constraints 按以下规则设置：
- 贴顶背景：constraints vertical=TOP，horizontal=STRETCH，宽度跟随屏幕水平缩放。
- 贴底背景：constraints vertical=BOTTOM，horizontal=STRETCH，宽度跟随屏幕水平缩放。
- 全屏背景（尺寸与屏幕长宽一致）：constraints horizontal=STRETCH，vertical=STRETCH，同时跟随屏幕水平和垂直缩放。
- 背景内部有装饰子节点时，子节点同样按上述规则设置 constraints。
情况 2：背景层与内容层在同一父 FRAME 下且不侵入其他模块区域
将背景的视觉属性（fill、stroke、cornerRadius、shadow）转移到父 Frame 自身属性上，原背景节点删除，父 Frame 做 Auto Layout 排列内容子节点。父 Frame 的 constraints 按情况 1 的规则设置。
情况 3：背景层与内容层在同一父 FRAME 下但侵入其他模块区域
必须拆分，拆分后背景层按情况 1 处理，内容层按情况 2 处理。
```

## Module 级 Constraints 设置规则

```text
Page Frame 内的所有直接子 Module，必须按以下规则设置 constraints，使其随 Page Frame 尺寸变化正确响应：

- 所有内容模块（创作主卡、参数区、灵感列表等）统一设为全宽：x=0，width=Page Frame 宽度，constraints horizontal=STRETCH。
  左右视觉边距通过模块内部 padding 实现，不得把模块自身 width 缩窄为 Page Frame 宽度减去边距后的值。
  例如：创作主卡 x=0 w=360，内部 padding left=16 right=16，而不是 x=16 w=328。

- 全宽无内边距模块（页面背景、全屏遮罩）：x=0，width=Page Frame 宽度，constraints horizontal=STRETCH，vertical=STRETCH 或 MIN（按贴顶/全屏区分）。

- 固定底部悬浮 CTA：x=0，width=Page Frame 宽度，constraints horizontal=STRETCH，vertical=MAX（贴底）。
  回填完成后必须验证：bottom offset = Page Frame 高度 - CTA y - CTA 高度，应等于 0（或设计规定值）；若 y 偏移则必须修正。
  固定底部 CTA 必须是 Page Frame 的最后一个子节点（Z 轴最上层）；Auto Layout 回填如导致顺序变化，必须在完成后修正 Z 轴顺序，否则判定为 FAIL。

Module 内 Control 的 constraints 默认为 MIN+MIN，不需要单独设置，除非有明确响应需求。
```

## 子节点横向 Sizing 规则

```text
Module 内横向撑满的子节点（输入框、按钮、卡片内容区、列表容器等），必须设 layoutSizingHorizontal = FILL，不得写死固定宽度。
验证方式：拉伸 Page Frame 后，子节点宽度应同步变化；若不变，判定为需修正。
例外：有明确固定宽度语义的控件（如参数胶囊、图标按钮、固定尺寸卡片）可保持 FIXED，但必须在 run record 中说明原因。
```

## 带背景属性 Module 的 inner_wrapper 规则

```text
凡 Module 带有视觉背景属性（fill、border/stroke、cornerRadius、shadow/effects）且需要通过 padding 控制内容与背景边缘之间的视觉间距，必须在 Module 内部增加一层 inner_wrapper：
1. Module 本身：全宽（x=0，width=Page Frame 宽），无背景属性，无 padding，constraints=STRETCH。
2. inner_wrapper：承载所有背景属性（fill、stroke、cornerRadius、shadow），设置 padding，layoutSizingHorizontal=FILL，layoutSizingVertical=FIXED 或 HUG。
3. 子节点：在 inner_wrapper 内部排列，横向撑满子节点设 layoutSizingHorizontal=FILL。
不得将背景属性与 padding 同时设在 Module 本身上——背景属性决定视觉边界，padding 决定内容间距，两者作用于同一节点时背景会铺满全宽而内容缩进，导致视觉边界与内容边距不一致。
inner_wrapper 命名使用 `{module}_inner` 或 `{module}_card`，必须使用英文 snake_case，并表达业务语义。
```

## 结构原则

```text
页面主业务区块使用 `{module}_section`。
允许为表达已有排列关系自动新增有语义的 `{module}_container`、`{module}_wrapper`、`{module}_content_container`、`{module}_list` 或 `{module}_row`。
新增结构必须使用英文 snake_case，并表达业务语义或布局职责；不得使用 `wrapper_1`、`spacer`、`auto_layout_frame` 等无语义命名。
只有人工确认后，才可新增空白占位 Frame、纯 padding frame、hidden bucket 或无业务语义结构层。
具备视觉背景、描边、阴影或圆角的承载层使用 `{module}_card`、`{module}_surface` 或 `{module}_panel`。
横向 / 纵向重复内容容器使用 `{module}_list` 或 `{module}_carousel_list`。
重复项使用 `{module}_item_{n}`、`{module}_card_{n}` 或 `{module}_chip_{semantic}`。
固定底部悬浮 CTA 使用 `{action}_fixed_cta` 或 `{module}_fixed_cta`，并保持 fixed 语义。
```

## 重复控件 Wrap 规则

```text
参数选择器、标签组、chip group 等非横滑重复控件，如果父级宽度会随屏幕或容器变化，
必须使用可换行的 list 结构表达响应关系。

推荐结构：
module_xxx
  title
  xxx_chip_list
    xxx_chip_a
    xxx_chip_b
    ...

xxx_chip_list 使用 horizontal Auto Layout + wrap。
chip 自身保持按内容计算后的固定 / hug 尺寸。
父级变宽时，chip 应按可用宽度提行；父级变窄时，chip 应换行。

不得只设置父级 horizontal stretch，却让内部 chip 继续停留在固定绝对坐标。
如新增 list / wrapper 是为了表达已有参数组或标签组的真实排列关系，可以自动执行。
自动执行时必须在 run record 中记录 old_parent、new_parent、调整原因、静态视觉不变性校验和回滚方式。
```

## 横向静态展示区

```text
横向示例、横向卡片列表、横向灵感列表在当前状态只需保证静态展示正确时，
可使用非对称可视区：
- x 等于左安全边距。
- width 等于页面宽度减左安全边距，右边贴到屏幕边界。
- 初始状态最左侧内容完整展示，不得被左边裁切。
- 内部卡片可向右延展。

只有 Wireframe、Layout Spec 或 Visual Spec 明确标注横滑 / 横向滚动时，
才进一步建立 viewport + inner list 的完整滚动结构。
```

## 检查流程

```text
1. 修改前读取目标节点和参考节点 metadata。
2. 判断哪些节点是用户原始界面元素，哪些是可新增的结构包装层。
3. 先保留静态坐标建立结构，再逐步设置 Auto Layout。
4. 每次修改后用 metadata 检查关键节点 x/y/width/height 是否偏离静态稿。
5. 每个目标节点设置完成后，必须读取该节点 layoutMode 属性，确认值为 HORIZONTAL 或 VERTICAL；layoutMode 为 NONE 视为未生效，必须重新执行，不得带入后续流程。
6. 自动执行 screenshot 检查，确认 Auto Layout 修改前后视觉是否发生非预期变化；截图检查只用于 Auto Layout 视觉不变性校验，不作为全局视觉审美判断。
7. 如需临时拉伸测试，必须复制临时副本，测试后删除副本；测试项必须覆盖页面级背景、内容安全区、主要内容模块和 fixed CTA。
8. 交付前必须扫描目标节点整棵树，检查是否存在由 Auto Layout 流程新建、复制、迁移或隐藏后遗留的临时隐藏图层；若存在必须删除，不能交付。
9. 交付前必须扫描目标节点整棵树，检查是否存在 layoutPositioning=ABSOLUTE；若存在且当前任务或项目规则未明确允许，必须先修复，不能交付。
10. 交付前必须扫描本次新增/修改的规则、记录、页面文件和交付说明，检查是否包含本机绝对路径；若存在必须改为仓库相对路径。
11. 最终回复必须明确说明流程临时隐藏图层扫描结果、absolute positioning 扫描结果和本机绝对路径扫描结果。
12. 所有冲突、放弃项、结构调整方案、人工确认结果和执行结果必须写入 run record。
```

## 落盘边界

```text
跨页面、跨项目稳定成立的 Auto Layout 方法进入 rules/autolayout_rules.md。
当前项目同类页面稳定成立的 UI 调整进入 workspace/design_system/manual-hifi-adjustment-rules.md。
单个页面或单个状态的具体节点、坐标、业务状态和修复记录进入 workspace/visual_specs/{page_id}.md 或 workspace/records/run_xxx.md。
一次性错误、回滚说明和项目反馈必须进入 workspace/records/run_xxx.md，不进入通用规则。
规则、记录、页面文件和交付说明中禁止使用本机绝对路径；引用项目文件必须使用仓库相对路径。
“绝对路径”和 “Figma absolute positioning” 是两个独立禁止项：前者禁止出现在文本落盘和交付说明中，后者禁止出现在 Auto Layout 交付结构中，除非当前任务或项目规则逐项明确允许。
```

## Auto Layout 结构调整边界

```text
需要人工确认：
- 新增空白占位 Frame，例如 spacer、padding frame、hidden bucket。
- 新增无业务语义或仅为撑开布局的结构层。
- 为了 Auto Layout 改变业务模块边界、Z 轴业务语义或可见内容归属。

可以自动执行：
- 背景层与内容层拆分，前提是不改变视觉效果和业务归属。
- 为表达已有排列关系新增有业务语义的 wrapper/container。
- 调整父子层级，前提是不改变业务内容、可见文案、样式、尺寸、间距和视觉顺序。
- 将已有同类子项归入语义容器，例如参数行、卡片列表、按钮内容组。

自动执行要求：
- 新增结构必须使用英文 snake_case，并表达业务语义或布局职责。
- 每次结构调整必须记录 old_parent、new_parent、调整原因和视觉不变性校验结果。
- 调整后必须执行 metadata、screenshot、absolute positioning 扫描和 Layer Naming Recheck。
```

## 结构调整审批机制

```text
允许为 Auto Layout 新增有语义的 wrapper、container 或调整父子层级，但必须满足：

1. 只允许为了表达布局关系、响应关系或 Auto Layout 约束。
   不得新增、删除、合并或拆分业务内容、按钮、状态、入口、文案或交互语义。

2. 属于「可以自动执行」范围的结构调整可直接执行；属于「需要人工确认」范围的结构调整，
   必须执行前列出拟调整的节点清单、调整原因、预期 Auto Layout 收益和风险，等待人工确认；未确认前不得执行。

3. 确认后执行时，必须记录每处结构变化：
   - 调整前父级
   - 调整后父级
   - 是否新增 wrapper/container
   - 调整原因
   - 回滚方式

4. 执行后必须完成：
   - metadata 对比，关键节点 x/y/width/height 不得有 1px 以上偏移
   - screenshot 对比，不得出现可见视觉差异
   - 临时拉伸测试，验证响应逻辑
   - 删除临时测试副本
   - Layer Naming Recheck
   - absolute positioning 扫描

5. 如出现 1px 以上偏移、层级遮挡、文案折行、资产丢失或业务语义变化，
   必须停止并报告，不得继续下游流程。
```

## 顶部导航栏 Auto Layout 判定

```text
顶部导航栏必须先判断真实结构，再决定使用 Auto Layout 还是 constraints。

只有以下两种情况才使用横向 Auto Layout：
1. 左侧 + 右侧同时有内容（无中间内容）：使用 Auto Layout，space-between。
2. 左侧 + 中间 + 右侧同时有内容：使用 Auto Layout，通过左右区域等宽或经确认的布局 spacer 保持中间内容视觉居中。

除以上两种情况外，其余所有结构（只有左侧内容、只有右侧内容、只有中间内容、只有左侧+中间、只有中间+右侧等）一律不使用横向 Auto Layout，改用 constraints 固定各内容位置。

不得为了凑两栏或三栏结构新增不可见业务组件、伪按钮或无语义占位内容。

如需新增布局 wrapper、container 或 spacer 才能表达 Auto Layout 结构，必须走「结构调整审批机制」。

导航栏处理后，必须检查：
- 各内容位置符合静态稿视觉
- 各内容未被拉伸或压缩变形
- 关键节点 x/y/width/height 无 1px 以上非预期偏移
```

## Z 轴独立层处理规则

```text
Z 轴与内容层不同的层，包括：
- 背景层：任何承担背景功能的矩形或 frame，不限于渐变，纯色背景同样适用。
- 悬浮层：弹窗、Toast、吸顶导航、底部悬浮按钮等。

以上层禁止放入内容 Auto Layout 流（content_frame 或任何 layoutMode=VERTICAL/HORIZONTAL 的容器）。

正确结构：作为 Page Frame 的直接子节点，与 content_frame 平级，通过节点顺序控制 Z 轴位置：
- 背景层排在 content_frame 之前（Z 轴在内容下方）。
- 悬浮层、固定底部层排在 content_frame 之后（Z 轴在内容上方）。

各层通过 constraints 独立控制位置：
- 贴顶背景层：constraints horizontal=STRETCH, vertical=MIN
- 贴底悬浮层：constraints horizontal=STRETCH, vertical=MAX
- 全屏背景层：constraints horizontal=STRETCH, vertical=STRETCH

禁止使用 layoutPositioning=ABSOLUTE 表达上述层级关系。
```

## 背景矩形节点迁移规则

```text
当背景矩形节点（rounded-rectangle 或 rectangle）的所有视觉属性（fill、stroke、cornerRadius、shadow/effects）全量迁移到父级 frame 属性后，原背景矩形节点必须删除，不得保留原节点。

适用场景：
- 模块内 inner_wrapper 迁移（将 surface 节点属性迁移到新建的 inner_wrapper frame）
- 父 frame fill 合并（将背景节点属性迁移到父 frame 自身属性）

迁移后检查：
- 父级 frame 视觉属性（fill、cornerRadius、shadow）与原背景矩形一致
- 原背景矩形节点在图层树中不可见且不存在
- 截图确认视觉无变化后，方可进入下一步
```

## Step 7 后置验证（mandatory）

```text
对所有 constraint vertical 为 MAX 或 MIN 的节点，
在 setLayoutMode / setPadding 操作完成后，
必须立即 get_node 回读 y 和 height，
计算 bottom = y + height，
断言 bottom ≤ page_frame.h。
如果 bottom > page_frame.h，立即修正 y = page_frame.h - height，
再次回读确认，不得跳过。
```

## Step 8 Gate Check 补充检查项

```text
- [ ] page_frame 所有直接子节点：bottom = y + height ≤ page_frame.h
      FAIL 条件：任意节点 bottom > page_frame.h
      FAIL 时：报告节点 ID 和溢出量，不得输出 PASS
```
