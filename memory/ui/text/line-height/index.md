# ui/text/line-height

TextStyle.lineHeight 与 ArkUI lineHeight/lineSpacing 语义

[上一级](../index.md)

## 本级经验

- [TextStyle.lineHeight 与 ArkUI .lineHeight 同名不等价：Compose 单行文本盒不随 lineHeight 撑高](lesson-c67467bacd820624e4fc.lesson.md)
  - 时机：规格提取阶段，为排版令牌（TextStyle → 统一 AttributeModifier）写 Source→ArkTS 映射契约并定难度时
  - 情境：源是 Compose Material3 Typography，各 TextStyle 都带 lineHeight.sp；目标打算用一个 AttributeModifier 给全部 Text 套样式，页面里大量单行文本（Summary 行、卡片标题）与少量多行段落共用同一令牌。
  - 例外：目标只对多行段落施加 lineHeight、单行文本另有令牌
- [主题 modifier 与容器定高不得把 lineHeight 当单行文本盒高](lesson-89f5064b1f821945e706.lesson.md)
  - 时机：界面实现阶段，落地统一文本 AttributeModifier，或为包裹单行 Text 的容器（ArkUI 横向 List 等需显式交叉轴尺寸）推导固定高度时
  - 情境：目标工程有统一排版令牌（fontSize/lineHeight 数值来自 Type.kt），页面里有需要显式高度的行容器，容器内文本多为单行。
