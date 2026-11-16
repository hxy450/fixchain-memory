# 实现列表或输入行时，按源 item XML 逐项取尺寸和可选入口，不照搬工程里的相似行

审的是：代码
触发（任一种）：
- 读到：源 item XML 写了 android:layout_height、android:layout_marginBottom、paddingStart、圆角背景、android:textSize，另有默认 android:visibility="gone"、由数据决定是否显示的可选入口；写错的样子：目标行照搬工程里已有相似行的 .height / .margin({ top }) / .borderRadius / .padding / .fontSize，和 item XML 不一致，或没有按数据显示可选入口
适用范围：把 Android 列表项、输入行（item XML 加代码里按数据动态添加）落成 ArkUI 组件时
做法：
- 按源 item XML 逐项取高度、外边距方向（top 还是 bottom）、内边距、圆角、字号，以及可选入口的显示条件（如按数据字段决定显隐）
- 复用工程内已有相似行时，先把它和源 XML 对一遍，不把未核实的旧值当模板
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 修好后改为高 35、底部间距 14、圆角 6，文案库入口 padding 14 / 字号 12 并按数据字段显示：照源 item XML 和代码里的 setMargins 取值（出处：卡里修好并验证过）
针对本应用要查的：
- 行的尺寸和可选入口条件：源工程 res/layout 下这一行的 item XML，以及代码里 inflate 它后 setMargins、setVisibility 的地方；XML 读 layout_height、margin*、padding*、background 的圆角、textSize；代码读动态加的间距方向和入口显隐条件
来源：1 张卡，1 个应用
- case-cdc57384e71fa7c70345（组件岛Widget Island）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 1 ← 诊断
