# ui/layout/units

px/vp 运算域与整数几何公式

[上一级](../index.md)

## 本级经验

- [Compose Layout/MeasureScope 的整数几何公式运行在 px 域：spec 必须标注运算单位](lesson-ab7d9425cdfbe3070720.lesson.md)
  - 时机：规格提取阶段，把源码自定义 Layout / MeasureScope 里的整数除法或 .toInt() 截断翻译成 ArkTS 目标公式并标注运算单位时
  - 情境：源码在 constraints.maxWidth、placeable 宽高（Int px）上做 Kotlin 整数除法或 .toInt() 来分配槽宽/放置子项；目标侧宽度来自 onAreaChange（vp 浮点）或 measureText（px）。
  - 例外：源码公式作用于 Dp 值而非 constraints/placeable（如 56.dp、16.dp 常量）
- [落地源码整除公式的纯函数：参数名带 px/vp，调用处做 vp2px→公式→px2vp 往返](lesson-86a32ca71a1965302635.lesson.md)
  - 时机：界面实现阶段，用 onAreaChange / measureText 的返回值喂源码整数几何公式并写成纯函数时
  - 情境：公式含 floor/trunc/Int 除法；输入来自 onAreaChange（vp 浮点）或 measureText（px）。
