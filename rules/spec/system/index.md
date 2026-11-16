# 系统能力、设备与三方 SDK

读到源端用蓝牙、NFC、定位、剪贴板等系统服务，WorkManager、前台 Service、常驻通知，MediaPlayer / SoundPool，分享面板，或厂商 SDK、Flutter 插件，规格里写这些能力的映射、权限和降级时

## 触发族

- [分享面板的渠道清单](share-channels/index.md)（1 条）：读到源端分享面板有系统、第三方平台、应用内多个渠道；规格里渠道清单只在依赖接缝说明里，验收条目没有逐渠道的条目
- [源端直接开关蓝牙的 BluetoothAdapter.enable / disable](bluetooth-toggle/index.md)（2 条）：源码里点击开关直接调 BluetoothAdapter.enable() / disable()，规格或验收条目里写的是蓝牙开关在鸿蒙上的契约（走系统设置、只写一种调用、没写回读）
- [源端 WorkManager Worker 的后台计时和进度通知](workmanager-background-timer/index.md)（5 条）：源端用 WorkManager Worker 在后台跨步推进计时、逐拍刷新进度通知、按钮经 PendingIntent.getBroadcast 静默投递、回前台按任务名读 WorkInfo，规格里铸成整体降级的 HARD-DIV / PD 决策、只锚定单步剩余时长或只放进程内状态
- [源端 MediaPlayer / SoundPool 播 res/raw 音频](raw-audio-playback/index.md)（3 条）：源端用 MediaPlayer.create(context, R.raw.x) 或 SoundPool load / play 播 res/raw 音频，规格的映射行写成 AVPlayer 重播、url=fd:// 设源或 AVPlayer 实例池
- [NFC 贴卡的系统派发入口和前台派发](nfc-tag-dispatch/index.md)（2 条）：源端 Manifest 的 activity / activity-alias 带 android.nfc.action.TECH_DISCOVERED，偏好里用 setComponentEnabledSetting 启停这个 alias，onResume 里 enableForegroundDispatch，规格里写成「无对等 → 应用内开关模拟」或让开关连前台派发一起拦
- [Flutter 插件的 MethodChannel 契约和 OHOS 选层](flutter-plugin-channel-layer/index.md)（4 条）：插件包的 Dart 源码、*_android / platform_interface 实现里有 MethodChannel、invokeMethod、原生 when (call.method) 分支，pubspec 只联邦 android/ios，插件的 solution 里 channels 为空或只按 Dart 枚举列方法，就给了 F5 / blocked 结论
- [源端能力探测的分支和不支持、外跳路径](capability-check-branches/index.md)（3 条）：读到源端入口先判 NfcAdapter.getDefaultAdapter() 为 null、再判 isEnabled()、不支持时弹对话框、按钮发 market:// 或 Settings.ACTION_NFC_SETTINGS 的 Intent 并带失败回退；规格把这些分支收成一个 isAvailable()、统一收敛为说明文本，或把一个分支的副作用扩到全部
- [安卓免权限的系统服务映射后的权限契约](mapped-api-permissions/index.md)（2 条）：读到源端用 ClipboardManager、NfcAdapter 这类无需运行时权限的系统服务；规格或功能基线写「requestPermissions 为空」「免权限」，没逐个查已映射接口的 @permission
- [源端自建的应用内分享渠道面板](in-app-share-channels/index.md)（2 条）：读到源端分享入口截图后调自建分享工具的 shareImage(...)、传渠道项列表、回调按 platformName 分发到各渠道；外部入口核对表把既有目标定为 systemShare.ShareController 系统面板，没列源端交互形态，也没找目标工程里的「分享至」Sheet
- [被归为「三方无等价」的厂商或三方 SDK 能力](vendor-sdk-no-equivalent/index.md)（3 条）：读到源端通过厂商或三方 SDK 用某项能力（如 HMS 账号授权），映射参考里可能写着可对到某个 Kit；规格把这个通道归入「三方无等价」HARD-DIV，写「无 1:1 等价 → 占位」，没查目标是否有系统 Kit 或厂商鸿蒙版
- [定位 SDK 结果里附带的地址](location-sdk-address/index.md)（1 条）：源端定位 SDK 回调结果（如 AMapLocation）里带 district、city 等地址字段并被业务直接当地名用；规格定位服务接口写的返回值
- [前台服务的承载类](foreground-service/index.md)（1 条）：源端 Service（如 LifecycleService）调 startForeground、manifest 写 foregroundServiceType；规格或决策台账里映射的承载类和 module.json5 extensionAbilities 的 type
- [Fragment 里常驻的设备监听和它发的常驻通知](device-listener-ongoing-notification/index.md)（1 条）：读到 Fragment 里注册一次、不注销的设备监听，连接、断开、电量回调在开关为真时以固定通知 ID、setOngoing(true) 更新通知，二级页另有随页面注销的监听；规格只写「监听按页面生命周期订阅/注销」，把常驻通知也归进页面生命周期，没指定唯一发布服务
- [交给外部应用的隐式 Intent 和可用性回退](implicit-intent-fallback/index.md)（2 条）：读到源 helper 按 scheme 用 ACTION_VIEW / ACTION_DIAL / ACTION_SENDTO 交给外部应用、可用性检查为假时回退或提示（如 geo: 打不开改开网页地图）；规格断言目标平台没有这套能力、把回退标 superseded，或服务层只留一个分类函数，动作和可用性探测没有目标符号承接
- [MediaRecorder 录制器映射成 AVRecorder](media-recorder/index.md)（3 条）：读到源端用 MediaRecorder 录音录像（setMaxDuration / setMaxFileSize、OnInfoListener.onInfo 按 what 分支、同步的 stop() / release() 后再重连相机）；规格映射表写「MediaRecorder → AVRecorder 状态机等价」，缺限额行、onInfo 各分支的 AC 或停录与关相机的串行契约
- [MediaPlayer / ExoPlayer 播放器映射成 AVPlayer](media-player-avplayer/index.md)（3 条）：读到源端用 MediaPlayer 或 ExoPlayer / media3 播放（宿主 onPause / onStop 里不停播、Player.Listener 分 STATE_BUFFERING / STATE_READY、轮询 bufferedPosition、多卡共享一个实例）；规格或台账写「→ AVPlayer 行为等价」「→ Video 组件」，或以会新增播控卡片为由不做后台续播
- [androidx ExifInterface 读写 EXIF](exif-interface/index.md)（1 条）：读到源端用 androidx ExifInterface 读写图片 EXIF（注释写着支持 WebP 和 PNG、调 setGpsInfo(location)），规格决定自研替代库，映射只写「JPEG 段级读写」「tag 名域不变」
- [交给别的应用读的 content URI（FileProvider、ACTION_SEND）](shared-uri-grant/index.md)（2 条）：读到源端经 FileProvider 生成 URI 放进剪贴板或分享，或 Intent.ACTION_SEND 带 EXTRA_STREAM、ACTION_VIEW 打开媒体 URI，没写显式授权标志；规格的剪贴板契约或映射行只写「图片 URI 写入」「startAbility sendData + EXTRA_STREAM uri」，没写接收方凭什么读
- [AlarmManager 精确闹钟和它到点发的通知](alarm-exact-reminder/index.md)（1 条）：读到源端 AlarmManager 精确闹钟到点自绘通知、按钮各带 PendingIntent（贪睡、推迟）；规格把代理提醒的按钮写成带 wantAgent 的 actionButton，或以「系统托管」降级到点副作用和开机恢复，没写发布失败码、有效提醒条数上限和到点无回调
- [源端 Camera2 相机的能力位、手动参数和采集回调](camera2-capture/index.md)（5 条）：读到源端 Camera2 相机代码：能力探测里写死为 true 的支持位、SENSOR_EXPOSURE_TIME 这类手动参数、靠 AE 状态驱动的前屏补光、onImageAvailable 里先复制字节再 image.close()；规格的契约、映射表或 AC 写成恒真判定、只列接口名、只写「AE 状态不可观测 → 近似」或只抽出「立即 close」，没写目标端的查询接口、单位值域、回退时序和释放顺序
