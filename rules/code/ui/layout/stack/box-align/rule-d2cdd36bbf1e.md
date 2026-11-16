# Box 里各占自身高度的悬浮顶栏、底栏，迁到 Stack 时逐个定位，不合并成全屏 Column

审的是：代码
触发（任一种）：
- 读到：Compose `Box(fillMaxSize)` 里叠在滚动内容上、只占自身高度的 `Modifier.zIndex` 顶栏和 `Modifier.align(Alignment.BottomCenter)` 底栏；写错的样子：两栏被并进 Stack 里一个 `Column().width('100%').height('100%')`，中间 `Blank().layoutWeight(1)` 撑开
- 读到：Box 子项用 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高（如 Divider 加 heightIn 的行）；写错的样子：Stack 里新增 Column() { Blank(); 底栏 }.width('100%').height('100%') 作定位壳
适用范围：源端 Box / FrameLayout 里按内容定高的悬浮顶栏、底栏，迁成 ArkUI Stack 子项时
做法：
- 每个悬浮栏单独作 Stack 子项，宽 '100%'、高随内容，不铺满全屏，逐个定位（也可用 Stack({ alignContent }) 或 offset）
- 顶栏写 Row(...).width('100%').position({ x: 0, y: 0 }).zIndex(<高于内容>)
- 底栏写 .width('100%').position({ bottom: 0, left: 0 })，或在 RelativeContainer 里 .alignRules({ bottom: { anchor: '__container__', align: VerticalAlign.Bottom } })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- position(value: Position | Edges | LocalizedEdges): T（Edges 出自声明 @since 12）：相对父组件内容区的绝对定位；Position 按内容区左上角定位，传 Edges 可按 bottom 边定位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.position）
- position 适用于置顶显示、悬浮按钮等在父组件中位置固定的场景：悬浮顶栏用 position 定位是文档给的用法（出处：ts-universal-attributes-location.md，position）
- interface Edges { top?: Dimension; left?: Dimension; bottom?: Dimension; right?: Dimension }：按四条边给偏移（出处：鸿蒙 SDK 的 ets/component/units.d.ts，Edges）
- zIndex(value: number): T：同一容器内兄弟组件的层级，值大的显示在上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex）
- alignRules(value: AlignRuleOption): T；AlignRuleOption.bottom?: VerticalAlignParam；以容器作锚点写 { anchor: "__container__", align: VerticalAlign.Top }，底部改用 VerticalAlign.Bottom：RelativeContainer 里按锚点对齐的写法（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.alignRules；ts-container-relativecontainer.md，示例1（以容器和容器内组件作为锚点进行布局））
- StackOptions.alignContent 默认 Alignment.Center：Stack 的所有子项共用一个对齐方式，不逐个定位时都居中（出处：鸿蒙 SDK 的 ets/component/stack.d.ts，StackOptions.alignContent）
- offset(value: Position | Edges | LocalizedEdges): T：同族接口：CommonMethod.offset，相对自身原位置偏移（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.offset）
- 顶栏 position({ x: 0, y: 0 }) + zIndex 后留在顶部，下层 Scroll 和 Swiper 照常滑动：逐个定位、不铺满全屏的写法（出处：卡里修好并验证过）
未核实：底栏的 position 的 bottom 边和 RelativeContainer 两种锚定写法 case-7d423b2bf98cdaabda82 里没有上机验证，返修实际用的是给返回按钮加 zIndex
来源：2 张卡，2 个应用
- case-7d423b2bf98cdaabda82（Jetsnack）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-9b8bac5680e58daada3a（青商城）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；取值 8 ← 诊断
