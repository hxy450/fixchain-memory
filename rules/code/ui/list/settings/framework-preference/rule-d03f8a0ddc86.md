# 源是框架 PreferenceFragment 时，偏好行照 preference_material 取值

审的是：代码
触发（任一种）：
- 读到：源端 `android.preference.PreferenceFragment` 用 `addPreferencesFromResource(...)` 加载 PreferenceScreen，没有自定义 layout；写错的样子：偏好行内距、最小高、字号是估计值（标「待核」）；字色用 `sys.color.ohos_id_color_text_primary` 一类 sys 色，分隔线用 `ohos_id_color_list_separator` 且内缩、末项后无线
适用范围：把框架 PreferenceScreen（无自定义 layout）迁成 ArkUI List 时的偏好行外观
做法：
- 照 preference_material 写：最小高取 listPreferredItemHeightSmall，左右 padding 取 listPreferredItemPaddingStart/End，文字区上下 16vp；title 取 textAppearanceListItem 字号和 textColorPrimary，summary 取 textAppearanceListItemSecondary 字号和 textColorSecondary；按主题从平台资源解析成数值，不用估计值和 sys 色
- 分隔线照 listDivider（list_divider_material，高 1dp）写 List.divider({ strokeWidth: 1, color: <解析出的分隔线色> })，全宽不内缩；List 末项后不画线，末项后另补一条
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- preference_material：minHeight=?attr/listPreferredItemHeightSmall，paddingStart=?attr/listPreferredItemPaddingStart，文字区 paddingTop/Bottom=16dp，title 用 ?attr/textAppearanceListItem，summary 用 ?attr/textAppearanceListItemSecondary 和 ?attr/textColorSecondary：框架偏好行的布局，各值要按主题解析（出处：Android SDK 平台资源 data/res/layout/preference_material.xml（按应用的 compileSdk 取对应平台））
- Theme.Material：listPreferredItemHeightSmall=48dip；listPreferredItemPaddingStart=@dimen/list_item_padding_start_material → action_bar_content_inset_material=16dp：Material 主题下行最小高 48、左右内距 16（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material；data/res/values/dimens_material.xml，action_bar_content_inset_material（按应用的 compileSdk 取对应平台））
- TextAppearance.Material.ListItem 继承 Subhead（16sp、textColorPrimary）；ListItemSecondary 继承 Body1（14sp）：title 16、summary 14（出处：Android SDK 平台资源 data/res/values/styles_material.xml，TextAppearance.Material.ListItem；data/res/values/dimens_material.xml，text_size_subhead_material（按应用的 compileSdk 取对应平台））
- list_divider_material：shape 高 1dp，tint=?attr/colorListDivider，color=?attr/opacityListDivider（list_divider_opacity_material=#1f000000）：框架列表分隔线是 1dp 细线，颜色随主题前景色（出处：Android SDK 平台资源 data/res/drawable/list_divider_material.xml；data/res/values/colors_material.xml，list_divider_opacity_material（按应用的 compileSdk 取对应平台））
- divider(value: ListDividerOptions | null): ListAttribute；第一个子组件上方和最后一个子组件下方不画分割线：末项后的线要另补（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.divider；ts-container-list.md，divider）
- 左右、上下 16，text_primary 与新增 summary 色，分隔线全宽并补末项后一条：修复后的偏好行（出处：卡里修好并验证过）
针对本应用要查的：
- 主、次文字色和分隔线色：应用主题（AndroidManifest 的 android:theme 顺着 styles.xml 的 parent）属于哪一族，再到对应平台 data/res/values/themes_material.xml 找 textColorPrimary、textColorSecondary、colorListDivider，顺着 color/text_color_primary.xml 等引用找到 colorForeground、primaryContentAlpha、secondaryContentAlpha；颜色 = colorForeground × 对应 alpha，亮、暗主题各解析一套写进 base/dark color.json。例：Theme.Material.Light 下 colorForeground 为黑，android-36 的 primaryContentAlpha 0.87、secondaryContentAlpha 0.60，android-30 的 secondaryContentAlpha 为 0.54
来源：1 张卡，1 个应用
- case-fe1caa813d814978decf（Privacy Friendly 2048）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4、诊断；取值 6 ← 诊断
