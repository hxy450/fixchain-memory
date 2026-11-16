# 自定义块继承 AppCompatButton 只换背景时，组件契约写明按钮样式的默认投影

审的是：规格
触发（任一种）：
- 读到：自定义块 extends AppCompatButton / Button，只调 setBackgroundResource 换背景，没有 setStateListAnimator(null)、setElevation(0) 或 borderless 样式；写错的样子：规格里这个控件只写成「可点击 + 背景着色」或字号自适应，没写静止态投影和按下态抬升
适用范围：规格里给继承按钮的自定义控件写组件契约时，应用主题是按钮带 stateListAnimator 的 Material / AppCompat 一族
不适用的情形：源码有 setStateListAnimator(null)、setElevation(0) 或用了 borderless 样式时，没有这份默认投影
做法：
- 把按钮样式带来的默认外观写进组件契约：静止态的 elevation 投影（来自 stateListAnimator），按下态另有 translationZ 抬升，数值按应用主题的 buttonStyle 查出
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material.Button 的 stateListAnimator 是 @anim/button_state_list_anim_material：平台按钮样式自带的高程动画（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.Button（按应用的 compileSdk 取对应平台））
- button_state_list_anim_material：启用态 elevation = button_elevation_material，按下态再加 translationZ = button_pressed_z_material：静止态有投影，按下时抬高（出处：Android SDK 平台资源 data/res/anim/button_state_list_anim_material.xml（按应用的 compileSdk 取对应平台））
- button_elevation_material = 2dp，button_pressed_z_material = 4dp：静止态投影 2dp，按下态再抬 4dp（出处：Android SDK 平台资源 data/res/values/dimens_material.xml，button_elevation_material、button_pressed_z_material（按应用的 compileSdk 取对应平台））
- Base.Widget.AppCompat.Button 在 v21 以上的 parent 是 android:Widget.Material.Button：AppCompat 主题下的按钮继承平台 Material 按钮的 stateListAnimator（出处：androidx.appcompat:appcompat 包内 res/values-v21/values-v21.xml，Base.Widget.AppCompat.Button（按应用依赖的版本））
针对本应用要查的：
- 这个按钮实际用的样式和投影数值：源工程的主题 XML 里 buttonStyle（或 android:buttonStyle）的取值，顺着 style 的 parent 一路找到 android:stateListAnimator 和 android:elevation；读出 stateListAnimator 指向的动画文件里各状态的 elevation、translationZ 引用的 dimen；例：AppCompat 主题、v21 以上用平台 Widget.Material.Button，静止 2dp、按下再加 4dp
未核实：AppCompatButton 默认取 buttonStyle 属性出自库代码，本机没有源码
来源：1 张卡，1 个应用
- case-1320d29332e802ec2cce（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；例外 1 ← 建议 2
