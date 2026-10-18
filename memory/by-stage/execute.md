# 阶段：执行与实现（execute）

本阶段可用的 513 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/capability/degradation](../topics/app/capability/degradation/index.md) — 能力确实不可用时只降级做不到的一步，运行期显式提示

- [决策批准的平台能力要真实现，只在运行期按结果降级](../topics/app/capability/degradation/lesson-efb94f2d70d4df1c65d7.lesson.md) · 信号：backgroundTaskManager.startBackgroundRunning, ohos.permission.KEEP_BACKGROUND_RUNNING, notificationManager.requestEnableNotification, WantAgent
- [后台计时降级只砍执行载体，保留逐拍刷新与回前台补算](../topics/app/capability/degradation/lesson-30643cd3f209b896ffd1.lesson.md) · 信号：WorkManager, elapsedRealtime, PendingIntent.getBroadcast, backgroundTaskManager.requestSuspendDelay
- [平台差异只收敛做不到的一步，其余出口照源保留](../topics/app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md) · 信号：HARD-DIV, startAbility, viewData, market://
- [应用内计时替代后台 Worker 时恢复入口共用扣减函数](../topics/app/capability/degradation/lesson-35a684862ee500f08912.lesson.md) · 信号：WorkManager, backgroundTaskManager, keepScreenOn, WakeLock
- [激励广告不可用时显式提示并按台账放行，不伪造奖励](../topics/app/capability/degradation/lesson-0f67121af7969203b76b.lesson.md) · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward

### [app/capability/launch](../topics/app/capability/launch/index.md) — 拉起外部应用、系统设置与分享：Want 预检与目标核对

- [应用内分享面板复用应用内弹层并逐渠道映射](../topics/app/capability/launch/lesson-b366cf7ae68525577f57.lesson.md) · 信号：ShareUtil, ShareItem, shareItems, platformName
- [打开系统设置的显式 Want 包名需在目标设备核对](../topics/app/capability/launch/lesson-4bea916d1ff67e51d455.lesson.md) · 信号：startAbility, bundleName, abilityName, com.huawei.hmos.settings
- [隐式 Want 先 canOpenLink 预检，不靠抛错](../topics/app/capability/launch/lesson-948d876672049969b865.lesson.md) · 信号：bundleManager.canOpenLink, querySchemes, 17700056, startAbility

### [app/capability/sdk-lookup](../topics/app/capability/sdk-lookup/index.md) — 判定无等价前先查 Kit、ohpm、SDK 声明与权限注解

- [三方算法库输出以库真值字面为契约，不自研子集](../topics/app/capability/sdk-lookup/lesson-3f9e120416e534d4e6d5.lesson.md) · 信号：ical4j, RRule, Recur, EventRecurrenceFormatter
- [动态取色用 getColors 加回退，写明弃用](../topics/app/capability/sdk-lookup/lesson-9769c8f754044944d3ad.lesson.md) · 信号：dynamicLightColorScheme, dynamicDarkColorScheme, @ohos.wallpaper, getColors
- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](../topics/app/capability/sdk-lookup/lesson-e9890889e591196c3d0d.lesson.md) · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit
- [应用内开关蓝牙先查 access 开关接口再定方案](../topics/app/capability/sdk-lookup/lesson-7a081dc36013a60358ac.lesson.md) · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable
- [无 OHOS 实现的插件先按底层能力建本地兼容插件](../topics/app/capability/sdk-lookup/lesson-45739c78f9767dacbc81.lesson.md) · 信号：dependency_overrides, platform_interface, MethodChannel, ohos/flutter_plugins
- [权限按目标 API 的 @permission 汇总](../topics/app/capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md) · 信号：@permission, requestPermissions, module.json5, ohos.permission.READ_PASTEBOARD
- [计费网络判定按承载显式映射，不靠单能力位](../topics/app/capability/sdk-lookup/lesson-20afdfffa13dc5bca10c.lesson.md) · 信号：isActiveNetworkMetered, @ohos.net.connection, NET_CAPABILITY_NOT_METERED, bearerTypes

### [app/cross-cutting](../topics/app/cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

- [基类横切行为逐方法映射，按子类布局核守卫再接线](../topics/app/cross-cutting/lesson-2fcb6612ee4106b34e17.lesson.md) · 信号：BaseActivity, BaseBusinessActivity, dispatchTouchEvent, onBackPressed
- [开关控制的常驻通知由应用级服务持有，不随页面 VM](../topics/app/cross-cutting/lesson-e9f03fcc7f1e781c4b24.lesson.md) · 信号：notificationManager.publish, aboutToAppear, aboutToDisappear, NavDestination
- [新增错误日志沿用 hilog 约定，不写 console.*](../topics/app/cross-cutting/lesson-11e9d15d947b30d2ce7e.lesson.md) · 信号：hilog.error, console.log, @kit.PerformanceAnalysisKit, DOMAIN
- [日志迁移审计按源端调用边界列日志点，不只核对配置](../topics/app/cross-cutting/lesson-e23468a0e439f8cf53e9.lesson.md) · 信号：log2File, debugFile, BqLog, hilog.info
- [自有服务端埋点引擎按源码移植并在门面注册](../topics/app/cross-cutting/lesson-dc3ac0500599ef7c9636.lesson.md) · 信号：ServiceLoader, ApiService, http.createHttp, Tracker
- [设置开关逐项落实运行期消费方，只调 setter 不算完成](../topics/app/cross-cutting/lesson-4d0f0176b3d09c33f1eb.lesson.md) · 信号：DataStore, SharedPreferences, preferences, @ObservedV2
- [诊断日志上传按源端打包清单与协议实现，收窄先确认](../topics/app/cross-cutting/lesson-d434bb5c16bc721d9a00.lesson.md) · 信号：usesCleartextTraffic, networkSecurityConfig, presignedUrl, http.request
- [退出登录先停同步再单事务清账号业务表并广播](../topics/app/cross-cutting/lesson-8b8e304a737e9fded451.lesson.md) · 信号：clearAllTables, RelationalStore, preferences, accessToken

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入声明、扩展能力与卡片登记

- [form_config 规格与刷新从源卡片声明换算，不填默认](../topics/app/entry/lesson-bc48518f40742add0054.lesson.md) · 信号：form_config, supportDimensions, defaultDimension, updateEnabled
- [intent-filter 逐条映射为 skills](../topics/app/entry/lesson-daba8a5b555e6657d085.lesson.md) · 信号：intent-filter, ohos.want.action.sendData, maxFileSupported, SEND_MULTIPLE
- [shortcuts 元数据挂 Ability 下，不挂模块级](../topics/app/entry/lesson-67118603fcc769a5edc9.lesson.md) · 信号：ohos.ability.shortcuts, module.json5, $profile:, shortcuts_config
- [前台服务改扩展能力先查基类导出，type 与基类成对](../topics/app/entry/lesson-16c24b9a44153d703f04.lesson.md) · 信号：extensionAbilities, ServiceExtensionAbility, AppServiceExtensionAbility, WorkSchedulerExtensionAbility
- [卡片按实际宽高选布局，getFormRect 下发尺寸](../topics/app/entry/lesson-7ad5a7d149de5bcec7da.lesson.md) · 信号：FormExtensionAbility, formProvider.getFormRect, onSizeChanged, formProvider.updateForm
- [固定快捷方式用 productViewManager](../topics/app/entry/lesson-fe5cf66672ce205ee0d7.lesson.md) · 信号：requestPinShortcut, isRequestPinShortcutSupported, disableShortcuts, ShortcutManager
- [外部入口页需确定快捷声明、Want 分支与参数写者](../topics/app/entry/lesson-c46f182cf1d01a97e05f.lesson.md) · 信号：ohos.ability.shortcuts, shortcuts_config.json, onNewWant, Want
- [深链声明 skills、domainVerify，隐式验收](../topics/app/entry/lesson-d77baa7494930d485425.lesson.md) · 信号：ohos.want.action.viewData, entity.system.browsable, pathStartWith, intent-filter
- [需显式 init 的封装在入口 onCreate 最早处调用](../topics/app/entry/lesson-8a881c2e07f80f83447c.lesson.md) · 信号：UIAbility.onCreate, AbilityStage.onCreate, NetworkConfig.init, HttpClient

### [app/hybrid](../topics/app/hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

- [Flutter 宿主迁移要打开实际容器子类逐项迁事件桥接](../topics/app/hybrid/lesson-6717b958e274143453a8.lesson.md) · 信号：FlutterBoostFragment, addEventListener, sendEventToFlutter, FlutterUIComponent
- [pushNativeRoute 按页面名建路由映射表不透传](../topics/app/hybrid/lesson-6587c954fd44464a7382.lesson.md) · 信号：FlutterBoostDelegate, pushNativeRoute, pageName, flutter_boost
- [兼容层返回对象保留宽高语义，大图先在原生侧缩放](../topics/app/hybrid/lesson-e85bdb26fa6acc0cc9f7.lesson.md) · 信号：AssetEntity, ImageSource, getImageInfo, compressAndGetFile
- [通道方法集按原生分支全集与 Dart 调用点双向对照](../topics/app/hybrid/lesson-e6b1032f702fc61940f2.lesson.md) · 信号：MethodChannel, setMethodCallHandler, call.method, invokeMethod

### [app/map](../topics/app/map/index.md) — 地图与定位接入：SDK 单例初始化与就绪、定位权限成组、坐标系与行政区名补齐、原生地图组件生命周期

- [占位地图换原生地图时接定位出口并转换坐标系](../topics/app/map/lesson-b5e8609c6602b3828fa9.lesson.md) · 信号：moveCamera, newLatLngZoom, MyLocationStyle, setMyLocationEnabled
- [定位只给坐标时用逆地理编码取行政区名，不留空名](../topics/app/map/lesson-a317e16cd9f46aa34962.lesson.md) · 信号：geoLocationManager.getAddressesFromLocation, geoLocationManager.getCurrentLocation, AMapLocation, subLocality
- [精确与模糊定位权限成组声明申请，任一授予即继续定位](../topics/app/map/lesson-b72e0d67fe27db2ae041.lesson.md) · 信号：ohos.permission.APPROXIMATELY_LOCATION, ohos.permission.LOCATION, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION
- [预构建子页中原生地图可见时初始化、隐藏暂停、卸载释放](../topics/app/map/lesson-0e997c4e9745728b7db6.lesson.md) · 信号：MapViewComponent, XComponent, HitTestMode.Transparent, HitTestMode.None
- [高德各单例分别设隐私与密钥，PoiQueryV2 必填城市](../topics/app/map/lesson-9477f662ac13df03778c.lesson.md) · 信号：PoiQueryV2, updatePrivacyShow, updatePrivacyAgree, setApiKey

### [app/media](../topics/app/media/index.md) — 媒体文件的用户可见出入口：安全控件与 picker 授权时序、沙箱落点与导出、播放 URI、预取与快照尺寸限制

- [SaveButton 底色圆角设在控件自身，不靠外层容器画](../topics/app/media/lesson-e1211056a34f58403e3a.lesson.md) · 信号：SaveButton, Color.Transparent, backgroundColor, borderRadius
- [SaveButton 授权回调只做快速写入，下载放点击前](../topics/app/media/lesson-089bb378b1ec034a3e84.lesson.md) · 信号：SaveButton, SaveButtonOnClickResult, photoAccessHelper, onClick
- [公共目录产物改落沙箱时每条链写出导出步骤](../topics/app/media/lesson-b59097ee968fe827f70d.lesson.md) · 信号：WRITE_EXTERNAL_STORAGE, ACTION_MEDIA_SCANNER_SCAN_FILE, DocumentViewPicker.save, MediaScannerConnection
- [图库选图用 PhotoViewPicker 并复制进应用目录](../topics/app/media/lesson-ad1db0aa0434c2e766fd.lesson.md) · 信号：PhotoViewPicker, READ_IMAGEVIDEO, MediaStore, photo_manager
- [导入导出按源运行时语义：OOM 兜底与 DEFLATED](../topics/app/media/lesson-8534b92df38e546092fe.lesson.md) · 信号：OutOfMemoryError, RangeError, ZipOutputStream, setMethod
- [本地路径接 Video src 前转为 file:// 地址](../topics/app/media/lesson-2b3d45c1a89dc1ead7e3.lesson.md) · 信号：Video, file://, fileUri.getUriFromPath, setUrl
- [源端主动预取后续图片时用图片解码真实预取并限缓存](../topics/app/media/lesson-cde53c6eab199d1262b2.lesson.md) · 信号：image.createImageSource, createPixelMap, PixelMap.release, imageLoader.enqueue
- [长内容存图先查快照尺寸限制，超一屏分段渲染拼接](../topics/app/media/lesson-e0f3b5b744e6b0518814.lesson.md) · 信号：componentSnapshot.createFromBuilder, SnapshotOptions, readPixels, writePixels
- [音频导入用 AudioViewPicker 并复制进沙箱](../topics/app/media/lesson-62ac5e65ac4aa51128bd.lesson.md) · 信号：AudioViewPicker, photoAccessHelper, MediaStore.Audio, READ_MEDIA_AUDIO

### [app/modules](../topics/app/modules/index.md) — 多模块（壳 HAP + HAR）边界：构建常量来源、跨模块导入、资源闭包归属与可复用函数的模块放置

- [DEBUG 条件映射 BuildProfile，不删分支](../topics/app/modules/lesson-3af52968ce5762501cd3.lesson.md) · 信号：BuildConfig.DEBUG, BuildProfile.DEBUG, BuildProfile.ets, BUILD_MODE_NAME
- [HAR 不引宿主 BuildProfile，模式由壳层注入](../topics/app/modules/lesson-6bd9ae0de39cecc06744.lesson.md) · 信号：BuildProfile, assembleHap, Index.ets, oh-package.json5
- [业务模块拆分按页面归属建表，不以源包分组为边界](../topics/app/modules/lesson-99b35920e77ae01076ea.lesson.md) · 信号：pageMap, NavPathStack, oh-package.json5, features/
- [共用非 UI 函数迁到普通模块，不从路由页面模块导出](../topics/app/modules/lesson-b58f26f0fdb7fb00db9e.lesson.md) · 信号：pages/, pageMap, services/, utils/
- [页面迁入 HAR 时带走 $r 与按名取资源的资源闭包](../topics/app/modules/lesson-edb937b04e0f1494ca37.lesson.md) · 信号：$r, getStringByNameSync, Unknown resource name, oh-package.json5

### [app/nfc](../topics/app/nfc/index.md) — NFC 读卡：能力三态前置检查、贴卡拉起的 skills 声明、按 UIAbility 前台派发与页面仿真

- [NFC 前台派发按 Ability 注册，页面用可见页表](../topics/app/nfc/lesson-a4ee90eabe3eef99ddbe.lesson.md) · 信号：enableForegroundDispatch, onNewIntent, tag.registerForegroundDispatch, onForeground
- [NFC 前置检查分不支持/关闭/可用三态，不折成布尔](../topics/app/nfc/lesson-5a140e45ecb578dd61ed.lesson.md) · 信号：NfcAdapter, isEnabled(), Settings.ACTION_NFC_SETTINGS, canIUse
- [贴卡拉起声明 TAG_FOUND，开关只管系统派发](../topics/app/nfc/lesson-89368bd540176a43d4a2.lesson.md) · 信号：android.nfc.action.TECH_DISCOVERED, tech-list, activity-alias, setComponentEnabledSetting

### [app/notification](../topics/app/notification/index.md) — 通知与代理提醒：WantAgent 按钮 requestCode 与刷新、通知字段约束、代理提醒边界与回退

- [代理提醒按自身 d.ts 映射按钮贪睡，写发布失败回退](../topics/app/notification/lesson-7f1bc7ddc88fab2d03bd.lesson.md) · 信号：reminderAgentManager, ActionButton, ActionButtonType, NotificationActionButton
- [通知按钮每次构建用不同 requestCode，正文不给空串](../topics/app/notification/lesson-716d06e75b7c2102c36c.lesson.md) · 信号：PendingIntent, requestCode, UPDATE_PRESENT_FLAG, wantAgent.getWantAgent

### [app/playback](../topics/app/playback/index.md) — 音视频播放：AVPlayer/SoundPool 设源与状态机、错误通道、装载令牌与释放、后台播放

- [rawfile 设 fdSrc 不拼 fd:// 串](../topics/app/playback/lesson-1267d6cabb117824c67a.lesson.md) · 信号：getRawFdSync, getRawFd, fdSrc, AVFileDescriptor
- [surface 按对应源页绑定，画面等比内接](../topics/app/playback/lesson-6b4950ca1655ae7bcb8f.lesson.md) · 信号：XComponent, SURFACE, surfaceId, AVPlayer
- [异步 AVPlayer 装载用代数令牌，停服务时显式复位](../topics/app/playback/lesson-511385674c16eb68c88c.lesson.md) · 信号：AVPlayer, STOPPED, PLAYING
- [短提示音保留混播与播放中 start 不重启语义](../topics/app/playback/lesson-5475edc47af05c1c6a5b.lesson.md) · 信号：MediaPlayer.create, requestAudioFocus, AudioFocusRequest, AudioSessionManager.activateAudioSession
- [组合异源切换步骤时不先改写入口守卫读取的状态](../topics/app/playback/lesson-6b2879705254045a49c5.lesson.md) · 信号：同一项即忽略
- [退后台续播时接 AVSession 与音频长时任务](../topics/app/playback/lesson-65db317135138c3181c7.lesson.md) · 信号：avSession.createAVSession, setAVPlaybackState, setBackgroundPlayMode, backgroundTaskManager.startBackgroundRunning
- [重载只释放实例并作废令牌，宿主销毁才全清 context](../topics/app/playback/lesson-1a3150939a5e45c02b0e.lesson.md) · 信号：release(), loadMusic
- [错误只经 on('error') 报，调用接 catch](../topics/app/playback/lesson-d0736ecd82af68edb87a.lesson.md) · 信号：on('error'), stateChange, onPlayerError, ExoPlayer
- [门面同步路径也要有源懒加载 getter 的回退来源](../topics/app/playback/lesson-cd4a69e85ec59eabf5b9.lesson.md) · 信号：seekTo, getPosition, getDuration

### [app/recreation](../topics/app/recreation/index.md) — 源端 Activity 重建语义：配置变化、进程回收与重启在不重建的 UIAbility 上显式处理与恢复

- [保留实例按是否配置重建区分，不以单例存在代替](../topics/app/recreation/lesson-ed571550c44efdeb321e.lesson.md) · 信号：NonConfigurationInstance, onConfigurationUpdate, hasInstance, configChanges
- [回收重建单列分支：仅系统回收时恢复整栈与原参数](../topics/app/recreation/lesson-b0405a29415547485ecb.lesson.md) · 信号：rememberNavController, NavHost, savedInstanceState, TaskStackBuilder
- [无 configChanges 时按源重建时序刷新关弹窗](../topics/app/recreation/lesson-94715d0df4c03a8fb5a5.lesson.md) · 信号：android:configChanges, screenOrientation, onSaveInstanceState, savedInstanceState
- [有随系统字号缩放的文本就声明跟随系统字号](../topics/app/recreation/lesson-ea965b7baf2488be23cd.lesson.md) · 信号：fontScale, configChanges, fontSizeScale, followSystem
- [杀进程意在重启用 restartApp 不用退出](../topics/app/recreation/lesson-73618bb856a8a7dfe7fc.lesson.md) · 信号：System.exit, Runtime.exit, Process.killProcess, ApplicationContext.restartApp

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [8 位颜色保持 #AARRGGBB，转换后逐项往返核对](../topics/app/resources/lesson-783faf2767a952034514.lesson.md) · 信号：colors.xml, color.json, #AARRGGBB, #RRGGBBAA
- [app.json5 的 icon 改指分层图标并补齐前景背景](../topics/app/resources/lesson-feec63f65102f5396e51.lesson.md) · 信号：app.json5, $media:layered_image, $media:app_icon, layered-image
- [分层图标前景裁到可见区，前景背景同尺寸](../topics/app/resources/lesson-d838f9236f7452b82738.lesson.md) · 信号：adaptive-icon, layered-image, layered_image.json, mipmap
- [反编译资源的 $父名__N 片段单独分类，输出名校验字符](../topics/app/resources/lesson-850dc758d337c4780ae9.lesson.md) · 信号：apktool, animated-vector, animation-list, __N
- [启动窗图标取自适应前景层，底色取源主题窗口背景](../topics/app/resources/lesson-c4af68b3ee1456525e8e.lesson.md) · 信号：startWindowIcon, startWindowBackground, start_window_background, windowSplashScreen
- [小图标转规范尺寸时图形居中到显示区，低清源不放大](../topics/app/resources/lesson-66e082374dc8992f48ae.lesson.md) · 信号：xxhdpi, 1024×1024, layered_image, mipmap
- [应用显示名同时改 AppScope 与入口 label 值](../topics/app/resources/lesson-55f44e2efdc1a49ac387.lesson.md) · 信号：app_name, EntryAbility_label, string.json, app.json5
- [沿用脚手架包名前核对决策与签名；vendor 按源端落地](../topics/app/resources/lesson-fb996956b33a1ba65861.lesson.md) · 信号：bundleName, com.example, applicationId, app.json5
- [版本号经 bundleManager 运行时读取，不写成常量](../topics/app/resources/lesson-a6ed8a9c6017ddb73beb.lesson.md) · 信号：BuildConfig.VERSION_NAME, BuildConfig.VERSION_CODE, bundleManager.getBundleInfoForSelfSync, GET_BUNDLE_INFO_DEFAULT
- [资源值按精确名查全部 values*，限定词写分支](../topics/app/resources/lesson-0c9e222422d81871b464.lesson.md) · 信号：getColor, getDimension, getInteger, values-land
- [颜色只写 hex 或 $color:，数组项写成对象](../topics/app/resources/lesson-94a3f7a5ec5ad8f8a3e8.lesson.md) · 信号：colors.xml, arrays.xml, @android:color, $color:

### [app/startup](../topics/app/startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

- [启动弹窗按源函数接口与显示守卫实现不换列表接口](../topics/app/startup/lesson-bbb31db6c369047ee32c.lesson.md) · 信号：@GET, Retrofit, CustomDialog, promptAction.openCustomDialog
- [延后采集通道时单独移植超时兜底发布就绪事件](../topics/app/startup/lesson-99a8d47085e4b1ae44de.lesson.md) · 信号：OaidResultEvent, Observable.timer, FWD-REF, OAID
- [持久化主题在 loadContent 前同步设好](../topics/app/startup/lesson-dcb3c5e66dec2d126234.lesson.md) · 信号：ApplicationContext.setColorMode, setColorMode, getPreferencesSync, loadContent
- [源端启动固定进主页时目标也进主页，登录页压在其上](../topics/app/startup/lesson-4c254d10ef9264683c55.lesson.md) · 信号：SplashActivity, NavPathStack, pushPathByName, LoginGuard
- [目标初始化极快时把首启加载页最短可见时长写进验收](../topics/app/startup/lesson-41bb62cd13921e4eedde.lesson.md) · 信号：SplashActivity, SplashScreen, windowStage.loadContent, setTimeout
- [迁启动链路时列出各去向页初始化请求与登录态组合](../topics/app/startup/lesson-8c24f05ec8df45401482.lesson.md) · 信号：initRequestData, SplashActivity, MainActivity, refreshToken
- [首启无已选项时定义显式空态，不以空编码请求](../topics/app/startup/lesson-95aa64d6b0a5c041d326.lesson.md) · 信号：hasInit, selectedCity, cityCode, preferences
- [首屏依赖异步装配服务时用可复位就绪门await后路由](../topics/app/startup/lesson-ccbf0a7f5b1809ef5880.lesson.md) · 信号：EntryAbility.onCreate, loadContent, onReady, Promise

### [app/system-state](../topics/app/system-state/index.md) — 系统能力的异步状态真值：终态回读、分协议聚合、回调会话归属、同步抛错收敛、读后增量写回与返回值判定

- [三方授权回调先比对 state，不匹配即忽略](../topics/app/system-state/lesson-95314752073ab4760059.lesson.md) · 信号：requestId, authCode, errCode, SendAuth.Resp
- [分协议连接回调按设备聚合，全部断开才判断开](../topics/app/system-state/lesson-ecc67592eba3402c0a1f.lesson.md) · 信号：connectionStateChange, A2DP, HFP, ACL
- [声明 void 的同步接口查 @throws 并在服务层捕获](../topics/app/system-state/lesson-7ed00c55221c0f935d95.lesson.md) · 信号：startBLEScan, stopBLEScan, @ohos.bluetooth.ble, BusinessError
- [接 getOAID 需声明跟踪同意权限，全零串视为未授权](../topics/app/system-state/lesson-2b00c4ffaeb442d87e5e.lesson.md) · 信号：identifier.getOAID, ohos.permission.APP_TRACKING_CONSENT, requestPermissionsFromUser, checkAccessToken
- [蓝牙开关以 getState 回读终态为准，过渡态不写关闭](../topics/app/system-state/lesson-29922f57cc365ff3d638.lesson.md) · 信号：access.getState, access.on('stateChange'), STATE_ON, STATE_OFF
- [读基线写增量的亮度手势分映射读写两侧，就绪时预读](../topics/app/system-state/lesson-33791daf74fc4298779e.lesson.md) · 信号：setWindowBrightness, getWindowProperties().brightness, settings.display.SCREEN_BRIGHTNESS_STATUS, ACTION_DOWN

### [app/window](../topics/app/window/index.md) — 窗口级行为：Activity 窗口标志与画中画映射到共享主窗口/PiPWindow 的作用范围与状态

- [画中画映射 PiPWindow 链路，不凭记忆判手机端没有](../topics/app/window/lesson-a45be20055d942e12052.lesson.md) · 信号：PictureInPictureParams, onUserLeaveHint, onPictureInPictureModeChanged, @ohos.PiPWindow
- [页窗口标志在共享主窗口上随页显隐成对开关](../topics/app/window/lesson-ea9a6cfecca9e091c7ea.lesson.md) · 信号：FLAG_KEEP_SCREEN_ON, FLAG_SECURE, getWindow(), window.getLastWindow
## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/api-signatures](../topics/arkts/api-signatures/index.md) — 调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定

- [intl 货币格式化须显式传 currency 码](../topics/arkts/api-signatures/lesson-19cedec8ad1bc4b08b2c.lesson.md) · 信号：intl.NumberFormat, getCurrencyInstance, style: 'currency', @kit.LocalizationKit
- [tabBar 不接受 { title } 对象字面量](../topics/arkts/api-signatures/lesson-b402fa546504a1dd6db7.lesson.md) · 信号：TabContent, .tabBar(, TabBarOptions, BottomTabBarStyle
- [依赖 API 单位与作用范围时两端都读语义说明](../topics/arkts/api-signatures/lesson-f5cf8413ebea57f3b415.lesson.md) · 信号：vp2px, px2vp, .d.ts, uiContext
- [写 SDK 调用前按本地 .d.ts 核对成员名与可空性](../topics/arkts/api-signatures/lesson-6e558834938be19c04e2.lesson.md) · 信号：ets/component, ets/api, AppStorageV2.connect, getHostContext
- [单调计时映射 getUptime 并选 TimeType](../topics/arkts/api-signatures/lesson-ce456d60534d97524aa4.lesson.md) · 信号：System.nanoTime, SystemClock.elapsedRealtime, systemDateTime.getUptime, TimeType.ACTIVE
- [属性方法不传 ResourceStr 联合值按重载定型](../topics/arkts/api-signatures/lesson-63660a8304f7d3920bfc.lesson.md) · 信号：accessibilityText, ResourceStr, @Computed, contentDescription
- [禁编译写大页后对照this成员常量导入与$r键声明](../topics/arkts/api-signatures/lesson-e04e26f1f98116275982.lesson.md) · 信号：$r('app., resources/base/element, @Local, @Param

### [arkts/async-mapping](../topics/arkts/async-mapping/index.md) — 源端同步调用、线程与事件投递改成 Promise/异步 API 后的时序、重入、线程与结果三态

- [EventBus 需同步按引用投递时自建订阅表](../topics/arkts/async-mapping/lesson-9db967b1941da87f27be.lesson.md) · 信号：EventBus, EventBus.getDefault, @ohos.events.emitter, eventHub
- [单线程执行器改 Promise 队列时给重入内部版本](../topics/arkts/async-mapping/lesson-cdc6de4ebcdeeadc287c.lesson.md) · 信号：Executor, runnable.run(), Promise
- [后台拷贝用异步 IO 或 taskpool，不包 *Sync](../topics/arkts/async-mapping/lesson-c54d1c8af2177b819837.lesson.md) · 信号：AsyncTask, doInBackground, THREAD_POOL_EXECUTOR, fileIo.copyFileSync
- [被拒与故障都 reject 时用单次适配器还原三态](../topics/arkts/async-mapping/lesson-47faf26b44bb4075b0d2.lesson.md) · 信号：BusinessError, Promise&lt;void&gt;, IOException, TagLostException
- [连续同步平台调用改 Promise 时在网关内串行](../topics/arkts/async-mapping/lesson-ba0cb144aa48f9584060.lesson.md) · 信号：Vibrator.cancel, vibrate(pattern), stopVibration, startVibration

### [arkts/java-stdlib](../topics/arkts/java-stdlib/index.md) — Java/Kotlin 标准库调用（集合序、字符串、正则、格式化、日历）与形似 JS API 的语义差异复刻

- [DecimalFormat 按半偶舍入与应用语言复刻](../topics/arkts/java-stdlib/lesson-ae093dedda604fddf17e.lesson.md) · 信号：DecimalFormat, BigDecimal, setScale, RoundingMode.HALF_EVEN
- [Java 读行切分格式化日历集中兼容实现](../topics/arkts/java-stdlib/lesson-237091b9b04bc4cd340b.lesson.md) · 信号：BufferedReader.readLine, String.split, String.format, SimpleDateFormat
- [位置参数插入用 split/join，不把参数当替换串](../topics/arkts/java-stdlib/lesson-ecbaa1723e2beb9b1aec.lesson.md) · 信号：getString, String.format, %1$s, String.replace
- [形似 JS 的平台库调用按源语义逐项移植](../topics/arkts/java-stdlib/lesson-5e3ba83ebfe5bbdf9278.lesson.md) · 信号：Pattern, replaceAll, compareToIgnoreCase, List.remove
- [集合迭代序、byte 比较与返回码按 Java](../topics/arkts/java-stdlib/lesson-1f4747c81f16e9529787.lesson.md) · 信号：HashSet, HashMap, keySet, toArray

### [arkts/runtime-semantics](../topics/arkts/runtime-semantics/index.md) — 源端同步调用或数值运算改成 ArkTS 后的运行时差异：异步失败分支、初始化顺序、错误通道与 number 边界

- [Float 运算比较按 float32 后用 ===](../topics/arkts/runtime-semantics/lesson-0deb51172ebdd2e056a9.lesson.md) · 信号：Math.fround, toFloat(), Float, (int)
- [Kit 错误取 message 与 code，码先归一](../topics/arkts/runtime-semantics/lesson-b19162077a2ab886d809.lesson.md) · 信号：BusinessError, Number(code), instanceof Error, @ohos.net.http
- [仓库方法前置失败走声明的错误通道不返回空集合](../topics/arkts/runtime-semantics/lesson-5c703b4b1128e37dbef5.lesson.md) · 信号：UIAbilityContext, requestPermissionsFromUser, photoAccessHelper, Repository
- [异步 initialize 失败分支要复位状态并离开加载态](../topics/arkts/runtime-semantics/lesson-338f11844f0010e46bc3.lesson.md) · 信号：initialize(), LoadingProgress, aboutToAppear, SharedPreferences
- [比值计算保留零分母分支与钳制，0/0 得 NaN](../topics/arkts/runtime-semantics/lesson-52d7edb9042110e30eb4.lesson.md) · 信号：coerceIn, NaN, total == 0, Math.min
- [超安全整数的 long 常量以字符串拼进 SQL](../topics/arkts/runtime-semantics/lesson-5f669c379cfcdb14ad10.lesson.md) · 信号：Long.MAX_VALUE, Number.MAX_SAFE_INTEGER, bigint, 9223372036854775807
- [输入初值先于首个 await；源端同步初始化保持同步](../topics/arkts/runtime-semantics/lesson-843a70afd7e08bfed97c.lesson.md) · 信号：TextInput, aboutToAppear, @Local, onCreate

### [arkts/strict-mode](../topics/arkts/strict-mode/index.md) — ArkTS 严格类型系统对对象字面量、接口实现、异常收窄与类声明顺序的限制，不编译时也会留到编译门

- [SDK 观察者声明为 class 时用类型标注的对象字面量](../topics/arkts/strict-mode/lesson-6e74f064efe2649fc295.lesson.md) · 信号：errorManager.on('error'), ErrorObserver, onUnhandledException, onException
- [static 初始化器引用的类须先声明或从独立文件导入](../topics/arkts/strict-mode/lesson-f80ae7c3747420ef16f7.lesson.md) · 信号：AppStorageV2.connect, PersistenceV2.globalConnect, @ObservedV2, new Cls()
- [对象字面量写具名类，Record 替换用字段类或 Map](../topics/arkts/strict-mode/lesson-1696967d1320c7735732.lesson.md) · 信号：Record&lt;string, Object&gt;, \[key: string\], Array&lt;{, constructor(public
- [接口参数用 implements 的具名类，不传函数字面量](../topics/arkts/strict-mode/lesson-931ef95a3d0cf202fe5b.lesson.md) · 信号：Port, Repository, Adapter
- [重抛异常前先收窄为 Error，不直接 throw 变量](../topics/arkts/strict-mode/lesson-dbfae443e671c568e14e.lesson.md) · 信号：throw error, instanceof Error, catch (, new Error(String(

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [@BuilderParam 传值写箭头闭包不传方法引用](../topics/arkts/ui-syntax/lesson-7d643db6ab406ae64c77.lesson.md) · 信号：@BuilderParam, 10905102, @Builder, content: this.
- [V2 装饰器裸写，插槽默认值只引用 @Builder 函数](../topics/arkts/ui-syntax/lesson-8b145360b447a10d52ef.lesson.md) · 信号：@Event(), @Local(), @Param(), @BuilderParam
- [build() 组件逐行书写，含组件方法用 @Builder](../topics/arkts/ui-syntax/lesson-08e71bb72d05b1d79d28.lesson.md) · 信号：build(), @Builder, ForEach, Repeat
- [stateStyles 只写 @Styles 或点号块](../topics/arkts/ui-syntax/lesson-39d1dee415d4a252fc5c.lesson.md) · 信号：stateStyles, @Styles, StateStyles, 10905203
- [换容器头核对对齐链，Stack 用 alignContent](../topics/arkts/ui-syntax/lesson-18d9c9a34c1952f43f53.lesson.md) · 信号：justifyContent, alignItems, alignContent, Stack
- [组件成员名避开 position/width 等通用属性](../topics/arkts/ui-syntax/lesson-c1968bdf112ed3e6b259.lesson.md) · 信号：zIndex, @Param
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/model](../topics/data/model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持

- [UI 模型展示字段逐项按源端绑定取值，code/ID 先转换](../topics/data/model/lesson-22f5100f6718eaecc66f.lesson.md) · 信号：RecyclerView.Adapter, onBindViewHolder, join(, iconId
- [名称谓词在内部做大小写归一不靠调用方](../topics/data/model/lesson-0ac4dfb5731bf1559e78.lesson.md) · 信号：toLowerCase(), lowercase(Locale.ROOT), Locale.ROOT, equalsIgnoreCase
- [多组表单收集请求时按模式设独立字段](../topics/data/model/lesson-dee3401b34b8fab1a0fb.lesson.md) · 信号：sector/block/value
- [完成态派生逐分支移植源函数，审计摘要只作线索](../topics/data/model/lesson-4ad956bab5fca6d7f418.lesson.md) · 信号：isCompleted, completedCount, completionMode, occurrenceDate
- [实体字段按源类型真值定型，null 与空串分开](../topics/data/model/lesson-5a67ac0592e5a3fa20b9.lesson.md) · 信号：Parcel, String.valueOf, cursor.getString, ResultSet.getString
- [带本月语义的保存与查询按源实体构造参数建关联键](../topics/data/model/lesson-6a95a3ae5f47a15892fc.lesson.md) · 信号：Budget(month, getBudgetByTimestamp, Repository, @Query
- [持久化字符串枚举映射用逐成员 switch 不做名称变换](../topics/data/model/lesson-b92a8a56aee6db5e9c52.lesson.md) · 信号：FRENCH_PRESS, toUpperCase, replace('_', default:
- [逐字段搬运 Builder 构造时核对两端字段单位](../topics/data/model/lesson-c73deaf6f27d3426c4e9.lesson.md) · 信号：Builder, durationMs, durationSec, *1000

### [data/network-auth](../topics/data/network-auth/index.md) — 鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者

- [token 失效判定按响应拦截器实际分支的码迁移](../topics/data/network-auth/lesson-bad79e090d2af44d167b.lesson.md) · 信号：reasonCode, HandleErrorInterceptor, TokenInterceptor, LoginExpired
- [响应头携带 token 时 HTTP 封装连头一起返回](../topics/data/network-auth/lesson-2a4e6af209308c08aaa6.lesson.md) · 信号：headers()\["Authorization"\], RefreshToken, Response&lt;BaseResponse, TokenManager
- [拦截器注入的请求头逐条迁到默认头，格式以源码为准](../topics/data/network-auth/lesson-217e93ef9097efc519f1.lesson.md) · 信号：addHeader, TokenInterceptor, Authorization, Bearer
- [拦截器读取的本地公参键都要有写入者，只迁读取不算完](../topics/data/network-auth/lesson-7e04234bdf5aef97b651.lesson.md) · 信号：Interceptor, OAID, preferences, deviceId
- [请求通道按源端重载决定取 key 门，握手基址随请求](../topics/data/network-auth/lesson-62499aa25e87fa6ab5e1.lesson.md) · 信号：ensureKey, OkGo, baseUrl, sessionKey

### [data/network-endpoint](../topics/data/network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

- [拼接函数统一处理 baseUrl 与 path 之间的斜杠](../topics/data/network-endpoint/lesson-d767b84213eb5ef93034.lesson.md) · 信号：${baseUrl}${path}, baseUrl, @GET, @POST
- [服务地址沿键名追到源端常量，host 与环境不自拟](../topics/data/network-endpoint/lesson-246252824c631aa6eff5.lesson.md) · 信号：BuildConfig.BASE_URL, SpKey.BASE_URL, NetworkModule, baseUrl
- [构建期注入的地址与密钥从私有配置接入，空配置拒发包](../topics/data/network-endpoint/lesson-30ccd1d65d2c39029256.lesson.md) · 信号：buildProfileFields, process.getEnvironmentVar, BuildConfig, parameterFile
- [网络权限声明进 module.json5，任务要有写者](../topics/data/network-endpoint/lesson-faec7be031b7f64752c4.lesson.md) · 信号：module.json5, requestPermissions, ohos.permission.INTERNET, ohos.permission.GET_NETWORK_INFO
- [链接 getter 按完整返回表达式拼渠道参数](../topics/data/network-endpoint/lesson-da377615b178b2fe0c67.lesson.md) · 信号：AdEntrance.getStartChannel, aliasCode=, WebView

### [data/network-request](../topics/data/network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

- [@FieldMap 用表单编码，@Body 才用 JSON](../topics/data/network-request/lesson-1cc76f37fe0aea9fef25.lesson.md) · 信号：@FieldMap, @FormUrlEncoded, @Field, @Body
- [Service 收不透明 body 时追到源端构造处照抄字段](../topics/data/network-request/lesson-0bc494e864b2d8ab1a34.lesson.md) · 信号：@Body, RequestBody, data: Object, device_id
- [cryptoFramework 规格串只写算法位数，结果判空](../topics/data/network-request/lesson-3684e08592c85de82204.lesson.md) · 信号：cryptoFramework, createAsyKeyGenerator, convertPemKeySync, doFinalSync
- [移植加解密工具保留空串直返与解密失败回退原文](../topics/data/network-request/lesson-4232e195ff42fc63ba43.lesson.md) · 信号：AESUtil, aesEncrypt, aesDecrypt, isEmpty

### [data/parsing](../topics/data/parsing/index.md) — JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度

- [@ohos.xml 开始事件按顺序无关组装并建命名空间栈](../topics/data/parsing/lesson-447985a4376146f6d9f2.lesson.md) · 信号：@ohos.xml, XmlPullParser, tokenValueCallbackFunction, attributeWithTagCallbackFunction
- [JSON 取值的空值与类型规则按 org.json 定](../topics/data/parsing/lesson-5034b56be6fd828164c9.lesson.md) · 信号：org.json, getString, optString, getInt
- [byte\[\] 常量逐下标转写核总长，冲突以源为准](../topics/data/parsing/lesson-0bba9db6a18f2e732334.lesson.md) · 信号：byte\[\], Uint8Array, KeyA, KeyB
- [fromJson 宽类型取值用 typeof 收窄再赋值](../topics/data/parsing/lesson-2622bc32995ac62389c3.lesson.md) · 信号：fromJson, typeof, instanceof, Record&lt;string, Object&gt;
- [org.json 输出按库语义：null 删键、转义 /](../topics/data/parsing/lesson-0caaa4efc70dad90a15f.lesson.md) · 信号：JSONObject.put, JSONObject.NULL, JSONArray, toString(indent)
- [proto3 手写编解码按 wire type 成对实现读写](../topics/data/parsing/lesson-ae1aa4ff5e2217b67e06.lesson.md) · 信号：wire type, varint, int32, sfixed32
- [先定目标 res.data 对应源端哪层类型，再逐层写取值键](../topics/data/parsing/lesson-dc5c370e370c2be803c1.lesson.md) · 信号：res.data, BaseResponse&lt;T&gt;, getObject, getArray
- [命名常量替换字面区间时按每处用途选端点](../topics/data/parsing/lesson-1d0b6dde849cbd70ee8f.lesson.md) · 信号：substring(12,20), substring(12,18), GPB
- [大整数 id 用 bigint，解析前给数字加引号保真](../topics/data/parsing/lesson-c066489fcf35ab37378c.lesson.md) · 信号：JSON.parse, bigint, Long, 2^53
- [显式解码器保留 Gson 数字与字符串互转的宽松规则](../topics/data/parsing/lesson-871d3751cadde6dda1dc.lesson.md) · 信号：Gson, string(), number(), typeof

### [data/preferences](../topics/data/preferences/index.md) — 偏好键值存储：装载时机与同步读写、批量提交原子性、读点缺省值与默认值落盘

- [偏好入口同步装载，读写走 Sync 接口](../topics/data/preferences/lesson-93b3eeff61598bc42172.lesson.md) · 信号：getSharedPreferences, PreferenceManager.getDefaultSharedPreferences, getPreferencesSync, getPreferences
- [同键多读点缺省不同时逐读点保留，不收敛为单一默认](../topics/data/preferences/lesson-11e4e15acdbadf579e07.lesson.md) · 信号：getBoolean, getString, getXxx
- [批量 commit 改为先暂存校验再 putSync](../topics/data/preferences/lesson-24bc4929b771a9a33ef4.lesson.md) · 信号：SharedPreferences.Editor, editor.putX, putSync, flushSync
- [设置页出现时为缺键写 XML 默认值并落盘](../topics/data/preferences/lesson-4283cc343b875489b851.lesson.md) · 信号：addPreferencesFromResource, PreferenceFragment, PreferenceActivity, PreferenceScreen

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作

- [Room 迁移保留库名、schema 版本与显式升级分支](../topics/data/storage/lesson-a6f300f9295ba538f23b.lesson.md) · 信号：@Database(version, addMigrations, AutoMigration, fallbackToDestructiveMigration
- [SQLiteOpenHelper 首次取库才建库，启动不预建](../topics/data/storage/lesson-519f6769ca714500d9c3.lesson.md) · 信号：SQLiteOpenHelper, getReadableDatabase, getWritableDatabase, relationalStore
- [mkdirSync 对已存在目录抛错，先判存在再建](../topics/data/storage/lesson-3f6b5d0b0ea6806a1b0c.lesson.md) · 信号：fileIo.mkdirSync, 13900015, fileIo.accessSync, @kit.CoreFileKit
- [单语句直接写，事务含 await 用独立事务](../topics/data/storage/lesson-a078efd3361b4abe58e3.lesson.md) · 信号：createTransaction, beginTransaction, beginTrans, rollBack
- [手写 INSERT 省略自增主键列，id=0 表示未赋值](../topics/data/storage/lesson-5c101b4b3f08ab317202.lesson.md) · 信号：@PrimaryKey(autoGenerate = true), INSERT OR REPLACE, relationalStore, executeSql
- [手写建表 SQL 表名列名统一加引号，关键字不裸写](../topics/data/storage/lesson-c55c56444f5271471a64.lesson.md) · 信号：CREATE TABLE, createSql, relationalStore, executeSql
- [按 VERSION 分派建表升降级，打开失败可重试](../topics/data/storage/lesson-7d8f649aa2713323e072.lesson.md) · 信号：SQLiteOpenHelper, onCreate, onUpgrade, onDowngrade
- [按日期实时计算的字段不改绑静态资产，先查内置能力](../topics/data/storage/lesson-6d259db1ffd8927834a2.lesson.md) · 信号：Lunar.fromDate, dayYi, dayJi, Intl.DateTimeFormat
- [演示预置数据逐字段取自源种子工厂与 assets 不自拟](../topics/data/storage/lesson-1c513fdf2cf212354aa0.lesson.md) · 信号：DemoDataFactory, rawfile, LocalDate.now(), plusDays
- [首次启动播种在启动路径落调用并保留标记门控](../topics/data/storage/lesson-dc3f2589254d02893b0e.lesson.md) · 信号：Application.onCreate, seedDemoDataOnFirstLaunch, has_seeded_demo_data, EntryAbility.onCreate
- [首次建库播种放进建表分支同一事务，手动补充不带 id](../topics/data/storage/lesson-488a3bd782acef92f5cf.lesson.md) · 信号：onCreate, RoomDatabase.Callback, copy(id = 0), ValuesBucket

### [data/sync](../topics/data/sync/index.md) — 同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤

- [同步终态只在最后一轮后发一次，开始进度保留源门控](../topics/data/sync/lesson-34f35851208470602570.lesson.md) · 信号：SyncCoordinator, EventBus, onComplete
- [同步调度合并在途任务要补跑尾随请求，失败项重推](../topics/data/sync/lesson-cfe552e1b20080212ce9.lesson.md) · 信号：Mutex.withLock, Promise
- [多路聚合缓存至少一路成功才写，命中校验时效和载荷](../topics/data/sync/lesson-c6379cfcbee86500f91f.lesson.md) · 信号：refreshTime, Promise.all, Promise.allSettled, TTL
- [异步落库完成后再广播触发重查的事件](../topics/data/sync/lesson-1d3ab8b9d39bd8f6e24d.lesson.md) · 信号：Promise
- [替代作业聚合器时结束作业写显式终态不删键](../topics/data/sync/lesson-d18e6e019cad3d26839b.lesson.md) · 信号：WorkManager, LiveData, COMPLETED
- [重写多阶段数据流程时保留缓存写入等副作用步骤](../topics/data/sync/lesson-686bbe76f7c2c783f2bd.lesson.md) · 信号：DAO, currentId, Repository
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/claimed-without-receipt](../topics/process/claimed-without-receipt/index.md) — 凭文本形式的调用、部分输出、过期构建或自动脚本结果宣告写入与完成，缺少真实回执核验

- [sed/perl 改含 $r 的片段用单引号并读回](../topics/process/claimed-without-receipt/lesson-6dae0bf2657b0e339742.lesson.md) · 信号：perl -pi, sed -i, $r(, app.float
- [写文件以执行回执为准，覆盖入口页后内容断言读回](../topics/process/claimed-without-receipt/lesson-776ed5eb216833c6b002.lesson.md) · 信号：loadContent, Hello World, RelativeContainer, apply_patch
- [功能对齐以代码落点为准，空回调不算实现](../topics/process/claimed-without-receipt/lesson-9147be4d87153de9c5b6.lesson.md) · 信号：onClick, JSON.stringify, NavPathStack, onEventMainThread
- [缺 hvigorw 时用工具自带构建，文本契约不算编译](../topics/process/claimed-without-receipt/lesson-25bc0b7518d335a947d6.lesson.md) · 信号：hvigorw, assembleHap, command-line-tools/bin/hvigorw, CompileArkTS

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [占位只登记输入缺值的情况，能实现的当场实现](../topics/process/deferred-fulfillment/lesson-a2f6a4ae9a72be740de6.lesson.md) · 信号：forward-ref-uncertain, resource-pending-asset, .d.ts, getXxxProperties
- [规格留待裁决条目，决策轮逐条出题或关闭](../topics/process/deferred-fulfillment/lesson-35b9cdfd5d22ce53465e.lesson.md) · 信号：待裁决, Kit, decision ledger, placeholder
- [解前向占位按触发文本逐项兑现，写常量不算闭合](../topics/process/deferred-fulfillment/lesson-eb4de4fd7452308a0483.lesson.md) · 信号：FWD-REF, forward-ref-uncertain, TODO, return false
- [页内先写共享件副本时登记待收敛并回收](../topics/process/deferred-fulfillment/lesson-447ba5818e4e203272e8.lesson.md) · 信号：待收敛项

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [Application 注册的接收器读本体写入规格](../topics/process/enumeration-gaps/lesson-4fb1c103822a8fd30b2a.lesson.md) · 信号：BroadcastReceiver, registerReceiver, CONNECTIVITY_ACTION, @ohos.net.connection
- [截图页范围含其入口直达二级页，不取最窄解释](../topics/process/enumeration-gaps/lesson-91c89aff3f8c5c47bd2a.lesson.md) · 信号：startActivity, Intent, Activity, setOnClickListener

### [process/handoff-loss](../topics/process/handoff-loss/index.md) — 跨阶段推进、批次收口、重新规划或转述派工时，移交项、全局动作与规则原文在传递中丢失

- [执行替换清单先建公共门面，收尾 rg 旧写法归零](../topics/process/handoff-loss/lesson-af15c43279110b3b7692.lesson.md) · 信号：ToastService, promptAction.showToast, DialogHelper.showToast, LazyForEach
- [跨文件补实现的功能登记带负责方与验证的移交项](../topics/process/handoff-loss/lesson-4f81eeea17b94190c2de.lesson.md) · 信号：HANDOFF, resolve_by, slice:N, TODO

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [内联被调组件时按调用点实参整链代入公式](../topics/process/inferred-not-traced/lesson-4428ce765fcef294b004.lesson.md) · 信号：derivedStateOf, Composable, timeMultiplier, animatedProgress
- [守卫移到调用侧时并入被调方法体内全部守卫](../topics/process/inferred-not-traced/lesson-06e3564e91948a2b05a3.lesson.md) · 信号：saveStateToFile, saveState, createNewGame, initialize()
- [推断默认选中前读默认值回调、过滤函数与回退条件](../topics/process/inferred-not-traced/lesson-e7a9842a56aa53621d27.lesson.md) · 信号：BasePage, override fun, defaultSelection
- [新旧两套实现并存时以当前构建启用的为基准](../topics/process/inferred-not-traced/lesson-2e8ffecce25935dda502.lesson.md) · 信号：buildConfigField, manifestPlaceholders, gradle
- [源端层层委托时追到最终实现再写规格与代码](../topics/process/inferred-not-traced/lesson-4606ccc434e247d4a240.lesson.md) · 信号：DialogHelper, DAO, Repository, LazyColumn
- [辅助谓词与 getter 读到定义再翻译，不按名字推断](../topics/process/inferred-not-traced/lesson-b3f534eb740a768d95a6.lesson.md) · 信号：isPlayingState, playPause, LiveData&lt;String&gt;, PAUSED
- [非空类型上的 null 判断按死分支迁移](../topics/process/inferred-not-traced/lesson-8c18bb22a8ecfe8c7f8a.lesson.md) · 信号：collectAsState, Flow&lt;Boolean&gt;, DataStore, == null

### [process/lossy-transcription](../topics/process/lossy-transcription/index.md) — 逐句转写源端表达式与状态逻辑时简化改写，丢括号分支或合并不同生命周期的字段

- [复位函数只复位源端每局路径实际赋值的字段](../topics/process/lossy-transcription/lesson-e2a08b9a98504718cd24.lesson.md) · 信号：initGame
- [布尔组合条件逐字保留括号并列真值表](../topics/process/lossy-transcription/lesson-381ebc5899e92cbd23a2.lesson.md) · 信号：LTR

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [共享组件挂载页面以源宿主容器 replace/add 为准](../topics/process/secondary-over-source/lesson-34c8ac69ad849f8c24e1.lesson.md) · 信号：FragmentTransaction, replace(, add(, Fragment
- [共享组件替换页面片段前逐项比对源码视觉](../topics/process/secondary-over-source/lesson-ad6f23b88f09b55dd92a.lesson.md) · 信号：orphan component, @Builder, borderRadius, fontColor
- [写页前读源 ViewModel/Service 列行为清单](../topics/process/secondary-over-source/lesson-1997518f92b444368073.lesson.md) · 信号：ViewModel, Service, Screen, DAO
- [合成快照点击清单空时按源布局 onClick 绑定实现跳转](../topics/process/secondary-over-source/lesson-3ea52b78643f49c13cd1.lesson.md) · 信号：android:onClick, @{page::, view_xml_synthesized, clickable_elements
- [多模块同名布局按页面类模块与 Binding 类解析](../topics/process/secondary-over-source/lesson-d75ddb53d6609b35d025.lesson.md) · 信号：layout_sources, ViewBinding, DataBinding, fragment_mine.xml
- [沿用已生成页面或兄弟写法前回源码核对语义](../topics/process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md) · 信号：@Builder, onReady, maxLength, replace_all
- [派工要求按源码确认的值回源码核对，没读到标未核实](../topics/process/secondary-over-source/lesson-93214f5a49c4d1d82316.lesson.md) · 信号：kapt stub, .kt, Interceptor, grep
- [规格与源码冲突按源实现，例外只认决策 ID](../topics/process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md) · 信号：decision_ref, decision_gaps, source-notes, PD-

### [process/unapproved-deviation](../topics/process/unapproved-deviation/index.md) — 未经带编号决策批准就修正源端缺陷、补写源端没有的元素或按成本降级

- [不补源端没有的元素；框架默认元素须保留](../topics/process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md) · 信号：ListPreference, DialogPreference, android.R.string.cancel, PD-
- [源端可观察缺陷照迁并核次数，修正走待批决策](../topics/process/unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md) · 信号：decision_gaps, source-notes, IOException, Thread

### [process/unloaded-input](../topics/process/unloaded-input/index.md) — 必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../topics/process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md) · 信号：Get-Content, Select-String, -Encoding UTF8, $OutputEncoding
- [上下文压缩后按 spec_ref 与源码锚点重读再写计划代码](../topics/process/unloaded-input/lesson-f616adca9430826b1661.lesson.md) · 信号：spec_ref, feature-index, integration_points, Activity
- [必读 skill 与源码逐份读全，截断即重读再写码](../topics/process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md) · 信号：SKILL.md, sed -n, loaded_skills, rg
- [按他文件返回语义改调用方前重读其当前版本](../topics/process/unloaded-input/lesson-35f4f9b3cf566d33e79c.lesson.md) · 信号：ViewModel
- [编排者代写切片前加载 worker 的全部派工输入](../topics/process/unloaded-input/lesson-b90d7f55409a3a34253d.lesson.md) · 信号：spec_refs, feature-plan, ui-manifest, Adapter

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [结论先查本机 SDK 与依赖源，查不到才标置信度](../topics/process/unverified-as-fact/lesson-c0f990ea57a901951ba8.lesson.md) · 信号：HARD, dp, .gitmodules, ?android:attr
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/accessibility](../topics/ui/accessibility/index.md) — 无障碍语义转写：角色、可用态、朗读节点合并与独立、图标朗读文本来源

- [可点击行卡转写 role、enabled 与朗读合并](../topics/ui/accessibility/lesson-5caf7eadb69e940926f9.lesson.md) · 信号：clickable, combinedClickable, Role.Button, accessibilityRole
- [无障碍文本按源描述用 $r，空不臆造](../topics/ui/accessibility/lesson-d80ced7be82765244889.lesson.md) · 信号：contentDescription, accessibilityText, stringResource, IconButton

### [ui/animation/frame-clock](../topics/ui/animation/frame-clock/index.md) — 帧驱动与计时：invalidate、自建渲染线程与帧时钟动画迁成 vsync 帧回调，请求合并、实例数与前后台时间推进

- [SurfaceView 线程循环按实例迁，vsync 驱动](../topics/ui/animation/frame-clock/lesson-4da9eabca745b3b2be91.lesson.md) · 信号：SurfaceView, SurfaceHolder.Callback, lockCanvas, unlockCanvasAndPost
- [invalidate 迁成单一下一帧入口，待决标志合并](../topics/ui/animation/frame-clock/lesson-27d9e16a099c2fb437eb.lesson.md) · 信号：View.invalidate, invalidate(), onDraw, UIContext.postFrameCallback
- [自驱 ticker 进度按帧时间减起点，不钳增量](../topics/ui/animation/frame-clock/lesson-6d6ba721c81206d45fbe.lesson.md) · 信号：Animatable, animateTo, tween(, LinearEasing

### [ui/animation/transitions](../topics/ui/animation/transitions/index.md) — 显隐、尺寸、内容切换、列表条目与页面转场动画按源时长、曲线与先后顺序落为 ArkUI 动画

- [Compose 显隐与尺寸动画逐项落实，不只渐变](../topics/ui/animation/transitions/lesson-a4e6bcfb28597691c028.lesson.md) · 信号：AnimatedVisibility, expandVertically, shrinkVertically, AnimatedContent
- [NavHost 四向转场由页面绑定共享转场态](../topics/ui/animation/transitions/lesson-9de3322165e533d6b790.lesson.md) · 信号：enterTransition, exitTransition, popEnterTransition, popExitTransition
- [View 显隐动画与页面转场按源时长顺序实现](../topics/ui/animation/transitions/lesson-76258c72cc6764d88db3.lesson.md) · 信号：startAnimation, ViewPropertyAnimator, setCustomAnimations, res/anim
- [进入无转场按目的地页定，未调用按主题动画](../topics/ui/animation/transitions/lesson-9886f489045488c8b454.lesson.md) · 信号：overridePendingTransition, windowAnimationStyle, activity_open_enter, pushPathByName

### [ui/dialog/carriers](../topics/ui/dialog/carriers/index.md) — 按源弹层类型选载体：真弹窗不以页面叠层或路由页充当、V2 页面的弹窗 API、锚定下拉与自定义内容。

- [V2 页面弹窗用浮层或 openCustomDialog](../topics/ui/dialog/carriers/lesson-3f3e1ff0a4d0e0299bda.lesson.md) · 信号：@ComponentV2, CustomDialogController, @CustomDialog, openCustomDialog
- [半透明卡片 Activity 迁 DIALOG 模式透明路由](../topics/ui/dialog/carriers/lesson-22c2a8f0e6b782b95448.lesson.md) · 信号：windowIsTranslucent, backgroundDimEnabled, windowBackground, NavDestinationMode.DIALOG
- [带 setView 或图标的对话框改用自定义弹窗](../topics/ui/dialog/carriers/lesson-18fca50f9c801cb282ec.lesson.md) · 信号：setView, AlertDialog.show, showAlertDialog, MaterialAlertDialogBuilder
- [当前页 show 的底部弹窗叠在宿主页上不改路由页](../topics/ui/dialog/carriers/lesson-7ef02de8bbc10734c3d2.lesson.md) · 信号：bottomDialog, BottomSheetDialog, HMRouter, Navigation
- [按源弹层类型选形态：底部面板才用 bindSheet](../topics/ui/dialog/carriers/lesson-21db515a505be4845497.lesson.md) · 信号：DialogHelper, CustomDialog, AlertDialog, BottomSheetDialog
- [真弹窗迁成系统弹窗或半模态，不用可见性叠层充当](../topics/ui/dialog/carriers/lesson-368c4592e4c7075c1871.lesson.md) · 信号：XPopup, CenterPopupView, AttachPopupView, BottomPopupView
- [锚定下拉与溢出菜单原位还原，不换 Select/Menu](../topics/ui/dialog/carriers/lesson-666a746081ba1e447322.lesson.md) · 信号：showAsDropDown, PopupWindow, bindPopup, Select
- [页内遮罩弹窗显示时背景移出无障碍树](../topics/ui/dialog/carriers/lesson-96eea0feeae116ef9262.lesson.md) · 信号：accessibilityLevel, no-hide-descendants, openCustomDialog, showAlertDialog

### [ui/dialog/content](../topics/ui/dialog/content/index.md) — 弹窗内容与行为的还原：按源布局逐控件重建、复用共享弹窗组件、打开触发点、展开后加载数据、下拉关闭的手势门禁。

- [ComponentContent 后赋的回调以闭包传入](../topics/ui/dialog/content/lesson-1c27b6c7cf05c05733d9.lesson.md) · 信号：ComponentContent, wrapBuilder, openCustomDialog, @Param
- [含列表的 bindSheet 按手势起点决定下拉关闭](../topics/ui/dialog/content/lesson-f35f4912277e0c9a1b14.lesson.md) · 信号：onWillDismiss, onWillSpringBackWhenDismiss, nestedScroll, SELF_FIRST
- [弹窗展开后才加载数据：先开弹层再内部异步加载带重试](../topics/ui/dialog/content/lesson-5f8833721d3c4a11c60a.lesson.md) · 信号：onExpanded, bindSheet
- [源弹窗按布局或库模板逐控件还原不用通用弹窗](../topics/ui/dialog/content/lesson-1f366fe4ccdc917ce0fc.lesson.md) · 信号：DialogXxxBinding.inflate, R.layout, android:hint, setContentView
- [源端委托共享弹窗时复用目标共享组件不留副本](../topics/ui/dialog/content/lesson-6d3ac9a5c0382377b91e.lesson.md) · 信号：XxxDialog.show, onAction, Dialog.show, DialogFragment
- [长按菜单按 onCreateContextMenu 移植](../topics/ui/dialog/content/lesson-9975dd1d15f5c73758e8.lesson.md) · 信号：registerForContextMenu, onCreateContextMenu, multi_select, android:visible
- [页内对话框可见性状态逐一接通打开触发点](../topics/ui/dialog/content/lesson-f0d5a447e645bc253019.lesson.md) · 信号：Modifier.clickable, @Local, @Builder, onClick

### [ui/dialog/frame](../topics/ui/dialog/frame/index.md) — 弹层外壳外观：宽度公式、遮罩、圆角底色、投影、箭头与档位按源主题或库取值

- [M3 警告框按主题代际取外观并设遮罩](../topics/ui/dialog/frame/lesson-39077e6612d5f97b0731.lesson.md) · 信号：MaterialAlertDialogBuilder, Theme.Material3, Theme.MaterialComponents, colorSurfaceContainerHigh
- [平台默认 AlertDialog 先从平台资源写可见契约](../topics/ui/dialog/frame/lesson-9c4de55af3c1ecd8eaa4.lesson.md) · 信号：AlertDialog.Builder, DialogPreference, ListPreference, EditTextPreference
- [库对话框窗宽遮罩按提供方取值，不写 100%](../topics/ui/dialog/frame/lesson-1bff1c90d9df6c9609ec.lesson.md) · 信号：material-dialogs, md_dialog_max_width, md_dialog_horizontal_margin, windowMinWidthMinor
- [底部面板按实际高度定档，显式关 showClose](../topics/ui/dialog/frame/lesson-df1f691759f84ba9e688.lesson.md) · 信号：BottomSheetDialogFragment, ModalBottomSheet, skipPartiallyExpanded, STATE_EXPANDED
- [气泡整体着色用 popupColor，不只给内容加背景](../topics/ui/dialog/frame/lesson-05dc4eb9548bf3fef6ae.lesson.md) · 信号：bindPopup, popupColor, backgroundBlurStyle, BlurStyle.NONE

### [ui/dialog/mounting](../topics/ui/dialog/mounting/index.md) — 弹窗挂载层级与宿主节点：sheet 之上、覆层挂整窗根、锚点所在页、SheetMode 与 targetId

- [sheet 内二级弹窗用全屏模态承载，自绘遮罩居中卡片](../topics/ui/dialog/mounting/lesson-009212ca2c691b97d76c.lesson.md) · 信号：bindSheet, bindContentCover, BottomSheetDialog, DialogFragment
- [依附式弹窗宿主按锚点视图所在页确定，按实测坐标定位](../topics/ui/dialog/mounting/lesson-29f62d177a17d08b4e4f.lesson.md) · 信号：AttachPopup, atView, componentUtils, Fragment
- [多个独立底部弹层不在同一节点链式 bindSheet](../topics/ui/dialog/mounting/lesson-b661a3a6a4c0a1e2a3c9.lesson.md) · 信号：bindSheet, @Local, BottomSheetDialog, SheetOptions
- [弹层内跳页的半模态用 EMBEDDED 挂宿主节点](../topics/ui/dialog/mounting/lesson-97bf3cf56f55715f7e42.lesson.md) · 信号：SheetMode.EMBEDDED, openBindSheet, targetId, showBindSheet
- [组件外开自定义弹窗用 ComponentContent 承载](../topics/ui/dialog/mounting/lesson-a3ac761b0d52a6bccb9f.lesson.md) · 信号：ComponentContent, wrapBuilder, openCustomDialog, closeCustomDialog
- [页内覆层挂覆盖整窗的宿主根，按钮行先定高再撑分隔线](../topics/ui/dialog/mounting/lesson-0a26e0cfc44a183d3a02.lesson.md) · 信号：Theme.Dialog, windowIsFloating, layout_height=match_parent, Stack

### [ui/graphics/canvas-text](../topics/ui/graphics/canvas-text/index.md) — Canvas 文字绘制：字体串与注册就绪、TextMetrics 度量字段选取、段落方向与基线取整

- [fillText 按串首强方向字符设 direction](../topics/ui/graphics/canvas-text/lesson-68717b80482f4bd12825.lesson.md) · 信号：Canvas.drawText, drawText, fillText, ctx.direction
- [字体串用注册名不加引号，测宽前等字体就绪](../topics/ui/graphics/canvas-text/lesson-74295d12b4edc025569f.lesson.md) · 信号：ctx.font, font.registerFont, registerFont, Typeface.createFromAsset
- [文字度量按源 API 分层选 TextMetrics 字段](../topics/ui/graphics/canvas-text/lesson-f876887b216b6caf9f39.lesson.md) · 信号：getTextBounds, Paint.ascent, getFontMetrics, measureText

### [ui/graphics/drawing](../topics/ui/graphics/drawing/index.md) — Canvas 自绘的移植：坐标原点共用、自适应公式的参照常量、共享绘制分支的统一规则与被注释绑定的静态化。

- [Adapter 注释掉的绑定按未启用，只按 XML 静态属性](../topics/ui/graphics/drawing/lesson-cd87ec49e06af8e6459a.lesson.md) · 信号：Adapter, onBindViewHolder, maxTop, minTop
- [反复 render 的画布每帧先清屏](../topics/ui/graphics/drawing/lesson-351ce34d3ebe51b8ff8e.lesson.md) · 信号：clearRect, onDraw, render(), CanvasRenderingContext2D
- [折线点与标签共用原点，点坐标含留白时不再加 position](../topics/ui/graphics/drawing/lesson-dca31bed776aaf7cb328.lesson.md) · 信号：valToY, ItemDecoration, Polyline, paddingTop
- [按 px 公式移植画布时主画布与离屏都用 PX 构造](../topics/ui/graphics/drawing/lesson-7083c6ad69ab19ad17dd.lesson.md) · 信号：LengthMetricsUnit.PX, CanvasRenderingContext2D, measureText, Paint.setTextSize
- [烘焙位图改每帧绘制时状态留快照、按比例缩放](../topics/ui/graphics/drawing/lesson-046c8bbb304684669060.lesson.md) · 信号：onSizeChanged, Bitmap, onDraw, setBounds
- [自绘红点按实际分支取尺寸，半径换直径](../topics/ui/graphics/drawing/lesson-99fe69fc59afa886750d.lesson.md) · 信号：BadgeView, setBadgeCount, drawCircle, Circle
- [自适应尺寸公式的参照基数写成独立常量不替换](../topics/ui/graphics/drawing/lesson-f395cbdf6742a7f4c761.lesson.md) · 信号：referenceCellHeight, contentHeight / 6, Canvas, onDraw
- [预缩放位图在 PixelMap 上按同一采样缩放](../topics/ui/graphics/drawing/lesson-c3bd9c8b2f24c209a659.lesson.md) · 信号：BitmapFactory.decodeResource, createScaledBitmap, drawBitmap, drawImage

### [ui/graphics/icons](../topics/ui/graphics/icons/index.md) — 图标资源的选取与显示：原图复制不以近名替代、固有 dp 与触摸盒分离、场景变体映射、动画矢量帧与 Lottie 接入。

- [Lottie 动画层接 @ohos/lottie 不换静态图](../topics/ui/graphics/icons/lesson-ea55fe23fea47c1cfca3.lesson.md) · 信号：LottieAnimationView, @ohos/lottie, setAnimation, oh-package.json5
- [Material 图标按同变体从可核来源取 pathData](../topics/ui/graphics/icons/lesson-74d535afb21b2270119e.lesson.md) · 信号：Icons.Rounded, Icons.AutoMirrored.Rounded, pathData, android.jar
- [animated-vector 按 atEnd 插值形变](../topics/ui/graphics/icons/lesson-e6b1f9094ec3b905cab5.lesson.md) · 信号：rememberAnimatedVectorPainter, AnimatedImageVector, animated-vector, atEnd
- [viewBox 取 viewport，宽高取 dp 尺寸](../topics/ui/graphics/icons/lesson-4e306a66aba5f1d76fdf.lesson.md) · 信号：VectorDrawable, viewBox, viewportWidth, viewportHeight
- [图标按资源固有 dp 显示，触摸盒放外层不设成盒尺寸](../topics/ui/graphics/icons/lesson-bdc493f5950835f9bfcc.lesson.md) · 信号：centerInside, ImageFit.Contain, wrap_content, drawableLeft
- [图标用源端原图，缺失从 drawable 密度目录复制不替代](../topics/ui/graphics/icons/lesson-943544ce27bf04f9faf8.lesson.md) · 信号：does not have a base resource, drawable-xxhdpi, SymbolGlyph, $r('app.media
- [编码到资源的多变体映射按取值字段拆分不合一](../topics/ui/graphics/icons/lesson-c65e8e59008a5e31bcad.lesson.md) · 信号：iconEx, bgEx, icon2Ex, setBackgroundResource

### [ui/graphics/images](../topics/ui/graphics/images/index.md) — 背景图与图片组件的缩放、形状裁剪与分层落地：layer-list 逐层、整屏位图拉伸、自定义图片组件与兜底预览。

- [layer-list 背景按生效 flavor 逐层落组件](../topics/ui/graphics/images/lesson-0da8733ee0a6c52924da.lesson.md) · 信号：layer-list, sourceSet, ImageFit.Fill, $r
- [整屏背景位图用 ImageFit.Fill 不默认裁切](../topics/ui/graphics/images/lesson-7708f650eb4b55dce045.lesson.md) · 信号：android:background, ImageFit.Fill, ImageFit.Cover, scaleType
- [无来源兜底预览不加源端没有的边框选中态装饰](../topics/ui/graphics/images/lesson-c8909c3cb5f925913407.lesson.md) · 信号：borderWidth, FrameLayout, placeholder
- [自定义图片组件先读定义：圆形裁剪译 Cover 加圆角](../topics/ui/graphics/images/lesson-9dcd69d2824702310959.lesson.md) · 信号：CircleShape, ContentScale.Crop, ImageFit.Cover, borderRadius

### [ui/interaction/app-bar](../topics/ui/interaction/app-bar/index.md) — 工具栏导航图标与菜单项：按实际生效者定汉堡或 Up，showAsAction 分流图标位与溢出

- [导航图标按生效者画，菜单按 showAsAction 分流](../topics/ui/interaction/app-bar/lesson-a6121cc7eaf207b702f7.lesson.md) · 信号：ActionBarDrawerToggle, syncState, parentActivityName, setDisplayHomeAsUpEnabled

### [ui/interaction/click-binding](../topics/ui/interaction/click-binding/index.md) — 点击绑定的归属与副作用：挂在源端真正持有点击的节点、按处理器分支迁副作用、回调契约兑现、被注释的监听视为死按钮。

- [onClick 挂在源端真正持有点击的节点，整栏或子控件](../topics/ui/interaction/click-binding/lesson-fd3add7128663eb9998f.lesson.md) · 信号：setOnClickListener, onClick, LinearLayout, DataBinding
- [两态按钮图标写成 if/else 或单 Image 选资源](../topics/ui/interaction/click-binding/lesson-ed5556325b6d8f510e2f.lesson.md) · 信号：Button, Image, setImageResource, ImageButton
- [带点击绑定控件按源处理器分支逐项迁移副作用](../topics/ui/interaction/click-binding/lesson-55e33a0621c3008ab8b3.lesson.md) · 信号：android:onClick, setChecked, postDelayed, ohos.permission.VIBRATE
- [接入专页时逐项兑现 @Event 回调契约不用空值短路](../topics/ui/interaction/click-binding/lesson-c061106fa1d809e518da.lesson.md) · 信号：@Event, requestPhotoEditorSession, dragEnable, cropEnable
- [改共享组件加默认原行为的入参并接全部宿主](../topics/ui/interaction/click-binding/lesson-67e0a326dea085296fb9.lesson.md) · 信号：GONE, @Event, @Param
- [监听回调体被注释时按无响应控件迁移，审计不放行](../topics/ui/interaction/click-binding/lesson-f3e614f295aa409485fd.lesson.md) · 信号：setOnClickListener, android:clickable, onClick, TODO

### [ui/interaction/focus-ime](../topics/ui/interaction/focus-ime/index.md) — 焦点链与输入法：按键事件挂载点、可获焦组件、软键盘收放 API、首屏获焦时机与搜索框状态

- [Activity onKeyDown 挂页根，页内需可获焦](../topics/ui/interaction/focus-ime/lesson-80e1d2c095a3698a7156.lesson.md) · 信号：onKeyDown, dispatchKeyEvent, onKeyEvent, NavDestination
- [SearchView 展开焦点提交收起分开建模](../topics/ui/interaction/focus-ime/lesson-4995a3977dc8bc7fa696.lesson.md) · 信号：SearchView, actionView, expandActionView, collapseActionView
- [收键盘用 hideTextInput，焦点绑 onFocus](../topics/ui/interaction/focus-ime/lesson-99da84bf5c70367eb3df.lesson.md) · 信号：hideTextInput, showTextInput, hideSoftKeyboard, showSoftKeyboard
- [根快捷键只处理根上收过按下的抬起](../topics/ui/interaction/focus-ime/lesson-a10cde3d336eee4eebe7.lesson.md) · 信号：onKeyUp, onKeyEvent, KeyType.Up, KeyType.Down
- [首屏输入框待窗口获焦后再 requestFocus](../topics/ui/interaction/focus-ime/lesson-9d42548ee3c075de3330.lesson.md) · 信号：requestFocus, window.findWindow, isFocused, WINDOW_ACTIVE

### [ui/interaction/gestures](../topics/ui/interaction/gestures/index.md) — 触摸与手势移植：逐指派发过滤、自写状态机阈值、识别器默认参数、系统拖拽与长按触感

- [onTouch 逐指派发按源端接收方式过滤](../topics/ui/interaction/gestures/lesson-68023ac5f088c72a775a.lesson.md) · 信号：onTouch, getAction, getActionMasked, ACTION_POINTER_DOWN
- [手势起点 Image 写 draggable(false)](../topics/ui/interaction/gestures/lesson-b30da57443f68ab9046a.lesson.md) · 信号：.draggable(false), Image, onTouch, PanGesture
- [自写触摸状态机按源阈值复刻，不换识别器](../topics/ui/interaction/gestures/lesson-b9f5cb5d3ae174e5bf70.lesson.md) · 信号：onTouch, dispatchTouchEvent, ItemTouchHelper, ScaleGestureDetector
- [长按手势显式补系统长按触感](../topics/ui/interaction/gestures/lesson-8a752faf9f5dff52e3ff.lesson.md) · 信号：combinedClickable, onLongClick, hapticFeedbackEnabled, LongPressGesture

### [ui/interaction/hit-testing](../topics/ui/interaction/hit-testing/index.md) — 叠放层的命中测试与手势归属：全尺寸覆盖层透传、Block 只放遮罩、侧滑行按钮热区、滑删方向与触发瞬间的坐标取值。

- [Block 只放无子控件的遮罩层，面板根容器 Default](../topics/ui/interaction/hit-testing/lesson-cf018b76af68b4c00895.lesson.md) · 信号：HitTestMode.Block, hitTestBehavior, HitTestMode.Default, showCustomDialog
- [SwipeToDismissBox 方向按手势与偏移符号写明](../topics/ui/interaction/hit-testing/lesson-7f5eba1b969bddfb34dc.lesson.md) · 信号：SwipeToDismissBox, enableDismissFromStartToEnd, EndToStart, StartToEnd
- [不处理点击的全尺寸覆盖层显式设 Transparent 命中](../topics/ui/interaction/hit-testing/lesson-4a4f8d845a204ffa244b.lesson.md) · 信号：hitTestBehavior, HitTestMode.Transparent, HitTestMode.None, FrameLayout
- [吞触摸的叠放层显式 Block，空 onClick 不挡](../topics/ui/interaction/hit-testing/lesson-df573635678a799a5f80.lesson.md) · 信号：HitTestMode.Block, HitTestMode.BLOCK_HIERARCHY, HitTestMode.Transparent, HitTestMode.None
- [锚点坐标在点击回调即时取，onAreaChange 只兜底](../topics/ui/interaction/hit-testing/lesson-963bf871aa4e910a8fc8.lesson.md) · 信号：getLocationInWindow, onAreaChange, GestureEvent.fingerList, globalX

### [ui/interaction/input](../topics/ui/interaction/input/index.md) — EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

- [TextInput 关默认装饰，按主题状态背景复刻](../topics/ui/interaction/input/lesson-1150c0c721e6dc0dede4.lesson.md) · 信号：showPasswordIcon, InputType.Password, cancelButton, textPassword
- [inputType 只映射键盘，有 digits 才过滤](../topics/ui/interaction/input/lesson-0457a04c31208e1fb916.lesson.md) · 信号：inputType, textCapCharacters, textNoSuggestions, numberSigned
- [setError 迁尾部图标加聚焦气泡、改动即清](../topics/ui/interaction/input/lesson-f7edea01f8308bf563ef.lesson.md) · 信号：setError, TextInputLayout, showError, errorMessage
- [可编辑且分段着色用 RichEditor 承载](../topics/ui/interaction/input/lesson-ef93bb2086aef9604aa1.lesson.md) · 信号：RichEditor, addTextSpan, EditText, Spannable
- [平台正则按定义逐段移植并全串匹配](../topics/ui/interaction/input/lesson-90e0f1db3e1e13a6fd6a.lesson.md) · 信号：Patterns.WEB_URL, Patterns.EMAIL_ADDRESS, String.matches, (?i)
- [拒绝输入用 maxLength 或 onWillChange](../topics/ui/interaction/input/lesson-617ffbd840398cf95efc.lesson.md) · 信号：maxLength, onValueChange, onChange, onWillChange
- [透明 TextInput 铺满掩码格并获焦，多段各独立节点](../topics/ui/interaction/input/lesson-90a7888a65eefb3e94b3.lesson.md) · 信号：requestFocus, onAppear, TextInput, Stack
- [金额含小数时不用 InputType.Number](../topics/ui/interaction/input/lesson-a5aeed3d4c376cd085d1.lesson.md) · 信号：InputType.Number, InputType.NUMBER_DECIMAL, toDoubleOrNull, numberDecimal

### [ui/interaction/press-states](../topics/ui/interaction/press-states/index.md) — 可点击控件的按压与禁用态外观：隐式按压反馈补齐、禁用外观来源与点击拦截

- [可点击容器用 stateStyles 补按压态](../topics/ui/interaction/press-states/lesson-fde79829831c2269e925.lesson.md) · 信号：stateStyles, stateEffect, combinedClickable, Card(onClick
- [源禁用只换背景时不用 .enabled(false)](../topics/ui/interaction/press-states/lesson-99080bd3bfc1bcbb9c5f.lesson.md) · 信号：setEnabled, android:enabled, .enabled(false), state_enabled

### [ui/interaction/selectors](../topics/ui/interaction/selectors/index.md) — 选择控件的选项、初值与选中标记：选项按源数据源、自定义属性初值、级联回填、条件勾选不换 Radio、Slider 步数。

- [Slider steps 翻步长：区间/(steps+1)](../topics/ui/interaction/selectors/lesson-d715fa78ada2e79a5fd2.lesson.md) · 信号：Slider, valueRange, Float.toString, toFixed
- [Switch thumbContent 无对应参数时自绘](../topics/ui/interaction/selectors/lesson-c3a3797da8b412c31aa7.lesson.md) · 信号：thumbContent, Switch, Toggle, ToggleType.Switch
- [selectable 行条件勾选按原结构实现不换 Radio](../topics/ui/interaction/selectors/lesson-d53223f43ad454261f26.lesson.md) · 信号：Modifier.selectable, ic_check, Radio, RadioButton
- [自定义 View 的 XML 属性只在被读取时生效](../topics/ui/interaction/selectors/lesson-a6edef3bb44e01a82b72.lesson.md) · 信号：android:checked, styleable, obtainStyledAttributes, setChecked
- [选择器回填的省市区多级值实现选择流程一次写回](../topics/ui/interaction/selectors/lesson-b845647090bfeac053ed.lesson.md) · 信号：TextPicker, TextInput, readOnly, focusable
- [选项列表按源 ViewModel 数据源迁移，截图只核外观](../topics/ui/interaction/selectors/lesson-60c1c37b0703e5d3b8d6.lesson.md) · 信号：RecyclerView, Fragment, ViewModel, data-binding

### [ui/layout/constraints](../topics/ui/layout/constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。

- [ConstraintLayout 转顺序流前先列出各子项锚点](../topics/ui/layout/constraints/lesson-3fe0026df9abc72ff788.lesson.md) · 信号：constraintBottom_toBottomOf, constraintBottom_toTopOf, dimensionRatio, layoutWeight
- [RelativeLayout gravity 平移整组子项](../topics/ui/layout/constraints/lesson-c7eccff80bac02281029.lesson.md) · 信号：RelativeLayout, android:gravity, center_vertical, alignParentTop
- [Stack 子项 .align() 无效，对齐用满高容器](../topics/ui/layout/constraints/lesson-92aee54a305ea0bde363.lesson.md) · 信号：.align(, alignContent, Alignment.TopStart, layout_gravity
- [单视图居中加兄弟悬挂用 RelativeContainer](../topics/ui/layout/constraints/lesson-e607a28fcd91acd2b40f.lesson.md) · 信号：RelativeContainer, alignRules, __container__, constraintTop_toBottomOf
- [基线对齐用 Row 居中近似，内距逐行复制，标签靠右对齐](../topics/ui/layout/constraints/lesson-c4990fef246323ffda03.lesson.md) · 信号：alignBy(LastBaseline), wrapContentWidth(End), weight(1), layoutWeight
- [纵向容器默认起始对齐与贴顶在目标显式写出](../topics/ui/layout/constraints/lesson-08b9064f678f1635e647.lesson.md) · 信号：alignItems(HorizontalAlign.Start), alignItems(VerticalAlign.Top), Alignment.Top, constraintSize

### [ui/layout/immersion](../topics/ui/layout/immersion/index.md) — 安全区沉浸：是否全屏、系统栏底色与避让带由哪一层承担

- [Tab 宿主不统一加顶部安全区，按子页源处理分别避让](../topics/ui/layout/immersion/lesson-48e9408812c28e934db8.lesson.md) · 信号：ImmersionBar, statusBarView, titleBarMarginTop, fitsSystemWindows
- [expandSafeArea 非避让，前景按避让区补内距](../topics/ui/layout/immersion/lesson-a8452bfea5d42d3dcae3.lesson.md) · 信号：expandSafeArea, setWindowLayoutFullScreen, getWindowAvoidArea, TYPE_SYSTEM
- [根视图状态栏 padding 与底色由页面容器承担](../topics/ui/layout/immersion/lesson-baf0ca22a69e7b76f636.lesson.md) · 信号：setPadding, DecorView, setBackgroundColor, statusBarColor
- [源窗口延伸到系统栏下才全屏，底部避让加在屏底层](../topics/ui/layout/immersion/lesson-0e1c846868f2683cc280.lesson.md) · 信号：getWindowAvoidArea, TYPE_NAVIGATION_INDICATOR, TYPE_SYSTEM, bottomRect
- [状态栏实色带挂外层 Column，把 Tabs 包进该层](../topics/ui/layout/immersion/lesson-fe10bd2491ca4ba82cb5.lesson.md) · 信号：Tabs, TabContent, Column, Swiper

### [ui/layout/insets](../topics/ui/layout/insets/index.md) — 系统栏与软键盘避让值的取值、单位与只消费一次

- [innerPadding 顶部即状态栏高，目标只在一处避让](../topics/ui/layout/insets/lesson-f64afc22d41b130f1628.lesson.md) · 信号：Scaffold, innerPadding, consumeWindowInsets, contentWindowInsets
- [下发状态栏高度参数需写明消费层，Stack 各层同基准](../topics/ui/layout/insets/lesson-2cf2614847a8dba832b3.lesson.md) · 信号：Stack, @Param, windowTopPadding, statusBarHeight
- [标题栏接 topInset 前判定源端避让方，内距只取一份](../topics/ui/layout/insets/lesson-cde4120ab9ad7412b1da.lesson.md) · 信号：fitsSystemWindows, topInset, paddingTop, .height()
- [源 adjustResize 时键盘避让设 RESIZE](../topics/ui/layout/insets/lesson-f86b02e97cc77e31d51a.lesson.md) · 信号：adjustResize, windowSoftInputMode, imePadding, KeyboardAvoidMode.RESIZE
- [路由页先核内容原点，已在 inset 下只补源顶距余量](../topics/ui/layout/insets/lesson-c7ee1769ca29abd236d3.lesson.md) · 信号：NavDestination, HMRouter, expandSafeArea, SafeAreaType.SYSTEM
- [避让区与窗口尺寸是 px，写入窗口模型前先 px2vp](../topics/ui/layout/insets/lesson-cf111aadb8804649b578.lesson.md) · 信号：getWindowAvoidArea, px2vp, windowRect, getWindowProperties
- [页面读避让值用主窗口，不用 getLastWindow](../topics/ui/layout/insets/lesson-8e0e9fe5373a2bbe47af.lesson.md) · 信号：getLastWindow, getMainWindowSync, getMainWindow, avoidAreaChange

### [ui/layout/intrinsic](../topics/ui/layout/intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。

- [IntrinsicSize.Min 行先算固有高度写显式值](../topics/ui/layout/intrinsic/lesson-cb1a12afca61db08ed9a.lesson.md) · 信号：IntrinsicSize.Min, fillMaxHeight, align(Top), padding(top)
- [Material 按钮区分布局占位、背景实绘与触控范围](../topics/ui/layout/intrinsic/lesson-b73a1ac8908f74856a02.lesson.md) · 信号：minimumInteractiveComponentSize, IconButton, Surface, Box
- [TableLayout 列宽取各列自然宽最大值不等分](../topics/ui/layout/intrinsic/lesson-6cb9ad45093ce2ca28af.lesson.md) · 信号：TableLayout, TableRow, stretchColumns, shrinkColumns
- [内容定尺寸的父级里不写 100%，描边画在自身](../topics/ui/layout/intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md) · 信号：matchContentSize, fillMaxSize, Modifier.border, HitTestMode.None
- [图片盒尺寸与盒内缩放分开，高度用位图像素比](../topics/ui/layout/intrinsic/lesson-624248be2c5f81082268.lesson.md) · 信号：adjustViewBounds, layout_constrainedWidth, aspectRatio, constraintSize
- [实测宽落在框架最小值时写 constraintSize](../topics/ui/layout/intrinsic/lesson-42364ad323112c3342ae.lesson.md) · 信号：constraintSize, minWidth, maxWidth, AppCompat
- [并排图片列按固有宽比例分列高度用 aspectRatio](../topics/ui/layout/intrinsic/lesson-0618cdf331560d389f0e.lesson.md) · 信号：aspectRatio, wrap_content, Blank().layoutWeight(1), layoutWeight
- [步进器居中子项组不给中间项 layoutWeight(1)](../topics/ui/layout/intrinsic/lesson-02b2fcd7d157d97f95c8.lesson.md) · 信号：gravity=center, FlexAlign.Center, wrap_content, justifyContent
- [跨列卡片同行等高按列宽留边推 aspectRatio](../topics/ui/layout/intrinsic/lesson-4fc212d401ac7b2a4218.lesson.md) · 信号：aspectRatio, onAreaChange, GridItem, Grid

### [ui/layout/layers](../topics/ui/layout/layers/index.md) — 页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。

- [RelativeLayout 无规则子项放同一 Stack](../topics/ui/layout/layers/lesson-7dcf2d92c689c96c190b.lesson.md) · 信号：RelativeLayout, layout_below, layout_above, layout_toEndOf
- [addView 挂根部的视图放 Stack 最底层铺满](../topics/ui/layout/layers/lesson-c3dcc5a25a0ad59c53c1.lesson.md) · 信号：addView, removeView, LayoutParams, Stack
- [只构造未绘制的底层按构造态显示，不套隐藏分支](../topics/ui/layout/layers/lesson-1e279118c32645022ac2.lesson.md) · 信号：addView, setVisibility, INVISIBLE, VISIBLE
- [底栏之上的 BottomSheet 面板用布局内 Stack](../topics/ui/layout/layers/lesson-9f45b5d79206b5654aff.lesson.md) · 信号：BottomSheetBehavior, STATE_COLLAPSED, HIDDEN, CoordinatorLayout
- [接线已转换页保留全屏底层加状态前景层骨架](../topics/ui/layout/layers/lesson-4de4283ec625be7e976c.lesson.md) · 信号：FEATURE_NO_TITLE, MapView, showRoute, tabData
- [新增可选背景层时上层不透明内容透明或合成](../topics/ui/layout/layers/lesson-cba11443f9a59fdaf4f7.lesson.md) · 信号：BlendMode.DARKEN, blendMode, ImageFit.Contain, Drawable
- [源 XML 的 gone 节点不渲染，固定尺寸点击容器作热区](../topics/ui/layout/layers/lesson-f1a98587fe72ff68c5a8.lesson.md) · 信号：tools:listitem, visibility="gone", setVisibility, findViewById

### [ui/layout/scrolling](../topics/ui/layout/scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。

- [Lazy 首尾留白用 contentStartOffset](../topics/ui/layout/scrolling/lesson-4030f978a230df37de2b.lesson.md) · 信号：contentStartOffset, contentEndOffset, contentPadding, PaddingValues
- [LazyRow 转可横滑容器，不降成普通 Row](../topics/ui/layout/scrolling/lesson-caa043fb95ff63e321e2.lesson.md) · 信号：LazyRow, horizontalArrangement, Arrangement.SpaceEvenly, AnimatedVisibility
- [scrollToItem 映射为起始对齐不居中](../topics/ui/layout/scrolling/lesson-f0a40d990c62738fc04e.lesson.md) · 信号：scrollToItem, animateScrollToItem, LazyListState, scrollToIndex
- [只把源滚动区子节点放进 Scroll，固定头部留外面](../topics/ui/layout/scrolling/lesson-46a0d7f239efac925d33.lesson.md) · 信号：NestedScrollView, layout_below, layout_weight, layoutWeight(1)
- [嵌套滚动的 Web 高度跟文档，并锁 H5 自身滚动](../topics/ui/layout/scrolling/lesson-fd2dd522fdb03b3e5385.lesson.md) · 信号：wrap_content, nestedScroll, PARENT_FIRST, onPageEnd
- [并排卡等高用 onSizeChange 实测高度传递](../topics/ui/layout/scrolling/lesson-8334433bea644f2a89ae.lesson.md) · 信号：onSizeChange, SizeOptions, NestedScrollView, match_parent
- [折叠顶栏按滚动偏移算 fraction 插值不两态切换](../topics/ui/layout/scrolling/lesson-67ab02abe6ec76f4129e.lesson.md) · 信号：exitUntilCollapsedScrollBehavior, LargeTopAppBar, collapsedFraction, onDidScroll
- [拆卡片时 heightIn 上限挂在 Scroll 上](../topics/ui/layout/scrolling/lesson-420023d472f48bed8ef9.lesson.md) · 信号：heightIn, verticalScroll, constraintSize, maxHeight
- [未写 overScrollMode 时只在可滚时回弹](../topics/ui/layout/scrolling/lesson-80dd4e626e1c207028e6.lesson.md) · 信号：overScrollMode, IF_CONTENT_SCROLLS, EdgeEffect.Spring, alwaysEnabled
- [横向滚动容器交叉轴高度写数值不写 auto](../topics/ui/layout/scrolling/lesson-2d7c6de68f604ae77caf.lesson.md) · 信号：ScrollDirection.Horizontal, horizontalScroll, LazyRow, ScrollableTabRow

### [ui/layout/sizing](../topics/ui/layout/sizing/index.md) — 满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。

- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](../topics/ui/layout/sizing/lesson-45f77b3088fa69398f9e.lesson.md) · 信号：fillMaxWidth, requiredWidth, Visibility.Hidden, layoutWeight(1)
- [fragment 根 padding 只由宿主或组件一方实现](../topics/ui/layout/sizing/lesson-8a7d25959b954ffb9215.lesson.md) · 信号：LinearLayout, TabContent, ViewPager
- [weightSum 与权重和不等时按源算法分余量](../topics/ui/layout/sizing/lesson-adad817f2c3c8f1eaa09.lesson.md) · 信号：weightSum, layout_weight, layoutWeight, flexGrow
- [定宽兄弟后的多行 Text 加 flexShrink(1)](../topics/ui/layout/sizing/lesson-8566839cffc9e9e7fa30.lesson.md) · 信号：flexShrink(1), layoutWeight(1), layout-land, wrap_content
- [带同轴 margin 的 100% 改容器 padding](../topics/ui/layout/sizing/lesson-75f4743dff663f50966b.lesson.md) · 信号：layout_marginHorizontal, showAsDropDown, PopupWindow, calc(100%
- [整数 px 公式在 px 域取整再 px2vp 写入属性](../topics/ui/layout/sizing/lesson-0ef2cd00e1a91491b350.lesson.md) · 信号：px2vp, vp2px, measureText, onAreaChange
- [方向边距用 end 时各边统一 LengthMetrics](../topics/ui/layout/sizing/lesson-e3077bf60cfc3f34d0a2.lesson.md) · 信号：LengthMetrics, layout_marginStart, layout_marginEnd, @kit.ArkUI
- [权重槽可能小于 padding 时不放在 Image 上](../topics/ui/layout/sizing/lesson-8c5e3ea6e2c4ff7e8478.lesson.md) · 信号：layout_weight, ImageView, FIT_CENTER, layoutWeight
- [槽位子项搬进 Row 改等分权重，不留 100%](../topics/ui/layout/sizing/lesson-c572346f0be19acf5579.lesson.md) · 信号：layoutWeight(1), width('100%'), BarMode.Fixed, LayoutParams
- [移进 Refresh 的内容根节点改用显式高度居中](../topics/ui/layout/sizing/lesson-1c3d6367be48f70bb001.lesson.md) · 信号：@BuilderParam, Refresh, layoutWeight(1), height('100%')
- [背景之前的 padding 放外层，背景圆角裁剪放内层](../topics/ui/layout/sizing/lesson-5c6217b05bb4c266f254.lesson.md) · 信号：statusBarsPadding, navigationBarsPadding, Surface, borderRadius
- [随选中进度收放的间距按同一选中条件归零](../topics/ui/layout/sizing/lesson-c39245065cc26d8c9f64.lesson.md) · 信号：animationProgress, constraintSize, Layout

### [ui/layout/variants](../topics/ui/layout/variants/index.md) — 布局方向与限定词变体：supportsRtl、land、swNdp 按窗口条件分支

- [声明 RTL 时保留 start/end 并镜像图标](../topics/ui/layout/variants/lesson-786a04847bf10d364d9d.lesson.md) · 信号：android:supportsRtl, LengthMetrics, marginStart, paddingStart
- [布局变体逐控件对照，按窗口条件分支](../topics/ui/layout/variants/lesson-c8e645a542254d96997e.lesson.md) · 信号：layout-land, layout-sw600dp, setBackgroundResource, layout_sources
- [未声明 supportsRtl 时有序容器逐个设 Ltr](../topics/ui/layout/variants/lesson-148a3e67bd557bafd722.lesson.md) · 信号：android:supportsRtl, Direction.Ltr, Direction.Auto, .direction(

### [ui/libraries](../topics/ui/libraries/index.md) — 三方 UI 库承载的界面：取库工件核对几何、手势与算法后再定目标映射

- [三方 UI 库先取 AAR 核几何行为再定映射](../topics/ui/libraries/lesson-f79082832a2fb18c8754.lesson.md) · 信号：build.gradle, AppIntro2, SublimePicker, FloatingActionsMenu

### [ui/list/behaviors](../topics/ui/list/behaviors/index.md) — 列表容器行为：侧栏与分组列表的滚动联动、组头默认展开、Repeat 虚拟滚动的项高度核对、swipeAction 挂载。

- [分类页右侧用 Scroller 列表双向联动迁滚动保护](../topics/ui/list/behaviors/lesson-7723af3766fb843a2577.lesson.md) · 信号：scrollToIndex, onScrollIndex, Scroller, LazyListState
- [改用 Repeat 虚拟化前逐列表核对项高度来源](../topics/ui/list/behaviors/lesson-150e48577e599f64ee23.lesson.md) · 信号：virtualScroll, Repeat, LazyForEach, alignSelf(Stretch)
- [无组点击监听时组头仍默认切换展开状态](../topics/ui/list/behaviors/lesson-e01c6f821d631fad5383.lesson.md) · 信号：ExpandableListView, BaseExpandableListAdapter, setOnGroupClickListener, expandGroup
- [滑动操作挂在 ListItem 节点而非行 Builder](../topics/ui/list/behaviors/lesson-feaf8a4a916a022b13a1.lesson.md) · 信号：swipeAction, ItemTouchHelper, SwipeActions, ListItem

### [ui/list/data-sources](../topics/ui/list/data-sources/index.md) — 列表数据源的绑定与并发：各列表各自的数据与排序器、本地变换随列表迁移、分页门闩、代次保护与行内在途锁。

- [LazyForEach 换数据不换源对象，通知重载](../topics/ui/list/data-sources/lesson-40efd2d02a5ea9554a95.lesson.md) · 信号：LazyForEach, IDataSource, DataChangeListener, onDataReloaded
- [onReachEnd 分页加载中不重入、刷新中不派发](../topics/ui/list/data-sources/lesson-0a398b212a8a80bd0c7f.lesson.md) · 信号：SmartRefreshLayout, onReachEnd, onRefreshing, setOnLoadMoreListener
- [onRefreshing 先判刷新已在运行再发起](../topics/ui/list/data-sources/lesson-fa79c5a6658c68b71a21.lesson.md) · 信号：Refresh, onRefreshing, SwipeRefreshLayout, setOnRefreshListener
- [多个 Adapter 列表各绑各自数据源并实现级联推进回退](../topics/ui/list/data-sources/lesson-b6146f290e871c82e61d.lesson.md) · 信号：onPClick, onCClick, onBack, RecyclerView
- [批量异步修补按列表代次丢弃过期结果按 ID 修补](../topics/ui/list/data-sources/lesson-4cfd4cbcecfb3de96037.lesson.md) · 信号：requestSerial, onReachEnd, Promise
- [新列表排序找源端该列表自己的排序器不复用他表](../topics/ui/list/data-sources/lesson-eb59181d6dfaeb014aef.lesson.md) · 信号：Comparator, sortedWith, compareBy, Repository
- [迁移列表连同条目点击与本地 shuffled 变换一起实现](../topics/ui/list/data-sources/lesson-46307bc26d725b4634ca.lesson.md) · 信号：addOnItemTouchListener, Fisher-Yates, RecyclerView, Adapter

### [ui/list/items](../topics/ui/list/items/index.md) — 条目类型与渲染分支：多 viewType 卡片外观、绑定代码里的区块与模板、跨列占位、副行回退、配置驱动分派。

- [多类型卡片外观按各类 holder 取，不共用一套](../topics/ui/list/items/lesson-9de4c7648d23db5d7f86.lesson.md) · 信号：cardCornerRadius, viewType, ViewHolder, CardView
- [恒空占位不在多列 Grid 生成通栏 GridItem](../topics/ui/list/items/lesson-2bd2620e5d1ef4bb17b4.lesson.md) · 信号：spanSizeLookup, GridLayoutManager, GridItem, WaterFlow
- [按全部 item 布局与 handleXxx 分支建页面区块](../topics/ui/list/items/lesson-e17b45a28a8d92ecbd01.lesson.md) · 信号：addItemType, handleXxx, onCreateViewHolder, SwipeRefreshLayout
- [新增副行显示字段后主行空值不再回退该字段](../topics/ui/list/items/lesson-b202de11960c156829b5.lesson.md) · 信号：BluetoothDevice, getName(), getAddress(), deviceName
- [配置驱动编辑项按源工厂表逐 type 分派专页](../topics/ui/list/items/lesson-71f8a80418dbc2c442ce.lesson.md) · 信号：editorConfig, textColor, Fragment

### [ui/list/pager](../topics/ui/list/pager/index.md) — ViewPager 到 Swiper：页数与禁滑方式、初始页用 index 绑定、自绘 tab 双向联动与日历翻页容器

- [ViewPager 定页阈值与归位时长按其规则落实](../topics/ui/list/pager/lesson-fc05d6dfe9844a88815b.lesson.md) · 信号：ViewPager, Swiper, determineTargetPage, smoothScrollTo
- [分页日历相邻页并发查询，Swiper 落定后一次提交](../topics/ui/list/pager/lesson-85b33ff729ab0514a20a.lesson.md) · 信号：Swiper, Canvas, onAnimationEnd, onGestureSwipe
- [初始页用 Swiper.index，非 onReady 切页](../topics/ui/list/pager/lesson-ccccf83dc93ae809ccfb.lesson.md) · 信号：Swiper.index, changeIndex, onReady, SwiperController
- [单页不用 Swiper；禁滑用 disableSwipe](../topics/ui/list/pager/lesson-540747e352d7f006016d.lesson.md) · 信号：ViewPager2, disableSwipe, isUserInputEnabled, Swiper
- [自绘 tab 加 Swiper 双向联动分别接通](../topics/ui/list/pager/lesson-27aa2e80a3a4d7724450.lesson.md) · 信号：ViewPager2, onPageSelected, setCurrentItem, currentItem
- [自绘日历翻页用 Swiper 承载，每页一 Canvas](../topics/ui/list/pager/lesson-d4e63d27885d9e348723.lesson.md) · 信号：Swiper, Canvas, PanGesture, ViewPager2

### [ui/navigation/back-stack](../topics/ui/navigation/back-stack/index.md) — 返回键与栈变更：覆盖层逐层关闭、按启动来源的返回分支、子组件拦截返回、清栈重建与重复导航的净效果。

- [Fragment 事务与 finish 逐分支映射栈操作](../topics/ui/navigation/back-stack/lesson-9a113ce21ae30365ea5b.lesson.md) · 信号：popBackStackImmediate, addToBackStack, popBackStack, finish()
- [handleDeepLink 深链清栈合成起始页加目标](../topics/ui/navigation/back-stack/lesson-69229aa8c7b051229f26.lesson.md) · 信号：handleDeepLink, navDeepLink, uriPattern, FLAG_ACTIVITY_NEW_TASK
- [tab、深链与桌面重进的返回栈后果写验收并实现](../topics/ui/navigation/back-stack/lesson-39f137ee173e50363f79.lesson.md) · 信号：popUpTo, saveState, restoreState, launchSingleTop
- [同一成功多条导航响应只保留一个导航出口](../topics/ui/navigation/back-stack/lesson-683d8f5070802c518020.lesson.md) · 信号：FLAG_ACTIVITY_NEW_TASK, finish(), startActivity, NavPathStack
- [回根重建返回栈用 clear() 不用 pop()](../topics/ui/navigation/back-stack/lesson-96c890012b26b5cb32cd.lesson.md) · 信号：popUpTo, navPathStack.clear(), pop(), NavPathStack
- [子组件拦截返回由 @Entry 转调，多方后进先出](../topics/ui/navigation/back-stack/lesson-803ba029eea852122e77.lesson.md) · 信号：PredictiveBackHandler, BackHandler, onBackPress, @Event
- [宿主 onBackPressed 自顶向下关闭页内覆盖层](../topics/ui/navigation/back-stack/lesson-396d54479492828eeea3.lesson.md) · 信号：onBackPressed, onDismissRequest, BackHandler, ModalBottomSheet
- [栈底 NavDestination 返回退后台不出栈](../topics/ui/navigation/back-stack/lesson-efff93743d668b55b55a.lesson.md) · 信号：onBackPressed, moveAbilityToBackground, terminateSelf, onBackPress
- [父栈跳转按 Manifest 父链 clear 后重建](../topics/ui/navigation/back-stack/lesson-2986423250986124d039.lesson.md) · 信号：TaskStackBuilder, addNextIntentWithParentStack, startActivities, parentActivityName
- [返回按钮与系统返回共用分支按来源标志处理不默认 pop](../topics/ui/navigation/back-stack/lesson-f19632971e470d55c543.lesson.md) · 信号：isFromSplash, onBackPressed, pop(), NavDestination

### [ui/navigation/handoff](../topics/ui/navigation/handoff/index.md) — 跳转动作随行的交接：点击出口落实际跳转、跳前写入的共享状态、结果回传写回、同窗口 push 的方向切换与恢复。

- [副作用导航逐出口在 onClick 落实际跳转与参数](../topics/ui/navigation/handoff/lesson-32af50a1dfb0c1c254af.lesson.md) · 信号：findNavController().navigate, bundleOf, OpenTripDetail, onClick
- [带回调选择器改路由打开时同一改动接通结果回传](../topics/ui/navigation/handoff/lesson-14509c64bd43100ce443.lesson.md) · 信号：DialogFragment, onPop, pushPathByName, show(
- [横屏可触发的 push 先切目标页方向返回后恢复](../topics/ui/navigation/handoff/lesson-17b47c23f2d25008c808.lesson.md) · 信号：setRequestedOrientation, window.setPreferredOrientation, NavDestination.onShown, startActivity
- [跳转前写入的共享状态是契约，按原顺序迁移](../topics/ui/navigation/handoff/lesson-dfcdbb19cd93d29159b2.lesson.md) · 信号：setPlaylist, startActivity, pushPathByName, onClick

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [loadChildFragment 子页做壳内回退栈不改路由](../topics/ui/navigation/hosts/lesson-7bcb44f0e376ec67e5a8.lesson.md) · 信号：loadChildFragment, loadFragment, addToBackStack, navigationTag
- [main_pages 只登记路由页，子组件和弹窗不登记](../topics/ui/navigation/hosts/lesson-c4a6eaaf6a22c0b8823f.lesson.md) · 信号：main_pages.json, 10905402, @CustomDialog, router.pushUrl
- [外部入口导航守卫按目标已注册判断不查栈成员](../topics/ui/navigation/hosts/lesson-1b05b8d5cc528d5dc5bc.lesson.md) · 信号：isIntentAvailable, pushPathByName, pageMap, EntryAbility
- [多屏共享清理归外层生命周期，切屏不释放](../topics/ui/navigation/hosts/lesson-2ed8c21943925bf0ae9a.lesson.md) · 信号：DisposableEffect, onDispose, EntryAbility.onDestroy, aboutToDisappear
- [嵌入子页只用 @Consumer 注入的根栈](../topics/ui/navigation/hosts/lesson-1cebb531c991239d2691.lesson.md) · 信号：@Consumer('navPathStack'), context.pathStack, onReady, @Provider
- [根 Navigation 显式隐藏默认标题栏与工具栏](../topics/ui/navigation/hosts/lesson-69e07207a06a8a8a7ba9.lesson.md) · 信号：hideTitleBar, hideToolBar, NavBarContent, Scaffold
- [进入即跳转并 finish 的页面按路由跳板处理](../topics/ui/navigation/hosts/lesson-0b72c197ea20fbe6f277.lesson.md) · 信号：finish(), startActivity, initView, onCreate
- [首屏 NavDestination 压栈，隐藏栏需非空栈](../topics/ui/navigation/hosts/lesson-8953e390416a80d7dd8c.lesson.md) · 信号：Builder function is empty, current stack is not navPathStack, navDestination, NavDestinationContext

### [ui/navigation/parameters](../topics/ui/navigation/parameters/index.md) — 路由参数契约：固定目的地名与 param、按接收端定义载荷、多入口共享载荷、缺失哨兵与有效性、语义冲突拆字段。

- [入参以 @Param 显式承接并由宿主真实传入](../topics/ui/navigation/parameters/lesson-289cab2abd4268b26ce0.lesson.md) · 信号：@Param, @Event, newInstance, setCurrentCity
- [同一参数多语义时按源契约拆字段或入口解析](../topics/ui/navigation/parameters/lesson-e202ff0d01ace7dee225.lesson.md) · 信号：JSON.parse, pushPathByName, ViewModel, DTO
- [多入口目标页按全部 extras 定义共享路由载荷](../topics/ui/navigation/parameters/lesson-953309e05bc1cd36c0d1.lesson.md) · 信号：searchFromMap, locationType, searchText, setResult
- [带参路由目的地用固定名，参数只走 param](../topics/ui/navigation/parameters/lesson-300200dd52892e9dadd2.lesson.md) · 信号：pushPathByName, pageMap, pathInfo.param, NavDestinationContext
- [路由入参在 aboutToAppear 读取并校验必填](../topics/ui/navigation/parameters/lesson-0d7d6e7302f8c8c77c66.lesson.md) · 信号：router.getParams(), router.pushUrl, requireArguments, navArgs
- [路由参数以接收端为准，不读的 extra 不透传](../topics/ui/navigation/parameters/lesson-4a7c04b864ef635c87b6.lesson.md) · 信号：putExtra, getXxxExtra, onReady, startActivity
- [路由参数缺失哨兵与有效性判定一致，错误态隐藏入口](../topics/ui/navigation/parameters/lesson-c433adebb9d20f273b22.lesson.md) · 信号：pathInfo.param, Number.isInteger, NavPathStack, -1

### [ui/state/binding](../topics/ui/state/binding/index.md) — 状态到控件的绑定与刷新：随状态变的参数不作 @Builder 值参、事件给出的目标值直写、按状态显隐、乐观更新。

- [Tab 默认选中只初始化一次，items 更新仅同步高亮](../topics/ui/state/binding/lesson-b6abeeb9b9476b1f1f4d.lesson.md) · 信号：@Param, @Event, @Monitor, selectedIndex
- [setVisibility 分支随状态迁移，GONE 不渲染](../topics/ui/state/binding/lesson-43a9050245b1afa165bf.lesson.md) · 信号：setVisibility, Visibility.Hidden, GONE, setText
- [上抛自身可见性的组件常建，不包 if/None](../topics/ui/state/binding/lesson-3a00fd66c5188f5cfdf4.lesson.md) · 信号：Visibility.None, visibility="gone", aboutToAppear, Fragment
- [乐观更新先翻转本地状态再发请求，回调只回填真值](../topics/ui/state/binding/lesson-18c8e7630a96d66540bc.lesson.md) · 信号：isFavorite, isLiked, onSuccess, @Local
- [回调中置位的状态按回调门控并补控件过滤](../topics/ui/state/binding/lesson-af89611fa71ea0eb6f45.lesson.md) · 信号：onQueryTextSubmit, SearchView, onSubmit, isLoading
- [宿主标题栏与 H5 导航栏按页面状态双向决定显隐](../topics/ui/state/binding/lesson-1a5fbc237ad071a62aaa.lesson.md) · 信号：runJavaScript, onOverrideUrlLoading, onTitleReceive, onPageEnd
- [开关事件目标值直传 setter，不用 toggle 取反](../topics/ui/state/binding/lesson-40fc63b124b4a44e7a9f.lesson.md) · 信号：onToggleChange, isOn, @Event, @Param
- [状态派生值不传 @Builder，改 @Param 子组件](../topics/ui/state/binding/lesson-8d2979542fa2cd65150c.lesson.md) · 信号：@Builder, @Param, @ComponentV2, Repeat

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [Toast 时长逐调用点传参，取串后保留加工](../topics/ui/state/feedback/lesson-8335bc404934f58c6f31.lesson.md) · 信号：Toast.makeText, LENGTH_SHORT, LENGTH_LONG, showToast
- [onErrorReceive 判主框架才切失败态](../topics/ui/state/feedback/lesson-051f8984f21058916bd9.lesson.md) · 信号：onErrorReceive, isMainFrame(), Web, web.d.ts
- [全局广播浮层按源端队列语义播放不自加去重上限](../topics/ui/state/feedback/lesson-2cc8bcca579d597cb6a2.lesson.md) · 信号：addAll, remove(0), onAnimationEnd, WindowManager
- [单一 SnackbarHost 用唯一宿主按源排队定时长](../topics/ui/state/feedback/lesson-187c725b1bb9d8d1bf4d.lesson.md) · 信号：SnackbarHost, Snackbar, actionLabel, SnackbarDuration
- [同一业务链每个入口都调用服务并在终态收口 loading](../topics/ui/state/feedback/lesson-a87eaa08f98ea95d04d5.lesson.md) · 信号：showLoading, hideLoading, UIContext
- [多来源与次级动作按区块存错误，不整页报错](../topics/ui/state/feedback/lesson-a82d821385bf8fb3feb0.lesson.md) · 信号：=== null, LiveData, try/catch, Success
- [异步结果回调按成功失败分支列全副作用逐项对齐](../topics/ui/state/feedback/lesson-ac7a2e17b8d88c3cee7b.lesson.md) · 信号：LiveData, showToast, AlertDialog.Builder, Settings.ACTION_APPLICATION_DETAILS_SETTINGS
- [推迟通知能力时为接口返回数据定义替代去向](../topics/ui/state/feedback/lesson-9d54e42c44b0d3e78bb1.lesson.md) · 信号：NotificationManager, onData, Toast, showToast
- [校验失败用全局 showToast，页内错误文字放固定行](../topics/ui/state/feedback/lesson-f97fc44e58a8d23333f0.lesson.md) · 信号：showToast, promptAction, layoutWeight, Toast
- [系统写入降级为保存后成功反馈改为引导手动设置](../topics/ui/state/feedback/lesson-e44d598230615f3f3262.lesson.md) · 信号：WallpaperManager, RingtoneManager, photoAccessHelper, showToast

### [ui/state/lifecycle](../topics/ui/state/lifecycle/index.md) — 生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

- [ON_STOP 接 onHidden，含导航离开](../topics/ui/state/lifecycle/lesson-19dd006e049c3f9d7563.lesson.md) · 信号：LocalLifecycleOwner, LifecycleEventObserver, ON_STOP, ON_RESUME
- [TextInput 获焦回调先判是否用户触摸再写业务状态](../topics/ui/state/lifecycle/lesson-4c476a62732697c56c22.lesson.md) · 信号：onFocus, enableKeyboardOnFocus, stopEditing, clearFocus
- [remember 按首次或 key 变才求值](../topics/ui/state/lifecycle/lesson-3b4a96141329db62a6af.lesson.md) · 信号：remember {, remember(, derivedStateOf, LaunchedEffect
- [共享单例按键丢弃过期响应，加载入口先单飞不取消上一请求](../topics/ui/state/lifecycle/lesson-c883a0ff96c32dfbd9ba.lesson.md) · 信号：onRefreshing, Refresh, @Monitor, aboutToAppear
- [回调迁 ViewModel 逐条迁赋值，开关两条路径都落地](../topics/ui/state/lifecycle/lesson-d7c148c4a233c59ff151.lesson.md) · 信号：ON_RESUME, onShown, onPageShow, LifecycleEventObserver
- [每次可见的重载迁 onShown 或订阅](../topics/ui/state/lifecycle/lesson-b3bb0bc33f4caded78a2.lesson.md) · 信号：aboutToAppear, onShown, onHidden, onWillShow
- [注册监听存句柄，aboutToDisappear 同引用移除](../topics/ui/state/lifecycle/lesson-14b7f4090b7b83873b22.lesson.md) · 信号：addListener, removeListener, aboutToDisappear, aboutToAppear

### [ui/state/observation](../topics/ui/state/observation/index.md) — 共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。

- [@Monitor 监听数组路径时，生产方以新数组重新赋值](../topics/ui/state/observation/lesson-0cc7ae4eec0a59086202.lesson.md) · 信号：@Monitor, @Trace, StateFlow.update, .push(
- [Activity 实例字段的会话态按页面实例建服务](../topics/ui/state/observation/lesson-d9143de006714935afe2.lesson.md) · 信号：getInstance, new Service()
- [共享状态 key 只用字母数字下划线，禁连字符](../topics/ui/state/observation/lesson-7508ddc52eaf816887f0.lesson.md) · 信号：AppStorageV2.connect, PersistenceV2, @ObservedV2, kebab-case
- [拆 ViewModel 单例，跨页状态显式传递而非换 new](../topics/ui/state/observation/lesson-fc724027e2c995632733.lesson.md) · 信号：getInstance(), AppStorageV2, @Param, @Monitor
- [换位列表的首尾序号按当前位置渲染时算](../topics/ui/state/observation/lesson-09a0bceae55d05616ecc.lesson.md) · 信号：itemsIndexed, ForEach, Repeat, itemGenerator
- [替换对象时 ForEach 键并入显示字段；稳定键则原位更新](../topics/ui/state/observation/lesson-2e636699fa65aefd63f0.lesson.md) · 信号：ForEach, Repeat, RepeatItem, @Param
- [未保存检测用改动标志，不对 @Local 数组 ===](../topics/ui/state/observation/lesson-5d6e099ff0c8965f2b3c.lesson.md) · 信号：@Local, UIUtils.getTarget, mutableStateOf, canSafelyExit
- [直读 @Trace 字段，不复制为 @Local 快照](../topics/ui/state/observation/lesson-08c38f950b69e991607d.lesson.md) · 信号：@ObservedV2, @Trace, @Local, AppStorageV2.connect

### [ui/text/copy](../topics/ui/text/copy/index.md) — 可见文案的来源：沿资源引用链取逐字值、静态页文案取自 XML、代码格式化文案建参数化资源、语言目录按源生成。

- [代码内经资源管理器取值传 $r().id](../topics/ui/text/copy/lesson-22432022455bff6f849b.lesson.md) · 信号：getStringSync, getStringArrayValueSync, getIntPluralStringValueSync, getPluralStringValueSync
- [代码格式化的固定措辞文案建参数化资源，$r 传参不写模板串](../topics/ui/text/copy/lesson-d442eb6e9aab4d77db18.lesson.md) · 信号：SimpleDateFormat, String.format, $r('app.string, string.json
- [可见文案沿引用链取 strings.xml 逐字值，非枚举名](../topics/ui/text/copy/lesson-31ab9f59945e5f0259ea.lesson.md) · 信号：strings.xml, @string/, stringResource
- [字符串全集取含依赖库的合并资源表，不只模块 res](../topics/ui/text/copy/lesson-fe295e164208c44e9116.lesson.md) · 信号：apktool, aapt2, values-*, ~/.gradle/caches
- [字符串按 aapt2 语义转值：折空白、剥引号](../topics/ui/text/copy/lesson-f88b9c824280ce239dea.lesson.md) · 信号：strings.xml, string.json, aapt2, el.text
- [系统文案建专属键补各语言框架译文](../topics/ui/text/copy/lesson-ff19b09146b57d0f91a8.lesson.md) · 信号：android.R.string.ok, @android:string/cancel, android.R.string, positiveButtonText
- [缺文案键新建专属键并交接原值，不借近义](../topics/ui/text/copy/lesson-4567f9f77f4280ec1747.lesson.md) · 信号：string.json, strings.xml, android:text, $r('app.string.
- [语言目录按源 values-* 全集与粒度镜像](../topics/ui/text/copy/lesson-b58df29f032cc6a8c9d6.lesson.md) · 信号：values-zh, values-zh-rTW, strings.xml, zh_CN
- [说明类静态页按源 XML 逐卡迁移，文案逐字取自源布局](../topics/ui/text/copy/lesson-0197307e63e8d848ba02.lesson.md) · 信号：@drawable, android:text, string.json, $r('app.string

### [ui/text/formatting](../topics/ui/text/formatting/index.md) — 显示值的加工在目标端复现：AnnotatedString 加工、setSpan 开区间、格式化精度与带兜底的访问器。

- [setSpan 转 Span 按 end 开区间逐字核范围](../topics/ui/text/formatting/lesson-eb59a95e5eb219c238b0.lesson.md) · 信号：SpannableString, setSpan, Span, ForegroundColorSpan
- [textAllCaps 按 locale 大写](../topics/ui/text/formatting/lesson-cce58a1538fedfda3695.lesson.md) · 信号：textAllCaps, AllCapsTransformationMethod, toLocaleUpperCase, textCase
- [复用基类格式化 getter 前核精度，不同则子类全覆写](../topics/ui/text/formatting/lesson-042445ba332611e04a80.lesson.md) · 信号：formatPrice, getPrice(, getValue(, toFixed
- [富文本加工与链接一并迁，单符号实体画图形](../topics/ui/text/formatting/lesson-57a52be767730880cbba.lesson.md) · 信号：AnnotatedString, buildAnnotatedStringWithUrls, LinkAnnotation, StyledString
- [源端用兜底访问器取显示值，目标调等价访问器不自拟兜底](../topics/ui/text/formatting/lesson-1fa08bf929cfced0ff34.lesson.md) · 信号：ResourceStr, toString(), $r(

### [ui/text/typography](../topics/ui/text/typography/index.md) — 文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

- [ellipsize=middle 无枚举时测量实现中间截断](../topics/ui/text/typography/lesson-a184209501ba02cb62e7.lesson.md) · 信号：ellipsize="middle", android:ellipsize, TextOverflow, measureText
- [动态文本字号行距按 dp×文字倍率落 vp，几何才乘画布比例](../topics/ui/text/typography/lesson-4c494b9f89c7e9db2b55.lesson.md) · 信号：dynamicTextScale, fontSizeScale, dpF, lineSpacing
- [单行盒高与多行行距分开，lineHeight 不同名直映](../topics/ui/text/typography/lesson-2a2924aaebbfbea80780.lesson.md) · 信号：lineHeight, .lineHeight(), lineSpacing, LengthMetrics.fp
- [单行省略补 BREAK_ALL，多行末行写差异](../topics/ui/text/typography/lesson-836a5414b52f0e062f1f.lesson.md) · 信号：maxLines, TextOverflow.Ellipsis, android:ellipsize, textOverflow
- [可折叠正文按测量高度判溢出，默认 Clip](../topics/ui/text/typography/lesson-c61ac79c7db81729a544.lesson.md) · 信号：onTextLayout, didOverflowHeight, hasVisualOverflow, maxLines
- [可能为空的 Text 保留一行高，不条件渲染](../topics/ui/text/typography/lesson-6668f8800d3ddaaf52ed.lesson.md) · 信号：TextView, wrap_content, INVISIBLE, Visibility.Hidden
- [缺枚举的 FontWeight 写数值，不换近名](../topics/ui/text/typography/lesson-605038b091e03c26c005.lesson.md) · 信号：FontWeight.SemiBold, FontWeight.Light, FontWeight.ExtraBold, FontWeight.Thin

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [Brush 渐变描边用外层渐变加内衬实底实现](../topics/ui/theme/effects/lesson-5d56afe5595bb26eaf2f.lesson.md) · 信号：Modifier.border, Brush.linearGradient, Surface, linearGradient
- [Brush 渐变转 linearGradient 并解析色序](../topics/ui/theme/effects/lesson-46805f8bf5da7b0c914b.lesson.md) · 信号：Brush.horizontalGradient, linearGradient, GradientDirection.Right, Surface
- [blendMode 着色把底色字形渐变放同一离屏组](../topics/ui/theme/effects/lesson-3024193e4816229c5370.lesson.md) · 信号：blendMode, BlendApplyType, drawWithContent, BlendMode.Plus
- [blur 半径先确认 vp 单位，模糊层放大后裁边](../topics/ui/theme/effects/lesson-6be3938453498c25e9a5.lesson.md) · 信号：Modifier.blur, BlurredEdgeTreatment, vp2px
- [elevation 阴影按 vp2px 换算并集中到共享函数](../topics/ui/theme/effects/lesson-d0aad947e26220fb43fa.lesson.md) · 信号：ShadowOptions, Modifier.shadow, vp2px, .shadow(
- [tint 着色渐变装饰层用容器 linearGradient](../topics/ui/theme/effects/lesson-fcd86aeea6209ea0718b.lesson.md) · 信号：app:tint, ?attr/colorBackground, fillColor, linearGradient
- [圆角加描边时 radius 写进 .border()](../topics/ui/theme/effects/lesson-8b7c4ece5e5bf7704a44.lesson.md) · 信号：.border(, .borderRadius(, cornerRadius, setStroke
- [文字阴影用 textShadow，不用组件 shadow](../topics/ui/theme/effects/lesson-2f1af636a29b131071b3.lesson.md) · 信号：shadowColor, shadowRadius, textShadow, .shadow(
- [模糊、乘法压暗与折叠着色按源参数等价实现](../topics/ui/theme/effects/lesson-55cac970ada4ca8fd3f1.lesson.md) · 信号：LightingColorFilter, .blur(
- [渐变端点几何换算成 linearGradient 角度与色标](../topics/ui/theme/effects/lesson-4ce3a1c186651285f362.lesson.md) · 信号：Brush.linearGradient, horizontalGradient, TileMode.Mirror, linearGradient
- [背景对象逐分支迁：url 用图片，否则按色数生成纯色或渐变](../topics/ui/theme/effects/lesson-2dc88a09f6cfbbe3393c.lesson.md) · 信号：orientation, linearGradient, backgroundImage, backgroundColor

### [ui/theme/sources](../topics/ui/theme/sources/index.md) — 控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

- [style 引用先展开再逐实例叠加覆写，圆角不照抄相邻](../topics/ui/theme/sources/lesson-bc5b8558ab086168b462.lesson.md) · 信号：@style/, styles.xml, @Builder, borderRadius
- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../topics/ui/theme/sources/lesson-47785524c7f132ea7efe.lesson.md) · 信号：colorPrimary, colorOnPrimary, Theme.MaterialComponents, LocalContentColor
- [布局引用的 @drawable 先打开取数值写进规格与修饰链](../topics/ui/theme/sources/lesson-771d1ba1a032b769097a.lesson.md) · 信号：progressDrawable, textCursorDrawable, layer-list, caretStyle
- [库与框架组件默认几何先查 SDK/库 res 分侧取](../topics/ui/theme/sources/lesson-5a82d62ff7e087616968.lesson.md) · 信号：TopAppBar, Snackbar, MaterialTheme.colorScheme, Tokens
- [视觉属性逐项取自源布局、item 布局与适配器分支，不近似](../topics/ui/theme/sources/lesson-e4e65a99e545871f96ae.lesson.md) · 信号：drawableLeft, drawableStart, ImageView, TextView

### [ui/theme/tokens](../topics/ui/theme/tokens/index.md) — 颜色与字体令牌的落地：按色值反查资源键、深色目录同步、深浅状态的可观察与系统栏图标、字族注册。

- [?attr 主题色逐主题取值导出 base/dark 对键](../topics/ui/theme/tokens/lesson-1856958fc6d369f0e2bb.lesson.md) · 信号：?attr/colorPrimary, colorControlNormal, colorOnSecondary, values-night
- [“零硬编码色值”只禁字面值，允许 $r 引用语义色](../topics/ui/theme/tokens/lesson-2e4279c4b82f06af64fd.lesson.md) · 信号：$r('app.color, #RRGGBB, backgroundColor, fontColor
- [三键导航按 TYPE_SYSTEM 底高判定后给导航栏着色](../topics/ui/theme/tokens/lesson-8bc258c2833be65f4fcd.lesson.md) · 信号：setNavigationBarColor, config_navBarInteractionMode, getWindowAvoidArea, TYPE_SYSTEM
- [多字重字族逐文件 registerFont，入口只注册一次](../topics/ui/theme/tokens/lesson-046baeb5ffbb10a6abc5.lesson.md) · 信号：registerFont, familyName, familySrc, $rawfile
- [应用内切主题时命令式取色随主题重解析](../topics/ui/theme/tokens/lesson-f1069f514c0eb98702fb.lesson.md) · 信号：setColorMode, getColorSync, getOverrideResourceManager, setWindowSystemBarProperties
- [按源端实际色值与字号在资源中反查同值键，不按名选键](../topics/ui/theme/tokens/lesson-4e9507a2a793c5583aa8.lesson.md) · 信号：color.json, float.json, $r('app.color, $r('app.float
- [深浅主题状态放可观察对象，入口同步，组件渲染期读取](../topics/ui/theme/tokens/lesson-7b19b801e0f21481d1d6.lesson.md) · 信号：isSystemInDarkTheme, onConfigurationUpdate, colorMode, @ObservedV2
- [状态栏图标按源浅色标志定，无标志即白色](../topics/ui/theme/tokens/lesson-824031d5fddf81036b54.lesson.md) · 信号：setWindowSystemBarProperties, statusBarContentColor, navigationBarContentColor, windowLightStatusBar
- [追加主题色时同步写 dark 目录同名键，已有文件只追加](../topics/ui/theme/tokens/lesson-1e972af4bc7e27b23d9c.lesson.md) · 信号：color.json, resources/dark, resources/base, darkColors

### [ui/web](../topics/ui/web/index.md) — ArkWeb 承载 WebView：WebSettings 默认值、viewport、导航拦截与外链、控制器挂接时序

- [导航拦截按手势判用户点击，挂接后再 loadData](../topics/ui/web/lesson-f095b7b87fbc8d8ed03d.lesson.md) · 信号：shouldOverrideUrlLoading, loadDataWithBaseURL, onLoadIntercept, isMainFrame
- [无 WebViewClient 时外链交系统浏览器](../topics/ui/web/lesson-42cf412cacabb3c8c281.lesson.md) · 信号：WebViewClient, setWebViewClient, shouldOverrideUrlLoading, onOverrideUrlLoading
- [未设 WebSettings 时按安卓默认逐项显式设](../topics/ui/web/lesson-65ebab594a9dabe77ac2.lesson.md) · 信号：WebSettings, javaScriptAccess, zoomAccess, overviewModeAccess
