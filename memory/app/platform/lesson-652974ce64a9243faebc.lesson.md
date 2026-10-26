# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

ID：`lesson-652974ce64a9243faebc` · 版本：4

[本主题](index.md)

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。也包括规格权限节只按 AndroidManifest 逐项映射（如把旧版存储权限写成“不需要，走媒体库”），而目标改用的传感器订阅、媒体资产写入与删除等 API 在 d.ts 中带 @permission；清单由规格权限节与各切片移交汇总生成。 也包括源端在 Android 侧无需权限的窗口标志（如 FLAG_SECURE）映射到带 @permission 的窗口 API（window.setWindowPrivacyMode），规格只凭源 Manifest 写“目标不声明任何权限”，并做成 requestPermissions 为空的静态验收或已批决策。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD）。
2. 汇总清单以工程中实际调用的受权限 API 为准：检索 sensor.on、deleteAssets、createAsset 等调用点与 requestPermissions 逐项对照（例：订阅加速度计、陀螺仪需 ohos.permission.ACCELEROMETER/GYROSCOPE，MediaAssetChangeRequest 写删需 ohos.permission.WRITE_IMAGEVIDEO）。读接口声明时取完整 JSDoc，不用过滤注释的 grep 丢掉 @permission 与 @throws 201；切片移交的权限需求与规格的“不需要”冲突时，以 d.ts 或 skill 文档核实后裁决，不以规格措辞否决有依据的移交；user_grant 权限同时补运行期请求与 reason 字符串；受限开放权限（如 WRITE_IMAGEVIDEO、READ_IMAGEVIDEO）还需签名配置中的受限权限授权，工程没有该授权时改走不需要它的路线（相机系统资产保存、showAssetsCreationDialog、picker），不把声明当作已获得。
3. 查到 @permission 后，在 SDK 的 toolchains/lib/PermissionDefinitions.json（按文件名检索时不区分大小写）读该权限的 grantMode 与 availableLevel 再定写法：system_grant 且 normal 只需在 module.json5 声明、安装即授予；user_grant 另加运行期申请与 reason；availableLevel 为 system_basic 及以上才涉及 ACL 或签名授权，不凭记忆判级别（例：setWindowPrivacyMode 需 ohos.permission.PRIVACY_WINDOW，HarmonyOS 6.1.0(23) SDK 中为 system_grant、normal）。规格或已批决策写了“requestPermissions 为空/不声明任何权限”而所调 API 带 @permission 时，带 d.ts 行号与已核级别交决策方改判后写入；写全空的静态验收前，按规格列出的系统能力面逐个核 @permission，任何一个带权限就不写全空断言。

来源支持：5 张卡 · 已知 3 次迁移（部分未记录） · 已知 3 个应用（部分未记录）

## 来源（按需复核）

- [case-0524405ca4510433cf06](../../../store/cases/case-0524405ca4510433cf06/4c21295f6ebe22983213cfee13bc1536c6e4e3cb5ab54f8042ca60663a8a84f7.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`4c21295f6ebe22983213cfee13bc1536c6e4e3cb5ab54f8042ca60663a8a84f7`
- [case-149fd657e7134bf86261](../../../store/cases/case-149fd657e7134bf86261/76fbb9c3cf5c8c90f368c676283ddd9f80585443f0d66eee63ccee0b2aaaf3b2.json) · 结论：recommendation:2
  卡片版本：`76fbb9c3cf5c8c90f368c676283ddd9f80585443f0d66eee63ccee0b2aaaf3b2`
- [case-58c3f872e3c907fb4b68](../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：recommendation:4
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
- [case-68b4a8d96f961e70b0c9](../../../store/cases/case-68b4a8d96f961e70b0c9/386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:5
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
