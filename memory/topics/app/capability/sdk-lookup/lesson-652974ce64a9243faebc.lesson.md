# 写目标权限清单时按每个已映射系统 API 在 SDK d.ts 中的 @permission 汇总，不因 Android 端无需运行时权限就断言 requestPermissions 为空

ID：`lesson-652974ce64a9243faebc` · 版本：2 · 阶段：spec/execute · 主题：[app/capability/sdk-lookup](index.md)

概要：权限按目标 API 的 @permission 汇总

信号：`@permission`, `requestPermissions`, `module.json5`, `ohos.permission.READ_PASTEBOARD`, `pasteboard.getData`, `@ohos.pasteboard`, `ClipboardManager`, `NFC_TAG`

## 何时使用

规格提取（权限契约）与实现阶段，确定 module.json5 的 requestPermissions 与运行期申请时

## 适用情境

源端读剪贴板等操作在 Android 上无需声明或运行时授权；目标把 ClipboardManager 等映射到 @ohos.pasteboard 等 Kit API；规格的权限段只写了最显眼的能力（如“NFC Kit 免权限、requestPermissions 为空”），各页直接调用这些 API。

## 原因

目标 API 的权限要求写在 d.ts 的 @permission 注解里，与 Android 是否需要权限无关；按源端权限清单推断，会漏掉目标独有的权限（如 pasteboard.getData 需要 ohos.permission.READ_PASTEBOARD），调用在运行时失败。来源中权限契约写成“requestPermissions 为空”，唯一的权限写者只按 NFC d.ts 补了 NFC_TAG，剪贴板读取权限直到修复期查 d.ts 才补上。

## 做法

1. 每映射一个系统 API，就查它在 SDK d.ts 中的 @permission，把汇总结果写进权限契约与 module.json5，并为需要用户授权的权限安排运行期申请（如读剪贴板前申请 READ_PASTEBOARD）。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [manifest 未声明的窗口缺省解析成目标值并指派](../../entry/lesson-c1d7ec16bb02aa152c33.lesson.md)（共享 1 张卡）
- [持久化主题在 loadContent 前同步设好](../../startup/lesson-dcb3c5e66dec2d126234.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-cc22f6cc1041c8cc1129](../../../../../store/cases/case-cc22f6cc1041c8cc1129/ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3.json) · 结论：rec-39c7fa7430
  卡片版本：`ec6e60182fe19865967b7c173312ac2be6c4dbf45c87407c6da85b673b5778f3`
