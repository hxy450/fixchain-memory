# 源端 48dp 按钮带 padding 时，目标宽高写 48 再加 padding，不写成 24 加 padding

审的是：代码
触发（任一种）：
- 读到：按钮 View 的 android:layout_width / layout_height 为 48dp，另有 android:padding="12dp"；写错的样子：目标写成 .width(24).height(24).padding(12)，把 padding 当成尺寸之外另加
适用范围：源端控件尺寸和 padding 同时写明、迁成 ArkUI 组件时
做法：
- 目标照源端写 .width(48).height(48).padding(12)：安卓 layout 尺寸已包含 padding
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- padding 把内容从 View 边缘往里推（左 padding 为 2 时内容离左边 2 像素）：安卓的 layout_width/height 是含 padding 的外框尺寸（出处：android.view.View（类注释 Size, padding and margins））
- 按钮改为 48×48 加 padding 12 后与源端一致：目标同样按外框尺寸写宽高（出处：卡里修好并验证过）
未核实：鸿蒙声明和文档里没找到「宽高包含 padding」的明确原文，按卡里返修结果写
来源：1 张卡，1 个应用
- case-4f627840679361f165a3（AntennaPod）：做法第 1 步 ← 诊断；取值 2 ← 诊断
