# 完整复刻要字符级末行省略时，用 measureTextSize 二分预截「前缀+…」，只换折叠态

审的是：代码
触发（任一种）：
- 读到：Compose 多行正文 `Text(maxLines = N, overflow = TextOverflow.Ellipsis)`（或 `android:ellipsize`），决策台账要求完整复刻（D0）；写错的样子：目标只写 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })`，折叠态末行按词截断、接「 ...」，和安卓按字符填满接「…」不一致
适用范围：D0 为完整复刻、多行正文折叠态末行要和安卓一样按字符截断时
做法：
- 在 Text 上用 `.onSizeChange((oldValue, newValue) => …)` 回读换行宽度 w，存进状态变量
- 用 measureTextSize({ textContent, constraintWidth: `${w}vp`, fontSize, fontWeight, lineHeight, wordBreak: WordBreak.BREAK_WORD })（字体参数与 Text 同一套）二分出排成不超过 N 行的最长「前缀 + '\u2026'」，折叠态显示它
- 只替换折叠态文本；展开态和首帧（宽度还没测出）保留原文加 `.maxLines(N).textOverflow({ overflow: TextOverflow.Ellipsis })` 兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- measureTextSize(options: MeasureOptions): SizeOptions（MeasureUtils 的方法），返回的宽高单位是 px：量一段文字在给定宽度下排出来的宽高；先用 getMeasureUtils() 取实例（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- getMeasureUtils(): MeasureUtils：从 UIContext 取 MeasureUtils 实例（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getMeasureUtils）
- static measureTextSize(options: MeasureOptions): SizeOptions，@deprecated since 18，@useinstead MeasureUtils#measureTextSize：同族接口：@ohos.measure 里的旧静态方法，API 18 起改用 MeasureUtils（出处：鸿蒙 SDK 的 ets/api/@ohos.measure.d.ts，MeasureText.measureTextSize）
- MeasureOptions：textContent、constraintWidth、fontSize、fontWeight、fontFamily、lineHeight、maxLines、wordBreak：测量参数要和 Text 上实际用的字体参数一致（出处：鸿蒙 SDK 的 ets/api/@ohos.measure.d.ts，MeasureOptions）
- onSizeChange(event: SizeChangeCallback): T；SizeChangeCallback = (oldValue: SizeOptions, newValue: SizeOptions) => void：组件因布局更新改变尺寸时回调，用它拿到换行宽度（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onSizeChange）
- 省略号常量写 '\u2026'：和安卓的单个省略号字符一致（出处：卡里修好并验证过）
- 预截后折叠态末行按字符截断、无前导空格，复验通过；未测出宽度时回退原文 + maxLines/Ellipsis：修好后的效果（出处：卡里修好并验证过）
针对本应用要查的：
- 正文 Text 实际用的字体参数：目标工程里这段 Text 用的 Typography 或样式定义，以及源端 Compose 的 TextStyle；把字号、字重、字体、行高原样填进 MeasureOptions，constraintWidth 用 onSizeChange 回读的宽度
未核实：卡里没写明 measureTextSize 用的是 MeasureUtils 还是旧的 MeasureText；ArkUI ellipsisMode(END) 或 wordBreak(BREAK_ALL) 能否做到字符级末行，卡里没有试验记录
来源：1 张卡，1 个应用
- case-b57f1b660260b8843ce3（Jetsnack）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3；取值 6 ← 诊断；取值 7 ← 诊断
