# 框架偏好控件无自定义 layout 时，到平台布局和主题读出外观，再写成显式值

审的是：代码
触发（任一种）：
- 读到：PreferenceFragment 用 addPreferencesFromResource 加载偏好，没有自定义 layout；写错的样子：设置行的行高、内距、字号、字色、分隔线用估计值或 sys.color 语义色，行内 Toggle 自身可点
适用范围：框架 PreferenceScreen 迁成 ArkUI 设置页时的偏好行
做法：
- 到 Android SDK 平台资源 data/res/layout/ 找这个偏好的框架布局（preference_material.xml、preference_widget_switch.xml 等），记下尺寸、文字样式和 clickable 的写法
- 其中的 ?attr/… 按应用主题所属的那一族，到对应平台 data/res/values/ 里顺着 @dimen、@style、@color 读出数值，颜色亮、暗各解析一套
- 写成显式值：尺寸和字号写数值，颜色进 base / dark 的 color.json，布局里不接点击的子控件在目标端也不接点击
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- preference_material：minHeight=?attr/listPreferredItemHeightSmall，paddingStart=?attr/listPreferredItemPaddingStart，文字区 paddingTop/Bottom=16dp，title 用 ?attr/textAppearanceListItem，summary 用 ?attr/textAppearanceListItemSecondary 和 ?attr/textColorSecondary：框架偏好行的布局，各值要按主题解析（出处：Android SDK 平台资源 data/res/layout/preference_material.xml（按应用的 compileSdk 取对应平台））
- <Switch android:focusable="false" android:clickable="false" />：SwitchPreference 右侧的开关自身不接收点击和焦点，点击由整行处理（出处：Android SDK 平台资源 data/res/layout/preference_widget_switch.xml，Switch（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 这个偏好用的框架布局，以及其中引用的主题属性：Android SDK 平台资源 data/res/layout/ 下的 preference_*.xml（按应用的 compileSdk 取对应平台）；逐项读出 minHeight、padding、textAppearance、textColor、clickable / focusable，标出哪些是 ?attr/… 引用
- ?attr/… 在应用主题下的实际值：源工程 AndroidManifest 的 android:theme 顺着 styles.xml 的 parent 定出主题属于哪一族，再到对应平台 data/res/values/ 的 themes_material.xml、styles_material.xml、dimens_material.xml、colors_material.xml 按属性名找；顺着 @dimen、@style、@color 引用一步步读到数值；颜色 = colorForeground × 对应 alpha。例：android-36 的 Theme.Material 下 listPreferredItemHeightSmall 为 48dip，listPreferredItemPaddingStart 经 action_bar_content_inset_material 为 16dp
未核实：各 Preference 类经主题取到哪个框架布局和 widgetLayout（如 ListPreference、CheckBoxPreference）族里规矩没有查实，要按平台资源核对；源端是 androidx.preference 的 PreferenceFragmentCompat 时布局出自依赖库，族里规矩没有查过
来源：2 张卡，1 个应用
- case-01ea7d8b923cd659dbba（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-fe1caa813d814978decf（Privacy Friendly 2048）：做法第 1 步 ← 建议 4；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 4
