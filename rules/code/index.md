# 代码（code）

523 个族，1874 条规矩。整个产物的族一页看完见 [map.md](map.md)（每个主题一行，下面是「短号 族名（条数）」）。

## 一级主题

- [ArkTS 语法与工程](arkts/index.md)（41 条）：交回的 .ets 里有 @Builder、@BuilderParam、@ComponentV2 成员、.stateStyles、Record 和对象字面量，或构建日志报 arkts-* 和组件语法错误，或涉及 BuildProfile、HAR 模块和跨文件导入时
- [数据与存储](data/index.md)（99 条）：源端有 SharedPreferences / MMKV、Room / SQLite、Gson / org.json 模型、XML 解析、Repository / Dao 的调用和同步进度事件、文件读写和 ZIP、种子数据，目标端有 preferences、relationalStore、模型 class、JSON.parse、fs 读写时
- [生命周期与启动](lifecycle/index.md)（48 条）：源端有 Activity / Fragment 的 onCreate、onStart、onResume、onPause、onDestroy、闪屏和初始化、configChanges、savedInstanceState、Compose DisposableEffect，目标端有 EntryAbility 的回调、aboutToAppear / aboutToDisappear、onShown / onHidden、onReady 时
- [业务逻辑与源码语义](logic/index.md)（140 条）：源端有 Java / Kotlin 的分支条件、回调分支、提交前校验、ViewModel 方法在请求前后的步骤、工具类静态入口起的业务链、数值运算、集合遍历、异常捕获、协程并发、字符串和字节处理、日期计算，目标端有照着移植的 TS 业务代码时
- [音视频与媒体选取](media/index.md)（101 条）：源端有 VideoView、MediaPlayer、ExoPlayer / PlayerView、SoundPool、MediaController、选图和选文件的 Intent，目标端有 Video、AVPlayer、SoundPool、XComponent、PhotoViewPicker、SaveButton 时
- [页面导航与标题栏](navigation/index.md)（192 条）：源端有 startActivity / Intent、跳板 Activity 和透明主题的 Activity、Fragment 事务、Compose Navigation、onBackPressed、Activity 切换转场、Toolbar / ActionBar、DrawerLayout，目标端有 Navigation、NavDestination、NavPathStack、router.pushUrl、pageTransition、自绘标题栏时
- [网络](network/index.md)（42 条）：源端有 Retrofit 接口注解、OkHttp / OkGo 请求和拦截器、BaseResponse 响应壳、BuildConfig 里的服务地址，目标端有 @ohos.net.http 的封装、请求 url 和 header、响应解包时
- [占位、规格与测试](placeholder/index.md)（50 条）：派工、占位登记或代码注释里有 FWD-REF、PLACEHOLDER、P-ID 条目，规格的 AC、台账里的「平台无对等」，孤儿检测报 NO_IMPORTER，或单测、派工的要求和源端不同时
- [状态与数据流](state/index.md)（73 条）：源端有 ViewModel、LiveData / Flow、Compose remember / mutableStateOf、EventBus、data class copy，目标端有 @Local、@Param、@ObservedV2 / @Trace、@Monitor、AppStorageV2、@Builder 传参和页面的加载、空、错误状态时
- [系统能力与设备](system/index.md)（89 条）：源端有运行时权限、通知、WorkManager、地图和定位 SDK、NFC、蓝牙、网络状态、振动、OAID、Cipher 加解密、桌面小部件、登录授权 SDK、FlutterBoost，目标端有对应的 @ohos / @kit 接口、FormExtensionAbility 或三方 SDK 桥接时
- [界面](ui/index.md)（987 条）：源端是布局 XML 里的 View 控件或 Compose 界面元素（文字、图片和自绘、布局容器、列表和翻页、弹窗和提示、点击和输入控件、动效、主题和颜色、窗口和系统栏、三方库的自定义 View），目标端是 ArkUI 组件和它的尺寸、样式、属性时
- [网页](web/index.md)（12 条）：源端有 WebView、WebViewClient、WebSettings、loadDataWithBaseURL，目标端有 Web 组件、WebviewController、onLoadIntercept、onErrorReceive 时
