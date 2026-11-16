# 源端根视图 padding 避让状态栏时，代码给画布容器加顶部 padding，不在布局输出上做 Y 平移

审的是：代码
触发（任一种）：
- 读到：源端 DecorView.setPadding(0, statusBarInsets.top, 0, 0)，内容 View 的 onSizeChanged(width, height) 直接调布局方程；skill 映射写 view.setPadding → padding({ top: … })；写错的样子：Canvas 铺满整页、容器没有顶部 padding，布局用全画布高算，再给各 Y 字段加 topShift（如 vp2px(顶部避让)）；onSizeChanged 多了 topShift 参数，注释写「含安全区 topShift」
适用范围：把源端用根视图 padding 避让状态栏的自绘页面迁成 ArkUI Canvas 时
做法：
- 画布外层容器写 .backgroundColor(状态栏底色资源).padding({ top: 顶部避让高度 })，Canvas 只占 padding 以下的区域
- onSizeChanged / 布局方程直接用画布自身的宽高，删掉 topShift 参数和布局输出上的各处 Y 平移，命中坐标按画布坐标算
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- padding(value: Padding | Length | LocalizedPadding): T：容器内边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- getWindowAvoidArea(type: AvoidAreaType): AvoidArea，AvoidAreaType.TYPE_SYSTEM = 0，取 AvoidArea.topRect：顶部避让区（状态栏）的矩形（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea、AvoidAreaType.TYPE_SYSTEM、AvoidArea.topRect）
- Rect 的 height 单位为 px：topRect.height 是 px，写进 padding 前按 vp 换算（出处：arkts-apis-window-i.md，Rect）
- backgroundColor(value: ResourceColor): T：容器背景色，铺在状态栏区域（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundColor）
来源：1 张卡，1 个应用
- case-7cd8faf4310e45fc7a2e（2048）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断
