# 框架样式的选择器背景迁成按状态换图的背景组件，不用透明底加默认压暗或半透明层

审的是：代码
触发（任一种）：
- 读到：源控件 style="@android:style/Widget.ImageWell" 这类框架样式，背景是 9-patch 状态选择器；或规格只写「透明」「平台默认」没给出处；写错的样子：目标写 .type(ButtonType.Normal).backgroundColor(Color.Transparent)，按下只剩 Button 默认压暗；或只放图标、按下时叠一层通用半透明层
适用范围：页面实现阶段落实以 @android:style 引用框架样式、背景为状态选择器的按钮和图标按钮时
做法：
- 规格没给出处时，回源布局看 style 引用，到 Android SDK 平台资源核实背景选择器后再写
- 建一个按状态换图的背景组件：常态用 normal 图，按下换 pressed 图（从平台 drawable-<密度> 取 9-patch，按密度缩放），图标或文字放在 9-patch 内容内边距（ImageWell 是 7.5/7/7.5/7）里
- 不用通用半透明层或 ArkUI Button 的默认按压效果代替源端的按下图
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- state_pressed → panel_picture_frame_bg_pressed_blue；默认 → panel_picture_frame_bg_normal（另有 state_focused → panel_picture_frame_bg_focus_blue）：要迁的状态和对应图（出处：Android SDK 平台资源 data/res/drawable/panel_picture_frame_background.xml（按应用的 compileSdk 取对应平台））
- 从 SDK 取出 normal 与 pressed_blue 两张 9-patch，自建按状态换图的边框组件，按密度缩放，图标放进 7.5/7/7.5/7 内边距后与源端一致：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 各状态图和内容内边距：Android SDK 平台资源 platforms/android-<应用 compileSdk>/data/res 下的 drawable/*.xml 选择器和 drawable-<密度>/*.9.png；选择器里每个 state 对应一张图；9-patch 右、下边的黑线给出内容内边距，按密度换算成 vp
来源：1 张卡，1 个应用
- case-268d985fb35cb7ff1cde（Blockinger）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 2；取值 2 ← 诊断
