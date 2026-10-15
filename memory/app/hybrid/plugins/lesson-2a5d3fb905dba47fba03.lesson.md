# 冻结 Dart 以 Permission.storage 等 Android 专用权限组门控只写私有目录的操作时，为 OHOS 加最小跳过分支

ID：`lesson-2a5d3fb905dba47fba03` · 版本：1

[本主题](index.md)

## 何时使用

Dart 受控修改阶段，处理经 permission_handler 一类插件请求、在 OHOS 没有对应系统权限的权限组门控时

## 适用情境

应用 Dart 无条件调用 Permission.storage.request()、manageExternalStorage 等 Android 专用权限组，并以授予结果门控下载、保存；被门控的操作只写应用私有目录（getApplicationDocumentsDirectory 等）；权限插件已换成同 API 的 OHOS 分支，该分支把这类权限组映射为空权限列表并判为拒绝。

## 例外与边界

- 被门控的操作确实写公共媒体库或共享目录时，按目标平台对应的权限或系统选择器方案处理，不跳过门控

## 原因

OHOS 没有与 Android 存储权限组对应的系统权限，权限插件的 OHOS 分支对空映射返回拒绝；冻结 Dart 中无条件的权限门因此恒失败，只写应用私有目录、本不需要权限的下载直接失败。只复核 Platform 分支的 Dart 适配扫描发现不了这类无条件门控。

## 做法

1. Dart 适配阶段除 Platform 分支外，再检索无条件的 Android 专用权限请求（Permission.storage、manageExternalStorage 等），并在权限插件 OHOS 分支中查该组的映射与空映射时的返回状态。
2. 映射为空或恒判拒绝、而被门控的操作只写应用私有目录时，在门控开头加最小的 if (Platform.isOhos) 跳过分支，其他平台保持原请求与拒绝处理。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3cc99a6c512ab85ed874](../../../../store/cases/case-3cc99a6c512ab85ed874/a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906`
