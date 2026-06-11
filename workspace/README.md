# Workspace

这里放当前要执行的项目输入和生成结果。

- `PRD/{prd_file}.md`：当前项目 PRD
- `intents/`：页面 Intent
- `priority_maps/`：页面元素权重排序
- `layout_specs/`：布局规格
- `structure_mapping/`：Wireframe 与采样端 Figma 来源的结构映射
- `design_system/`：采样端 Figma 来源提取出的设计系统草案和审核清单
- `visual_specs/`：页面高保真设计指令
- `figma_targets.md`：当前项目采样端 Figma 链接优先级列表，以及线框图输出端、高保真输出端和设计层输出端的 Figma 文件链接与 Page 名称；输出端 pageID 可选
- `records/`：执行记录

清理生成产物时使用仓库根目录下的 `scripts/clean_workspace_outputs.py`。该脚本保留 `PRD/`、`figma_targets.md`、`.gitkeep`、`archive/` 和 `harness/harness-backlog.md`。
