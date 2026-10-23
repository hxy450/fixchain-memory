# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

ID：`lesson-652974ce64a9243faebc` · 版本：3 · 阶段：spec/execute · 主题：[app/capability/sdk-lookup](index.md)

概要：权限按目标 API 的 @permission 汇总

信号：`@permission`, `requestPermissions`, `module.json5`, `ohos.permission.READ_PASTEBOARD`, `pasteboard.getData`, `@ohos.pasteboard`, `ClipboardManager`, `NFC_TAG`, `availableLevel`, `system_basic`

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。 也包括目标 API 要求的权限在 d.ts 中写作 user_grant、在 SDK 权限定义里 availableLevel 却高于 normal（如媒体库读写），写者只按 user_grant 做声明与运行期申请。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。 grantMode 只说明授权方式；availableLevel 为 system_basic/system_core 的权限，普通应用声明并在运行期申请后仍拿不到（一次设备观察：声明并申请后写入仍返回 201）。API 24 的 toolchains/lib/PermissionDefinitions.json 中 WRITE_IMAGEVIDEO、READ_IMAGEVIDEO 为 user_grant、availableLevel system_basic。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD）。 同时在 SDK toolchains/lib/PermissionDefinitions.json 查该权限的 availableLevel：高于 normal 的权限需在签名 profile 中申请受限权限，工程没有该授权时改选不依赖该权限的 API 路线，或登记签名依赖。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [最近媒体以自存 URI 为准，未授权不整库查询](../../media-library/lesson-43781ac1c21274acd48b.lesson.md)（共享 1 张卡）
- [资产回调无请求 ID 时一拍一输出，超时退役不串帧](../../camera/capture/lesson-8a1d50b9fdcdee8a5752.lesson.md)（共享 1 张卡）
- [相机产出走系统资产保存，不靠受限写权限](../../media-library/lesson-bc279ce222e98e0d5ede.lesson.md)（共享 1 张卡）
- [manifest 未声明的窗口缺省解析成目标值并指派](../../entry/lesson-c1d7ec16bb02aa152c33.lesson.md)（共享 1 张卡）
- [降采样改 desiredSize，方向按字符串映射](../../media/lesson-c61656e804e536885d20.lesson.md)（共享 1 张卡）

来源支持：4 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-58c3f872e3c907fb4b68](../../../../../store/cases/case-58c3f872e3c907fb4b68/8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36.json) · 结论：diagnosis, rec-437623b648
  卡片版本：`8f81496786965152a90c44e6cfca277833ac24fc4296e7268a881109215d0a36`
- [case-68b4a8d96f961e70b0c9](../../../../../store/cases/case-68b4a8d96f961e70b0c9/386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2.json) · 结论：rec-d7102f189c, rec-bbdd28d7dc, rec-d90a502c8e
  卡片版本：`386ad956262b8b2f06c0b86906195cab8fc5c3e9421247edab32f5faea6bc8a2`
- [case-cc22f6cc1041c8cc1129](../../../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：rec-39c7fa7430
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
- [case-d5c3514ada560cb5134d](../../../../../store/cases/case-d5c3514ada560cb5134d/f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f.json) · 结论：rec-48b6863aac
  卡片版本：`f08e3534f55b8cc6ebd570ff39c426fb4462edec6d303e3d2574fe5789a9b67f`
