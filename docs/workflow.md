# Workflow

## 主流程

```text
workspace/PRD/{prd_file}.md
→ workspace/intents/{page_id}.md
→ Intent Harness Check
→ workspace/priority_maps/{page_id}.md
→ Priority Harness Check
→ workspace/layout_specs/{page_id}.md
→ Layout Harness Check
→ Wireframe Preflight Check
→ Figma Wireframe
→ workspace/structure_mapping/
→ Structure Mapping Harness Check
→ workspace/design_system/
→ Design System Harness Check
→ workspace/visual_specs/{page_id}.md
→ Visual Spec Harness Check
→ Figma Hi-Fi
→ Hi-Fi Generation Harness Check
→ Figma Design Layer
→ Design Layer Publishing + Design System Backfill
→ Backfill Harness Check
→ Layer Naming Harness Gate
→ Auto Layout Harness Gate
→ Layer Naming Harness Recheck
→ workspace/records/run_xxx.md
```

`prompts/00_run_full_pipeline.md` 的自动边界是从 PRD 到设计层交付完成；Wireframe、Hi-Fi 和设计层中间结果不等待人工验收。每个阶段必须执行对应 Harness Gate，Gate 失败、规则冲突或 Figma 输出端无法解析时才停止。

## 执行入口

```text
全流程入口：prompts/00_run_full_pipeline.md
分步入口：prompts/01_prd_to_intent.md → prompts/02_intent_to_priority_map.md → prompts/03_priority_map_to_layout_spec.md → prompts/04_layout_spec_to_wireframe.md → prompts/05_structure_mapping.md → prompts/06_design_system_extraction.md → prompts/07_visual_spec.md → prompts/08_hifi_generation.md → prompts/09_hifi_review_backfill.md → prompts/10_layer_naming_normalization.md → prompts/11_autolayout_backfill.md
```

默认优先使用全流程入口端到端生成到设计层。分步入口仅用于单独修复、断点恢复或局部重跑。

## 执行顺序

1. PRD to Intent：识别页面、目标、用户任务和 PRD 硬约束。
2. Intent Harness Check：校验 Intent 是否覆盖 PRD 的页面目标、关键状态和硬约束。
3. Intent to Priority Map：同时参考 PRD 和 Intent，为页面元素标注 P0/P1/P2/P3。
4. Priority Harness Check：校验 Priority Map 是否服务 Intent，且不遗漏 PRD 必须出现的元素。
5. Priority Map to Layout Spec：同时参考 PRD、Intent 和 Priority Map，将权重排序转为可见布局模块。
6. Layout Harness Check：校验 Layout Spec 是否覆盖 Priority Map，并保持 PRD 与 Intent 一致。
7. Wireframe Preflight Check：生成 Wireframe 前，统一校验 PRD、Intent、Priority Map 和 Layout Spec 无冲突、无关键遗漏、无凭空新增。
8. Layout Spec to Wireframe：通过 Preflight 后，按 wireframe_rules 和 structure_preparation_rules 在 Figma 中生成一个页面状态一个 Frame 的线框图。
9. Structure Mapping：Wireframe Gate 通过后不等待人工验收，继续将 Wireframe 与采样端 Figma 来源结构建立页面、模块、控件和组件候选映射。
10. Structure Mapping Harness Check：校验映射覆盖、置信度、未映射项和复用依据。
11. Design System Extraction：从采样端 Figma 来源提取 raw style inventory、design system draft 和 review 清单。
12. Design System Harness Check：校验设计系统草案是否来自真实读取结果，且未把 AI 推测当成已确认规则。
13. Visual Spec：结合业务结构、线框图、结构映射和设计系统草案，生成每个页面的高保真设计指令。
14. Visual Spec Harness Check：校验 Visual Spec 是否服从 PRD、Intent、Priority Map、Layout Spec、Wireframe 和 Design System。
15. Hi-Fi Generation：按 Visual Spec 在 Figma 中生成 360 x 780 高保真设计稿。
16. Hi-Fi Generation Harness Check：校验高保真稿是否覆盖 Visual Spec、保持尺寸和可编辑结构。
17. Design Layer Publishing + Design System Backfill：将通过 Harness 的高保真结果复制或同步到设计层输出端，并将稳定结论回填到 Design System。
18. Backfill Harness Check：校验回填结论、设计层输出和记录是否可追溯。
19. Layer Naming Harness Gate：校验图层命名是否满足语义化、英文 snake_case、无默认名、无中文 frame-like 名称和无无效 source_ 前缀；不通过则回到命名规范化流程修正。
20. Auto Layout Harness Gate：校验 Auto Layout 回填是否保持静态视觉、无未经确认新增结构层、无未经确认 absolute positioning，并完成截图、metadata、拉伸和绝对路径扫描；不通过则回到 Auto Layout 制作流程修正。
21. Layer Naming Harness Recheck：Auto Layout 修改后复检新增或调整结构的命名；不通过则回到命名规范化流程修正。
22. Record：新增记录输入、范围、输出、Frame ID、自动 Gate 结果和变更。

命名规范化流程详见 `execution/10_layer_naming_normalization.md`。Auto Layout 回填流程详见 `execution/11_autolayout_backfill.md`。

## 判定优先级

```text
PRD > rules > Intent > Priority Map > Layout Spec > Wireframe > Structure Mapping > Design System > Visual Spec > Hi-Fi
```

PRD 是业务硬边界。rules 约束生成方式，不改写 PRD。
所有阶段必须全盘阅读 PRD，不得只读取局部页面说明或 PRD-原型图。若 PRD 中存在【PRD-原型图】、页面原型图、线框图或 Markdown 字符原型，原型图仅在页面结构、模块顺序、可见文案、状态表达和 CTA 位置等界面表达与其他 PRD 内容或下游产物冲突时优先；业务逻辑、字段约束、校验规则、数据模型、埋点和后台流程仍以 PRD 正文为准。

## 生成关系

```text
PRD → Intent
PRD + Intent → Priority Map
PRD + Intent + Priority Map → Layout Spec
PRD + Intent + Priority Map + Layout Spec → Wireframe
Wireframe + 采样端 Figma 来源 → Structure Mapping
采样端 Figma 来源 + Structure Mapping → Design System
PRD + Intent + Priority Map + Layout Spec + Wireframe + Structure Mapping + Design System → Visual Spec
Visual Spec → Hi-Fi
Hi-Fi → Design Layer
```

## Wireframe 生成规则

```text
Frame、尺寸、排布、命名、层级和系统 UI 规则来自 rules/wireframe_rules.md。
组件候选、Token 采样和 Pattern 候选的结构预备规则来自 rules/structure_preparation_rules.md。
标准 Wireframe、Hi-Fi 和设计层 Page Frame 尺寸固定为 360 x 780；PRD 中的设备规格只作为适配参考，不覆盖标准画布尺寸。
```

## Harness Gate

```text
每一步生成后必须做对应 Harness Check。
Wireframe 生成前必须做 Wireframe Preflight Check。
全流程入口必须从 PRD 自动执行到设计层交付完成；Wireframe、Hi-Fi 和设计层不设置人工验收停顿。
如果发现冲突、关键遗漏、凭空新增或 Gate 失败，先停止进入下一步，并回补或标注阻塞原因。
Layer Naming Harness Gate 和 Auto Layout Harness Gate 均为放行门禁；任一 Gate 不通过，必须回到对应流程定位问题、修正并重新检查，直到通过后才能进入下一步。
```

## 重跑策略

```text
过程产物默认覆盖为最新版本。
Figma Wireframe 默认覆盖 `workspace/figma_targets.md` 中线框图输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Figma Hi-Fi 默认覆盖 `workspace/figma_targets.md` 中高保真输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
Figma Design Layer 默认覆盖 `workspace/figma_targets.md` 中设计层输出端 Page 名称或 pageID 唯一解析到的 Page 内容。
workspace/records/run_xxx.md 每次新增，不覆盖旧记录。
只有用户明确要求保留旧版时，才在 Figma 中新建副本或追加版本。
```

## 清理后重跑

```text
当需要像首次执行一样验证 00 全流程时，可以先清理 workspace 中上一轮生成产物。
清理工具为 scripts/clean_workspace_outputs.py。
默认执行 `python3 scripts/clean_workspace_outputs.py` 只做 dry-run，打印将删除的文件。
确认范围后执行 `python3 scripts/clean_workspace_outputs.py --apply` 才实际删除。
清理脚本保留 rules、prompts、scripts、execution、workspace/PRD、workspace/figma_targets.md、workspace/archive、.gitkeep 和 workspace/harness/harness-backlog.md。
清理脚本删除 workspace/intents、priority_maps、layout_specs、structure_mapping、design_system、visual_specs、harness/run_* 和 records/run_* 中的生成文件。
清理本地生成产物不等于清理 Figma 输出端；如需完全从零验证，也必须同步清理或覆盖 Figma 中线框图、高保真图和设计层输出 Frame。
```

## Figma 采样端读取策略

```text
workspace/figma_targets.md 中的采样端链接是 Structure Mapping、Design System Extraction、Visual Spec 和 Hi-Fi Generation 的 Figma 采样来源。
采样端链接按 `数字. Figma链接` 填写；数字越小优先级越高。
同一数字允许多条 Figma 链接，权重相同，按书写顺序读取。
采样链接可以指向 Figma 文件、Page、Section、Frame 或具体节点；流程只解析 Figma 链接本身，不要求额外填写 pageID、Page 名称或 nodeID。
读取时按数字优先级升序执行；上一级可支撑判断时不得跳级到下一级。
若某一层级不可访问、内容不足或无法覆盖当前模块，才降级读取后续数字层级，并在 run record、mapping-review 或 design-system-review 中记录降级来源和原因。
同层或跨层采样结论冲突时，不得自行裁定；必须记录冲突项、相关采样链接和节点 ID，并作为 Gate 阻塞项停止当前流程。
```
