代码：523 个族，1874 条规矩。用短号取族（如 recall.py show f001）。

ArkTS 语法与工程（41 条）：交回的 .ets 里有 @Builder、@BuilderParam、@ComponentV2 成员、.stateStyles、Record 和对象字面量，或构建日志报 arkts-* 和组件语法错误，或涉及 BuildProfile、HAR 模块和跨文件导入时
ArkTS 语法与工程 / 构建与模块（18 条）：源端有 BuildConfig 字段，或交回的代码涉及 BuildProfile、HAR 模块、跨模块和跨文件的 import / export、新建的常量类文件，或为修编译错误改过文件时
  f237 BuildConfig 的构建字段（DEBUG、VERSION_NAME、VERSION_CODE）（3）；f241 新建的主题令牌、常量类 .ets 文件（2）
  f259 HAR 模块里的 BuildProfile 和跨模块导入（4）；f315 为修编译错误改过的文件（2）；f325 禁编译时一次写出的整页文件（1）；f343 被搬页面归到哪个模块（1）；f352 跨文件复用的函数的导出和导入（2）
  f354 编译报错后删改的调用和基类（2）；f707 循环导入和顶层继承的初始化顺序（1）
ArkTS 语法与工程 / 组件语法与装饰器（11 条）：交回的 .ets 里有 @Builder / @BuilderParam、build() 里的组件写法、@ComponentV2 的 @Param / @Local / @Event 成员、.stateStyles，或构建报 10905102、10905203 这类错误时
  f100 @BuilderParam 插槽的传参和默认值（4）；f101 build() 和 @Builder 里的组件语法（2）；f199 V2 组件的成员装饰器和成员名（2）
  f216 .stateStyles 的写法和 10905203 报错（3）
ArkTS 语法与工程 / 类型约束（12 条）：交回的代码里有 Record、索引签名、无类型的对象字面量、implements 和构造写法、process.getEnvironmentVar 这类可选值，或构建报 arkts-no-* 类型错误时
  f154 Record 类型和索引签名（3）；f155 没有声明类型的对象字面量（3）；f156 接口的实现和类的构造写法（3）；f219 构建报错里的 SDK 类型约束（2）
  f367 process.getEnvironmentVar 读出的可选配置（1）
数据与存储（99 条）：源端有 SharedPreferences / MMKV、Room / SQLite、Gson / org.json 模型、XML 解析、Repository / Dao 的调用和同步进度事件、文件读写和 ZIP、种子数据，目标端有 preferences、relationalStore、模型 class、JSON.parse、fs 读写时
  f091 照源码移植的 Service、Repository 和 Dao 调用（4）；f094 同步和后台操作的进度、状态事件（4）；f267 共享和按成员两种完成状态的 userId 写入（2）
  f268 文件读写、建目录和 ZIP 打包（11）；f360 演示和种子数据（1）；f792 DAO 读写里的加解密钩子（2）
数据与存储 / 数据库（19 条）：源端有 Room 的 @Database / @Entity / @PrimaryKey / Migration、SQLiteOpenHelper，目标端有 relationalStore 的 getRdbStore、CREATE TABLE、insert、事务时
  f209 Room 数据库迁成 relationalStore 的建表和版本（6）；f292 源端 SQLite 落库的主键、时机和建库（5）
  f298 Room 自增主键 @PrimaryKey(autoGenerate = true) 的写入（2）；f299 RdbStore 的事务接口（beginTrans 与 beginTransaction）（3）
  f767 Room 的 UPDATE / DELETE 返回的受影响行数（2）；f805 Cursor 按文本读回的数值列（1）
数据与存储 / 数据模型与解析（39 条）：源端有 Kotlin data class / Java bean、Gson 的 @SerializedName、org.json 的 JSONObject、enum、SAX / XmlPullParser，目标端有模型 class、JSON.parse 后的取值、@ohos.xml 解析时
  f052 Gson 模型里的 Long 字段和 JSON 数值的解析（5）；f173 从 Kotlin data class 迁来的模型类和 JSON 解码（5）；f210 org.json 的读取和序列化语义（4）
  f211 逐条解析和导入时单条记录出错的处理（2）；f232 移植的模型类和它的构造器（3）；f303 @ohos.xml 的 XmlPullParser 解析回调（2）；f356 共享模型的枚举成员和持久化值（1）
  f696 Kotlin @Serializable 模型迁成的 DTO（7）；f697 copy() 建的顶层哨兵对象（1）；f749 Moshi 等解析器解析失败时的结果和错误类型（2）；f761 构造时显式传 null 的引用字段（1）
  f787 源端枚举字段在目标模型里的类型（1）；f800 Jsoup 节点遍历改写成的自研解析器（2）；f807 模型类的 equals 和脏检查方法（1）；f827 Gson 反射序列化写出的 JSON（1）
  f841 Java 实体的数值字段和落库绑定（1）
数据与存储 / 偏好存储（17 条）：源端有 SharedPreferences、MMKV 的读写，目标端有 preferences 的封装、putSync / flush 和它用的 Context 时
  f197 SharedPreferences 迁成 preferences 的偏好存储（9）；f324 MMKV 里持久化的界面切换状态（1）；f328 preferences 用的 Context（1）
  f731 偏好读点的缺省值、读取类型和读取时机（6）
生命周期与启动（48 条）：源端有 Activity / Fragment 的 onCreate、onStart、onResume、onPause、onDestroy、闪屏和初始化、configChanges、savedInstanceState、Compose DisposableEffect，目标端有 EntryAbility 的回调、aboutToAppear / aboutToDisappear、onShown / onHidden、onReady 时
  f059 启动链和初始化的顺序（9）；f060 源端对象、静态字段和监听的存活期（4）；f137 源端生命周期回调里的副作用（6）；f139 入口 Ability 的全局异常监听（errorManager）（1）
  f146 未声明 android:configChanges 时的配置变化重建（9）；f147 进程回收后的页面栈恢复（savedInstanceState、NavHost）（3）
  f193 EntryAbility 的入口页和启动顺序（4）；f230 Compose 的生命周期观察者和 DisposableEffect（4）；f348 onStart / onResume 里每次重做的初始化（1）
  f349 派工要求承接的基类横切钩子（1）；f689 onCreate 里 findViewById 后对子 View 的接线（3）；f719 源端的整应用重启（System.exit、startActivity 后退出进程）（2）
  f754 SavedStateHandle 保存态和数据库值的先后（1）
业务逻辑与源码语义（140 条）：源端有 Java / Kotlin 的分支条件、回调分支、提交前校验、ViewModel 方法在请求前后的步骤、工具类静态入口起的业务链、数值运算、集合遍历、异常捕获、协程并发、字符串和字节处理、日期计算，目标端有照着移植的 TS 业务代码时
  f010 源端的分支条件和执行时机（9）；f083 源 ViewModel 方法在请求、提交前后的步骤（5）；f123 工具类静态入口起的业务链（2）；f218 带结果回调的拦截和分支（2）；f342 提交方法开头的参数校验（1）
  f735 Kotlin 的 when 分支和 ?: 回退链（4）；f779 应用接口的 on* 错误回调和它们的提示（2）；f780 能力门函数（supports…）的多重条件（2）；f795 依赖库里取不到源码的类、方法和常量（6）
  f838 回调接口实现类覆写的回调（1）
业务逻辑与源码语义 / 异步与并发（15 条）：源端有 viewModelScope.launch、多路请求和缓存、Mutex.withLock、Executors 单线程执行器、Thread 轮询重连循环，目标端有 Promise、async / await、请求取消和排队时
  f081 ViewModel 多路请求的部分失败和缓存（5）；f082 协程 launch 的并发和排队（2）；f240 Java 线程、执行器和轮询循环的执行语义（2）；f699 Java 线程和阻塞调用改写成 async（4）
  f806 按键登记的在途任务表（1）；f825 单飞缓存的 Promise 入口（1）
业务逻辑与源码语义 / 集合与顺序（14 条）：源端有 HashSet / HashMap 遍历、addAll、按下标赋值、按引用原地改写数组、filter / sortedBy / Comparator 排序，目标端有 Set、Map、find、slice、.sort 时
  f227 仓库和数据源方法里的集合筛选、排序（4）；f294 列表排序的 Comparator 和排序偏好（2）；f321 Java 集合的遍历顺序和入队语义（5）；f326 按下标给列表项赋值（1）
  f359 按引用原地改写的数组参数（2）
业务逻辑与源码语义 / 日期和时间（11 条）：源端有 Calendar、SimpleDateFormat、时区和周的计算、System.nanoTime、农历算法库，目标端有手写的日期拆分、时区偏移和时钟函数时
  f265 农历算法库（com.nlf.calendar）按日期实时计算的字段（2）；f266 Calendar 和 SimpleDateFormat 的日期、周与时区计算（4）
  f361 System.nanoTime 一类的单调时钟计时（1）；f777 java.time 的 Instant / ZonedDateTime 解析和日期比较（3）；f835 重复规则库（RRULE）的序列化和文案（1）
业务逻辑与源码语义 / 异常与日志（17 条）：源端有 try/catch 按异常类或消息分流、Log.e / Log.w、会抛错的异步初始化，目标端有 catch 的范围、Promise 的 .catch、console.error / hilog 时
  f221 新写或改写的日志调用（2）；f305 异步初始化的 Promise 和 catch 分支（4）；f307 Java 异常的捕获和分流（7）；f338 主体加载和辅助请求共用的 try（1）
  f753 源函数的失败处理范围：try/catch 和 Either 的 Left（2）；f772 BusinessError.code 的错误码判别（1）
业务逻辑与源码语义 / 数值运算（13 条）：源端有 (float) 强转和 f 后缀字面量、Float 相等比较、算式里的倍率和偏移、超出 2^53 的 long 常量、模型字段的时间单位，目标端有 TS 的算式和数值常量时
  f280 源端 Float 相等比较和比值钳制（2）；f320 Java float 运算和截断（4）；f337 源端算式里的倍率和偏移项（2）；f353 两端模型同名数值字段的单位（1）；f366 超出 2^53 的 long 常量（1）
  f816 与源端或 Base 层同名的常量和哨兵值（2）；f831 调用实参里的字面数值（1）
业务逻辑与源码语义 / 字符串、字节与编解码（36 条）：源端有 BufferedReader.readLine、String.split / trim、android.util.Patterns、byte[] 字面量、substring 下标、proto 字段的 varint / fixed32，目标端有 split、TextDecoder、RegExp、Uint8Array 和手写的 codec 时
  f184 Java 读行和字符串处理的语义（7）；f264 手写 proto 编解码的标量读写方法（2）；f272 手写字节编解码里的有符号整数（3）；f312 源码里的字节数组字面量和切片下标（2）
  f323 android.util.Patterns 的平台正则（2）；f690 替代 ExifInterface 的手写 EXIF/TIFF 编解码（5）；f716 Uri、Base64、MIME 类型这类安卓工具方法的移植（1）
  f742 Kotlin / Java 字符串和正则函数的语义（4）；f745 Kotlin 字符串的转数和判空函数（2）；f760 源端的 URL 解析和链接截取（6）；f828 正则字面量里的 U+2028 / U+2029（1）
  f839 字符串常量里的控制字符转义（1）
音视频与媒体选取（101 条）：源端有 VideoView、MediaPlayer、ExoPlayer / PlayerView、SoundPool、MediaController、选图和选文件的 Intent，目标端有 Video、AVPlayer、SoundPool、XComponent、PhotoViewPicker、SaveButton 时
  f069 Video 的 src 里的本地文件地址（2）；f181 AVPlayer 的状态机和异步播控（5）；f220 音效和播放器的封装（6）；f277 系统选择器和相册保存控件（11）
  f283 Flutter 选图插件的兼容层（AssetPicker.pickAssets / AssetEntity）（4）；f319 播放器的播放、暂停和切集状态转移（3）；f335 播放器视图的尺寸和层级（2）
  f355 UI 侧播放控制器的取媒体和挂视频面（2）；f714 媒体库的查询和删除（photoAccessHelper.getAssets、MediaAssetChangeRequest.deleteAssets）（4）
  f727 MediaRecorder 录像迁成 AVRecorder 的配置、上限和错误（5）；f741 MediaRecorder 迁成 AVRecorder 的录制控制（4）；f762 跨卡片、跨退后台存活的播放器（2）
  f823 选图后上传并回填文本的链路（2）；f832 SAF 新建文档和 DocumentViewPicker 保存（1）；f837 相机的多帧拍照（连拍、HDR、包围曝光）（1）
音视频与媒体选取 / 相机、录像与录音（47 条）：源端有 Camera / Camera2 的 CameraDevice、预览和拍照会话、CaptureRequest / CaptureResult / CameraCharacteristics 的参数键、快门点击和长按连拍、MediaRecorder 录像、CamcorderProfile 选档、AudioRecord 采集，目标端有 cameraManager、CameraInput、PhotoSession / VideoSession、PhotoOutput.capture、VideoOutput、ManualExposure / ManualFocus / ManualIso、AVRecorder 或 AudioCapturer 时
  f700 相机的打开、关闭和重开（1）；f711 Camera2 手动参数迁到相机会话的单位和取值换算（5）；f756 MediaRecorder 的音源、封装格式和音频参数（4）；f757 录像的视频档、帧率和录像会话（3）
  f763 相机会话和录像输出的拆卸与释放（3）；f764 AudioRecord 录音采集的创建和启动（1）；f775 手动 ISO、曝光、捕获结果和录音振幅（3）
  f778 拍照调用和它的回调（takePicture、PhotoOutput.capture）（7）；f796 拍照 profile 的格式和取字节通路（photoProfiles、CameraFormat）（3）
  f802 Camera2 会话的输出配置和拍照数据（4）；f803 相机能力位、模式和可选值（7）；f809 相机打开回调里消费的一次性拍照请求（2）；f810 拉起相机前的能力预检和权限申请（1）
  f820 相机预览的 TextureView 和 XComponent（1）；f822 拍照和停录后的缩略图（2）
页面导航与标题栏（192 条）：源端有 startActivity / Intent、跳板 Activity 和透明主题的 Activity、Fragment 事务、Compose Navigation、onBackPressed、Activity 切换转场、Toolbar / ActionBar、DrawerLayout，目标端有 Navigation、NavDestination、NavPathStack、router.pushUrl、pageTransition、自绘标题栏时
  f055 点击入口跳到哪一页（14）；f056 跳转前后的附带动作（4）；f057 异步结果回来后的跳转和提示（6）；f061 开头即跳走的跳板 Activity（2）；f068 源 Activity 的切换转场（3）
  f103 Navigation 入口和首屏的挂载（7）；f104 NavPathStack 的路由名、出栈和返回刷新（11）；f136 根页的返回键（启动 Activity 没覆写 onBackPressed）（2）
  f157 Fragment 事务压栈打开的子页（6）；f233 Activity 的返回键处理（onBackPressed、OnBackPressedDispatcher）（4）
  f365 透明主题的 Activity（windowIsTranslucent）（1）；f705 Fragment 换页的自定义动画（1）；f842 宽窗的列表-详情分栏（1）
页面导航与标题栏 / 外部入口与深链（45 条）：源端有 intent-filter 深链、onNewIntent、PendingIntent、TaskStackBuilder，或交给外部应用的 ACTION_VIEW / ACTION_SEND / Settings Intent，目标端有 EntryAbility 的 onNewWant、want.uri、startAbility 的 Want、WantAgent、systemShare 时
  f058 拉起浏览器和系统设置的 Want（9）；f128 onNewIntent 与外部深链的再次拉起（4）；f169 Intent 发起的外部入口、通知动作和分享（8）
  f196 TaskStackBuilder 父栈和路由栈的恢复与再次拉起（4）；f274 深链的 intent-filter、navDeepLink 和 want.uri 解析（9）
  f752 ShortcutManager 固定的桌面快捷方式（1）；f758 响应拍照、录像意图时的结果回传（5）；f766 接收别的应用分享来的 ACTION_SEND（3）
  f781 指向应用自身的包名（getPackageName、APPLICATION_ID）（1）；f793 外部应用拉起时 Intent extras 里的协议键（1）
页面导航与标题栏 / 页面和组件的入参（24 条）：源端有 Intent 的 putExtra / get…Extra、Bundle、Fragment 的 setArguments / newInstance / navArgs，目标端有路由参数对象、NavDestination 取参、子组件的 @Param 时
  f054 Intent extra 迁成路由参数（12）；f113 源 Fragment 入参到目标页面和组件的传递（3）；f271 路由参数的有效性判定和错误态（2）；f733 打开设置子屏时经 Bundle 传的能力快照（2）
  f794 NavDestination 路由参数类的定义、导出和取用（5）
页面导航与标题栏 / 标题栏、抽屉与菜单（61 条）：源端有 Toolbar / ActionBar、onCreateOptionsMenu、setDisplayHomeAsUpEnabled、DrawerLayout、CollapsingToolbarLayout、Compose TopAppBar，目标端有自绘标题栏、NavDestination 的 title / menu、hideTitleBar 时
  f168 照源端 @Composable 复刻的标题行组件（2）；f180 DrawerLayout 抽屉和汉堡工具栏（7）；f183 CollapsingToolbarLayout 折叠头部（5）
  f201 工具栏的高度、标题字号和颜色（9）；f202 标题栏的返回箭头（4）；f203 自绘标题栏的顶部避让（8）；f234 平台 ActionBar 和选项菜单（12）
  f282 Compose 折叠顶栏（LargeTopAppBar 配 exitUntilCollapsedScrollBehavior）（3）；f341 编辑态切换的顶栏和底栏（1）；f695 菜单 XML 里的子菜单（1）
  f722 窗口 ActionBar 溢出菜单的面板（2）；f743 Compose 模态抽屉和 M3 底栏的自绘替代（2）；f791 ActionMode 多选上下文操作栏（CAB）（3）
  f811 Ionic 的 IonHeader / IonToolbar 顶部工具栏（2）
网络（42 条）：源端有 Retrofit 接口注解、OkHttp / OkGo 请求和拦截器、BaseResponse 响应壳、BuildConfig 里的服务地址，目标端有 @ohos.net.http 的封装、请求 url 和 header、响应解包时
  f053 Retrofit 接口注解声明的路径、方法和请求编码（3）；f072 响应壳 BaseResponse 和 Bean 的字段（3）；f079 Retrofit Response<> 带的响应头（2）
  f148 OkGo 请求通道和会话密钥握手门（2）；f161 服务地址、接口路径和默认环境（6）；f162 网络配置的注入和初始化时机（5）；f254 网络回调里信封成功和 data 层错误码的判别（2）
  f304 源端 OkHttp 拦截器和统一响应壳（5）；f313 预签名上传的诊断日志包（2）；f344 配置地址拼接运行期参数的链接（1）；f739 OkHttp 缓存迁成 rcp ResponseCache（3）
  f740 request.agent 的下载任务（1）；f759 源端 catch 里的 HTTP 失败和目标的失败信封（2）；f771 HTTP 非 2xx 响应的状态码和原因短语（3）
  f808 rcp 拦截器和 401 刷新链里的取值与日志（2）
占位、规格与测试（50 条）：派工、占位登记或代码注释里有 FWD-REF、PLACEHOLDER、P-ID 条目，规格的 AC、台账里的「平台无对等」，孤儿检测报 NO_IMPORTER，或单测、派工的要求和源端不同时
  f065 代码里的 FWD-REF 占位（11）；f067 源端没有的入口控件（2）；f078 规格 AC、状态接口和对接点要的行为（16）；f090 占位登记条目的兑现（9）；f281 带求交过滤的初始化分支的单测（2）
  f318 第三方 SDK 的占位登记（1）；f322 写着「等价于源端谓词」的占位（1）；f346 写成恒 false 的「平台无对等」能力和标志（4）；f347 指定为唯一尺寸来源的布局信息（1）
  f358 孤儿检测报 NO_IMPORTER 的页面和弹窗（1）；f362 比源端更严的 RED 测试契约（1）；f730 派工或壳注释点名要接通的控件（1）
状态与数据流（73 条）：源端有 ViewModel、LiveData / Flow、Compose remember / mutableStateOf、EventBus、data class copy，目标端有 @Local、@Param、@ObservedV2 / @Trace、@Monitor、AppStorageV2、@Builder 传参和页面的加载、空、错误状态时
状态与数据流 / 页面加载、空与错误状态（5 条）：源 Screen 用 hiltViewModel()、collectAsState() 由 ViewModel 和网络状态驱动，或 UiState、规格、决策台账分出 loading、failed、空态、不可用，目标页有加载、空、错误分支，或是模板空壳、写死的假数据时
  f224 由 ViewModel 和网络状态驱动的源页面（2）；f231 加载、失败、空态和不可用等页面状态（3）
状态与数据流 / 跨页面与跨组件的状态传递（29 条）：源端有多页共用的 ViewModel、EventBus 的 post / @Subscribe 和 setResult 回传、Activity 在 setContent 里下传的设置、共享页头、子 Composable 和子组件的状态参数，目标端有 AppStorageV2 / PersistenceV2.connect、@Param / @Event、@Builder 值参、事件 emit 和返回后刷新时
  f044 多参数 @Builder 的状态值参（5）；f099 EventBus 事件的订阅、发布和返回刷新（11）；f105 AppStorageV2 / PersistenceV2 的 connect 调用（4）
  f106 共享 ViewModel 拆成页面实例后的状态下传（4）；f330 共享页头传递的视觉字段（1）；f776 子组件内部创建的 ViewModel 和页面的注入点（1）
  f784 Activity 壳层经 setContent 下传的设置和派生结果（3）
状态与数据流 / Compose 状态迁 V2 与 @Trace 观察（19 条）：源端有 Compose remember / mutableStateOf / derivedStateOf、LaunchedEffect(key) 这类按键值重跑的副作用、data class copy 更新，目标端有 @Local、@Computed、@ObservedV2 / @Trace 模型和数组、@Watch / @Monitor、UIUtils.getTarget 时
  f080 data class 用 copy 更新的列表项和模型字段（5）；f107 页面读 @ObservedV2 模型的 @Trace 状态（7）；f114 Compose remember 状态迁成 V2 状态后的重置时机（4）
  f747 Compose 按键值变化才重跑的副作用（2）；f785 定时器里逐格计算的 @Trace 数组（1）
状态与数据流 / ViewModel 与数据层（20 条）：源端 ViewModel 用 LiveData / Flow 发布页面数据，数据来自 Repository、Room Dao、assets 文本、引擎或回调实现类，目标端有 VM、store、gateway 的字段从哪赋值、何时赋值、状态初值、addListener 订阅、写后刷新和给 UI 的门面接口时
  f062 ViewModel 发布的数据在目标端的来源和赋值时机（9）；f064 列表、选项和页面模型数据的来源（5）；f070 单例数据层的 addListener 订阅（2）；f703 只在事件分支里写的状态字段初值（1）
  f710 VM 到 UI 的门面接口（1）；f734 引擎持有的模式在界面上的镜像状态（1）；f768 Room LiveData 观察的表在目标存储里的刷新（1）
系统能力与设备（89 条）：源端有运行时权限、通知、WorkManager、地图和定位 SDK、NFC、蓝牙、网络状态、振动、OAID、Cipher 加解密、桌面小部件、登录授权 SDK、FlutterBoost，目标端有对应的 @ohos / @kit 接口、FormExtensionAbility 或三方 SDK 桥接时
  f275 源端 Cipher 加解密工具的空值和失败分支（5）；f276 cryptoFramework 的密钥规格串和加解密结果（3）；f291 Glance 桌面小部件迁成服务卡片（4）
  f314 FlutterBoost 宿主页的事件通道（1）；f357 Flutter 调原生的分发（pushNativeRoute、MethodChannel）（2）；f708 复制到剪贴板（ClipboardManager）（1）
  f736 桌面小部件迁成的 ArkTS 卡片（2）；f804 d.ts 里带 @throws 801 的接口变体（1）
系统能力与设备 / 登录、授权与三方 SDK（6 条）：源端按 token 判登录态，或调微信这类 SDK 授权、支付并在回调里按类型分流，目标端有登录态判断、授权回调的 state 校验和 SDK 回调处理时
  f159 单会话授权回调的 state 校验（2）；f252 按 token 判定的登录态（3）；f327 SDK 回调类型常量（1）
系统能力与设备 / 设备与连接（26 条）：源端有 NfcAdapter、MifareClassic、BluetoothAdapter、ConnectivityManager、Vibrator、OAID，目标端有 nfc、bluetooth、connection、vibrator、identifier 这类系统接口时
  f127 NFC 前台派发（enableForegroundDispatch）的开关时机（3）；f245 NfcAdapter 的可用性判断和贴卡入口（3）；f249 ConnectivityManager 的网络类型和计费判断（2）
  f250 蓝牙 A2DP、HFP 的连接状态（1）；f263 蓝牙开关、状态和扫描（8）；f290 OAID 设备标识的采集（3）；f309 Vibrator 振动和提示音（2）；f311 MIFARE Classic 标签接口（3）
  f788 系统省流量开关（Data Saver）和计费网络判定（1）
系统能力与设备 / 地图与定位（15 条）：源端有高德等地图 SDK 的 MapView、AMapLocationClient、POI 搜索和 SDK 初始化，目标端有地图组件或桥接、定位结果和占位的地图区时
  f112 高德 POI 搜索和定位接口的调用（4）；f138 源布局里的原生地图（MapView / AMapNaviView）（5）；f284 源端地图 SDK 的 MapView 和定位坐标（4）
  f296 高德 SDK 各产品单例的初始化（2）
系统能力与设备 / 通知与后台任务（13 条）：源端有 NotificationCompat.Builder、NotificationChannel、常驻通知、WorkManager / CoroutineWorker，目标端有 notificationManager.publish、NotificationRequest、SlotType 或后台计时时
  f001 WorkManager 后台计时 Worker（3）；f204 通知的正文和模板（4）；f205 常驻通知的发布者和生命周期（2）；f363 通知渠道和通知槽（NotificationChannel、SlotType）（1）
  f698 AlarmManager 定时提醒和它的 BroadcastReceiver（3）
系统能力与设备 / 权限（10 条）：源端申请定位、媒体、存储等运行时权限并有拒绝分支，目标端有 requestPermissionsFromUser、checkAccessTokenSync 和 module.json5 的权限声明时
  f129 定位权限（ACCESS_FINE / COARSE_LOCATION）的申请和判定（4）；f130 权限拒绝、服务关闭或无坐标时的失败分支（3）；f131 媒体与存储类权限的权限名和声明（2）
  f715 调用声明带 @permission 的接口时的权限声明和移交登记（1）
界面（987 条）：源端是布局 XML 里的 View 控件或 Compose 界面元素（文字、图片和自绘、布局容器、列表和翻页、弹窗和提示、点击和输入控件、动效、主题和颜色、窗口和系统栏、三方库的自定义 View），目标端是 ArkUI 组件和它的尺寸、样式、属性时
界面 / 动效（21 条）：源端有 Animator 和它的 setDuration、动效起点的锚点位置、Compose 的 animateItem / animateContentSize / AnimatedContent、AnimatedVectorDrawable、LottieAnimationView，目标端有 animateTo、.animation、.transition 或 lottie 时
  f017 动效起点的锚点窗口位置（3）；f075 Compose 的尺寸、内容切换和列表项动画（6）；f295 Compose 的 AnimatedVectorDrawable 动画图标（2）；f340 浮层出场动画的时长（1）
  f345 LottieAnimationView 动画层（1）；f706 显隐切换带的淡入淡出动画（1）；f801 共享元素转场的 geometryTransition（2）
  f814 Compose AnimatedVisibility 的显隐动画（3）；f818 ValueAnimator 改写成的自驱帧循环（2）
界面 / 弹窗与浮层（136 条）：源端有 AlertDialog、DialogFragment、BottomSheetDialog、PopupWindow、XPopup、Toast、Snackbar、上下文菜单，目标端有 openCustomDialog、CustomDialogController、bindSheet、bindPopup、Stack 里的遮罩浮层、showToast 时
  f115 半模态面板里再弹出的对话框的呈现层级（2）；f116 源对话框迁成哪种弹窗承载（13）；f117 复刻平台 AlertDialog 的外观（18）；f118 自绘弹窗的打开、关闭和触摸穿透（8）
  f120 弹窗组件和宿主之间的接线（4）；f121 可取消的 AlertDialog 的返回键和取消去向（3）；f150 安卓对话框改写成的页内弹层（7）；f198 V2 页面里的自定义弹窗（3）
  f228 Compose 的 Dialog、AlertDialog 迁成的弹窗形态（4）；f251 按接口返回数据条件弹出的弹窗（2）；f258 外部库模板按配置对象弹出的隐私协议弹窗（4）
  f720 对话框窗口层的遮罩、投影、圆角、宽度和位置（7）；f721 对话框库 Builder 建的对话框（material-dialogs）的形制和排版缺省（3）；f746 对话框接口的条目和回调参数（1）
界面 / 弹窗与浮层 / 菜单、气泡与下拉面板（24 条）：源端有 PopupWindow 的 showAsDropDown / showAtLocation、registerForContextMenu / onCreateContextMenu、AttachPopupView、Balloon 气泡，目标端有 bindPopup、bindMenu、openMenu 或锚定在控件上的浮层时
  f149 PopupWindow 弹出面板（showAsDropDown / showAtLocation）（5）；f195 锚定父页控件的 AttachPopupView 提示（3）
  f260 安卓上下文菜单（registerForContextMenu / onCreateContextMenu）（10）；f306 skydoves Balloon 气泡（2）
  f726 下拉菜单式的选择项（ListPreference 的 DROPDOWN_MENU、DropdownMenu）（1）；f815 Compose 的 DropdownMenu、Popup 和 cascade 菜单（3）
界面 / 弹窗与浮层 / 底部弹层与上拉面板（13 条）：源端有 BottomSheetDialog / BottomSheetDialogFragment、ModalBottomSheet、BottomSheetBehavior、SlidingUpPanelLayout，目标端有 bindSheet 和 SheetOptions，或 Stack 加 translate 写的面板时
  f119 bindSheet 的挂载点和 SheetOptions（4）；f122 当前页底部弹层的承载和层级（4）；f172 BottomSheetBehavior 底部面板（2）；f214 底部弹层的承载和关闭（2）
  f334 SlidingUpPanelLayout 上拉面板（1）
界面 / 弹窗与浮层 / 吐司与提示条（20 条）：源端有 Toast.makeText、Snackbar / SnackbarHost，目标端有 promptAction.showToast、统一的 ToastService 门面或自绘的提示条时
  f009 Toast 提示和结果反馈的形式（10）；f243 Compose 的 Snackbar 和 SnackbarHost（6）；f350 统一吐司门面（ToastService）（1）
  f732 吐司和 Snackbar 的显示位置（2）；f798 Crouton 提示条的调用和队列（1）
界面 / 图片和图形（135 条）：源端有 ImageView、@drawable 位图和 shape、自定义 View 的 onDraw / Canvas / Paint、elevation 阴影、模糊，目标端有 Image、Canvas、backgroundColor、linearGradient、border、shadow、blur 时
  f178 elevation 高程阴影（4）；f238 背景图的模糊变换和 LightingColorFilter 压暗（1）；f261 Compose Modifier.blur 的模糊（2）
界面 / 图片和图形 / 背景、渐变与描边（48 条）：源端有 android:background 引用的 drawable（shape、layer-list、gradient、selector）、CardView 圆角、Compose Brush 渐变或 drawWithContent，目标端有 backgroundColor、backgroundImage、linearGradient、border、borderRadius 时
  f012 组件自身 Drawable 背景的预览层（3）；f089 背景和进度条引用的 drawable 层（4）；f092 android:background 引用的背景图和状态背景（5）
  f093 没写背景或背景为 @null 的控件（5）；f141 Compose Brush 线性渐变（Brush.linearGradient / horizontalGradient）（6）
  f143 android:background 引用的 shape drawable 与 CardView 圆角（9）；f144 drawable 里的 <gradient> 渐变（窗口背景、ImageView 着色）（2）
  f222 按选择对象分图片、单色、渐变生成的背景（2）；f223 同一视图上的圆角加描边（1）；f229 Compose 用 drawWithContent 写的自定义 Modifier 扩展（2）
  f737 主题 ripple 和 selector 提供的按压反馈（5）；f770 Compose 的边缘渐隐（fadingEdges / fadingEdge）（4）
界面 / 图片和图形 / 位图、图标与快照（37 条）：源端有 ImageView / ImageButton 的 android:src、@drawable 位图、Compose Icons、当图标用的字符，或按内容总高导出长图，目标端有 Image 的宽高和 objectFit、SymbolGlyph、componentSnapshot 时
  f006 按内容总高导出的长图快照（2）；f018 没写固定尺寸的密度目录位图（6）；f019 固定承载区里的图标按钮（5）；f020 源布局引用的 @drawable 位图资源（7）
  f022 ImageView 的宽高比、夹紧和条目高（3）；f329 当图标用的字符和 SymbolGlyph 系统符号（3）；f364 Compose 内置的 Icons 矢量图标（2）
  f712 BitmapFactory 的解码选项（inSampleSize、inJustDecodeBounds）（1）；f728 位图的 tint 着色（android:tint、ColorFilter.tint）（1）
  f774 按素材固有比例定高的图片（ContentScale.FillWidth、无宽高约束的 img）（2）；f819 按 EXIF 方向旋转的位图（2）；f821 PixelMap 的所有者和释放（2）
  f840 图片加载库的占位图、错误图和淡入（1）
界面 / 图片和图形 / 自绘画布（43 条）：源端有自定义 View 或 SurfaceView 的 onDraw、Paint、Canvas.drawText / drawBitmap、invalidate、Typeface，目标端有 Canvas、CanvasRenderingContext2D、fillText、drawImage、帧循环时
  f002 自绘 View 里的文字度量和 drawText（7）；f003 自绘 View 的尺寸推导和画布单位（6）；f004 自绘 View 一次性准备的背景位图和颜色（3）；f005 自绘 View 改成组件组合（2）
  f007 View.invalidate 的重绘请求和帧调度（7）；f013 setBounds 拉伸的预烘焙位图和取整坐标（3）；f016 构造期解码和预缩放的位图（3）
  f182 自绘 Paint / Canvas 的绘制分支和坐标（3）；f225 Canvas 上用的注册字体（2）；f239 SurfaceView 自绘和它的渲染线程（4）
  f701 drawBitmap 加 Matrix 的位图绘制（1）；f702 onDraw 里向别的类查询的状态和位置（2）
界面 / 点击、输入与控件（141 条）：源端有 setOnClickListener、Compose clickable、EditText / TextField、CheckBox、Switch、SeekBar、ProgressBar、OnTouchListener、onKeyDown，目标端有 .onClick、TextInput、Checkbox、Toggle、Slider、Progress、.onTouch、手势、.onKeyEvent 时
界面 / 点击、输入与控件 / 点击（23 条）：源端有 android:onClick、setOnClickListener、数据绑定的 android:onClick="@{…}"、Compose Modifier.clickable，目标端有 .onClick、它挂在哪一层和点击前的门控时
  f037 点击动作前的确认弹窗和条件门控（3）；f038 onClick 回调的事件参数（1）；f066 源端的点击监听和目标的 .onClick（8）；f071 数据绑定布局里的点击绑定（4）
  f096 Compose 的 clickable / toggleable 点击修饰（6）；f824 写操作点击前的账号就绪守卫（1）
界面 / 点击、输入与控件 / 选择、开关与进度控件（38 条）：源端有 CheckBox、RadioButton、Switch、SeekBar、Compose Slider、按状态切图的 ImageButton、ProgressBar，目标端有 Checkbox、Radio、Toggle、Slider、Progress 和选中、加载状态时
  f049 选项的选中、取消选中和按选中决定的按钮可用（4）；f063 ImageButton 一类图标按钮和开关的状态切换与获焦（9）；f153 按偏好二选一的 Compose 进度组件（2）
  f158 CheckBox、RadioButton 和单选列表行（4）；f213 勾选控件和勾选状态（7）；f242 平台 SeekBar、Switch 控件迁 Slider、Toggle（5）
  f310 Compose 的 Slider（2）；f368 控制进度显示的加载状态（1）；f692 Compose 的不定进度条（1）；f748 按值表索引的 SeekBar 进度（2）
  f751 Compose 的 CircularProgressIndicator（1）
界面 / 点击、输入与控件 / 输入框与软键盘（56 条）：源端有 EditText、SearchView、Compose TextField、android:inputType / maxLength / textCursorDrawable、windowSoftInputMode，目标端有 TextInput、TextArea、Search、caretColor、inputFilter、获焦和键盘避让时
  f132 EditText 的光标（textCursorDrawable）（4）；f133 EditText 的背景与 TextInput 默认带出的外观（8）；f134 定长格子密码框（EditText 子类叠掩码格）（3）
  f135 EditText 的 maxLength 与程序写入（setText、TextWatcher）（3）；f163 EditText 的 inputType 和输入过滤（8）；f179 SearchView 迁成 Search（5）
  f207 软键盘避让模式（2）；f208 输入框的获焦和弹键盘（6）；f256 Compose 的输入框和开关控件（8）；f293 EditText 输入值的取用（2）；f336 TextInput 的获焦回调（1）
  f691 InputMethodManager 收起软键盘（2）；f704 EditText 的 imeOptions 和软键盘回车键（1）；f723 EditText.setError 的字段错误提示（1）
  f724 多行 EditText 的最小行数和高度（minLines）（1）；f725 setText 预填的输入框的光标位置（1）
界面 / 点击、输入与控件 / 触摸、手势与按键（24 条）：源端有 OnTouchListener / onTouchEvent、GestureDetector、跟手拖动、onKeyDown / dispatchKeyEvent，目标端有 .onTouch、PanGesture、parallelGesture、.onKeyEvent 时
  f215 安卓触摸回调迁成 onTouch（11）；f235 Activity 的按键回调（onKeyDown、onKeyUp）（8）；f288 绑了 PanGesture 的拖拽层（下拉关弹层、侧滑露按钮）（2）
  f765 拖拽柄上的 startDrag 和拖拽阴影（2）；f789 长按监听（setOnLongClickListener）和松手回调（1）
界面 / 布局与尺寸（174 条）：源端有布局 XML（LinearLayout、RelativeLayout、ConstraintLayout、FrameLayout、TableLayout，include / inflate 进来的布局、layout-land 等变体）、android:visibility，或 Compose 的 Row、Column、Box、自定义 Layout 和项目自己的 @Composable 组件，目标端有 Row、Column、Stack、共享 @Component 和 .width、.height、.margin、.padding、显隐条件时
  f021 源布局里的图文结构（8）；f034 源端控件的显隐：XML 初值和代码里的 setVisibility（15）；f035 共享组件和子页面的显隐入参（6）
  f085 资源限定符目录的覆盖（values-w / sw、layout-land）（5）；f102 换外层容器后留下的布局修饰（2）；f124 inflate / setContentView 加载的弹窗与页面布局（4）
  f191 项目自定义 Compose 组件和共享组件（7）；f255 Compose 自定义 Layout 的测量和摆放（3）；f332 TableLayout 的列宽（2）；f813 Compose FlowRow 的换行排列（1）
界面 / 布局与尺寸 / 线性排列与权重（22 条）：源端有 LinearLayout 的 gravity、layout_gravity、layout_weight、weightSum，或 Compose Row / Column 的 weight、verticalAlignment，目标端有 Row、Column 的 alignItems、justifyContent、layoutWeight 时
  f026 LinearLayout 的 gravity 和子项对齐（5）；f027 LinearLayout 的权重子项（layout_weight、weightSum）（4）；f028 横向行里 wrap_content 子项的宽度（2）
  f029 兄弟间距用的单侧外边距（2）；f166 Compose 行容器的高度和垂直对齐（3）；f175 Compose Row 子项的 weight、fillMaxWidth 和基线对齐（4）
  f718 Ionic 内容区的纵向排布（IonContent）（1）；f729 按 layout_weight 分高、带大内边距的 ImageView（1）
界面 / 布局与尺寸 / 宽高与边距（53 条）：源端有 layout_width / layout_height、match_parent、wrap_content、layout_margin*、padding*、dp 尺寸，或 Compose 的 padding、size、fillMaxSize、heightIn 修饰，目标端有 .width、.height、.margin、.padding、constraintSize 时
  f030 随内容高的父容器里的 height('100%')（3）；f031 wrap_content 行里 match_parent 高的子项（2）；f045 match_parent 子项转成 '100%' 的写法（4）
  f048 按钮和图片的显式宽高（2）；f051 布局 XML 上的外边距、内边距和尺寸（12）；f084 源布局写定的尺寸、字号和颜色（10）
  f126 Compose 的 fillMaxSize、heightIn、matchContentSize 尺寸修饰（5）；f142 Compose 未定尺寸的 Surface / Box 的尺寸与描边（2）
  f165 Compose 的 padding 和系统栏内距修饰符（7）；f167 M3 IconButton 的最小触控尺寸（1）；f331 dp 尺寸在目标端的单位（4）；f738 wrap_content 容器按子项定宽（1）
界面 / 布局与尺寸 / 叠层与相对定位（46 条）：源端有 FrameLayout、RelativeLayout、ConstraintLayout 的叠放和相对规则，或 Compose Box 的 contentAlignment、Modifier.align，目标端有 Stack、.align、.position、zIndex、hitTestBehavior 时
  f046 Stack 上层的点击命中（7）；f047 FrameLayout 里的头像与角标（3）；f050 RelativeLayout 子项的相对规则、贴边和叠放（12）
  f088 ConstraintLayout 子项的约束和锚点（7）；f140 Compose Box 叠放子项的对齐和定位（contentAlignment、Modifier.align）（6）
  f300 Stack 上叠加的覆盖层和全屏遮罩（7）；f713 按朝向在代码里重排的 RelativeLayout 子控件（2）；f797 布局里的 start / end 方向和 RTL 镜像（2）
界面 / 列表、滚动与翻页（132 条）：源端有 RecyclerView、ListView、ExpandableListView、Compose LazyColumn / LazyRow、ScrollView、ViewPager / TabLayout、PreferenceFragment，目标端有 List、ListItem、Grid、ForEach、LazyForEach、Repeat、Scroll、Swiper、Tabs、Refresh 时
  f036 列表适配器的条目绑定（12）；f040 列表条目和行内按钮的点击（3）；f097 LazyColumn 列表页的内容结构（3）；f164 工厂按 type 分派的编辑项列表（5）
  f170 RecyclerView 的列表和网格（7）；f176 条目里用图标画的勾选和评分（2）；f244 LazyColumn 的程序滚动和左右分类联动（4）；f246 列表区域的空数据分支（1）
  f257 ExpandableListView 的分组头（2）；f270 Compose SwipeToDismissBox 的列表行滑删（3）；f278 LazyColumn、LazyRow 和 RecyclerView 列表容器（3）
  f693 滚动中的可见比例判断（1）；f694 LazyColumn 的 stickyHeader 吸顶（2）；f812 瀑布流迁成 WaterFlow 的列宽和间距（1）
界面 / 列表、滚动与翻页 / 数据、键与刷新（28 条）：源端有 Adapter 的 setList / submitList / notifyItemChanged、removeAllViews 后逐项重建、SwipeRefreshLayout / SmartRefreshLayout、LazyForEach，目标端有 IDataSource、ForEach / Repeat 的键函数、Refresh、onReachEnd 时
  f039 列表数据源、条目的键和更新后的刷新（7）；f076 列表项的键和位置相关值（2）；f145 removeAllViews 后逐项 addView 重建的行（3）；f160 刷新时被重建的列表内容（3）
  f206 列表页的加载入口和刷新状态（4）；f253 LazyForEach 列表改写成 Repeat（2）；f262 下拉刷新和加载更多（6）；f786 ForEach 键函数和项里随语言、状态变的文案（1）
界面 / 列表、滚动与翻页 / 翻页与标签页（24 条）：源端有 ViewPager / ViewPager2、TabLayout 和它承载的子 Fragment，目标端有 Swiper、Tabs、TabContent、.tabBar、SwiperController 时
  f108 Swiper 的当前页和选中同步（8）；f109 逐页承载自绘视图的 Swiper 翻页（2）；f110 Swiper 禁止滑动和容器的触摸拦截（3）；f111 ViewPager / Tab 承载的子 Fragment 页（4）
  f369 TabContent 的 .tabBar 参数（1）；f717 Web Swiper 组件的分页点和导航箭头（5）；f836 原生 ViewPager 的定页和归位（1）
界面 / 列表、滚动与翻页 / 滚动容器（17 条）：源端有 ScrollView、NestedScrollView 和写在它外面的顶栏，目标端有 Scroll、它的内容 Column 的高度和 edgeEffect 时
  f023 滚动容器之外的顶栏和标题栏（1）；f024 Scroll 内容区的高度和纵向位置（8）；f025 ScrollView 的越界模式（1）；f769 Compose 滚动容器的滚动条和越界效果（5）
  f826 ScrollView 没写的滚动条外观和进页唤醒（2）
界面 / 列表、滚动与翻页 / 设置页与偏好项（14 条）：源端有 PreferenceFragment / PreferenceActivity、res/xml 里的 Preference、ListPreference、SwitchPreference，目标端有 List / ListItem 写的设置行时
  f248 平台主题下 ListView 和偏好界面的默认外观（8）；f273 框架 PreferenceFragment 的设置页（5）；f351 带 android:icon 的 Preference 行（1）
界面 / 文本与文案（106 条）：源端有 TextView、Compose Text / TextStyle、strings.xml、getString / stringResource、String.format、DecimalFormat、Html.fromHtml、Spannable、contentDescription，目标端有 Text、Span、$r('app.string.…')、fontSize、lineHeight、maxLines、accessibilityText 时
界面 / 文本与文案 / 界面文案与取串（30 条）：源端有 strings.xml、R.string / Res.string、android:text、getString / stringResource（带或不带格式参数）、i18next 的 t('…')、contentDescription，目标端有 Text('…') 字面量、$r('app.string.…')、resourceManager.getStringSync、模板串或拼接出的文案、.accessibilityText 时
  f073 组件上的 .accessibilityText（3）；f186 可见文案的逐字取值（9）；f187 带格式参数的文案（7）；f188 代码里经 resourceManager 取文案（8）
  f190 翻译键 t() 的文案和 FWD-REF 过渡（3）
界面 / 文本与文案 / 字号、字体与文字外观（16 条）：源端有 TextView / EditText 的 textSize、textColor、textAppearance、fontFamily、shadow*（或没写、由主题决定），由 dp 乘文字倍率算出的字号，或 Compose MaterialTheme.typography 的命名样式、FontWeight、FontFamily(Font(R.font…))，目标端有 Text / TextInput 的 fontSize、fontColor、fontWeight、fontFamily、textShadow、registerFont 时
  f011 dp 加文字倍率得出的字号（2）；f095 TextView / EditText 的文字外观（9）；f287 Compose 文本样式的字号、字重和字体族（5）
界面 / 文本与文案 / 行高、行数与省略（21 条）：源端有 TextView 的 android:lineHeight、includeFontPadding、maxLines / lines / ellipsize（或都没写）、可能为空的 wrap_content 文本，或 Compose TextStyle 的 lineHeight、Text 的 maxLines / overflow，目标端有 Text 的 .lineHeight、.lineSpacing、maxLines、minLines、textOverflow，或按一行高度算的容器高度和相邻元素定位时
  f177 文字控件的行数限制和省略（11）；f286 Compose TextStyle 的 lineHeight（6）；f709 可能为空的 wrap_content 文本的行高（1）；f817 TextView 没写行高时的行距（3）
界面 / 文本与文案 / 应用语言与区域（7 条）：源端有 AppCompatDelegate.setApplicationLocales / getApplicationLocales、supported_locales、Locale.getDisplayName、按设备语言主标签映射语言码、lowercase(Locale.ROOT) 或按 locale 的 toUpperCase / textAllCaps，目标端有 i18n.System.setAppPreferredLanguage、getSystemLanguage / getFirstPreferredLanguage、getConfigurationSync().locale、toLocaleUpperCase 时
  f015 大小写转换和区域标签（2）；f189 应用内切换语言与语言名（4）；f773 系统语言标签的解析和映射（1）
界面 / 文本与文案 / 富文本、链接与标记（12 条）：源端有 SpannableString.setSpan、ForegroundColorSpan、ClickableSpan / URLSpan、LinkMovementMethod、Linkify.addLinks、Html.fromHtml、Compose buildAnnotatedString / LinkAnnotation，或用 react-markdown 渲染 Markdown，目标端有 Span、RichEditor、TextController、Text 上的手势和自写的链接或标记解析时
  f236 带 LinkAnnotation 链接的 AnnotatedString 文本（4）；f279 Html.fromHtml 生成的文字内容（2）；f316 Spannable 分段着色的文字（2）
  f744 Linkify 自动链接的识别和切分（2）；f790 TextView 里按触点命中的链接 span（ClickableSpan、LinkMovementMethod）（1）
  f833 Markdown 渲染和自写的行内标记解析（1）
界面 / 文本与文案 / 数字、日期与数据值的显示格式（20 条）：源端在显示前用 String.format、NumberFormat / DecimalFormat、getCurrencyInstance、Formatter.formatShortFileSize、DateFormat、PrettyTime、DateUtils.formatDateTime，或用 when / switch 穷举表、转换函数把数据值转成显示文本，目标端有 intl.NumberFormat / DateTimeFormat / RelativeTimeFormat、toFixed、toLocaleString、toString()、自写的格式化和分档函数时
  f008 数据值转显示文本的转换和格式化（6）；f014 平台格式化器的数字、金额、日期格式化（12）；f783 PrettyTime、DateUtils.formatDateTime 一类的相对时间和日期显示（2）
界面 / 主题、颜色与样式（68 条）：源端有主题和 style、?attr 颜色、@color 资源、Material 控件的默认外观、Compose MaterialTheme / colorScheme / contentColor、深浅色切换，目标端有 $r('app.color.…') 等资源引用、fontColor、backgroundColor、setColorMode 时
  f074 引用主题属性 ?attr 的颜色（9）；f077 源控件没写的外观属性（主题的默认控件样式）（11）；f151 Compose 主题的深浅色和动态配色状态（4）；f152 组件里读取的 Compose 主题色（9）
  f194 随状态或容器变化的颜色（2）；f200 Material 控件没写外观属性时的默认外观（8）；f217 颜色资源引用和源端色值（7）；f269 应用内切换主题和深色模式（3）；f302 Compose 没写颜色的文本和图标（5）
  f317 组件属性里的 $r 资源引用（3）；f333 控件经 style 继承的圆角和形状值（1）；f750 M3 色板和排版令牌的构造（1）；f782 getColorSync 取到的 ARGB 颜色的拆分和插值（2）
  f799 三方 UI 库控件的尺寸和动画取值（1）；f830 Ionic 组件的默认样式和子项顺序（1）；f834 Compose Material 的 Badge 角标（1）
界面 / 三方界面库（2 条）：源端界面由三方库渲染：Activity 继承库的基类（如 AppIntro2）、布局里是库的自定义 View 节点（如 ColorPicker）、用库的 PagerAdapter / ViewPager 子类填页，目标端要照库里的尺寸、动画和手势写 ArkUI 时
  f829 三方库渲染的页面和控件（2）
界面 / 窗口与系统栏（72 条）：源端有 Activity 的窗口标志、主题的全屏和系统栏颜色、fitsSystemWindows、WindowInsets、DisplayMetrics、屏幕方向、常亮、画中画和亮度，目标端有 window 的 setWindowLayoutFullScreen、setWindowSystemBarProperties、getWindowAvoidArea、expandSafeArea 时
  f098 Activity 的全屏和无标题窗口标志（4）；f174 入口窗口的全屏方式和系统栏颜色（6）；f185 DisplayMetrics 屏幕宽高参与的几何（1）；f226 Activity 的屏幕方向声明与运行时切换（2）
  f289 窗口常亮和画中画（FLAG_KEEP_SCREEN_ON、PictureInPicture）（4）；f308 状态栏图标深浅和系统栏内容色（4）；f339 窗口亮度的读取和手势调节（2）；f755 设窗口级属性时拿的窗口对象（1）
界面 / 窗口与系统栏 / 安全区与避让（48 条）：源端有 fitsSystemWindows、透明状态栏下的留白、WindowInsets、Compose Scaffold 的 innerPadding、ImmersionBar，目标端有 getWindowAvoidArea 取值，或页面、Tabs 宿主、贴底元素上的避让 padding 和 expandSafeArea 时
  f086 全屏页的顶部状态栏避让（9）；f087 全屏页贴底元素的导航条避让（2）；f125 Compose Scaffold 外壳和内容区的顶部避让（7）；f171 包住 Tabs 的宿主容器上的内边距（6）
  f192 窗口避让区的取值和换算（7）；f212 透明状态栏下的顶部留白和背景（2）；f247 底部避让 padding 所在的容器层（3）；f285 DecorView 上的状态栏底色和顶部避让（2）
  f297 全屏沉浸页的避让 padding（10）
网页（12 条）：源端有 WebView、WebViewClient、WebSettings、loadDataWithBaseURL，目标端有 Web 组件、WebviewController、onLoadIntercept、onErrorReceive 时
  f032 wrap_content 的 WebView（2）；f033 WebView 的链接拦截和单页 H5 状态（2）；f041 loadDataWithBaseURL 程序装载的正文（2）
  f042 WebViewClient 的拦截和出错回调（2）；f043 单页 H5 外面的原生返回和标题栏（1）；f301 源 WebView 的 WebSettings 设置（3）
