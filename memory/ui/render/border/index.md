# ui/render/border

draw-only 描边与容器测量

[上一级](../index.md)

## 本级经验

- [Compose 纯绘制描边落到 ArkUI 时，无显式宽高的容器不得直接 .border()：描边会计入测量](lesson-d3a4b7097bbf73279cb9.lesson.md)
  - 时机：规格映射与界面实现阶段，把 Compose Modifier.border 等 draw-only 修饰符落到尺寸由内容决定的 ArkUI 容器（Stack/Column）上时
  - 情境：源 border 由 Modifier.border(BorderStroke, shape) 在调用方已定尺寸的盒内侧绘制、不改测量尺寸；目标容器自身不设 width/height，尺寸由 @BuilderParam 内容决定。
  - 例外：目标容器自身已有显式 width/height（此时 .border 在盒内绘制不改尺寸）
