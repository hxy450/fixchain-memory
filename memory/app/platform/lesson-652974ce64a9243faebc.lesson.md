# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

ID：`lesson-652974ce64a9243faebc` · 版本：2

[本主题](index.md)

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。 也包括 Android 端无需权限的窗口标志（如 FLAG_SECURE）映射到带 @permission 的窗口 API（window.setWindowPrivacyMode 需 ohos.permission.PRIVACY_WINDOW），规格或已批决策已写“目标不声明任何权限”。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD）。
2. 查到 @permission 后在 SDK 的 toolchains/lib/PermissionDefinitions.json 核 grantMode 与 availableLevel（文件名检索不区分大小写）：system_grant 且 normal 只需在 module.json5 声明、安装即授予；user_grant 另加运行期申请；system_basic 及以上才涉及 ACL 或签名授权。规格或已批决策写了“requestPermissions 为空/不声明任何权限”时，带 d.ts 行号与已核级别交决策方改判后写入，不凭未核实的级别维持空清单或把冲突挂成延期。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-0524405ca4510433cf06](../../../store/cases/case-0524405ca4510433cf06/4c21295f6ebe22983213cfee13bc1536c6e4e3cb5ab54f8042ca60663a8a84f7.json) · 结论：diagnosis, recommendation:5, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`4c21295f6ebe22983213cfee13bc1536c6e4e3cb5ab54f8042ca60663a8a84f7`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:5
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
