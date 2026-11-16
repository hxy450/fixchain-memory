# 重复 XML 元素抽成 @Builder 时，逐实例不同的 layout_marginTop 等作为参数传入

审的是：代码
触发（任一种）：
- 读到：源布局 XML 里几个同类元素（如分组标题 TextView）各自写了不同的 android:layout_marginTop，按钮写了 android:layout_marginTop，装饰图写了 android:layout_marginVertical；写错的样子：目标端把它们抽成没有边距参数的 @Builder，各实例都没有或都是同一个上间距；或按钮写成和 XML 不同的 .margin({ top: ... }) 数值
适用范围：把安卓布局 XML 里重复的元素在 ArkTS 里抽成 @Builder 复用时，以及写完后核对边距和尺寸
做法：
- @Builder 加上逐实例不同的属性参数，如 @Builder sectionTitle(text: string, topMargin: number)，内部写 .margin({ top: topMargin })，调用处按各元素的 layout_marginTop 数值传入
- 写完逐条对照 XML 的 margin 和尺寸：layout_marginTop=NNdp 写 .margin({ top: NN })，layout_marginVertical 写 .margin({ top: NN, bottom: NN })，不自行折算或省略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- margin(value: Margin | Length | LocalizedMargin): T，默认值 0：组件外边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.margin）
- Margin = Padding = { top?: Length; right?: Length; bottom?: Length; left?: Length }：按边分别给值（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Padding / Margin）
- 数值不带单位时默认单位 vp（屏幕密度相关像素）：.margin({ top: 30 }) 即 30vp（出处：ts-pixel-units.md，基本像素单位）
- layout_marginVertical 等同于 layout_marginTop 和 layout_marginBottom 取同一值；与它们同时写时 layout_marginVertical 优先，layout_margin 又优先于它：源端这几个边距属性的取值顺序（出处：Android SDK 平台资源 data/res/values/attrs.xml，ViewGroup_MarginLayout 的 layout_marginVertical（按应用的 compileSdk 取对应平台））
- XML 的 layout_marginTop=30dp、66dp 在目标端写成 .margin({ top: 30 })、.margin({ top: 66 }) 后间距和安卓一致：dp 数值照搬成 vp 数值（出处：卡里修好并验证过）
- padding(value: Padding | Length | LocalizedPadding): T：同族接口：内边距，同样按边给值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
来源：1 张卡，1 个应用
- case-bd76c218ac0773e443e3（android-train-ticket-vest7）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；取值 5 ← 诊断
