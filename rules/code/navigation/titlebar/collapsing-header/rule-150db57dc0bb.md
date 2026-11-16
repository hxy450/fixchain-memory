# 源码按折叠态切换工具栏图标着色时，目标移植状态判定和两态颜色，不写死一色

审的是：代码
触发（任一种）：
- 读到：源码在 AppBarLayout 的 OnOffsetChangedListener 里按折叠进度切换工具栏图标着色（展开态白、折叠态主题色）；写错的样子：目标工具栏图标颜色写死一个次要色（如固定的 fillColor），不随滚动折叠态变化
适用范围：源端折叠头部的工具栏图标按 AppBarLayout 偏移切换颜色，目标用 Scroll 实现折叠头部时
做法：
- 移植折叠态判定和颜色映射：按滚动偏移算出折叠状态变量（@Local 或 @State），图标颜色在展开色和折叠色之间按它切换
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- fillColor(value: ResourceColor): ImageAttribute，只对 SVG 图片生效：给 Image 图标叠加填充色；位图图标设了也不变色（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.fillColor）
- 图标按折叠状态变量着色后，展开态白、折叠态主题色与源端一致：状态驱动着色是上机核对过的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 折叠判定的阈值和两态颜色：源工程里挂在 AppBarLayout.addOnOffsetChangedListener 上的着色代码；看它按什么偏移或比例判定折叠、两态各取什么颜色（主题属性还是颜色资源），照样写成目标的判定和颜色资源
来源：1 张卡，1 个应用
- case-9058ac868b6feb3a04e0（AntennaPod）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断
