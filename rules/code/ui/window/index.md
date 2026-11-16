# 窗口与系统栏

源端有 Activity 的窗口标志、主题的全屏和系统栏颜色、fitsSystemWindows、WindowInsets、DisplayMetrics、屏幕方向、常亮、画中画和亮度，目标端有 window 的 setWindowLayoutFullScreen、setWindowSystemBarProperties、getWindowAvoidArea、expandSafeArea 时

## 子主题

- [安全区与避让](insets/index.md)（48 条）：源端有 fitsSystemWindows、透明状态栏下的留白、WindowInsets、Compose Scaffold 的 innerPadding、ImmersionBar，目标端有 getWindowAvoidArea 取值，或页面、Tabs 宿主、贴底元素上的避让 padding 和 expandSafeArea 时

## 触发族

- [Activity 的全屏和无标题窗口标志](window-flags/index.md)（4 条）：读到源 Activity 的 setFlags(FLAG_FULLSCREEN)、android:windowFullscreen、requestWindowFeature(FEATURE_NO_TITLE)；产物里 setWindowSystemBarEnable([]) 把导航栏一起隐藏、根容器四向 expandSafeArea，或页面多了标题栏、没写 hideTitleBar(true)
- [入口窗口的全屏方式和系统栏颜色](system-bar-color/index.md)（6 条）：源主题和 Activity 里的全屏、沉浸和系统栏颜色写法（windowFullscreen、FLAG_FULLSCREEN、android:navigationBarColor、setNavigationBarColor），对应 EntryAbility 里的 setWindowLayoutFullScreen 和 setWindowSystemBarProperties
- [DisplayMetrics 屏幕宽高参与的几何](display-metrics/index.md)（1 条）：源端用 getDisplayMetrics().widthPixels / heightPixels 算格径、留白、行数的公式（常在 FLAG_FULLSCREEN、targetSdk 低的 Activity 里），对应目标取尺寸的写法（getDefaultDisplaySync、windowRect、getWindowAvoidArea）
- [Activity 的屏幕方向声明与运行时切换](screen-orientation/index.md)（2 条）：读到 AndroidManifest.xml 的 android:screenOrientation 或运行时 setRequestedOrientation；交回的页面没有 setPreferredOrientation，或进入时切了方向、离开和返回时不恢复
- [窗口常亮和画中画（FLAG_KEEP_SCREEN_ON、PictureInPicture）](keep-screen-on-pip/index.md)（4 条）：读到源端 getWindow().addFlags / clearFlags(FLAG_KEEP_SCREEN_ON)、WakeLock 或 PictureInPictureParams 进出画中画，产物里是 setWindowKeepScreenOn 的置位和复位位置、各退出路径上的状态复位，以及 PiPWindow 相关代码
- [状态栏图标深浅和系统栏内容色](system-bar-content-color/index.md)（4 条）：读过的源主题或基类 Activity 里设状态栏图标深浅（windowLightStatusBar、SYSTEM_UI_FLAG_LIGHT_STATUS_BAR），或参考模板给了默认内容色；交回的代码里 setWindowSystemBarProperties 的 statusBarContentColor / navigationBarContentColor
- [窗口亮度的读取和手势调节](window-brightness/index.md)（2 条）：读到源手势在 ACTION_DOWN 读 window.attributes.screenBrightness、等于 BRIGHTNESS_OVERRIDE_NONE 时回退 Settings.System.SCREEN_BRIGHTNESS；产物里亮度基线写死 0.5、注释称 window 无亮度读取 API，只调了 setWindowBrightness
- [设窗口级属性时拿的窗口对象](main-window-access/index.md)（1 条）：读到源端经 LocalView 或 Activity 取 window，再设 FLAG_SECURE、isAppearanceLightStatusBars 这类窗口级属性；产物里主题服务或页面用 window.getLastWindow(context) 取窗口，还是在 onWindowStageCreate 取到主窗口后注入
