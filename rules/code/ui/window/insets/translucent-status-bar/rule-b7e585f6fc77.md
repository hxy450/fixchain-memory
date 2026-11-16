# 源端背景铺到状态栏后、只把顶栏下移时，目标在背景节点本身加 expandSafeArea(TOP)

审的是：代码
触发（任一种）：
- 读到：源码只给顶栏 updateLayoutParams { topMargin = 状态栏高度 }，背景铺在透明状态栏后面；写错的样子：背景节点写成「固定高度 + 状态栏高度」、文字列 padding top 为「状态栏高度 + N」，背景节点本身没有 .expandSafeArea，背景到不了状态栏
- 写错的样子：路由页根 Column 没有 expandSafeArea，却 .padding({ top: 状态栏高度 }).backgroundColor(页面底色)，状态栏下露出一条单独的色带
适用范围：设计要求背景、色块或工具栏底色延伸到状态栏后面，页面由 NavDestination 承载、内容从状态栏下沿排布时
做法：
- 在要铺到状态栏的那个背景节点本身加 .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])（卡里用的是 [SafeAreaType.SYSTEM, SafeAreaType.CUTOUT]）；背景图对齐顶部，文字列再用状态栏高度做 padding 避让
- 整页底色都要延伸时，在根节点加 .expandSafeArea([SafeAreaType.SYSTEM, SafeAreaType.CUTOUT])，底色设成状态栏处该显示的颜色，保留顶部 padding 给内容避让
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 背景 Stack 加 .expandSafeArea([SafeAreaType.SYSTEM, SafeAreaType.CUTOUT], [SafeAreaEdge.TOP])、文字列保留状态栏高度避让后沉浸效果正确；只在页面根和宿主上加没用：修复后的写法（出处：卡里修好并验证过）
- expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>): T：扩展安全区的签名（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea）
- expandSafeArea 只作用于当前组件，不向父组件或子组件传递；组件边界与安全区重合时才能延伸进去：必须加在背景节点本身，且它要贴着页面顶（出处：ts-universal-attributes-expand-safe-area.md，expandSafeArea 说明）
- 设置固定宽高时，扩展方向只支持 [SafeAreaEdge.TOP, SafeAreaEdge.START]，扩展后组件尺寸不变：固定高度的背景节点向上扩展可行（出处：ts-universal-attributes-expand-safe-area.md，expandSafeArea 说明）
- SafeAreaType.SYSTEM = 0（状态栏和导航条）、CUTOUT = 1；SafeAreaEdge.TOP = 0：枚举取值（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SafeAreaType、SafeAreaEdge）
来源：1 张卡，1 个应用
- case-6597b7f7858db941262c（android-train-ticket-vest7）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 诊断；取值 1 ← 诊断
