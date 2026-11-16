# Activity 的全屏和无标题窗口标志

agent 会看到什么：读到源 Activity 的 setFlags(FLAG_FULLSCREEN)、android:windowFullscreen、requestWindowFeature(FEATURE_NO_TITLE)；产物里 setWindowSystemBarEnable([]) 把导航栏一起隐藏、根容器四向 expandSafeArea，或页面多了标题栏、没写 hideTitleBar(true)

## 规矩

- rule-585a8a8bef87｜源只有 FLAG_FULLSCREEN 时只隐藏状态栏，不用 setWindowSystemBarEnable([])｜读到：源 Activity 只有 setFlags(FLAG_FULLSCREEN) / android:windowFullscreen，没有隐藏导航栏的标志；写错：入口 Ability 里写 setWindowSystemBarEnable([])，状态栏、导航栏和导航条一起隐藏
- rule-03c3ef15cf7f｜源端只有 FLAG_FULLSCREEN 时，页面根容器不四向 expandSafeArea 铺进挖孔和导航区｜读到：源 Activity 只有 setFlags(FLAG_FULLSCREEN) / android:windowFullscreen，没有延伸到导航栏下的标志；写错：页面根 Stack 或背景 Image 上写 .expandSafeArea([SafeAreaType.SYSTEM, SafeAreaType.CUTOUT]) 不限边，背景和内容铺进挖孔边和导航区
- rule-737449f8a2a5｜源页关了标题（FEATURE_NO_TITLE）时，目标页 hideTitleBar(true)，不加标题栏｜读到：源 Activity 调 requestWindowFeature(Window.FEATURE_NO_TITLE)，页面只承载一个全屏视图（如 AMapNaviView）；写错：目标页加了自定义白色标题栏，或 NavDestination 没写 .hideTitleBar(true)、露出系统标题栏
- rule-9d3ac1dd4de0｜源主题全屏且沉浸只切导航栏时，非沉浸用 setWindowSystemBarEnable(['navigation'])｜读到：主题 <item name="android:windowFullscreen">true</item>；Activity 的沉浸切换只显隐导航栏（注释如「only show/hide navigation bars, as we run with system bars always hidden」）；写错：非沉浸分支调用 setWindowSystemBarEnable(['status', 'navigation'])，把源端始终隐藏的状态栏显示出来
