# 背景引用 @drawable 或 CardView 圆角时，打开源资源读出 shape 各值再写属性

审的是：代码
触发（任一种）：
- 读到：控件的 android:background="@drawable/…"（各布局变体可能不同），或列表项的根是 CardView，写了 app:cardCornerRadius="@dimen/…"；写错的样子：目标的 .backgroundColor / .borderRadius / .border 是猜的、照抄兄弟页的，或把 shape 写成 .backgroundImage
适用范围：迁移控件背景形状、卡片圆角和描边时
做法：
- 顺着引用打开源资源：@drawable/… 看同名 XML 的根标签，<shape> 读 <solid>、<corners>（逐角）、<stroke>；CardView 读 app:cardCornerRadius；@dimen、@color 解析到值；每个布局变体各读一次
- 写成显式属性：.backgroundColor(<solid 的 color>)，圆角写 .borderRadius(…)（四角不同用 BorderRadiuses），有 <stroke> 时写 .border({ width, color, radius })；dp 数值照写成 vp，位图、九宫格才用 backgroundImage
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- DrawableCorners 的 radius 是 dimension；GradientDrawableSolid 的 color 是 color；GradientDrawableStroke 有 width、color：shape 里各子标签的属性和格式，分别对应到 borderRadius、backgroundColor、border（出处：Android SDK 平台资源 data/res/values/attrs.xml，DrawableCorners、GradientDrawableSolid、GradientDrawableStroke（按应用的 compileSdk 取对应平台））
- BorderOptions.radius?: BorderRadiuses | Length | LocalizedBorderRadiuses：描边和圆角可以写在同一个 .border({ width, color, radius }) 里（出处：鸿蒙 SDK 的 ets/component/units.d.ts，BorderOptions.radius）
- border() 不带 radius 时，前面 borderRadius 设的圆角被重置；给 border 带上 radius 后圆角恢复：有描边时圆角要写进 border（出处：卡里修好并验证过）
- CardView 的 cardCornerRadius 是 dimension 属性；不写时 Base.CardView 用 cardview_default_radius = 2dp：例：CardView 没写 cardCornerRadius、也没有样式覆盖时圆角是 2dp（出处：androidx.cardview:cardview 包内 res/values/values.xml，CardView 的 cardCornerRadius、cardview_default_radius（按应用依赖的版本））
针对本应用要查的：
- 背景 drawable 的类型和 shape 里的取值：源工程 res/drawable*/ 下与 @drawable/ 引用同名的 XML 或图片；各 res/layout*/ 变体里同一控件的 android:background；根标签是 <shape> 的读 corners、solid、stroke；.png/.jpg/.9.png 按位图处理；@color 纯色是直角；运行时 setBackgroundResource 只改被调用的那个控件
- 卡片的圆角真值：列表项布局或 holder addView 的视图 inflate 的 res/layout XML 根 CardView 的 app:cardCornerRadius，再到 res/values 下 dimens.xml 找同名 dimen；解析到 dp 值，写进目标端同名 float 资源；CardView 没写 cardCornerRadius 时查它的 style 或库默认
未核实：CardView 会把子视图裁成圆角；目标端只写 borderRadius 是否还要配 .clip(true) 才裁子组件，卡里没验证
来源：5 张卡，5 个应用
- case-06c7df8f8d85e13580ac（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 2
- case-14fd5b307673d523bead（Privacy Friendly 2048）：做法第 1 步 ← 建议 1
- case-5b1b0e2ce03be0dc6d37（组件岛Widget Island）：做法第 1 步 ← 建议 2
- case-7d027e7b2cd42e741308（android-train-ticket-vest7）：做法第 1 步 ← 建议 4
- case-f226842558d82e3f3ad9（AntennaPod）：做法第 2 步 ← 建议 5；取值 3 ← 诊断
