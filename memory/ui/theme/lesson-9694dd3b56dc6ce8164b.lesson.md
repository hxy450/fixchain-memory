# View 体系 Material 控件映射 ArkUI 内置组件时，先按主题代际列出源端库默认外观与度量，再逐项显式设置 ArkUI 属性

ID：`lesson-9694dd3b56dc6ce8164b` · 版本：2

[本主题](index.md)

## 何时使用

界面实现与规格提取阶段，把 CheckBox、RadioButton、Switch/SwitchPreference、TabLayout、EditText/Spinner、工具栏 SearchView、MaterialToolbar（?attr/actionBarSize）、BottomNavigationView、FAB、OutlinedButton、NavigationView 菜单项或框架 ActionBar 溢出菜单映射为 ArkUI 组件，而布局未写具体样式值时

## 适用情境

映射参考只给一对一或逐属性映射，而 ArkUI 组件自带的默认外观与源端 Material 默认不同（Checkbox 默认圆形、Radio 默认勾选样式、Toggle 胶囊开关、TextInput/Select 默认填充底、Tabs 默认标签样式、Menu 为系统定位的圆角卡片）；源端取值由 Theme.Material3.*、MaterialComponents、AppCompat 或框架主题的组件默认样式决定，库在 values-land、values-sw600dp 下可能另有取值；工程里可能有按 M2 默认值或兄弟页先例写的同类组件。

## 例外与边界

- 源端为控件写了 widgetLayout、thumb/track、itemIconTint 等具体覆写，或在 style 中写出具体值时，按显式值转换；style 只继承库样式（如 Widget.Material3.Button.OutlinedButton）时仍按本条解析库默认

## 原因

ArkUI 内置组件的默认外观与源端库默认不同，逐属性直译只搬了 XML 写出的几项，其余外观落到 ArkUI 默认；检索不到显式覆写就套用 M2 或 AppCompat 默认，或沿用兄弟页数值，会系统性偏离源主题代际的外观；按竖屏单值实现在横屏也会偏离。功能映射（Switch → Toggle、菜单 → Menu）不等于外观一致。

## 做法

1. 先读页面元数据列出的 styles.xml，沿 parent 链确认组件库代际或框架主题（Theme.Material3.*、Theme.MaterialComponents.*、Theme.AppCompat.*、android:Theme.*），从对应 aar 或 SDK 资源取默认外观与度量，连同 values-land、values-sw600dp 的覆盖值；检索不到覆写不等于采用 M2 默认。
2. 逐项与 ArkUI 默认值对照并显式设置：Checkbox .shape(CheckBoxShape.ROUNDED_SQUARE)、Radio 的 indicatorType、TextInput/Select 透明底、Tabs 用 SubTabBarStyle 指定 labelStyle 与指示条；工具栏里展开的 SearchView 映射为 Search 时用透明底，放大镜同工具栏图标色，提示色取 textColorHint，不加胶囊底；源样式继承 MDC/M3 按钮时，从合并资源解析 textAppearance 的 letterSpacing 与文字颜色 selector，不凭记忆取强调色。
3. Switch/SwitchPreference → Toggle 只是功能映射：框架 Material Switch 为细轨道加外凸带投影拇指，外观要一致时自绘或显式定制；偏好行中开关不接收点击、由整行切换，开关设 hitTestBehavior(HitTestMode.None)。
4. 工具栏度量按代际取：Material3 主题的 actionBarSize 为 m3_appbar_size_compact 64dp，Widget.Material3.Toolbar 标题为 TitleLarge 22sp 常规字重（material 1.12.0 values.xml）；标题起点按其继承链上的 contentInsetStart、contentInsetStartWithNavigation（M3 设为 0dp）、titleMargin 与导航按钮最小宽度解析；AppCompat 的 abc_action_bar_default_height_material 竖屏 56dp、values-land 48dp、sw600dp 64dp，abc_text_size_title_material_toolbar 竖屏 20dp、values-land 14dp（appcompat 1.7.1），用 base 与 horizontal 等同名资源承载。
5. 底栏选中标签按 itemTextAppearanceActiveBoldEnabled 加粗，徽标宿主收至图标尺寸后右上锚定；Material3 主题下未写 style 的 FAB 为 shapeAppearanceCornerLarge 16dp 圆角方形配 colorPrimaryContainer/onPrimaryContainer，OutlinedButton 文字为 LabelLarge 14sp Medium（material 1.12.0 values.xml 的 ShapeAppearance.M3.Sys.Shape.Corner.Large 与 values-v21.xml 的 TextAppearance.M3.Sys.Typescale.LabelLarge：sans-serif-medium 14sp）。
6. AppCompat 主题下未写样式的 TabLayout（Widget.Design.TabLayout）MODE_FIXED 竖屏 tabGravity=fill 均分；values-land 与 sw600dp 为 center：各 Tab 取最宽 Tab 宽并整体居中，总宽放不下才退回 fill（material 1.12.0 的 values-land、values-sw600dp-v13 中 tabGravity=center、tabMode=fixed）；ArkUI Tabs 默认只等价竖屏情形。
7. 未写 item 样式的 NavigationView 菜单项写出选中项通栏底色、加粗与 colorPrimary 着色，未选图标次文字色着色，组间通栏分隔与列表上下留白，并标明取自 Material 默认样式。
8. 框架 ActionBar 的溢出菜单（showAsAction=never 的项）由平台主题的弹出菜单样式绘制：从 SDK 的 actionOverflowMenuStyle（Theme.Holo 指向 popupMenuStyle）、popup_menu_item_layout 与对应 dimens 取最小宽度、行高、字号与左右内边距、分隔线、底色与边线、锚定位置（例：android-36.1 中 popup_menu_item_layout 的 minWidth 为 196dip，行高取 dropdownListPreferredItemHeight，Theme.Holo 下即 listPreferredItemHeightSmall 48dip）；要求一比一时用页内浮层：全屏遮罩只负责关闭并吞掉事件，面板贴锚点下沿，宿主返回键先关闭浮层；规格只写“Menu + MenuItem”时，只改底色与字色不算对齐。

来源支持：9 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-01ea7d8b923cd659dbba](../../../store/cases/case-01ea7d8b923cd659dbba/47a9f8cf52b0f7110a910cabd68145e781df2e4650e126db023c482fd2521561.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:2
  卡片版本：`47a9f8cf52b0f7110a910cabd68145e781df2e4650e126db023c482fd2521561`
- [case-6d63b644ee5d30db83f4](../../../store/cases/case-6d63b644ee5d30db83f4/ddcd8864bda1e51dc2c723173453a36369b2f6aa0e3e59ad80302717e5926fae.json) · 结论：recommendation:1
  卡片版本：`ddcd8864bda1e51dc2c723173453a36369b2f6aa0e3e59ad80302717e5926fae`
- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:4
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
- [case-a3dc4d0187d7ddc456e8](../../../store/cases/case-a3dc4d0187d7ddc456e8/f859e7871c0c6c7b9d5e869a46ae4f3510862fa498179e0840d4b2f955a32599.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:5
  卡片版本：`f859e7871c0c6c7b9d5e869a46ae4f3510862fa498179e0840d4b2f955a32599`
- [case-b0d293fe50601628c722](../../../store/cases/case-b0d293fe50601628c722/6d95f50479304037c98d6272e83476612b21381ffc2800d10c36764fcb11b018.json) · 结论：recommendation:3
  卡片版本：`6d95f50479304037c98d6272e83476612b21381ffc2800d10c36764fcb11b018`
- [case-c40332380c19d002090d](../../../store/cases/case-c40332380c19d002090d/20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9`
- [case-c6728cbe6feb50c4f9ea](../../../store/cases/case-c6728cbe6feb50c4f9ea/2a5d1d6f4cb5079c43c4f61adce706947e30e16e02f7f239104a98381741e0a3.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`2a5d1d6f4cb5079c43c4f61adce706947e30e16e02f7f239104a98381741e0a3`
- [case-cee85a6c89d26db1ef48](../../../store/cases/case-cee85a6c89d26db1ef48/4d1df012cffa48633bcbe560992518a78ed6fc5a2e6e9394efc12e37b2577dea.json) · 结论：recommendation:1, recommendation:3
  卡片版本：`4d1df012cffa48633bcbe560992518a78ed6fc5a2e6e9394efc12e37b2577dea`
- [case-f226842558d82e3f3ad9](../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：recommendation:3
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
