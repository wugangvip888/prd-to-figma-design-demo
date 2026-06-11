# 当前文件架构 / Current File Structure

本文档记录 `prd-to-figma-design/` 当前真实存在的项目文件架构。系统文件（如 `.DS_Store`）和 `.git/` 不纳入结构说明。

本项目以 `AI_Design_System/docs/file_structure.md` 为结构样例，当前记录 PRD 到线框图、高保真设计生成流程所需的目录和核心文件。

## 维护规则

- 本文件只记录当前真实存在的目录和核心文件结构，不记录临时文件、系统文件或运行中间产物。
- 文件和目录在结构树中使用 `英文名（中文名）` 格式，例如 `file_index.md（文件索引）`。
- 只在新增、删除、重命名目录或核心文件时更新本文件；普通内容修改不需要更新。
- `workspace/records/run_xxx.md` 按需展示，默认只展示到记录目录。
- 文件用途的详细说明放在 `docs/file_index.md`，本文件只做结构快照和中文名标注。

```text
prd-to-figma-design/
├── README.md（项目入口说明）
│
├── docs/（项目说明层）
│   ├── file_index.md（文件索引）
│   ├── file_structure.md（当前文件架构）
│   ├── harness_check_summary.md（Harness检查汇总）
│   ├── process_rules.md（流程治理规则）
│   ├── self_check.md（自检清单）
│   ├── workflow.md（工作流说明）
│   └── harness-backlog.md（Harness待补强检查能力待办清单）
│
├── scripts/（脚本层）
│   ├── clean_workspace_outputs.py（workspace生成产物清理脚本）
│   ├── fetch_placeholder_image_v3.py（占位图片获取脚本）
│   ├── figma_autolayout_check.py（Figma Auto Layout Harness Gate 机器检测脚本）
│   ├── figma_geometry_check.py（Figma 高保真几何 Harness Gate 检测脚本）
│   └── harness_check.py（Harness检查脚本）
│
├── prompts/（提示词目录— 入口，给 AI 的启动指令，告诉它去做什么。）
│   ├── 00_run_full_pipeline.md（全流程执行提示词）
│   ├── 01_prd_to_intent.md（PRD到Intent提示词）
│   ├── 02_intent_to_priority_map.md（Intent到元素权重排序提示词）
│   ├── 03_priority_map_to_layout_spec.md（权重排序到Layout Spec提示词）
│   ├── 04_layout_spec_to_wireframe.md（Layout Spec到线框图提示词）
│   ├── 05_structure_mapping.md（结构映射提示词）
│   ├── 06_design_system_extraction.md（设计系统提取提示词）
│   ├── 07_visual_spec.md（高保真设计指令提示词）
│   ├── 08_hifi_generation.md（高保真生成提示词）
│   ├── 09_hifi_review_backfill.md（高保真审核回填提示词）
│   ├── 10_layer_naming_normalization.md（图层命名规范化提示词）
│   └── 11_autolayout_backfill.md（Auto Layout回填提示词）
│
├── rules/（规则层— 标准，定义什么是对的，什么是错的。跨项目通用。）
│   ├── autolayout_rules.md（Auto Layout补齐规则）
│   ├── intent_rules.md（Intent规则）
│   ├── priority_rules.md（页面元素权重排序规则）
│   ├── layout_spec_rules.md（Layout Spec规则）
│   ├── wireframe_rules.md（线框图规则）
│   ├── structure_preparation_rules.md（结构预备规则）
│   ├── structure_mapping_rules.md（结构映射规则）
│   ├── design_system_rules.md（设计系统提取规则）
│   ├── visual_spec_rules.md（高保真设计指令规则）
│   ├── hifi_generation_rules.md（高保真生成规则）
│   ├── hifi_review_rules.md（高保真审核回填规则）
│   ├── harness_rules.md（Harness校验规则）
│   └── project/（项目级规则子目录）
│       └── 360_zhixiao.md（360智效项目规则）
│
├── execution/（执行层— 步骤，告诉 AI 怎么一步一步做，是操作手册。）
│   ├── 00_run_full_pipeline.md（全流程执行文档）
│   ├── 01_prd_to_intent.md（PRD到Intent执行文档）
│   ├── 02_intent_to_priority_map.md（Intent到元素权重排序执行文档）
│   ├── 03_priority_map_to_layout_spec.md（权重排序到Layout Spec执行文档）
│   ├── 04_layout_spec_to_wireframe.md（Layout Spec到线框图执行文档）
│   ├── 05_structure_mapping.md（结构映射执行文档）
│   ├── 06_design_system_extraction.md（设计系统提取执行文档）
│   ├── 07_visual_spec.md（高保真设计指令执行文档）
│   ├── 08_hifi_generation.md（高保真生成执行文档）
│   ├── 09_hifi_review_backfill.md（高保真审核回填执行文档）
│   ├── 10_layer_naming_normalization.md（图层命名规范化执行文档）
│   ├── 11_autolayout_backfill.md（Auto Layout回填执行文档）
│   └── wireframe_construction_method.md（线框图构造方法）
│
├── workspace/（当前项目工作区— 产物，每次跑流程生成的结果落在这里。）
│   ├── README.md（工作区说明）
│   ├── figma_targets.md（Figma采样端与输出目标登记）
│   ├── PRD/（PRD输入目录）
│   │   └── {prd_file}.md（当前项目PRD，文件名按项目而定）
│   │
│   ├── intents/（Intent输出目录）
│   ├── priority_maps/（页面元素权重排序目录）
│   ├── layout_specs/（Layout Spec输出目录）
│   ├── structure_mapping/（结构映射输出目录）
│   ├── design_system/（设计系统输出目录）
│   ├── visual_specs/（高保真设计指令输出目录）
│   ├── records/（运行记录目录）
│   ├── harness/（Harness Gate JSON 输出目录）
│   ├── figma_scripts/（Figma脚本暂存目录，当前为空）
│   └── archive/（归档目录）
```

## 当前完成状态

```text
docs：workflow、process_rules、file_index、file_structure、self_check 已建立。
prompts：全流程入口，以及 PRD到Intent、Intent到Priority Map、Priority Map到Layout Spec、Layout Spec到Wireframe、Structure Mapping、Design System Extraction、Visual Spec、Hi-Fi Generation、Hi-Fi Review Backfill、Layer Naming Normalization、Auto Layout Backfill 分步提示词已建立。
rules：Intent、Priority、Layout Spec、Wireframe、Structure Preparation、Structure Mapping、Design System、Visual Spec、Hi-Fi Generation、Hi-Fi Review、Harness 规则已建立。
execution：全流程执行文档、01-11 分步执行文档和线框图构造方法已建立。
workspace：当前项目工作区已建立，已放入真实 PRD 和 Figma 目标登记；intents、priority_maps、layout_specs、structure_mapping、design_system、visual_specs、harness 和 records 中的生成产物可通过清理脚本重置后重新跑流程。
scripts：Harness 检查、占位图片获取和 workspace 生成产物清理脚本已建立。
```

## 当前空目录

```text
workspace 生成产物目录可通过 `python3 scripts/clean_workspace_outputs.py --apply` 清理到仅保留 .gitkeep 和约定保留文件的状态，用于重新跑流程。
```
