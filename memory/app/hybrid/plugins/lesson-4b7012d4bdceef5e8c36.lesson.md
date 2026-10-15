# Flutter 插件标记可用前，按应用实际调用追到执行的原生实现，核对它请求的权限与返回状态；纯 Dart 上层包、同 API 的 OHOS 分支都不等于行为等价

ID：`lesson-4b7012d4bdceef5e8c36` · 版本：1

[本主题](index.md)

## 何时使用

插件适配阶段，判定 Flutter 插件（纯 Dart 上层包、同包 OHOS 分支或本地化副本）可直接复用、标记 verified/build_verified，并据此决定应用 Dart 保持冻结时

## 适用情境

业务经纯 Dart 上层包（如选图 UI）调用读系统媒体库的原生插件，或经权限插件请求 Android 专用权限组（如 Permission.storage）并以授予结果门控下载、保存等流程；插件已换成同 Dart API 的 OHOS 实现，pub get、HAP 构建与插件注册均通过。

## 原因

依赖解析分类（keep_pure_dart、同包分支）只说明插件怎样接入，不说明 OHOS 实现请求哪些权限、在拒绝或无映射时返回什么；以构建和注册为证据标可用，权限差异要到用户操作时才暴露。来源两例：选图链实际执行的 photo_manager OHOS 实现走 photoAccessHelper 请求 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO，宿主只声明 INTERNET，请求被拒、图库不出现；permission_handler 的 OHOS 分支把 storage 组映射为空权限列表并判为拒绝，冻结 Dart 中无条件的存储权限门控使只写应用私有目录的下载直接失败。

## 做法

1. 对选图、保存、下载等链路从业务调用展开传递依赖，追到实际执行的原生插件；在其 OHOS 实现与 Dart 常量中检索 requestPermissions、ohosPermissions、photoAccessHelper 及权限组映射，列出每个方法所需权限和拒绝/无映射时的状态，与宿主 module.json5 对账，并在插件方案的 methods 中逐项记 implemented 或 unsupported。
2. 需要媒体库读写权限时，先确认当前应用能否申请；普通应用按系统选择器方案在本地兼容包中实现，并保持原 Dart API 与返回类型。
3. 权限组在 OHOS 映射为空或恒判拒绝、而被门控的操作只写应用私有目录（getApplicationDocumentsDirectory 等）时，把它列为 Dart 受控修改的必须修改点：加最小的 Platform.isOhos 跳过分支，其他平台保持原请求。
4. verified 标记以真机调用该链路（含拒绝、取消路径）的结果为依据；只有构建、注册器与宿主首屏证据时，记为待运行验证，不据此判定应用 Dart 无需修改。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3cc99a6c512ab85ed874](../../../../store/cases/case-3cc99a6c512ab85ed874/a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`a006127e89450a3a31fb06bc2eb26808f21a6b50e362b73fb9d6a87dd95fa906`
- [case-96b417fb2e059d43f8bf](../../../../store/cases/case-96b417fb2e059d43f8bf/b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b19ceb28695c5cd396d90d8eb8cdaf92306b067d26ce80fe0ba8b310d812ec4e`
