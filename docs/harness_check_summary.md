# Harness Check 完整清单（2026-05-26 更新版）

本文档为 `rules/harness_rules.md` 的可读性汇总，经过全面机械化改写，所有检查项均已转为可客观验证的断言。

从 2026-05-27 起，Gate 结论必须由 `scripts/harness_check.py` 生成的结构化文件裁决：

```text
workspace/harness/{run_id}_{gate}_gate.json
```

结论只允许三种：**PASS（附具体证据）**、**FAIL（附具体违规位置）**、**BLOCKED（上游 Gate 未 PASS 或缺少 gate json）**。

Agent、run record、自然语言总结、截图存在本身和 Figma Frame 已生成，都不能作为 Gate PASS。缺少 gate json 时默认 BLOCKED。

当前机器检查入口覆盖以下 Gate：

```text
intent
priority
layout
wireframe_preflight
structure_mapping
design_system
visual_spec
hifi_generation
```

---

## Step 01 — Intent Gate

**[1]** Intent 字段逐项对应 PRD，必须在 run record 中逐条列出，不得以"已覆盖"一句带过：
- (a) Intent 中每个字段（page_goal、primary_action、secondary_entries、key_states、hard_constraints）必须写出对应的 PRD 段落编号或原文引用；写不出，FAIL。
- (b) PRD 中含"必须"、"核心"、"不得"、"禁止"、"默认"语义的句子，必须在 Intent 的 hard_constraints 中逐条体现；缺少任一条，FAIL。

---

## Step 02 — Priority Gate

**[2]** Priority Map 能证明同时参考了 PRD 和 Intent，必须在 run record 中提供具体引用：
- (a) 每个 P0/P1 模块必须写出 PRD 来源（段落编号或原文引用）；写不出，FAIL。
- (b) 每个 P0/P1 模块必须写出 Intent 来源（字段名：page_goal / primary_action / secondary_entries / key_states / hard_constraints）；写不出，FAIL。

**[3]** Priority Map 分级逐项对应 Intent 字段，且 PRD 必须出现的元素均已覆盖，必须逐项列出：
- (a) 每个模块必须写出对应的 Intent 字段名；写不出，FAIL。
- (b) PRD 中含"必须"、"核心"、"默认"语义的每个元素，必须在 Priority Map 中以 P0 或 P1 出现；缺少任一，FAIL。
- 不得以"业务核心"、"设计需要"等自定义理由代替 Intent 字段名或 PRD 原文，FAIL。

---

## Step 03 — Layout Gate

**[4]** Layout Spec 能证明同时参考了 PRD、Intent 和 Priority Map，必须在 run record 中逐条列出引用：
- (a) 每个 module 必须写出 Priority Map 中对应的 module_id 和优先级（P0–P3）；写不出，FAIL。
- (b) 每个 module 必须写出 PRD 段落编号或原文引用作为业务依据；写不出，FAIL。
- (c) Intent.hard_constraints 中每条约束必须在 Layout Spec 中有对应体现；不为空但无对应体现，FAIL。

**[5]** Layout Spec 每个 module 包含线框图生成所需的最小字段，必须逐项验证：
- (a) 每个 module 必须有明确尺寸规格（显式 width/height 数值，或 width=100% 且有父容器参照）；缺失，FAIL。
- (b) 每个包含子内容的 module 必须有 layout_direction（horizontal / vertical / stack）；缺失，FAIL。
- (c) 每个叶子 module 必须有 content 描述或 component_candidate；两者均缺，FAIL。

**[6]** Layout Spec 的 Frame 树字段符合 Figma 图层创建要求，不得以"可映射"一句带过：
- (a) 每个 module 的 frame_role 必须是 page / module / control / element 之一；不在此列或缺失，FAIL。
- (b) 每个 module 的 parent 必须指向已存在的 module_id 或显式标注为页面根；指向不存在的 module_id，FAIL。
- (c) 凡列出 component_candidate 的 module，必须同时写出 component_reason；有 candidate 无 reason，FAIL。

**[附]** 检查 Priority Map 中的元素是否被覆盖或明确排除。

**[附]** 检查 Frame 树是否无孤立模块、无循环引用、无无语义命名。

---

## Step 03 — Wireframe Preflight Gate

**[7]** PRD、Intent、Priority Map 和 Layout Spec 四者之间无冲突、无关键遗漏、无凭空新增，必须逐项列出结论：
- (a) 凭空新增：Layout Spec 中每个 module 必须能写出对应的 PRD 段落编号或原型图标注；写不出，FAIL。
- (b) 关键遗漏：PRD 中每个含"必须"、"核心"、"默认"语义的元素必须能在 Layout Spec 的 module 列表中找到对应 module_id；找不到，FAIL。
- (c) 冲突：Layout Spec 中任何 module 的顺序、包含关系或存在性与 PRD 正文或 Intent 描述相反，FAIL。

**[附]** 检查 Layout Spec 的 Frame 树是否足以按 Page Frame → Module Frame → Control Frame → Element 顺序生成 Figma 图层。

**[附]** 检查 Layout Spec 和 Wireframe 计划中的可见文案是否来自 PRD、PRD 原型图或已确认上游产物，不得自行改写、润色、缩写、扩写、翻译或替换。

**[附]** 检查组件候选是否仍为候选记录，不得在线框图阶段升级为正式组件库。

> 只有通过 Wireframe Preflight Gate，才能进入 Figma Wireframe 生成。

---

## Step 05 — Structure Mapping Harness Check

**[附]** 检查线框图 Page Frame 是否全部处理。

**[9]** 线框图保留 Page Frame → Module Frame → Control Frame → Element 层级，必须在 run record 中逐一列出 Page Frame 所有直接子节点：
- 直接挂在 Page Frame 下的非 Module-Frame 节点数量必须为 0；任何 Text、Rectangle、Group 或未命名 Frame 直接作为 Page Frame 子节点，FAIL。
- 不得以"层级正常"一句带过。

**[10]** Priority Map 中每个 P0/P1/P2 模块在 Structure Mapping 中都有明确处理记录，必须逐一列出：
- (a) 映射成功：必须写出采样端 Figma 来源对应节点 ID（格式 n:n）、节点字段名、sample_priority 和 sample_url；写不出节点 ID 或采样来源，FAIL。
- (b) 明确未映射：必须写出未映射原因并说明设计决策来源；只写"无对应"或"新增"一词，FAIL。
- 不得以"基本对应"、"参考旧稿"、"结构类似"等模糊表述代替，FAIL。

**[11]** Structure Mapping 中每个 component_candidate 有采样端 Figma 来源结构依据，必须逐条列出：
- (a) 每个 candidate 必须写出采样端 Figma 来源对应节点 ID（格式 n:n）、节点类型、sample_priority 和 sample_url；写不出，FAIL。
- (b) 如采样端 Figma 来源无对应组件，必须写出"采样端无对应组件"并说明替代依据（Design System style_id 或 PRD 原型图标注编号）；不说明，FAIL。

**[12]** 组件候选的映射依据包含结构层面的共同点，不得以视觉相似作为唯一映射理由，必须逐条列出：
- (a) 映射依据必须包含以下三项之一以上：相同 frame_role、相同子元素类型组成、相同业务语义；仅凭"视觉相似"、"颜色相近"、"尺寸接近"，FAIL。
- (b) 必须写出采样端节点的 frame_role 和子元素类型，与目标 module 进行逐项比对；缺少比对记录，FAIL。

**[13]** Structure Mapping 中每个映射确认源模块与目标模块服务同一业务功能，必须逐条写出业务语义对比：
- (a) 每个映射必须写出采样端节点的业务功能描述和目标 module 的业务功能描述；两者业务语义明显不同，FAIL。
- (b) 仅继承结构规格但业务内容不同的映射，必须明确标注"仅继承结构规格，不继承业务内容"；缺少标注，FAIL。

**[附]** 检查低置信度映射是否进入 mapping-review.md。

---

## Step 06 — Design System Harness Check

**[DS-1]** raw-style-inventory.json 必须有顶层 items 数组，每条 item 必须有 id、source_node_id、sample_priority、sample_url、decision_level；缺少任一，FAIL。

**[DS-2]** decision_level 只允许 component_match、priority_sampling、structure_fallback；其他值，FAIL。

**[DS-3]** design-system-draft.json 每个 style_id 必须有 source_ref，且能在 raw-style-inventory.items.id 中找到；找不到，FAIL。

**[DS-4]** style_id 不得含点号；出现含点号的全局语义 token 命名，FAIL。

**[14]** design-system-review.md 中冲突项必须以表格逐行列出：属性名 | PRD值 | 源文件值 | 暂定值 | 状态：
- 状态字段只允许两种值：「待人工确认」或「已人工确认（附决定日期）」；AI 执行阶段写入其他裁定结论，FAIL。
- design-system-draft.json 中凡有冲突的属性，review_required 必须为 true；review_required 为 false 但状态仍为「待人工确认」，FAIL。

**[附]** 不得把 AI 推测值写入 raw-style-inventory.json；每条采集值必须来自真实 Figma 节点。

---

## Step 07 — Visual Spec Harness Check

**[15]** Visual Spec 中每个模块的关键属性能逐条追溯到上游产物的具体值，必须逐条列出来源：
- (a) 尺寸 / 间距：必须写出 Layout Spec 中对应字段名和数值；无法写出，FAIL。
- (b) 颜色：必须写出 design-system-draft.json 中对应 style_id 和十六进制值；找不到，FAIL。
- (c) 字体 / 字号 / 字重：必须写出 design-system-draft.json 中对应 style_id；找不到，FAIL。
- (d) 圆角：必须写出 design-system-draft.json 中对应 style_id；找不到，FAIL。
- (e) 模块存在性：Visual Spec 中出现的每个模块必须在 Priority Map 中有 P0/P1/P2/P3 分级记录；Priority Map 未列出，FAIL。

**[16]** Visual Spec 中 P0/P1/P2/P3 分级转译为可量化的视觉属性差异，必须逐级列出对应视觉值：
- (a) P0 模块必须在以下至少两项上与 P1/P2/P3 有具体数值差异：字号（px）、字重（数值）、颜色（十六进制）、尺寸（px）；写不出，FAIL。
- (b) P1 模块必须在以下至少一项上与 P2/P3 有具体数值差异：字号、字重、颜色；写不出，FAIL。
- (c) 不得出现两个不同优先级模块在同一属性上数值相同的情况；如存在，必须写出其他属性上的区分依据，否则 FAIL。

**[17]** Visual Spec 中如存在 Design System 未定义的设计值，必须逐条列出，不得以"无法覆盖"一句带过：
- (a) 每个颜色值未在 design-system-draft.json 中找到 style_id 时，必须写出已搜索但不存在的 style_id 和搜索路径，并标注"待人工确认"；无法写出搜索记录，FAIL。
- (b) 每个圆角值、字号、字重未找到 style_id 时，必须写出搜索记录和"待人工确认"标注；无法写出，FAIL。
- (c) 凡标注"待人工确认"的条目必须在 design-system-review.md 中有对应行记录；缺少，FAIL。

**[附]** Visual Spec 中引用的每个 style_id（格式 `style_id: xxx`）必须存在于 design-system-draft.json.styles；找不到，FAIL。

**[18]** Visual Spec 中每个 Tab、按钮、输入字段、状态、模块和交互控件均有 Priority Map 条目对应，必须逐一列出：
- (a) 每个交互控件或功能模块必须能写出 Priority Map 中对应的模块名和优先级（P0–P3）；写不出，FAIL。
- (b) 不得以"视觉需要"或"样式参考"为由写入 Priority Map 未列出的 Tab、按钮、状态或交互入口；如存在，FAIL。

---

## Step 08 — Hi-Fi Generation Harness Check

**[19]** Hi-Fi 覆盖 Visual Spec，必须在 run record 中逐一列出每个模块及其在 Hi-Fi 中的对应图层名：
- (a) Visual Spec 中每个模块必须在 Hi-Fi 中有同名或注释说明等价名的 Frame；缺少任一，FAIL。
- (b) 每个模块的关键尺寸属性（width、height、padding）必须能写出具体 Figma 属性值作为证据；写不出，FAIL。

**[附]** 检查 Page Frame 是否保持 360 × 780。

**[附]** 检查高保真稿是否完整继承线框图已有可见文案，不得改写、润色、缩写、扩写、翻译或替换。

**[20]** Hi-Fi 处于可编辑状态，必须逐项验证：
- (a) 不得存在 isLocked=true 的图层；如存在，必须列出图层名，FAIL。
- (b) 文本图层必须是 TEXT 类型，不得是 VECTOR 或 BOOLEAN_OPERATION；如存在栅格化文本，必须列出图层名，FAIL。
- (c) 所有 Frame、Group 的命名必须符合 Layer Naming 规范（英文 snake_case，有业务语义，无默认 Figma 名称）；不符合，FAIL（与 Layer Naming Gate 联动）。

**[21]** Hi-Fi 未临场改写业务结构或设计规则，以下任一触发 FAIL，必须逐项列出比对结论：
- (a) Hi-Fi 中 Page Frame 直接子 Frame 数量 ≠ Wireframe 中 Page Frame 直接子 Frame 数量。
- (b) Hi-Fi 中任一模块的可见文案与 PRD 原文逐字不符（改写、缩写、润色、扩写均算）。
- (c) Hi-Fi 中出现 Visual Spec 未定义的颜色值（十六进制）。
- (d) Hi-Fi 中出现 Visual Spec 或 design-system-draft.json 未定义的圆角值。

**[附]** Hi-Fi 使用的颜色值必须能在 run record 或 Visual Spec 中找到对应的 style_id 追溯记录（格式：颜色值 -> style_id -> source_ref）。

**[附]** 检查是否没有因视觉采样新增线框图或 Visual Spec 未定义的内容模块、Tab、按钮、字段、状态或交互控件。

**[附]** 检查是否没有把采样稿、旧界面或采样端 Figma 来源页面整体复制、整体移植或整体替换到当前设计稿；如存在，判定为严重生成偏差，不得通过。

**[附]** 检查是否没有因视觉采样改写目标稿已有文案、功能架构、业务状态或交互语义；视觉采样只能改设计规范，不能改业务内容。

**[附]** 如存在按钮、Tab、选择器、输入框、卡片、列表等组件形态的等价视觉表达替换，检查业务对象、触发动作、可选项含义、选项数量、激活 / 禁用状态语义、输入字段含义和必要入口是否保留，是否未新增业务入口、未删减功能、未迁移采样稿文案。

**[22]** Hi-Fi 中采样源资产的复用情况，必须在 run record 中逐条列出每个资产的处理决策：
- (a) 凡采样端 Figma 来源中有明确节点 ID（格式 n:n）且类型为 IMAGE 或 VECTOR 的资产，必须在 Hi-Fi 中复用；如使用占位代替，必须写出"节点 n:n 无法复用"及具体原因；无法写出节点 ID、sample_priority、sample_url 和原因，FAIL。
- (b) 如采样端 Figma 来源中无对应资产节点，必须明确写出"采样端无对应资产"并说明占位类型；无说明，FAIL。

**[附]** 检查渐变样式是否同时匹配 gradientStops 和 gradientTransform，且没有使用默认渐变方向替代采样源方向。

**[23]** Hi-Fi 中装饰性资产的图层归属和 Z 轴顺序，必须逐条列出：
- (a) 每个装饰性资产必须位于其装饰目标的业务 Frame 内部（与装饰目标同一 Module Frame 下），不得直接挂在 Page Frame 下或位于其他业务模块的 Frame 内；违反，FAIL。
- (b) 每个装饰性资产在其父 Frame 内的 Z 轴顺序必须低于（图层列表中排列于下方）同 Frame 内的主要内容图层；违反，FAIL。

**[附]** 检查用于计算间距的 Module Frame 是否收紧到有效子元素外接边界，主模块间距是否按真实边界一致计算。

**[附]** 检查按钮、Chip、标签等控件文字是否在背景容器内 X/Y 双轴居中。

**[附]** 检查字段名和值是否在语义需要时拆成独立文本，且未为已取消交互的字段添加箭头或其他交互暗示。

**[附]** 如页面存在固定底部 CTA，检查 CTA 是否以 Page Frame 底部为基准保持 24px 下边距、位于 Z 轴最上层、有 90px 底部保护背景层，且关键内容未被 CTA 覆盖。

**[附]** 如用户提供【采样源】截图和【设计图】截图，检查是否已执行截图视觉对比审核，并输出对比结论、偏差清单、修改建议、偏差归因和是否需要重跑。

---

## Step 08 — Layer Naming Harness Gate

**[附]** 检查目标范围内 frame-like 节点是否不存在默认 Figma 名称（Frame 1、Group 1、Rectangle 8、Text 12 等）。

**[附]** 检查目标范围内 frame-like 节点是否不存在中文命名、无上下文 label、无交付意义 source_ 前缀和纯位置词命名。

**[附]** 检查命名是否统一使用英文 snake_case，并表达业务语义或结构职责。

**[附]** 检查重复项数字尾缀是否只用于真实重复项或资产序列，不用于临时占位。

**[附]** 检查命名调整是否只改变 name，不改变视觉、布局、层级、样式、文字内容或业务语义。

**[附]** 检查命名扫描结果、剩余问题和人工确认点是否写入 run record。

> 只有 Layer Naming Harness Gate 通过，才允许进入 Auto Layout 回填。

---

## Step 08 — Auto Layout Harness Gate

**[附]** 检查 Auto Layout 回填是否保持原静态稿视觉位置、尺寸、间距、字体、图片、图标、装饰和业务层级不变。

**[附]** 检查是否没有为了 Auto Layout 新增未经确认的 wrapper、container、spacer、padding frame 或 hidden bucket。

**[附]** 检查复杂结构是否允许保留普通 Frame，并通过 constraints 表达响应关系。

**[附]** 检查目标树是否不存在未经用户明确允许的 layoutPositioning=ABSOLUTE。

**[附]** 检查背景、整屏视口、安全内容区、横滑列表、固定底部 CTA 和页面级浮层是否符合对应宽度、约束和层级规则。

**[附]** 检查是否已自动执行 metadata、screenshot 和必要的临时拉伸副本校验，且测试后删除临时副本。

**[附]** 检查本次新增或修改的规则、记录、页面文件和交付说明是否不存在本机绝对路径。

**[附]** 检查冲突、例外、放弃项、人工确认点、absolute positioning 扫描结果和本机绝对路径扫描结果是否写入 run record。

> 只有 Auto Layout Harness Gate 通过，才允许进入交付。

---

## Step 09 — Backfill Harness Check

**[25]** Backfill 中每条人工审核结论已明确标注归属范围，必须在 run record 中逐条列出：
- (a) 单页修正：结论标注 scope=single_page，只写入 workspace/records/run_xxx.md，不得写入 workspace/design_system/ 或 rules/；违反，FAIL。
- (b) 项目级设计系统结论：结论标注 scope=project，只写入 workspace/design_system/，不得写入 rules/；违反，FAIL。
- (c) 跨项目通用规则：结论标注 scope=cross_project 且写出可复用的业务场景描述；无场景描述，FAIL。

**[附]** 检查项目内同类页面可复用但尚不适合进入跨项目 rules/ 的高保真手动调整，是否进入 workspace/design_system/manual-hifi-adjustment-rules.md。

**[26]** 写入 design system 或 rules/ 的每条结论满足稳定性和可复用性要求，必须逐条列出依据：
- (a) 稳定性：必须有人工确认记录（run record 中含裁定日期和决定描述）；无人工确认记录，不得写入，FAIL。
- (b) 可复用性：写入 rules/ 的结论必须写出适用的业务场景范围；仅描述当前页面具体事实，不得写入 rules/，FAIL。

**[附]** 检查回填是否记录来源、影响范围和是否需要重跑。

**[27]** 如存在截图视觉对比偏差，每条偏差有可核查的归因依据，必须在 run record 中逐条列出：
- (a) 单页修正：必须写出"此偏差只影响当前页面，其他同类页面无相同问题"；无此声明，不得归类为单页修正，FAIL。
- (b) 设计系统缺口：必须写出 Design System 中缺少的具体 style_id；写不出，不得归类，FAIL。
- (c) Visual Spec 表达不足：必须写出 Visual Spec 中缺失或描述不清的具体字段名和缺失内容；写不出，不得归类，FAIL。
- (d) 生成执行偏差：必须写出 Hi-Fi 生成中具体哪步操作与 Visual Spec 不符（含字段名和数值）；写不出，不得归类，FAIL。
- 不得把单张截图事实直接写入 rules/；只有经人工确认且跨项目适用的结论才能进入 rules/；违反，FAIL。

---

## 使用说明

- **[数字]**：原始 27 条定性清单中被机械化改写的编号，便于追溯修改历史。
- **[附]**：原始清单中判定为已足够具体、未列入 27 条的检查项，保持原文不变。
- 所有检查结论只允许两种：**通过（附产物中的具体字段值或节点 ID）** 或 **失败（附具体违规位置）**。
- 禁止使用模糊表述："基本符合"、"大体正确"、"来源可追溯"等均判定为失败。
