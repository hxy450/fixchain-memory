# 带 progressDrawable 的 ProgressBar，Progress 高度和颜色取该 drawable

审的是：代码
触发（任一种）：
- 读到：布局 XML 里 ProgressBar 写 android:progressDrawable="@drawable/…"；写错的样子：对应的 Progress 自定了 .height(4) 一类没有出处的高度，.backgroundColor(...) 沿用工程里已有的、含义不同的颜色资源
适用范围：带自定义 progressDrawable 的水平 ProgressBar 迁成 ArkUI Progress（ProgressType.Linear）时
做法：
- Progress({ value, total, type: ProgressType.Linear }).height(<drawable 高度，dp 写成 vp>).backgroundColor(<background 项的颜色>)；轨道色新建颜色资源，不沿用含义不同的已有颜色
- .color(...) 取 progress 项的颜色；是渐变时写 .color(new LinearGradient([{ color: <startColor>, offset: 0 }, { color: <endColor>, offset: 1 }]))
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 修好后 .height(12) 取自 drawable 高度，轨道色新建资源取 drawable 的轨道色：高度和轨道色照源端 drawable（出处：卡里修好并验证过）
- Progress 重写了通用属性 backgroundColor，加在 Progress 上设的是进度条底色：轨道色就写在 Progress 的 .backgroundColor 上（出处：ts-basic-components-progress.md，属性）
- color(value: ResourceColor | LinearGradient): ProgressAttribute<Type>：进度条前景色，可传纯色或渐变（出处：鸿蒙 SDK 的 ets/component/progress.d.ts，ProgressAttribute.color）
- API version 23 起 Linear、Capsule 样式支持 LinearGradient 渐变；22 及以前传渐变会以默认主题色显示：目标 API 低于 23 时渐变不生效（出处：ts-basic-components-progress.md，color）
- constructor(colorStops: ColorStop[])；ColorStop 有 color: ResourceColor、offset: Length：LinearGradient 的构造（出处：鸿蒙 SDK 的 ets/component/data_panel.d.ts，LinearGradient.constructor、ColorStop）
- LinearStyleOptions.strokeRadius?: PX | VP | LPX | Resource，默认 strokeWidth / 2：线性进度条圆角，默认就是两端半圆（出处：鸿蒙 SDK 的 ets/component/progress.d.ts，LinearStyleOptions.strokeRadius）
- progressDrawable 的 layer-list 里 @android:id/background 是轨道、@android:id/progress 是进度层：源端颜色从这两项读（出处：Android SDK 平台资源 data/res/drawable/progress_horizontal.xml，layer-list 的 @android:id/background 和 @android:id/progress 项（按应用的 compileSdk 取对应平台））
- trackColor(value: ResourceColor | LinearGradient): SliderAttribute：同族接口：Slider 的轨道色同样可传渐变（出处：鸿蒙 SDK 的 ets/component/slider.d.ts，SliderAttribute.trackColor）
针对本应用要查的：
- drawable 的高度、轨道色、进度色或渐变：源工程 res/drawable 下 progressDrawable 引用的那个 XML；高度读 <size android:height> 或 item 的 android:height；background 项读 <solid android:color>；progress 项读 <gradient android:startColor / endColor> 或 <solid>
未核实：渐变进度色卡里没上机验证（修复时前景仍用主题色）；只设 .height 而不设 LinearStyleOptions.strokeWidth（默认 4vp）时条的粗细，卡里没单独核对
来源：1 张卡，1 个应用
- case-9a108f83b6eca279b883（android-train-ticket-vest7）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
