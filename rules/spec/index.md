# 规格（spec）

227 个族，561 条规矩。整个产物的族一页看完见 [map.md](map.md)（每个主题一行，下面是「短号 族名（条数）」）。

## 一级主题

- [验收条目与验收判定](acceptance/index.md)（14 条）：规格里有验收条目（AC）和它挂的源码真值、UT 设计，或交回的验收报告、回归诊断给出 PASS、「两端一致」这类判定时
- [标题栏、菜单与抽屉](app-bar/index.md)（18 条）：读到源端有菜单 XML（showAsAction）、上下文菜单、ActionBar / Toolbar / TopAppBar、DrawerLayout + NavigationView，规格里写标题栏、Up 箭头、溢出菜单、折叠顶栏和抽屉时
- [本地数据与偏好](data/index.md)（34 条）：读到源端的数据库、JSON 解析、assets 预置数据、外部存储，或偏好 XML、SharedPreferences / DataStore，规格里写数据表、存储、设置页和偏好键时
- [弹窗与提示](dialog/index.md)（26 条）：读到源端弹 AlertDialog、Dialog、经工具类或 Helper 弹的弹窗、BottomSheetDialogFragment / ModalBottomSheet、BottomSheetBehavior 面板或 Toast，规格里写弹窗清单、底部面板和提示时
- [图形与自绘](graphics/index.md)（29 条）：读到源端有自定义 View 的 onDraw / Paint / SurfaceView、Compose 绘制修饰符、@drawable 引用的外观、共享组件里的形状或动画，规格里写画布、图片、阴影描边和动画时
- [布局与尺寸](layout/index.md)（15 条）：读到源布局的 LinearLayout、ConstraintLayout、NestedScrollView、TableLayout、代码里循环 addView 搭的视图，或 Compose 的 Column、Modifier 链、自定义 Layout，规格里写容器映射、对齐、权重和尺寸时
- [生命周期与配置重建](lifecycle/index.md)（24 条）：读到 Activity 的 onCreate、onResume、onPause、onSaveInstanceState、getLastNonConfigurationInstance、configChanges，Compose DisposableEffect、LifecycleEventObserver，或 Application 初始化链，规格里写生命周期映射、存档和刷新时机、配置变化重建时
- [列表、网格与翻页](list/index.md)（18 条）：读到源端有 ListView、GridView、RecyclerView / GridLayoutManager、LazyColumn / LazyRow、SmartRefreshLayout、ViewPager2 或 ActionMode 多选，规格里写列表、网格、刷新分页和翻页时
- [源码逻辑与数值](logic/index.md)（46 条）：读到源码里决定结果的分支、异常、集合遍历、float 运算、常量、格式化、日期时间和线程调用，规格的 AC、映射行或源码笔记要按它写出确切行为时
- [页面导航与入口](navigation/index.md)（57 条）：读到源端的 startActivity / Intent、finish、返回键、Compose NavHost、FragmentTransaction、导航图，或 LAUNCHER、闪屏、深链 intent-filter，规格里写导航表、返回落点、启动路由和外部入口时
- [网络接口与同步](network/index.md)（25 条）：读到 Retrofit Service、OkHttp 拦截器、Gson 和 Bean 模型、按异常类型分的网络失败、响应解密钩子，或待推送队列和同步任务，规格里写 API 表、请求头、错误码表、响应契约、测试环境和同步顺序时
- [平台差异决策与偏离](platform-gap/index.md)（24 条）：规格或决策台账里写了「无对等」「降级」「不迁移」「PD」「显式差异」「用户例外」这类平台差异决策和偏离，或写它们的依据栏时
- [资源与应用配置](resource/index.md)（31 条）：读到 res 下的 values-* / layout-* 限定词目录、按名引用的颜色和尺寸资源、AndroidManifest 的 application / activity 声明和 supportsRtl、BuildConfig 开关和多套 base URL，或目标 app.json5 的身份，规格里写资源表、配置值和身份项时
- [迁移范围与功能归属](scope/index.md)（15 条）：规格里写迁移范围、功能归属（page_id ownership、归某 feature）、功能入口页、跨页面共享组件、别的规格留给本文档承接的条目，或引用上游清单和台账（api-inventory、skip-list）时
- [源码证据与页面元数据](source-evidence/index.md)（23 条）：交回的 meta.json、基线快照或源码理解笔记里有页面元数据、合成的快照，或写了没读到定义的谓词、空子模块里的实现、声明没保证的回调顺序、实现建议的出处这类不确定项时
- [页面状态与数据流](state/index.md)（12 条）：读到 ViewModel、LiveData / StateFlow、remember、data class copy、Activity 实例字段和 static 字段，规格里写状态契约、状态接口表（@Local）、复位和数据流时
- [系统能力、设备与三方 SDK](system/index.md)（47 条）：读到源端用蓝牙、NFC、定位、剪贴板等系统服务，WorkManager、前台 Service、常驻通知，MediaPlayer / SoundPool，分享面板，或厂商 SDK、Flutter 插件，规格里写这些能力的映射、权限和降级时
- [主题、颜色与默认外观](theme/index.md)（46 条）：读到 styles.xml / themes.xml 的主题继承（AppCompat、MaterialComponents、Material3、android:Theme.*）、?attr/ 主题属性、Color.* 常量，或源控件没写颜色和外观属性，规格里写主题色、控件默认外观和颜色映射时
- [文本、控件与触摸](widget/index.md)（33 条）：读到源端有 TextView、EditText、Slider、WebView 等控件或 Compose Text / TextStyle，onTouch、GestureDetector、SwipeToDismissBox 触摸处理，contentDescription 等无障碍语义，规格里写文本样式、输入约束、控件状态和手势时
- [窗口与系统栏](window/index.md)（24 条）：读到源端有状态栏、导航栏、全屏和沉浸的写法（FLAG_FULLSCREEN、NoTitleBar 主题、WindowInsets、fitsSystemWindows、ImmersionBar、windowBackground、FLAG_KEEP_SCREEN_ON），或规格里写沉浸式、安全区避让、系统栏颜色和窗口背景时
