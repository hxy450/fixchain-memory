# Flutter 插件标记可用前，按应用实际调用追到执行的原生实现，核对它请求的权限与返回状态；纯 Dart 上层包、同 API 的 OHOS 分支都不等于行为等价

## 何时使用

插件适配阶段，判定 Flutter 插件（纯 Dart 上层包、同包 OHOS 分支或本地化副本）可直接复用、标记 verified/build_verified，并据此决定应用 Dart 保持冻结时

## 适用情境

业务经纯 Dart 上层包（如选图 UI）调用读系统媒体库的原生插件，或经权限插件请求 Android 专用权限组（如 Permission.storage）并以授予结果门控下载、保存等流程；插件已换成同 Dart API 的 OHOS 实现，pub get、HAP 构建与插件注册均通过。

## 例外与边界

- 第 2 步的系统选择器只覆盖“读”（让用户选图、选视频）；链路是把图片、视频写进图库时，普通应用改用保存安全控件或授权弹窗（showAssetsCreationDialog）保存，同样不申请 WRITE_IMAGEVIDEO，Dart API 与返回类型照样保持

## 原因

依赖解析分类（keep_pure_dart、同包分支）只说明插件怎样接入，不说明 OHOS 实现请求哪些权限、在拒绝或无映射时返回什么；以构建和注册为证据标可用，权限差异要到用户操作时才暴露。来源两例：选图链实际执行的 photo_manager OHOS 实现走 photoAccessHelper 请求 READ_IMAGEVIDEO/WRITE_IMAGEVIDEO，宿主只声明 INTERNET，请求被拒、图库不出现；permission_handler 的 OHOS 分支把 storage 组映射为空权限列表并判为拒绝，冻结 Dart 中无条件的存储权限门控使只写应用私有目录的下载直接失败。

## 做法

1. 对选图、保存、下载等链路从业务调用展开传递依赖，追到实际执行的原生插件；在其 OHOS 实现与 Dart 常量中检索 requestPermissions、ohosPermissions、photoAccessHelper 及权限组映射，列出每个方法所需权限和拒绝/无映射时的状态，与宿主 module.json5 对账，并在插件方案的 methods 中逐项记 implemented 或 unsupported。
2. 需要媒体库读写权限时，先确认当前应用能否申请；普通应用按系统选择器方案在本地兼容包中实现，并保持原 Dart API 与返回类型。
3. 权限组在 OHOS 映射为空或恒判拒绝、而被门控的操作只写应用私有目录（getApplicationDocumentsDirectory 等）时，把它列为 Dart 受控修改的必须修改点：加最小的 Platform.isOhos 跳过分支，其他平台保持原请求。
4. verified 标记以真机调用该链路（含拒绝、取消路径）的结果为依据；只有构建、注册器与宿主首屏证据时，记为待运行验证，不据此判定应用 Dart 无需修改。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 3 步〕permission_handler 的 OHOS 分支把 storage 权限组映射为空的权限列表，请求该组时状态判为 DENIED
- 〔做法第 3 步〕鸿蒙应用可以在应用文件目录下保存和处理自己的文件，不需要申请权限；访问用户文件才要走用户文件的方式
- 〔做法第 3 步〕安卓 Context#getDataDir 返回存放本应用全部私有文件的目录
- 〔做法第 1 步〕ohos.permission.INTERNET 的权限级别是 normal、授权方式是 system_grant
- 〔原因 / 做法第 2 步〕ohos.permission.READ_IMAGEVIDEO、WRITE_IMAGEVIDEO 的权限级别是 system_basic、授权方式是 user_grant，属受限开放权限：普通应用要通过 ACL 跨级申请，使用前需额外申请 ACL 白名单
- 〔做法第 2 步〕PhotoViewPicker 拉起系统图库让用户选择，接口本身无需申请权限，目前适用于界面 UIAbility
- 〔做法第 1 步〕APL 为 normal 的应用只能使用 normal 级权限，声明了 system_basic 或 system_core 级权限时安装报 9568289 install failed due to grant request permissions failed
- 〔做法第 1 步〕module.json5 里申请 user_grant 权限时 reason、usedScene 必填，usedScene.when 只能填 inuse 或 always
