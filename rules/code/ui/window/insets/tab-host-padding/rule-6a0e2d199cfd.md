# 补状态栏实色带时宿主是 Tabs，把 Tabs 包进带避让 padding 和底色的 Column，不挂在 Tabs 上

审的是：代码
触发（任一种）：
- 读到：源 Activity 或它的基类在 onCreate 里把状态栏设成实色；写错的样子：全屏布局的页面把顶部避让 .padding({ top: … }) 和 .backgroundColor(…) 直接挂在 Tabs（或 Swiper 这类由子页面铺满的容器）上，指望 padding 区透出色带
适用范围：ArkUI 页面全屏布局、靠顶部避让 padding 画出源端实色状态栏色带，且宿主是 Tabs、Swiper 这类由子页面铺满的容器时
做法：
- 外层写一个只承担避让的普通 Column：Column() { Tabs() { … }.height('100%') }.layoutWeight(1).padding({ top: 避让高度 }).backgroundColor(状态栏颜色)
- Tabs 本身去掉顶部 padding 和 backgroundColor，原来挂在 Tabs 上的 layoutWeight 移到外层 Column
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Tabs 上挂 padding(top) + backgroundColor 时真机顶部仍是白带；改成外层 Column 承担 layoutWeight(1)、padding(top) 和底色、Tabs 取 height('100%') 后顶部是连续色带：两种写法的真机对照（出处：卡里修好并验证过）
- padding(value: Padding | Length | LocalizedPadding): T：组件内边距，默认 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- backgroundColor(value: ResourceColor): T：组件背景色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundColor）
- layoutWeight(value: number | string): T：在父容器 Row、Column、Flex 的主轴上按权重分配空间，默认 0（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight）
未核实：Tabs 的 padding 区为何不显示自身背景（TabContent 满铺覆盖还是背景未绘制）卡里没有定论；卡里真机行为出自 API 22（HarmonyOS 6.0.2），本机声明是 API 23；Swiper、Navigation 是否同样不显示 padding 区背景卡里没有验证
来源：1 张卡，1 个应用
- case-6910f2ad1e73fb272245（企业安全培训）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
