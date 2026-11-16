# 等分子项搬进自绘 Row/Column 时写 .layoutWeight(1)，不留 .width('100%')

审的是：代码
触发（任一种）：
- 读到：安卓水平 LinearLayout 没有静态子项，子项由代码以 LinearLayout.LayoutParams(0, MATCH_PARENT) 加 weight = 1f 等分；写错的样子：目标 Row + ForEach 里每个子项写 .width('100%')，没有 .layoutWeight(...)
- 读到：目标端原先由 Tabs（BarMode.Fixed）的 tabBar 或 Grid 槽位承载的子项写 .width('100%') / .height('100%')；写错的样子：子项搬进自绘 Row / Column + ForEach 后仍写 .width('100%')，N 个子项主轴宽度之和超过父宽
适用范围：把原由 Tabs、Grid 等容器分配槽位、或源端由 LinearLayout weight 等分的子项，放进自绘 Row / Column 时
做法：
- Row / Column 里的等分子项写 .layoutWeight(1)，删掉从旧容器槽位带来的 .width('100%')；源端 LayoutParams 主轴尺寸为 0、weight 为 N 的写 .layoutWeight(N)
- 组件来源写成「XML + 代码」、容器 XML 里没有静态子项时，子项主轴尺寸按代码里动态添加子项的 LayoutParams / weight 定
- 核算 Row 内 N 个子项主轴宽度之和不超过父宽（3 个 .width('100%') 必然溢出）；接入组件替换内置 tabBar 时对被接入组件同样复核
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- layoutWeight(value: number | string): T：按权重在父容器（Row、Column、Flex）主轴上分配尺寸，默认值 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight）
- layoutWeight 生效值大于 0 的子元素从主轴剩余空间按权重分配尺寸，分配时忽略元素本身的尺寸设置；仅在 Row/Column/Flex 中生效：写了 layoutWeight 后不必再写主轴的 width（出处：ts-universal-attributes-size.md，layoutWeight）
- 尺寸用百分比设置时，参考最近设置了固定大小的祖先节点的尺寸：Row 里的 .width('100%') 是整个父容器的宽，不是一个槽位的宽（出处：ts-universal-attributes-size.md，开头的说明）
- LinearLayout.LayoutParams(int width, int height, float weight)；weight 为 0 不拉伸，大于 0 的按比例分多余空间：源端等分子项写成宽 0 加 weight，对应目标的 layoutWeight（出处：android.widget.LinearLayout.LayoutParams#LayoutParams(int, int, float)、LinearLayout.LayoutParams#weight）
- 子项 .width('100%') 改成 .layoutWeight(1) 后三个页签同时可见：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 每个子项在主轴上的尺寸和权重：源工程里组件来源列出的 Java / Kotlin 代码文件，按 LayoutParams( 和 weight 找动态添加子项的那段；主轴尺寸为 0、weight 为 N 的写 .layoutWeight(N)；主轴是固定 dp 值的写 .width(该值)
来源：1 张卡，1 个应用
- case-ce3a01377b3cd72f23e3（实时公交）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 5 ← 诊断
