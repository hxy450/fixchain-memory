# 上下文菜单的点击入口做居中模态列表，长按入口用跟随触点的菜单，不用 bindMenu/bindPopup 锚定

审的是：代码
触发（任一种）：
- 读到：源码 registerForContextMenu(view) 加点击时 openContextMenu(view)，onCreateContextMenu 设 setHeaderTitle / setHeaderIcon；写错的样子：目标只在按钮上挂 .bindMenu(...) 或 .bindPopup(..., { placement: Placement.Bottom }) 锚定下拉，没有长按入口，标题图标丢失
适用范围：实现安卓上下文菜单（点击打开和长按打开）时
做法：
- 点击入口：弹出居中模态列表对话框，顶部是 header 标题和图标，禁用项照源端 setEnabled(false) 处理
- 长按入口：在同一视图上挂跟随触点弹出的浮动菜单，如 .bindContextMenu(this.menuBuilder, ResponseType.LongPress)（不设 placement）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindContextMenu(content: CustomBuilder, responseType: ResponseType, options?: ContextMenuOptions): T：长按或右键弹出的上下文菜单（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindContextMenu）
- 作为 bindContextMenu(8+) 入参时 placement 默认效果是菜单跟随点击位置弹出；作为 bindMenu 入参时默认 Placement.BottomLeft：要触点浮动就用 bindContextMenu 且不设 placement；bindMenu 是锚定组件的下拉（出处：ts-universal-attributes-menu.md，ContextMenuOptions 的 placement）
- 单击为带标题图标的居中模态列表、长按为触点浮动菜单后，两种入口与源端一致：卡里修好的形态（出处：卡里修好并验证过）
未核实：卡里修好用的是自建菜单组件，长按入口具体用的接口卡里没写；bindContextMenu 是按声明和文档补的
来源：1 张卡，1 个应用
- case-48eaca54675fe3fdc6e9（MifareClassicTool）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断、建议 4；取值 3 ← 诊断
