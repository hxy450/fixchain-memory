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
3. 查到 @permission 后，在 SDK 的 toolchains/lib/PermissionDefinitions.json（按文件名检索时不区分大小写）读该权限的 grantMode 与 availableLevel 再定写法：system_grant 且 normal 只需在 module.json5 声明、安装即授予；user_grant 另加运行期申请与 reason；availableLevel 为 system_basic 及以上才涉及 ACL 或签名授权，不凭记忆判级别（例：setWindowPrivacyMode 需 ohos.permission.PRIVACY_WINDOW，HarmonyOS 6.1.0(23) SDK 中为 system_grant、normal）。规格或已批决策写了“requestPermissions 为空/不声明任何权限”而所调 API 带 @permission 时，带 d.ts 行号与已核级别交决策方改判后写入；写全空的静态验收前，按规格列出的系统能力面逐个核 @permission，任何一个带权限就不写全空断言。

来源支持：5 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕pasteboard 的 getData / getDataSync 从 API 12 的声明段起带 @permission ohos.permission.READ_PASTEBOARD（API 11 的声明段没有），未授权时抛 201；经粘贴控件 PasteButton 读取剪贴板的应用无需申请该权限，点击控件得到的临时授权持续到灭屏、应用切后台或退出。〔成立范围：对 @ohos.pasteboard 的 SystemPasteboard 读取接口；同一接口在 d.ts 里有多段按版本叠加的 JSDoc，权限只写在较新的那段；最常见的不成立情形：粘贴控件样式不合法（尺寸、颜色使其不可识别）时授权失败。〕
- 〔做法第 1 步〕ohos.permission.READ_PASTEBOARD 在 SDK 权限定义里是 user_grant、availableLevel system_basic，属于受限开放权限：普通应用要先通过 ACL 方式申请，再在 module.json5 声明，并在运行期向用户申请授权。〔成立范围：对 HarmonyOS 6.1.0（API 23）SDK 的权限定义和对应文档；最常见的不成立情形：工程签名配置里没有该受限权限的 ACL 授权。〕
- 〔做法第 3 步〕SDK 权限定义里 ohos.permission.ACCELEROMETER、GYROSCOPE、NFC_TAG、PRIVACY_WINDOW 都是 system_grant、availableLevel normal，只需在 module.json5 声明、安装即授予，不需要运行期申请；READ_IMAGEVIDEO、WRITE_IMAGEVIDEO 是 user_grant、system_basic 的受限开放权限。〔成立范围：对 HarmonyOS 6.1.0（API 23）SDK 的 PermissionDefinitions.json；权限级别会随版本调整（文档举例 FILE_ACCESS_PERSIST 自 API 12 起改为 normal），以工程所用 SDK 为准；最常见的不成立情形：换用更早或更新的 SDK 时级别不同。〕
- 〔做法第 2 步〕module.json5 的 requestPermissions 里，申请 user_grant（或 manual_settings）权限时 reason 与 usedScene 都必填（usedScene.when 只能填 inuse 或 always），这两个字段用于应用上架校验；system_grant 权限这两个字段选填。〔成立范围：对 requestPermissions 的每一项；reason 用 $string 资源引用并需多语种适配；最常见的不成立情形：只补了 reason、漏了 usedScene。〕
- 〔做法第 1 步〕abilityAccessCtrl 的 requestPermissionsFromUser 在用户拒绝授权后不会再拉起弹框，需要用户在系统「设置」里手动授予，或调用 requestPermissionOnSetting（API 12 起）拉起权限设置弹框。〔成立范围：对 user_grant 权限的运行期申请；最常见的不成立情形：用户此前没有拒绝过时，requestPermissionsFromUser 仍会弹框。〕
- 〔适用情境〕安卓 ClipboardManager.getPrimaryClip() 不需要声明权限，但应用不是默认输入法且没有输入焦点时返回 null；鸿蒙读剪贴板则要 READ_PASTEBOARD 授权或经粘贴控件。〔成立范围：对 android.content.ClipboardManager 的读取，依据是 android-36.1 的 javadoc 说明（判定在系统剪贴板服务端，SDK 源码里看不到实现）；最常见的不成立情形：应用是默认输入法时不受输入焦点限制。〕
