# 控件 style 引用 @android:style/… 时，规格按平台资源写各状态背景和内边距，不凭记忆写透明

审的是：规格
触发（任一种）：
- 读到：布局里 Button / ImageButton 写 style="@android:style/Widget.ImageWell" 这类框架样式（或快照的 style-ref 以 @android: 开头），没写 android:background；写错的样子：转换决策写「透明背景无描边」「透明底」「平台默认」，没给出处，也没写按下态和内容内边距
适用范围：规格里为以 @android:style 引用框架样式的控件写转换决策行（背景、边框、按下态、内容内边距）时
做法：
- 到 Android SDK 平台资源 values/styles.xml 找该样式的 background、padding、minHeight、textAppearance，再沿 drawable 解析到选择器各状态的图，逐项写进这个控件的转换决策行
- 以 Widget.ImageWell 为例写成：背景 panel_picture_frame_background（常态 panel_picture_frame_bg_normal，按下 panel_picture_frame_bg_pressed_blue），9-patch 内容内边距 7.5/7/7.5/7dp；查不到的标「待核」，不写「透明/无描边」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <style name="Widget.ImageWell"> <item name="background">@drawable/panel_picture_frame_background</item>：ImageWell 的外观全在这个背景选择器里，不是透明（出处：Android SDK 平台资源 data/res/values/styles.xml，Widget.ImageWell（按应用的 compileSdk 取对应平台））
- state_focused → panel_picture_frame_bg_focus_blue；state_pressed → panel_picture_frame_bg_pressed_blue；默认 → panel_picture_frame_bg_normal：选择器的三种状态图（都是 9-patch）（出处：Android SDK 平台资源 data/res/drawable/panel_picture_frame_background.xml（按应用的 compileSdk 取对应平台））
- 常态灰框、按下蓝框；9-patch 内容内边距 7.5/7/7.5/7dp：从平台资源取图后看到的外观和内边距（出处：卡里修好并验证过）
针对本应用要查的：
- 所引用框架样式的各项外观：Android SDK 平台资源 platforms/android-<应用 compileSdk>/data/res/values/styles.xml 里同名 style，及其 background 指向的 drawable/*.xml 选择器；每个 item 的状态和图名写进决策行；9-patch 的内容内边距看 drawable-<密度> 下那张 .9.png 右边和下边的黑线
来源：1 张卡，1 个应用
- case-268d985fb35cb7ff1cde（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 3 ← 诊断
