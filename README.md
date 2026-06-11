# PRD to Figma Design

本项目用于从 PRD 生成结构化线框图，并在此基础上继续承接 Figma 结构映射、Design System 提取、Visual Spec 和 AI 高保真设计生成流程。

## 流程

```text
PRD
→ Intent
→ Harness Check
→ Element Priority Map
→ Harness Check
→ Layout Spec
→ Layout Harness Check
→ Wireframe Preflight Check
→ Figma Wireframe
→ Structure Mapping
→ Structure Mapping Harness Check
→ Design System Extraction
→ Design System Harness Check
→ Visual Spec
→ Visual Spec Harness Check
→ Hi-Fi Generation
→ Hi-Fi Generation Harness Check
→ Design Layer Publishing
→ Backfill Harness Check
→ Layer Naming Harness Gate
→ Auto Layout Harness Gate
→ Layer Naming Harness Recheck
→ Run Record
```

## 包含

- PRD 到页面 Intent
- PRD + Intent 到页面元素权重排序
- PRD + Intent + Priority Map 到 Layout Spec
- PRD + Intent + Priority Map + Layout Spec 到 Figma Wireframe
- Wireframe + 采样端 Figma 来源到 Structure Mapping
- 采样端 Figma 来源 + Structure Mapping 到 Design System 草案
- Layout Spec + Structure Mapping + Design System 到 Visual Spec
- Visual Spec 到 Figma 高保真设计稿
- 高保真生成结果到设计层发布与 Design System Backfill
- 每一步生成后的 Harness Check
- Wireframe 生成前的 Preflight Check
- 每次执行、Figma 生成和人工审核回填的 Run Record

## 当前未完成

- 代码生成

## 快速开始

1. 将 PRD 文件放入 `workspace/PRD/`。
2. 在 `workspace/figma_targets.md` 填写采样端 Figma 链接优先级列表，以及线框图输出端和高保真输出端的 Figma 文件链接与 Page 名称；pageID 可选，执行时可按 Page 名称解析。
3. 执行 `prompts/00_run_full_pipeline.md`，自动生成 Intent、Priority Map、Layout Spec、Figma Wireframe、Structure Mapping、Design System、Visual Spec、Figma Hi-Fi、设计层、Layer Naming 和 Auto Layout。
4. 中间的 Wireframe、Hi-Fi 和设计层不等待人工检查；任一 Harness Gate 失败时停止并记录阻塞原因。

## 清理生成数据

重新从 00 流程验证规则时，可清理上一轮生成产物，保留 PRD、Figma 目标、规则、脚本和提示词：

```bash
python3 scripts/clean_workspace_outputs.py
python3 scripts/clean_workspace_outputs.py --apply
```

默认是 dry-run，只打印将删除的文件；加 `--apply` 才会实际删除。

## 分步执行

如需人工分步审核，也可以按顺序执行：

1. `prompts/01_prd_to_intent.md`
2. `prompts/02_intent_to_priority_map.md`
3. `prompts/03_priority_map_to_layout_spec.md`
4. `prompts/04_layout_spec_to_wireframe.md`
5. `prompts/05_structure_mapping.md`
6. `prompts/06_design_system_extraction.md`
7. `prompts/07_visual_spec.md`
8. `prompts/08_hifi_generation.md`
9. `prompts/09_hifi_review_backfill.md`
10. `prompts/10_layer_naming_normalization.md`
11. `prompts/11_autolayout_backfill.md`
