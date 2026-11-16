# 状态栏图标深浅和系统栏内容色

agent 会看到什么：读过的源主题或基类 Activity 里设状态栏图标深浅（windowLightStatusBar、SYSTEM_UI_FLAG_LIGHT_STATUS_BAR），或参考模板给了默认内容色；交回的代码里 setWindowSystemBarProperties 的 statusBarContentColor / navigationBarContentColor

## 通用查法

### 系统栏内容色是手写常数时，按源端主题和代码里的浅色状态栏标志定深浅

审的是：代码
触发（任一种）：
- 读到：源主题（含 values-vNN 和 parent 链）的 android:windowLightStatusBar、代码里的 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR / APPEARANCE_LIGHT_STATUS_BARS，或一处都没有；写错的样子：statusBarContentColor / navigationBarContentColor 是照模板或按底色自选的常数，没有源端依据
适用范围：用 setWindowSystemBarProperties 或 systemBarStyle 设系统栏内容色、源端是安卓 View 主题时
做法：
- 在源工程 res/values* 主题文件里找应用和 Activity 主题的 android:windowLightStatusBar，顺 parent 读到依赖库或平台主题；再在代码里搜 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR、APPEARANCE_LIGHT_STATUS_BARS
- 有一处为 true 是深色图标，内容色写深色（如 '#FF000000'）；都没有是白色图标，写 '#ffffff'；主题名里的 Light 和底色深浅不算依据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- windowLightStatusBar（boolean）：设了才把状态栏画成适配浅底的样式，对应 View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR 和 WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS：源端让状态栏图标变深的三种写法（出处：Android SDK 平台资源 data/res/values/attrs.xml，windowLightStatusBar（按应用的 compileSdk 取对应平台））
- 平台主题里只有 Theme.Material.Light.LightStatusBar 等变体写了 windowLightStatusBar=true，Theme.Material.Light 本身没写：parent 链读到平台的 Light 主题时，默认仍是白色状态栏图标（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light.LightStatusBar（按应用的 compileSdk 取对应平台））
- statusBarContentColor?: string；navigationBarContentColor?: string：SystemBarProperties 里的状态栏、导航栏文字颜色；设了以后 isStatusBarLightIcon / isNavigationBarLightIcon 无效，默认值 '#E5FFFFFF'（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，SystemBarProperties；arkts-apis-window-i.md，SystemBarProperties）
针对本应用要查的：
- 源端状态栏图标明暗：源工程 res/values* 下主题文件里应用和 Activity 主题的 android:windowLightStatusBar，顺 parent 到依赖库或平台主题；再搜 Java/Kotlin 里的 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR、APPEARANCE_LIGHT_STATUS_BARS；有一处为 true 就是深色图标，写深色内容色；都没有就是白色，写 '#ffffff'
来源：2 张卡，2 个应用
- case-436d1b16d79796c667d6（android-panorama-map-vest7）：做法第 2 步 ← 建议 1
- case-e2bca560f2a4516d2fb5（2048）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2

## 规矩

- rule-c412c1a65641｜系统栏内容色按源端状态栏图标深浅定，不照搬模板的浅色 #FFFFFFFF｜读到：参考模板或派工里写 setWindowSystemBarProperties「透明背景 + 浅色文字」、statusBarContentColor 设 #FFFFFF，没有给出源端状态栏图标的深浅；写错：UIAbility 里 statusBarContentColor / navigationBarContentColor 写成 '#FFFFFFFF'，而源端基类 Activity 或主题设的是深色状态栏图标、白色状态栏
- rule-f89b2207295d｜源主题和代码都没设浅色状态栏标志时，statusBarContentColor 写 '#ffffff'｜读到：源主题（含 Theme.AppCompat.Light.NoActionBar 一类「Light」主题）和 values-vNN 覆盖里没有 android:windowLightStatusBar，代码里没有 SYSTEM_UI_FLAG_LIGHT_STATUS_BAR、APPEARANCE_LIGHT_STATUS_BARS；写错：setWindowSystemBarProperties 里 statusBarContentColor 写成深色（如 '#776e65'），注释按「浅色主题」或「对比足够」论证；或只设了 statusBarColor、navigationBarColor，没写 statusBarContentColor
- rule-65baa6a8d89e｜源主题按明暗设状态栏图标极性时，statusBarContentColor 随主题下发，不写死白色｜读到：源端主题在组合期设 isAppearanceLightStatusBars = isLight，有深浅两套配色；写错：窗口初始化把 statusBarContentColor / navigationBarContentColor 写死为 '#FFFFFF'，或壳层的写死值覆盖了主题服务的设置
