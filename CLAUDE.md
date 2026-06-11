# CLAUDE.md — PRD to Figma Design Demo

## 强制前置规则（每次操作前必读）

在对本项目执行任何 Figma 操作、结构修改、命名变更、节点创建之前，必须先读取对应规则文件：

| 操作类型 | 必读规则文件 |
|---|---|
| Figma Wireframe 创建、修改、重构 | `rules/wireframe_rules.md` 和 `rules/structure_preparation_rules.md` |
| Auto Layout 操作 | `rules/autolayout_rules.md` |
| 高保真设计生成 | `rules/hifi_generation_rules.md` 和 `rules/design_system_rules.md` |
| 高保真审核与回填 | `rules/hifi_review_rules.md` |
| 设计系统提取 | `rules/design_system_rules.md` |
| Visual Spec 生成 | `rules/visual_spec_rules.md` |
| 结构映射 | `rules/structure_mapping_rules.md` |
| Layout Spec 生成 | `rules/layout_spec_rules.md` |
| Intent 生成 | `rules/intent_rules.md` |
| Priority Map 生成 | `rules/priority_rules.md` |
| Harness Gate 执行 | `rules/harness_rules.md` |

不得凭经验或记忆直接行动，必须以规则文件为准。

## 高保真生成强制前置输出（三层执行机制）

执行任何高保真 Figma 写操作前，必须完成以下三层机制，缺一不可：

### 第一层：执行前输出复用判断表（等待人工确认后才能动 Figma）

每个模块必须输出以下表格行：

| 模块 | source_candidate ID + 路径 | 复用级别 | 规则原文引用（≤2句）| 支撑结论 | 执行方式 |
|------|--------------------------|---------|-------------------|---------|---------|

**source_candidate 列格式要求：**
- 必须同时提供 ID 和 Figma 文件路径，格式：`节点ID（文件名 / 页面名 / Section名 / Frame名）`
- 示例：`437:7602（Demo / 源文件 / 同界面 / module_prompt_input_card）`
- 禁止只写 ID，不写路径

**规则原文引用格式要求：**
- 只引用直接支撑复用级别判断的那一句，不超过 2 句
- 引用后加括号注明：`（支撑结论：Level X，因为……）`
- 禁止引用大段原文稀释关键判断

示例：
| main_card | 437:7602 | Level 2 | "不得把 Level 1/Level 2 的 source_candidate 仅当作 token 参考后手工重绘" | （支撑结论：Level 2，因为采样源节点可访问，需 import 后修改文案） | import节点后修改文案和颜色 |

**输出判断表后，必须停止，发送以下消息等待用户回复：**
「复用判断表已输出，请确认后回复"confirm"继续执行。」
收到"confirm"之前，禁止调用任何 Figma 工具。

### 第二层：人工抽查 P0 模块

P0 模块（如主卡）的规则原文引用，人工需验证：引用的原文是否真实存在、是否真的支撑该复用级别结论。

### 第三层：每模块执行后截图确认

每个模块叠加视觉属性后必须截图，确认执行结果与复用判断表一致，再进行下一个模块。

## 项目结构

```
rules/          各阶段规则文件（操作前必读）
execution/      各阶段执行指令
scripts/        harness_check.py 等工具脚本
workspace/
  PRD/          输入 PRD
  intents/      Intent 产物
  priority_maps/  Priority Map 产物
  layout_specs/   Layout Spec 产物
  structure_mapping/  结构映射产物
  design_system/  设计系统产物
  visual_specs/   Visual Spec 产物
  records/        执行记录
  harness/        Gate 结果
  figma_targets.md  Figma 文件链接
```

## Figma 文件

采样端与输出端配置均以 `workspace/figma_targets.md` 为准。

## 命名系统（wireframe_rules.md 摘要）

以下为核心规定，完整规定以 `rules/wireframe_rules.md` 为准：

- Page Frame：`[nn]_[page_name]_state_[state_value]`
- Module Frame：`module_[module_id]`
- Control Frame：`control_[control_id]` 或语义控件名（如 `xxx_tabs`、`xxx_button`）
- Element：`[element_type]_[semantic_name]`
- Tab 控件结构：`xxx_tabs` > `selected_tab_label` / `unselected_tab_label` / `selected_indicator`
- 全部使用英文 snake_case，禁止中文命名、无语义数字尾缀、位置词

## 禁止行为

- 禁止凭经验推断节点结构，必须以规则文件为准
- 禁止自行创造规则文件中未定义的层级或命名
- 禁止在未读对应规则文件的情况下执行任何 Figma 写入操作
- 禁止对 PRD 文案进行创意改写或补全

## Harness

- 执行命令：`python scripts/harness_check.py --run-id <run_id> --gate <gate_name>`
- Gate 顺序：intent → priority → layout → wireframe_preflight → wireframe_color_check → structure_mapping → design_system → visual_spec → hifi_generation → backfill → layer_naming → auto_layout → layer_naming_recheck
- 每个 Gate 必须实际运行 `harness_check.py`，不得用"目测通过"代替
- Gate 结果必须有对应 `.json` 文件落盘，无文件视为未执行
- **注意**：当前 Harness 不检查 Figma 节点实体结构，仅检查文档完整性。Figma 层级、命名和结构正确性须人工或操作前规则阅读保障。

## 语言

所有回复使用中文。
