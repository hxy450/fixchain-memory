# 开启全屏布局前逐边核对源端系统栏：只沉浸状态栏（透明状态栏、未设 navigationBarColor、targetSdk≤34）时底部保留不透明导航栏底色；全屏后前景按测得的避让区逐边补 padding（顶部加在包住标题栏的层，底部加在伸到窗口底边的层）；expandSafeArea 只让背景越过安全区，预设系统标题栏也不会自动避让

ID：`lesson-a8452bfea5d42d3dcae3` · 版本：7

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-a8452bfea5d42d3dcae3.json` 改了 1 句，后面接了 19 条已核实的平台事实。原文、来源和证据卡见 [memory/ui/safearea/lesson-a8452bfea5d42d3dcae3.lesson.md](../../../../memory/ui/safearea/lesson-a8452bfea5d42d3dcae3.lesson.md)。

## 何时使用

界面实现阶段，为调用 setWindowLayoutFullScreen(true) 的入口壳（根 Navigation + Tabs/NavDestination）落实状态栏与底部导航条避让、决定各边背景是否延伸时；转换承载内嵌子页的壳 NavDestination、移植 Android insets 代码，或入口根 Navigation 四向 expandSafeArea 后逐页核对时

## 适用情境

规格或 ui-manifest 标注全屏页、需要沉浸式安全区，并把 API 细节委托给具名 skill（如 arkts-immersive-safearea）；EntryAbility 开启全屏布局，页面标题由 NavDestination 标题栏或自绘标题承担；源端通常是 enableEdgeToEdge 加 safeDrawingPadding。也包括源端只用 SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN 加透明 statusBarColor，没有 navigationBarColor、windowTranslucentNavigation、HIDE_NAVIGATION，targetSdk≤34：导航栏是不透明黑底，应用内容止于其上。也包括页面只给标题栏补了顶部避让，伸到窗口底边的内容（如按 min(宽,高) 取边长的棋盘）没有底部避让。也包括壳页承载声明豁免安全区、自绘工具栏的内嵌子页，源端顶部 inset 由子 Fragment 的 AppBarLayout 或 Toolbar 根布局 fitsSystemWindows 隐式消费；或 NavDestination 页保留预设系统标题栏。

## 原因

setWindowLayoutFullScreen(true) 让窗口内容铺到系统栏下，expandSafeArea 只允许容器背景延伸进安全区，两者都不会给前景留出避让空间；既不测量避让区也不补 padding，标题与返回键就画进状态栏。只补顶部时，伸到窗口底边的内容落进导航条区（来源中横屏棋盘最下一行与重开按钮被盖住）。“透明状态栏”也不等于整窗沉浸：源端导航栏不透明时，全屏后让页面底色填进导航区就与源端不同。来源中规格模板要求所有全屏页按四层架构实现，却没问每条系统栏在源端是什么样；只照搬源 Activity 显式写出的 insets 代码会漏掉经 fitsSystemWindows 隐式消费的顶部；预设系统标题栏不会因根容器扩展而自动避让。

## 做法

1. 开全屏前逐边列出源端状态栏、导航栏的颜色与是否沉浸：只有源端让内容画到某条系统栏下（enableEdgeToEdge、LAYOUT_HIDE_NAVIGATION、透明 navigationBarColor 或 targetSdk≥35）时，才让该边背景延伸；源端导航栏不透明时，全屏后在底部避让区叠同色、不参与命中的占位，不让页面底色填充。
2. 规格把沉浸式实现委托给具名 skill 时，先完整加载该 skill，按其分层清单（窗口全屏、避让区测量、前景 padding）实现，不以自拟的最简方案代替；找不到 skill 时在实现记录中写明缺口。
3. 用 getWindowAvoidArea(TYPE_SYSTEM) 的 topRect.height 取顶部避让；底部取 TYPE_SYSTEM 与 TYPE_NAVIGATION_INDICATOR 两者 bottomRect.height 的较大值。经 UIContext 的 px2vp 换算后按边落实：顶部加在包住标题栏的那一层，底部加在伸到窗口底边的内容层（入口尚未开全屏时也接上；共享窗口模型在入口未开全屏时发布 0，因为非沉浸式布局下系统已替内容避开状态栏和导航区域），按 min(宽,高) 取边长的区域在避让之后测量；在 avoidAreaChange 时更新。背景需要延伸到系统栏下时，才在背景节点自身加 expandSafeArea。
4. 壳页承载声明豁免安全区的内嵌子页时，根容器同时补顶部与底部避让；移植 insets 时逐边核对四边各由谁负责，包括经 fitsSystemWindows 隐式消费的顶部。
5. 需要标题栏的全屏 NavDestination 页用 hideTitleBar(true)，自绘工具栏并给其所在容器加顶部避让；除非在根容器扩展状态下实测确认，不预设系统标题栏会自动避让。

## 可选检查

- 工程开启了全屏布局，却找不到任何 getWindowAvoidArea 读取或基于避让高度的 padding 时，视为安全区未落实；有设备时截图核对标题与状态栏的纵向区间不重叠。
- 开启全屏的一方逐页 grep 顶部与底部避让的消费点：只处理了顶部或只处理了底部的页面不算完成，并在横屏下核对贴底内容不落进导航条区。

## 已核实的平台事实

核实时用的是 API 23（HarmonyOS 6.1.0，SDK ets 6.1.0.105）；文档用 2026-05 的 OpenHarmony 中文文档副本；安卓 平台资源 android-34（windowOptOutEdgeToEdgeEnforcement 用 android-36）；源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看；每条下面的「写法」是在 SDK 声明里核过的导入语句、归属、签名和枚举成员，写代码时直接照抄。

- 〔做法第 1 步〕导航栏底色：应用主题与代码都没另设 navigationBarColor、未强制 edge-to-edge、设备 config_navBarDefaultTransparent 为 false 时用 navigation_bar_compatible（不透明黑）；targetSdk ≥ 35 强制 edge-to-edge 时两栏颜色置透明、内容不按 insets 适配（出处：com.android.internal.policy.PhoneWindow#generateLayout、#ENFORCE_EDGE_TO_EDGE；Android SDK 平台资源 data/res/values/colors.xml，navigation_bar_compatible；android-36 的 data/res/values/attrs.xml，windowOptOutEdgeToEdgeEnforcement）
- 〔做法第 1 步〕SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN：窗口按已请求 SYSTEM_UI_FLAG_FULLSCREEN 的方式布局，内容可被状态栏盖住；导航栏一侧对应的是另一个标志 SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION（出处：android.view.View#SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN、#SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION）
- 〔做法第 1 步〕hitTestBehavior(value: HitTestMode): T；HitTestMode.None：自身不响应触摸测试，也不阻塞子节点、兄弟节点和祖先节点（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior；ets/component/enums.d.ts，HitTestMode；文档 ts-appendix-enums.md，HitTestMode）
  写法：通用属性与枚举，全局可用，不用导入
        .hitTestBehavior(HitTestMode.None)
        HitTestMode：Default | Block | Transparent | None | BLOCK_HIERARCHY（API 20）| BLOCK_DESCENDANTS（API 20）
- 〔做法第 1 步〕SystemBarProperties.navigationBarColor 在 OpenHarmony 文档里是三键导航栏底色；设备上一次试设 navigationBarColor 没有生效（卡里上机）（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties.navigationBarColor；文档 arkts-apis-window-i.md，SystemBarProperties；卡里修好并验证过（导航栏色））
  写法：import { window } from '@kit.ArkUI';
        window.SystemBarProperties.navigationBarColor?: string  // 经 win.setWindowSystemBarProperties(systemBarProperties: window.SystemBarProperties): Promise<void> 设置
- 〔原因 / 做法第 3 步〕setWindowLayoutFullScreen(true) 时布局不避让状态栏与三键导航栏、组件可能与其重叠；非沉浸式布局下界面内容默认避开状态栏和导航区域；进出沉浸式不改变窗口尺寸和位置；isImmersiveLayout(): boolean（API 20）可查当前状态（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.setWindowLayoutFullScreen、Window.isImmersiveLayout；文档 arkts-apis-window-Window.md，setWindowLayoutFullScreen；immersive-window-feature.md，沉浸式布局）
  写法：import { window } from '@kit.ArkUI';
        // win：入口 onWindowStageCreate(windowStage: window.WindowStage) 里 windowStage.getMainWindowSync(): window.Window；页面里 window.getLastWindow(this.getUIContext().getHostContext()!): Promise<window.Window>
        win.setWindowLayoutFullScreen(isLayoutFullScreen: boolean): Promise<void>  // API 9
        win.isImmersiveLayout(): boolean  // API 20
- 〔做法第 3 步〕getWindowAvoidArea(type: AvoidAreaType): AvoidArea；TYPE_SYSTEM = 0（文档：含状态栏和三键导航栏）、TYPE_NAVIGATION_INDICATOR = 4（底部导航区，三键导航显示时也存在）；状态栏在 topRect、底部导航区在 bottomRect（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowAvoidArea、AvoidAreaType、AvoidArea；文档 arkts-apis-window-e.md，AvoidAreaType；immersive-window-feature.md，避让区域AvoidArea的计算方式）
  写法：import { window } from '@kit.ArkUI';  // win 为 window.Window，同步方法，API 9
        const sys: window.AvoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
        const nav: window.AvoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
        Math.max(sys.bottomRect.height, nav.bottomRect.height)  // px；顶部用 sys.topRect.height
- 〔做法第 3 步〕Rect 的 width、height 单位 px、整数；UIContext.px2vp(value: number): number 把 px 换成 vp（出处：文档 arkts-apis-window-i.md，Rect；鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.px2vp）
  写法：window.Rect = { left: number; top: number; width: number; height: number }
        this.getUIContext().px2vp(value: number): number  // 组件里取 UIContext（getUIContext 自 API 11，px2vp 自 API 12）；Ability 里用 win.getUIContext()
- 〔做法第 3 步〕on(type: 'avoidAreaChange', callback: Callback<AvoidAreaOptions>): void，AvoidAreaOptions = { type: AvoidAreaType; area: AvoidArea }；off(type: 'avoidAreaChange', callback?) 注销（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('avoidAreaChange')、Window.off('avoidAreaChange')、AvoidAreaOptions）
  写法：import { window } from '@kit.ArkUI';  // win 为 window.Window；回调参数 AvoidAreaOptions 自 API 12
        win.on('avoidAreaChange', (data: window.AvoidAreaOptions) => { data.type; data.area.bottomRect.height; });
- 〔做法第 3 步〕横屏时系统隐藏状态栏，避让区的变化晚于 windowSizeChange 到达：在 windowSizeChange 回调里读 getWindowAvoidArea 得到的是旋转前的旧值，新值随之后的 avoidAreaChange 送达（出处：卡里修好并验证过）
- 〔原因 / 做法第 3 步〕expandSafeArea(types?, edges?) 默认 types [SYSTEM, CUTOUT, KEYBOARD]、edges 四边；只扩展绘制区域、不改变布局；只作用于当前组件、不向父子传递；组件边界与安全区重合时才延伸；固定宽高时只支持 TOP、START 方向（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.expandSafeArea；文档 ts-universal-attributes-expand-safe-area.md，expandSafeArea）
  写法：通用属性与枚举，全局可用，不用导入
        .expandSafeArea(types?: Array<SafeAreaType>, edges?: Array<SafeAreaEdge>)  // API 10
        SafeAreaType：SYSTEM | CUTOUT | KEYBOARD；SafeAreaEdge：TOP | BOTTOM | START | END
        例：.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])
- 〔做法第 3 步〕固定 width/height 的组件，内容区 = 设定尺寸减 padding 与 border：避让 padding 加在固定高度的标题栏自身会挤占内容高度，加在外层容器则不会（出处：文档 arkts-layout-development-overview.md，布局元素的组成）
  写法：通用属性，全局可用，不用导入
        .width(value: Length)、.height(value: Length)（API 15 起另可传 LayoutPolicy）；.padding(value: Padding | Length | LocalizedPadding)
        Padding = { top?: Length; right?: Length; bottom?: Length; left?: Length }；Length 为 number 时单位 vp
- 〔适用情境 / 做法第 5 步〕NavDestination 自 API 11 默认 expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP, SafeAreaEdge.BOTTOM])，Navigation 默认 expandSafeArea([SYSTEM, KEYBOARD, CUTOUT], [TOP, BOTTOM])：扩展的只是绘制区，不替前景避让（出处：文档 ts-basic-components-navdestination.md，NavDestination；文档 ts-basic-components-navigation.md，Navigation）
  写法：全局组件，全局可用，不用导入
        Navigation()；Navigation(pathInfos: NavPathStack)（API 10）；NavDestination()
        改默认值：.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.TOP])
- 〔做法第 4 步〕fitsSystemWindows=true 时调整该 View 的 padding 给状态栏等系统窗口留出空间（只在非嵌入的 activity 中生效）：源端顶部 inset 可能由布局里带这个属性的那一层隐式消费（出处：Android SDK 平台资源 data/res/values/attrs.xml，fitsSystemWindows）
- 〔做法第 5 步〕hideTitleBar(value: boolean): NavDestinationAttribute，默认 false；API 13 起另有 hideTitleBar(hide: boolean, animated: boolean)，animated 默认 false（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.hideTitleBar；文档 ts-basic-components-navdestination.md，hideTitleBar）
  写法：NavDestination() 的属性方法，全局组件，全局可用，不用导入
        NavDestination() { /* 页面内容 */ }.hideTitleBar(true)
- 〔做法第 5 步〕全屏布局下根 Navigation 四向 expandSafeArea 时，NavDestination 的预设标题栏画进状态栏区域，不会自动避让（出处：卡里修好并验证过）
- 〔做法第 1 步〕应用主题与代码都没另设 statusBarColor 时各标准父主题的状态栏底色：Theme.Holo、Theme.Holo.Light 为 #FF000000，且 windowDrawsSystemBarBackgrounds=false（系统自绘黑底，statusBarColor 不生效）；其余主题 windowDrawsSystemBarBackgrounds=true、statusBarColor=?attr/colorPrimaryDark：Theme.Material、Theme.Material.Light.DarkActionBar、Theme.AppCompat、AppCompat.Light.DarkActionBar、Theme.MaterialComponents、MaterialComponents.Light.DarkActionBar 与两个 DayNight 的夜间为 #FF000000；Theme.Material.Light、Theme.AppCompat.Light、AppCompat.DayNight（日间）#FF757575；Theme.MaterialComponents.Light、MaterialComponents.DayNight（日间）#3700B3；Material3 浅色 #FF6750A4、深色 #FFD0BCFF；Theme.DeviceDefault 在 API≤30 同 Material，API 31 起为动态色。这些父主题都不设 windowLightStatusBar（状态栏图标为浅色）。android-30 至 36、appcompat 1.1.0–1.8.0、material 1.4.0–1.14.0 相同（出处：Android SDK 平台资源 data/res/values/themes.xml，statusBarColor、windowDrawsSystemBarBackgrounds；data/res/values/themes_material.xml，Theme.Material.Light.DarkActionBar、colorPrimaryDark；data/res/values/colors_material.xml，primary_dark_material_light；androidx.appcompat:appcompat 1.1.0、1.7.1、1.8.0 包内 res/values-v21，Platform.AppCompat.Light（android:colorPrimaryDark）；com.google.android.material:material 1.4.0、1.12.0、1.14.0 包内 res/values，design_default_color_primary_dark、Base.Theme.MaterialComponents.Light.DarkActionBar）
- 〔做法第 1 步〕应用主题没有另设时，所有标准父主题（Holo、Material、DeviceDefault、AppCompat、MaterialComponents、Material3 及其 Light、DarkActionBar、DayNight）windowTranslucentStatus、windowTranslucentNavigation、windowFullscreen 都是 false：平台只有 *.NoActionBar.TranslucentDecor 变体把两项半透明设为 true，*.NoActionBar.Fullscreen、*.NoActionBar.Overscan、Theme.NoTitleBar.Fullscreen、Theme.Black.NoTitleBar.Fullscreen 等变体设 windowFullscreen=true，AppCompat 与 MaterialComponents 没有设这几项的应用主题。主题里的 navigationBarColor 资源：API≤33 为 @color/black，API≥34 为 navigation_bar_default（#00808080，窗口再换成不透明黑，见导航栏条）；所有父主题都不设 windowLightNavigationBar（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.NoActionBar.TranslucentDecor、Theme.Material.NoActionBar.Fullscreen、windowTranslucentStatus；data/res/values/themes_holo.xml，Theme.Holo.NoActionBar.TranslucentDecor、Theme.Holo.NoActionBar.Fullscreen；data/res/values/themes.xml，Theme.Black.NoTitleBar.Fullscreen、navigationBarColor；android-33 与 android-34 的 values/colors.xml，navigation_bar_default；androidx.appcompat:appcompat 1.8.0、com.google.android.material:material 1.14.0 包内 res/values*（没有主题设 android:windowFullscreen、android:windowTranslucentStatus））
- 〔适用情境 / 做法第 1 步〕androidx.activity 的 enableEdgeToEdge() 不传参数时（activity 1.8.0 与 1.13.0 相同）：先 setDecorFitsSystemWindows(false)，状态栏用 SystemBarStyle.auto(透明, 透明)，导航栏用 SystemBarStyle.auto(DefaultLightScrim #E6FFFFFF, DefaultDarkScrim #801B1B1B)；API 29+ 上 auto 样式给两栏都设透明色、statusBarContrastEnforced=false、navigationBarContrastEnforced=true（三键导航时由系统自己加对比遮罩，手势导航下无遮罩）；API 26–28 导航栏直接用上述浅/深遮罩色。图标深浅按系统深色模式切换（出处：androidx.activity:activity 1.8.0、1.13.0 字节码 EdgeToEdge.enable、EdgeToEdge 静态初始化（DefaultLightScrim、DefaultDarkScrim）、EdgeToEdgeApi29、EdgeToEdgeApi26、SystemBarStyle.getScrimWithEnforcedContrast）
- 〔做法第 4 步〕fitsSystemWindows 默认 false。设为 true 的 View 在默认 onApplyWindowInsets 里走 fitSystemWindows：把系统窗口 inset 设成自己的 padding，并返回已消费的 inset。targetSdk < 30（R）时 ViewGroup 按子 View 顺序分发，一旦被消费就不再发给后面的兄弟；targetSdk ≥ 30 时每个子 View 都收到父级同一份 inset，兄弟之间不再互相吞掉（出处：android.view.View#onApplyWindowInsets、#fitSystemWindows、#sBrokenInsetsDispatch；android.view.ViewGroup#dispatchApplyWindowInsets、#brokenDispatchApplyWindowInsets、#newDispatchApplyWindowInsets）
