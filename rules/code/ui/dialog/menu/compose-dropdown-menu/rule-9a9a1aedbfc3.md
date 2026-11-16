# 源端锚定或居中的无遮罩菜单，目标用 bindMenu 锚定或透明点外层，不加灰遮罩和固定位置

审的是：代码
触发（任一种）：
- 读到：Compose 菜单（DropdownMenu / CascadeDropdownMenu）放在触发 IconButton 所在的 Box 里锚定弹出，没有变暗遮罩；写错的样子：页面级 Stack 浮层：遮罩写成 .backgroundColor('#33000000') 或 '#66000000'，面板用 .position({ top: …, right: … }) 固定在屏幕某处
- 读到：基于 Popup(Alignment.Center) 的居中菜单：全屏 Box 没有背景色，只做点外关闭；写错的样子：居中菜单的点外关闭层写了 .backgroundColor('#66000000')，面板宽度写成固定值而不是源端的屏宽比例
适用范围：把源端锚定下拉菜单、级联菜单或居中弹出菜单迁成 ArkUI 时
做法：
- 锚定菜单在触发按钮上写 .bindMenu(this.MenuBuilder)，让菜单跟随各自的锚点，不在页面 Stack 里自绘固定 top/right 面板
- 必须自绘点外关闭层（如居中菜单）时，层保持透明（不写 #33000000 / #66000000），只负责点外关闭；面板宽度按源端的屏宽比例
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindMenu(content: Array<MenuElement> | CustomBuilder, options?: MenuOptions): T：给组件绑定点击弹出的菜单，锚定在这个组件上（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindMenu）
- bindMenu(isShow: boolean, content: Array<MenuElement> | CustomBuilder, options?: MenuOptions): T：用状态变量控制显隐的重载（@since 12）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindMenu）
- ContextMenuOptions.placement 默认 Placement.BottomLeft：MenuOptions 继承它；不写时菜单在触发组件下方、左侧对齐，位置不够时自动调整（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ContextMenuOptions.placement）
- ContextMenuOptions.mask 默认：有预览时 true，否则 false（@since 20）：bindMenu 默认不带遮罩，和源端无遮罩一致（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ContextMenuOptions.mask）
- 改成 bindMenu 锚定 + 透明点外层后，返修报告里行为不同的条目关闭：锚定无遮罩的形态（出处：卡里修好并验证过）
针对本应用要查的：
- 居中菜单的宽度比例：源工程里居中菜单组件的定义，找给 Popup 内容设固定宽度的那个常量；读出它和屏宽的比例，目标按同一比例算宽度
未核实：卡里的环境是 API 24（6.1.1），本机用 API 23 的声明核实
来源：1 张卡，1 个应用
- case-45230e39613edd881823（jerboa）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 5 ← 诊断
