# 带 ActionBar 的页面规格写定 Up 箭头显不显示和依据，不写「若有」

审的是：规格
触发（任一种）：
- 读到：源 Activity 用带窗口 ActionBar 的 AppCompat 主题，Manifest 有 parentActivityName 或 PARENT_ACTIVITY meta-data，onOptionsItemSelected 处理 android.R.id.home；写错的样子：页面规格的导航表写「ActionBar Up（若有）」，没写定 Up 箭头显不显示；或写「无返回箭头——源端未调 setDisplayHomeAsUpEnabled」而没提 parentActivityName
适用范围：为带 ActionBar 的安卓页面写规格时，导航和标题栏那一节
做法：
- 规格里写一句：「Up 箭头：显示（或不显示）；依据：主题是否带窗口 ActionBar、Manifest 有无 parentActivityName / PARENT_ACTIVITY、setDisplayHomeAsUpEnabled 是否显式调用及取值」
- 主题带窗口 ActionBar 且有 parentActivityName、没有显式调用时写「显示」，并写明箭头点击执行 onOptionsItemSelected 里 android.R.id.home 分支的逻辑
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Activity#onCreate 里 mActivityInfo.parentActivityName != null 时，ActionBar 的默认 Up 设为开启：声明了 parentActivityName 就默认显示 Up（出处：android.app.Activity#onCreate）
- setDefaultDisplayHomeAsUpEnabled 只在没有显式设过 DISPLAY_HOME_AS_UP 时生效：显式调用 setDisplayHomeAsUpEnabled 时以显式调用为准（出处：com.android.internal.app.WindowDecorActionBar#setDefaultDisplayHomeAsUpEnabled）
- Base.V7.Theme.AppCompat 的 windowActionBar = true；Theme.AppCompat.NoActionBar 的 windowActionBar = false：判断主题带不带窗口 ActionBar（出处：androidx.appcompat:appcompat 包内 res/values/values.xml，Base.V7.Theme.AppCompat、Theme.AppCompat.NoActionBar（按应用依赖的版本））
针对本应用要查的：
- 这个 Activity 实际用的主题带不带窗口 ActionBar：源工程 AndroidManifest 里这个 Activity 的 android:theme（没有就看 application 的），再到源工程 res/values 的 styles、themes 文件里顺着 parent 链找；落到 NoActionBar 或 windowActionBar 为 false 的没有窗口 ActionBar；落到 Theme.AppCompat、DarkActionBar 这一族的有
未核实：AppCompat 库代码里的同一默认 Up 逻辑按卡写，本机只核对了框架 android.app.Activity
来源：1 张卡，1 个应用
- case-855df43db43e4ed66f9e（Privacy Friendly 2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 1、建议 3
