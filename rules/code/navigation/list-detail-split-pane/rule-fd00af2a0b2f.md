# 宽窗列表-详情分栏按当前目的地的 pane 角色判断，不按所在顶层

审的是：代码
触发（任一种）：
- 读到：源端 ListDetailSceneStrategy 按各目的地的 metadata 分栏：只有某个目的地带 ListDetailSceneStrategy.detailPane()，列表根是 listPane(detailPlaceholder = …)，同顶层下 push 的其他目的地（如顶栏 Search）没有 pane 元数据；规格路由表只把详情目的地标为「详情 pane」；写错的样子：分栏条件写成「宽窗 && 当前顶层 === 列表顶层」驱动 Navigation 的 .mode(NavigationMode.Split)，同一顶层下 push 的非详情目的地也被挤进右侧详情 pane
适用范围：用单个 Navigation 的 Split / Stack 模式加宽度断点模拟源端宽窗列表-详情分栏时
做法：
- 分栏条件写成「宽窗 && 当前目的地是详情 pane 角色（源端带 detailPane() 的目的地，或路由表标了「详情 pane」的）」；同一顶层下 push 的非详情目的地保持 NavigationMode.Stack 全宽 push
- 拿不准时先在源码 grep 各入口的 pane 元数据（detailPane / listPane / 无）；写完逐个列出这个顶层下能打开的目的地，对照路由表核对宽窗下各自是单栏还是进详情 pane
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- mode(value: NavigationMode): NavigationAttribute，默认 NavigationMode.Auto：Navigation 的显示模式，分栏条件的结果写在这里（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.mode）
- NavigationMode.Stack：导航栏和内容区堆叠显示；NavigationMode.Split：并排显示；NavigationMode.Auto：窗口宽度大于 minNavBarWidth 与 minContentWidth 之和时分栏：三种模式的含义（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationMode）
- navBarWidth(value: Length): NavigationAttribute，默认 240，单位 vp：分栏时左侧列表宽度（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.navBarWidth）
- 条件追加「当前路由是详情目的地」后，宽窗下从列表点搜索进入全宽页面，不再挤进右侧 pane：修好的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 各目的地在宽窗下的 pane 角色：源工程里各目的地的 entry 定义（Navigation3 entryProvider / EntryProvider），搜 detailPane()、listPane(；带 detailPane() 的进详情 pane，带 listPane 的是列表，都没有的按普通全宽页面处理
未核实：源端在 600–840vp 只有列表根时是否双栏没核到；空列表根是否分栏、600vp 断点不在本条范围
来源：1 张卡，1 个应用
- case-47f91f2992cdb1f6e390（nowin_v930_cc_ds）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、建议 3；取值 4 ← 诊断
