# android:background 引用 drawable 时，先看它是位图、9-patch 还是选择器再写目标

审的是：代码
触发（任一种）：
- 读到：源控件的 android:background 引用 @drawable/…，或 style 引用的框架样式（@android:style/…）带背景：位图、带透明边缘或装饰的位图、.9.png、<selector> 状态选择器；写错的样子：目标凭名字写背景：Image 用默认或 ImageFit.Cover 裁切、背景图下垫了品牌色、只写 Color.Transparent 加默认按压，没对照 drawable 的实际内容
适用范围：安卓控件以 android:background（含样式带来的背景）显示 drawable，迁成 ArkUI 组件背景时
做法：
- 顺着 android:background 或 style 的引用打开实际的 drawable（应用资源，或 Android SDK 平台资源里的框架背景），看它是普通位图、带透明边缘或装饰的位图、9-patch 还是 <selector>
- 按类型写目标：铺满容器的位图写 Image(...).objectFit(ImageFit.Fill)；透明处露出的底色取页面背景色；选择器按 state 换图，不用默认压暗代替
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- View 背景 drawable 的 bounds 设为 (0, 0, mRight - mLeft, mBottom - mTop)；BitmapDrawable 默认 gravity 是 Gravity.FILL：源端位图背景按容器边界拉伸铺满，不保持宽高比（出处：android.view.View#setBackgroundBounds；android.graphics.drawable.BitmapDrawable 的 BitmapState.mGravity）
- ImageFit.Fill：不保持宽高比缩放，图片填满显示边界；ImageFit.Cover：保持宽高比缩放，使两边都大于等于显示边界（超出部分被裁）：Fill 对应 View 背景的拉伸铺满，Cover 会裁掉一部分（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，ImageFit.Fill、ImageFit.Cover）
- windowBackground：format="reference|color"：布局根没写背景时，页面底色来自 Activity 主题的这一项（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowBackground（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 背景 drawable 的实际内容：源工程 res/drawable*、mipmap* 里按名找 android:background 引用的文件；引用框架样式时到 Android SDK 平台资源 platforms/android-<应用 compileSdk>/data/res 下的 drawable/*.xml 选择器和 drawable-<密度>/*.9.png；位图看有没有透明边缘、装饰元素在图中的位置（占图宽的比例）；选择器逐个 state 记下对应的图；9-patch 右、下边的黑线给出内容内边距，按密度换算成 vp
- 透明处露出的页面背景色：源工程布局 XML 里页面根布局（或包住它的外层容器）的 android:background；根布局没写时看 Activity 主题的 android:windowBackground；读出颜色值，写在背景图所在组件和页面根容器的 backgroundColor 上
未核实：9-patch 背景在目标端按拉伸区缩放的写法，族里的卡没验证
来源：3 张卡，3 个应用
- case-25f05bb6ccf6238a63a1（android-train-ticket-vest7）：做法第 2 步 ← 建议 1
- case-268d985fb35cb7ff1cde（Blockinger）：做法第 1 步 ← 建议 2
- case-d827908975df4e90ae2b（app_hnaccurateweather_live_android）：做法第 2 步 ← 建议 2
