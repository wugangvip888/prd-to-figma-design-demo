# Harness Backlog

## 目的

记录后续需要补强的 Harness 检查能力。
当前文件仅作为待办清单，不影响现有 gate，也不修改 `scripts/harness_check.py`。

## 待升级项

1. 状态样式作用节点检查
   - 校验 disabled / selected / active / error 等状态样式是否只作用于对应控件节点。
   - 禁止状态样式上移到父级容器、保护层、页面背景或无状态语义节点。

2. Figma 实际间距检查
   - 根据 Design System 中的 spacing style_id，读取 Hi-Fi 实际节点 x / y / width / height。
   - 校验同语义节点间距是否与 source_ref 对应的源节点一致。
   - 示例：parameter chip 的 label/value gap、value/icon gap、right padding。

3. 横向溢出检查
   - 校验非横滑容器的 Frame 不突破父级容器或页面安全边距。
   - 只有 Wireframe / Layout Spec / Visual Spec 明确标注横滑时，才允许内部滚动内容超出父级可视宽度。

4. 业务文本完整展示检查
   - 校验字段名、字段值、按钮文案、标题等业务文本节点没有被压缩到小于目标文案实际显示宽度。
   - 横向空间不足时，应通过换行、分行或调整兄弟元素解决，而不是压缩业务文本。

5. 重叠检查
   - 校验同父级文本、控件、图标和辅助说明之间不存在 bounding box overlap。
   - 重点覆盖多行文案替换后的 hint / counter / action 纵向重排。

6. 图标来源检查
   - 校验 Hi-Fi 中新增或替换的 icon / symbol 是否能追溯到采样源节点、项目图标库或 design-system-draft.json 资产记录。
   - 禁止未记录来源的 emoji、Unicode 或临时 icon 占位进入最终高保真。

7. Figma 几何检查接入方式
   - 后续评估是否在 `scripts/harness_check.py` 中接入 Figma API / MCP metadata 读取。
   - 需要处理节点 ID 变化、命名变化、网络/API 失败和检查稳定性问题。

