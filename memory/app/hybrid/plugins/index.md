# app/hybrid/plugins

Flutter pub 插件的 OHOS 替代：无现成包时的选层与阻断判定、标记可用前的权限与运行核对、本地兼容层交给冻结 Dart 业务的对象契约（尺寸元数据、分辨率与 UI 线程负载）

[上一级](../index.md)

## 本级经验

- [Flutter 插件标记可用前，按应用实际调用追到执行的原生实现，核对它请求的权限与返回状态；纯 Dart 上层包、同 API 的 OHOS 分支都不等于行为等价](lesson-4b7012d4bdceef5e8c36.lesson.md)
  - 时机：插件适配阶段，判定 Flutter 插件（纯 Dart 上层包、同包 OHOS 分支或本地化副本）可直接复用、标记 verified/build_verified，并据此决定应用 Dart 保持冻结时
  - 情境：业务经纯 Dart 上层包（如选图 UI）调用读系统媒体库的原生插件，或经权限插件请求 Android 专用权限组（如 Permission.storage）并以授予结果门控下载、保存等流程；插件已换成同 Dart API 的 OHOS 实现，pub get、HAP 构建与插件注册均通过。
- [Flutter 插件没有现成 OHOS 包时，先按底层能力评估本地兼容插件；判阻断要写明缺失能力，Dart 冻结下的显式失败也要由 OHOS 插件回调](lesson-45739c78f9767dacbc81.lesson.md)
  - 时机：插件适配阶段，为 Registry/pub 上没有 OHOS 实现的 Flutter 插件选择替代层级（同包分支、本地兼容插件、换包或阻断）并写 dependency_overrides 时
  - 情境：Flutter 复用路线且应用 Dart 冻结；某 federated 插件只声明 Android/iOS 实现，Registry 无对应 OHOS 包；其原生侧做的是 HTTP 上传、签名、文件读写等通用能力；Dart 调用方以 Future、Completer 或事件监听等待平台回调，并处在核心功能链上。
  - 例外：已逐项查明原生实现依赖的底层能力在 HarmonyOS 没有可用 Kit，且决策记录写明缺失能力与替代方案
- [兼容层交给冻结业务的对象，按全部消费方保留尺寸等元数据语义，并按下游处理上限先在原生侧缩放大图](lesson-e85bdb26fa6acc0cc9f7.lesson.md)
  - 时机：插件兼容层实现或返修阶段，决定把系统选择器结果、缓存副本以什么分辨率、带哪些元数据包装成原 API 对象交给冻结 Dart 业务，或为性能删改其中的计算时
  - 情境：Flutter 应用 Dart 冻结；本地兼容包把系统选择器结果包装成 AssetEntity 等原 API 对象，经共享入口分发给多个业务页面；下游有页面用对象宽高计算比例，有链路用 package:image 等纯 Dart 库在 UI isolate 同步解码、缩放、编码；用户可能选择千万像素级相机照片。
