规格：227 个族，561 条规矩。用短号取族（如 recall.py show f001）。

验收条目与验收判定（14 条）：规格里有验收条目（AC）和它挂的源码真值、UT 设计，或交回的验收报告、回归诊断给出 PASS、「两端一致」这类判定时
  f591 对话框列出预置项时的列表范围和过滤条件（1）；f635 RDB 共享写入口的验收判定方式（1）；f638 只有静态证据的选图功能验收（1）；f640 回归诊断里「两端 1:1、服务端问题」的结论（1）
  f646 AC 标的源码真值区间和赋值组（1）；f648 新 UI 入口的视觉要素（1）；f649 迁移算法的 UT 区分用例（1）；f666 上游说有而源布局里没有的组件（1）
  f688 源码里的断点和阈值比较（width > N.dp）（2）；f848 AC 要照抄的源端条件和已批准的怪癖（2）；f859 参考文档、派工意图与 AC 对源端行为说法相反（2）
标题栏、菜单与抽屉（18 条）：读到源端有菜单 XML（showAsAction）、上下文菜单、ActionBar / Toolbar / TopAppBar、DrawerLayout + NavigationView，规格里写标题栏、Up 箭头、溢出菜单、折叠顶栏和抽屉时
  f583 菜单项的 android:showAsAction 和溢出菜单（5）；f599 DrawerLayout + NavigationView 抽屉页（3）；f607 带窗口 ActionBar 的页面的 Up 箭头（2）
  f642 exitUntilCollapsed 折叠大标题顶栏（2）；f678 上下文菜单（registerForContextMenu、openContextMenu）（1）
  f856 Compose ModalNavigationDrawer 模态抽屉（2）；f864 Compose 的下拉菜单和级联菜单（2）；f880 工具栏里的 SearchView 和 ActionBarDrawerToggle（1）
本地数据与偏好（34 条）：读到源端的数据库、JSON 解析、assets 预置数据、外部存储，或偏好 XML、SharedPreferences / DataStore，规格里写数据表、存储、设置页和偏好键时
  f876 带 String 重载或 Parcel 字符串写法的数值字段（1）
本地数据与偏好 / 设置页与偏好存储（17 条）：读到 addPreferencesFromResource 加载的偏好 XML（Preference、SwitchPreference、ListPreference、EditTextPreference）、SharedPreferences / DataStore 的键和默认值、偏好标记控制的一次性引导，规格里写设置页、偏好表和首次进入行为时
  f550 偏好 XML 里平台偏好项的默认外观和对话框（8）；f551 偏好 XML 的 android:defaultValue（1）；f554 SharedPreferences / DataStore 的偏好键和默认值（6）
  f687 偏好标记控制的一次性引导（1）；f890 onPreferenceChange 回调里的联动流程（1）
本地数据与偏好 / 数据库、JSON 与文件（16 条）：读到 SQLiteOpenHelper、Room @Entity、org.json、assets/ 下的预置 JSON 或 DB、种子数据类、外部存储公共目录和 MediaStore，规格里写数据表、逐列清单、建库时机、解析和下载导出时
  f576 源工程 assets/ 下的预置数据（2）；f577 源码用 org.json 读写 JSON（4）；f596 SQLiteOpenHelper 子类的建库时机（1）；f627 源工程种子类构造的固定演示数据（1）
  f631 源端读写外部存储公共目录和 MediaStore 媒体库（5）；f644 Room 实体的列清单（1）；f887 数据模型里的多值枚举列（1）
  f894 Room 数据库的文件名（databaseBuilder 的 name）（1）
弹窗与提示（26 条）：读到源端弹 AlertDialog、Dialog、经工具类或 Helper 弹的弹窗、BottomSheetDialogFragment / ModalBottomSheet、BottomSheetBehavior 面板或 Toast，规格里写弹窗清单、底部面板和提示时
  f518 AlertDialog.Builder 弹出的系统对话框（12）；f544 经工具方法弹出的对话框（1）；f564 源码里给用户的 Toast 和通知提示（3）；f614 页面上弹出、布局不在页面 XML 里的弹窗和底部面板（4）
  f617 底部弹层的展开高度（ModalBottomSheet、BottomSheetDialogFragment）（2）；f684 CoordinatorLayout 里带 BottomSheetBehavior 的常驻面板（1）
  f843 由主题或库决定的对话框窗口外观（3）
图形与自绘（29 条）：读到源端有自定义 View 的 onDraw / Paint / SurfaceView、Compose 绘制修饰符、@drawable 引用的外观、共享组件里的形状或动画，规格里写画布、图片、阴影描边和动画时
图形与自绘 / 自绘与画布（17 条）：读到自定义 View 的 onDraw、onSizeChanged、Paint（setTextSize、measureText、getTextBounds、setTypeface）、SurfaceView 渲染线程，或 Compose drawWithContent 里的 blendMode，规格里写画布单位、文字度量、字体和重绘时
  f541 自绘 View 的单位、尺寸分支和位图缩放（5）；f542 自绘 View 的状态读取和重绘时机（2）；f568 自绘 View 用 Paint 取的文字度量（3）；f571 SurfaceView 自有渲染线程的帧循环（3）
  f579 Typeface.createFromAsset 装的自定义字体用在画布上（2）；f601 依赖画布已有内容的混合模式（blendMode）（2）
图形与自绘 / 图片、形状与动画（12 条）：读到布局里 @drawable 的 background / progressDrawable、容器背景加 ImageView 图标、Compose 的 Modifier.shadow / border、共享组件里的 shape，或 AnimatedImageVector、Animator 动画，规格里写图片资源、形状、阴影描边和动画时
  f539 容器背景加嵌套 ImageView 的元素（1）；f582 共享组件定义里自带的形状和裁剪（1）；f604 Compose 只绘制的修饰符（Modifier.shadow、Modifier.border）的映射（2）
  f606 布局里 @drawable 引用的控件外观（progressDrawable、background）（1）；f630 源端动画（AnimatedImageVector 形变、多组 Animator 分支）（4）
  f862 Coil 全局 ImageLoader 的图片管线（1）；f886 Compose 用的 Material Icons 具名图标（1）；f892 位图上的着色（ColorFilter.tint、setColorFilter）（1）
布局与尺寸（15 条）：读到源布局的 LinearLayout、ConstraintLayout、NestedScrollView、TableLayout、代码里循环 addView 搭的视图，或 Compose 的 Column、Modifier 链、自定义 Layout，规格里写容器映射、对齐、权重和尺寸时
  f515 Compose 修饰符链里的内距、背景和尺寸（5）；f562 Compose 自定义 Layout 在 constraints 上的 Int 整除（2）；f590 排在固定高度兄弟之后的填满内容区（1）
  f625 源布局容器（NestedScrollView、LinearLayout）的滚动范围和默认对齐（2）；f670 源布局容器里子项的宽度分配（权重、表格列宽）（2）；f671 代码里循环 new 再 addView 搭出的视图（2）
  f683 ConstraintLayout 里四向锚 parent 的单视图和挂在它下面的兄弟（1）
生命周期与配置重建（24 条）：读到 Activity 的 onCreate、onResume、onPause、onSaveInstanceState、getLastNonConfigurationInstance、configChanges，Compose DisposableEffect、LifecycleEventObserver，或 Application 初始化链，规格里写生命周期映射、存档和刷新时机、配置变化重建时
  f520 Activity 的 configChanges 和配置变化重建（7）；f566 源端挂在生命周期回调上的释放和移交（5）；f594 Activity 的 NonConfigurationInstance 续存分支（2）
  f595 Application 初始化链里注册的 BroadcastReceiver（1）；f609 源 Activity 的存档触发回调（1）；f680 源 Activity 和业务基类生命周期回调里的刷新和副作用（2）
  f850 System.exit 一类的应用「重启」（3）；f870 相机打开回调里读的一次性入口标志（1）；f882 onCreate 里同步语句和组合、挂载的先后（2）
列表、网格与翻页（18 条）：读到源端有 ListView、GridView、RecyclerView / GridLayoutManager、LazyColumn / LazyRow、SmartRefreshLayout、ViewPager2 或 ActionMode 多选，规格里写列表、网格、刷新分页和翻页时
  f516 共享基类里的 ActionMode 多选（3）；f538 GridView / ListView 的滚动和按压态（2）；f589 Compose 惰性列表（LazyColumn / LazyRow）区块（4）
  f641 SmartRefreshLayout 下拉刷新和加载更多的互斥（1）；f658 多列容器里的 no-op 广告位（1）；f668 侧栏分类页的内容区（1）
  f685 ViewPager2 加 FragmentStateAdapter 的实际页数（1）；f860 Compose PullToRefreshBox 下拉刷新（2）；f873 按 position 从当前数据表取行的列表点击回调（1）
  f883 源码自定义的触底加载 helper（1）；f889 ViewPager 翻页的释放定页和归位动画（1）
源码逻辑与数值（46 条）：读到源码里决定结果的分支、异常、集合遍历、float 运算、常量、格式化、日期时间和线程调用，规格的 AC、映射行或源码笔记要按它写出确切行为时
  f866 源端的字符串切分、正则和解码调用（3）；f869 源端取设备语言和语言映射的逻辑（2）；f878 源码交给依赖库算出的结果（RRULE 序列化、相对时间、URL 解析）（4）
源码逻辑与数值 / 分支、异常与集合（12 条）：读到 catch 后返回、提前 return、零分母和钳制保护、HashSet / HashMap 遍历、由不同调用点传入的一组常量、克隆的命名和内容、没捕获的异常退出，规格的 AC 或映射表写这些分支和顺序时
  f565 源码里 catch 异常和提前 return 的边界分支（5）；f592 源端辅助方法里的边界保护（零分母、钳制、空集合）（1）；f612 由不同调用点传入的一组来源常量（2）
  f622 HashSet / HashMap 遍历决定的输出顺序（1）；f623 克隆操作的名称变换和内容来源（1）；f661 照源保留的崩溃退出（1）；f874 接口实现类覆写的一组 on* 回调（1）
源码逻辑与数值 / 线程与调用顺序（9 条）：读到新开 Thread 后 Handler.post / runOnUiThread、单线程执行器、sleep 重连循环或前后依赖的同步调用，规格里写竞态、异步形态和串行要求时
  f545 后台线程回投 UI 和单线程执行器（6）；f626 源端同步执行的调用序列和阻塞循环（3）
源码逻辑与数值 / 数值、常量与日期时间（16 条）：读到 (float) 强转后 (int) 截断、byte[] 协议常量、DecimalFormat / NumberFormat / String.format、SimpleDateFormat / Calendar、System.nanoTime，规格里写公式、常量表、格式化精度、时区和计时 API 时
  f563 源码里的定长 byte[] 协议常量（2）；f575 随默认时区和区域变化的日期时间调用（5）；f621 Java 源表达式里的 float 运算和 (int) 截断（2）；f652 联动字段的格式化精度（1）
  f656 数值格式化的舍入模式和区域（3）；f667 计时 API 的映射（1）；f863 引用别处 const val 符号的默认值（1）；f865 直接写在平台或传感器 API 实参里的字面参数（1）
页面导航与入口（57 条）：读到源端的 startActivity / Intent、finish、返回键、Compose NavHost、FragmentTransaction、导航图，或 LAUNCHER、闪屏、深链 intent-filter，规格里写导航表、返回落点、启动路由和外部入口时
页面导航与入口 / 启动与外部入口（21 条）：读到 AndroidManifest 里的 LAUNCHER、深链 intent-filter、navDeepLink，闪屏或跳板 Activity、入口 onCreate 的启动分支，或桌面小组件等系统表面，规格里写冷启动路由、再次拉起、深链和外部入口时
  f525 清单里的深链 intent-filter（5）；f534 LAUNCHER 跳板和再次拉起（4）；f540 桌面小组件等系统表面的应用内替代页（1）；f553 启动判定里的登录态和首启分支（3）
  f558 入口 onCreate 里 super.onCreate 之前的调用（1）；f615 由常量拼出的深链和分享链接 URI（1）；f846 清单 intent-filter 声明的外部动作和分享接收（3）
  f847 外部入口的实例形态和分发时机（3）
页面导航与入口 / 页面跳转与返回（36 条）：读到 startActivity / putExtra、finish、onBackPressed、TaskStackBuilder、overridePendingTransition、Compose NavHost / navigate、导航图 <argument>、Fragment 挂进宿主容器，规格里写页面导航表、入参、返回栈、转场和页面清单时
  f526 点击监听器里的跳转目标（6）；f527 跳转目标页和页面清单（3）；f529 TaskStackBuilder 父栈和回收后的任务栈（3）；f530 调用方传了、接收方不读的 Intent 参数（1）
  f532 成功后 startActivity 加 finish 的组合跳转（2）；f533 根 Activity 没覆写的返回键（3）；f555 Activity 跳转的转场动画（4）
  f567 源端 Compose Navigation 的 NavHost 和导航调用（7）；f578 挂在宿主 Activity 里的 Fragment 子组件（4）；f662 导航目的地的 argument 声明（1）
  f881 Compose 的共享元素转场（sharedElement、sharedBounds）（1）；f888 页面之间回传结果的通道（savedStateHandle 回传）（1）
网络接口与同步（25 条）：读到 Retrofit Service、OkHttp 拦截器、Gson 和 Bean 模型、按异常类型分的网络失败、响应解密钩子，或待推送队列和同步任务，规格里写 API 表、请求头、错误码表、响应契约、测试环境和同步顺序时
  f548 Service 接口的参数类型和请求体（3）；f549 同步队列的选取条件和失败项（2）；f552 OkHttp 拦截器里的请求头和鉴权失效（4）；f608 接口字段表里 id 的线上类型和数值量级（1）
  f629 「未提供测试 base_url / 测试账号」的适用范围（1）；f650 按异常类型分类的网络失败（1）；f653 解密失败时回退原文的响应钩子（1）；f660 源端同步序列的步骤（2）；f665 同步任务的并发调度（1）
  f682 Gson 反序列化改写成显式 decoder 的契约（1）；f849 三方 SDK 里定义的接口、字段和参数（5）；f871 三方 SDK 自建的 HTTP 客户端（超时、重试、异常映射）（2）
  f877 SDK 按服务端版本分的路由表（1）
平台差异决策与偏离（24 条）：规格或决策台账里写了「无对等」「降级」「不迁移」「PD」「显式差异」「用户例外」这类平台差异决策和偏离，或写它们的依据栏时
  f598 决策台账里对系统能力写的「平台无对等」和降级条目（7）；f602 决策台账里 PD 条目的依据、批准状态和缺陷表（7）；f613 spec gap 里安卓固定行为与规格验收的冲突（1）
  f632 差异决策里当作查证依据的经验提醒（1）；f674 联调时与源端声明不一致的用户描述（1）；f676 决策台账里的大字体（随系统字号缩放）条目（1）；f677 被记成降级的界面视觉效果（自绘组件、输入框富文本）（4）
  f679 转述平台差异决策时超出它列明的范围（2）
资源与应用配置（31 条）：读到 res 下的 values-* / layout-* 限定词目录、按名引用的颜色和尺寸资源、AndroidManifest 的 application / activity 声明和 supportsRtl、BuildConfig 开关和多套 base URL，或目标 app.json5 的身份，规格里写资源表、配置值和身份项时
  f519 Manifest 里 application 和 activity 的声明（9）；f521 supportsRtl 声明和 RTL 语言资源（5）；f522 横屏限定词的布局和资源变体（4）
  f523 按资源名引用的颜色和尺寸资源（2）；f524 res 下的 values-* 语言和屏宽目录（4）；f637 构建配置决定的实现和接口环境（BuildConfig 开关、多套 base URL）（5）
  f663 脚手架身份的 bundleName（1）；f852 layout-* 限定符目录里的同名布局变体（1）
迁移范围与功能归属（15 条）：规格里写迁移范围、功能归属（page_id ownership、归某 feature）、功能入口页、跨页面共享组件、别的规格留给本文档承接的条目，或引用上游清单和台账（api-inventory、skip-list）时
  f586 功能入口页上的红点、数量和角标（2）；f597 别的规格或契约里定义、留给本文档承接的条目（3）；f611 源端入口委托的跨页面共享组件（1）
  f636 规格引用的上游清单和台账条目（api-inventory、接口清单、skip-list）（3）；f681 源端行为、页面和接口归到哪个 feature（6）
源码证据与页面元数据（23 条）：交回的 meta.json、基线快照或源码理解笔记里有页面元数据、合成的快照，或写了没读到定义的谓词、空子模块里的实现、声明没保证的回调顺序、实现建议的出处这类不确定项时
  f543 页面的源码布局和合成的 meta.json（3）；f581 没有真机 dump、由源码合成的基线快照（2）；f639 只读到调用、没读到定义的辅助谓词（1）；f647 实现建议里的去重和上限属性（1）
  f654 声明没写先后的平台回调（2）；f655 未检出子模块里的关键实现（1）；f845 仓库里没有源码的三方库（二进制依赖）（11）；f855 规格里标「[推断]」写入的平台行为（1）；f891 被当作先例照抄的同批生成代码（1）
页面状态与数据流（12 条）：读到 ViewModel、LiveData / StateFlow、remember、data class copy、Activity 实例字段和 static 字段，规格里写状态契约、状态接口表（@Local）、复位和数据流时
  f546 ViewModel 里请求前补齐和列表组装的步骤（3）；f547 ViewModel 的状态字段和格式化字段（2）；f557 Activity 实例字段和 static 字段的作用域（2）
  f619 remember 持有、由焦点等框架事件驱动的页面状态（1）；f624 整体替换的列表和订阅队列（copy、StateFlow.update）（1）；f664 每局重开的复位 AC（1）
  f686 状态接口表里与通用属性同名的成员（1）；f875 §状态管理里新拟的 AppStorageV2 / PersistenceV2 键名（1）
系统能力、设备与三方 SDK（47 条）：读到源端用蓝牙、NFC、定位、剪贴板等系统服务，WorkManager、前台 Service、常驻通知，MediaPlayer / SoundPool，分享面板，或厂商 SDK、Flutter 插件，规格里写这些能力的映射、权限和降级时
  f531 分享面板的渠道清单（1）；f560 源端直接开关蓝牙的 BluetoothAdapter.enable / disable（2）；f570 源端 WorkManager Worker 的后台计时和进度通知（5）
  f573 源端 MediaPlayer / SoundPool 播 res/raw 音频（3）；f574 NFC 贴卡的系统派发入口和前台派发（2）；f587 Flutter 插件的 MethodChannel 契约和 OHOS 选层（4）
  f605 源端能力探测的分支和不支持、外跳路径（3）；f616 安卓免权限的系统服务映射后的权限契约（2）；f620 源端自建的应用内分享渠道面板（2）；f634 被归为「三方无等价」的厂商或三方 SDK 能力（3）
  f657 定位 SDK 结果里附带的地址（1）；f659 前台服务的承载类（1）；f675 Fragment 里常驻的设备监听和它发的常驻通知（1）；f851 交给外部应用的隐式 Intent 和可用性回退（2）
  f857 MediaRecorder 录制器映射成 AVRecorder（3）；f858 MediaPlayer / ExoPlayer 播放器映射成 AVPlayer（3）
  f861 androidx ExifInterface 读写 EXIF（1）；f868 交给别的应用读的 content URI（FileProvider、ACTION_SEND）（2）
  f879 AlarmManager 精确闹钟和它到点发的通知（1）；f884 源端 Camera2 相机的能力位、手动参数和采集回调（5）
主题、颜色与默认外观（46 条）：读到 styles.xml / themes.xml 的主题继承（AppCompat、MaterialComponents、Material3、android:Theme.*）、?attr/ 主题属性、Color.* 常量，或源控件没写颜色和外观属性，规格里写主题色、控件默认外观和颜色映射时
  f517 TextView 和 Button 没写的外观属性（5）；f535 AppCompat / MaterialComponents 主题的语义色（5）；f536 平台主题 android:Theme.* 提供的控件外观（6）
  f559 Material3 组件的库默认外观（6）；f584 没写样式、外观由平台主题提供的控件（6）；f588 继承按钮、只换背景的自定义控件（4）
  f610 由主题决定的颜色（?attr/ 引用、android:theme 覆盖、状态栏图标明暗）（5）；f672 代码里的框架颜色常量（Color.GREEN、Color.RED）（1）
  f853 values-vNN 下另有同名定义的应用主题（4）；f854 根部 MaterialTheme 注入的全局主题（1）；f872 Ionic 应用的主题变量和全局 mode（2）
  f885 外观全来自第三方 UI 库默认样式的组件（1）
文本、控件与触摸（33 条）：读到源端有 TextView、EditText、Slider、WebView 等控件或 Compose Text / TextStyle，onTouch、GestureDetector、SwipeToDismissBox 触摸处理，contentDescription 等无障碍语义，规格里写文本样式、输入约束、控件状态和手势时
  f528 源码里控件的状态切换和展示加工（4）；f569 Compose Text 和 TextStyle 的文字样式（4）；f593 Compose material3 Slider 的刻度和默认外观（3）
  f600 安卓触摸监听（onTouch、GestureDetector）的触控契约（6）；f618 WebView 的 WebSettings 配置和导航回调（1）
  f628 EditText 的 inputType、InputFilter 和分段着色（4）；f633 SwipeToDismissBox 的滑删方向（1）；f643 多行正文的末行省略（maxLines + Ellipsis）（1）
  f669 源界面 Text 里的 emoji 字面文本（1）；f673 源组件的无障碍语义（contentDescription、role、合并朗读）（2）
  f844 源控件靠框架默认的行为（setError、预填光标、imeOptions）（3）；f867 源端 onKeyDown 的按键分发和遥控导航（2）；f893 整套迁移的 Markdown 渲染库（Markwon 插件链）（1）
窗口与系统栏（24 条）：读到源端有状态栏、导航栏、全屏和沉浸的写法（FLAG_FULLSCREEN、NoTitleBar 主题、WindowInsets、fitsSystemWindows、ImmersionBar、windowBackground、FLAG_KEEP_SCREEN_ON），或规格里写沉浸式、安全区避让、系统栏颜色和窗口背景时
  f514 Scaffold 的 innerPadding 和顶部安全区（2）；f537 布局根没写背景时透出的窗口背景（5）；f556 Activity 窗口的 FLAG_KEEP_SCREEN_ON（2）
  f561 根视图按状态栏 insets 设顶部 padding（2）；f572 低 targetSdk 全屏窗口下以 DisplayMetrics 为基准的几何（2）；f580 源 Activity 的去标题和全屏窗口标志（3）
  f585 嵌入页里的 ImmersionBar 沉浸调用（2）；f603 窗口沉浸和系统栏外观（4）；f645 只在某一导航模式下出现的底部遮挡（1）；f651 靠隐藏系统资源判断的源端分支（1）
