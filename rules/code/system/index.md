# 系统能力与设备

源端有运行时权限、通知、WorkManager、地图和定位 SDK、NFC、蓝牙、网络状态、振动、OAID、Cipher 加解密、桌面小部件、登录授权 SDK、FlutterBoost，目标端有对应的 @ohos / @kit 接口、FormExtensionAbility 或三方 SDK 桥接时

## 子主题

- [登录、授权与三方 SDK](account/index.md)（6 条）：源端按 token 判登录态，或调微信这类 SDK 授权、支付并在回调里按类型分流，目标端有登录态判断、授权回调的 state 校验和 SDK 回调处理时
- [设备与连接](device/index.md)（26 条）：源端有 NfcAdapter、MifareClassic、BluetoothAdapter、ConnectivityManager、Vibrator、OAID，目标端有 nfc、bluetooth、connection、vibrator、identifier 这类系统接口时
- [地图与定位](map/index.md)（15 条）：源端有高德等地图 SDK 的 MapView、AMapLocationClient、POI 搜索和 SDK 初始化，目标端有地图组件或桥接、定位结果和占位的地图区时
- [通知与后台任务](notification/index.md)（13 条）：源端有 NotificationCompat.Builder、NotificationChannel、常驻通知、WorkManager / CoroutineWorker，目标端有 notificationManager.publish、NotificationRequest、SlotType 或后台计时时
- [权限](permission/index.md)（10 条）：源端申请定位、媒体、存储等运行时权限并有拒绝分支，目标端有 requestPermissionsFromUser、checkAccessTokenSync 和 module.json5 的权限声明时

## 触发族

- [源端 Cipher 加解密工具的空值和失败分支](cipher-util-branches/index.md)（5 条）：读到源端用 Cipher.getInstance 的加解密工具（空串前置返回、catch 里返回原文、按构建类型解密响应），产物里是目标 cryptoFramework 加解密封装和请求、响应中间件里对应的分支
- [cryptoFramework 的密钥规格串和加解密结果](crypto-framework-api/index.md)（3 条）：读到 Java 端 KeyFactory、Cipher.getInstance 的算法串，产物里是 cryptoFramework.createAsyKeyGenerator / createCipher 的规格串，以及 update、doFinal 结果的 .data 取值
- [Glance 桌面小部件迁成服务卡片](glance-form-card/index.md)（4 条）：读到源端 GlanceAppWidget（SizeMode.Exact、按 LocalSize.current 的宽高断点选布局），产物里是 FormExtensionAbility 下发卡片尺寸、FormDimension 档位映射，以及卡片页里用到的事件、组件和 struct 写法
- [FlutterBoost 宿主页的事件通道](flutter-boost-events/index.md)（1 条）：读过的源码里宿主挂 FlutterBoostFragment 子类或有事件通道常量表，用 addEventListener / sendEventToFlutter 收发事件；交回的宿主页只挂 FlutterUIComponent、没有对应的监听和推送
- [Flutter 调原生的分发（pushNativeRoute、MethodChannel）](flutter-native-dispatch/index.md)（2 条）：读到源端原生侧 FlutterBoostDelegate.pushNativeRoute 里 when (pageName) 分到各原生 Activity、setMethodCallHandler 里 when (call.method) 的分支；产物里 pushNativeRoute 把 getPageName() 直接交给路由 push，或 onMethodCall 只有按 Dart 枚举列出的 case、其余落到 notImplemented()
- [复制到剪贴板（ClipboardManager）](clipboard/index.md)（1 条）：读到源端用 ClipboardManager.setPrimaryClip 放 ClipData（复制图片时放 FileProvider 生成的 URI）；产物里 pasteboard.createData 的 MIME 类型（MIMETYPE_TEXT_URI / MIMETYPE_PIXELMAP）、放进去的沙箱 URI 和复制成功后的提示
- [桌面小部件迁成的 ArkTS 卡片](app-widget-form/index.md)（2 条）：读到 AppWidgetProvider、appwidget-provider 的 minWidth / minHeight、RemoteViews 布局，或卡片数据流（运行标志加条目）；产物里 FormExtensionAbility 读的状态来源、form_config.json 的 designWidth 和卡片里的字号、图标尺寸
- [d.ts 里带 @throws 801 的接口变体](throws-801-variant/index.md)（1 条）：读到 d.ts 里同一能力的几个变体（同步、Promise、带 ID 参数）中某个单独写了 @throws { BusinessError } 801 - Capability not supported；产物里所有调用方共用的封装选了这个变体（如 RdbStore.beginTrans）
