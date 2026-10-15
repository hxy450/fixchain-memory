# 写目标权限清单时按已映射 API 在 d.ts 中的 @permission 汇总，并按权限级别选申请方式，不因 Android 无需权限就断言为空

ID：`lesson-652974ce64a9243faebc` · 版本：4

[本主题](index.md)

## 何时使用

规格提取（权限契约）、实现与构建收口阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断会漏掉目标独有的权限，这些权限既不声明也不申请。权限还有级别与授权方式之分：PermissionDefinitions.json 里 availableLevel 为 system_basic 及以上的权限（如 READ_PASTEBOARD），普通应用只声明加运行期申请拿不到。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5。
2. 对每个权限查 SDK toolchains/lib/PermissionDefinitions.json 的 grantMode 与 availableLevel：normal 级的 user_grant 权限声明后安排运行期申请；system_basic 及以上的（如 READ_PASTEBOARD）改用 d.ts 说明的用户触发路径（读剪贴板用 PasteButton 安全控件，用户点击后获得读取当前剪贴板的授权，见 component/paste_button.d.ts）或登记 ACL 申请，不只写运行期申请。
3. 构建日志出现“To use this API, you need to apply for the permissions: X”时，把 X 与 module.json5 的 requestPermissions 逐项对照；缺项先补声明或按上一步换授权路径，不判构建或权限检查 PASS。权限声明按实际调用的 API 汇总，不照抄仓库中已有的单个权限字符串。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-8c249997059a2524ea7b](../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：recommendation:5, diagnosis
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-cc22f6cc1041c8cc1129](../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：recommendation:5, diagnosis
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
