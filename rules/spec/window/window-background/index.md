# 布局根没写背景时透出的窗口背景

agent 会看到什么：读到布局根没写 android:background 或写 @null、铺满的 SurfaceView 没置顶、Activity 用 Translucent 主题或平台主题的 windowBackground；规格写「背景 #某色 透出」「暗底背景（Holo 默认）」「Stack + 底层 Image」「全屏 NavDestination + 半透明遮罩」

## 通用查法

### 页面或透明层下的可见底色，规格按叠放顺序找到提供方并解析到最终值

审的是：规格
触发（任一种）：
- 读到：布局根或容器没写 android:background、写了 @null，或有透明的 SurfaceView、Translucent 主题的页叠在上面；底色要从 Activity 主题的 windowBackground 取；写错的样子：规格写「背景 #某色 透出」「暗底背景（Holo 默认）」「Stack + 底层 Image」，没写可见底色由谁提供、解析出的值
适用范围：规格写页面根背景、透明层透出和画布区域底色时
做法：
- 从看得见的那一层往下逐层核对：控件和布局根的 android:background（没写或 @null 继续往下）、没置顶的 SurfaceView 区域（看它每帧画的底色）、Activity 主题的 windowBackground（Translucent 主题时是下层页面）
- 落到 windowBackground 时沿主题 parent 链到平台主题，在 SDK 平台资源里顺着 @drawable 解析到最终 shape（selector 取默认项，读 gradient 或 solid）
- 规格写提供方和解析出的值（渐变写起止色和 angle）；颜色资源先查有没有被引用，没引用的不当底色
针对本应用要查的：
- 页面所用的主题和它的 windowBackground：源工程 AndroidManifest 的 android:theme、res/values*/styles.xml 的 parent 链；按应用的 compileSdk 取对应平台的 Android SDK 平台资源 data/res/values/themes*.xml 和 data/res/drawable；找该主题的 windowBackground（没写的按 parent 或名字前缀找父主题），顺着 @drawable 解析到 shape；例：parent 为 android:Theme.Holo 时经 screen_background_selector_dark 的默认项解析到 background_holo_dark 渐变（#ff000000 到 #ff272d33，angle 270）
未核实：本族规矩只核对了 android-35 平台资源里 Theme / Theme.Holo 的 windowBackground，别的平台主题没逐个查
来源：2 张卡，2 个应用
- case-2a82c31c11fb4f1c7fa5（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 1、建议 2
- case-31a0a063e8315d356c6c（Bubble Shooter）：做法第 1 步 ← 建议 1

## 规矩

- rule-b9df9e19e976｜源端是 Theme.Holo 等平台主题时，规格把 windowBackground 解析到最终 drawable｜读到：styles.xml 里应用主题 parent="android:Theme.Holo"（或其他 android:Theme.*），布局根没有 android:background；写错：页面规格只写「暗底背景（Holo 默认，取不到精确值处标待核）」没有值；或把窗口背景写成 @color/background_holo_dark 那样的单色 #ff000000
- rule-333a4805996d｜透明层下的页面底色取主题 windowBackground，不把无引用的颜色写成窗口背景｜读到：颜色资源 XML 里定义了某个 <color>，layout、style、Java 里都没有引用它；写错：设计系统色彩表或规格把这个颜色写成某页的窗口背景 / 根布局背景
- rule-66f6d96972e4｜铺满的 SurfaceView 未置顶时，规格写区域可见底色，不把容器背景当画布底层 Image｜读到：容器有 android:background 位图，布局或 onCreate 的 addView 给它加了铺满的 SurfaceView / GLSurfaceView 子类（FrameLayout 默认铺满），源码搜不到 setZOrderOnTop(true)，每帧先 drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR)；写错：规格写「background=@drawable/… → Stack + 底层 Image(ImageFit.Fill)」「Stack{ 背景Image, 画布 }」，把 drawColor(TRANSPARENT, CLEAR) 对成 clearRect，没写这一区域的可见底色
- rule-70c257eb36b0｜透明主题页的规格写明「下层页面保持可见、仅压暗」和透明路由｜读到：源 Activity 用 Translucent 主题（`android:windowIsTranslucent` 为 true、透明 `android:windowBackground`、`android:backgroundDimEnabled`）；写错：规格只写「半透明 Activity → 全屏 NavDestination + 半透明背景遮罩」或「主题级透明 → 页面级蒙层」，没写下层页面要可见、目标路由要透明
