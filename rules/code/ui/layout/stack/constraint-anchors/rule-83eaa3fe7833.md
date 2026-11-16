# 0dp×0dp 加 dimensionRatio 夹在上下锚点间时，边长取可用宽高的较小者

审的是：代码
触发（任一种）：
- 读到：ConstraintLayout 子项 android:layout_width="0dp"、android:layout_height="0dp"，带 app:layout_constraintDimensionRatio，上下分别锚在相邻子项上（layout_constraintTop_toBottomOf / layout_constraintBottom_toTopOf）；写错的样子：目标在 .layoutWeight(1) 的 Row / Column 里写 Image(...).width('100%').aspectRatio(1)，没有高度上限，源端的上下 margin 留在 Image 上
适用范围：把 ConstraintLayout 里宽高都为 0dp、带比例、上下都有锚点的子项改写成 layoutWeight 容器里的比例子项时
做法：
- 边长按 min(可用宽, 可用高) 定，不凭屏幕估算认定高度够：高受限时写 .height('100%').aspectRatio(<宽/高>)，并限制宽度不超过可用宽
- 源端比例子项的上下 margin 放到承担 .layoutWeight(1) 的容器上，不留在比例子项自身
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aspectRatio(value: number): T：宽高比，aspectRatio = width / height（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.aspectRatio）
- 只设 width 和 aspectRatio 时 height = width / aspectRatio；只设 height 和 aspectRatio 时 width = height * aspectRatio；三者都设时 height 不生效：宽驱动还是高驱动由写了哪一边决定（出处：ts-universal-attributes-layout-constraints.md，aspectRatio）
- constraintSize 的优先级高于 aspectRatio：限宽时 constraintSize 的 maxWidth 先于比例生效（出处：ts-universal-attributes-layout-constraints.md，aspectRatio）
- 宽驱动 width('100%').aspectRatio(1) 时 Image 高超过 layoutWeight 容器；改成 height('100%').aspectRatio(1)、上下 margin 移到容器后不溢出：修复前后量到的布局（出处：卡里修好并验证过）
- layout_constraintDimensionRatio 的 format 是 string：源端比例写成字符串（如「1:1」），目标 aspectRatio 要的是宽除以高的数值（出处：androidx.constraintlayout:constraintlayout 包内 res/values/values.xml，layout_constraintDimensionRatio（按应用依赖的版本））
未核实：高驱动不一定是所有屏幕下的唯一正确形态，源端封面的实际边长没有精确测得；卡里的观察出自 HarmonyOS 6.1.1(24)，本机核对声明用的是 API 23
来源：1 张卡，1 个应用
- case-50467dd451cd7c5be566（免费来电多多）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
