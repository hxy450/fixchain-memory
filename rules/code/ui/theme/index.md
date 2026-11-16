# 主题、颜色与样式

源端有主题和 style、?attr 颜色、@color 资源、Material 控件的默认外观、Compose MaterialTheme / colorScheme / contentColor、深浅色切换，目标端有 $r('app.color.…') 等资源引用、fontColor、backgroundColor、setColorMode 时

## 触发族

- [引用主题属性 ?attr 的颜色](theme-attr-color/index.md)（9 条）：读到源端颜色写成 ?attr/…（vector 的 android:fillColor、Toolbar 背景、图标的 colorControlNormal）或取主题的 windowBackground，交回的代码给 Image 的 fillColor、backgroundColor、fontColor 绑了颜色键或没绑
- [源控件没写的外观属性（主题的默认控件样式）](widget-default-style/index.md)（11 条）：读到 TextView、Button、AppCompatButton 子类、TabLayout 只写了部分外观属性（没写 style、textColor、textAllCaps、tabGravity 等，或只写了 textAppearance），交回的代码只照显式写的属性写，其余落到 ArkUI 默认
- [Compose 主题的深浅色和动态配色状态](theme-mode-state/index.md)（4 条）：读到 @Composable 主题函数按 isSystemInDarkTheme()、DataStore 里的外观开关或 dynamicLightColorScheme / dynamicDarkColorScheme 选配色；产物里的主题状态类、EntryAbility 里的同步和 setColorMode、wallpaper.getColors 调用
- [组件里读取的 Compose 主题色](theme-color-read/index.md)（9 条）：读到 Compose 组件取 MaterialTheme.colorScheme.X 或自定义 Theme.colors.X（经 CompositionLocal 下发）；产物里对应的颜色写成名字相近的资源、浅色常量，或在字段初始化器、@Param 默认值里只取一次
- [随状态或容器变化的颜色](state-color/index.md)（2 条）：源端 Compose 颜色不是资源原色、而是随容器或状态算出来的写法（Surface(elevation > 0) 的叠白、color.copy(alpha = if (!enabled) 0.38f else 1f)），对应目标的 backgroundColor、fontColor 和按状态的 opacity
- [Material 控件没写外观属性时的默认外观](material-default-look/index.md)（8 条）：源布局里 Button、FloatingActionButton、BottomNavigationView 等 Material 控件没写 style 和外观属性、外观来自主题；产物里对应组件的 backgroundColor、fontColor、borderRadius、fontWeight、letterSpacing
- [颜色资源引用和源端色值](color-token-value/index.md)（7 条）：源端颜色是字面量、@color/ 或 getColor(R.color.名)，目标工程已有一批颜色键；产物里 $r('app.color.…') 选了哪个键、'#…' 字面量从哪来
- [应用内切换主题和深色模式](in-app-theme-switch/index.md)（3 条）：读到源端按偏好 setTheme、recreate、AppCompatDelegate.setDefaultNightMode 切换浅色 / 深色主题；产物里 setColorMode 的调用时机、getColorSync 命令式取色和系统栏内容色
- [Compose 没写颜色的文本和图标](compose-content-color/index.md)（5 条）：读到 Compose 的 Text 没传 color、Icon 没写 tint，颜色来自外层 Surface / Scaffold 的 contentColor 或 LocalContentColor，产物里是 Text 的 fontColor、Image 的 fillColor 用了哪个色资源
- [组件属性里的 $r 资源引用](resource-ref-r/index.md)（3 条）：读过的派工或改写前的代码要求尺寸、颜色走 $r('app.float.…') 一类资源引用；交回的代码里属性参数写成 $r(...)、裸的 'app.类型.名' 字符串或数值常量
- [控件经 style 继承的圆角和形状值](style-inherited-shape/index.md)（1 条）：读到布局 XML 里控件写 style="@style/…"，圆角、高度写在样式的 <item> 里，元素本身没覆写或别处元素覆写了；产物里对应组件的 .borderRadius(...) 取了外层卡片、相邻按钮、别处覆写的值，或按半高写成胶囊
- [M3 色板和排版令牌的构造](m3-scheme-typography-tokens/index.md)（1 条）：读到 lightColorScheme(...) / darkColorScheme(...) 构造的色板、Typography() 基准上 copy(fontSize = …, lineHeight = …) 的排版；产物里的颜色令牌和文字令牌只迁了源端显式写的字段，缺 surfaceContainer*、fontWeight、letterSpacing
- [getColorSync 取到的 ARGB 颜色的拆分和插值](argb-color-blend/index.md)（2 条）：读到颜色端点取自 resourceManager.getColorSync(...)（32 位 ARGB 数）或 color.json 的 '#AARRGGBB'，规格要求按 fraction 插值或混色，工程里可能已有按 >>> 24、& 0xFF 拆通道的混色工具；产物里页面各自用 slice(1, 3) / parseInt / padStart 拆拼颜色
- [三方 UI 库控件的尺寸和动画取值](third-party-widget-values/index.md)（1 条）：读到布局或代码里三方 UI 库的类名和自定义属性（com.getbase.floatingactionbutton.FloatingActionsMenu 的 fab_*、Crouton 的 Configuration.Builder().setInAnimation）；产物里自研替代组件上自定的圆角、内边距、Column space、rotate 角度和 transition 时长
- [Ionic 组件的默认样式和子项顺序](ionic-component-defaults/index.md)（1 条）：读到 setupIonicReact({ mode })、IonCard / IonCardHeader 这类 Ionic 组件只写了部分 inline style，或容器是 flex-direction: *-reverse；产物里只照 inline style 写的 Text 和卡片外观、按 DOM 序排的子组件
- [Compose Material 的 Badge 角标](compose-badge/index.md)（1 条）：读到 Compose 的 BadgedBox 里 Badge(containerColor = …) { Text(count.toString()) }；产物里 ArkUI Badge({ count, style }) 的 maxCount、字色、字号、badgeSize，或自绘文本加 offset 当角标
