# 源端 Start/End 边距时目标写 start/end 的 LengthMetrics，不转 left/right

审的是：代码
触发（任一种）：
- 读到：源布局 XML 里有 android:paddingStart / paddingEnd / layout_marginStart / layout_marginEnd，或 layout_gravity="start|end"；写错的样子：对应组件写成 .padding({ left, right }) / .margin({ right }) 这类物理键
- 读到：Compose 里 Modifier.padding(end = …) / padding(start = …)，Manifest 里 android:supportsRtl="true"；写错的样子：写成 .margin({ right: … }) / .padding({ left: … })，全工程没有 LengthMetrics
适用范围：源清单 android:supportsRtl="true"，把 XML 布局或 Compose 的逻辑方向内外边距迁成 ArkUI padding/margin 时
做法：
- 源端是 Start/End 的写 .padding({ top: LengthMetrics.vp(t), start: LengthMetrics.vp(<start>), end: LengthMetrics.vp(<end>) })，margin 同理；同一对象各边都用 LengthMetrics（从 @kit.ArkUI 导入）；源端只给 Left/Right 的才用 left/right
- 写完后在目标文件里搜 left: 和 right:，逐条回对源端那个属性是不是 Start/End
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- padding(value: Padding | Length | LocalizedPadding): T；margin(value: Margin | Length | LocalizedMargin): T：padding/margin 同时接受物理键的 Padding/Margin 和逻辑键的 LocalizedPadding/LocalizedMargin（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding、CommonMethod.margin）
- LocalizedPadding { top?: LengthMetrics; end?: LengthMetrics; bottom?: LengthMetrics; start?: LengthMetrics }；LocalizedMargin = LocalizedPadding：逻辑键对象里四个边都是 LengthMetrics，改成 start/end 时 top/bottom 也要写成 LengthMetrics（出处：鸿蒙 SDK 的 ets/component/units.d.ts，LocalizedPadding、LocalizedMargin）
- static vp(value: number): LengthMetrics：把源端 dp 数值照搬成 vp 包成 LengthMetrics（出处：鸿蒙 SDK 的 ets/api/arkui/Graphics.d.ts，LengthMetrics.vp）
- 方向类通用属性要支持镜像，用 start/end 入参类型替换 left/right、x/y：left/right 是绝对方向，RTL 下不镜像（出处：arkts-internationalization.md，使用镜像能力 / 使用约束）
- paddingStart、paddingEnd、layout_marginStart、layout_marginEnd 的 format 是 dimension：源端是起始/结束边的尺寸，带 dp 单位（出处：Android SDK 平台资源 data/res/values/attrs.xml，View 的 paddingStart、ViewGroup_MarginLayout 的 layout_marginEnd（按应用的 compileSdk 取对应平台））
- safeAreaPadding(paddingValue: Padding | LengthMetrics | LocalizedPadding): T：同族接口：CommonMethod.safeAreaPadding 也接受 LocalizedPadding（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.safeAreaPadding）
- padding(value: Padding | Dimension | LocalizedPadding): BottomTabBarStyle：同族接口：BottomTabBarStyle 的内边距（出处：鸿蒙 SDK 的 ets/component/tab_content.d.ts，BottomTabBarStyle.padding）
针对本应用要查的：
- 源应用是否声明了 RTL 支持：源工程 AndroidManifest.xml 的 application 标签，按 android:supportsRtl 找；值为 true 时 Start/End 随布局方向解析；没写或 false 时安卓按 LTR 兼容模式解析
未核实：case-927e26bb7b18f83f2f38 的环境是 API 24，本机按 API 23 的声明核实
来源：2 张卡，2 个应用
- case-01833db0536ba02ed2ce（Cofi）：做法第 1 步 ← 建议 4、诊断
- case-927e26bb7b18f83f2f38（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
