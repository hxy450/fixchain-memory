# Flutter 插件标记可用前，按业务调用追到实际执行的原生插件，核对其 OHOS 实现请求的权限与拒绝、无映射时的返回

ID：`lesson-4b7012d4bdceef5e8c36` · 版本：2

[本主题](index.md)

## 何时使用

插件适配阶段，判定 Flutter 插件（纯 Dart 上层包、同包 OHOS 分支或本地化副本）可直接复用、标记 verified/build_verified，并据此决定应用 Dart 保持冻结时

## 适用情境

业务经纯 Dart 上层包（如选图 UI）调用读系统媒体库的原生插件，或经权限插件请求权限组并以授予结果门控下载、保存等流程；插件已换成同 Dart API 的 OHOS 实现，pub get、HAP 构建与插件注册均通过。

## 原因

依赖解析分类（keep_pure_dart、同包分支）只说明插件怎样接入，不说明 OHOS 实现请求哪些权限、在拒绝或无映射时返回什么；以构建和注册为证据标可用，权限差异要到用户操作时才暴露。

## 做法

1. 对选图、保存、下载等链路从业务调用展开传递依赖，追到实际执行的原生插件；在其 OHOS 实现与 Dart 常量中检索 requestPermissions、ohosPermissions、photoAccessHelper 及权限组映射，列出每个方法所需权限和拒绝/无映射时的状态，与宿主 module.json5 对账，并在插件方案的 methods 中逐项记 implemented 或 unsupported。
2. 所需权限是普通应用不能申请的媒体库读写权限时，选图改走系统选择器（lesson-ad1db0aa0434c2e766fd）；权限组在 OHOS 映射为空或恒判拒绝时，把应用 Dart 中对应的门控列为必须修改点交给 Dart 受控修改，不以 build_verified 放行。
3. verified 标记以真机调用该链路（含拒绝、取消路径）的结果为依据；只有构建、注册器与宿主首屏证据时不标 verified，也不据此判定应用 Dart 无需修改，把真机走该链路列入验收项。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3cc99a6c512ab85ed874](../../../../store/cases/case-3cc99a6c512ab85ed874/a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906`
- [case-96b417fb2e059d43f8bf](../../../../store/cases/case-96b417fb2e059d43f8bf/b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e`
