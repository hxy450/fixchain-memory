# 复刻溢出菜单或 PopupMenu 宽度时用 constraintSize 写下限和上限，不写 width(196)

审的是：代码
触发（任一种）：
- 读到：菜单 XML 的 <item> 带 showAsAction="never"（进溢出菜单）或用 PopupMenu 弹出，标题是 @string/ 字符串资源；框架菜单项布局 abc_popup_menu_item_layout 写着 android:minWidth="196dip"；写错的样子：自绘的菜单弹层或菜单行写成 .width(196)（或别的实测宽度），没有 maxWidth 上限，标题 Text 没有 maxLines(1)
适用范围：把安卓溢出菜单、PopupMenu 复刻成 ArkUI 自绘弹层（不用系统 Menu/bindMenu）时，菜单宽度和菜单项标题的写法
做法：
- 菜单容器写 .constraintSize({ minWidth: 196, maxWidth: Math.max(窗口宽 / 2, 320) })，宽度由最宽的菜单项撑开，不写 .width(N)
- 菜单项标题 Text 加 .maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })，长译文单行显示
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constraintSize(value: ConstraintSizeOptions): T：限制组件布局时的尺寸范围，ConstraintSizeOptions 有 minWidth、maxWidth、minHeight、maxHeight；默认 {minWidth: 0, maxWidth: Infinity, minHeight: 0, maxHeight: Infinity}（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.constraintSize；ets/component/units.d.ts，ConstraintSizeOptions）
- android:minWidth="196dip"：框架菜单项布局的最小宽度，196 是下限，不是内容宽度（出处：androidx.appcompat:appcompat 包内 res/layout/abc_popup_menu_item_layout.xml，ListMenuItemView 的 android:minWidth（按应用依赖的版本）；Android SDK 平台资源 data/res/layout/popup_menu_item_layout.xml（按应用的 compileSdk 取对应平台））
- mPopupMaxWidth = Math.max(widthPixels / 2, config_prefDialogWidth)：框架弹出菜单的宽度上限：屏宽的一半和 config_prefDialogWidth 取大者，菜单宽按最宽项测量、不超过它（出处：com.android.internal.view.menu.StandardMenuPopup 构造函数；com.android.internal.view.menu.StandardMenuPopup#tryShow 里的 measureIndividualMenuWidth）
- config_prefDialogWidth：values 320dp，values-large 440dp，values-sw600dp 580dp：上限里的那个常量随屏幕配置变；手机上是 320dp。AppCompat 包内 abc_config_prefDialogWidth 取值相同（出处：Android SDK 平台资源 data/res/values/config.xml、values-large/config.xml、values-sw600dp/config.xml，config_prefDialogWidth（按应用的 compileSdk 取对应平台）；androidx.appcompat:appcompat 包内 res/values/values.xml，abc_config_prefDialogWidth）
- 标题 TextView 带 android:singleLine="true"、android:ellipsize="marquee"：安卓菜单项标题只占一行，超长时截断，不折行（出处：androidx.appcompat:appcompat 包内 res/layout/abc_popup_menu_item_layout.xml，@+id/title 的 TextView（按应用依赖的版本））
- maxLines(value: number): TextAttribute；textOverflow(options: TextOverflowOptions): TextAttribute；TextOverflow.Ellipsis：Text 默认自动折行；设了 maxLines 后不超过指定行数，多出的文字由 textOverflow 决定，Ellipsis 用省略号替换（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.maxLines、TextAttribute.textOverflow；ets/component/enums.d.ts，TextOverflow.Ellipsis）
- constraintSize(value: ConstraintSizeOptions): T：同族接口：安全控件（SecurityComponentMethod）的尺寸约束（出处：鸿蒙 SDK 的 ets/component/security_component.d.ts，SecurityComponentMethod.constraintSize）
- itemConstraintSize(value: ConstraintSizeOptions): WaterFlowAttribute：同族接口：WaterFlow 子项的尺寸约束（出处：鸿蒙 SDK 的 ets/component/water_flow.d.ts，WaterFlowAttribute.itemConstraintSize）
未核实：上限里的「窗口宽」取窗口宽度还是屏幕宽度、怎样换成 vp，卡里没写明；AppCompat 代码里的菜单上限是否同样用 abc_config_prefDialogWidth，本机只有编译产物，按框架源码类推
来源：1 张卡，1 个应用
- case-58314365b74c00244c4f（Privacy Friendly 2048）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断
