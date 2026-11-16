# 规矩库

卡库版本：`e797fb1557779c4778acad0c24d9e779e0b8de07d3af8883992c0820dbe0103c`；规矩 2923 条。按产物进入，再按主题、触发族往下找。

## 代码（code）

- [ArkTS 语法与工程](code/arkts/index.md)（41 条）：交回的 .ets 里有 @Builder、@BuilderParam、@ComponentV2 成员、.stateStyles、Record 和对象字面量，或构建日志报 arkts-* 和组件语法错误，或涉及 BuildProfile、HAR 模块和跨文件导入时
- [数据与存储](code/data/index.md)（99 条）：源端有 SharedPreferences / MMKV、Room / SQLite、Gson / org.json 模型、XML 解析、Repository / Dao 的调用和同步进度事件、文件读写和 ZIP、种子数据，目标端有 preferences、relationalStore、模型 class、JSON.parse、fs 读写时
- [生命周期与启动](code/lifecycle/index.md)（48 条）：源端有 Activity / Fragment 的 onCreate、onStart、onResume、onPause、onDestroy、闪屏和初始化、configChanges、savedInstanceState、Compose DisposableEffect，目标端有 EntryAbility 的回调、aboutToAppear / aboutToDisappear、onShown / onHidden、onReady 时
- [业务逻辑与源码语义](code/logic/index.md)（140 条）：源端有 Java / Kotlin 的分支条件、回调分支、提交前校验、ViewModel 方法在请求前后的步骤、工具类静态入口起的业务链、数值运算、集合遍历、异常捕获、协程并发、字符串和字节处理、日期计算，目标端有照着移植的 TS 业务代码时
- [音视频与媒体选取](code/media/index.md)（101 条）：源端有 VideoView、MediaPlayer、ExoPlayer / PlayerView、SoundPool、MediaController、选图和选文件的 Intent，目标端有 Video、AVPlayer、SoundPool、XComponent、PhotoViewPicker、SaveButton 时
- [页面导航与标题栏](code/navigation/index.md)（192 条）：源端有 startActivity / Intent、跳板 Activity 和透明主题的 Activity、Fragment 事务、Compose Navigation、onBackPressed、Activity 切换转场、Toolbar / ActionBar、DrawerLayout，目标端有 Navigation、NavDestination、NavPathStack、router.pushUrl、pageTransition、自绘标题栏时
- [网络](code/network/index.md)（42 条）：源端有 Retrofit 接口注解、OkHttp / OkGo 请求和拦截器、BaseResponse 响应壳、BuildConfig 里的服务地址，目标端有 @ohos.net.http 的封装、请求 url 和 header、响应解包时
- [占位、规格与测试](code/placeholder/index.md)（50 条）：派工、占位登记或代码注释里有 FWD-REF、PLACEHOLDER、P-ID 条目，规格的 AC、台账里的「平台无对等」，孤儿检测报 NO_IMPORTER，或单测、派工的要求和源端不同时
- [状态与数据流](code/state/index.md)（73 条）：源端有 ViewModel、LiveData / Flow、Compose remember / mutableStateOf、EventBus、data class copy，目标端有 @Local、@Param、@ObservedV2 / @Trace、@Monitor、AppStorageV2、@Builder 传参和页面的加载、空、错误状态时
- [系统能力与设备](code/system/index.md)（89 条）：源端有运行时权限、通知、WorkManager、地图和定位 SDK、NFC、蓝牙、网络状态、振动、OAID、Cipher 加解密、桌面小部件、登录授权 SDK、FlutterBoost，目标端有对应的 @ohos / @kit 接口、FormExtensionAbility 或三方 SDK 桥接时
- [界面](code/ui/index.md)（987 条）：源端是布局 XML 里的 View 控件或 Compose 界面元素（文字、图片和自绘、布局容器、列表和翻页、弹窗和提示、点击和输入控件、动效、主题和颜色、窗口和系统栏、三方库的自定义 View），目标端是 ArkUI 组件和它的尺寸、样式、属性时
- [网页](code/web/index.md)（12 条）：源端有 WebView、WebViewClient、WebSettings、loadDataWithBaseURL，目标端有 Web 组件、WebviewController、onLoadIntercept、onErrorReceive 时

## 计划与派工（plan）

- [构建与编译](plan/build/index.md)（8 条）：派工里写了禁止 worker 编译、不跑 hvigor、附 ArkTS 限制清单，或者交回的报告、回执、CHECK-1、编译门报告里写了构建结果（BUILD SUCCESSFUL / FAILED、0 errors、编译尚未执行）时
- [覆盖清单与跳过清单](plan/coverage/index.md)（17 条）：交回的是 skip-list、覆盖清单、对齐表、ui-manifest、feature-index，或债务闸、覆盖检查报出的 gap，以及被跳过、标「平台无对等」的条目时
- [数据、网络与日志](plan/data/index.md)（5 条）：源端有 Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器、Room Migration、偏好标记，或者台账列了日志边界，计划和契约要写网络层、数据库、偏好接口、日志任务时
- [决策台账与决策缺口](plan/decisions/index.md)（10 条）：读到的决策台账、PD 决策卡、规格里的条件或作用域限定和源码、派工对不上，交回的 decision_gaps、handback、巡检问题单里要记分歧或延后裁决时
- [派工说明](plan/dispatch/index.md)（18 条）：交回的是给执行子代理的派工说明或派工补充：要交的源文件、前置 skill、必读清单、迁移陷阱编号、suggested_skills、控件映射和参数、另加的要求和限制、派发先后时
- [修复工单与问题单](plan/fix/index.md)（6 条）：交回的是修复工单、问题文件、UT 分诊、修复报告或修复回执：工单建议的修法、RED 用例、§6 预期效果、按截图删减、本轮不修的偏差时
- [交回报告与完成说法](plan/handback/index.md)（34 条）：交回的回执、交付说明、收口报告、转换报告、slice notes 里写着「已实现」「已补齐」「已对齐」「全部完成」「resolved」「均保留」这类完成说法时
- [交接摘要与移交项](plan/handoff/index.md)（12 条）：交回的交接摘要、契约摘要、计划或 TODO 里转述源端方法的行为，或者上游交接、子代理回执写明某项交给别的任务、主线程或后续切片承接时
- [入口与生命周期](plan/lifecycle/index.md)（18 条）：源端 Application、Activity 和业务基类的 onCreate、onResume、onPause、onDestroy、onBackPressed 里有行为，或者目标端要接到 EntryAbility、入口页、共享服务的停止和释放上时
- [占位登记与前向引用](plan/placeholders/index.md)（79 条）：交回的产物里有 placeholder-registry 条目、FWD-REF / UNC 标记、// HANDOFF: 行、resolve_by、近似项或资源未就绪的登记，或者有留给后续切片的交互、数据和事件时
- [切片计划与重构计划](plan/plan/index.md)（14 条）：交回的是切片计划、重构计划、批次与模块拆分或改动清单：scope、acceptance、integration_points、Step、跨业务依赖，以及换了承接方的源端职责时
- [工程配置与模块](plan/project/index.md)（33 条）：派工、移交、计划或报告涉及 module.json5（requestPermissions、方向、extensionAbilities、shortcuts）、app.json5（bundleName、vendor、label、icon、configuration）、form_config、应用身份步骤或 HAR 模块时
- [资源](plan/resources/index.md)（15 条）：派工、交接、资源映射报告或收口回报涉及 strings.xml / string.json、colors.xml / color.json、$r 令牌、多语言、图标和 SVG 资源的来源与转换结果时
- [三方 SDK 与插件](plan/third-party/index.md)（3 条）：规格、skill 映射表、pubspec 或 .flutter-plugins-dependencies 里有要平台 Key 的厂商 SDK（如 com.amap.api）、Flutter 插件和它依赖的原生插件时
- [界面](plan/ui/index.md)（70 条）：读到的源码或规格里有窗口与系统栏、弹窗、布局尺寸、列表、共享组件、页面路由、主题、吐司和通知这类界面写法，派工、登记、计划或报告要交代它们时
- [验证报告与验收结论](plan/verification/index.md)（11 条）：交回的验证汇总、视觉校验、阶段报告、差异清单、巡检单、收尾一致性结论里有 PASS、✔、BLOCKED 判定，或者有要真机、截图才能确认的项时

## 资源（resource）

- [应用级信息（AppScope）](resource/app-info/index.md)（25 条）：源端 Gradle 有 applicationId、resValue，AndroidManifest 的 <application> 写了 android:label、android:icon；目标端有 AppScope/app.json5 的 bundleName、vendor、icon，app_name、EntryAbility_label 字符串，或分层图标、启动窗图标时
- [颜色](resource/colors/index.md)（25 条）：源端有 colors.xml、values-night、布局和 Compose 里的色值，或颜色来自 ?attr 主题属性、控件默认样式、@android:color 和 Material 等库主题；目标端有 color.json 和 dark 目录时
- [图片和矢量图](resource/media/index.md)（11 条）：源端 drawable 下有位图和 <vector>、<animated-vector>，布局或代码用 @drawable、R.drawable 引用图片，或 Compose 用 Icons.* 图标；目标端有 resources 下 media 目录里的图片和 SVG 时
- [模块配置（module.json5）](resource/module-config/index.md)（23 条）：源 AndroidManifest 有 <activity>、<service>、<intent-filter>，res/xml 下有 shortcuts、appwidget-provider，或导航图里有页面；目标端有 module.json5 的 abilities、extensionAbilities、skills、metadata，app.json5 的 configuration，或 profile 下的 main_pages.json、form_config.json 时
- [权限声明](resource/permissions/index.md)（12 条）：源 AndroidManifest 有 uses-permission，或目标 module.json5 的 requestPermissions 里要声明 ohos.permission.* 时
- [原始文件（rawfile）](resource/rawfile/index.md)（3 条）：源工程 src/main/assets 下有音频、预置数据等文件，代码用 AssetManager、openFd 按文件名读；目标端有 resources/rawfile 和 getRawFd 时
- [资源名和资源键](resource/resource-keys/index.md)（5 条）：目标端 resources 下有 media 文件和 element/*.json 的条目，页面用 $r('app.…')、module.json5 用 $string: 引用它们，或源 res 来自 apktool 反编译、资源由转换脚本批量生成写回时
- [字符串](resource/strings/index.md)（29 条）：源端有 res/values*/strings.xml、arrays.xml 和 values-* 语言目录，或控件、代码引用的 @string、@android:string、android.R.string 文案；目标端有 string.json、strarray.json 和语言限定词目录时
- [三方 SDK 和插件](resource/third-party-sdk/index.md)（2 条）：源端接了微信 OpenSDK 等三方 SDK 或 Flutter 插件；目标端有 oh-package.json5 的依赖、querySchemes，或根 pubspec.yaml 的 dependency_overrides 时

## 规格（spec）

- [验收条目与验收判定](spec/acceptance/index.md)（14 条）：规格里有验收条目（AC）和它挂的源码真值、UT 设计，或交回的验收报告、回归诊断给出 PASS、「两端一致」这类判定时
- [标题栏、菜单与抽屉](spec/app-bar/index.md)（18 条）：读到源端有菜单 XML（showAsAction）、上下文菜单、ActionBar / Toolbar / TopAppBar、DrawerLayout + NavigationView，规格里写标题栏、Up 箭头、溢出菜单、折叠顶栏和抽屉时
- [本地数据与偏好](spec/data/index.md)（34 条）：读到源端的数据库、JSON 解析、assets 预置数据、外部存储，或偏好 XML、SharedPreferences / DataStore，规格里写数据表、存储、设置页和偏好键时
- [弹窗与提示](spec/dialog/index.md)（26 条）：读到源端弹 AlertDialog、Dialog、经工具类或 Helper 弹的弹窗、BottomSheetDialogFragment / ModalBottomSheet、BottomSheetBehavior 面板或 Toast，规格里写弹窗清单、底部面板和提示时
- [图形与自绘](spec/graphics/index.md)（29 条）：读到源端有自定义 View 的 onDraw / Paint / SurfaceView、Compose 绘制修饰符、@drawable 引用的外观、共享组件里的形状或动画，规格里写画布、图片、阴影描边和动画时
- [布局与尺寸](spec/layout/index.md)（15 条）：读到源布局的 LinearLayout、ConstraintLayout、NestedScrollView、TableLayout、代码里循环 addView 搭的视图，或 Compose 的 Column、Modifier 链、自定义 Layout，规格里写容器映射、对齐、权重和尺寸时
- [生命周期与配置重建](spec/lifecycle/index.md)（24 条）：读到 Activity 的 onCreate、onResume、onPause、onSaveInstanceState、getLastNonConfigurationInstance、configChanges，Compose DisposableEffect、LifecycleEventObserver，或 Application 初始化链，规格里写生命周期映射、存档和刷新时机、配置变化重建时
- [列表、网格与翻页](spec/list/index.md)（18 条）：读到源端有 ListView、GridView、RecyclerView / GridLayoutManager、LazyColumn / LazyRow、SmartRefreshLayout、ViewPager2 或 ActionMode 多选，规格里写列表、网格、刷新分页和翻页时
- [源码逻辑与数值](spec/logic/index.md)（46 条）：读到源码里决定结果的分支、异常、集合遍历、float 运算、常量、格式化、日期时间和线程调用，规格的 AC、映射行或源码笔记要按它写出确切行为时
- [页面导航与入口](spec/navigation/index.md)（57 条）：读到源端的 startActivity / Intent、finish、返回键、Compose NavHost、FragmentTransaction、导航图，或 LAUNCHER、闪屏、深链 intent-filter，规格里写导航表、返回落点、启动路由和外部入口时
- [网络接口与同步](spec/network/index.md)（25 条）：读到 Retrofit Service、OkHttp 拦截器、Gson 和 Bean 模型、按异常类型分的网络失败、响应解密钩子，或待推送队列和同步任务，规格里写 API 表、请求头、错误码表、响应契约、测试环境和同步顺序时
- [平台差异决策与偏离](spec/platform-gap/index.md)（24 条）：规格或决策台账里写了「无对等」「降级」「不迁移」「PD」「显式差异」「用户例外」这类平台差异决策和偏离，或写它们的依据栏时
- [资源与应用配置](spec/resource/index.md)（31 条）：读到 res 下的 values-* / layout-* 限定词目录、按名引用的颜色和尺寸资源、AndroidManifest 的 application / activity 声明和 supportsRtl、BuildConfig 开关和多套 base URL，或目标 app.json5 的身份，规格里写资源表、配置值和身份项时
- [迁移范围与功能归属](spec/scope/index.md)（15 条）：规格里写迁移范围、功能归属（page_id ownership、归某 feature）、功能入口页、跨页面共享组件、别的规格留给本文档承接的条目，或引用上游清单和台账（api-inventory、skip-list）时
- [源码证据与页面元数据](spec/source-evidence/index.md)（23 条）：交回的 meta.json、基线快照或源码理解笔记里有页面元数据、合成的快照，或写了没读到定义的谓词、空子模块里的实现、声明没保证的回调顺序、实现建议的出处这类不确定项时
- [页面状态与数据流](spec/state/index.md)（12 条）：读到 ViewModel、LiveData / StateFlow、remember、data class copy、Activity 实例字段和 static 字段，规格里写状态契约、状态接口表（@Local）、复位和数据流时
- [系统能力、设备与三方 SDK](spec/system/index.md)（47 条）：读到源端用蓝牙、NFC、定位、剪贴板等系统服务，WorkManager、前台 Service、常驻通知，MediaPlayer / SoundPool，分享面板，或厂商 SDK、Flutter 插件，规格里写这些能力的映射、权限和降级时
- [主题、颜色与默认外观](spec/theme/index.md)（46 条）：读到 styles.xml / themes.xml 的主题继承（AppCompat、MaterialComponents、Material3、android:Theme.*）、?attr/ 主题属性、Color.* 常量，或源控件没写颜色和外观属性，规格里写主题色、控件默认外观和颜色映射时
- [文本、控件与触摸](spec/widget/index.md)（33 条）：读到源端有 TextView、EditText、Slider、WebView 等控件或 Compose Text / TextStyle，onTouch、GestureDetector、SwipeToDismissBox 触摸处理，contentDescription 等无障碍语义，规格里写文本样式、输入约束、控件状态和手势时
- [窗口与系统栏](spec/window/index.md)（24 条）：读到源端有状态栏、导航栏、全屏和沉浸的写法（FLAG_FULLSCREEN、NoTitleBar 主题、WindowInsets、fitsSystemWindows、ImmersionBar、windowBackground、FLAG_KEEP_SCREEN_ON），或规格里写沉浸式、安全区避让、系统栏颜色和窗口背景时
