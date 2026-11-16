# ListPreference(DROPDOWN_MENU) 映射为锚在该行的 bindMenu 菜单，不写成行内展开

审的是：代码
触发（任一种）：
- 读到：ListPreference(type = ListPreferenceType.DROPDOWN_MENU)，规格映射为 Select；写错的样子：目标写成点击切换 expanded、在行下方插入选项列表的行内展开（带 chevron_up / chevron_down），沿用了别的页面 ReadOnlyDropdown 式的先例
适用范围：页面实现阶段，迁移 compose-preference 的 ListPreference 下拉菜单形态
做法：
- 映射为锚在该行上的弹出菜单：行组件上 .bindMenu(菜单项或 @Builder, options)，或用 Select；选中后更新值并关菜单
- 复用工程先例前，先核对先例对应的 Android 组件和本页是否相同；行内展开的只读下拉不能替代 preference 的弹出菜单
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindMenu(content: Array<MenuElement> | CustomBuilder, options?: MenuOptions): T：给组件绑定弹出菜单，点击时弹在该组件旁（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindMenu）
- bindMenu(isShow: boolean, content: Array<MenuElement> | CustomBuilder, options?: MenuOptions): T：同族接口：由状态变量控制显示的重载（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindMenu）
- Select(options: Array<SelectOption>): SelectAttribute：下拉选择组件，规格里写的 Select（出处：鸿蒙 SDK 的 ets/component/select.d.ts，SelectInterface）
未核实：卡里环境是鸿蒙 6.1.1(24)，本机按 API 23 核对
来源：1 张卡，1 个应用
- case-69c1c089176794fbe5db（jerboa）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3
