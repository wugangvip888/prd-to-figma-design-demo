# Structure Mapping Rules

## 目标

定义 Wireframe 与采样端 Figma 来源之间的结构映射规则。

## 基本原则

```text
以线框图结构为目标，以采样端 Figma 来源为 UI 结构依据。
线框图必须保留 Page Frame → Module Frame → Control Frame → Element 层级后，才允许进入结构映射。
映射必须保留业务语义、信息层级、交互行为和状态差异。
视觉相似不等于同一组件。
采样端 Figma 来源中无关结构不得强行映射到新页面。
低置信度判断必须进入 mapping-review.md。
```

## 映射层级

```text
Page Frame：页面状态级映射。
Module Frame：业务模块级映射。
Control Frame：控件组合级映射。
Element：文本、图标、按钮、输入框等元素级映射。
Asset：图片、图标、装饰素材等可复用资产级映射。
```

映射要求：

```text
优先以 module_* 和 control_* 作为复用判断边界。
component_candidate 只能从稳定的 Module Frame 或 Control Frame 产生，不得从散落 Text、Rectangle 或无语义 Group 产生。
如果线框图存在大量散落节点，必须先回到 Wireframe 阶段整理，不得在 Structure Mapping 阶段临时发明组件边界。
采样端 Figma 来源的组件或组映射到线框图时，必须保留线框图的业务层级，不得为了贴合采样端结构打散 Module Frame 或 Control Frame。
不得只做 Page / Module 级映射；凡 P0/P1/P2 模块已映射到采样端来源，必须继续下钻到 Control / Element / Asset 级，除非采样端确无对应子结构，并在 mapping-review.md 写明原因。
Control 级映射必须记录：采样端节点 ID、节点类型、子元素类型、内部 padding、gap、关键子节点 x/y、宽高、对齐关系和目标控件对应关系。
Element 级映射必须记录：文本节点宽度策略、文本对齐方式、是否允许 hug/fixed/fill、图标是否存在可复用资产节点 ID、元素与父控件的相对 x/y。
Asset 级映射必须记录：图片、图标、装饰资产的采样端节点 ID、节点类型、资产 URL（如可读取）、复用方式、不可复用原因和目标节点归属。
渐变、资产 URL、间距数值、padding、gap、文本与背景的对齐关系均属于结构映射证据，必须传递给 Design System Extraction 和 Visual Spec。
```

## 禁止事项

```text
不在本阶段生成最终组件库。
不在本阶段生成最终 Token。
不在本阶段绘制高保真设计稿。
不因为视觉相似合并业务语义不同的结构。
不忽略 P0/P1/P2 关键模块的未映射原因。
不从散落节点、无语义 Frame 或纯视觉组合中直接生成组件候选。
不得只做模块级映射，跳过 control / element / asset 级映射。
不得在采样端存在可复用图标资产节点时，用字符或临时图形替代图标资产。
不得忽略渐变、资产 URL、padding、gap、x/y、宽高、对齐关系等可追溯数值证据的提取。
```
