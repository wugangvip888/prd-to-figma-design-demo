# 文件索引 / File Index

本文件记录 `prd-to-figma-design` 的目录职责、核心文件用途、生成方式和维护流程。

本项目以 `AI_Design_System/docs/file_index.md` 为结构样例，当前已包含 PRD 到线框图、结构映射、设计系统提取、Visual Spec 和高保真生成流程资产。

## 目录索引

| 路径 | 中文名称 | 作用 | 当前状态 |
|---|---|---|---|
| README.md | 项目入口说明 | 说明项目目标、流程边界、快速开始方式 | 已建立 |
| docs/ | 项目说明层 | 存放文件索引、文件结构、工作流、流程治理规则和自检清单 | 已建立 |
| scripts/ | 脚本层 | 存放 Harness 检查、Figma Auto Layout / 几何机器检测、占位图片获取和 workspace 生成产物清理脚本 | 已建立 |
| prompts/ | Prompt 层 | 存放全流程入口 Prompt 和 01-11 分步执行 Prompt | 已建立 |
| rules/ | 规则层 | 存放 Intent、Priority Map、Layout Spec、Wireframe、Structure Mapping、Design System、Visual Spec、Hi-Fi 和 Harness 的判断规则 | 已建立 |
| execution/ | 执行层 | 记录每一步怎么执行、输入输出和审核点 | 已建立 |
| workspace/ | 当前项目工作区 | 存放当前项目 PRD、生成结果和运行记录 | 已建立 |
| workspace/PRD/ | PRD 输入目录 | 存放当前项目原始 PRD | 已建立 |
| workspace/figma_targets.md | Figma 目标登记 | 存放当前项目采样端 Figma 链接优先级列表、线框图输出端、高保真输出端和设计层输出端的 Figma 文件链接与 Page 名称；输出端 pageID 可选 | 已建立 |
| workspace/intents/ | Intent 输出目录 | 每个页面一个 Intent 文件 | 已建立，可用清理脚本重置 |
| workspace/priority_maps/ | 元素权重排序目录 | 每个页面一个 Priority Map 文件 | 已建立，可用清理脚本重置 |
| workspace/layout_specs/ | Layout Spec 输出目录 | 每个页面一个 Layout Spec 文件 | 已建立，可用清理脚本重置 |
| workspace/structure_mapping/ | 结构映射输出目录 | 存放 Wireframe 与采样端 Figma 来源的结构映射、组件候选索引和审核清单 | 已建立，可用清理脚本重置 |
| workspace/design_system/ | 设计系统输出目录 | 存放采样端 Figma 来源真实样式清单、设计系统草案和人工审核清单 | 已建立，可用清理脚本重置 |
| workspace/visual_specs/ | 高保真设计指令目录 | 每个页面一个 Visual Spec 文件 | 已建立，可用清理脚本重置 |
| workspace/records/ | 运行记录目录 | 记录每次执行输入、范围、输出和人工确认 | 已建立，可用清理脚本重置 |
| workspace/archive/ | 归档目录 | 存放重跑前移出的旧 workspace 阶段产物 | 已建立 |
| workspace/archive/{run_id}/ | 重跑前旧产物归档 | 按需归档旧 Intent、Priority Map、Layout Spec、Structure Mapping、Design System 和 Visual Spec | 按需建立 |
| workspace/harness/ | Harness Gate 结果目录 | 存放每次运行的 Gate JSON 结果文件（`{run_id}_{gate}_gate.json`） | 已建立，Gate JSON 可用清理脚本重置 |
| workspace/figma_scripts/ | Figma 脚本暂存目录 | 存放临时性 Figma Plugin 脚本或调试脚本；当前为空，按需放入 | 已建立，当前为空 |

## 文件索引

### Docs

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| file_index.md | 文件索引 | docs/ | 记录目录职责、核心文件用途和维护方式 | 人工维护 | 文档治理 |
| file_structure.md | 当前文件架构 | docs/ | 记录当前真实存在的目录和核心文件结构 | 人工维护 | 文档治理 |
| workflow.md | 工作流说明 | docs/ | 记录 PRD → Intent → Priority Map → Layout Spec → Wireframe → Structure Mapping → Design System → Visual Spec → Hi-Fi → Design Layer → Backfill → Layer Naming → Auto Layout 的端到端流程顺序和 Harness Gate | 人工维护 | 文档治理 |
| process_rules.md | 流程治理规则 | docs/ | 定义 prompts、execution、rules、records、docs 的职责边界和读取顺序 | 人工维护 | 文档治理 |
| self_check.md | 自检清单 | docs/ | 定义结构、引用、流程、Wireframe / Hi-Fi 尺寸、重跑策略和断点续跑的健康检查项 | 人工维护 | 文档治理 |
| harness-backlog.md | Harness 待补强检查能力待办清单 | docs/ | 记录后续需要补强的 Harness 检查能力；当前作为待办清单，不影响现有 gate，不随产物重跑清理 | 人工维护 | Harness Gate |

### Scripts

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| harness_check.py | Harness 检查脚本 | scripts/ | 生成 machine-owned Harness Gate JSON 和 gate summary | 人工维护 | Harness Gate |
| fetch_placeholder_image_v3.py | 占位图片获取脚本 | scripts/ | 根据关键词获取可用于 Figma 图片填充的占位图片 URL | 人工维护 | Hi-Fi Generation |
| figma_autolayout_check.py | Figma Auto Layout Harness Gate 机器检测脚本 | scripts/ | 机械检测设计层 page_frame 内所有节点是否已正确设置 Auto Layout，输出 auto_layout gate JSON | 人工维护 | Auto Layout Harness Gate |
| figma_geometry_check.py | Figma 高保真几何 Harness Gate 检测脚本 | scripts/ | 校验高保真 Frame 几何属性（尺寸、位置）是否符合 Visual Spec 规格，输出 hifi_geometry gate JSON | 人工维护 | Hi-Fi Generation Harness Gate |
| clean_workspace_outputs.py | workspace 生成产物清理脚本 | scripts/ | 清理上一轮生成产物，保留 PRD、Figma 目标、规则、提示词、脚本、archive、.gitkeep 和 docs/harness-backlog.md；默认 dry-run，`--apply` 才删除 | 人工维护 | 重跑准备 |

### Prompts

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| 00_run_full_pipeline.md | 全流程执行提示词 | prompts/ | 指导 AI 从 PRD 自动执行到设计层交付完成，并写入 Run Record；中间 Wireframe、Hi-Fi 和设计层不等待人工验收 | 人工维护 | 端到端全流程 |
| 01_prd_to_intent.md | PRD 到 Intent 提示词 | prompts/ | 指导 AI 从 PRD 生成页面 Intent | 人工维护 | Flow 01 |
| 02_intent_to_priority_map.md | Intent 到元素权重排序提示词 | prompts/ | 指导 AI 同时参考 PRD 和 Intent 生成 P0/P1/P2/P3 页面元素权重排序 | 人工维护 | Flow 02 |
| 03_priority_map_to_layout_spec.md | 权重排序到 Layout Spec 提示词 | prompts/ | 指导 AI 同时参考 PRD、Intent 和 Priority Map 转成 Layout Spec | 人工维护 | Flow 03 |
| 04_layout_spec_to_wireframe.md | Layout Spec 到线框图提示词 | prompts/ | 指导 AI 先执行 Wireframe Preflight，再根据 PRD、Intent、Priority Map 和 Layout Spec 在 Figma 生成线框图 Frame | 人工维护 | Flow 04 |
| 05_structure_mapping.md | 结构映射提示词 | prompts/ | 指导 AI 将 Wireframe 与采样端 Figma 来源建立结构映射 | 人工维护 | Flow 05 |
| 06_design_system_extraction.md | 设计系统提取提示词 | prompts/ | 指导 AI 从采样端 Figma 来源和结构映射中提取设计系统草案 | 人工维护 | Flow 06 |
| 07_visual_spec.md | 高保真设计指令提示词 | prompts/ | 指导 AI 生成每个页面的高保真设计指令 | 人工维护 | Flow 07 |
| 08_hifi_generation.md | 高保真生成提示词 | prompts/ | 指导 AI 根据 Visual Spec 在 Figma 中生成高保真设计稿 | 人工维护 | Flow 08 |
| 09_hifi_review_backfill.md | 高保真回填与设计层发布提示词 | prompts/ | 指导 AI 基于高保真 Harness 结果自动回填稳定设计系统结论并发布设计层 | 人工维护 | Flow 09 |
| 10_layer_naming_normalization.md | 图层命名规范化提示词 | prompts/ | 指导 AI 执行 Frame / 图层命名规范化，并通过 Layer Naming Harness Gate 放行 | 人工维护 | Hi-Fi Harness / 命名治理 |
| 11_autolayout_backfill.md | Auto Layout 回填提示词 | prompts/ | 指导 AI 为已有高保真静态稿补 Auto Layout，并通过 Auto Layout Harness Gate 和 Layer Naming Harness Recheck 放行 | 人工维护 | Hi-Fi Harness / Auto Layout 治理 |

### Rules

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| intent_rules.md | Intent 规则 | rules/ | 定义 Intent 固定字段、写作规则和 PRD 强约束提取方式 | 人工维护 | Flow 01 |
| autolayout_rules.md | Auto Layout 补齐规则 | rules/ | 定义为已有高保真静态稿补 Auto Layout 时的元素保护、字体保护、静态位置保持、冲突处理和落盘边界 | 人工维护 | Flow 08 / Hi-Fi 手动调整 |
| priority_rules.md | 页面元素权重排序规则 | rules/ | 定义 P0/P1/P2/P3 分级、判断规则和输出格式 | 人工维护 | Flow 02 |
| layout_spec_rules.md | Layout Spec 规则 | rules/ | 定义 Layout Spec 模块格式、模块边界、描述规则和自检规则 | 人工维护 | Flow 03 |
| wireframe_rules.md | 线框图规则 | rules/ | 定义 Frame 输出单位、Page Frame 尺寸、页面排布、层级结构、P0/P1/P2/P3 表达和禁止事项 | 人工维护 | Flow 04 |
| structure_preparation_rules.md | 结构预备规则 | rules/ | 定义线框图如何为后续组件候选、样式采样和 Pattern 归纳保留结构边界 | 人工维护 | Flow 04 / Flow 05 |
| structure_mapping_rules.md | 结构映射规则 | rules/ | 定义 Wireframe 与采样端 Figma 来源之间的结构映射规则 | 人工维护 | Flow 05 |
| design_system_rules.md | 设计系统提取规则 | rules/ | 定义 raw style inventory、design system draft 和 review 的分层提取规则 | 人工维护 | Flow 06 |
| visual_spec_rules.md | 高保真设计指令规则 | rules/ | 定义 Visual Spec 如何同时服从业务结构和设计系统 | 人工维护 | Flow 07 |
| hifi_generation_rules.md | 高保真生成规则 | rules/ | 定义 Figma 高保真设计稿生成规则 | 人工维护 | Flow 08 |
| hifi_review_rules.md | 高保真审核回填规则 | rules/ | 定义人工审核和设计系统回填规则 | 人工维护 | Flow 09 |
| harness_rules.md | Harness 校验规则 | rules/ | 定义分步 Gate、Wireframe Preflight、冲突处理和变更沉淀规则 | 人工维护 | 全流程 |
| （项目级规则子目录） | 项目级规则 | rules/project/ | 存放特定项目的专属规则文件，不跨项目复用 | 人工维护 | 项目级治理 |
| 360_zhixiao.md | 360 智效项目规则 | rules/project/ | 360 智效项目专属规则占位文件 | 人工维护 | 项目级治理 |

### Execution

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| 00_run_full_pipeline.md | 全流程执行文档 | execution/ | 定义从 PRD 到设计层交付完成的端到端自动编排、Gate、停止条件和断点续跑 | 人工维护 | 端到端全流程 |
| 01_prd_to_intent.md | PRD 到 Intent 执行文档 | execution/ | 定义从 PRD 生成 Intent 的输入、输出、步骤和自检 | 人工维护 | Flow 01 |
| 02_intent_to_priority_map.md | Intent 到权重排序执行文档 | execution/ | 定义生成 Priority Map 的输入、输出、步骤和 Priority Gate | 人工维护 | Flow 02 |
| 03_priority_map_to_layout_spec.md | 权重排序到 Layout Spec 执行文档 | execution/ | 定义生成 Layout Spec 的输入、输出、步骤和 Layout Gate | 人工维护 | Flow 03 |
| 04_layout_spec_to_wireframe.md | Layout Spec 到线框图执行文档 | execution/ | 定义 Wireframe Preflight、Figma 线框图生成和变更记录要求 | 人工维护 | Flow 04 |
| 05_structure_mapping.md | 结构映射执行文档 | execution/ | 定义 Wireframe 与采样端 Figma 来源结构映射的输入、输出、步骤和 Harness Check | 人工维护 | Flow 05 |
| 06_design_system_extraction.md | 设计系统提取执行文档 | execution/ | 定义从采样端 Figma 来源提取设计系统草案的输入、输出、步骤和 Harness Check | 人工维护 | Flow 06 |
| 07_visual_spec.md | 高保真设计指令执行文档 | execution/ | 定义生成 Visual Spec 的输入、输出、步骤和 Harness Check | 人工维护 | Flow 07 |
| 08_hifi_generation.md | 高保真生成执行文档 | execution/ | 定义根据 Visual Spec 生成 Figma 高保真稿的输入、输出、步骤和 Harness Check | 人工维护 | Flow 08 |
| 09_hifi_review_backfill.md | 高保真回填与设计层发布执行文档 | execution/ | 定义高保真 Harness 结论回填到 Design System 并发布设计层的流程 | 人工维护 | Flow 09 |
| 10_layer_naming_normalization.md | 图层命名规范化执行文档 | execution/ | 定义 Frame / 图层命名扫描、命名映射、重命名、复扫和 Layer Naming Harness Gate 放行流程 | 人工维护 | Hi-Fi Harness / 命名治理 |
| 11_autolayout_backfill.md | Auto Layout 回填执行文档 | execution/ | 定义已有高保真静态稿 Auto Layout 回填、视觉校验、拉伸测试、absolute positioning 扫描和 Auto Layout Harness Gate 放行流程 | 人工维护 | Hi-Fi Harness / Auto Layout 治理 |
| wireframe_construction_method.md | 线框图构造方法 | execution/ | 定义 Page Frame、Module Frame、Control Frame、Element 的构造顺序和自检顺序 | 人工维护 | Flow 04 |

### Workspace

| English Name | 中文名称 | 路径 | 作用 | 生成方式 | 维护流程 |
|---|---|---|---|---|---|
| {prd_file}.md | 当前项目 PRD | workspace/PRD/ | 当前要生成线框图的 PRD 输入，文件名按项目而定 | 人工维护 | PRD 输入 |
| figma_targets.md | Figma 目标登记 | workspace/ | 记录当前项目采样端 Figma 链接优先级列表、线框图输出端、高保真输出端和设计层输出端的 Figma 文件链接、Page 名称、可选 pageID 和用途；采样端链接使用 `数字. Figma链接` 格式，数字表示采样优先级 | 人工维护 / 执行前确认 | Flow 04 / Flow 05 / Flow 06 / Flow 08 / Flow 09 |
| {page_id}.md | 页面 Intent | workspace/intents/ | 记录单个页面的目标、首要动作、视觉重心、主要操作和硬约束 | AI 生成 / 人工审核 | Flow 01 |
| {page_id}.md | 页面元素权重排序 | workspace/priority_maps/ | 记录单个页面元素的 P0/P1/P2/P3 分级和原因 | AI 生成 / 人工审核 | Flow 02 |
| {page_id}.md | 页面 Layout Spec | workspace/layout_specs/ | 记录单个页面的可见布局模块、权重、关键内容和 PRD 约束 | AI 生成 / 人工审核 | Flow 03 |
| component-index.json | 组件候选索引 | workspace/structure_mapping/ | 记录采样端 Figma 来源与 Wireframe 中可复用组件候选的结构依据和置信度 | AI 生成 / 人工审核 | Flow 05 |
| page-structure-map.json | 页面结构映射 | workspace/structure_mapping/ | 记录 Wireframe 页面、模块、控件与采样端 Figma 来源结构的映射关系 | AI 生成 / 人工审核 | Flow 05 |
| mapping-review.md | 结构映射审核清单 | workspace/structure_mapping/ | 记录低置信度映射、未映射项和人工确认问题 | AI 生成 / 人工审核 | Flow 05 |
| raw-style-inventory.json | 真实样式清单 | workspace/design_system/ | 记录从采样端 Figma 来源真实读取到的样式、Auto Layout 和结构数据 | AI 生成 / 人工审核 | Flow 06 |
| design-system-draft.json | 设计系统草案 | workspace/design_system/ | 记录当前线框图实际用到的按需样式草案，每条样式用 style_id 命名并追溯到 raw-style-inventory.items；components 可选，只记录当前线框图实际用到的组件关系 | AI 生成 / 人工审核 | Flow 06 |
| design-system-review.md | 设计系统审核清单 | workspace/design_system/ | 记录低置信度归纳、冲突项和人工确认项 | AI 生成 / 人工审核 | Flow 06 / Flow 09 |
| {page_id}.md | 页面 Visual Spec | workspace/visual_specs/ | 记录单个页面的高保真设计指令 | AI 生成 / 人工审核 | Flow 07 |
| run_xxx.md | 运行记录 | workspace/records/ | 每次执行新增记录，记录输入来源、执行范围、Figma 采样端、线框图输出端、高保真输出端、设计层输出端、输出结果、Frame ID、断点续跑信息、Gate 结果、Figma 后变更和回填结论 | AI 生成 / 自动 Gate 校验 | 全流程 |
| {run_id}_{gate}_gate.json | Harness Gate JSON | workspace/harness/ | 每个 Gate 的机器校验结果文件，由 harness_check.py 或对应 Figma Gate 脚本生成；缺失时 Gate 视为 BLOCKED | AI / 脚本生成 | Harness Gate |
| （暂存 Figma 脚本） | Figma 脚本暂存目录 | workspace/figma_scripts/ | 暂存用于特定 run 的临时 Figma 操作脚本；当前为空目录，脚本不纳入版本跟踪 | 按需存放 | 临时使用 |
| {run_id}/ | 旧产物归档 | workspace/archive/ | 按需保存从零重跑前移出的旧阶段产物，records 不随产物归档移动 | 人工维护 | 重跑归档 |
| README.md | 工作区说明 | workspace/ | 说明 workspace 目录用途 | 人工维护 | 文档治理 |

## 维护规则

```text
新增、删除、重命名目录或核心文件时，必须同步更新 docs/file_structure.md。
新增、删除、重命名核心文件或改变文件职责时，必须同步更新 docs/file_index.md。
只修改文件正文内容且不改变职责时，不需要更新 file_index.md 或 file_structure.md。
```

## 当前缺口

```text
当前核心目录和流程文档已建立。
可通过 `scripts/clean_workspace_outputs.py` 清理上一轮生成产物，再从 PRD 和 Figma 目标登记重新跑流程。
Harness Gate 已有 `scripts/harness_check.py`；Layer Naming / Auto Layout 的独立 machine-owned gate 仍待接入脚本化检查。
```
