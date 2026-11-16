# 标题栏按钮按压背景是无界 <ripple android:radius> 时，按半径画圆，不铺满按钮

审的是：代码
触发（任一种）：
- 读到：ActionBar 按钮（Widget.Material.ActionButton）的 background 是 ?attr/actionBarItemBackground，解析到 action_bar_item_background_material：<ripple android:radius="20dp">，无 mask、无内容层；写错的样子：标题栏 Up、图标、溢出按钮的 stateStyles pressed 写 .backgroundColor('#33FFFFFF')，铺满整个按钮矩形
适用范围：Material 主题标题栏按钮的按压态迁成 ArkUI 时
做法：
- 用 onTouch 记录按下状态和按钮尺寸，在图标下层绝对定位一个半径等于 android:radius（20dp 即直径 40vp）的径向圆，颜色取涟漪色，圆心在按钮内容区中心，圆外无色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Theme.Material：actionBarItemBackground = @drawable/action_bar_item_background_material；该 drawable 是 <ripple android:color="?attr/colorControlHighlight" android:radius="20dp" />：无 mask、无内容层的无界涟漪，半径 20dp（出处：Android SDK 平台资源 data/res/values/themes_material.xml，actionBarItemBackground；data/res/drawable/action_bar_item_background_material.xml（按应用的 compileSdk 取对应平台））
- RippleDrawable 没有子层和 mask、又作为 View 背景时，画在祖先背景上，绘制区可超出 drawable 边界：无界涟漪不受按钮矩形约束（出处：android.graphics.drawable.RippleDrawable）
- onTouch(event: (event: TouchEvent) => void): T：记录按下、抬起和按钮尺寸（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouch）
- 标题栏是 20dp 无界白色圆、圆心在按钮内容区中心；改为 onTouch 加图标下层 40vp 圆后与源端一致：修法（出处：卡里修好并验证过）
针对本应用要查的：
- 标题栏按钮涟漪的半径和颜色：源主题链里的 actionBarItemBackground（或 Toolbar 按钮的 background），再到 Android SDK 平台资源 data/res/drawable 下对应 xml 和 colorControlHighlight；读 android:radius 作圆半径；颜色按 colorControlHighlight 解析，深色栏上是浅色
未核实：圆心位置（按钮内容区中心）出自对照设备实测
来源：1 张卡，1 个应用
- case-b76baecf687e5ab5817a（Sokoban）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
