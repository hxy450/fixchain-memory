# 阶段：规格提取（spec）

本阶段可用的 216 条经验，按领域与主题分组；一条经验可属于多个阶段。

[返回根索引](../index.md)

## app — 应用级装配与横切机制：入口清单、启动链路、平台能力与系统状态、媒体文件、混合桥接、模块与资源产物

### [app/camera/capture](../topics/app/camera/capture/index.md) — 拍照触发与结果链：完成/失败回传与多帧交付、前屏补光、照片缓冲释放与资产回调

- [Photo 字节先复制或用完再 release，不释放后用](../topics/app/camera/capture/lesson-c81407857f6e70183c27.lesson.md) · 信号：photoAvailable, Photo.release, getComponent, byteBuffer
- [拍照桥接保留完成失败回传，多帧模式整组交付](../topics/app/camera/capture/lesson-91d254bb9a5187884b4b.lesson.md) · 信号：takePicture, captureBurst, CaptureCallback, onCaptureCompleted

### [app/camera/parameters](../topics/app/camera/parameters/index.md) — 手动曝光、ISO、对焦的单位值域，设备能力位查询与实时读数的取值通道

- [手动参数按 CameraKit 单位与值域换算，读写同口径](../topics/app/camera/parameters/lesson-2ce79e76ffde307832b9.lesson.md) · 信号：SENSOR_EXPOSURE_TIME, CONTROL_AE_EXPOSURE_COMPENSATION, SENSOR_SENSITIVITY, LENS_FOCUS_DISTANCE
- [能力位按会话查询并在提交后快照](../topics/app/camera/parameters/lesson-b28eaf0ed2aefc219beb.lesson.md) · 信号：CameraCharacteristics, CONTROL_AWB_AVAILABLE_MODES, isExposureModeSupported, isWhiteBalanceModeSupported

### [app/camera/recording](../topics/app/camera/recording/index.md) — 录像会话与 AVRecorder：profile 与帧率、启停串行、编码选项映射与应用层限额

- [AVRecorder 启停串行：共享停止任务、启动可取消](../topics/app/camera/recording/lesson-d41878bcc79f7e356a54.lesson.md) · 信号：MediaRecorder.prepare, MediaRecorder.stop, MediaRecorder.release, AVRecorder.prepare
- [应用层录像限额按已录时长计，保留停止分支](../topics/app/camera/recording/lesson-1957f0e6ad83f19258e8.lesson.md) · 信号：setMaxDuration, setMaxFileSize, OnInfoListener, MEDIA_RECORDER_INFO_MAX_DURATION_REACHED
- [录像选项按 AVRecorder 枚举映射，缺能力就报错](../topics/app/camera/recording/lesson-9826c047e0381581db09.lesson.md) · 信号：setVideoEncoder, setOutputFormat, setAudioSource, setCaptureRate

### [app/camera/session](../topics/app/camera/session/index.md) — CameraKit 会话的输入输出组成、提交时机、拍照 profile、拆卸重建顺序与相机就绪时机

- [一次性拍照请求在相机就绪回调消费，不用页面显示](../topics/app/camera/session/lesson-e3bf30ce225c1c8964aa.lesson.md) · 信号：StateCallback.onOpened, onConfigured, CameraInput.open, aboutToAppear

### [app/capability/degradation](../topics/app/capability/degradation/index.md) — 能力确实不可用时只降级做不到的一步，运行期显式提示

- [后台计时降级只砍执行载体，保留逐拍刷新与回前台补算](../topics/app/capability/degradation/lesson-30643cd3f209b896ffd1.lesson.md) · 信号：WorkManager, elapsedRealtime, PendingIntent.getBroadcast, backgroundTaskManager.requestSuspendDelay
- [平台差异只收敛做不到的一步，其余出口照源保留](../topics/app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md) · 信号：HARD-DIV, startAbility, viewData, market://
- [激励广告不可用时显式提示并按台账放行，不伪造奖励](../topics/app/capability/degradation/lesson-0f67121af7969203b76b.lesson.md) · 信号：showRewarded, onReward, RewardedAd, onUserEarnedReward

### [app/capability/launch](../topics/app/capability/launch/index.md) — 拉起外部应用、系统设置与分享：Want 预检与目标核对

- [应用内分享面板复用应用内弹层并逐渠道映射](../topics/app/capability/launch/lesson-b366cf7ae68525577f57.lesson.md) · 信号：ShareUtil, ShareItem, shareItems, platformName
- [隐式 Want 先 canOpenLink 预检，不靠抛错](../topics/app/capability/launch/lesson-948d876672049969b865.lesson.md) · 信号：bundleManager.canOpenLink, querySchemes, 17700056, startAbility

### [app/capability/sdk-lookup](../topics/app/capability/sdk-lookup/index.md) — 判定无等价前先查 Kit、ohpm、SDK 声明与权限注解

- [三方算法库输出以库真值字面为契约，不自研子集](../topics/app/capability/sdk-lookup/lesson-3f9e120416e534d4e6d5.lesson.md) · 信号：ical4j, RRule, Recur, EventRecurrenceFormatter
- [动态取色用 getColors 加回退，写明弃用](../topics/app/capability/sdk-lookup/lesson-9769c8f754044944d3ad.lesson.md) · 信号：dynamicLightColorScheme, dynamicDarkColorScheme, @ohos.wallpaper, getColors
- [厂商 SDK 先查 Kit 与 ohpm 包，不先写无等价](../topics/app/capability/sdk-lookup/lesson-e9890889e591196c3d0d.lesson.md) · 信号：ohpm, @amap/amap_lbs_common, @tencent/wechat_open_sdk, @kit.AccountKit
- [应用内开关蓝牙先查 access 开关接口再定方案](../topics/app/capability/sdk-lookup/lesson-7a081dc36013a60358ac.lesson.md) · 信号：enableBluetoothAsync, disableBluetoothAsync, @ohos.bluetooth.access, BluetoothAdapter.enable
- [无 OHOS 实现的插件先按底层能力建本地兼容插件](../topics/app/capability/sdk-lookup/lesson-45739c78f9767dacbc81.lesson.md) · 信号：dependency_overrides, platform_interface, MethodChannel, ohos/flutter_plugins
- [权限按目标 API 的 @permission 汇总](../topics/app/capability/sdk-lookup/lesson-652974ce64a9243faebc.lesson.md) · 信号：@permission, requestPermissions, module.json5, ohos.permission.READ_PASTEBOARD

### [app/cross-cutting](../topics/app/cross-cutting/index.md) — 源端由基类、DI 或全局单例隐式生效的横切行为（日志、埋点、设置、会话清理、通知）在目标的归属与逐点接线

- [开关控制的常驻通知由应用级服务持有，不随页面 VM](../topics/app/cross-cutting/lesson-e9f03fcc7f1e781c4b24.lesson.md) · 信号：notificationManager.publish, aboutToAppear, aboutToDisappear, NavDestination
- [诊断日志上传按源端打包清单与协议实现，收窄先确认](../topics/app/cross-cutting/lesson-d434bb5c16bc721d9a00.lesson.md) · 信号：usesCleartextTraffic, networkSecurityConfig, presignedUrl, http.request

### [app/entry](../topics/app/entry/index.md) — 入口 Ability 与 module.json5 装配：初始化时序、全局守护、外部进入与结果回传、扩展能力与卡片登记

- [intent-filter 逐条映射为 skills](../topics/app/entry/lesson-daba8a5b555e6657d085.lesson.md) · 信号：intent-filter, ohos.want.action.sendData, maxFileSupported, SEND_MULTIPLE
- [manifest 未声明的窗口缺省解析成目标值并指派](../topics/app/entry/lesson-c1d7ec16bb02aa152c33.lesson.md) · 信号：AndroidManifest, screenOrientation, windowSoftInputMode, auto_rotation_restricted
- [前台服务改扩展能力先查基类导出，type 与基类成对](../topics/app/entry/lesson-16c24b9a44153d703f04.lesson.md) · 信号：extensionAbilities, ServiceExtensionAbility, AppServiceExtensionAbility, WorkSchedulerExtensionAbility
- [固定快捷方式用 productViewManager](../topics/app/entry/lesson-fe5cf66672ce205ee0d7.lesson.md) · 信号：requestPinShortcut, isRequestPinShortcutSupported, disableShortcuts, ShortcutManager
- [外部入口页需确定快捷声明、Want 分支与参数写者](../topics/app/entry/lesson-c46f182cf1d01a97e05f.lesson.md) · 信号：ohos.ability.shortcuts, shortcuts_config.json, onNewWant, Want
- [多处 setResult 合并为一次带结果结束](../topics/app/entry/lesson-2f8c5cc0c4cc4938ec79.lesson.md) · 信号：setResult, RESULT_OK, RESULT_CANCELED, terminateSelfWithResult
- [深链声明 skills、domainVerify，隐式验收](../topics/app/entry/lesson-d77baa7494930d485425.lesson.md) · 信号：ohos.want.action.viewData, entity.system.browsable, pathStartWith, intent-filter

### [app/hybrid](../topics/app/hybrid/index.md) — Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

- [Flutter 宿主迁移要打开实际容器子类逐项迁事件桥接](../topics/app/hybrid/lesson-6717b958e274143453a8.lesson.md) · 信号：FlutterBoostFragment, addEventListener, sendEventToFlutter, FlutterUIComponent
- [通道方法集按原生分支全集与 Dart 调用点双向对照](../topics/app/hybrid/lesson-e6b1032f702fc61940f2.lesson.md) · 信号：MethodChannel, setMethodCallHandler, call.method, invokeMethod

### [app/map](../topics/app/map/index.md) — 地图与定位接入：SDK 单例初始化与就绪、定位权限成组、坐标系与行政区名补齐、原生地图组件生命周期

- [定位只给坐标时用逆地理编码取行政区名，不留空名](../topics/app/map/lesson-a317e16cd9f46aa34962.lesson.md) · 信号：geoLocationManager.getAddressesFromLocation, geoLocationManager.getCurrentLocation, AMapLocation, subLocality

### [app/media](../topics/app/media/index.md) — 媒体文件出入口与图片处理：picker 与安全控件、沙箱导出、播放 URI、解码预取、PixelMap 释放与快照限制

- [公共目录产物改落沙箱时每条链写出导出步骤](../topics/app/media/lesson-b59097ee968fe827f70d.lesson.md) · 信号：WRITE_EXTERNAL_STORAGE, ACTION_MEDIA_SCANNER_SCAN_FILE, DocumentViewPicker.save, MediaScannerConnection
- [图库选图用 PhotoViewPicker 并复制进应用目录](../topics/app/media/lesson-ad1db0aa0434c2e766fd.lesson.md) · 信号：PhotoViewPicker, READ_IMAGEVIDEO, MediaStore, photo_manager
- [导入导出按源运行时语义：OOM 兜底与 DEFLATED](../topics/app/media/lesson-8534b92df38e546092fe.lesson.md) · 信号：OutOfMemoryError, RangeError, ZipOutputStream, setMethod
- [音频导入用 AudioViewPicker 并复制进沙箱](../topics/app/media/lesson-62ac5e65ac4aa51128bd.lesson.md) · 信号：AudioViewPicker, photoAccessHelper, MediaStore.Audio, READ_MEDIA_AUDIO

### [app/media-library](../topics/app/media-library/index.md) — 系统媒体库直接读写：受限权限下的相机资产保存、最近媒体入口、删除确认与外部查看分享

- [最近媒体以自存 URI 为准，未授权不整库查询](../topics/app/media-library/lesson-43781ac1c21274acd48b.lesson.md) · 信号：MediaStore, MediaStore.Images.Media.EXTERNAL_CONTENT_URI, getAssets, getThumbnail
- [查看分享媒体 URI 用精确 MIME 并授读权限](../topics/app/media-library/lesson-044358011be198c5bf87.lesson.md) · 信号：ACTION_VIEW, ACTION_SEND, EXTRA_STREAM, startAbility
- [相机产出走系统资产保存，不靠受限写权限](../topics/app/media-library/lesson-bc279ce222e98e0d5ede.lesson.md) · 信号：MediaStore, IS_PENDING, MediaRecorder, createAsset

### [app/nfc](../topics/app/nfc/index.md) — NFC 读卡：能力三态前置检查、贴卡拉起的 skills 声明、按 UIAbility 前台派发与页面仿真

- [NFC 前置检查分不支持/关闭/可用三态，不折成布尔](../topics/app/nfc/lesson-5a140e45ecb578dd61ed.lesson.md) · 信号：NfcAdapter, isEnabled(), Settings.ACTION_NFC_SETTINGS, canIUse
- [贴卡拉起声明 TAG_FOUND，开关只管系统派发](../topics/app/nfc/lesson-89368bd540176a43d4a2.lesson.md) · 信号：android.nfc.action.TECH_DISCOVERED, tech-list, activity-alias, setComponentEnabledSetting

### [app/notification](../topics/app/notification/index.md) — 通知与代理提醒：WantAgent 按钮 requestCode 与刷新、通知字段约束、代理提醒边界与回退

- [代理提醒按自身 d.ts 映射按钮贪睡，写发布失败回退](../topics/app/notification/lesson-7f1bc7ddc88fab2d03bd.lesson.md) · 信号：reminderAgentManager, ActionButton, ActionButtonType, NotificationActionButton

### [app/playback](../topics/app/playback/index.md) — 音视频播放：AVPlayer/SoundPool 设源与状态机、错误通道、装载令牌与释放、后台播放

- [rawfile 设 fdSrc 不拼 fd:// 串](../topics/app/playback/lesson-1267d6cabb117824c67a.lesson.md) · 信号：getRawFdSync, getRawFd, fdSrc, AVFileDescriptor
- [短提示音保留混播与播放中 start 不重启语义](../topics/app/playback/lesson-5475edc47af05c1c6a5b.lesson.md) · 信号：MediaPlayer.create, requestAudioFocus, AudioFocusRequest, AudioSessionManager.activateAudioSession
- [退后台续播时接 AVSession 与音频长时任务](../topics/app/playback/lesson-65db317135138c3181c7.lesson.md) · 信号：avSession.createAVSession, setAVPlaybackState, setBackgroundPlayMode, backgroundTaskManager.startBackgroundRunning

### [app/recreation](../topics/app/recreation/index.md) — 源端 Activity 重建与新实例语义：配置变化、进程回收、重启与新请求在不重建的 UIAbility 上显式处理

- [singleton 收新请求时带版本重跑请求解析](../topics/app/recreation/lesson-45ae43a8f3ace3513834.lesson.md) · 信号：android:launchMode, launchType, onNewWant, onCreate
- [保留实例按是否配置重建区分，不以单例存在代替](../topics/app/recreation/lesson-ed571550c44efdeb321e.lesson.md) · 信号：NonConfigurationInstance, onConfigurationUpdate, hasInstance, configChanges
- [回收重建单列分支：仅系统回收时恢复整栈与原参数](../topics/app/recreation/lesson-b0405a29415547485ecb.lesson.md) · 信号：rememberNavController, NavHost, savedInstanceState, TaskStackBuilder
- [无 configChanges 时按源重建时序刷新关弹窗](../topics/app/recreation/lesson-94715d0df4c03a8fb5a5.lesson.md) · 信号：android:configChanges, screenOrientation, onSaveInstanceState, savedInstanceState
- [有随系统字号缩放的文本就声明跟随系统字号](../topics/app/recreation/lesson-ea965b7baf2488be23cd.lesson.md) · 信号：fontScale, configChanges, fontSizeScale, followSystem
- [杀进程意在重启用 restartApp 不用退出](../topics/app/recreation/lesson-73618bb856a8a7dfe7fc.lesson.md) · 信号：System.exit, Runtime.exit, Process.killProcess, ApplicationContext.restartApp

### [app/resources](../topics/app/resources/index.md) — 应用身份与资源产物从源端换算：脚手架模板值的替换、element/media 转换格式、图标尺寸与产物校验

- [沿用脚手架包名前核对决策与签名；vendor 按源端落地](../topics/app/resources/lesson-fb996956b33a1ba65861.lesson.md) · 信号：bundleName, com.example, applicationId, app.json5
- [资源值按精确名查全部 values*，限定词写分支](../topics/app/resources/lesson-0c9e222422d81871b464.lesson.md) · 信号：getColor, getDimension, getInteger, values-land

### [app/startup](../topics/app/startup/index.md) — 冷启动链路：启动去向与登录态组合、首屏就绪门与首启空状态、启动门闩兜底、加载页时长与启动弹窗守卫

- [延后采集通道时单独移植超时兜底发布就绪事件](../topics/app/startup/lesson-99a8d47085e4b1ae44de.lesson.md) · 信号：OaidResultEvent, Observable.timer, FWD-REF, OAID
- [持久化主题在 loadContent 前同步设好](../topics/app/startup/lesson-dcb3c5e66dec2d126234.lesson.md) · 信号：ApplicationContext.setColorMode, setColorMode, getPreferencesSync, loadContent
- [源端启动固定进主页时目标也进主页，登录页压在其上](../topics/app/startup/lesson-4c254d10ef9264683c55.lesson.md) · 信号：SplashActivity, NavPathStack, pushPathByName, LoginGuard
- [目标初始化极快时把首启加载页最短可见时长写进验收](../topics/app/startup/lesson-41bb62cd13921e4eedde.lesson.md) · 信号：SplashActivity, SplashScreen, windowStage.loadContent, setTimeout
- [迁启动链路时列出各去向页初始化请求与登录态组合](../topics/app/startup/lesson-8c24f05ec8df45401482.lesson.md) · 信号：initRequestData, SplashActivity, MainActivity, refreshToken
- [首启无已选项时定义显式空态，不以空编码请求](../topics/app/startup/lesson-95aa64d6b0a5c041d326.lesson.md) · 信号：hasInit, selectedCity, cityCode, preferences

### [app/window](../topics/app/window/index.md) — 窗口级行为：Activity 窗口标志与画中画映射到共享主窗口/PiPWindow 的作用范围与状态

- [画中画映射 PiPWindow 链路，不凭记忆判手机端没有](../topics/app/window/lesson-a45be20055d942e12052.lesson.md) · 信号：PictureInPictureParams, onUserLeaveHint, onPictureInPictureModeChanged, @ohos.PiPWindow
- [页窗口标志在共享主窗口上随页显隐成对开关](../topics/app/window/lesson-ea9a6cfecca9e091c7ea.lesson.md) · 信号：FLAG_KEEP_SCREEN_ON, FLAG_SECURE, getWindow(), window.getLastWindow
## arkts — ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

### [arkts/api-signatures](../topics/arkts/api-signatures/index.md) — 调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定

- [依赖 API 单位与作用范围时两端都读语义说明](../topics/arkts/api-signatures/lesson-f5cf8413ebea57f3b415.lesson.md) · 信号：vp2px, px2vp, .d.ts, uiContext
- [单调计时映射 getUptime 并选 TimeType](../topics/arkts/api-signatures/lesson-ce456d60534d97524aa4.lesson.md) · 信号：System.nanoTime, SystemClock.elapsedRealtime, systemDateTime.getUptime, TimeType.ACTIVE
- [属性方法不传 ResourceStr 联合值按重载定型](../topics/arkts/api-signatures/lesson-63660a8304f7d3920bfc.lesson.md) · 信号：accessibilityText, ResourceStr, @Computed, contentDescription

### [arkts/async-mapping](../topics/arkts/async-mapping/index.md) — 源端同步调用、线程与事件投递改成 Promise/异步 API 后的时序、重入、线程与结果三态

- [连续同步平台调用改 Promise 时在网关内串行](../topics/arkts/async-mapping/lesson-ba0cb144aa48f9584060.lesson.md) · 信号：Vibrator.cancel, vibrate(pattern), stopVibration, startVibration
- [阻塞等待改 Promise 后签名与调用链一路 await](../topics/arkts/async-mapping/lesson-c53d56284f178b5ab63f.lesson.md) · 信号：Thread.join, Object.wait, CountDownLatch.await, Future.get

### [arkts/java-stdlib](../topics/arkts/java-stdlib/index.md) — Java/Kotlin 标准库调用（集合序、字符串、正则、格式化、日历）与形似 JS API 的语义差异复刻

- [DecimalFormat 按半偶舍入与应用语言复刻](../topics/arkts/java-stdlib/lesson-ae093dedda604fddf17e.lesson.md) · 信号：DecimalFormat, BigDecimal, setScale, RoundingMode.HALF_EVEN
- [Java 读行切分格式化日历集中兼容实现](../topics/arkts/java-stdlib/lesson-237091b9b04bc4cd340b.lesson.md) · 信号：BufferedReader.readLine, String.split, String.format, SimpleDateFormat
- [形似 JS 的平台库调用按源语义逐项移植](../topics/arkts/java-stdlib/lesson-5e3ba83ebfe5bbdf9278.lesson.md) · 信号：Pattern, replaceAll, compareToIgnoreCase, List.remove
- [集合迭代序、byte 比较与返回码按 Java](../topics/arkts/java-stdlib/lesson-1f4747c81f16e9529787.lesson.md) · 信号：HashSet, HashMap, keySet, toArray

### [arkts/runtime-semantics](../topics/arkts/runtime-semantics/index.md) — 源端同步调用或数值运算改成 ArkTS 后的运行时差异：异步失败分支、初始化顺序、错误通道与 number 边界

- [Float 运算比较按 float32 后用 ===](../topics/arkts/runtime-semantics/lesson-0deb51172ebdd2e056a9.lesson.md) · 信号：Math.fround, toFloat(), Float, (int)
- [Kit 错误取 message 与 code，码先归一](../topics/arkts/runtime-semantics/lesson-b19162077a2ab886d809.lesson.md) · 信号：BusinessError, Number(code), instanceof Error, @ohos.net.http

### [arkts/ui-syntax](../topics/arkts/ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性

- [组件成员名避开 position/width 等通用属性](../topics/arkts/ui-syntax/lesson-c1968bdf112ed3e6b259.lesson.md) · 信号：zIndex, @Param
## data — 数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

### [data/model](../topics/data/model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持

- [实体字段按源类型真值定型，null 与空串分开](../topics/data/model/lesson-5a67ac0592e5a3fa20b9.lesson.md) · 信号：Parcel, String.valueOf, cursor.getString, ResultSet.getString

### [data/network-auth](../topics/data/network-auth/index.md) — 鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者

- [token 失效判定按响应拦截器实际分支的码迁移](../topics/data/network-auth/lesson-bad79e090d2af44d167b.lesson.md) · 信号：reasonCode, HandleErrorInterceptor, TokenInterceptor, LoginExpired
- [响应头携带 token 时 HTTP 封装连头一起返回](../topics/data/network-auth/lesson-2a4e6af209308c08aaa6.lesson.md) · 信号：headers()\["Authorization"\], RefreshToken, Response&lt;BaseResponse, TokenManager

### [data/network-endpoint](../topics/data/network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明

- [服务地址沿键名追到源端常量，host 与环境不自拟](../topics/data/network-endpoint/lesson-246252824c631aa6eff5.lesson.md) · 信号：BuildConfig.BASE_URL, SpKey.BASE_URL, NetworkModule, baseUrl

### [data/network-request](../topics/data/network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退

- [Service 收不透明 body 时追到源端构造处照抄字段](../topics/data/network-request/lesson-0bc494e864b2d8ab1a34.lesson.md) · 信号：@Body, RequestBody, data: Object, device_id
- [移植加解密工具保留空串直返与解密失败回退原文](../topics/data/network-request/lesson-4232e195ff42fc63ba43.lesson.md) · 信号：AESUtil, aesEncrypt, aesDecrypt, isEmpty

### [data/parsing](../topics/data/parsing/index.md) — JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度

- [JSON 取值的空值与类型规则按 org.json 定](../topics/data/parsing/lesson-5034b56be6fd828164c9.lesson.md) · 信号：org.json, getString, optString, getInt
- [byte\[\] 常量逐下标转写核总长，冲突以源为准](../topics/data/parsing/lesson-0bba9db6a18f2e732334.lesson.md) · 信号：byte\[\], Uint8Array, KeyA, KeyB
- [org.json 输出按库语义：null 删键、转义 /](../topics/data/parsing/lesson-0caaa4efc70dad90a15f.lesson.md) · 信号：JSONObject.put, JSONObject.NULL, JSONArray, toString(indent)
- [大整数 id 用 bigint，解析前给数字加引号保真](../topics/data/parsing/lesson-c066489fcf35ab37378c.lesson.md) · 信号：JSON.parse, bigint, Long, 2^53
- [自研 EXIF 写入按库源码取语义，值区顺排](../topics/data/parsing/lesson-ac58c27e534158e65647.lesson.md) · 信号：ExifInterface, setAttribute, setGpsInfo, TAG_GPS_TIMESTAMP

### [data/preferences](../topics/data/preferences/index.md) — 偏好键值存储：装载时机与同步读写、批量提交原子性、读点缺省值与默认值落盘

- [偏好入口同步装载，读写走 Sync 接口](../topics/data/preferences/lesson-93b3eeff61598bc42172.lesson.md) · 信号：getSharedPreferences, PreferenceManager.getDefaultSharedPreferences, getPreferencesSync, getPreferences
- [偏好契约按源全部读写点定格式、缺键与持久性](../topics/data/preferences/lesson-bf7a5ff24d5ae4193eb4.lesson.md) · 信号：SharedPreferences, getString, putString, editor.putString
- [同键多读点缺省不同时逐读点保留，不收敛为单一默认](../topics/data/preferences/lesson-11e4e15acdbadf579e07.lesson.md) · 信号：getBoolean, getString, getXxx
- [设置页出现时为缺键写 XML 默认值并落盘](../topics/data/preferences/lesson-4283cc343b875489b851.lesson.md) · 信号：addPreferencesFromResource, PreferenceFragment, PreferenceActivity, PreferenceScreen

### [data/storage](../topics/data/storage/index.md) — 本地持久化：relationalStore 建表与迁移、自增主键写入、预置数据与播种时机、fileIo 文件与目录操作

- [SQLiteOpenHelper 首次取库才建库，启动不预建](../topics/data/storage/lesson-519f6769ca714500d9c3.lesson.md) · 信号：SQLiteOpenHelper, getReadableDatabase, getWritableDatabase, relationalStore
- [手写建表 SQL 表名列名统一加引号，关键字不裸写](../topics/data/storage/lesson-c55c56444f5271471a64.lesson.md) · 信号：CREATE TABLE, createSql, relationalStore, executeSql
- [按日期实时计算的字段不改绑静态资产，先查内置能力](../topics/data/storage/lesson-6d259db1ffd8927834a2.lesson.md) · 信号：Lunar.fromDate, dayYi, dayJi, Intl.DateTimeFormat
- [演示预置数据逐字段取自源种子工厂与 assets 不自拟](../topics/data/storage/lesson-1c513fdf2cf212354aa0.lesson.md) · 信号：DemoDataFactory, rawfile, LocalDate.now(), plusDays

### [data/sync](../topics/data/sync/index.md) — 同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤

- [同步调度合并在途任务要补跑尾随请求，失败项重推](../topics/data/sync/lesson-cfe552e1b20080212ce9.lesson.md) · 信号：Mutex.withLock, Promise
- [重写多阶段数据流程时保留缓存写入等副作用步骤](../topics/data/sync/lesson-686bbe76f7c2c783f2bd.lesson.md) · 信号：DAO, currentId, Repository
## process — 迁移流程中输入、规格、检查结论与跨任务移交在交接环节失真的机制

### [process/check-gaming](../topics/process/check-gaming/index.md) — 用注释关键字、删功能、改产品语义或相似度阈值迎合检查与测试通过，而非落实源端语义

- [单测预期按源端实现手算，不编造更严的过滤期望](../topics/process/check-gaming/lesson-5bc9af19bedaecaf627c.lesson.md) · 信号：@Test, assertEquals, hypium, describe(

### [process/deferred-fulfillment](../topics/process/deferred-fulfillment/index.md) — 延后到别处兑现的占位、待裁决项与派发任务：登记边界、承接方与闭合是否真正落实

- [点击入口写具体导航契约，无兑现方不留 forward-ref](../topics/process/deferred-fulfillment/lesson-7f6b818559cfac767e4b.lesson.md) · 信号：forward-ref, WebView, URL, Intent
- [规格留待裁决条目，决策轮逐条出题或关闭](../topics/process/deferred-fulfillment/lesson-35b9cdfd5d22ce53465e.lesson.md) · 信号：待裁决, Kit, decision ledger, placeholder

### [process/enumeration-gaps](../topics/process/enumeration-gaps/index.md) — 枚举迁移范围、入口能力、验收条目或归属时漏掉源端实际存在的项、分支与中间步骤

- [Application 注册的接收器读本体写入规格](../topics/process/enumeration-gaps/lesson-4fb1c103822a8fd30b2a.lesson.md) · 信号：BroadcastReceiver, registerReceiver, CONNECTIVITY_ACTION, @ohos.net.connection
- [ViewModel 每步须有 feature 认领或跨契约](../topics/process/enumeration-gaps/lesson-431a65808f9b46b95974.lesson.md) · 信号：initData, getPlaceById, queryPlaceById, homeV2
- [增量迁功能时反查全部入口页上的红点与计数](../topics/process/enumeration-gaps/lesson-32141cb6d0d09cabd2f1.lesson.md) · 信号：Fragment
- [导航目的地写页面入参契约：名、类型、可空与读取方式](../topics/process/enumeration-gaps/lesson-f4d335605b44a60116b9.lesson.md) · 信号：nav_graph, &lt;argument&gt;, requireArguments(), getString
- [应用壳契约枚举源导航全部入口含深链与 scheme](../topics/process/enumeration-gaps/lesson-3348c580951ef82a9737.lesson.md) · 信号：NavPathStack, onNewWant, onCreate, module.json5
- [截图页范围含其入口直达二级页，不取最窄解释](../topics/process/enumeration-gaps/lesson-91c89aff3f8c5c47bd2a.lesson.md) · 信号：startActivity, Intent, Activity, setOnClickListener
- [拆层后各层方法按源端覆写与调用全集核对](../topics/process/enumeration-gaps/lesson-61a9fc7190c51c663697.lesson.md) · 信号：@Override, Listener, Callback, Facade
- [窗口/控件封装类的分叉可见行为逐项写入契约](../topics/process/enumeration-gaps/lesson-5948050d3b6dc39239a4.lesson.md) · 信号：setOffline, setEnabled, FootBar, SharedPreferences
- [系统表面降级为应用内页时写明入口位置与形式](../topics/process/enumeration-gaps/lesson-238588d3cceaf707ccfe.lesson.md) · 信号：Widget, AppWidget, FormExtensionAbility, LongPressGesture
- [验收条目实读源码段落，照抄比较符并给边界样例](../topics/process/enumeration-gaps/lesson-08854573a81a9fa03746.lesson.md) · 信号：width &gt; 600, Linkify, ViewModel, setOnBannerListener

### [process/inferred-not-traced](../topics/process/inferred-not-traced/index.md) — 凭名字、所在模块、import 或调用点推断语义，没有追到定义、委托终点与实际绑定

- [新旧两套实现并存时以当前构建启用的为基准](../topics/process/inferred-not-traced/lesson-2e8ffecce25935dda502.lesson.md) · 信号：buildConfigField, manifestPlaceholders, gradle
- [源端层层委托时追到最终实现再写规格与代码](../topics/process/inferred-not-traced/lesson-4606ccc434e247d4a240.lesson.md) · 信号：DialogHelper, DAO, Repository, LazyColumn
- [辅助谓词与 getter 读到定义再翻译，不按名字推断](../topics/process/inferred-not-traced/lesson-b3f534eb740a768d95a6.lesson.md) · 信号：isPlayingState, playPause, LiveData&lt;String&gt;, PAUSED
- [非空类型上的 null 判断按死分支迁移](../topics/process/inferred-not-traced/lesson-8c18bb22a8ecfe8c7f8a.lesson.md) · 信号：collectAsState, Flow&lt;Boolean&gt;, DataStore, == null
- [页面入口只按布局与页面类实际绑定推导，不补源端没有的控件](../topics/process/inferred-not-traced/lesson-76aa7901a0ae1af9d544.lesson.md) · 信号：initView, setOnClickListener, ViewModel, onClick
- [页面归属按实际 Service 调用判定，不按模块默认](../topics/process/inferred-not-traced/lesson-ad7d770bd5b826e58516.lesson.md) · 信号：resolve_by, Retrofit, Service, page_id

### [process/lossy-transcription](../topics/process/lossy-transcription/index.md) — 逐句转写源端表达式、条件与状态逻辑时简化改写：丢分支或条件、合并不同生命周期的字段

- [复位函数只复位源端每局路径实际赋值的字段](../topics/process/lossy-transcription/lesson-e2a08b9a98504718cd24.lesson.md) · 信号：initGame
- [多条件门控与行为参数逐项落码，不删不换不丢](../topics/process/lossy-transcription/lesson-dbffe1dd0333c713f94a.lesson.md) · 信号：&amp;&amp;, ||, canIUse

### [process/secondary-over-source](../topics/process/secondary-over-source/index.md) — 规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

- [共享组件挂载页面以源宿主容器 replace/add 为准](../topics/process/secondary-over-source/lesson-34c8ac69ad849f8c24e1.lesson.md) · 信号：FragmentTransaction, replace(, add(, Fragment
- [合成快照点击清单空时按源布局 onClick 绑定实现跳转](../topics/process/secondary-over-source/lesson-3ea52b78643f49c13cd1.lesson.md) · 信号：android:onClick, @{page::, view_xml_synthesized, clickable_elements
- [多模块同名布局按页面类模块与 Binding 类解析](../topics/process/secondary-over-source/lesson-d75ddb53d6609b35d025.lesson.md) · 信号：layout_sources, ViewBinding, DataBinding, fragment_mine.xml

### [process/unapproved-deviation](../topics/process/unapproved-deviation/index.md) — 未经带编号决策批准就修正源端缺陷、补写源端没有的元素或按成本降级

- [不补源端没有的元素；框架默认元素须保留](../topics/process/unapproved-deviation/lesson-352b96f599237cd27403.lesson.md) · 信号：ListPreference, DialogPreference, android.R.string.cancel, PD-
- [成本类降级按范围裁剪，闸门自动批准不算改判](../topics/process/unapproved-deviation/lesson-7827e0707780cb7546ee.lesson.md) · 信号：module.json5, form_config
- [源端可观察缺陷照迁并核次数，修正走待批决策](../topics/process/unapproved-deviation/lesson-14411595fd9ac1e17683.lesson.md) · 信号：decision_gaps, source-notes, IOException, Thread

### [process/unloaded-input](../topics/process/unloaded-input/index.md) — 必读输入因截断、乱码、上下文压缩或过期读取并未真正进入上下文就开始写码

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../topics/process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md) · 信号：Get-Content, Select-String, -Encoding UTF8, $OutputEncoding
- [必读 skill 与源码逐份读全，截断即重读再写码](../topics/process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md) · 信号：SKILL.md, sed -n, loaded_skills, rg

### [process/unverified-as-fact](../topics/process/unverified-as-fact/index.md) — 把生成期无法核验的推测、自拟值或假设写成硬性结论、期望值或已实现项

- [下“不存在”结论前确认检索覆盖完整声明与范围](../topics/process/unverified-as-fact/lesson-8b7a50eeb92fc3bdb1e7.lesson.md) · 信号：.d.ts, sed -n, head -n, grep -n
- [结论先查本机 SDK 与依赖源，查不到才标置信度](../topics/process/unverified-as-fact/lesson-c0f990ea57a901951ba8.lesson.md) · 信号：HARD, dp, .gitmodules, ?android:attr
- [规格常量分应用参数与源平台取值，后者写目标取法](../topics/process/unverified-as-fact/lesson-d280d90bb76be18536f6.lesson.md) · 信号：static final, = true, .0f
- [规格所需值上游缺失时回源码补或标待核，不自拟](../topics/process/unverified-as-fact/lesson-77ca67f164d77ec63cda.lesson.md) · 信号：api-inventory.json, auth_model, common.md, raw_apis.json
## ui — 界面迁移：布局几何、主题图形、文本、状态反馈、导航、弹窗、交互输入与列表分页的机制级对照

### [ui/accessibility](../topics/ui/accessibility/index.md) — 无障碍语义转写：角色、可用态、朗读节点合并与独立、图标朗读文本来源

- [可点击行卡转写 role、enabled 与朗读合并](../topics/ui/accessibility/lesson-5caf7eadb69e940926f9.lesson.md) · 信号：clickable, combinedClickable, Role.Button, accessibilityRole

### [ui/animation/frame-clock](../topics/ui/animation/frame-clock/index.md) — 帧驱动与计时：invalidate、自建渲染线程与帧时钟动画迁成 vsync 帧回调，请求合并、实例数与前后台时间推进

- [SurfaceView 线程循环按实例迁，vsync 驱动](../topics/ui/animation/frame-clock/lesson-4da9eabca745b3b2be91.lesson.md) · 信号：SurfaceView, SurfaceHolder.Callback, lockCanvas, unlockCanvasAndPost
- [自驱 ticker 进度按帧时间减起点，不钳增量](../topics/ui/animation/frame-clock/lesson-6d6ba721c81206d45fbe.lesson.md) · 信号：Animatable, animateTo, tween(, LinearEasing

### [ui/animation/transitions](../topics/ui/animation/transitions/index.md) — 显隐、尺寸、内容切换、列表条目与页面转场动画按源时长、曲线与先后顺序落为 ArkUI 动画

- [Compose 显隐与尺寸动画逐项落实，不只渐变](../topics/ui/animation/transitions/lesson-a4e6bcfb28597691c028.lesson.md) · 信号：AnimatedVisibility, expandVertically, shrinkVertically, AnimatedContent
- [NavHost 四向转场由页面绑定共享转场态](../topics/ui/animation/transitions/lesson-9de3322165e533d6b790.lesson.md) · 信号：enterTransition, exitTransition, popEnterTransition, popExitTransition
- [View 显隐动画与页面转场按源时长顺序实现](../topics/ui/animation/transitions/lesson-76258c72cc6764d88db3.lesson.md) · 信号：startAnimation, ViewPropertyAnimator, setCustomAnimations, res/anim
- [进入无转场按目的地页定，未调用按主题动画](../topics/ui/animation/transitions/lesson-9886f489045488c8b454.lesson.md) · 信号：overridePendingTransition, windowAnimationStyle, activity_open_enter, pushPathByName

### [ui/dialog/carriers](../topics/ui/dialog/carriers/index.md) — 按源弹层类型选载体：真弹窗不以页面叠层或路由页充当、V2 页面的弹窗 API、锚定下拉与自定义内容。

- [半透明卡片 Activity 迁 DIALOG 模式透明路由](../topics/ui/dialog/carriers/lesson-22c2a8f0e6b782b95448.lesson.md) · 信号：windowIsTranslucent, backgroundDimEnabled, windowBackground, NavDestinationMode.DIALOG
- [当前页 show 的底部弹窗叠在宿主页上不改路由页](../topics/ui/dialog/carriers/lesson-7ef02de8bbc10734c3d2.lesson.md) · 信号：bottomDialog, BottomSheetDialog, HMRouter, Navigation

### [ui/dialog/content](../topics/ui/dialog/content/index.md) — 弹窗内容与行为的还原：按源布局逐控件重建、复用共享弹窗组件、打开触发点、展开后加载数据、下拉关闭的手势门禁。

- [源弹窗按布局或库模板逐控件还原不用通用弹窗](../topics/ui/dialog/content/lesson-1f366fe4ccdc917ce0fc.lesson.md) · 信号：DialogXxxBinding.inflate, R.layout, android:hint, setContentView

### [ui/dialog/frame](../topics/ui/dialog/frame/index.md) — 弹层外壳外观：宽度公式、遮罩、圆角底色、投影、箭头与档位按源主题或库取值

- [M3 警告框按主题代际取外观并设遮罩](../topics/ui/dialog/frame/lesson-39077e6612d5f97b0731.lesson.md) · 信号：MaterialAlertDialogBuilder, Theme.Material3, Theme.MaterialComponents, colorSurfaceContainerHigh
- [平台默认 AlertDialog 先从平台资源写可见契约](../topics/ui/dialog/frame/lesson-9c4de55af3c1ecd8eaa4.lesson.md) · 信号：AlertDialog.Builder, DialogPreference, ListPreference, EditTextPreference
- [库对话框窗宽遮罩按提供方取值，不写 100%](../topics/ui/dialog/frame/lesson-1bff1c90d9df6c9609ec.lesson.md) · 信号：material-dialogs, md_dialog_max_width, md_dialog_horizontal_margin, windowMinWidthMinor
- [底部面板按实际高度定档，显式关 showClose](../topics/ui/dialog/frame/lesson-df1f691759f84ba9e688.lesson.md) · 信号：BottomSheetDialogFragment, ModalBottomSheet, skipPartiallyExpanded, STATE_EXPANDED

### [ui/graphics/canvas-text](../topics/ui/graphics/canvas-text/index.md) — Canvas 文字绘制：字体串与注册就绪、TextMetrics 度量字段选取、段落方向与基线取整

- [Paint 状态读回改为自记，不读 ctx 属性](../topics/ui/graphics/canvas-text/lesson-c91afa108d966666d22b.lesson.md) · 信号：Paint.getTextSize, getTextSize, getTextAlign, ctx.font
- [fillText 按串首强方向字符设 direction](../topics/ui/graphics/canvas-text/lesson-68717b80482f4bd12825.lesson.md) · 信号：Canvas.drawText, drawText, fillText, ctx.direction
- [字体串用注册名不加引号，测宽前等字体就绪](../topics/ui/graphics/canvas-text/lesson-74295d12b4edc025569f.lesson.md) · 信号：ctx.font, font.registerFont, registerFont, Typeface.createFromAsset
- [文字度量按源 API 分层选 TextMetrics 字段](../topics/ui/graphics/canvas-text/lesson-f876887b216b6caf9f39.lesson.md) · 信号：getTextBounds, Paint.ascent, getFontMetrics, measureText

### [ui/graphics/drawing](../topics/ui/graphics/drawing/index.md) — Canvas 自绘的移植：坐标原点共用、自适应公式的参照常量、共享绘制分支的统一规则与被注释绑定的静态化。

- [按 px 公式移植画布时主画布与离屏都用 PX 构造](../topics/ui/graphics/drawing/lesson-7083c6ad69ab19ad17dd.lesson.md) · 信号：LengthMetricsUnit.PX, CanvasRenderingContext2D, measureText, Paint.setTextSize
- [预缩放位图在 PixelMap 上按同一采样缩放](../topics/ui/graphics/drawing/lesson-c3bd9c8b2f24c209a659.lesson.md) · 信号：BitmapFactory.decodeResource, createScaledBitmap, drawBitmap, drawImage

### [ui/graphics/icons](../topics/ui/graphics/icons/index.md) — 图标资源的选取与显示：原图复制不以近名替代、固有 dp 与触摸盒分离、场景变体映射、动画矢量帧与 Lottie 接入。

- [animated-vector 按 atEnd 插值形变](../topics/ui/graphics/icons/lesson-e6b1f9094ec3b905cab5.lesson.md) · 信号：rememberAnimatedVectorPainter, AnimatedImageVector, animated-vector, atEnd
- [图标用源端原图，缺失从 drawable 密度目录复制不替代](../topics/ui/graphics/icons/lesson-943544ce27bf04f9faf8.lesson.md) · 信号：does not have a base resource, drawable-xxhdpi, SymbolGlyph, $r('app.media

### [ui/graphics/images](../topics/ui/graphics/images/index.md) — 背景图与图片组件的缩放、形状裁剪与分层落地：layer-list 逐层、整屏位图拉伸、自定义图片组件与兜底预览。

- [整屏背景位图用 ImageFit.Fill 不默认裁切](../topics/ui/graphics/images/lesson-7708f650eb4b55dce045.lesson.md) · 信号：android:background, ImageFit.Fill, ImageFit.Cover, scaleType

### [ui/interaction/app-bar](../topics/ui/interaction/app-bar/index.md) — 工具栏导航图标与菜单项：按实际生效者定汉堡或 Up，showAsAction 分流图标位与溢出

- [导航图标按生效者画，菜单按 showAsAction 分流](../topics/ui/interaction/app-bar/lesson-a6121cc7eaf207b702f7.lesson.md) · 信号：ActionBarDrawerToggle, syncState, parentActivityName, setDisplayHomeAsUpEnabled

### [ui/interaction/focus-ime](../topics/ui/interaction/focus-ime/index.md) — 焦点链与输入法：按键事件挂载点、可获焦组件、软键盘收放 API、首屏获焦时机与搜索框状态

- [SearchView 展开焦点提交收起分开建模](../topics/ui/interaction/focus-ime/lesson-4995a3977dc8bc7fa696.lesson.md) · 信号：SearchView, actionView, expandActionView, collapseActionView

### [ui/interaction/gestures](../topics/ui/interaction/gestures/index.md) — 触摸与手势移植：逐指派发过滤、自写状态机阈值、识别器默认参数、系统拖拽与长按触感

- [onTouch 逐指派发按源端接收方式过滤](../topics/ui/interaction/gestures/lesson-68023ac5f088c72a775a.lesson.md) · 信号：onTouch, getAction, getActionMasked, ACTION_POINTER_DOWN
- [自写触摸状态机按源阈值复刻，不换识别器](../topics/ui/interaction/gestures/lesson-b9f5cb5d3ae174e5bf70.lesson.md) · 信号：onTouch, dispatchTouchEvent, ItemTouchHelper, ScaleGestureDetector

### [ui/interaction/hit-testing](../topics/ui/interaction/hit-testing/index.md) — 叠放层的命中测试与手势归属：全尺寸覆盖层透传、Block 只放遮罩、侧滑行按钮热区、滑删方向与触发瞬间的坐标取值。

- [SwipeToDismissBox 方向按手势与偏移符号写明](../topics/ui/interaction/hit-testing/lesson-7f5eba1b969bddfb34dc.lesson.md) · 信号：SwipeToDismissBox, enableDismissFromStartToEnd, EndToStart, StartToEnd

### [ui/interaction/input](../topics/ui/interaction/input/index.md) — EditText 到 TextInput 的属性转换：默认装饰关闭、长度上限、小数输入、光标取证与掩码格叠层获焦。

- [inputType 只映射键盘，有 digits 才过滤](../topics/ui/interaction/input/lesson-0457a04c31208e1fb916.lesson.md) · 信号：inputType, textCapCharacters, textNoSuggestions, numberSigned
- [setError 迁尾部图标加聚焦气泡、改动即清](../topics/ui/interaction/input/lesson-f7edea01f8308bf563ef.lesson.md) · 信号：setError, TextInputLayout, showError, errorMessage
- [可编辑且分段着色用 RichEditor 承载](../topics/ui/interaction/input/lesson-ef93bb2086aef9604aa1.lesson.md) · 信号：RichEditor, addTextSpan, EditText, Spannable

### [ui/interaction/press-states](../topics/ui/interaction/press-states/index.md) — 可点击控件的按压与禁用态外观：隐式按压反馈补齐、禁用外观来源与点击拦截

- [源禁用只换背景时不用 .enabled(false)](../topics/ui/interaction/press-states/lesson-99080bd3bfc1bcbb9c5f.lesson.md) · 信号：setEnabled, android:enabled, .enabled(false), state_enabled

### [ui/interaction/selectors](../topics/ui/interaction/selectors/index.md) — 选择控件的选项、初值与选中标记：选项按源数据源、自定义属性初值、级联回填、条件勾选不换 Radio、Slider 步数。

- [Slider steps 翻步长：区间/(steps+1)](../topics/ui/interaction/selectors/lesson-d715fa78ada2e79a5fd2.lesson.md) · 信号：Slider, valueRange, Float.toString, toFixed

### [ui/layout/constraints](../topics/ui/layout/constraints/index.md) — 锚点与对齐语义的转换：源端默认对齐与锚点落到 Column/Row/Stack/RelativeContainer。

- [单视图居中加兄弟悬挂用 RelativeContainer](../topics/ui/layout/constraints/lesson-e607a28fcd91acd2b40f.lesson.md) · 信号：RelativeContainer, alignRules, __container__, constraintTop_toBottomOf

### [ui/layout/immersion](../topics/ui/layout/immersion/index.md) — 安全区沉浸：是否全屏、系统栏底色与避让带由哪一层承担

- [Tab 宿主不统一加顶部安全区，按子页源处理分别避让](../topics/ui/layout/immersion/lesson-48e9408812c28e934db8.lesson.md) · 信号：ImmersionBar, statusBarView, titleBarMarginTop, fitsSystemWindows
- [根视图状态栏 padding 与底色由页面容器承担](../topics/ui/layout/immersion/lesson-baf0ca22a69e7b76f636.lesson.md) · 信号：setPadding, DecorView, setBackgroundColor, statusBarColor
- [源窗口延伸到系统栏下才全屏，底部避让加在屏底层](../topics/ui/layout/immersion/lesson-0e1c846868f2683cc280.lesson.md) · 信号：getWindowAvoidArea, TYPE_NAVIGATION_INDICATOR, TYPE_SYSTEM, bottomRect

### [ui/layout/insets](../topics/ui/layout/insets/index.md) — 系统栏与软键盘避让值的取值、单位与只消费一次

- [innerPadding 顶部即状态栏高，目标只在一处避让](../topics/ui/layout/insets/lesson-f64afc22d41b130f1628.lesson.md) · 信号：Scaffold, innerPadding, consumeWindowInsets, contentWindowInsets
- [标题栏接 topInset 前判定源端避让方，内距只取一份](../topics/ui/layout/insets/lesson-cde4120ab9ad7412b1da.lesson.md) · 信号：fitsSystemWindows, topInset, paddingTop, .height()
- [源 adjustResize 时键盘避让设 RESIZE](../topics/ui/layout/insets/lesson-f86b02e97cc77e31d51a.lesson.md) · 信号：adjustResize, windowSoftInputMode, imePadding, KeyboardAvoidMode.RESIZE

### [ui/layout/intrinsic](../topics/ui/layout/intrinsic/index.md) — 由内容、位图比例或库内部规则决定的尺寸：wrap_content、固有高度与宽高比不用百分比或估值代替。

- [Material 按钮区分布局占位、背景实绘与触控范围](../topics/ui/layout/intrinsic/lesson-b73a1ac8908f74856a02.lesson.md) · 信号：minimumInteractiveComponentSize, IconButton, Surface, Box
- [TableLayout 列宽取各列自然宽最大值不等分](../topics/ui/layout/intrinsic/lesson-6cb9ad45093ce2ca28af.lesson.md) · 信号：TableLayout, TableRow, stretchColumns, shrinkColumns
- [内容定尺寸的父级里不写 100%，描边画在自身](../topics/ui/layout/intrinsic/lesson-a58ebfe7a4c55b041b14.lesson.md) · 信号：matchContentSize, fillMaxSize, Modifier.border, HitTestMode.None

### [ui/layout/layers](../topics/ui/layout/layers/index.md) — 页面骨架与叠放层按运行时真实结构落定：运行时挂载、重叠子视图、gone 节点不按 XML 占位定几何。

- [只构造未绘制的底层按构造态显示，不套隐藏分支](../topics/ui/layout/layers/lesson-1e279118c32645022ac2.lesson.md) · 信号：addView, setVisibility, INVISIBLE, VISIBLE
- [底栏之上的 BottomSheet 面板用布局内 Stack](../topics/ui/layout/layers/lesson-9f45b5d79206b5654aff.lesson.md) · 信号：BottomSheetBehavior, STATE_COLLAPSED, HIDDEN, CoordinatorLayout

### [ui/layout/scrolling](../topics/ui/layout/scrolling/index.md) — 滚动容器的包含范围、交叉轴尺寸、首尾留白与高度上限，以及 Scroll 内嵌套内容的测高与滚动归属。

- [Lazy 首尾留白用 contentStartOffset](../topics/ui/layout/scrolling/lesson-4030f978a230df37de2b.lesson.md) · 信号：contentStartOffset, contentEndOffset, contentPadding, PaddingValues
- [LazyRow 转可横滑容器，不降成普通 Row](../topics/ui/layout/scrolling/lesson-caa043fb95ff63e321e2.lesson.md) · 信号：LazyRow, horizontalArrangement, Arrangement.SpaceEvenly, AnimatedVisibility
- [只把源滚动区子节点放进 Scroll，固定头部留外面](../topics/ui/layout/scrolling/lesson-46a0d7f239efac925d33.lesson.md) · 信号：NestedScrollView, layout_below, layout_weight, layoutWeight(1)
- [折叠顶栏按滚动偏移算 fraction 插值不两态切换](../topics/ui/layout/scrolling/lesson-67ab02abe6ec76f4129e.lesson.md) · 信号：exitUntilCollapsedScrollBehavior, LargeTopAppBar, collapsedFraction, onDidScroll

### [ui/layout/sizing](../topics/ui/layout/sizing/index.md) — 满铺、剩余空间与边距内距的尺寸公式及单位域：百分比、layoutWeight、calc 与 px/vp 取舍。

- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](../topics/ui/layout/sizing/lesson-45f77b3088fa69398f9e.lesson.md) · 信号：fillMaxWidth, requiredWidth, Visibility.Hidden, layoutWeight(1)
- [weightSum 与权重和不等时按源算法分余量](../topics/ui/layout/sizing/lesson-adad817f2c3c8f1eaa09.lesson.md) · 信号：weightSum, layout_weight, layoutWeight, flexGrow
- [整数 px 公式在 px 域取整再 px2vp 写入属性](../topics/ui/layout/sizing/lesson-0ef2cd00e1a91491b350.lesson.md) · 信号：px2vp, vp2px, measureText, onAreaChange
- [背景之前的 padding 放外层，背景圆角裁剪放内层](../topics/ui/layout/sizing/lesson-5c6217b05bb4c266f254.lesson.md) · 信号：statusBarsPadding, navigationBarsPadding, Surface, borderRadius

### [ui/layout/variants](../topics/ui/layout/variants/index.md) — 布局方向与限定词变体：supportsRtl、land、swNdp 按窗口条件分支

- [声明 RTL 时保留 start/end 并镜像图标](../topics/ui/layout/variants/lesson-786a04847bf10d364d9d.lesson.md) · 信号：android:supportsRtl, LengthMetrics, marginStart, paddingStart
- [布局变体逐控件对照，按窗口条件分支](../topics/ui/layout/variants/lesson-c8e645a542254d96997e.lesson.md) · 信号：layout-land, layout-sw600dp, setBackgroundResource, layout_sources
- [未声明 supportsRtl 时有序容器逐个设 Ltr](../topics/ui/layout/variants/lesson-148a3e67bd557bafd722.lesson.md) · 信号：android:supportsRtl, Direction.Ltr, Direction.Auto, .direction(

### [ui/libraries](../topics/ui/libraries/index.md) — 三方 UI 库承载的界面：取库工件核对几何、手势与算法后再定目标映射

- [三方 UI 库先取 AAR 核几何行为再定映射](../topics/ui/libraries/lesson-f79082832a2fb18c8754.lesson.md) · 信号：build.gradle, AppIntro2, SublimePicker, FloatingActionsMenu

### [ui/list/behaviors](../topics/ui/list/behaviors/index.md) — 列表容器行为：侧栏与分组列表的滚动联动、组头默认展开、Repeat 虚拟滚动的项高度核对、swipeAction 挂载。

- [分类页右侧用 Scroller 列表双向联动迁滚动保护](../topics/ui/list/behaviors/lesson-7723af3766fb843a2577.lesson.md) · 信号：scrollToIndex, onScrollIndex, Scroller, LazyListState

### [ui/list/data-sources](../topics/ui/list/data-sources/index.md) — 列表数据源的绑定与并发：各列表各自的数据与排序器、本地变换随列表迁移、分页门闩、代次保护与行内在途锁。

- [onReachEnd 分页加载中不重入、刷新中不派发](../topics/ui/list/data-sources/lesson-0a398b212a8a80bd0c7f.lesson.md) · 信号：SmartRefreshLayout, onReachEnd, onRefreshing, setOnLoadMoreListener

### [ui/list/items](../topics/ui/list/items/index.md) — 条目类型与渲染分支：多 viewType 卡片外观、绑定代码里的区块与模板、跨列占位、副行回退、配置驱动分派。

- [多类型卡片外观按各类 holder 取，不共用一套](../topics/ui/list/items/lesson-9de4c7648d23db5d7f86.lesson.md) · 信号：cardCornerRadius, viewType, ViewHolder, CardView
- [恒空占位不在多列 Grid 生成通栏 GridItem](../topics/ui/list/items/lesson-2bd2620e5d1ef4bb17b4.lesson.md) · 信号：spanSizeLookup, GridLayoutManager, GridItem, WaterFlow

### [ui/list/pager](../topics/ui/list/pager/index.md) — ViewPager 到 Swiper：页数与禁滑方式、初始页用 index 绑定、自绘 tab 双向联动与日历翻页容器

- [ViewPager 定页阈值与归位时长按其规则落实](../topics/ui/list/pager/lesson-fc05d6dfe9844a88815b.lesson.md) · 信号：ViewPager, Swiper, determineTargetPage, smoothScrollTo
- [单页不用 Swiper；禁滑用 disableSwipe](../topics/ui/list/pager/lesson-540747e352d7f006016d.lesson.md) · 信号：ViewPager2, disableSwipe, isUserInputEnabled, Swiper

### [ui/navigation/back-stack](../topics/ui/navigation/back-stack/index.md) — 返回键与栈变更：覆盖层逐层关闭、按启动来源的返回分支、子组件拦截返回、清栈重建与重复导航的净效果。

- [Fragment 事务与 finish 逐分支映射栈操作](../topics/ui/navigation/back-stack/lesson-9a113ce21ae30365ea5b.lesson.md) · 信号：popBackStackImmediate, addToBackStack, popBackStack, finish()
- [handleDeepLink 深链清栈合成起始页加目标](../topics/ui/navigation/back-stack/lesson-69229aa8c7b051229f26.lesson.md) · 信号：handleDeepLink, navDeepLink, uriPattern, FLAG_ACTIVITY_NEW_TASK
- [tab、深链与桌面重进的返回栈后果写验收并实现](../topics/ui/navigation/back-stack/lesson-39f137ee173e50363f79.lesson.md) · 信号：popUpTo, saveState, restoreState, launchSingleTop
- [同一成功多条导航响应只保留一个导航出口](../topics/ui/navigation/back-stack/lesson-683d8f5070802c518020.lesson.md) · 信号：FLAG_ACTIVITY_NEW_TASK, finish(), startActivity, NavPathStack
- [栈底 NavDestination 返回退后台不出栈](../topics/ui/navigation/back-stack/lesson-efff93743d668b55b55a.lesson.md) · 信号：onBackPressed, moveAbilityToBackground, terminateSelf, onBackPress
- [父栈跳转按 Manifest 父链 clear 后重建](../topics/ui/navigation/back-stack/lesson-2986423250986124d039.lesson.md) · 信号：TaskStackBuilder, addNextIntentWithParentStack, startActivities, parentActivityName

### [ui/navigation/hosts](../topics/ui/navigation/hosts/index.md) — Navigation/@Entry 宿主与页面注册：栈来源、首屏压栈、路由跳板、默认标题栏、外部入口守卫与跨页生命周期。

- [多屏共享清理归外层生命周期，切屏不释放](../topics/ui/navigation/hosts/lesson-2ed8c21943925bf0ae9a.lesson.md) · 信号：DisposableEffect, onDispose, EntryAbility.onDestroy, aboutToDisappear

### [ui/state/feedback](../topics/ui/state/feedback/index.md) — 操作结果反馈：异步结果各分支的副作用、失败隔离与降级语义、loading 收口、提示浮层的承载与队列。

- [全局广播浮层按源端队列语义播放不自加去重上限](../topics/ui/state/feedback/lesson-2cc8bcca579d597cb6a2.lesson.md) · 信号：addAll, remove(0), onAnimationEnd, WindowManager
- [推迟通知能力时为接口返回数据定义替代去向](../topics/ui/state/feedback/lesson-9d54e42c44b0d3e78bb1.lesson.md) · 信号：NotificationManager, onData, Toast, showToast

### [ui/state/lifecycle](../topics/ui/state/lifecycle/index.md) — 生命周期触发的加载与复位：返回不再走 aboutToAppear、加载入口单飞、监听成对释放、框架会恢复的焦点与状态。

- [ON_STOP 接 onHidden，含导航离开](../topics/ui/state/lifecycle/lesson-19dd006e049c3f9d7563.lesson.md) · 信号：LocalLifecycleOwner, LifecycleEventObserver, ON_STOP, ON_RESUME
- [翻译 remember 复位语义时列出框架会恢复的界面态](../topics/ui/state/lifecycle/lesson-1f6e36f8e8bf9df951da.lesson.md) · 信号：rememberSaveable, pushPath, NavBar, Tabs

### [ui/state/observation](../topics/ui/state/observation/index.md) — 共享可观察模型的订阅：@Trace 字段判定与直读、新数组赋值发变更、ForEach 键与原位更新、实例拆分。

- [Activity 实例字段的会话态按页面实例建服务](../topics/ui/state/observation/lesson-d9143de006714935afe2.lesson.md) · 信号：getInstance, new Service()
- [共享状态 key 只用字母数字下划线，禁连字符与点号](../topics/ui/state/observation/lesson-7508ddc52eaf816887f0.lesson.md) · 信号：AppStorageV2.connect, PersistenceV2, @ObservedV2, kebab-case
- [判字段是否需 @Trace 前先读其修改方法与显示界面](../topics/ui/state/observation/lesson-4d1c980bbbd20275f5c3.lesson.md) · 信号：@Trace, @ObservedV2, data class, copy(

### [ui/text/copy](../topics/ui/text/copy/index.md) — 可见文案的来源：沿资源引用链取逐字值、静态页文案取自 XML、代码格式化文案建参数化资源、语言目录按源生成。

- [语言目录按源 values-* 全集与粒度镜像](../topics/ui/text/copy/lesson-b58df29f032cc6a8c9d6.lesson.md) · 信号：values-zh, values-zh-rTW, strings.xml, zh_CN

### [ui/text/typography](../topics/ui/text/typography/index.md) — 文本度量的换算：lineHeight 与单行盒高、字号倍率 dp→vp，以及单行中间省略与多行末行截断粒度。

- [单行盒高与多行行距分开，lineHeight 不同名直映](../topics/ui/text/typography/lesson-2a2924aaebbfbea80780.lesson.md) · 信号：lineHeight, .lineHeight(), lineSpacing, LengthMetrics.fp
- [单行省略补 BREAK_ALL，多行末行写差异](../topics/ui/text/typography/lesson-836a5414b52f0e062f1f.lesson.md) · 信号：maxLines, TextOverflow.Ellipsis, android:ellipsize, textOverflow

### [ui/theme/effects](../topics/ui/theme/effects/index.md) — 渲染效果换算：阴影 px 单位、模糊边缘、blendMode 离屏范围、渐变端点几何与角度、渐变描边与背景分支。

- [blendMode 着色把底色字形渐变放同一离屏组](../topics/ui/theme/effects/lesson-3024193e4816229c5370.lesson.md) · 信号：blendMode, BlendApplyType, drawWithContent, BlendMode.Plus
- [elevation 阴影按 vp2px 换算并集中到共享函数](../topics/ui/theme/effects/lesson-d0aad947e26220fb43fa.lesson.md) · 信号：ShadowOptions, Modifier.shadow, vp2px, .shadow(

### [ui/theme/sources](../topics/ui/theme/sources/index.md) — 控件外观数值的真实来源：应用主题、库默认 Tokens、style 继承、被引用 drawable 与截图取证。

- [主题或宿主隐式提供的外观写成显式样式，取值自实际提供方](../topics/ui/theme/sources/lesson-47785524c7f132ea7efe.lesson.md) · 信号：colorPrimary, colorOnPrimary, Theme.MaterialComponents, LocalContentColor
- [布局引用的 @drawable 先打开取数值写进规格与修饰链](../topics/ui/theme/sources/lesson-771d1ba1a032b769097a.lesson.md) · 信号：progressDrawable, textCursorDrawable, layer-list, caretStyle
- [库与框架组件默认几何先查 SDK/库 res 分侧取](../topics/ui/theme/sources/lesson-5a82d62ff7e087616968.lesson.md) · 信号：TopAppBar, Snackbar, MaterialTheme.colorScheme, Tokens

### [ui/theme/tokens](../topics/ui/theme/tokens/index.md) — 颜色与字体令牌的落地：按色值反查资源键、深色目录同步、深浅状态的可观察与系统栏图标、字族注册。

- [?attr 主题色逐主题取值导出 base/dark 对键](../topics/ui/theme/tokens/lesson-1856958fc6d369f0e2bb.lesson.md) · 信号：?attr/colorPrimary, colorControlNormal, colorOnSecondary, values-night
- [“零硬编码色值”只禁字面值，允许 $r 引用语义色](../topics/ui/theme/tokens/lesson-2e4279c4b82f06af64fd.lesson.md) · 信号：$r('app.color, #RRGGBB, backgroundColor, fontColor
- [三键导航按 TYPE_SYSTEM 底高判定后给导航栏着色](../topics/ui/theme/tokens/lesson-8bc258c2833be65f4fcd.lesson.md) · 信号：setNavigationBarColor, config_navBarInteractionMode, getWindowAvoidArea, TYPE_SYSTEM
- [状态栏图标按源浅色标志定，无标志即白色](../topics/ui/theme/tokens/lesson-824031d5fddf81036b54.lesson.md) · 信号：setWindowSystemBarProperties, statusBarContentColor, navigationBarContentColor, windowLightStatusBar

### [ui/web](../topics/ui/web/index.md) — ArkWeb 承载 WebView：WebSettings 默认值、viewport、导航拦截与外链、控制器挂接时序

- [未设 WebSettings 时按安卓默认逐项显式设](../topics/ui/web/lesson-65ebab594a9dabe77ac2.lesson.md) · 信号：WebSettings, javaScriptAccess, zoomAccess, overviewModeAccess
