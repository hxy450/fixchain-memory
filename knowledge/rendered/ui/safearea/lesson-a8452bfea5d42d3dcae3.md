# 开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 navigationBarColor、targetSdk≤34）时底部保留不透明导航栏底色；全屏后前景按测得的避让区逐边补 padding（顶部加在包住标题栏的层，底部加在伸到窗口底边的层）；expandSafeArea 只让背景越过安全区，预设系统标题栏也不会自动避让

## 何时使用

界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让、决定各边背景是否延伸时；转换承载内嵌子页的壳 NavDestination、移植 Android insets 代码，或入口根 Navigation 四向 expandSafeArea 后逐页核对时

## 适用情境

规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。也包括源端只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor，没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION，targetSdk≤34：导航栏是不透明黑底，应用内容止于其上。也包括页面只给标题栏补了顶部避让，伸到窗口底边的内容（如按 min(宽,高) 取边长的棋盘）没有底部避让。也包括壳页承载声明豁免安全区、自绘工具栏的内嵌子页，源端顶部 inset 由子 Fragment 的 AppBarLayout 或 Toolbar 根布局 fitsSystemWindows 隐式消费；或 NavDestination 页保留预设系统标题栏。

## 原因

setWindowLayoutFullScreen(true) 让窗口内容铺到系统栏下，expandSafeArea 只允许容器背景延伸进安全区，两者都不会给前景留出避让空间；既不测量避让区也不补 padding，标题与返回键就画进状态栏。只补顶部时，伸到窗口底边的内容落进导航条区（来源中横屏棋盘最下一行与重开按钮被盖住）。“透明状态栏”也不等于整窗沉浸：源端导航栏不透明时，全屏后让页面底色填进导航区就与源端不同。来源中规格模板要求所有全屏页按四层架构实现，却没问每条系统栏在源端是什么样；只照搬源 Activity 显式写出的 insets 代码会漏掉经 fitsSystemWindows 隐式消费的顶部；预设系统标题栏不会因根容器扩展而自动避让。

## 做法

1. 开全屏前逐边列出源端状态栏、导航栏的颜色与是否沉浸：只有源端让内容画到某条系统栏下（enableEdgeToEdge、LAYOUT_HIDE_NAVIGATION、应用主题或代码显式设了透明 navigationBarColor，或 targetSdk≥35 且主题没有用 windowOptOutEdgeToEdgeEnforcement=true 退出强制，targetSdk≥36 时这项退出无效；只继承平台主题、没另设 navigationBarColor 且不被强制 edge-to-edge 时，AOSP 配置下导航栏是黑色），或源窗口背景按整窗铺满（Material / AppCompat 系主题下按窗口尺寸拉伸或定位的位图背景，见 lesson-0e1c846868f2683cc280 第 1 步「窗口背景层」）时，才让该边背景延伸；源端导航栏不透明时，全屏后在底部避让区叠同色、不参与命中的占位，不让页面底色填充。
2. 规格把沉浸式实现委托给具名 skill 时，先完整加载该 skill，按其分层清单（窗口全屏、避让区测量、前景 padding）实现，不以自拟的最简方案代替；找不到 skill 时在实现记录中写明缺口。
3. 用 getWindowAvoidArea(TYPE_SYSTEM) 的 topRect.height 取顶部避让；底部取 TYPE_SYSTEM 与 TYPE_NAVIGATION_INDICATOR 两者 bottomRect.height 的较大值。经 UIContext 的 px2vp 换算后按边落实：顶部加在包住标题栏的那一层，底部加在伸到窗口底边的内容层（入口尚未开全屏时也接上；共享窗口模型在入口未开全屏时发布 0，因为非沉浸式布局下系统已替内容避开状态栏和导航区域），按 min(宽,高) 取边长的区域在避让之后测量；在 avoidAreaChange 时更新。背景需要延伸到系统栏下时，才在背景节点自身加 expandSafeArea；Navigation、NavDestination 自 API 11 起默认带 SYSTEM 类型、TOP 与 BOTTOM 两边的 expandSafeArea，某边背景不该延伸时在该组件上显式重写 edges。
4. 壳页承载声明豁免安全区的内嵌子页时，根容器同时补顶部与底部避让；移植 insets 时逐边核对四边各由谁负责，包括经 fitsSystemWindows 隐式消费的顶部。
5. 需要标题栏的全屏 NavDestination 页用 hideTitleBar(true)，自绘工具栏并给其所在容器加顶部避让；除非在根容器扩展状态下实测确认，不预设系统标题栏会自动避让。

## 可选检查

- 工程开启了全屏布局，却找不到任何 getWindowAvoidArea 读取或基于避让高度的 padding 时，视为安全区未落实；有设备时截图核对标题与状态栏的纵向区间不重叠。
- 开启全屏的一方逐页 grep 顶部与底部避让的消费点：只处理了顶部或只处理了底部的页面不算完成，并在横屏下核对贴底内容不落进导航条区。

来源支持：8 张卡 · 已知 6 次迁移（部分未记录） · 已知 6 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36 平台资源（themes_material.xml、themes_device_defaults.xml、colors.xml、config.xml 另对照 android-30、33、34、35、37.0）；android-36.1 的源码；androidx.activity:activity 1.8.1（字节码）；androidx.activity:activity 1.8.1、1.13.0 源码包；androidx.appcompat:appcompat 1.1.0、1.8.0；com.google.android.material:material 1.4.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 做法第 1 步〕View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 让窗口按状态栏隐藏的样子布局（内容可画到状态栏下），只涉及状态栏；SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION 才让窗口按导航栏隐藏的样子布局；两者都已弃用，非浮动窗口改用 Window.setDecorFitsSystemWindows(false)
- 〔适用情境 / 做法第 1 步〕应用主题和代码都没有另设 navigationBarColor、窗口没有被强制 edge-to-edge、设备的 config_navBarDefaultTransparent 为 false（AOSP 取值；android-34 起的平台资源才有这一项）时，PhoneWindow 把导航栏画成 navigation_bar_compatible（黑色）；android-34 起（核到 37.0）平台 Theme.Material、Theme.Material.Light 和继承它们的 DeviceDefault 主题的 navigationBarColor 写的是 navigation_bar_default（#00808080），PhoneWindow 把这个值当作没设，android-33 及以前的平台资源里直接写 @color/black；AppCompat（1.1.0–1.8.0）、MaterialComponents 和 Material3（material 1.4.0–1.14.0）主题都不另设 navigationBarColor，沿用平台主题这一项
- 〔适用情境 / 做法第 1 步〕应用主题和代码都没有另设 statusBarColor、窗口没有被强制 edge-to-edge 时，状态栏颜色取主题的 android:statusBarColor：平台 Theme.Material.Light 为 ?attr/colorPrimaryDark 即 #FF757575，Theme.Material 为 #FF000000（android-30 至 37.0 相同）；Theme.DeviceDefault.Light 在 android-30 为 #FF757575，android-33 起取系统调色板色 system_neutral1_50（平台资源里 android-33、34 为 #FFF0F0F3，35、36 为 #FFF1F0F7，37.0 为 #FFF1F0F6）；Theme.DeviceDefault 在 android-30 为 #FF000000，android-33、34 为 #FF191C1E，35 起（核到 37.0）为 #FF1A1B20；targetSdk ≥ 35 被强制 edge-to-edge 时状态栏一律透明
- 〔适用情境 / 做法第 1 步〕AppCompat（1.1.0 至 1.8.0）、MaterialComponents 和 Material3（material 1.4.0 至 1.14.0）的应用主题都不另设 android:statusBarColor，API 21 起沿用平台主题的 ?attr/colorPrimaryDark，取到的是库主题自己的 colorPrimaryDark：Theme.AppCompat.Light #FF757575、Theme.AppCompat #FF000000、Theme.MaterialComponents.Light #FF3700B3；Material3 主题把 colorPrimaryDark 指向 colorPrimary，Theme.Material3.Light 为 #FF6750A4、Theme.Material3.Dark 为 #FFD0BCFF；应用主题、代码没有另设且没有被强制 edge-to-edge 时状态栏就是这个颜色
- 〔适用情境 / 做法第 1 步〕应用 targetSdk ≥ 35（VANILLA_ICE_CREAM）时窗口被强制 edge-to-edge：框架不按 insets 收缩内容视图，状态栏颜色设为透明且 setStatusBarColor 不起作用；Window.setNavigationBarColor 的文档也写导航栏颜色透明、改不了，源码里导航栏颜色仍被留作对比遮罩：窗口要求导航栏对比度（targetSdk ≥ 29 且主题没另设 enforceNavigationBarContrast 时为 true）且系统没有抑制导航栏遮罩时，主题或代码给的不透明导航栏色按 80% 不透明度画成遮罩，透明色则画系统默认遮罩（浅色外观为 90% 白），不要求对比度时画成透明；主题的 windowOptOutEdgeToEdgeEnforcement=true 可以退出强制，targetSdk ≥ 36（BAKLAVA）时这项被忽略
- 〔适用情境〕源端 targetSdk 34、只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor、没设 navigationBarColor 时，安卓设备上导航栏取色为黑底，应用内容止于导航栏上方
- 〔适用情境 / 做法第 1 步〕androidx.activity 1.8.1 的 enableEdgeToEdge() 在 API 21 起都调 setDecorFitsSystemWindows(window, false)，让内容画到状态栏和导航栏下；不传样式时：API 29 起状态栏、导航栏颜色都设为透明，关掉状态栏对比度强制、打开导航栏对比度强制，导航栏颜色透明且打开对比度强制时由系统决定要不要画对比遮罩；API 26–28 状态栏透明、导航栏按日夜设成半透明遮罩（浅色 #E6FFFFFF、深色 #801B1B1B）；API 23–25 导航栏用深色遮罩 #801B1B1B；API 21–22 改加 FLAG_TRANSLUCENT_STATUS、FLAG_TRANSLUCENT_NAVIGATION。1.13.0 不传样式时 API 29 起的颜色结果相同（API 35 起样式不透明才另加保护层视图），另把 layoutInDisplayCutoutMode 在 API 28、29 设为 SHORT_EDGES、API 30 起设为 ALWAYS
- 〔适用情境 / 做法第 4 步〕android:fitsSystemWindows 为 true 时按状态栏等系统窗口调整这个 View 的 padding，给它们留出空间（只在非嵌入的 Activity 里生效）；View 没有覆写 fitSystemWindows、onApplyWindowInsets 时用 insets 直接替换它原有的 padding，并把这部分系统窗口 insets 标为已消费：它的子 View 收不到，targetSdk 低于 30 时排在它后面的兄弟 View 也收不到，targetSdk ≥ 30 时兄弟各自收到父布局给的 insets
- 〔原因 / 做法第 3 步〕非沉浸式布局下应用界面内容默认避开状态栏和导航区域；沉浸式布局下可布局区域延伸到整个窗口，内容可与状态栏、导航区域重叠（系统界面元素层级始终在上），需要应用自己做布局避让
- 〔原因 / 做法第 3 步〕Window.setWindowLayoutFullScreen(true)（Promise 版 API 9 起）把应用主窗口或子窗口设为沉浸式布局：布局不避让状态栏与三键导航栏，组件可能与其重叠；设为 false 时布局避让它们，组件不会与其重叠；进入或退出沉浸式布局不改变窗口尺寸和位置（文档写 API 10 起窗口默认全屏大小、由组件模块控制布局）
- 〔原因 / 做法第 3 步〕expandSafeArea(types?, edges?) 让组件在不改变布局的情况下把绘制区域扩展到安全区外，不给前景让出避让空间；不传参时 types 取 SYSTEM、CUTOUT、KEYBOARD，edges 取 TOP、BOTTOM、START、END 四边；安全区不限制内部组件的布局和大小
- 〔做法第 1、3 步〕Navigation、NavDestination 自 API 11 起默认带安全区扩展：Navigation 为 expandSafeArea([SYSTEM, KEYBOARD, CUTOUT], [TOP, BOTTOM])，NavDestination 为 expandSafeArea([SYSTEM], [TOP, BOTTOM])，可以重写覆盖
- 〔做法第 3 步〕Window.getWindowAvoidArea(type)（API 9 起）同步返回 AvoidArea，含 topRect、bottomRect、leftRect、rightRect；Rect 的 left、top、width、height 单位是 px；避让区域可能为 0；AvoidArea.visible 没有实际含义
- 〔做法第 3 步〕AvoidAreaType.TYPE_SYSTEM = 0 是系统默认区域，文档写明包含状态栏和三键导航栏区域；TYPE_NAVIGATION_INDICATOR = 4（API 11 起）是底部导航区域，文档写三键导航显示时底部导航避让区域始终存在
- 〔做法第 3 步〕目标 SDK 为 API 24（HarmonyOS 6.1.1）的设备上：三键导航时 TYPE_NAVIGATION_INDICATOR 的 bottomRect.height 为 0，底部高度在 TYPE_SYSTEM 的 bottomRect 里；手势导航时 TYPE_SYSTEM 的 bottomRect.height 为 0，手势条高度在 TYPE_NAVIGATION_INDICATOR 里；这与文档 AvoidAreaType「三键导航显示时底部导航避让区域始终存在」的写法不同，运行时表现以卡里实测为准
- 〔做法第 3 步〕Window.on('avoidAreaChange', callback)（API 9 起；回调参数类型 AvoidAreaOptions 自 API 12 起，带 type 和 area）在当前窗口系统避让区变化时回调，文档列的常见触发有窗口在全屏、悬浮、分屏模式间切换，窗口旋转，折叠屏折叠展开；on('windowSizeChange') 的回调只带窗口尺寸 Size，不带避让区
- 〔做法第 3 步〕目标 SDK 为 API 24 的设备上横屏时系统隐藏状态栏，避让区的变化晚于 windowSizeChange 到达；只在 windowSizeChange 回调里重读 getWindowAvoidArea 拿到的是旧的避让值
- 〔做法第 3 步〕UIContext.px2vp(value)（API 12 起）把 px 换成 vp；本机 SDK 的 API 23 起还可以用 @Env(SystemProperties.WINDOW_AVOID_AREA) 直接取以 vp 为单位的避让区（UIEnvAvoidAreaVP），避让区变化时自动更新
- 〔做法第 1 步〕hitTestBehavior(HitTestMode.None) 让组件自身不响应触摸测试，也不阻塞子节点、兄弟节点和祖先节点的触摸测试
- 〔原因 / 做法第 2、3 步〕目标 SDK 为 API 24 的模拟器上：入口 setWindowLayoutFullScreen(true)、只在根 Navigation 内的 Column 上加 expandSafeArea([SYSTEM], [TOP, BOTTOM])、不读避让区也不补 padding 时，Tab 页标题和 NavDestination 标题、返回键画进状态栏（截图测得标题字形的纵向区间落在状态栏区间内）
- 〔做法第 5 步〕目标 SDK 为 API 22 的设备上：根 Navigation 四向 expandSafeArea、窗口为沉浸式布局时，保留 .title() 系统标题栏的 NavDestination 页在截图里标题栏叠进状态栏；这一表现出自修复会话截图，卡里没有查到系统标题栏避让的官方规则
- 〔做法第 5 步〕NavDestinationAttribute.hideTitleBar(value)（API 9 起）设置是否隐藏 NavDestination 的标题栏，没有设时为 false（显示）；API 13 起另有 hideTitleBar(hide, animated) 重载
- 〔做法第 3 步〕同一个容器上同时写固定 .height(N) 和 .padding({ top: 避让值 }) 时，避让值算在 N 之内，标题栏内容区被压扁，可见高度小于 N
