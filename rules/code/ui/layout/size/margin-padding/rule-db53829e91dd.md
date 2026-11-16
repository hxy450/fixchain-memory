# 源容器自身的 layout_margin，写在对应 Stack/Row/Column 的 .margin 上，不能漏

审的是：代码
触发（任一种）：
- 读到：源 XML 的非叶子容器（如 FrameLayout）上写了 android:layout_marginTop 等外边距；写错的样子：对应的 Stack / Row / Column 没写 .margin({ top: … })，只写了它子控件的边距
适用范围：按源布局 XML 转写含嵌套容器的弹窗或页面时
做法：
- 列出源 XML 中所有带 layout_margin* / padding* 的容器，逐个在输出里找到对应容器的 .margin({ top: <dp 值> }) / .padding(...)，dp 数值照搬为 vp
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- margin(value: Margin | Length | LocalizedMargin): T：组件外边距，默认 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- padding(value: Padding | Length | LocalizedPadding): T：组件内边距，默认 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- Length 为 number 时默认单位 vp：源端 dp 值照搬数值（出处：ts-types.md，Length）
- 头部容器补 .margin({ top: 16 }) 后与源布局一致：漏掉的是容器自身的外边距（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-89e7732b8a374944c6b2（免费来电多多）：做法第 1 步 ← 建议 3、诊断；取值 4 ← 诊断
