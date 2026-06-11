# Auto Layout Backfill

## 目标

为已有 Figma 高保真静态稿补齐 Auto Layout、constraints 和 layout sizing，使结构可维护、可拉伸、可交付。

本流程以保持原静态稿视觉结果为最高优先级，不重新设计页面。

## 输入

```text
目标 Figma 文件、Page 或节点范围
已通过 Layer Naming Harness Gate 的节点树
rules/autolayout_rules.md
rules/harness_rules.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 输出

```text
已完成 Auto Layout 回填的 Figma 节点树
Auto Layout Harness Gate 结果
Layer Naming Harness Recheck 结果
workspace/records/run_xxx_autolayout_backfill.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/autolayout_rules.md
rules/harness_rules.md
rules/hifi_generation_rules.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 前置条件

```text
Layer Naming Harness Gate 必须已通过。
目标范围必须明确。
静态稿关键节点 x / y / width / height 必须可读取。
如现有结构不足以直接表达 Auto Layout，先按 `rules/autolayout_rules.md` 的「Auto Layout 结构调整边界」判断：有语义 wrapper/container、背景层与内容层拆分、同类子项归入语义容器可以自动执行；空白占位 Frame、无业务语义结构层或改变业务归属的调整必须等待人工确认。
```

## 执行步骤

1. 确认目标范围和基准视觉  
   读取目标节点 metadata，记录关键节点的 `x / y / width / height`、层级、constraints 和现有 Auto Layout 属性。

2. 判断结构是否适合 Auto Layout  
   识别哪些节点可以直接改为 Auto Layout，哪些复杂结构应保留普通 Frame + constraints。  
   如果目标范围包含顶部导航栏，必须按 `rules/autolayout_rules.md` 的「顶部导航栏 Auto Layout 判定」先判断其真实结构。

3. 标记禁止改动对象  
   明确不得删除、替换或重建的节点：
   - 原始文字
   - 图形标题
   - 图标
   - 图片
   - 装饰笔触
   - 业务控件
   - 已确认的页面状态内容

4. 逐层设置 Auto Layout  
   从局部模块开始，按真实语义设置方向、padding、gap、alignment、layout sizing 和 constraints。  
   不得为了套用 Auto Layout 改动静态视觉位置。

5. 处理复杂结构  
   如果复杂结构需要新增 `wrapper`、`container`、`spacer`、`padding frame` 或调整父子层级才能表达 Auto Layout，必须先按 `rules/autolayout_rules.md` 的「Auto Layout 结构调整边界」分类：有语义 wrapper/container 和同类子项语义容器可自动执行；空白占位 Frame、无业务语义结构层或改变业务归属的调整必须等待人工确认。具体审批要求见 `rules/autolayout_rules.md` 的「结构调整审批机制」。

6. 处理背景和浮层  
   背景节点只有在符合 `rules/autolayout_rules.md` 的边界时，才可将视觉属性转移到父 frame fill。  
   固定底部 CTA 使用 sibling order 和 constraints 表达层级与位置，不使用 Figma absolute positioning。

7. 每轮修改后校验静态视觉  
   修改后读取 metadata，检查关键节点是否发生非预期偏移。  
   自动执行 screenshot 检查，确认 Auto Layout 修改前后视觉是否发生非预期变化。  
   screenshot 检查只用于 Auto Layout 视觉不变性校验，不作为全局视觉审美判断。

8. 执行临时拉伸测试  
   需要验证响应关系时，复制临时副本进行拉伸测试。  
   测试范围必须覆盖：
   - 页面级背景
   - 顶部渐变或整屏底色
   - 内容安全区
   - 主要内容模块
   - 横滑视口
   - 固定底部 CTA

9. 删除临时测试副本  
   拉伸测试完成后删除临时副本，不把测试节点留在交付结构中。

10. 执行 absolute positioning 扫描  
    扫描目标节点整棵树，确认不存在未经用户明确允许的 `layoutPositioning=ABSOLUTE`。

11. 执行本机绝对路径扫描  
    扫描本次新增或修改的规则、记录、页面文件和交付说明，确认不存在本机绝对路径。

12. 执行 Auto Layout Harness Gate  
    按 `rules/harness_rules.md` 中的 `Auto Layout Harness Gate` 检查。  
    Gate 不通过时，回到对应步骤定位问题，修正后重新执行 Gate。

13. 执行 Layer Naming Harness Recheck  
    Auto Layout 修改可能新增或调整结构层，必须重新执行命名复检。  
    Recheck 不通过时，回到 `execution/10_layer_naming_normalization.md` 修正命名。

14. 写入 run record  
    记录目标范围、修改内容、冲突点、例外、结构调整方案、人工确认结果、执行结果、截图校验、拉伸测试、absolute positioning 扫描结果、本机绝对路径扫描结果和 Gate 结果。

## 禁止事项

```text
不得改变原静态稿视觉效果。
不得删除、替换或重建用户已有界面元素。
不得改变字体、字重、字形或文字节点字体属性。
不得为了 Auto Layout 改动已有图层的位置、尺寸、间距或视觉层级。
不得擅自新增空白占位 Frame、无业务语义结构层、spacer、padding frame 或 hidden bucket；有语义 wrapper/container 和同类子项语义容器按 `rules/autolayout_rules.md` 的「Auto Layout 结构调整边界」自动执行并记录。
不得使用 layoutPositioning=ABSOLUTE 保视觉位置。
不得把不可见样式源节点留在 Auto Layout 普通流里撑高父级。
不得只检查内容区，忽略页面级背景和 fixed CTA 的拉伸结果。
```

## Harness Gate

```text
Auto Layout Harness Gate 通过条件：
- 静态稿视觉位置、尺寸、间距、字体、图片、图标、装饰和业务层级未发生非预期变化。
- 没有新增未经当前任务、项目规则或人工确认允许的辅助结构层。
- 复杂结构不得默认跳过；如需保留普通 Frame + constraints，必须记录原因、影响范围和人工确认结果。
- 目标树不存在未经用户明确允许的 layoutPositioning=ABSOLUTE。
- 背景、安全区、横滑视口、固定底部 CTA 和页面级浮层符合规则。
- 已自动完成 metadata、screenshot 和必要的临时拉伸副本校验。
- 临时测试副本已删除。
- 本次新增或修改文件不存在本机绝对路径。
- 冲突、例外、结构调整方案、人工确认结果、执行结果和扫描结果已写入 run record。
```

## 失败回路

```text
Auto Layout Harness Gate 未通过
→ 定位失败项
→ 回到对应制作步骤
→ 修正 Auto Layout / constraints / sizing / 背景 / 层级
→ 重新做 metadata、screenshot、拉伸或扫描校验
→ 重新执行 Auto Layout Harness Gate
```

未通过 Gate 时，不得进入交付。
