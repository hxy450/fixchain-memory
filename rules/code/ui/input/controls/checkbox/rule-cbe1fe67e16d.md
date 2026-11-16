# checkable 菜单项转 MenuItem 时，除 selected 外要写 selectIcon(true)

审的是：代码
触发（任一种）：
- 读到：菜单 XML 的 <item> 写了 android:checkable="true"；写错的样子：对应 MenuItem 只写了 .selected(...)，没有 .selectIcon(...)，选中时看不到勾
适用范围：把带勾选状态的安卓菜单项迁成 ArkUI MenuItem 时
做法：
- 写成 MenuItem({ content: … }).selected(<勾选状态>).selectIcon(true)；selected 绑定源端 checked 状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- selectIcon(value: boolean | ResourceStr | SymbolGlyphModifier): MenuItemAttribute：选中时是否显示勾；true 显示默认对勾，也可传自定义图标（出处：鸿蒙 SDK 的 ets/component/menu_item.d.ts，MenuItemAttribute.selectIcon）
- selectIcon 默认值 false：不写就不显示勾，只写 selected 看不出选中（出处：ts-basic-components-menuitem.md，selectIcon）
- selected(value: boolean): MenuItemAttribute：菜单项是否选中，默认 false（出处：鸿蒙 SDK 的 ets/component/menu_item.d.ts，MenuItemAttribute.selected）
- checkable：Whether the item is capable of displaying a check mark.：源端 checkable 就是要显示勾选标记（出处：Android SDK 平台资源 data/res/values/attrs.xml，MenuItem 的 checkable（按应用的 compileSdk 取对应平台））
来源：1 张卡，1 个应用
- case-85baa9234cc4f4798784（AntennaPod）：做法第 1 步 ← 建议 5、诊断
