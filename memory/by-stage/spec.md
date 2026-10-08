# 阶段：规格提取（spec）

本阶段可用的 88 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/capability](../topics/app/capability/index.md) — 平台能力与厂商 SDK 的等价判定：先查 Kit、ohpm 与本地声明再选型，不可用时运行期显式降级而非阻断或伪造

- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](../topics/app/capability/lesson-e9890889e591196c3d0d.lesson.md) · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit
- [应用内开关蓝牙先查 access 开关接口再定方案](../topics/app/capability/lesson-7a081dc36013a60358ac.lesson.md) · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable
- [无 OHOS 实现的插件先按底层能力建本地兼容插件](../topics/app/capability/lesson-45739c78f9767dacbc81.lesson.md) · 信号：dependency_overrides, platform_interface, MethodChannel, ohos/flutter_plugins
- [激励广告不可用时显式提示并按台账放行，不伪造奖励](../topics/app/capability/lesson-0f67121af7969203b76b.lesson.md) · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward

### [app/cross-cutting](../topics/app/cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

- [开关控制的常驻通知由应用级服务持有，不随页面 VM](../topics/app/cross-cutting/lesson-e9f03fcc7f1e781c4b24.lesson.md) · 信号：notificationManager.publish, aboutToAppear, aboutToDisappear, NavDestination
- [诊断日志上传按源端打包清单与协议实现，收窄先确认](../topics/app/cross-cutting/lesson-d434bb5c16bc721d9a00.lesson.md) · 信号：usesCleartextTraffic, networkSecurityConfig, presignedUrl, http.request

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入声明、扩展能力与卡片登记

- [前台服务改扩展能力先查基类导出，type 与基类成对](../topics/app/entry/lesson-16c24b9a44153d703f04.lesson.md) · 信号：extensionAbilities, ServiceExtensionAbility, AppServiceExtensionAbility, WorkSchedulerExtensionAbility
- [外部入口页需确定快捷声明、Want 分支与参数写者](../topics/app/entry/lesson-c46f182cf1d01a97e05f.lesson.md) · 信号：ohos.ability.shortcuts, shortcuts_config.json, onNewWant, Want
- [深链迁移要声明 skills，用隐式 Want 验收](../topics/app/entry/lesson-d77baa7494930d485425.lesson.md) · 信号：ohos.want.action.viewData, entity.system.browsable, pathStartWith, intent-filter

### [app/hybrid](../topics/app/hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

- [Flutter 宿主迁移要打开实际容器子类逐项迁事件桥接](../topics/app/hybrid/lesson-6717b958e274143453a8.lesson.md) · 信号：FlutterBoostFragment, addEventListener, sendEventToFlutter, FlutterUIComponent
- [通道方法集按原生分支全集与 Dart 调用点双向对照](../topics/app/hybrid/lesson-e6b1032f702fc61940f2.lesson.md) · 信号：MethodChannel, setMethodCallHandler, call.method, invokeMethod

### [app/map](../topics/app/map/index.md) — 地图与定位接入：SDK 单例初始化与就绪、定位权限成组、坐标系与行政区名补齐、原生地图组件生命周期

- [定位只给坐标时用逆地理编码取行政区名，不留空名](../topics/app/map/lesson-a317e16cd9f46aa34962.lesson.md) · 信号：geoLocationManager.getAddressesFromLocation, geoLocationManager.getCurrentLocation, AMapLocation, subLocality

### [app/media](../topics/app/media/index.md) — 媒体文件的用户可见出入口：安全控件与 picker 授权时序、沙箱落点与导出、播放 URI、预取与快照尺寸限制

- [公共目录产物改落沙箱时每条链写出导出步骤](../topics/app/media/lesson-b59097ee968fe827f70d.lesson.md) · 信号：WRITE_EXTERNAL_STORAGE, ACTION_MEDIA_SCANNER_SCAN_FILE, DocumentViewPicker.save, MediaScannerConnection
- [图库选图用 PhotoViewPicker 并复制进应用目录](../topics/app/media/lesson-ad1db0aa0434c2e766fd.lesson.md) · 信号：PhotoViewPicker, READ_IMAGEVIDEO, MediaStore, photo_manager
- [音频导入用 AudioViewPicker 并复制进沙箱](../topics/app/media/lesson-62ac5e65ac4aa51128bd.lesson.md) · 信号：AudioViewPicker, photoAccessHelper, MediaStore.Audio, READ_MEDIA_AUDIO

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [沿用脚手架包名前核对决策与签名；vendor 按源端落地](../topics/app/resources/lesson-fb996956b33a1ba65861.lesson.md) · 信号：bundleName, com.example, applicationId, app.json5

### [app/startup](../topics/app/startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

- [延后采集通道时单独移植超时兜底发布就绪事件](../topics/app/startup/lesson-99a8d47085e4b1ae44de.lesson.md) · 信号：OaidResultEvent, Observable.timer, FWD-REF, OAID
- [源端启动固定进主页时目标也进主页，登录页压在其上](../topics/app/startup/lesson-4c254d10ef9264683c55.lesson.md) · 信号：SplashActivity, NavPathStack, pushPathByName, LoginGuard
- [目标初始化极快时把首启加载页最短可见时长写进验收](../topics/app/startup/lesson-41bb62cd13921e4eedde.lesson.md) · 信号：SplashActivity, SplashScreen, windowStage.loadContent, setTimeout
- [迁启动链路时列出各去向页初始化请求与登录态组合](../topics/app/startup/lesson-8c24f05ec8df45401482.lesson.md) · 信号：initRequestData, SplashActivity, MainActivity, refreshToken
- [首启无已选项时定义显式空态，不以空编码请求](../topics/app/startup/lesson-95aa64d6b0a5c041d326.lesson.md) · 信号：hasInit, selectedCity, cityCode, preferences
## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/api-signatures](../topics/arkts/api-signatures/index.md) — 调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定

- [依赖 API 单位或默认行为时读声明紧邻注释](../topics/arkts/api-signatures/lesson-f5cf8413ebea57f3b415.lesson.md) · 信号：vp2px, .d.ts, vp, px
- [属性方法不传 ResourceStr 联合值按重载定型](../topics/arkts/api-signatures/lesson-63660a8304f7d3920bfc.lesson.md) · 信号：accessibilityText, ResourceStr, @Computed, contentDescription

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [组件成员名避开 position/width 等通用属性](../topics/arkts/ui-syntax/lesson-c1968bdf112ed3e6b259.lesson.md) · 信号：zIndex, @Param
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/network-auth](../topics/data/network-auth/index.md) — 鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者

- [token 失效判定按响应拦截器实际分支的码迁移](../topics/data/network-auth/lesson-bad79e090d2af44d167b.lesson.md) · 信号：reasonCode, HandleErrorInterceptor, TokenInterceptor, LoginExpired
- [响应头携带 token 时 HTTP 封装连头一起返回](../topics/data/network-auth/lesson-2a4e6af209308c08aaa6.lesson.md) · 信号：headers()\["Authorization"\], RefreshToken, Response&lt;BaseResponse, TokenManager

### [data/network-endpoint](../topics/data/network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

- [服务地址沿键名追到源端常量，host 与环境不自拟](../topics/data/network-endpoint/lesson-246252824c631aa6eff5.lesson.md) · 信号：BuildConfig.BASE_URL, SpKey.BASE_URL, NetworkModule, baseUrl

### [data/network-request](../topics/data/network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

- [Service 收不透明 body 时追到源端构造处照抄字段](../topics/data/network-request/lesson-0bc494e864b2d8ab1a34.lesson.md) · 信号：@Body, RequestBody, data: Object, device_id

### [data/parsing](../topics/data/parsing/index.md) — JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度

- [大整数 id 用 bigint，解析前给数字加引号保真](../topics/data/parsing/lesson-c066489fcf35ab37378c.lesson.md) · 信号：JSON.parse, bigint, Long, 2^53

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作

- [手写建表 SQL 表名列名统一加引号，关键字不裸写](../topics/data/storage/lesson-c55c56444f5271471a64.lesson.md) · 信号：CREATE TABLE, createSql, relationalStore, executeSql
- [按日期实时计算的字段不改绑静态资产，先查内置能力](../topics/data/storage/lesson-6d259db1ffd8927834a2.lesson.md) · 信号：Lunar.fromDate, dayYi, dayJi, Intl.DateTimeFormat
- [演示预置数据逐字段取自源种子工厂与 assets 不自拟](../topics/data/storage/lesson-1c513fdf2cf212354aa0.lesson.md) · 信号：DemoDataFactory, rawfile, LocalDate.now(), plusDays

### [data/sync](../topics/data/sync/index.md) — 同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤

- [同步调度合并在途任务要补跑尾随请求，失败项重推](../topics/data/sync/lesson-cfe552e1b20080212ce9.lesson.md) · 信号：Mutex.withLock, Promise
- [重写多阶段数据流程时保留缓存写入等副作用步骤](../topics/data/sync/lesson-686bbe76f7c2c783f2bd.lesson.md) · 信号：DAO, currentId, Repository
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [点击入口写具体导航契约，无兑现方不留 forward-ref](../topics/process/deferred-fulfillment/lesson-7f6b818559cfac767e4b.lesson.md) · 信号：forward-ref, WebView, URL, Intent
- [规格留待裁决条目，决策轮逐条出题或关闭](../topics/process/deferred-fulfillment/lesson-35b9cdfd5d22ce53465e.lesson.md) · 信号：待裁决, Kit, decision ledger, placeholder

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [Application 注册的接收器读本体写入规格](../topics/process/enumeration-gaps/lesson-4fb1c103822a8fd30b2a.lesson.md) · 信号：BroadcastReceiver, registerReceiver, CONNECTIVITY_ACTION, @ohos.net.connection
- [ViewModel 每步须有 feature 认领或跨契约](../topics/process/enumeration-gaps/lesson-431a65808f9b46b95974.lesson.md) · 信号：initData, getPlaceById, queryPlaceById, homeV2
- [导航目的地写页面入参契约：名、类型、可空与读取方式](../topics/process/enumeration-gaps/lesson-f4d335605b44a60116b9.lesson.md) · 信号：nav_graph, &lt;argument&gt;, requireArguments(), getString
- [应用壳契约枚举源导航全部入口含深链与 scheme](../topics/process/enumeration-gaps/lesson-3348c580951ef82a9737.lesson.md) · 信号：NavPathStack, onNewWant, onCreate, module.json5
- [截图页范围含其入口直达二级页，不取最窄解释](../topics/process/enumeration-gaps/lesson-91c89aff3f8c5c47bd2a.lesson.md) · 信号：startActivity, Intent, Activity, setOnClickListener
- [窗口/控件封装类的分叉可见行为逐项写入契约](../topics/process/enumeration-gaps/lesson-5948050d3b6dc39239a4.lesson.md) · 信号：setOffline, setEnabled, FootBar, SharedPreferences
- [系统表面降级为应用内页时写明入口位置与形式](../topics/process/enumeration-gaps/lesson-238588d3cceaf707ccfe.lesson.md) · 信号：Widget, AppWidget, FormExtensionAbility, LongPressGesture
- [验收条目实读源码段落，照抄比较符并给边界样例](../topics/process/enumeration-gaps/lesson-08854573a81a9fa03746.lesson.md) · 信号：width &gt; 600, Linkify, grep, ViewModel

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [源端层层委托时追到最终实现再写规格与代码](../topics/process/inferred-not-traced/lesson-4606ccc434e247d4a240.lesson.md) · 信号：DialogHelper, DAO, Repository, LazyColumn
- [辅助谓词与 getter 读到定义再翻译，不按名字推断](../topics/process/inferred-not-traced/lesson-b3f534eb740a768d95a6.lesson.md) · 信号：isPlayingState, playPause, LiveData&lt;String&gt;, PAUSED
- [页面入口只按布局与页面类实际绑定推导，不补源端没有的控件](../topics/process/inferred-not-traced/lesson-76aa7901a0ae1af9d544.lesson.md) · 信号：initView, setOnClickListener, ViewModel, onClick
- [页面归属按实际 Service 调用判定，不按模块默认](../topics/process/inferred-not-traced/lesson-ad7d770bd5b826e58516.lesson.md) · 信号：resolve_by, Retrofit, Service, page_id

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [共享组件挂载页面以源宿主容器 replace/add 为准](../topics/process/secondary-over-source/lesson-34c8ac69ad849f8c24e1.lesson.md) · 信号：FragmentTransaction, replace(, add(, Fragment
- [合成快照点击清单空时按源布局 onClick 绑定实现跳转](../topics/process/secondary-over-source/lesson-3ea52b78643f49c13cd1.lesson.md) · 信号：android:onClick, @{page::, view_xml_synthesized, clickable_elements
- [多模块同名布局按页面类模块与 Binding 类解析](../topics/process/secondary-over-source/lesson-d75ddb53d6609b35d025.lesson.md) · 信号：layout_sources, ViewBinding, DataBinding, fragment_mine.xml

### [process/unloaded-input](../topics/process/unloaded-input/index.md) — 必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../topics/process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md) · 信号：Get-Content, Select-String, -Encoding UTF8, $OutputEncoding
- [必读 skill 与源码逐份读全，截断即重读再写码](../topics/process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md) · 信号：SKILL.md, sed -n, loaded_skills, rg

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [生成期无法核验的结论标置信度，不定 HARD 或具体 dp](../topics/process/unverified-as-fact/lesson-c0f990ea57a901951ba8.lesson.md) · 信号：HARD, dp, SDK
- [规格所需值上游缺失时回源码补或标待核，不自拟](../topics/process/unverified-as-fact/lesson-77ca67f164d77ec63cda.lesson.md) · 信号：api-inventory.json, auth_model, common.md, raw_apis.json
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/dialog/carriers](../topics/ui/dialog/carriers/index.md) — 按源弹层类型选载体：真弹窗不以页面叠层或路由页充当、V2 页面的弹窗 API、锚定下拉与自定义内容。

- [当前页 show 的底部弹窗叠在宿主页上不改路由页](../topics/ui/dialog/carriers/lesson-7ef02de8bbc10734c3d2.lesson.md) · 信号：bottomDialog, BottomSheetDialog, HMRouter, Navigation

### [ui/interaction/hit-testing](../topics/ui/interaction/hit-testing/index.md) — 叠放层的命中测试与手势归属：全尺寸覆盖层透传、Block 只放遮罩、侧滑行按钮热区、滑删方向与触发瞬间的坐标取值。

- [SwipeToDismissBox 方向按手势与偏移符号写明](../topics/ui/interaction/hit-testing/lesson-7f5eba1b969bddfb34dc.lesson.md) · 信号：SwipeToDismissBox, enableDismissFromStartToEnd, EndToStart, StartToEnd

### [ui/interaction/selectors](../topics/ui/interaction/selectors/index.md) — 选择控件的选项、初值与选中标记：选项按源数据源、自定义属性初值、级联回填、条件勾选不换 Radio、Slider 步数。

- [Slider steps 翻步长：区间/(steps+1)](../topics/ui/interaction/selectors/lesson-d715fa78ada2e79a5fd2.lesson.md) · 信号：Slider, valueRange

### [ui/layout/constraints](../topics/ui/layout/constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。

- [单视图居中加兄弟悬挂用 RelativeContainer](../topics/ui/layout/constraints/lesson-e607a28fcd91acd2b40f.lesson.md) · 信号：RelativeContainer, alignRules, __container__, constraintTop_toBottomOf

### [ui/layout/intrinsic](../topics/ui/layout/intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。

- [Material 按钮区分布局占位、背景实绘与触控范围](../topics/ui/layout/intrinsic/lesson-b73a1ac8908f74856a02.lesson.md) · 信号：minimumInteractiveComponentSize, IconButton, Surface, Box
- [贴合内容的描边背景写在内容节点不用 100% 覆盖层](../topics/ui/layout/intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md) · 信号：matchContentSize, fillMaxSize, Modifier.border, HitTestMode.None

### [ui/layout/safearea](../topics/ui/layout/safearea/index.md) — 全屏窗口安全区：避让值单位、expandSafeArea 与前景 padding 之别、inset 只消费一次及承载层

- [Tab 宿主不统一加顶部安全区，按子页源处理分别避让](../topics/ui/layout/safearea/lesson-48e9408812c28e934db8.lesson.md) · 信号：ImmersionBar, statusBarView, titleBarMarginTop, fitsSystemWindows
- [innerPadding 顶部即状态栏高，目标只在一处避让](../topics/ui/layout/safearea/lesson-f64afc22d41b130f1628.lesson.md) · 信号：Scaffold, innerPadding, consumeWindowInsets, contentWindowInsets

### [ui/layout/scrolling](../topics/ui/layout/scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。

- [Lazy 首尾留白用 contentStartOffset](../topics/ui/layout/scrolling/lesson-4030f978a230df37de2b.lesson.md) · 信号：contentStartOffset, contentEndOffset, contentPadding, PaddingValues
- [只把源滚动区子节点放进 Scroll，固定头部留外面](../topics/ui/layout/scrolling/lesson-46a0d7f239efac925d33.lesson.md) · 信号：NestedScrollView, layout_below, layout_weight, layoutWeight(1)

### [ui/layout/sizing](../topics/ui/layout/sizing/index.md) — 满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。

- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](../topics/ui/layout/sizing/lesson-45f77b3088fa69398f9e.lesson.md) · 信号：fillMaxWidth, requiredWidth, Visibility.Hidden, layoutWeight(1)
- [整数 px 公式在 px 域取整再 px2vp 写入属性](../topics/ui/layout/sizing/lesson-0ef2cd00e1a91491b350.lesson.md) · 信号：px2vp, vp2px, measureText, onAreaChange
- [背景之前的 padding 放外层，背景圆角裁剪放内层](../topics/ui/layout/sizing/lesson-5c6217b05bb4c266f254.lesson.md) · 信号：statusBarsPadding, navigationBarsPadding, Surface, borderRadius

### [ui/list/behaviors](../topics/ui/list/behaviors/index.md) — 列表容器行为：侧栏与分组列表的滚动联动、组头默认展开、Repeat 虚拟滚动的项高度核对、swipeAction 挂载。

- [分类页右侧用 Scroller 列表双向联动迁滚动保护](../topics/ui/list/behaviors/lesson-7723af3766fb843a2577.lesson.md) · 信号：scrollToIndex, onScrollIndex, Scroller, LazyListState

### [ui/list/data-sources](../topics/ui/list/data-sources/index.md) — 列表数据源的绑定与并发：各列表各自的数据与排序器、本地变换随列表迁移、分页门闩、代次保护与行内在途锁。

- [onReachEnd 分页加载中不重入、刷新中不派发](../topics/ui/list/data-sources/lesson-0a398b212a8a80bd0c7f.lesson.md) · 信号：SmartRefreshLayout, onReachEnd, onRefreshing, setOnLoadMoreListener

### [ui/list/items](../topics/ui/list/items/index.md) — 条目类型与渲染分支：多 viewType 卡片外观、绑定代码里的区块与模板、跨列占位、副行回退、配置驱动分派。

- [多类型卡片外观按各类 holder 取，不共用一套](../topics/ui/list/items/lesson-9de4c7648d23db5d7f86.lesson.md) · 信号：cardCornerRadius, viewType, ViewHolder, CardView
- [恒空占位不在多列 Grid 生成通栏 GridItem](../topics/ui/list/items/lesson-2bd2620e5d1ef4bb17b4.lesson.md) · 信号：spanSizeLookup, GridLayoutManager, GridItem, WaterFlow

### [ui/list/pager](../topics/ui/list/pager/index.md) — ViewPager 到 Swiper：页数与禁滑方式、初始页用 index 绑定、自绘 tab 双向联动与日历翻页容器

- [单页不用 Swiper；禁滑用 disableSwipe](../topics/ui/list/pager/lesson-540747e352d7f006016d.lesson.md) · 信号：ViewPager2, disableSwipe, isUserInputEnabled, Swiper

### [ui/navigation/back-stack](../topics/ui/navigation/back-stack/index.md) — 返回键与栈变更：覆盖层逐层关闭、按启动来源的返回分支、子组件拦截返回、清栈重建与重复导航的净效果。

- [tab 与深链的返回栈后果写验收并显式实现](../topics/ui/navigation/back-stack/lesson-39f137ee173e50363f79.lesson.md) · 信号：popUpTo, saveState, restoreState, launchSingleTop
- [同一成功多条导航响应只保留一个导航出口](../topics/ui/navigation/back-stack/lesson-683d8f5070802c518020.lesson.md) · 信号：FLAG_ACTIVITY_NEW_TASK, finish(), startActivity, NavPathStack

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [多屏共享清理归外层生命周期，切屏不释放](../topics/ui/navigation/hosts/lesson-2ed8c21943925bf0ae9a.lesson.md) · 信号：DisposableEffect, onDispose, EntryAbility.onDestroy, aboutToDisappear

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [全局广播浮层按源端队列语义播放不自加去重上限](../topics/ui/state/feedback/lesson-2cc8bcca579d597cb6a2.lesson.md) · 信号：addAll, remove(0), onAnimationEnd, WindowManager
- [推迟通知能力时为接口返回数据定义替代去向](../topics/ui/state/feedback/lesson-9d54e42c44b0d3e78bb1.lesson.md) · 信号：NotificationManager, onData, Toast, showToast

### [ui/state/lifecycle](../topics/ui/state/lifecycle/index.md) — 生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

- [翻译 remember 复位语义时列出框架会恢复的界面态](../topics/ui/state/lifecycle/lesson-1f6e36f8e8bf9df951da.lesson.md) · 信号：rememberSaveable, pushPath, NavBar, Tabs

### [ui/state/observation](../topics/ui/state/observation/index.md) — 共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。

- [判字段是否需 @Trace 前先读其修改方法与显示界面](../topics/ui/state/observation/lesson-4d1c980bbbd20275f5c3.lesson.md) · 信号：@Trace, @ObservedV2, data class, copy(

### [ui/text/typography](../topics/ui/text/typography/index.md) — 文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

- [单行盒高与多行行距分开，lineHeight 不同名直映](../topics/ui/text/typography/lesson-2a2924aaebbfbea80780.lesson.md) · 信号：lineHeight, .lineHeight(), lineSpacing, LengthMetrics.fp
- [多行省略末行粒度两端不同，规格写差异再测量兜底](../topics/ui/text/typography/lesson-836a5414b52f0e062f1f.lesson.md) · 信号：maxLines, TextOverflow.Ellipsis, android:ellipsize, textOverflow

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [blendMode 着色把底色字形渐变放同一离屏组](../topics/ui/theme/effects/lesson-3024193e4816229c5370.lesson.md) · 信号：blendMode, BlendApplyType, drawWithContent, BlendMode.Plus
- [elevation 阴影按 vp2px 换算并集中到共享函数](../topics/ui/theme/effects/lesson-d0aad947e26220fb43fa.lesson.md) · 信号：ShadowOptions, Modifier.shadow, vp2px, .shadow(

### [ui/theme/sources](../topics/ui/theme/sources/index.md) — 控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

- [M3 组件默认几何与留白从库 Tokens 分侧取值](../topics/ui/theme/sources/lesson-5a82d62ff7e087616968.lesson.md) · 信号：TopAppBar, Snackbar, Slider, MaterialTheme.colorScheme
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../topics/ui/theme/sources/lesson-47785524c7f132ea7efe.lesson.md) · 信号：colorPrimary, colorOnPrimary, Theme.MaterialComponents, LocalContentColor
- [布局引用的 @drawable 先打开取数值写进规格与修饰链](../topics/ui/theme/sources/lesson-771d1ba1a032b769097a.lesson.md) · 信号：progressDrawable, textCursorDrawable, layer-list, caretStyle

### [ui/theme/tokens](../topics/ui/theme/tokens/index.md) — 颜色与字体令牌的落地：按色值反查资源键、深色目录同步、深浅状态的可观察与系统栏图标、字族注册。

- [“零硬编码色值”只禁字面值，允许 $r 引用语义色](../topics/ui/theme/tokens/lesson-2e4279c4b82f06af64fd.lesson.md) · 信号：$r('app.color, #RRGGBB, backgroundColor, fontColor
