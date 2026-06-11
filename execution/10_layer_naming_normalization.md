# Layer Naming Normalization

## 目标

对目标 Figma 范围执行图层命名规范化，使 Page、Module、Control、Element 和 frame-like 节点具备稳定、可读、可交付的语义命名。

本流程只处理命名，不改变视觉、布局、层级、样式、文字内容或业务语义。

## 输入

```text
目标 Figma 文件、Page 或节点范围
已确认的线框图 / 高保真稿 / 人工修改稿
rules/wireframe_rules.md
rules/hifi_generation_rules.md
rules/harness_rules.md
workspace/design_system/manual-hifi-adjustment-rules.md（如存在）
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 输出

```text
已完成命名规范化的 Figma 节点树
Layer Naming Harness Gate 结果
workspace/records/run_xxx_layer_naming.md
```

## 执行前请读取

```text
docs/process_rules.md
docs/workflow.md
rules/wireframe_rules.md
rules/hifi_generation_rules.md
rules/harness_rules.md
最近一次相关 workspace/records/run_xxx.md（如存在）
```

## 执行步骤

1. 确认目标范围  
   明确本次处理的是整页、单个模块、单个组件，还是指定节点树。

2. 扫描命名问题  
   扫描目标范围内所有需要交付的节点，重点包括：
   - `FRAME`
   - `GROUP`
   - `INSTANCE`
   - `COMPONENT`
   - `COMPONENT_SET`
   - 直接影响交付可读性的 `TEXT`、`RECTANGLE`、`VECTOR`、`IMAGE`

3. 记录命名问题分类  
   分类记录以下问题：
   - 默认 Figma 名称，例如 `Frame 1`、`Group 23`、`Rectangle 8`、`Text 12`
   - 中文 frame-like 名称
   - 无上下文 `label`
   - 无交付意义 `source_` 前缀
   - 纯位置词命名，例如 `top_group`、`left_area`
   - 纯视觉词命名，例如 `pink_frame`
   - 无语义数字尾缀

4. 建立命名映射  
   根据父级模块、业务语义、控件动作、元素角色建立 `old_name -> new_name` 映射。  
   命名必须使用英文 `snake_case`。

5. 执行重命名  
   只修改节点 `name`，不得修改：
   - x / y / width / height
   - Auto Layout 属性
   - constraints
   - fills / strokes / effects
   - 字体、字重、字号、line height
   - 图层顺序
   - 可见文案和业务语义

6. 命名复扫  
   重命名后重新扫描目标范围，确认剩余问题数量。

7. 执行 Layer Naming Harness Gate  
   按 `rules/harness_rules.md` 中的 `Layer Naming Harness Gate` 检查。  
   Gate 不通过时，回到第 3 步定位问题，修正后重新执行 Gate。

8. 写入 run record  
   记录目标范围、扫描结果、重命名数量、剩余问题、人工确认点和 Gate 结果。

## 命名规则

```text
统一使用英文 snake_case。
优先表达业务语义，其次表达结构职责。
不使用中文。
不使用默认 Figma 名称。
不使用无上下文 label。
不使用无交付意义 source_ 前缀。
不使用纯位置词或纯视觉词作为核心命名。
数字尾缀只允许用于真实重复项或资产序列。
```

## 常用命名

```text
{module}_section
{module}_container
{module}_wrapper
{module}_card
{module}_surface
{module}_panel
{module}_list
{module}_carousel_list
{module}_item_{n}
{module}_card_{n}
{module}_chip_{semantic}
{action}_action
{action}_button
{action}_cta
{action}_icon
{module}_fixed_cta
label
value
placeholder
helper_text
divider
button_bg
capsule_bg
container_bg
icon_container
```

## Harness Gate

```text
Layer Naming Harness Gate 通过条件：
- 目标范围内不存在默认 Figma 名称。
- 目标范围内不存在中文 frame-like 名称。
- 目标范围内不存在无上下文 label。
- 目标范围内不存在无交付意义 source_ 前缀。
- 命名统一使用英文 snake_case。
- 命名表达业务语义或结构职责。
- 本流程只改变 name，不改变视觉、布局、层级、样式、文字内容或业务语义。
- 扫描结果、剩余问题和人工确认点已写入 run record。
```

## 失败回路

```text
Layer Naming Harness Gate 未通过
→ 回到命名问题分类
→ 修正命名映射
→ 执行重命名
→ 命名复扫
→ 重新执行 Layer Naming Harness Gate
```

未通过 Gate 时，不得进入 Auto Layout 回填。
