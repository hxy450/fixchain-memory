# ImageView 用 tint 给渐变着色时，用容器 linearGradient，不用 fillColor

审的是：代码
触发（任一种）：
- 读到：ImageView 带 app:tint（如 ?android:attr/colorBackground 这类主题色），android:src 是白到透明的渐变 shape；写错的样子：目标写成 Image($r('app.media.…')).fillColor(…) 给渐变 SVG 着色；深色主题下留下一条白色亮带
适用范围：安卓用 tint 给渐变 drawable 着色做装饰层（背景渐变、遮罩），迁成 ArkUI 时
做法：
- 在承载装饰层的容器上写 .linearGradient({ colors: [[$r('app.color.<主题色>'), 0], [$r('app.color.<主题色>_transparent'), 1]] })，起点取 tint 的主题色，终点取它的透明变体，方向照源 shape 的渐变方向
- 不依赖 SVG + fillColor；改用 linearGradient 后删掉不再引用的渐变 SVG
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- linearGradient(value: LinearGradientOptions): T：组件背景的线性渐变（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
- colors: Array<[ResourceColor, number]>；angle 默认 180；direction 默认 GradientDirection.Bottom：LinearGradientOptions 的颜色断点（颜色，位置 0–1）和方向默认值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions）
- fillColor(value: ResourceColor): ImageAttribute，只对 SVG 图片生效：叠加在图片上的填充色（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- fillColor 不会改写 SVG 里 url(#grad) 的渐变填充，白到透明的渐变仍是白色：这就是不能用 fillColor 表达 tint 的原因（出处：卡里修好并验证过）
- linearGradient(options: Optional<LinearGradientOptions>): T：同族接口：CommonMethod 上可传 undefined 关闭渐变的重载（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.linearGradient）
针对本应用要查的：
- tint 引用的主题色在源端的取值：源工程 Activity / 应用主题的 colorBackground 覆盖；没有覆盖时查 Android SDK 平台资源 data/res/values/themes_material.xml 里父主题的 colorBackground（按应用的 compileSdk 取对应平台）；顺着 @color/… 解析到具体色值，作为目标 base 主题色；深色主题取对应深色主题的值。例：Theme.Material 下是 @color/background_material_dark
来源：1 张卡，1 个应用
- case-5b7b00a1deb25ed0b8d3（AntennaPod）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 4 ← 诊断、建议 3
