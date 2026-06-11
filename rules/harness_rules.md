# Harness Rules

## 目标

Harness 用于在每一步生成后验证产物是否可进入下一步，尤其是在生成 Wireframe 前完成总校验，并在高保真阶段约束 AI 不偏离业务结构和设计系统。

## 强制执行合约

```text
Harness Gate 是流程唯一放行来源。
任何 Gate 的 PASS / FAIL / BLOCKED 结论只能由 scripts/harness_check.py 生成的 workspace/harness/{run_id}_{gate}_gate.json 表达。
Agent、人工执行记录、自然语言总结、截图存在本身、Figma Frame 已生成，本身均不能作为 PASS 依据。
缺少 gate json 时，该 Gate 默认视为 BLOCKED。
上游 Gate 未 PASS 时，下游阶段默认 BLOCKED，不得继续生成或标记通过。
run record 只能汇总 gate json 的结果，不得手写 Gate PASS。
如 run record 与 gate json 冲突，以 gate json 为准；冲突必须记录为执行异常。
```

## Gate Contract 格式

每个 Gate 必须按以下合约执行；规则文档负责定义标准，脚本负责裁决：

```text
必须输入：该 Gate 可读取的上游产物、Figma 元数据、采样端链接和人工确认记录。
必须输出：该阶段产物和 workspace/harness/{run_id}_{gate}_gate.json。
PASS 条件：所有必填文件存在，所有证据字段完整，所有可追溯关系成立，blocking_errors 为空。
FAIL 条件：当前 Gate 的输入或产物存在缺失、冲突、不可追溯、字段不完整、AI 自行裁定或模糊表述。
BLOCKED 条件：任一上游必需 Gate 不是 PASS，或缺少上游 gate json。
禁止事项：禁止手写 PASS；禁止用“已覆盖”“基本一致”“参考旧稿”等自然语言替代证据；禁止 Gate 失败后继续下游生成。
下游解锁条件：只有当前 Gate 的 gate json 中 status 为 PASS，下一阶段才允许执行。
```

`workspace/harness/{run_id}_{gate}_gate.json` 必须至少包含：

```json
{
  "run_id": "run_001",
  "gate": "design_system",
  "status": "FAIL",
  "checked_by": "scripts/harness_check.py",
  "checked_at": "2026-05-27T00:00:00+00:00",
  "evidence_files": [],
  "upstream_gates": {},
  "blocking_errors": [],
  "warnings": []
}
```

## 基本原则

```text
PRD 是最高业务边界。
Intent、Priority Map、Layout Spec、Wireframe、Structure Mapping、Design System、Visual Spec 和 Hi-Fi 不得与 PRD 冲突。
下游产物不得凭空新增 PRD 未定义的核心业务能力。
PRD 中影响页面表达的强约束不得遗漏。
每一步都必须能说明关键判断来自 PRD、Intent、Priority Map、Layout Spec、Wireframe、采样端 Figma 来源、Structure Mapping 或 Design System。
```

## 分步 Gate

```text
Intent Gate：
检查 Intent 是否逐项对应 PRD 中的页面目标、用户任务、关键状态和硬约束，必须在 run record 中逐条列出对应关系，不得以"已覆盖"一句带过：
(a) Intent 中每个字段（page_goal、primary_action、secondary_entries、key_states、hard_constraints）必须写出对应的 PRD 段落编号或原文引用；写不出来，判定为未覆盖，FAIL。
(b) PRD 中含"必须"、"核心"、"不得"、"禁止"、"默认"语义的句子，必须在 Intent 的 hard_constraints 字段中逐条体现；缺少任一条，判定为硬约束遗漏，FAIL。

Priority Gate：
检查 Priority Map 是否能证明同时参考了 PRD 和 Intent，必须在 run record 中提供具体引用，不得以"已参考 PRD 和 Intent"一句带过：
(a) Priority Map 中每个 P0/P1 模块必须写出 PRD 来源（段落编号或原文引用），用以说明该模块为何存在于页面；写不出任何 PRD 段落编号，判定为未参考 PRD，FAIL。
(b) Priority Map 中每个 P0/P1 模块必须写出 Intent 来源（对应字段名：page_goal / primary_action / secondary_entries / key_states / hard_constraints），用以说明该模块分级的依据；写不出任何 Intent 字段名，判定为未参考 Intent，FAIL。
检查 Priority Map 中每个 P0/P1/P2/P3 分级是否对应到 Intent 的具体字段，且 PRD 必须出现的元素均已覆盖，必须在 run record 中逐项列出，不得以"服务 Intent"一句带过：
(a) Priority Map 中每个模块必须写出对应的 Intent 字段名（page_goal / primary_action / secondary_entries / key_states / hard_constraints）；写不出字段名，判定为无依据分级，FAIL。
(b) PRD 中含"必须"、"核心"、"默认"语义的每个元素，必须在 Priority Map 中以 P0 或 P1 出现；缺少任一此类元素，判定为遗漏，FAIL。
不得以"业务核心"、"设计需要"等自定义理由代替具体 Intent 字段名或 PRD 原文，否则判定为 FAIL。

Layout Gate：
检查 Layout Spec 是否能证明同时参考了 PRD、Intent 和 Priority Map，必须在 run record 中逐条列出引用关系，不得以"已参考"一句带过：
(a) Layout Spec 中每个 module 必须写出 Priority Map 中对应的 module_id 和优先级（P0–P3）；写不出，判定为未参考 Priority Map，FAIL。
(b) Layout Spec 中每个 module 必须写出 PRD 段落编号或原文引用，作为该模块存在的业务依据；写不出，判定为未参考 PRD，FAIL。
(c) Intent.hard_constraints 中每条约束必须能在 Layout Spec 中找到对应的设计约束体现（如宽度固定、模块位置限制）；Intent.hard_constraints 不为空但 Layout Spec 无对应体现，判定为未参考 Intent，FAIL。
检查 Priority Map 中的元素是否被覆盖或明确排除。
检查 Layout Spec 中每个 module 的描述是否包含线框图生成所需的最小字段，必须逐项验证，不得以"描述充分"或"足以"一句带过：
(a) 每个 module 必须有明确的尺寸规格（显式 width/height 数值，或 width=100% 且有明确父容器参照）；缺失，判定为尺寸未定义，FAIL。
(b) 每个包含子内容的 module 必须有 layout_direction（horizontal / vertical / stack）；缺失，判定为布局方向未定义，FAIL。
(c) 每个叶子 module 必须有 content 描述或 component_candidate；两者均缺，判定为内容未定义，FAIL。
检查 Layout Spec 的 Frame 树字段是否符合 Figma 图层创建要求，不得以"可映射"一句带过：
(a) 每个 module 的 frame_role 必须是 page / module / control / element 之一；不在此列或缺失，判定为无法映射到 Figma 图层类型，FAIL。
(b) 每个 module 的 parent 必须指向 Layout Spec 中已存在的 module_id，或显式标注为页面根；parent 指向不存在的 module_id，判定为悬空引用，FAIL。
(c) 凡列出 component_candidate 的 module，必须同时写出 component_reason；有 candidate 无 reason，判定为 FAIL。
检查 Frame 树是否无孤立模块、无循环引用、无无语义命名。

Wireframe Preflight Gate：
检查 PRD、Intent、Priority Map 和 Layout Spec 之间是否存在可列举的冲突、遗漏或新增，必须逐项列出结论，不得以"整体符合"一句带过：
(a) 凭空新增：Layout Spec 中每个 module 必须能写出对应的 PRD 段落编号或原型图标注；写不出来判定为凭空新增，FAIL。
(b) 关键遗漏：PRD 中每个带有"必须"、"核心"、"默认"语义的元素必须能在 Layout Spec 的 module 列表中找到对应 module_id；找不到判定为关键遗漏，FAIL。
(c) 冲突：Layout Spec 中任何 module 的模块顺序、包含关系或存在性与 PRD 正文或 Intent 描述相反，判定为冲突，FAIL。
检查 Layout Spec 的 Frame 树是否足以按 Page Frame → Module Frame → Control Frame → Element 顺序生成 Figma 图层。
检查 Layout Spec 和 Wireframe 计划中的可见文案是否来自 PRD、PRD 原型图或已确认上游产物，不得自行改写、润色、缩写、扩写、翻译或替换。
检查组件候选是否仍为候选记录，不得在线框图阶段升级为正式组件库。
只有通过 Wireframe Preflight Gate，才能进入 Figma Wireframe 生成。

Structure Mapping Harness Check：
检查线框图 Page Frame 是否全部处理。
检查线框图是否保留 Page Frame → Module Frame → Control Frame → Element 层级：直接挂在 Page Frame 下的非 Module-Frame 节点数量必须为 0；任何 Text、Rectangle、Group 或未命名 Frame 直接作为 Page Frame 子节点，判定为散落节点，FAIL。必须在 run record 中逐一列出 Page Frame 所有直接子节点的名称和类型，以证明无散落节点，不得以"层级正常"一句带过。
检查 Priority Map 中每个 P0/P1/P2 模块是否在 Structure Mapping 中都有明确处理记录，必须在 run record 中逐一列出每个模块的映射结论，不得以"已映射"一句带过：
(a) 映射成功：必须写出采样端 Figma 来源对应节点 ID（格式 n:n）、节点字段名、sample_priority 和 sample_url；写不出节点 ID 或采样来源，判定为未明确映射，FAIL。
(b) 明确未映射：必须写出未映射原因（如"采样端无对应模块"、"新增功能无历史参考"）并说明设计决策来源；只写"无对应"或"新增"一词，判定为原因不明确，FAIL。
不得以"基本对应"、"参考旧稿"、"结构类似"等模糊表述代替具体节点 ID 或明确原因，否则判定为 FAIL。
检查 Structure Mapping 中每个 component_candidate 是否有采样端 Figma 来源结构依据，必须在 run record 中逐条列出，不得以"参考采样源"或"结构相似"一句带过：
(a) 每个 component_candidate 必须写出采样端 Figma 来源中对应节点的 ID（格式 n:n）、节点类型、sample_priority 和 sample_url；写不出节点 ID 或采样来源，判定为无结构依据，FAIL。
(b) 如采样端 Figma 来源中确无对应组件，必须明确写出"采样端无对应组件"并说明替代依据（如 Design System style_id 或 PRD 原型图标注编号）；不说明替代依据，判定为 FAIL。
检查 Structure Mapping 中每个组件候选的映射依据是否包含结构层面的共同点，不得以视觉外观相似作为唯一映射理由，必须在 run record 中逐条列出：
(a) 映射依据必须包含以下三项之一以上：相同 frame_role、相同子元素类型组成、相同业务语义；仅凭"视觉相似"、"颜色相近"、"尺寸接近"作为映射理由，判定为视觉相似误判，FAIL。
(b) 映射依据中必须写出采样端节点的 frame_role 和子元素类型，与目标 module 的 frame_role 和子元素类型进行逐项比对；缺少比对记录，判定为 FAIL。
检查 Structure Mapping 中每个映射是否确认源模块与目标模块服务同一业务功能，不得把业务语义不同的源结构映射到目标，必须在 run record 中逐条写出业务语义对比：
(a) 每个映射必须写出采样端节点的业务功能描述和目标 module 的业务功能描述；两者业务语义明显不同（如把"创作入口"映射到"翻译输入框"），判定为无关结构强行映射，FAIL。
(b) 仅继承结构规格（尺寸、间距、radius）但业务内容不同的映射不算违规，但必须明确标注"仅继承结构规格，不继承业务内容"；缺少此标注，判定为 FAIL。
检查低置信度映射是否进入 mapping-review.md。
检查 P0/P1/P2 模块已映射到采样端来源后，是否继续下钻到 Control / Element / Asset 级，必须在 run record 中逐一列出每个已映射模块的下钻结论，不得以"已映射"一句带过：
(a) 凡 P0/P1/P2 模块已映射且采样端有对应子结构，必须有 control_mappings 记录，包含采样端节点 ID、子元素类型、内部 padding、gap、关键子节点 x/y、宽高和对齐关系；缺少 control_mappings 记录，判定为 FAIL。
(b) 凡采样端存在可复用图标、图片或装饰资产节点，必须有 asset_mappings 记录，包含采样端节点 ID、节点类型、资产 URL（如可读取）、复用方式；缺少 asset_mappings 或无法写出节点 ID，判定为 FAIL。
(c) 渐变、padding、gap、关键子节点 x/y、文本与背景对齐关系均属于必须提取的可追溯数值证据；无法写出具体数值，判定为 FAIL。
(d) 如采样端确无对应子结构，必须在 mapping-review.md 中写明原因；只写"无对应"或留空，判定为 FAIL。
不得在采样端存在可复用图标资产节点时，用字符或临时图形替代；如不可复用，必须写出节点 ID 和不可复用原因，否则判定为 FAIL。

Design System Harness Check：
检查 raw-style-inventory.json 必须有顶层 items 数组，每条 item 必须有 id、source_node_id（格式 n:n）、sample_priority、sample_url、decision_level；缺少任一字段，判定为 FAIL。
检查 decision_level 只允许 component_match、priority_sampling、structure_fallback；其他值判定为 FAIL。
检查 design-system-draft.json 必须有顶层 styles 对象，每个 style_id 必须有 value 和 source_ref，source_ref 必须能在 raw-style-inventory.items.id 中找到；找不到判定为 FAIL。
检查 Structure Mapping 中已有 source_candidate 且 Priority Map 中为 P0/P1/P2 的模块，raw-style-inventory.json 必须按 source_candidate 写入 visual_audit 四态记录。主容器五项为 container.background_fill、container.gradient、container.border_stroke、container.radius、container.shadow_effects；子元素颜色按目标结构需要记录 children.text_color、children.icon_color、children.foreground_color。每项状态只能为 value、none、conflict、not_applicable；value 必须有具体值，conflict 必须有原因，缺项或四态非法判定为 FAIL。
检查 style_id 不得出现 color.primary.action、font.page.title 等含点号的全局语义 token 命名；出现判定为 FAIL。
检查 design-system-review.md 中冲突项是否以表格逐行列出：属性名 | PRD值 | 源文件值 | 暂定值 | 状态；状态字段只允许两种值：「待人工确认」或「已人工确认（附决定日期）」；AI 执行阶段写入任何其他裁定结论（如"PRD 优先"、"源文件优先"、"已确认"），判定为 AI 自行裁定，FAIL。检查 design-system-draft.json 中凡有冲突的属性，review_required 字段必须为 true；review_required 为 false 但 design-system-review.md 中该属性状态仍为「待人工确认」，判定为 FAIL。
检查是否没有把 AI 推测当成已确认规则；凡 source 字段含 "PRD 颜色规范" 且无对应 Figma 节点 ID 的颜色，判定为 AI 推测，FAIL。
检查 Structure Mapping 的 asset_mappings 中每条可复用资产节点是否在 design-system-draft.json 中有对应 asset_* 条目，包含采样端节点 ID 和资产 URL；缺少任一 asset_* 条目，判定为 FAIL。
检查 Structure Mapping 的 spacing_evidence 中每条可追溯间距数值是否在 design-system-draft.json 中有对应 spacing_* 条目；缺少任一 spacing_* 条目，判定为 FAIL。

Visual Spec Harness Check：
检查 Visual Spec 中每个模块的关键属性是否能逐条追溯到上游产物的具体值，必须在 run record 中逐条列出来源，不得以"服从上游"一句带过：
(a) 尺寸 / 间距：必须写出 Layout Spec 中对应字段名和数值；无法写出，判定为无法追溯，FAIL。
(b) 颜色：必须写出 design-system-draft.json 中对应 style_id 和十六进制值；颜色值找不到对应 style_id，判定为颜色未受 Design System 管辖，FAIL。
(c) 字体 / 字号 / 字重：必须写出 design-system-draft.json 中对应 style_id；找不到对应条目，判定为 FAIL。
(d) 圆角：必须写出 design-system-draft.json 中对应 style_id；找不到对应条目，判定为 FAIL。
(e) 模块存在性：Visual Spec 中出现的每个模块必须在 Priority Map 中有 P0/P1/P2/P3 分级记录；Priority Map 未列出的模块出现在 Visual Spec，判定为凭空新增，FAIL。
检查 Visual Spec 中 P0/P1/P2/P3 分级是否转译为可量化的视觉属性差异，必须在 run record 中逐级列出对应的视觉值，不得以"已转译为视觉层级"一句带过：
(a) P0 模块必须在以下至少两项上与 P1/P2/P3 有具体数值差异：字号（px）、字重（数值）、颜色（十六进制）、尺寸（px）；写不出具体差异数值，判定为层级未量化，FAIL。
(b) P1 模块必须在以下至少一项上与 P2/P3 有具体数值差异：字号、字重、颜色；写不出，判定为 FAIL。
(c) 不得出现两个不同优先级模块在同一属性（字号 / 字重 / 颜色）上数值相同的情况；如存在，必须写出其他属性上的区分依据，否则判定为 FAIL。
检查 Visual Spec 中是否存在 Design System 未定义的设计值，必须在 run record 中逐条列出，不得以"Design System 无法覆盖"一句带过：
(a) Visual Spec 中每个颜色值必须能在 design-system-draft.json 中找到对应 style_id；找不到时，必须写出已搜索但不存在的 style_id 和搜索路径，并标注为"待人工确认"；无法写出搜索记录，判定为 FAIL。
(b) Visual Spec 中每个圆角值、字号、字重必须能在 design-system-draft.json 中找到对应 style_id；找不到时，必须写出搜索记录和"待人工确认"标注；无法写出搜索记录，判定为 FAIL。
(c) 凡标注"待人工确认"的条目必须在 design-system-review.md 中有对应行记录；缺少对应行，判定为 FAIL。
检查 Visual Spec 中引用的每个 style_id（格式 `style_id: xxx`）是否存在于 design-system-draft.json.styles；找不到判定为 FAIL。
检查 Visual Spec 中每个 Tab、按钮、输入字段、状态、模块和交互控件是否均有 Priority Map 条目对应，必须在 run record 中逐一列出对应关系，不得以"未发现额外控件"一句带过：
(a) Visual Spec 中每个交互控件或功能模块必须能写出 Priority Map 中对应的模块名和优先级（P0–P3）；写不出对应 Priority Map 条目，判定为凭空新增，FAIL。
(b) 不得以"视觉需要"或"样式参考"为由在 Visual Spec 中写入 Priority Map 未列出的 Tab、按钮、状态或交互入口；如存在，判定为 FAIL。
检查 Structure Mapping 中已有 source_candidate 的 P0/P1/P2 模块或控件是否被 Visual Spec 自动处理，必须在 run record 中逐条列出，不得等待人工点名具体节点：
(a) 凡 Structure Mapping 中 mapping_type 为 component_inheritance 或 frame_level_inference，且目标模块 / 控件优先级为 P0/P1/P2，Visual Spec 必须列出 source_candidate，并逐项说明背景、描边、圆角、阴影、内边距、尺寸比例、字号层级、颜色层级和视觉权重的继承 / 不继承结论；缺少任一项，判定为 FAIL。
(b) 若 Visual Spec 不继承 source_candidate 的某项视觉属性，必须写出具体冲突来源（PRD 原文 / Wireframe 结构 / 人工确认记录 / Design System 冲突项）、影响范围和采用的替代 style_id；只写"不适用"、"按 PRD"、"仅参考结构"、"样式兜底"，判定为原因不充分，FAIL。
(c) 对 P0/P1 模块，若 source_candidate 存在且不继承其背景、描边、圆角、阴影中的任一核心容器视觉属性，必须有人工确认记录或 design-system-review.md 中的冲突表记录；否则判定为执行偏差，FAIL。

Hi-Fi Generation Harness Check：
检查高保真稿是否覆盖 Visual Spec，必须在 run record 中逐一列出 Visual Spec 定义的每个模块及其在 Hi-Fi 中的对应图层名，不得以"已覆盖"一句带过：
(a) Visual Spec 中每个模块必须在 Hi-Fi 中有同名或注释说明等价名的 Frame；缺少任一模块 Frame，判定为覆盖不完整，FAIL。
(b) Visual Spec 中每个模块的关键尺寸属性（width、height、padding）必须能在 Hi-Fi 对应 Frame 中写出具体 Figma 属性值作为证据；写不出具体值，判定为无证据，FAIL。
检查 Page Frame 是否保持 360 x 780。
检查高保真稿是否完整继承线框图已有可见文案，不得改写、润色、缩写、扩写、翻译或替换。
检查 Hi-Fi 是否处于可编辑状态，必须逐项验证，不得以"可继续编辑"一句带过：
(a) Hi-Fi 中不得存在 isLocked=true 的图层；如存在，必须列出图层名，判定为 FAIL。
(b) 文本图层必须是 TEXT 类型，不得是 VECTOR 或 BOOLEAN_OPERATION；如存在被栅格化的文本图层，必须列出图层名，判定为 FAIL。
(c) 所有 Frame、Group 的命名必须符合 Layer Naming 规范（英文 snake_case，有业务语义，无默认 Figma 名称）；不符合规范的图层名，判定为 FAIL（此项与 Layer Naming Gate 结论联动）。
检查 Hi-Fi 是否临场改写了业务结构或设计规则，以下任一条件触发 FAIL，必须逐项列出比对结论，不得以"未发现改写"一句带过：
(a) Hi-Fi 中 Page Frame 直接子 Frame 数量 ≠ Wireframe 中 Page Frame 直接子 Frame 数量。
(b) Hi-Fi 中任一模块的可见文案与 PRD 原文逐字不符（改写、缩写、润色、扩写均算）。
(c) Hi-Fi 中出现 Visual Spec 未定义的颜色值（十六进制）。
(d) Hi-Fi 中出现 Visual Spec 或 design-system-draft.json 未定义的圆角值。
检查 run record 或 Visual Spec 中必须记录颜色值到 style_id 到 source_ref 的追溯链；无追溯记录判定为 FAIL。
检查是否没有因视觉采样新增线框图或 Visual Spec 未定义的内容模块、Tab、按钮、字段、状态或交互控件。
检查是否没有把采样稿、旧界面或采样端 Figma 来源页面整体复制、整体移植或整体替换到当前设计稿；如存在，判定为严重生成偏差，不得通过。
检查是否没有因视觉采样改写目标稿已有文案、功能架构、业务状态或交互语义；视觉采样只能改设计规范，不能改业务内容。
如存在按钮、Tab、选择器、输入框、卡片、列表等组件形态或内部结构的等价视觉表达替换，检查业务对象、触发动作、可选项含义、选项数量、默认选中 / 激活 / 禁用状态语义、输入字段数据含义和必要入口是否保留，是否未新增业务入口、未删减目标稿已有功能、未迁移采样稿文案。
检查 Hi-Fi 中采样源资产（图片、图标、插画、装饰）的复用情况，必须在 run record 中以表格形式逐行列出 Design System asset_mappings 中每一条资产的处理结果，不得以"已优先复用"或"已处理"一句带过：
(a) 凡采样端 Figma 来源中有明确节点 ID（格式 n:n）且类型为 IMAGE 或 VECTOR 的资产，run record 必须以如下格式逐行记录：「采样端节点 ID | Hi-Fi 节点 ID | 复用方式（imageHash 复制 / clone / 直接引用）| 验证方式（读取 Hi-Fi 节点 fills.imageHash 或 type=IMAGE/VECTOR）」；缺少任一列，判定为 FAIL。
(b) 凡 Design System asset_mappings 中 type=IMAGE 的资产，必须在 run record 中写出 Hi-Fi 对应节点的 fills[0].type 实际值；fills[0].type ≠ IMAGE，判定为资产未复用，FAIL。
(c) 凡 Design System asset_mappings 中 type=VECTOR 或 VECTOR_COMPOSITE 的资产，必须在 run record 中写出 Hi-Fi 对应节点的 type 实际值；type = TEXT 或 RECTANGLE 且无 IMAGE fill，判定为字符/形状占位代替了图标资产，FAIL；无法写出 Hi-Fi 节点 ID，同样判定为 FAIL。
(d) 凡用字符（如 v、▼、●、+、×、📎 等）代替图标资产的节点，必须在 run record 中逐行写出「节点 ID | 字符内容 | 采样端对应资产节点 ID | 不可复用原因」；无法写出采样端节点 ID 和不可复用原因，判定为 FAIL。
(e) 如采样端 Figma 来源中无对应资产节点，必须明确写出"采样端无对应资产"并说明占位类型；无说明，判定为 FAIL。
检查渐变样式是否同时匹配 gradientStops 和 gradientTransform，且没有使用默认渐变方向替代采样源方向。必须在 run record 中以如下格式逐行列出页面内每一个渐变节点的验证结果：「Hi-Fi 节点 ID | fills[0].type 实际值 | gradientStops 数值（每个 stop 的 color 十六进制 + position）| gradientTransform 数值 | 采样端来源节点 ID」；fills[0].type = SOLID 但 Visual Spec 要求为渐变，判定为渐变未应用，FAIL；gradientStops 或 gradientTransform 与采样端不一致且无人工确认记录，判定为 FAIL；无法写出上述任一字段的具体数值，判定为 FAIL。
检查 Hi-Fi 中装饰性资产（背景图、插画、渐变色块、装饰线）的图层归属和 Z 轴顺序，必须逐条列出，不得以"归属正确"一句带过：
(a) 每个装饰性资产必须作为子图层位于其装饰目标的业务 Frame 内部（即与装饰目标同一 Module Frame 下），不得直接挂在 Page Frame 下或位于其他业务模块的 Frame 内；违反，判定为归属错误，FAIL。
(b) 每个装饰性资产在其父 Frame 内的 Z 轴顺序必须低于（即在图层列表中排列于下方）同 Frame 内的主要内容图层；违反，判定为层叠顺序错误，FAIL。
检查用于计算间距的 Module Frame 是否收紧到有效子元素外接边界，主模块间距是否按真实边界一致计算。
检查复用组件是否符合组件复用通用原则，必须在 run record 中覆盖本次 Hi-Fi 生成涉及的所有复用组件，不得抽样，每个组件逐项列出以下结论：
(a) 内部边距：是否来自采样端实际值，不得估算；无采样来源判定为 FAIL。
(b) 内部元素间距：是否来自采样端子节点实际坐标的间距关系，容器尺寸不同时是否已重新计算；直接照抄采样端绝对坐标值且容器尺寸不同，判定为 FAIL。
(c) 容器尺寸：标签、胶囊、按钮、Tab 等小控件是否跟随内容实际尺寸计算；一级容器、输入框是否保持不可变；小控件尺寸固定为采样端尺寸而未跟随内容，判定为 FAIL。
(d) 文字节点：Auto Layout 容器内的文字节点必须同时满足：textAutoResize = WIDTH_AND_HEIGHT（高度自适应内容）且 layoutSizingHorizontal = FILL（横向撑满父级）；任一缺失且无充分理由，判定为 FAIL。placeholder、example、guidance 类节点同样适用此双重约束，不接受"父级容器固定高度"或"输入框场景"作为豁免理由。
(e) 图标节点：是否优先复用资产；不可复用时是否写出原因并保留独立语义节点；无不可复用原因说明，判定为 FAIL。
(f) 设计规范：颜色、圆角、描边、投影是否来自采样端或 design-system-draft.json；临场自造数值且无来源，判定为 FAIL。
(g) 内部元素无重叠：同行子节点之间左右边界不得交叉；存在重叠，判定为 FAIL。
检查 Hi-Fi 中所有 TEXT 节点的 `textAutoResize` 和 `layoutSizingHorizontal` 属性，必须在 run record 中列出业务文案节点（标题、字段名、字段值、按钮文案、导航文字、辅助说明，以及 placeholder、example、guidance 类节点）的两项属性实际值。以下任一情况判定为 FAIL：(1) `textAutoResize = 'NONE'`（固定高度）且无充分理由；(2) `layoutSizingHorizontal = FIXED`（固定宽度）且无充分理由。充分理由只限于：有明确截断需求的场景（如固定行数截断）或有明确固定宽度语义的控件（如参数胶囊内文字），且必须写明目的和不裁切文字的证据。不接受"父级容器固定高度"或"输入框场景"作为豁免理由。
检查 Hi-Fi 中通过 Plugin API 新建的 TEXT 节点字体是否来自采样端：必须在 run record 中逐行写出「节点 ID | 节点名称 | fontFamily | fontStyle | 采样端来源节点 ID | 采样端 fontFamily | fontStyle | 是否一致」；无法写出采样端来源节点 ID，判定为字体硬编码，FAIL；fontStyle 与采样端不一致且无人工确认记录，判定为 FAIL。
检查字段名、字段值、单位 / 状态和操作图标是否在语义需要时拆成独立节点，且未为已取消交互的字段添加箭头或其他交互暗示；字段名和字段值即便视觉样式相同也必须分别对应独立图层，例如 `画风` 与 `二次元` 必须分开。如出现 `画风[二次元▼]`、`字幕[自动开 ●]`、`时长60秒▼` 这类把属性类型、属性内容和图标合并到同一文本层的结构，判定为 FAIL。即便图标暂时用字符表达，也必须保留独立的 icon / action_icon 语义节点和命名。
如页面存在被判定为悬浮、贴底、贴顶、fixed、sticky 或 overlay 显示的模块或组件，检查该节点是否位于当前页面状态的 Z 轴最上层，且未被普通内容模块、背景层、保护层或装饰层覆盖；违反判定为 FAIL。
如页面存在固定底部 CTA，检查 CTA 是否以 Page Frame 底部为基准保持 24px 下边距、是否位于 Z 轴最上层、是否有 90px 底部保护背景层，且关键内容未被 CTA 覆盖。
如用户提供【采样源】截图和【设计图】截图，检查是否已执行截图视觉对比审核，并输出对比结论、偏差清单、修改建议、偏差归因和是否需要重跑。

Layer Naming Harness Gate：
检查目标范围内 frame-like 节点是否不存在默认 Figma 名称，例如 Frame 1、Group 1、Rectangle 8、Text 12。
检查目标范围内 frame-like 节点是否不存在中文命名、无上下文 label、无交付意义 source_ 前缀和纯位置词命名。
检查命名是否统一使用英文 snake_case，并表达业务语义或结构职责。
检查重复项数字尾缀是否只用于真实重复项或资产序列，不用于临时占位。
检查命名调整是否只改变 name，不改变视觉、布局、层级、样式、文字内容或业务语义。
检查命名扫描结果、剩余问题和人工确认点是否写入 run record。
只有 Layer Naming Harness Gate 通过，才允许进入 Auto Layout 回填；如未通过，必须先回到命名规范化流程修正后重新检查。

Auto Layout Harness Gate：
检查 Auto Layout 回填是否保持原静态稿视觉位置、尺寸、间距、字体、图片、图标、装饰和业务层级不变。
检查是否没有为了 Auto Layout 新增未经确认的 wrapper、container、spacer、padding frame 或 hidden bucket。
检查复杂结构是否允许保留普通 Frame，并通过 constraints 表达响应关系。
检查目标树中所有预期为 Auto Layout 的 FRAME 节点 layoutMode 是否为 HORIZONTAL 或 VERTICAL；layoutMode=NONE 视为未生效，判定为 FAIL。
检查目标树中是否不存在由 Auto Layout 流程新建、复制、迁移或隐藏后遗留的临时隐藏图层；如存在，必须删除，残留判定为 FAIL。
检查目标树是否不存在未经用户明确允许的 layoutPositioning=ABSOLUTE。
检查背景、整屏视口、安全内容区、横滑列表、固定底部 CTA 和页面级浮层是否符合对应宽度、约束和层级规则。
检查所有内容模块（创作主卡、参数区、灵感列表等）是否为全宽（x=0，width=Page Frame 宽度），constraints=STRETCH；若模块自身 width 被缩窄为 Page Frame 宽度减去边距的值（如 w=328 而非 w=360），判定为 FAIL。
检查带有视觉背景属性（fill、stroke、cornerRadius、shadow）的 Module 是否同时设置了 padding：若背景属性与 padding 同时存在于同一 Module 节点上，判定为结构错误，FAIL；必须拆分为 Module（全宽无背景无 padding）+ inner_wrapper（承载背景和 padding）结构。
检查 Module 内横向撑满的子节点（输入框、按钮、卡片内容区等）是否设置了 layoutSizingHorizontal=FILL；固定宽度子节点必须在 run record 中说明原因；无说明且宽度固定，判定为 FAIL。
检查固定底部 CTA：
(a) x=0，width=Page Frame 宽度，constraints horizontal=STRETCH，vertical=MAX；任一不符，判定为 FAIL。
(b) bottom offset = Page Frame 高度 - CTA y - CTA 高度，必须等于 0（或设计规定值）；偏移超过 1px，判定为 FAIL。
(c) 固定底部 CTA 必须是 Page Frame 的最后一个子节点（Z 轴最上层）；不是最后一个子节点，判定为 FAIL。
检查是否已自动执行 metadata、screenshot 和必要的临时拉伸副本校验，且测试后删除临时副本。
拉伸响应校验（独立于视觉不变性校验）：将 Page Frame 宽度临时拉伸至 540px，截图确认所有 layoutSizingHorizontal=FILL 的子节点（文字节点、输入框、卡片内容区等）宽度同步变化；若任一预期 FILL 节点宽度未变化，判定 FAIL，run record 中列出不跟随变化的节点 ID。校验完成后恢复原宽度。
检查本次新增或修改的规则、记录、页面文件和交付说明是否不存在本机绝对路径。
检查冲突、例外、放弃项、人工确认点、流程临时隐藏图层扫描结果、absolute positioning 扫描结果和本机绝对路径扫描结果是否写入 run record。
只有 Auto Layout Harness Gate 通过，才允许进入交付；如未通过，必须回到 Auto Layout 制作流程定位原因、修正后重新检查。

Backfill Harness Check：
检查 Backfill 中每条人工审核结论是否已明确标注归属范围，必须在 run record 中逐条列出，不得以"已区分"一句带过：
(a) 单页修正：结论必须标注 scope=single_page，只写入 workspace/records/run_xxx.md，不得写入 workspace/design_system/ 或 rules/；如写入上述文件，判定为范围错误，FAIL。
(b) 项目级设计系统结论：结论必须标注 scope=project，只写入 workspace/design_system/，不得写入 rules/；如写入 rules/，判定为范围错误，FAIL。
(c) 跨项目通用规则：结论必须标注 scope=cross_project 且写出可复用的业务场景描述；无业务场景描述，判定为 FAIL。
检查项目内同类页面可复用但尚不适合进入跨项目 rules/ 的高保真手动调整，是否进入 workspace/design_system/manual-hifi-adjustment-rules.md。
检查写入 design system 或 rules/ 的每条结论是否满足稳定性和可复用性要求，必须在 run record 中逐条列出依据，不得以"稳定且可复用"一句带过：
(a) 稳定性：写入 design system 或 rules/ 的结论必须有人工确认记录（run record 中需含人工裁定日期和决定描述）；无人工确认记录，判定为未经确认，不得写入，FAIL。
(b) 可复用性：写入 rules/ 的结论必须写出适用的业务场景范围（如"适用于所有移动端翻译类页面"）；仅描述当前页面具体事实（如"翻译首页 CTA 按钮高度为 44px"），判定为不可复用，不得写入 rules/，FAIL。
检查回填是否记录来源、影响范围和是否需要重跑。
如存在截图视觉对比偏差，检查每条偏差是否有可核查的归因依据，必须在 run record 中逐条列出，不得以"偏差已归因"一句带过：
(a) 单页修正：必须写出"此偏差只影响当前页面，其他同类页面无相同问题"；无此声明，不得归类为单页修正，FAIL。
(b) 设计系统缺口：必须写出 Design System 中缺少的具体 style_id（如缺少 radius_button_large）；写不出 style_id，不得归类为设计系统缺口，FAIL。
(c) Visual Spec 表达不足：必须写出 Visual Spec 中缺失或描述不清的具体字段名和缺失内容；写不出字段名，不得归类为 Visual Spec 表达不足，FAIL。
(d) 生成执行偏差：必须写出 Hi-Fi 生成中具体哪步操作与 Visual Spec 不符（如"translate_go_button 高度写为 40px，Visual Spec 定义为 44px"）；写不出具体偏差位置，不得归类为生成执行偏差，FAIL。
不得把单张截图事实（如"按钮颜色偏红"）直接写入 rules/；只有经人工确认且跨项目适用的归因结论才能进入 rules/；违反，判定为 FAIL。
```

## 冲突处理

```text
发现 PRD 与下游产物冲突时，以 PRD 为准，先停止进入下一步。
发现 Intent、Priority Map、Layout Spec、Wireframe、Structure Mapping、Design System 或 Visual Spec 之间冲突时，先指出冲突位置和影响范围。
发现 PRD 有歧义时，不自行补业务结论；在产物或记录中标注待人工确认。
发现遗漏时，优先回补对应上游产物，再继续下游生成。
```

## 变更记录

```text
Wireframe、Structure Mapping、Design System、Visual Spec、Hi-Fi Generation 和 Backfill 后的任何结构、内容、状态、层级、样式或规则改动，必须写入 workspace/records/run_xxx.md。
记录必须包含：变更对象、变更前、变更后、变更原因、依据来源、是否影响上游文件、是否沉淀为通用规则。
Wireframe 生成后必须检查图层树是否存在大量散落 Text、Rectangle、Frame 1、Group 1 或直接挂在 Page Frame 下的非页面级元素。
如果图层树不符合 Page Frame → Module Frame → Control Frame → Element，必须先整理；无法整理时记录为失败，不得视为通过。
只有跨项目可复用的判断方法才能进入 rules/。
单个项目的页面事实、业务文案、模块位置和临时调整不得进入 rules/。
```

## 重跑策略

```text
重跑同一项目或同一页面时，默认覆盖当前页面的 Intent、Priority Map、Layout Spec、Structure Mapping、Design System 草案和 Visual Spec。
重跑 Wireframe 时，默认覆盖 workspace/figma_targets.md 中 Figma 内部图层名称对应的线框图内容。
重跑 Hi-Fi 时，默认覆盖目标高保真页面范围；只有用户明确要求保留旧版时，才新建副本或追加版本。
重跑或修正 Hi-Fi 时，覆盖范围只能是当前目标页面的高保真结果，不得用采样稿、旧界面或采样端 Figma 来源页面整体替换目标页面结构。
run record 不得覆盖；每次执行必须新增 workspace/records/run_xxx.md。
如果用户明确要求保留旧版线框图，才在 Figma 中新建副本或追加版本。
```
