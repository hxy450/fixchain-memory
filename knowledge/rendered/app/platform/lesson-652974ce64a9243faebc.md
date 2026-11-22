# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。也包括规格权限节只按 AndroidManifest 逐项映射（如把旧版存储权限写成“不需要，走媒体库”），而目标改用的传感器订阅、媒体资产写入与删除等 API 在 d.ts 中带 @permission；清单由规格权限节与各切片移交汇总生成。 也包括源端在 Android 侧无需权限的窗口标志（如 FLAG_SECURE）映射到带 @permission 的窗口 API（window.setWindowPrivacyMode），规格只凭源 Manifest 写“目标不声明任何权限”，并做成 requestPermissions 为空的静态验收或已批决策。按调用点汇总是为了补漏，不据此删清单里已有的声明：有些权限要求不写在 d.ts 方法的 @permission 上（如 Web 组件访问在线网页需要 ohos.permission.INTERNET，写在组件文档的“需要权限”里，组件声明没有 @permission），已声明却 grep 不到对应调用的权限，先查组件文档和依赖库再定去留。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD；它是 system_basic 级的受限开放权限，还要 ACL 授权，没有时改用粘贴控件 PasteButton 读取，粘贴控件无需申请该权限；PasteButton 要用户点击才授权：源端由用户点粘贴按钮触发读取时，放在原按钮的位置、沿用原来的读取后处理；源端不经点击自动读剪贴板的（如回到页面时自动检测），改用 PasteButton 会多一步点击，在规格里写明这是行为差异，不当作等价）。
2. 汇总清单以工程中实际调用的受权限 API 为准：检索 sensor.on、deleteAssets、createAsset 等调用点与 requestPermissions 逐项对照（例：订阅加速度计、陀螺仪需 ohos.permission.ACCELEROMETER/GYROSCOPE，MediaAssetChangeRequest 写删需 ohos.permission.WRITE_IMAGEVIDEO）。读接口声明时取完整 JSDoc，不用过滤注释的 grep 丢掉 @permission 与 @throws 201；切片移交的权限需求与规格的“不需要”冲突时，以 d.ts 或 skill 文档核实后裁决，不以规格措辞否决有依据的移交；user_grant 权限同时补运行期请求、reason 字符串与 usedScene（abilities 写用到该权限的组件，when 只填 inuse 或 always）；受限开放权限（如 WRITE_IMAGEVIDEO、READ_IMAGEVIDEO）还需签名配置中的受限权限授权，工程没有该授权时改走不需要它的路线（相机系统资产保存、showAssetsCreationDialog、picker），不把声明当作已获得。
3. 查到 @permission 后，在 SDK 的 toolchains/lib/PermissionDefinitions.json（按文件名检索时不区分大小写）读该权限的 grantMode 与 availableLevel 再定写法：system_grant 且 normal 只需在 module.json5 声明、安装即授予；user_grant 另加运行期申请与 reason；availableLevel 为 system_basic 及以上才涉及 ACL 或签名授权，不凭记忆判级别（例：setWindowPrivacyMode 需 ohos.permission.PRIVACY_WINDOW，HarmonyOS 6.1.0(23) SDK 中为 system_grant、normal）。规格或已批决策写了“requestPermissions 为空/不声明任何权限”而所调 API 带 @permission 时，带 d.ts 行号与已核级别交决策方改判后写入；写全空的静态验收前，按规格列出的系统能力面逐个核 @permission，任何一个带权限就不写全空断言。

来源支持：5 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码（WindowManager、ClipboardManager、SensorManager）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕鸿蒙接口要求的权限只写在 d.ts 里该方法注释的 @permission 行，同一注释块列出 @throws { BusinessError } 201；应用没有获得该权限时，调用在运行时以错误码 201 失败
- 〔原因 / 做法第 2 步〕module.json5 没有声明 ohos.permission.ACCELEROMETER、ohos.permission.GYROSCOPE、ohos.permission.WRITE_IMAGEVIDEO 的工程照常构建安装，设备日志里出现传感器订阅失败和 deleteAssets 的 201；没有声明 ohos.permission.PRIVACY_WINDOW 时，setWindowPrivacyMode 返回 201，hilog 有 PRIVACY_WINDOW 的 PERMISSION_DENIED
- 〔做法第 3 步〕module.json5 声明了 ohos.permission.PRIVACY_WINDOW、应用没有 ACL 也没有受限权限签名时，setWindowPrivacyMode(true) 生效期间截屏为黑，传 false 之后截屏正常
- 〔适用情境〕安卓上 WindowManager.LayoutParams.FLAG_SECURE 只是窗口标志，设置它不需要声明权限；SensorManager 读加速度计、陀螺仪不需要权限，只有采样率高于 200 Hz 时才要在清单里声明 HIGH_SAMPLING_RATE_SENSORS
- 〔适用情境〕安卓上 ClipboardManager.getPrimaryClip 没有权限要求；应用既不是默认输入法、也没有输入焦点时它返回 null
- 〔原因 / 做法第 1 步〕SystemPasteboard 的 getData（callback 与 Promise 两种）和 getDataSync 都带 @permission ohos.permission.READ_PASTEBOARD；文档写明剪贴板读取接口从 API 12 起才加上这项权限管控
- 〔做法第 1 步〕ohos.permission.READ_PASTEBOARD 列在受限开放权限里，权限级别 system_basic、授权方式 user_grant；用自定义控件读剪贴板要先经 ACL 跨级申请，再在 module.json5 声明，运行时弹窗向用户申请
- 〔做法第 1 步〕用粘贴控件 PasteButton 读剪贴板不需要申请 READ_PASTEBOARD，读取时不弹窗；点击控件得到的临时授权持续到灭屏、应用切到后台或退出，期间调用次数不限；控件样式不合法（尺寸、颜色导致不可见或不可识别）时授权失败
- 〔适用情境 / 做法第 3 步〕window.setWindowPrivacyMode 带 @permission ohos.permission.PRIVACY_WINDOW；PRIVACY_WINDOW 从 API 11 起是 normal 级、system_grant（API 9–10 为 system_basic）
- 〔做法第 2 步〕sensor.on 订阅 SensorId.ACCELEROMETER、SensorId.GYROSCOPE 分别带 @permission ohos.permission.ACCELEROMETER、ohos.permission.GYROSCOPE；这两项都是 normal 级、system_grant
- 〔做法第 2 步〕MediaAssetChangeRequest.deleteAssets、PhotoAccessHelper.createAsset、PhotoAccessHelper.applyChanges 带 @permission ohos.permission.WRITE_IMAGEVIDEO；MediaAssetChangeRequest.createAssetRequest 本身不带 @permission，权限要求落在随后的 applyChanges 上
- 〔做法第 2 步〕ohos.permission.WRITE_IMAGEVIDEO、ohos.permission.READ_IMAGEVIDEO 列在受限开放权限里，权限级别 system_basic、授权方式 user_grant；normal 级应用要经 ACL 跨级申请，直接改 HarmonyAppProvision 里 apl 的做法只限调试，不能用于上架
- 〔做法第 2 步〕保存图片、视频到图库可以不申请 WRITE_IMAGEVIDEO：用安全控件，或用 showAssetsCreationDialog 弹窗授权（声明里没有 @permission），后者返回已授权的媒体库 uri；弹窗要显示应用名，取自 module.json5 中 abilities 的 label 和 icon；传入沙箱路径能保存但弹窗没有预览
- 〔做法第 2 步〕没有受限权限签名授权的应用在模拟器上：相机照片经 createAsset 系列写入媒体库返回 201；经 photoAssetAvailable 拿到的相机资产调用 MediaAssetChangeRequest.saveCameraPhoto 能写入相册
- 〔做法第 3 步〕system_grant 权限在用户安装应用时由系统自动授予；user_grant 权限要在安装包里声明，并在运行时弹窗经用户允许后才获得
- 〔做法第 2、3 步〕module.json5 的 requestPermissions 里，申请 user_grant 或 manual_settings 权限时 reason（格式 $string: 资源引用，需多语种）和 usedScene 必填，usedScene.when 只能填 inuse 或 always；system_grant 权限这两项选填；这两个字段用于应用上架校验
- 〔做法第 3 步〕鸿蒙 SDK 的权限定义文件名为 PermissionDefinitions.json（大小写混写），在 openharmony/toolchains/lib 下，每项权限有 grantMode 与 availableLevel 字段，例如 PRIVACY_WINDOW 为 system_grant、normal，READ_PASTEBOARD 为 user_grant、system_basic
