# Compose Brush 线性渐变（Brush.linearGradient / horizontalGradient）

agent 会看到什么：读过的 Compose 源码里背景或描边用 Brush.horizontalGradient、Brush.linearGradient（带或不带 start / end、tileMode）；交回的换成了纯色或单色 .border，或 .linearGradient 的方向、色阶位置、repeating 是估的

## 通用查法

### Compose Brush 渐变迁 linearGradient 时，查清色序、端点和 tileMode 再写参数

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

## 规矩

- rule-b1848f7c0d3f｜源端背景是 Brush.horizontalGradient 时，目标写 linearGradient，不换成纯色｜读到：Compose 组件用 Modifier.background(Brush.horizontalGradient(colors)) 着色，外层 Surface(color = Color.Transparent)，colors 取自主题调色板里的某个渐变名；写错：目标只写 .backgroundColor($r('app.color.…')) 一个品牌纯色，没有 .linearGradient(...)
- rule-df5d46535afc｜Compose 默认对角渐变在宽高不等的组件上，angle 取 90+atan2(h,w)，不写 RightBottom｜读到：Compose 源码 Brush.linearGradient(colors) 没写 start / end（默认沿组件自身 (0,0) → (w,h)），用在宽高不等的胶囊、卡片上；写错：目标写 direction: GradientDirection.RightBottom 或 angle: 135，宽胶囊上渐变变成上下走向（上青下紫之类）
- rule-714976b7baf6｜Compose 端点渐变的面板比周期长时，linearGradient 的 stop 按周期/面板长缩放｜读到：Brush.horizontalGradient(colors, startX = …, endX = …, tileMode = …) 或 Brush.linearGradient(start = Offset(…), end = Offset(…))：渐变长度由端点距离给出，不是组件尺寸；写错：linearGradient({ direction / angle, repeating: true, colors }) 挂在为覆盖而加宽的面板上，colors 的位置仍从 0 铺到 1（末 stop 是 1）
- rule-7e7fcabcac73｜TileMode.Mirror 渐变端点平移时，写回文 stop 加 repeating 并平移面板，不转角度｜读到：Brush.linearGradient(colors, start = Offset(o, o), end = Offset(o + d, o + d), tileMode = TileMode.Mirror)，o 由 rememberInfiniteTransition / animateFloat 往复驱动，或 horizontalGradient 的 startX / endX 随滚动偏移；写错：linearGradient 的 angle 被做成 animateTo 往复旋转，colors 只有两色 0 / 1；或登记成「TileMode.Mirror 无对应」的降级
- rule-f81c27b8be42｜Compose 的 border 用 Brush 渐变时，目标用外层渐变加 padding 加内层实底拼描边环｜读到：Compose 源码 Modifier.border(width, Brush.linearGradient(colors), shape)，或封装它的渐变描边 Modifier（可能按状态显隐描边）；写错：目标写成单色 .border({ width: 1, color: 渐变首色 })，注释说「ArkUI border 只收单色，降级取首色」；或边宽和源 Modifier 的值不符
