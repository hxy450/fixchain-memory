# app/hybrid/plugins

Flutter pub 插件的 OHOS 替代：无现成包时的选层与阻断判定、标记可用前追到原生实现的权限与运行核对、本地兼容层交给冻结 Dart 业务的对象契约（尺寸元数据不以 0 占位）与下游同步处理原图时的预缩放

[上一级](../index.md)

## 本级经验

- [Flutter 插件标记可用前，按业务调用追到实际执行的原生插件，核对其 OHOS 实现请求的权限与拒绝、无映射时的返回](lesson-4b7012d4bdceef5e8c36.lesson.md)
  - 时机：插件适配阶段，判定 Flutter 插件（纯 Dart 上层包、同包 OHOS 分支或本地化副本）可直接复用、标记 verified/build_verified，并据此决定应用 Dart 保持冻结时
  - 情境：业务经纯 Dart 上层包（如选图 UI）调用读系统媒体库的原生插件，或经权限插件请求权限组并以授予结果门控下载、保存等流程；插件已换成同 Dart API 的 OHOS 实现，pub get、HAP 构建与插件注册均通过。
- [Flutter 插件没有现成 OHOS 包时，先按底层能力评估本地兼容插件；判阻断要写明缺失能力，Dart 冻结下的显式失败也要由 OHOS 插件回调](lesson-45739c78f9767dacbc81.lesson.md)
  - 时机：插件适配阶段，为 Registry/pub 上没有 OHOS 实现的 Flutter 插件选择替代层级（同包分支、本地兼容插件、换包或阻断）并写 dependency_overrides 时
  - 情境：Flutter 复用路线且应用 Dart 冻结；某 federated 插件只声明 Android/iOS 实现，Registry 无对应 OHOS 包；其原生侧做的是 HTTP 上传、签名、文件读写等通用能力；Dart 调用方以 Future、Completer 或事件监听等待平台回调，并处在核心功能链上。
  - 例外：已逐项查明原生实现依赖的底层能力在 HarmonyOS 没有可用 Kit，且决策记录写明缺失能力与替代方案
- [兼容层把选图结果包装成原 API 对象（如 AssetEntity）交给冻结 Dart 业务时，按全部消费方保留宽高等元数据，不以 0 占位](lesson-e85bdb26fa6acc0cc9f7.lesson.md)
  - 时机：插件兼容层实现或返修阶段，决定原 API 对象带哪些元数据，或为性能删改其中的计算时
  - 情境：Flutter 应用 Dart 冻结；本地兼容包把系统选择器结果或缓存副本包装成 AssetEntity 等原 API 对象，经共享入口分发给多个业务页面；下游有页面用对象宽高计算比例；修复者准备为省去整图解码删掉尺寸计算。
- [冻结 Dart 下游在 UI isolate 同步解码、缩放原图时，兼容层先用原生图片引擎按业务上限缩放，避免 OHOS 主线程阻塞被结束进程](lesson-34fb5eb76f00951848b5.lesson.md)
  - 时机：插件兼容层实现阶段，决定系统选图结果以什么分辨率交给冻结的 Dart 业务时
  - 情境：下游业务链用 package:image 等纯 Dart 库在 UI isolate 对所选原图同步 decode、copyResize、encode（如上传前压缩），业务自身有长边上限；用户可能选择千万像素级相机照片；同一 Dart 代码在 Android 上没有报卡死。
  - 例外：下游已在独立 isolate 处理，或只传递文件路径、不做像素运算时，保持原图交付
- [冻结 Dart 以 Permission.storage 等 Android 专用权限组门控只写私有目录的操作时，为 OHOS 加最小跳过分支](lesson-2a5d3fb905dba47fba03.lesson.md)
  - 时机：Dart 受控修改阶段，处理经 permission_handler 一类插件请求、在 OHOS 没有对应系统权限的权限组门控时
  - 情境：应用 Dart 无条件调用 Permission.storage.request()、manageExternalStorage 等 Android 专用权限组，并以授予结果门控下载、保存；被门控的操作只写应用私有目录（getApplicationDocumentsDirectory 等）；权限插件已换成同 API 的 OHOS 分支，该分支把这类权限组映射为空权限列表并判为拒绝。
  - 例外：被门控的操作确实写公共媒体库或共享目录时，按目标平台对应的权限或系统选择器方案处理，不跳过门控
