# Compose Brush 渐变迁 linearGradient 时，查清色序、端点和 tileMode 再写参数

审的是：代码
触发（任一种）：
- 读到：Compose Brush.linearGradient / horizontalGradient 的 colors、端点（start / end、startX / endX）和 tileMode；写错的样子：目标 .linearGradient(...) 的方向、色阶位置、平铺是估的，或换成了纯色、单色 .border
适用范围：Compose 线性渐变刷迁成 ArkUI linearGradient（背景或描边环）时
做法：
- 读色序：只给调色板名的，到主题 Kotlin 文件的调色板对象按名找 listOf(...) 的 Color(0x…)；渐变描边封装成 Modifier 的，看它 border 的默认参数
- 读方向和长度：没写 start / end 时沿组件 (0,0)→(w,h)，按实测宽高算 angle；写了端点按端点距离定周期，stop 按「周期 / 组件渐变线长」缩放；Mirror 写成回文 colors
- 写成显式 .linearGradient({ angle 或 direction 二选一, colors: [[颜色, 位置], …] })，末 stop < 1 时加 repeating: true
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LinearGradientOptions：direction 默认 GradientDirection.Bottom，angle 默认 180，colors: Array<[ResourceColor, number]>：不写方向是自上而下；colors 每项是 [颜色, 位置]（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions）
- direction 在 angle 不是 undefined 时不生效；colors 的位置取值 [0, 1.0]，0 是渐变开始处，1.0 是结束处：angle 和 direction 只写一个；位置是相对组件自身渐变线长的比例（出处：ts-universal-attributes-gradient-color.md，LinearGradientOptions 对象说明）
- repeating 默认 false：要平铺必须显式写 repeating: true，且末 stop 小于 1（出处：鸿蒙 SDK 的 ets/component/common.d.ts，LinearGradientOptions.repeating）
针对本应用要查的：
- 调色板里这个渐变名对应的色序：源工程主题 Kotlin 文件里调色板对象的构造，按渐变名找它指向的 listOf(...)，再找各元素的 Color(0x…) 常量；按 listOf 的顺序依次写进 colors，每个元素换成同值的 $r 令牌
- 渐变描边的边宽和颜色：源工程里定义这个渐变描边 Modifier 的 Kotlin 文件（按 Modifier 扩展函数名找），看 border(width = …, brush = …) 的默认参数；边宽取默认参数或调用处传的值，颜色取 Brush.linearGradient 的 colors
未核实：源端多于两个颜色时 Compose 按等分分布、目标位置取 i/(n-1)，未核实
来源：3 张卡，1 个应用
- case-40c445e1fb0a99ce0a72（Jetsnack）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3
- case-4a0392021e915d5b60d1（Jetsnack）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-f4f67940ef03672d639c（Jetsnack）：做法第 2 步 ← 建议 1、建议 2；做法第 3 步 ← 建议 1
