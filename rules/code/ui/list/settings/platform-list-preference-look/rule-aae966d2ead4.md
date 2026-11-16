# GridView/ListView 未改 listSelector 时，条目 pressed 按主题选择器色写底色

审的是：代码
触发（任一种）：
- 读到：源 GridView / ListView 没写 android:listSelector、android:drawSelectorOnTop，按压高亮来自 Activity 主题（分布在 values、values-v11 等 styles.xml）；写错的样子：条目写 .stateStyles({ pressed: { .opacity(0.7) } }) 一类整体变暗，或 pressed 色值是自拟的
- 读到：可点击的偏好行或 ListView 行，主题 listSelector 是 list_selector_holo_dark，行没把 background / selector 设成 null；写错的样子：可点击行没有按压态（理由是查不到 stateEffect），或按压色借用别的资源色
适用范围：源列表、网格或偏好行的按压反馈来自主题默认 listSelector，迁成 ArkUI 条目或自绘行时
做法：
- 按设备 API 取 values-vNN 里 Activity 主题的 parent 链定主题代际（低 minSdk 工程在新设备上也走 values-v11+），再取该主题 listSelector 按压态的颜色
- 在承载点击的条目或行容器上写 .stateStyles({ normal: { .backgroundColor(Color.Transparent) }, pressed: { .backgroundColor(按压色) } })，底色画在内容下面，不用 opacity 代替；stateEffect 只属 Button，不是省略的理由；禁用行不显示按压
- 取不到颜色时报告写明缺口，不以 opacity 兜底
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- drawSelectorOnTop：Otherwise the selector is drawn behind the selected item. The default value is false.：没写时按压色画在条目内容下面，图标和文字像素不变（出处：Android SDK 平台资源 data/res/values/attrs.xml，AbsListView 的 drawSelectorOnTop（按应用的 compileSdk 取对应平台））
- Theme.Holo：gridViewStyle = @style/Widget.Holo.GridView，其 listSelector = ?attr/selectableItemBackground，selectableItemBackground = @drawable/item_background_holo_dark：Holo 暗色主题下 GridView 默认选择器的解析链（出处：Android SDK 平台资源 data/res/values/themes_holo.xml、styles_holo.xml，Widget.Holo.GridView（按应用的 compileSdk 取对应平台））
- Widget.Holo.ListView 的 listSelector = ?attr/listChoiceBackgroundIndicator：ListView 走另一个主题属性，要分开查（出处：Android SDK 平台资源 data/res/values/styles_holo.xml，Widget.Holo.ListView（按应用的 compileSdk 取对应平台））
- list_selector_holo_dark 的按下态（state_pressed="true"）指向 list_selector_background_transition_holo_dark：列表行按压色出自这张图（出处：Android SDK 平台资源 data/res/drawable/list_selector_holo_dark.xml（按应用的 compileSdk 取对应平台））
- stateStyles(value: StateStyles): T：所有组件共有的多态样式，pressed、normal 各写一块（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.stateStyles、StateStyles.pressed）
- stateEffect(value: boolean): ButtonAttribute：只有 Button 有，别的容器没有（出处：鸿蒙 SDK 的 ets/component/button.d.ts，ButtonAttribute.stateEffect）
- Theme.Holo 暗色下按压为整格（含内边距空白）#40CCCCCC 底色画在图标下；写成 normal 透明、pressed backgroundColor('#40CCCCCC') 后两端取样一致：修好的写法（这个色值只对 Holo 暗色主题成立）（出处：卡里修好并验证过）
针对本应用要查的：
- Activity 主题的代际和 listSelector 的按压色：源工程 AndroidManifest.xml 里该 Activity（或 application）的 android:theme；res/values*/styles.xml 里同名主题，按设备 API 取最高的 values-vNN 看 parent 和 listSelector 覆盖；再到 Android SDK 平台资源 themes*.xml、styles*.xml 顺着 gridViewStyle / listViewStyle → listSelector 找到 data/res/drawable 里的 list_selector_* 等选择器；看 selector 里 state_pressed 的那一项；指向九宫格图片的要取样读出颜色（例：Theme.Holo 暗色下取样为 #40CCCCCC）
来源：2 张卡，2 个应用
- case-a8bb009f2c5e1b854f32（Blockinger）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4；取值 7 ← 建议 4、诊断
- case-ecf6bf1e97fdf99c99a3（Bubble Shooter）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；做法第 3 步 ← 建议 1；取值 7 ← 诊断、建议 2
