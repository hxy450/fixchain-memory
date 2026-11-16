# 源端单个字形当指示器时，目标按几何用 Circle 画；要用 Text 先量步进和位置

审的是：代码
触发（任一种）：
- 读到：源码在循环里 new TextView + setText(Html.fromHtml("&#8226;")) + setTextSize(大字号)，逐个 addView 作页码点；写错的样子：Row 里 ForEach 出 Text('•').fontSize(字号)，只靠字号对齐，没按源端步进、直径、垂直位置绘制
适用范围：组件实现阶段，绘制由源端文字字形充当的图形指示器时
做法：
- 按规格给的源端几何画图形：每点 Circle({ width: 直径, height: 直径 })，点间距按步进，放在与源端 TextView 同高的容器里按点心位置垂直定位
- 确要用 Text 画时，先在目标端量一次该字形在给定字号下的步进与位置（this.getUIContext().getMeasureUtils().measureTextSize({ textContent: '•', fontSize: 字号 }) 或截图），与源端几何不符就改成按几何画图形
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按源字体几何绘制 Circle（步进、直径、TextView 高度内垂直居中并裁剪、点心距顶的距离），各页面共用一个指示器组件：修好的画法（出处：卡里修好并验证过）
- Circle(value?: CircleOptions)；CircleOptions { width?: Length; height?: Length }：画圆点的组件，宽高取直径（出处：鸿蒙 SDK 的 ets/component/circle.d.ts，CircleInterface、CircleOptions）
- measureTextSize(options: MeasureOptions): SizeOptions，宽高单位都是 px：量字形在单行下的宽高；结果是 px，和 vp 比较前要换算（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- MeasureOptions { textContent: string | Resource; fontSize?: number | string | Resource; … }：量单个字形时传字符和字号（出处：鸿蒙 SDK 的 ets/api/@ohos.measure.d.ts，MeasureOptions）
- measureText(options: MeasureOptions): number，单位 px：同族接口：只量单行宽度（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureText）
来源：1 张卡，1 个应用
- case-5aab44999cc4e2080cd6（Privacy Friendly 2048）：做法第 1 步 ← 诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
