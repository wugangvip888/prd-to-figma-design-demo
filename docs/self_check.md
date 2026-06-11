# Self Check

本文件用于在执行全流程、修改流程文档或新增核心文件后，检查项目结构和引用是否健康。

## 结构检查

```text
README.md 存在。
docs/file_index.md、docs/file_structure.md、docs/workflow.md、docs/process_rules.md、docs/self_check.md 存在。
prompts/00_run_full_pipeline.md、prompts/01-09 分步 Prompt、prompts/10_layer_naming_normalization.md 和 prompts/11_autolayout_backfill.md 存在。
execution/00_run_full_pipeline.md、execution/01-09 分步执行文档、execution/10_layer_naming_normalization.md、execution/11_autolayout_backfill.md 和 execution/wireframe_construction_method.md 存在。
rules/intent_rules.md、rules/priority_rules.md、rules/layout_spec_rules.md、rules/wireframe_rules.md、rules/structure_preparation_rules.md、rules/structure_mapping_rules.md、rules/design_system_rules.md、rules/visual_spec_rules.md、rules/hifi_generation_rules.md、rules/autolayout_rules.md、rules/hifi_review_rules.md、rules/harness_rules.md 存在。
workspace/PRD/ 中存在当前 PRD 文件。
workspace/figma_targets.md 存在，且包含采样端链接、线框图输出端链接、高保真输出端链接和设计层输出端链接；采样端链接必须至少包含一条 `数字. Figma链接` 格式的记录，数字表示采样优先级；输出端必须包含 figma文件链接和 Page 名称或 pageID，pageID 可选，缺失时必须能按 Page 名称唯一解析。
workspace/intents/、workspace/priority_maps/、workspace/layout_specs/、workspace/structure_mapping/、workspace/design_system/、workspace/visual_specs/、workspace/records/ 存在。
scripts/clean_workspace_outputs.py 存在，默认 dry-run，必须加 `--apply` 才实际删除生成产物。
scripts/figma_autolayout_check.py 存在。
scripts/figma_geometry_check.py 存在。
如执行从零重跑前归档，workspace/archive/{run_id}/ 应存在并保留被移出的旧阶段产物，workspace/records/ 不随阶段产物归档移动。
```

## 引用检查

```text
README.md 的快速开始入口指向 prompts/00_run_full_pipeline.md。
docs/workflow.md 同时记录全流程入口和分步入口。
prompts/00_run_full_pipeline.md 引用的 docs、execution、rules 文件均存在。
prompts/01-09 引用的 docs、execution、rules 文件均存在。
prompts/10_layer_naming_normalization.md 和 prompts/11_autolayout_backfill.md 引用的 docs、execution、rules 文件均存在。
execution/00_run_full_pipeline.md 引用的 rules 和 execution 文件均存在。
execution/01-09 引用的 rules 文件均存在。
execution/10_layer_naming_normalization.md 和 execution/11_autolayout_backfill.md 引用的 docs、rules 文件均存在。
Wireframe 相关 prompt 和 execution 必须引用 rules/wireframe_rules.md、rules/structure_preparation_rules.md 和 execution/wireframe_construction_method.md。
`prompts/00_run_full_pipeline.md` 和 `execution/00_run_full_pipeline.md` 必须明确：自动流程从 PRD 执行到设计层交付完成；Wireframe、Hi-Fi 和设计层中间结果不等待人工验收，但每阶段必须通过对应 Harness Gate。
Structure Mapping 相关 prompt 和 execution 必须引用 rules/structure_mapping_rules.md。
Design System 相关 prompt 和 execution 必须引用 rules/design_system_rules.md。
Structure Mapping、Design System Extraction 和 Hi-Fi Generation 必须按 workspace/figma_targets.md 中采样端链接的数字优先级升序读取；同一数字内链接权重相同，按书写顺序读取；降级、不可访问或冲突必须在 run record 或审核清单中记录来源和原因。
Visual Spec 相关 prompt 和 execution 必须引用 rules/visual_spec_rules.md。
Hi-Fi 相关 prompt 和 execution 必须引用 rules/hifi_generation_rules.md、rules/autolayout_rules.md 和 rules/hifi_review_rules.md。
docs/file_index.md 与 docs/file_structure.md 对核心文件的记录一致。
新增、删除、重命名核心文件后，必须同步更新 docs/file_index.md 和 docs/file_structure.md。
新增归档目录或改变当前产物目录状态后，必须同步更新 docs/file_index.md 和 docs/file_structure.md 的当前状态说明。
```

## 流程检查

```text
全流程入口默认使用 prompts/00_run_full_pipeline.md。
PRD → Intent 后必须执行 Intent Gate。
PRD + Intent → Priority Map 后必须执行 Priority Gate。
PRD + Intent + Priority Map → Layout Spec 后必须执行 Layout Gate。
PRD + Intent + Priority Map + Layout Spec → Wireframe 前必须执行 Wireframe Preflight Gate。
Wireframe 生成时必须同时应用 wireframe_rules.md 和 structure_preparation_rules.md。
Figma Wireframe 生成并校验通过后必须自动继续 Structure Mapping，不等待人工验收 Wireframe。
Wireframe → Structure Mapping 后必须执行 Structure Mapping Harness Check。
Structure Mapping → Design System Extraction 后必须执行 Design System Harness Check。
Design System Extraction → Visual Spec 后必须执行 Visual Spec Harness Check。
Visual Spec → Hi-Fi Generation 后必须执行 Hi-Fi Generation Harness Check。
Hi-Fi Generation Harness Check 后必须执行 Hi-Fi Review + Design System Backfill。
Hi-Fi Review + Design System Backfill 后必须执行 Backfill Harness Check。
Backfill Harness Check 后必须执行 Layer Naming Harness Gate。
Layer Naming Harness Gate 通过后才能进入 Auto Layout 回填。
Auto Layout 回填后必须执行 Auto Layout Harness Gate。
Auto Layout Harness Gate 通过后必须执行 Layer Naming Harness Recheck。
任一 Gate 发现 PRD 冲突、关键遗漏或凭空新增时，不进入下一步。
```

## Wireframe / Hi-Fi 尺寸检查

```text
标准 Wireframe、Hi-Fi 和设计层 Page Frame 尺寸固定为 360 x 780。
Wireframe、Hi-Fi 和设计层的同一批标准页面 Frame 必须保持相同尺寸。
PRD 中出现的设备基准、手机型号、pt 尺寸、倍率、安全区或适配说明，只作为业务与适配参考，不得覆盖标准 Page Frame 尺寸。
如果 PRD 明确要求平板、桌面端、横屏或特殊容器，必须先在 Layout Spec 中记录为适配参考或待人工确认，但标准 Page Frame 仍保持 360 x 780，除非用户在当前执行中明确要求更改本项目标准尺寸。
Hi-Fi Generation 不得破坏 360 x 780 页面尺寸。
```

## 重跑检查

```text
重跑同一页面时，Intent、Priority Map、Layout Spec 和 Visual Spec 默认覆盖同名 {page_id}.md。
重跑 Wireframe 时，默认覆盖 workspace/figma_targets.md 中线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
重跑 Structure Mapping 和 Design System Extraction 时，默认覆盖 workspace 中对应最新产物。
重跑 Hi-Fi 时，默认覆盖 workspace/figma_targets.md 中高保真输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
重跑 Design Layer 时，默认覆盖 workspace/figma_targets.md 中设计层输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
workspace/records/run_xxx.md 每次新增，不覆盖旧记录。
只有用户明确要求保留旧版时，才在 Figma 中新建副本或追加版本。
如果用户选择清理后从 00 重新跑，必须先执行 `python3 scripts/clean_workspace_outputs.py` 查看 dry-run 范围；确认后才能执行 `python3 scripts/clean_workspace_outputs.py --apply`。
清理脚本不得删除 workspace/PRD、workspace/figma_targets.md、rules、prompts、scripts、execution、workspace/archive、.gitkeep 和 docs/harness-backlog.md。
清理本地生成产物后，如需完全从零验证，也必须同步清理或覆盖 Figma 输出端旧 Frame，避免新流程误用旧设计结果。
```

## 断点续跑检查

```text
每完成一个阶段产物后必须立即落盘。
流程中断时必须记录最后成功阶段、已生成产物、阻塞原因和恢复入口。
恢复执行时必须先读取最近一次相关 run record。
恢复执行时必须检查 workspace/intents、workspace/priority_maps、workspace/layout_specs、workspace/structure_mapping、workspace/design_system、workspace/visual_specs 中已有产物。
已通过 Gate 且未受上游修改影响的产物可以复用。
恢复 Wireframe 前必须重新执行 Wireframe Preflight Gate。
恢复到 Wireframe 后必须重新执行 Wireframe Gate；通过后自动继续 Structure Mapping。
恢复 Hi-Fi 前必须重新执行 Visual Spec Harness Check。
```

## 系统文件检查

```text
.DS_Store、日志文件和 .env 文件不应纳入项目结构说明。
.gitignore 应忽略 .DS_Store、*.log、.env 和 .env.*。
```
