# 继承按钮、只换背景的自定义控件

agent 会看到什么：源码里自定义控件继承 Button / AppCompatButton / MaterialButton，只 setBackgroundResource 换背景（有的再 setEnabled 或 setAutoSizeTextTypeUniformWithConfiguration），规格写成「可点击 + 背景着色」、只抄字号区间，或把 setEnabled 直译成 .enabled(false)

## 通用查法

### 继承按钮的控件只换背景时，规格顺 buttonStyle 查出样式仍带来的投影、内边距、字体和禁用态

审的是：规格
触发（任一种）：
- 读到：源码里自定义控件继承 Button / AppCompatButton / MaterialButton，只调 setBackgroundResource 换背景（或再 setEnabled），没有 setStateListAnimator(null)、setElevation(0) 或 borderless 样式；写错的样子：规格把它写成「可点击 + 背景着色」，没写按钮样式带来的投影、内边距、字体和禁用外观，或把 setEnabled 直译成 .enabled(false)
适用范围：规格提取阶段给继承按钮、只换了背景的自定义控件写组件契约和转换决策时
做法：
- 从主题的 buttonStyle 顺 parent 链找到平台或库的按钮样式，读出它提供的 stateListAnimator、背景的 padding 和 textAppearance
- 逐项判断换背景后还生效的：新背景不带 padding 时样式内边距保留，stateListAnimator 的投影和按下抬升保留；禁用外观看背景和 textColor 有没有 state_enabled 分支
- 把仍生效的各项按读出的数值写进组件契约；读不出的标待实测并写实测方法
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Material.Button：background = @drawable/btn_default_material，textAppearance = ?attr/textAppearanceButton，stateListAnimator = @anim/button_state_list_anim_material：平台按钮样式除背景外还提供字体和高程动画（出处：Android SDK 平台资源 data/res/values/styles_material.xml，Widget.Material.Button（按应用的 compileSdk 取对应平台））
- Base.Widget.AppCompat.Button 在 v21 以上的 parent 是 android:Widget.Material.Button：AppCompat 主题下的按钮沿用平台 Material 按钮的这些项（出处：androidx.appcompat:appcompat 包内 res/values-v21/values-v21.xml，Base.Widget.AppCompat.Button（按应用依赖的版本））
- 新背景的 getPadding 返回 true 时才改写内边距：换成不带 padding 的 shape 背景时，原样式带来的内边距保留（出处：android.view.View#setBackgroundDrawable）
- button_elevation_material = 2dp，button_pressed_z_material = 4dp：例：平台 Material 按钮静止态投影 2dp，按下再抬 4dp（出处：Android SDK 平台资源 data/res/values/dimens_material.xml，button_elevation_material、button_pressed_z_material（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 按钮实际用的样式：源工程主题 XML 里 buttonStyle（或 android:buttonStyle）的取值，顺 parent 到平台的 styles_material.xml 或 androidx.appcompat:appcompat、com.google.android.material:material 包内 res/values/values.xml；找到提供 stateListAnimator、background / padding、textAppearance 的那一项；例：AppCompat 主题、v21 以上落到平台 Widget.Material.Button
- 投影、内边距和字体的数值：stateListAnimator 指向的 res/anim 文件、背景 drawable、textAppearance 指向的样式；读各状态 elevation、translationZ 引用的 dimen；背景 drawable 的 inset 与 shape padding 相加；读 textAppearance 的 fontFamily、textStyle
- 源端禁用外观来自哪里：源工程 res/drawable*/ 下背景 <selector> 有没有 android:state_enabled="false" 的 <item>，res/color*/ 下 textColor 引用的是不是 <selector>；有分支的取分支里的颜色写进规格；没有的，禁用态就是代码换上的背景加固定字色
未核实：AppCompatButton 默认取 buttonStyle 属性出自库代码，族里规矩没有核到源码
来源：3 张卡，1 个应用
- case-1320d29332e802ec2cce（Privacy Friendly 2048）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 2
- case-314b7ba3e75b6d6b3a9d（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-787e380c801fb46d89a7（Privacy Friendly 2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1

## 规矩

- rule-9aaf86f2a028｜自定义块继承 AppCompatButton 只换背景时，组件契约写明按钮样式的默认投影｜读到：自定义块 extends AppCompatButton / Button，只调 setBackgroundResource 换背景，没有 setStateListAnimator(null)、setElevation(0) 或 borderless 样式；写错：规格里这个控件只写成「可点击 + 背景着色」或字号自适应，没写静止态投影和按下态抬升
- rule-684b7398ad07｜按钮子类用自动字号时，规格写出内容区（尺寸减内边距）、两向约束和按钮字体，不只抄字号区间｜读到：源码在继承 Button / AppCompatButton / MaterialButton 或带 style 的 TextView 上调用 setAutoSizeTextTypeUniformWithConfiguration，或写 autoSizeTextType="uniform"；构造里只 setBackgroundResource 换了背景；写错：规格映射行只写字号区间（「字号域 [min,max]」）加一句「自适应块宽 / 容器」，把按钮说成「仅为可点击+背景着色」，具体自适应属性留给实现期对 d.ts，风险标「低」
- rule-eed401c219ec｜禁用外观只靠换背景且字色固定时，规格写换背景加拦截点击，不用 .enabled(false)｜读到：源码先 setBackgroundResource(R.drawable.…) 换成灰底再 setEnabled(false)（或布局 android:enabled="false"），背景 drawable 的 <selector> 没有 android:state_enabled 分支，android:textColor 是固定颜色而非 ColorStateList；写错：规格的转换决策写「.enabled(…) + 背景切换」「enabled(false) 同时拦截点击」，没提 ArkUI 禁用态会对整个组件降透明，也没给禁用态的取色判据
