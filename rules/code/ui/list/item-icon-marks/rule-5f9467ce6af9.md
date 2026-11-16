# selectable 行只在选中时显示尾部勾选 Icon 时，按同一条件渲染勾选图，不用 Radio

审的是：代码
触发（任一种）：
- 读到：Row 带 Modifier.selectable(selected) { … }，函数体里只有 if (selected) 时才出现尾部 Icon(…, tint = …) 勾选图；写错的样子：写成了 Radio({ group: … })，每一行都有圆圈；或者勾选图没按 selected 条件出现
适用范围：把 Compose 里用条件尾部图标表示单选的行迁成 ArkUI 时
做法：
- 先在目标工程的 media 里确认有源端那张勾选图（没有就迁过来）
- 写成 if (selected) { Image($r('app.media.<勾选图>')).fillColor(<源 tint 对应的颜色资源>) } else { 同宽高的 Blank 占位 }，不改成 Radio
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(value: ResourceColor): ImageAttribute，只对 SVG 图生效：勾选图按源 tint 上色；位图格式时 fillColor 不起作用（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- (min?: number | string): BlankAttribute：未选中行的占位组件（出处：鸿蒙 SDK 的 ets/component/blank.d.ts，BlankInterface）
- 只有选中行显示 Image(勾选图).fillColor(品牌色)，未选中行用同尺寸 Blank 占位：修复后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 勾选图的资源和格式：目标工程 resources/base/media/ 下按源端 drawable 名找；源端在 res/drawable*/ 下；确认存在且是 SVG；不是 SVG 时 fillColor 不生效，要换成 SVG 或用已带颜色的图
未核实：卡里记的环境没写鸿蒙 SDK 版本，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-40b9281a2c93eda1c790（Jetsnack）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
