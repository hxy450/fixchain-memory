# 工具栏里展开的 SearchView 迁成 Search 用透明底，不加胶囊底色，提示色取 textColorHint

审的是：代码
触发（任一种）：
- 读到：菜单项的 actionView 是 SearchView（或其子类），showAsAction 带 collapseActionView，挂在 Toolbar / MaterialToolbar 上；源码和布局没给它声明容器底色；写错的样子：Search 上写了 .backgroundColor(…) 填充色（胶囊底），或者没写 .placeholderColor(…)，放大镜颜色和工具栏图标不一致
适用范围：SearchView 作为工具栏菜单 actionView 展开、源端没有声明容器底色时，迁成 ArkUI Search
做法：
- Search(...).backgroundColor(Color.Transparent)，不加源端没有的填充色和胶囊圆角
- .searchIcon({ color: <工具栏图标色> })，.placeholderColor(<源端的 textColorHint>)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Base.Widget.AppCompat.SearchView.ActionBar：queryBackground = @null，searchHintIcon = @null：工具栏主题覆盖（searchViewStyle 指向它）里的 SearchView 输入区没有底（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.Widget.AppCompat.SearchView.ActionBar、Base.ThemeOverlay.AppCompat.ActionBar（按应用依赖的版本））
- 放大镜图 abc_ic_search_api_material 的 android:tint="?attr/colorControlNormal"；ActionBar 主题覆盖里 colorControlNormal = ?android:attr/textColorPrimary：放大镜和工具栏其他图标同按 colorControlNormal 着色（出处：androidx.appcompat:appcompat 包内 res/drawable/abc_ic_search_api_material.xml；res/values/values.xml，Base.ThemeOverlay.AppCompat.ActionBar（按应用依赖的版本））
- Color.Transparent：透明色枚举值，写进 backgroundColor（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，Color.Transparent）
- searchIcon(value: IconOptions | SymbolGlyphModifier): SearchAttribute；IconOptions { size?: Length; color?: ResourceColor; src?: ResourceStr }，浅色模式默认 color '#99182431'：放大镜图标的颜色用 color 设（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.searchIcon、IconOptions）
- placeholderColor(value: ResourceColor): SearchAttribute，默认 '#99182431'：提示文字颜色，不写时是默认灰（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.placeholderColor）
- placeholderColor(value: ResourceColor): TextInputAttribute：同族接口：TextInput 的提示文字颜色（出处：鸿蒙 SDK 的 ets/component/text_input.d.ts，TextInputAttribute.placeholderColor）
- placeholderColor(value: ResourceColor): TextAreaAttribute：同族接口：TextArea 的提示文字颜色（出处：鸿蒙 SDK 的 ets/component/text_area.d.ts，TextAreaAttribute.placeholderColor）
针对本应用要查的：
- 源端搜索框的提示色：源工程的主题 XML：Toolbar 的 android:theme / app:theme 主题覆盖 → Activity 主题 → 应用主题，找 android:textColorHint；顺着 @color/…、?attr/… 引用解析到具体颜色，写进 placeholderColor
- 工具栏图标色（放大镜颜色）：同一条主题链上的 colorControlNormal；没覆盖时按工具栏主题覆盖的 ?android:attr/textColorPrimary 解析；解析出颜色，写进 searchIcon 的 color
未核实：ArkUI Search 不写 backgroundColor 时的默认底色，本机声明和文档副本里没查到
来源：1 张卡，1 个应用
- case-f226842558d82e3f3ad9（AntennaPod）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
