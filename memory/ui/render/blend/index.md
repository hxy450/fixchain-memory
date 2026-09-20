# ui/render/blend

Compose blendMode 叠色到 ArkUI 离屏混合的映射与预混

[上一级](../index.md)

## 本级经验

- [Compose 依赖画布已有内容的 blendMode 叠色，不能映射成 ArkUI 独立兄弟节点的离屏混合](lesson-80154b8ac09fefad5604.lesson.md)
  - 时机：规格提取阶段，为 Compose drawWithContent/drawRect(brush, blendMode) 这类依赖画布上已画内容的绘制修饰符确定 ArkUI 渲染映射、并决定是否定为 HARD 决策时
  - 情境：源码用 Modifier.drawWithContent { drawContent(); drawRect(Brush.linearGradient(colors), blendMode = Plus/Darken) } 给图标着色，效果依赖同一画布上已画好的底盘与字形（白底加法饱和仍白，只有深色字形像素变成渐变色）；目标侧渐变层、图标、底盘是 Stack 中并列的兄弟节点，准备用 .blendMode(mode, BlendApplyType.OFFSCREEN)。
  - 例外：源端 blendMode 的结果不依赖画布已有内容（如只对自身 alpha 起作用的 SRC_IN/DST_IN）
