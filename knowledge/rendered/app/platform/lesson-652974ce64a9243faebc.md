# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。也包括规格权限节只按 AndroidManifest 逐项映射（如把旧版存储权限写成“不需要，走媒体库”），而目标改用的传感器订阅、媒体资产写入与删除等 API 在 d.ts 中带 @permission；清单由规格权限节与各切片移交汇总生成。 也包括源端在 Android 侧无需权限的窗口标志（如 FLAG_SECURE）映射到带 @permission 的窗口 API（window.setWindowPrivacyMode），规格只凭源 Manifest 写“目标不声明任何权限”，并做成 requestPermissions 为空的静态验收或已批决策。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD；它是 system_basic 级的受限开放权限，还要 ACL 授权，没有时改用粘贴控件 PasteButton 读取，粘贴控件无需申请该权限）。
2. 汇总清单以工程中实际调用的受权限 API 为准：检索 sensor.on、deleteAssets、createAsset 等调用点与 requestPermissions 逐项对照（例：订阅加速度计、陀螺仪需 ohos.permission.ACCELEROMETER/GYROSCOPE，MediaAssetChangeRequest 写删需 ohos.permission.WRITE_IMAGEVIDEO）。读接口声明时取完整 JSDoc，不用过滤注释的 grep 丢掉 @permission 与 @throws 201；切片移交的权限需求与规格的“不需要”冲突时，以 d.ts 或 skill 文档核实后裁决，不以规格措辞否决有依据的移交；user_grant 权限同时补运行期请求与 reason 字符串；受限开放权限（如 WRITE_IMAGEVIDEO、READ_IMAGEVIDEO）还需签名配置中的受限权限授权，工程没有该授权时改走不需要它的路线（相机系统资产保存、showAssetsCreationDialog、picker），不把声明当作已获得。
3. 查到 @permission 后，在 SDK 的 openharmony/toolchains/lib/PermissionDefinitions.json（按文件名检索时不区分大小写）读该权限的 grantMode 与 availableLevel 再定写法：system_grant 且 normal 只需在 module.json5 声明、安装即授予；user_grant 另加运行期申请与 reason；availableLevel 为 system_basic 及以上才涉及 ACL 或签名授权，不凭记忆判级别（例：setWindowPrivacyMode 需 ohos.permission.PRIVACY_WINDOW，HarmonyOS 6.1.0(23) SDK 中为 system_grant、normal）。规格或已批决策写了“requestPermissions 为空/不声明任何权限”而所调 API 带 @permission 时，带 d.ts 行号与已核级别交决策方改判后写入；写全空的静态验收前，按规格列出的系统能力面逐个核 @permission，任何一个带权限就不写全空断言。

来源支持：5 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕剪贴板读取接口都标 @permission ohos.permission.READ_PASTEBOARD、缺权限抛 BusinessError 201：SystemPasteboard 的 getData(): Promise<PasteData>、getData(callback: AsyncCallback<PasteData>): void（首段 @since 9）和 getDataSync(): PasteData（首段 @since 11）；pasteboard 从 @kit.BasicServicesKit 导入
- 〔做法第 1 步〕ohos.permission.READ_PASTEBOARD 在受限开放权限列表里：权限级别 system_basic、授权方式 user_grant、起始版本 11；受限开放权限的开放范围是普通应用，但要通过 ACL 跨级别申请（调试阶段可改 HarmonyAppProvision 的 apl 重新签名，商用要在应用市场申请证书和 Profile）
- 〔做法第 1 步〕API 12 起剪贴板读取接口（getData、getDataSync、getUnifiedData 等）加了权限管控，访问方式两种：使用粘贴控件的应用可以无需申请权限；用自定义控件的应用走 READ_PASTEBOARD（ACL 申请 → module.json5 声明 → 弹窗向用户申请授权）
- 〔做法第 1 步〕粘贴控件 PasteButton（declare const PasteButton: PasteButtonInterface；PasteButton() 或 PasteButton(options: PasteButtonOptions)，首段 @since 10）：用户点击后应用获得临时授权，读剪贴板不弹窗；临时授权持续到灭屏、应用切后台或退出，授权期间调用次数不限；控件须可见可识别，样式不合法会授权失败
- 〔做法第 2 步〕sensor.on(type: SensorId.ACCELEROMETER, callback: Callback<AccelerometerResponse>, options?: Options): void 标 @permission ohos.permission.ACCELEROMETER，sensor.on(type: SensorId.GYROSCOPE, callback: Callback<GyroscopeResponse>, options?: Options): void 标 @permission ohos.permission.GYROSCOPE，都 @throws 201（首段 @since 9）；sensor 从 @kit.SensorServiceKit 导入
- 〔做法第 2、3 步〕ohos.permission.ACCELEROMETER、ohos.permission.GYROSCOPE：权限级别 normal、授权方式 system_grant、起始版本 7（文档与 SDK 6.1.0 的 PermissionDefinitions.json 一致）；normal 级权限不涉及证书授权字段，在 module.json5 声明即可
- 〔做法第 2 步〕媒体库写删接口的权限：MediaAssetChangeRequest.deleteAssets 两个重载（assets: Array<PhotoAsset> 与 uriList: Array<string>，都返回 Promise<void>，@since 11）、PhotoAccessHelper.createAsset 的三个重载（首段 @since 10）、PhotoAccessHelper.applyChanges(mediaChangeRequest: MediaChangeRequest): Promise<void>（@since 11）都标 @permission ohos.permission.WRITE_IMAGEVIDEO、缺权限抛 201；MediaAssetChangeRequest.createAssetRequest 本身没有 @permission，权限落在提交它的 applyChanges 上；photoAccessHelper 从 @kit.MediaLibraryKit 导入
- 〔做法第 2 步〕ohos.permission.WRITE_IMAGEVIDEO、ohos.permission.READ_IMAGEVIDEO 在受限开放权限列表里：权限级别 system_basic、授权方式 user_grant、起始版本 9，要经 ACL 跨级别申请，只在 module.json5 声明加运行时请求拿不到
- 〔做法第 2 步〕applyChanges 的文档写明：未申请 ohos.permission.WRITE_IMAGEVIDEO 时，可以用安全控件或授权弹窗的方式创建媒体资源
- 〔做法第 2 步〕PhotoAccessHelper.showAssetsCreationDialog(srcFileUris: Array<string>, photoCreationConfigs: Array<PhotoCreationConfig>): Promise<Array<string>>（@since 12，声明里没有 @permission）：显示保存确认弹窗，用户同意返回已创建并授予写权限的媒体库 URI 列表（永久生效），用户拒绝返回空列表；一次最多 100 张，只处理图片、视频 URI，不支持手动拼接的 URI；弹窗要显示应用名，module.json5 的 abilities 须配置 label 和 icon；PhotoCreationConfig 的 fileNameExtension、photoType 必填，title、subtype 可选（传 subtype 不生效）
- 〔做法第 2 步〕相机系统资产路线的接口：PhotoOutput.on(type: 'photoAssetAvailable', callback: AsyncCallback<photoAccessHelper.PhotoAsset>): void（首段 @since 12）；MediaAssetChangeRequest.saveCameraPhoto(): void（@since 12）与 saveCameraPhoto(imageFileType: ImageFileType): void（@since 13）的声明没有 @permission，文档示例为 new MediaAssetChangeRequest(asset) → saveCameraPhoto() → applyChanges；录像侧 AVRecorderConfig.fileGenerationMode?: FileGenerationMode（@since 12），AUTO_CREATE_CAMERA_SCENE = 1 由系统创建媒体文件、只在相机录像场景生效、忽略应用设的 URL，配合 on('photoAssetAvailable') 使用，APP_CREATE = 0 为应用在沙箱自建文件
- 〔做法第 2 步〕没有 WRITE_IMAGEVIDEO 受限权限签名授权的普通应用：在模拟器上经 createAsset 写入相册返回 201；相机照片经 photoAssetAvailable 拿到 PhotoAsset 后 saveCameraPhoto 提交、录像用 fileGenerationMode=AUTO_CREATE_CAMERA_SCENE 时能存入相册（applyChanges 的声明仍标 @permission WRITE_IMAGEVIDEO，这条路线的可用性以卡里实测为准）
- 〔做法第 3 步〕SDK 的 openharmony/toolchains/lib/PermissionDefinitions.json 顶层键 definePermissions，每项有 name、grantMode、availableLevel、since 等字段；HarmonyOS 6.1.0(23) SDK 中：PRIVACY_WINDOW、ACCELEROMETER、GYROSCOPE、NFC_TAG、INTERNET、VIBRATE、GET_NETWORK_INFO 为 system_grant / normal，READ_PASTEBOARD、WRITE_IMAGEVIDEO、READ_IMAGEVIDEO 为 user_grant / system_basic
- 〔做法第 3 步〕ohos.permission.PRIVACY_WINDOW：权限级别 normal、授权方式 system_grant、起始版本 9；变更信息：API 9–10 为 system_basic，API 11 起改为 normal
- 〔适用情境 / 做法第 3 步〕Window.setWindowPrivacyMode(isPrivacyMode: boolean): Promise<void> 与 setWindowPrivacyMode(isPrivacyMode: boolean, callback: AsyncCallback<void>): void（首段 @since 9）都标 @permission ohos.permission.PRIVACY_WINDOW，缺权限抛 201，窗口未创建或已销毁抛 1300002；window 从 @kit.ArkUI 导入
- 〔适用情境 / 做法第 3 步〕HarmonyOS 6.1.0(23) 设备上 module.json5 没有声明 PRIVACY_WINDOW 时，setWindowPrivacyMode 以 201 失败、hilog 有 PRIVACY_WINDOW PERMISSION_DENIED；声明后开启隐私模式截屏为黑、关闭后恢复
- 〔原因〕NFC 的 tag.registerForegroundDispatch 标 @permission ohos.permission.NFC_TAG（首段 @since 10；tag 从 @kit.ConnectivityKit 导入）；NFC_TAG 为 normal、system_grant
- 〔做法第 2、3 步〕module.json5 的 requestPermissions 每项：name 必填；申请 user_grant / manual_settings 权限时 reason 必填并需多语种适配，格式 $string:***；usedScene 必填，含 abilities（UIAbility 或 ExtensionAbility 名的数组）和 when（只能填 inuse 或 always）；system_grant 权限这两项选填。entry 模块声明的权限在整个应用生效，feature 模块无需重复声明
- 〔做法第 1、2 步〕运行期申请用 AtManager.requestPermissionsFromUser(context: Context, permissionList: Array<Permissions>): Promise<PermissionRequestResult>（另有 AsyncCallback 重载，首段 @since 9），查询是否已授予用 AtManager.checkAccessToken(tokenID: number, permissionName: Permissions): Promise<GrantStatus>（首段 @since 9）；abilityAccessCtrl 从 @kit.AbilityKit 导入
