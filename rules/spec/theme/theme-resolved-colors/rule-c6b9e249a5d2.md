# 规格写主题决定的颜色时，保留 ?attr/ 引用原样，并顺主题链读出昼夜两态的解析值

审的是：规格
触发（任一种）：
- 读到：源布局或主题里的颜色、外观来自主题：?attr/colorPrimary 这类主题属性、AppBarLayout / Toolbar 的 android:theme 覆盖、主题继承来的 windowLightStatusBar；写错的样子：规格只写属性名（「背景 colorPrimary」「contentColor 同步」）或一个十六进制值，看不出是主题属性还是写死色，也没有昼夜两态的解析值
适用范围：规格提取阶段描述源端由主题决定的颜色、顶栏文字和图标色、状态栏图标明暗时
做法：
- 原样保留引用：?attr/… 写成主题属性（昼夜两态），@color/… 写成写死的单态常量
- 照下面「要查的」顺主题链读出这个属性在昼、夜两态的值，写在引用旁边；落到依赖库或平台主题的，写明落到哪个主题
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- windowLightStatusBar 对应 View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR 和 WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS：主题里查完还要在代码里搜这两个运行时标志（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowLightStatusBar（按应用的 compileSdk 取对应平台））
- 例：顶栏 android:theme 落到 ThemeOverlay.AppCompat.Light 时标题色 #de000000、导航图标色 #8a000000；落到 .Dark 时 #ffffffff、#b3ffffff：一个顺主题链读出的昼夜两态取值（appcompat 1.7.1，样式没自己覆盖文字色时）（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.ThemeOverlay.AppCompat.Light、primary_text_default_material_light、primary_text_default_material_dark、secondary_text_default_material_dark（按应用依赖的版本））
针对本应用要查的：
- 主题属性在昼、夜两态的实际值：源工程 AndroidManifest 里 application / Activity 的 android:theme 和布局里控件的 android:theme，到 res/values、res/values-night 的 styles.xml、themes.xml 里顺 parent 找这个属性的 item；parent 落到依赖库（appcompat、material）时去库包内 res/values/values.xml，落到平台主题时去 Android SDK 平台资源 data/res/values 下的主题文件；样式自己写了这个属性的以样式为准；值是 @color/… 的再到 colors.xml（含 values-night）读出色值，昼、夜各记一个
未核实：控件的 android:theme 覆盖、style 和 Activity 主题三者的先后，族里规矩只在 Toolbar 的 ThemeOverlay 上核过；平台主题落在 data/res/values 下的哪个主题文件，族里规矩没有核实
来源：3 张卡，2 个应用
- case-7af8ba0d85382021da91（Privacy Friendly 2048）：做法第 1 步 ← 建议 2
- case-d5cb8650c08eea9be356（Privacy Friendly 2048）：做法第 2 步 ← 建议 3、建议 1
- case-e2bca560f2a4516d2fb5（2048）：做法第 2 步 ← 建议 4
