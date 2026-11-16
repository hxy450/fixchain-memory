# android:background 引用的 shape drawable 与 CardView 圆角

agent 会看到什么：读过的布局里控件的 android:background 引用 @drawable/…（<shape> 的 <solid>、<corners>、<stroke>，或各布局变体不同），列表项或 holder 动态加入的视图根是 CardView 带 app:cardCornerRadius；交回的底色、圆角、描边是猜的或照抄兄弟页，shape 被当成 backgroundImage，border() 冲掉了圆角

## 通用查法

### 背景引用 @drawable 或 CardView 圆角时，打开源资源读出 shape 各值再写属性

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

## 规矩

- rule-401b7b498310｜背景 drawable 是 <shape> 时转成圆角、底色和边框，不用 backgroundImage｜读到：android:background="@drawable/…" 指向的 drawable XML 根标签是 <shape>，里面有 <solid android:color>、<corners android:radius>（可能还有 <stroke>）；写错：目标写成 .backgroundImage($r('app.media.…')) 加 .backgroundImageSize(ImageSize.Cover)，把 shape 当位图，铺的是目标工程里同名的小尺寸圆角 SVG
- rule-27d3ce7f7ff9｜布局引用 shape drawable 和列表项布局时，照其中的颜色、各角圆角、描边、外边距写属性｜读到：控件的 android:background 引用 @drawable/… 形状（<shape> 里有 <solid>、<corners android:topLeftRadius …>、<stroke>），列表项布局带 android:layout_margin，输入框带起始的搜索图标；写错：ArkUI 里背景色和圆角是猜的：四角写成同一个圆角、没有 .border 描边、没有搜索图标；网格只设了间距（gutter）而项上没有 .margin
- rule-32e6b74e679c｜borderRadius 后接不带 radius 的 border() 时，圆角写进 border 的 radius｜写错：同一个组件先 .borderRadius(…) 再 .border({ width: …, color: … })，border 的参数里没有 radius
- rule-e71586390299｜源码运行时 setBackgroundResource 只覆盖被调用的控件，其余控件按各布局变体 XML 的背景取形状｜读到：Activity 代码只对部分控件变量调用 setBackgroundResource / setBackground；layout-land 变体里同一控件 android:background="@color/…"（纯色），竖屏变体是带 <corners> 的 shape drawable；写错：目标组件对所有按钮无条件写 .borderRadius(6)，没被运行时代码改背景的控件在横屏也成了圆角；注释写「运行时覆盖了两套 XML 背景」
- rule-2e252c80ab6b｜源按钮自绘底色或渐变改成 SaveButton 时，底色和圆角设在 SaveButton 自身，不设透明底｜读到：源按钮的 style 或背景 drawable 用 <gradient android:startColor / android:endColor>、<corners android:radius> 或半透明 <solid> 画底；派工或规格要求这个按钮改用 SaveButton 安全控件；写错：SaveButton 上写 .backgroundColor(Color.Transparent)，底色、linearGradient 和 borderRadius 交给外层 Row / Column 容器，注释把「渐变容器承载 + 透明 SaveButton」定为范式
- rule-7708071d1446｜holder 动态 addView 的视图要打开它的布局，取 CardView 的 cardCornerRadius｜读到：holder 把另一个组件的根视图 addView 进内容容器，那个视图的布局根是 CardView（或其子类），写了 app:cardCornerRadius="@dimen/…"；写错：目标端卡片的 .borderRadius($r(...)) 没有出自这个 CardView 布局，取的是别的布局或兄弟页的值，和源端 cardCornerRadius 不一致
- rule-73b3bdba2f8c｜参考兄弟页的卡片 Builder 时只借结构，圆角、描边、底色回本页源码核对｜读到：兄弟页 .ets 里已有卡片 @Builder（白底、.border(...)、.borderRadius(...)）；写错：本页卡片的圆角、描边、底色数值照搬兄弟页 Builder，没回本页安卓源码核对
- rule-5b834d26cf72｜源背景是带底边或描边的 layer-list 时，目标显式补 border 或 padding｜读到：源控件 `android:background` 引用的 drawable 是 `<layer-list>`：下层 item 是一种颜色，上层 item 用 `android:bottom` 等 inset 让下层露出一条边，或有 `<stroke>`；写错：目标只写了 `.backgroundColor(...)` 或 `.backgroundImage(...)`，露出的底边、描边缺失
