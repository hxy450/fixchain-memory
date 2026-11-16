# module.json5 的权限声明（requestPermissions）

agent 会看到什么：源 AndroidManifest 有 uses-permission，或目标代码调了要权限的系统接口（http.createHttp、Web、vibrator.startVibration、getSystemPasteboard().getData()、geoLocationManager）；module.json5 的 requestPermissions 缺对应的 ohos.permission.*，或 user_grant 权限缺 reason、usedScene

## 通用查法

### 系统接口要权限时，按 d.ts 的 @permission 和授权方式写 requestPermissions

审的是：资源
触发（任一种）：
- 读到：源 AndroidManifest.xml 有 uses-permission；写错的样子：module.json5 的 requestPermissions 缺对应的 ohos.permission.*
- 写错的样子：代码调了 @ohos.* / @kit.* 接口，d.ts 里的 @permission 不在 requestPermissions 里
- 读到：构建日志 WARN「you need to apply for the permissions: …」；写错的样子：requestPermissions 缺警告点名的 ohos.permission.*
适用范围：module.json5 的 requestPermissions，对照源端权限和目标代码调用的系统接口
做法：
- 对目标代码调用的每个系统接口，到鸿蒙 SDK 对应 .d.ts 按方法名读 @permission；源端 uses-permission 和构建警告点名的权限一并核对
- 按权限列表里的授权方式写：system_grant 只写 name；user_grant 再写 reason（$string 引用）和 usedScene { abilities, when: inuse 或 always }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getData(): Promise<PasteData> 标注 @permission ohos.permission.READ_PASTEBOARD：接口要的权限写在 .d.ts 该接口注释的 @permission 行（出处：鸿蒙 SDK 的 ets/api/@ohos.pasteboard.d.ts，SystemPasteboard.getData）
- ohos.permission.INTERNET、ohos.permission.VIBRATE：权限级别 normal，授权方式 system_grant：system_grant 权限声明即授予，只写 name（出处：permissions-for-all.md，ohos.permission.INTERNET、ohos.permission.VIBRATE）
- APPROXIMATELY_LOCATION 与 LOCATION 是 user_grant 权限，reason 和 usedScene 必填：user_grant 权限的条目要带 reason、usedScene（出处：declare-permissions.md，声明样例）
- usedScene.when 只能填 inuse 或 always：使用时机的取值（出处：declare-permissions.md，在配置文件中声明权限）
- 缺权限时调用抛 BusinessError 201 - Permission denied：少声明的权限编译能过，运行时才失败（出处：鸿蒙 SDK 的 ets/api/@ohos.net.http.d.ts，HttpRequest.request；ets/api/@ohos.vibrator.d.ts，vibrator.startVibration）
针对本应用要查的：
- 目标代码用到的每个系统接口要哪些权限：目标工程 .ets 文件里对 @ohos.* / @kit.* 模块方法的调用，到鸿蒙 SDK 对应 .d.ts 按方法名找；读注释里的 @permission 行；例：vibrator.startVibration 查出 ohos.permission.VIBRATE，connection.hasDefaultNet 查出 ohos.permission.GET_NETWORK_INFO
- 每项权限的授权方式：开发文档的应用权限列表 permissions-for-all.md，按权限名找小节；读「授权方式」一行：system_grant 只写 name；user_grant 再补 reason 和 usedScene
未核实：卡里环境是 HarmonyOS 6.0.1(21) / 6.1.1(24)，@permission 按本机 API 23 的声明核实；构建警告原文出自卡里的构建日志，本机声明和文档副本里没有找到这句
来源：2 张卡，2 个应用
- case-8c249997059a2524ea7b（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 5；做法第 2 步 ← 建议 1
- case-cc22f6cc1041c8cc1129（MifareClassicTool）：做法第 1 步 ← 建议 5

## 规矩

- rule-012731983d15｜代码发网络请求时，module.json5 要声明 ohos.permission.INTERNET｜读到：源 AndroidManifest.xml（合并清单）有 uses-permission android.permission.INTERNET 或 ACCESS_NETWORK_STATE；写错：module.json5 没有 requestPermissions 块，或其中缺 ohos.permission.INTERNET 或 GET_NETWORK_INFO
- rule-71be266b0d1f｜新增的 Web 页加载在线 URL 时，requestPermissions 补 INTERNET 权限｜读到：源端入口打开 WebView 加载 https:// 在线 URL；写错：目标端新增了 Web(...) 加载在线地址的页面，module.json5 的 requestPermissions 里没有 ohos.permission.INTERNET
- rule-f76fbad5eeb6｜调用振动接口时，module.json5 要声明 ohos.permission.VIBRATE｜读到：AndroidManifest.xml 有 `<uses-permission android:name="android.permission.VIBRATE" />`，代码里调 Vibrator；写错：目标 module.json5 的 requestPermissions 里没有 ohos.permission.VIBRATE
- rule-ca85930f8d2a｜module.json5 同时声明模糊和精确定位权限，构建权限警告逐项对照｜读到：源端 AndroidManifest 同时声明 ACCESS_FINE_LOCATION 和 ACCESS_COARSE_LOCATION；代码里调用 geoLocationManager.getCurrentLocation；写错：module.json5 的 requestPermissions 只有 ohos.permission.LOCATION 一项（照抄代码里的单个字符串）
- rule-8fb9fb5f2dc9｜代码调用带 @permission 的接口时，module.json5 的 requestPermissions 要声明｜写错：代码里调 pasteboard.getSystemPasteboard().getData()，module.json5 的 requestPermissions 却没有 ohos.permission.READ_PASTEBOARD（只按别的 d.ts 补了 ohos.permission.NFC_TAG）
- rule-25be79d84fdf｜接入 getOAID 时在 module.json5 声明追踪权限，带 reason 和 usedScene｜读到：目标代码调用 identifier.getOAID()；写错：module.json5 的 requestPermissions 里没有 ohos.permission.APP_TRACKING_CONSENT，或有了但缺 reason（$string 引用）、usedScene，或 reason 的字符串只在 base 没有 en_US
- rule-45601c8acb82｜requestPermissions 以代码实际调用的受权限接口为准汇总，user_grant 权限补 reason｜读到：目标 .ets 里调用 sensor.on(SensorId.GYROSCOPE …)、deleteAssets、createAsset 等声明 @permission 的接口；登记表里有要求声明 WRITE_IMAGEVIDEO 的移交项，规格权限节却写「不申请（媒体库路径）」；写错：module.json5 的 requestPermissions 缺 ohos.permission.ACCELEROMETER / GYROSCOPE / WRITE_IMAGEVIDEO，或以规格措辞否决了有 SDK 依据的移交项；user_grant 权限没有 reason 字符串
- rule-08ff1b768de6｜代码调 setWindowPrivacyMode 时，module.json5 声明 PRIVACY_WINDOW｜写错：代码里有 setWindowPrivacyMode(true/false)，module.json5 没有 requestPermissions 或其中没有 ohos.permission.PRIVACY_WINDOW；运行时 201 PERMISSION_DENIED 只被 hilog 记下
