# 源列表或偏好界面靠平台主题的默认外观时，顺主题到 SDK 平台资源读分隔线、按压色和几何，写成显式值

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
