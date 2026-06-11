# Process Rules

## 分层原则

```text
prompts 只记录 AI 调用入口和任务编排。
execution 只记录执行流程。
rules 只记录判断规则。
records 只记录执行结果和人工确认。
docs 只记录项目级说明。
```

不得在多个层级重复维护同一条规则。

## 执行前读取顺序

```text
1. docs/workflow.md
2. 当前 prompt
3. 对应 execution 文档
4. execution 中列出的 rules 文件
5. 业务输入文件
6. 最近一次相关 records（如存在）
```

如果 docs、execution、rules、records 之间不一致，先指出冲突，再继续执行。

## 规则引用要求

```text
执行任何涉及优先级判断或来源选择的决策前，必须先在 run record 或产物注释中写出：
  「依据：[规则文件名] — [原文摘录]」
  「执行结果：[具体值或决策]」

如果 AI 无法写出具体规则出处，说明当前决策无规则支撑，必须停止并列为待人工确认项，不得继续执行。

常见高风险决策点（必须引用规则，不得凭空选择）：
1. 颜色来源：PRD 建议色 vs 采样端颜色 → 规则已明确：采样端 Figma 来源决定颜色，无需人工裁定，直接引用规则执行。
2. 结构同构判断：是否继承旧稿骨架 → 规则已明确：同构条件须全部满足，引用规则逐条核查。
3. 冲突裁定：任何规则未覆盖的歧义 → 必须停止，列出冲突项，等待人工确认，不得自行选择。

规则已有明确答案的情况，AI 直接引用规则执行，不升级为"冲突"交给人工。
规则没有答案的情况，AI 停止，明确标注，等待人工裁定。
```

## Harness 自评防退化要求

```text
Harness Check 执行时，AI 必须以"挑战者"视角逐项核查，而非以"验证者"视角确认自己的工作。
对每个检查项，AI 必须先假设"此项可能失败"，再用产物中的具体值证明通过或失败。
禁止使用模糊表述通过检查项，例如"基本符合"、"大体正确"、"来源可追溯"。
检查项结论只允许两种：通过（附具体证据）或失败（附具体违规位置）。
凡检查项结论无法附上产物中的具体字段值或节点 ID 作为证据，该项判定为失败。
```



```text
每一步生成后必须执行对应 Harness Check。
Wireframe 生成前必须执行 Wireframe Preflight Check。
`prompts/00_run_full_pipeline.md` 必须自动执行到设计层交付完成；Wireframe、Hi-Fi 和设计层中间结果不等待人工验收。
Structure Mapping、Design System Extraction、Visual Spec、Hi-Fi Generation、Hi-Fi Review Backfill、Layer Naming Normalization 和 Auto Layout Backfill 后必须执行对应 Harness Check / Gate。
Harness Check 发现 PRD 冲突、关键遗漏或凭空新增时，不进入下一步。
图层命名规范化和 Auto Layout 回填必须分别执行独立 Harness Gate。
命名流程不通过 Layer Naming Harness Gate 时，不得进入 Auto Layout 回填；必须回到命名规范化流程修正后重新检查。
Auto Layout 流程不通过 Auto Layout Harness Gate 时，不得进入交付；必须回到 Auto Layout 制作流程修正后重新检查。
Auto Layout 修改后必须再次执行 Layer Naming Harness Recheck；不通过时回到命名规范化流程修正。
单次项目改动写入 records。
只有跨项目可复用的判断方法才沉淀到 rules。
```

## 断点续跑原则

```text
每完成一个阶段产物，必须立即写入对应 workspace 目录。
全流程执行中断时，必须尽可能写入或补写 workspace/records/run_xxx.md，记录已完成阶段、最后成功阶段、阻塞原因和下一步恢复入口。
恢复执行时，必须先读取最近一次相关 run record，再检查 workspace/intents、workspace/priority_maps、workspace/layout_specs、workspace/structure_mapping、workspace/design_system、workspace/visual_specs 中已存在的产物。
已通过 Gate 且未受 PRD 或人工修改影响的产物可以复用。
受 PRD、Intent、Priority Map、Layout Spec、Wireframe、Structure Mapping 或 Design System 上游变更影响的下游产物必须重新生成。
不得因为中断而跳过 Harness Gate、Wireframe Preflight Gate 或 Hi-Fi 生成前的 Visual Spec Harness Check。
不得因为断点续跑而跳过任何 Harness Gate。
```
