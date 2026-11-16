# 平台主题下 ListView 和偏好界面的默认外观

agent 会看到什么：读到 ListView、GridView、ExpandableListView、PreferenceActivity 没写 divider、listSelector、scrollbars 等，外观来自 Theme.Holo 等平台主题；交回的 List 缺分隔线或末行那条、按压态用 opacity 或自拟色、偏好行和对话框的几何凭记忆写，或 CheckBoxPreference 写成 Toggle

## 通用查法

### 源列表或偏好界面靠平台主题的默认外观时，顺主题到 SDK 平台资源读分隔线、按压色和几何，写成显式值

审的是：代码
触发（任一种）：
- 读到：ListView、GridView、PreferenceActivity 的列表没写 android:divider、android:listSelector，外观来自 Theme.Holo 等平台主题；写错的样子：目标 ListItem 的 Divider、stateStyles 的 pressed 色、行几何是凭记忆或借用的值，或没有
适用范围：源列表、偏好界面的外观由平台主题提供时
做法：
- 按 AndroidManifest.xml 的 android:theme 和按设备 API 取最高的 values-vNN 的 styles.xml 顺 parent 找到 android:Theme.* 那层
- 到 Android SDK 平台资源 themes_*.xml 读 listViewStyle、gridViewStyle、listDivider 等属性，再到 styles_*.xml 读样式的 divider、listSelector，顺 ?attr/、@drawable/ 找到 selector 或图
- 读出颜色和尺寸（九宫格图取样，px 按密度换成 vp），写成显式的 Divider 粗细和颜色、pressed 底色和行几何；取不到的报告缺口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Holo：gridViewStyle = @style/Widget.Holo.GridView，其 listSelector = ?attr/selectableItemBackground，selectableItemBackground = @drawable/item_background_holo_dark：例：Holo 暗色主题下 GridView 默认选择器的解析链（出处：Android SDK 平台资源 data/res/values/themes_holo.xml、styles_holo.xml，Widget.Holo.GridView（按应用的 compileSdk 取对应平台））
- Widget.Holo.ListView 的 divider = ?attr/listDivider，listSelector = ?attr/listChoiceBackgroundIndicator：例：ListView 的分隔线和选择器走另外的主题属性，要和 GridView 分开查（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.ListView（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- Activity 主题的代际：源工程 AndroidManifest.xml 里该 Activity（或 application）的 android:theme；res/values*/styles.xml 里同名主题，按设备 API 取最高的 values-vNN 看 parent；一直找到 android:Theme.* 那层；低 minSdk 工程在新设备上也走 values-v11 以上的父主题
- 分隔线、按压色和行几何的平台取值：Android SDK 平台资源（按 compileSdk 取对应平台）data/res/values 的 themes_*.xml、styles_*.xml，以及 drawable/ 和各密度 drawable 目录下被引用的 selector 和图；顺 state_pressed 项、listDivider 找到图或颜色；九宫格图取样读色，高度按密度换成 vp。例：Theme.Holo 暗色下按压底色取样为 #40CCCCCC、分隔线 #26FFFFFF
未核实：Theme.Holo 的 listViewStyle 指向的样式名，以及偏好行的行高、内边距在平台 preference_holo 布局里对应的资源名，族里规矩没有查实
来源：3 张卡，2 个应用
- case-a8bb009f2c5e1b854f32（Blockinger）：做法第 3 步 ← 建议 1
- case-c3ff122a5abfda1fa55d（Blockinger）：做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3
- case-ecf6bf1e97fdf99c99a3（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-3e528c37d622｜ListView 用主题分隔线时，每个 ListItem 末尾加 Divider，末行那条按底边条件显示｜读到：<ListView> 没写 android:divider，主题 listDivider 隐式画行间线（如 Theme.Holo 的 list_divider_holo_dark）；写错：List 的 ForEach 行里没有 Divider，也没有 .divider(...)；color.json 里没有列表分隔线颜色
- rule-a7f036910eb7｜ExpandableListView 的分隔线迁到 ArkUI 时，组内另设 ListItemGroup.divider｜读到：ExpandableListView 写了 android:divider / android:dividerHeight，没写 android:childDivider；写错：只设了 List.divider(...)，组头与子项之间、子项之间没有分隔线；或组内分隔线也用了 divider 的颜色
- rule-aae966d2ead4｜GridView/ListView 未改 listSelector 时，条目 pressed 按主题选择器色写底色｜读到：源 GridView / ListView 没写 android:listSelector、android:drawSelectorOnTop，按压高亮来自 Activity 主题（分布在 values、values-v11 等 styles.xml）；写错：条目写 .stateStyles({ pressed: { .opacity(0.7) } }) 一类整体变暗，或 pressed 色值是自拟的
- rule-966b5108fffb｜可滚动的 GridView/ListView 迁成 Grid/List 时，显式设滚动条和越界效果｜读到：源 GridView / ListView 没写 android:scrollbars、android:overScrollMode，内容超过一屏（行高 × 行数大于可视高度）；写错：Grid 上没有 .scrollBar(...)、.scrollBarWidth(...)、.scrollBarColor(...)、.edgeEffect(...)，沿用 BarState.Auto 和 EdgeEffect.None
- rule-5a0eef84b0ab｜自绘 Holo 偏好列表时，按平台几何写列表内边距、行高、分类头和分隔线规则｜读到：android.preference.PreferenceActivity + Theme.Holo，res/xml 里有 PreferenceCategory 和多个偏好项；写错：List 没有左右 16vp 内边距；每行后都画 divider（含分类头前）、末项后不画，或 List.divider 通栏；分类头 Medium 字重、不全大写、没有 2dp 底线；行内边距凭记忆写
- rule-0b7d16309d15｜CheckBoxPreference 写成平台六态图的方形复选框，不写成 Toggle 开关｜读到：res/xml 里有 <CheckBoxPreference>；规格写 Row + Checkbox（Holo 方形勾选），映射参考写 CheckBox→Checkbox；派工却写 CheckboxPreference→Toggle；写错：行内控件写成 Toggle({ type: ToggleType.Switch })，或把规格的 Checkbox 方案改写成 Toggle 并注明覆盖原方案
- rule-b4c1b4965472｜复刻偏好对话框时，尺寸、字号、颜色和图片从 SDK 的平台布局与主题取，不凭记忆自拟｜读到：<EditTextPreference> / <ListPreference> 由框架弹平台对话框，应用主题是 Theme.Holo 一族；写错：目标自绘面板写死自拟数值：标题字号、面板底色、带圆角填充底的 TextInput、按钮颜色，代码里找不到平台出处
