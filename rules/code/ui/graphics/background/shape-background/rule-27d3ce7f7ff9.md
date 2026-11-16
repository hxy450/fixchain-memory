# 布局引用 shape drawable 和列表项布局时，照其中的颜色、各角圆角、描边、外边距写属性

审的是：代码
触发（任一种）：
- 读到：控件的 android:background 引用 @drawable/… 形状（<shape> 里有 <solid>、<corners android:topLeftRadius …>、<stroke>），列表项布局带 android:layout_margin，输入框带起始的搜索图标；写错的样子：ArkUI 里背景色和圆角是猜的：四角写成同一个圆角、没有 .border 描边、没有搜索图标；网格只设了间距（gutter）而项上没有 .margin
适用范围：迁移布局时，控件背景引用 shape drawable、列表项由单独的 item 布局定义的
做法：
- 写之前先读布局引用的 drawable 和 item 布局 XML：<solid android:color> → .backgroundColor(…)；<corners> 各角 → .borderRadius({ topLeft, topRight, bottomLeft, bottomRight })；<stroke android:width android:color> → .border({ width, color })；item 的 android:layout_margin → 项上的 .margin(…)
- 写完后才读到的颜色、圆角、外边距，回写到已经生成的片段里
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T：组件圆角，四角不同时传 BorderRadiuses（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- BorderRadiuses = { topLeft?: Length, topRight?: Length, bottomLeft?: Length, bottomRight?: Length }：四个角各自的圆角，对应 <corners> 的 topLeftRadius / topRightRadius / bottomLeftRadius / bottomRightRadius（出处：鸿蒙 SDK 的 ets/component/units.d.ts，BorderRadiuses）
- border(value: BorderOptions): T：组件描边，对应 <stroke> 的 width 和 color（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.border）
- BorderOptions.radius?: BorderRadiuses | Length | LocalizedBorderRadiuses：同族接口：描边和圆角可以在同一个 .border({ width, color, radius }) 里写（出处：鸿蒙 SDK 的 ets/component/units.d.ts，BorderOptions.radius）
- margin(value: Margin | Length | LocalizedMargin): T：组件外边距，对应 item 布局的 android:layout_margin（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- <corners> 的 radius、topLeftRadius、topRightRadius、bottomLeftRadius、bottomRightRadius，format 是 dimension：源端四角可以各自不同，要逐角读（出处：Android SDK 平台资源 data/res/values/attrs.xml，DrawableCorners（按应用的 compileSdk 取对应平台））
- <stroke> 的 width、color、dashWidth、dashGap：源端描边的四个属性（出处：Android SDK 平台资源 data/res/values/attrs.xml，GradientDrawableStroke（按应用的 compileSdk 取对应平台））
- 改成按 drawable 的颜色写分组标题背景、白底分段圆角、描边搜索框加图标、项 5dp 外边距后与源一致：修好的结果：drawable 和 item 布局里的每个值都要落到属性上（出处：卡里修好并验证过）
针对本应用要查的：
- 背景形状的颜色、各角圆角、描边，和列表项的外边距、高度：源工程 res/drawable 下被 android:background 引用的 shape XML，res/layout 下列表项的布局 XML；<solid> 取 android:color，<corners> 逐角取半径，<stroke> 取 width 和 color；列表项取 android:layout_height 和 android:layout_margin
来源：1 张卡，1 个应用
- case-7d027e7b2cd42e741308（android-train-ticket-vest7）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 8 ← 诊断
