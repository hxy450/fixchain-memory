# 由主题决定的颜色（?attr/ 引用、android:theme 覆盖、状态栏图标明暗）

agent 会看到什么：读到源布局、主题里由主题决定的颜色：?attr/colorPrimary 这类主题属性、AppBarLayout / Toolbar 的 android:theme 覆盖、主题继承来的状态栏图标明暗；规格只写属性名、单个色值或只写底色，看不出引用类型，也没有昼夜两态的解析值

## 通用查法

### 规格写主题决定的颜色时，保留 ?attr/ 引用原样，并顺主题链读出昼夜两态的解析值

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

## 规矩

- rule-c5c564ae43ec｜页面规格写颜色时保留 ?attr/ 和 @color/ 的区别，不简写成属性名或只列色值｜读到：源布局写 android:background="?attr/colorPrimary"，别处又有 @color/colorPrimary 写死的引用；写错：页面规格或设计令牌写「背景 colorPrimary」或只列十六进制值，看不出是主题属性还是写死色
- rule-ab8e4a5c5933｜页面规格的顶栏写明 android:theme 覆盖和解析后的昼夜标题色、图标色及默认字号字重｜读到：页面 include 的工具栏布局里 AppBarLayout 带 android:theme（ThemeOverlay.AppCompat.Light，夜间 .Dark），Toolbar 只写 background=?attr/colorPrimary；写错：页面规格的「顶栏」只写「include 工具栏布局、背景 colorPrimary」，没写主题覆盖、解析后的标题色和导航图标色（昼夜两态）、Toolbar 默认字号字重
- rule-4105e7187ff6｜规格写主题链时写明状态栏图标明暗，状态栏外观的验收同时列底色和图标色｜读到：源主题继承 Theme.AppCompat.Light.NoActionBar 一类主题，用 colorPrimaryDark 或 setStatusBarColor 设状态栏底色；写错：规格的主题链和映射只写底色（如「contentColor 同步」「状态栏配色 parity」），没写 windowLightStatusBar 或运行时标志是否存在、图标是白是深；状态栏验收条目只判底色
- rule-07b48a5ef67f｜资源映射表记主题属性时，写明浅深解析值和对应的颜色键，不只用文字记值｜读到：源图标、控件引用了主题属性（?attr/…）着色；写错：资源映射文档里只用文字记了「属性=浅色值/深色值」，没写对应的 color.json 键名，或者写了 SVG 固定取浅色值却没写深色怎么适配
