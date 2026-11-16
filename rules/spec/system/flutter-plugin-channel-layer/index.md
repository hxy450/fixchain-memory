# Flutter 插件的 MethodChannel 契约和 OHOS 选层

agent 会看到什么：插件包的 Dart 源码、*_android / platform_interface 实现里有 MethodChannel、invokeMethod、原生 when (call.method) 分支，pubspec 只联邦 android/ios，插件的 solution 里 channels 为空或只按 Dart 枚举列方法，就给了 F5 / blocked 结论

## 规矩

- rule-680ccde0c72b｜插件选层前从缓存源码提取 MethodChannel 契约，channels 为空不下 F5 结论｜读到：插件包的 Dart 源码和 *_android、platform_interface 实现里有 `MethodChannel` 名、方法、参数和平台回调的事件；写错：插件的 solution 里 `channels` 是空列表，却给了 F5 / blocked 结论
- rule-63af6c94d462｜通道契约除 Dart 枚举外再列源原生 handler 全部分支，标出「原生已处理、Dart 未调用」｜读到：源原生侧 when (call.method) / switch 的分支比 Dart 侧方法枚举多（如日志类方法），Dart 侧有字符串字面量的 invokeMethod 或被注释的调用；写错：通道契约只按 Dart 侧方法枚举列方法，写「鸿蒙侧只需实现这 N 个方法即可」，没有源原生侧处理而枚举没有的方法
- rule-c0c685142a5f｜Registry 无 OHOS 包的插件，先写 F3 可行性：底层能力对应的 Kit，找不到才选 F5｜读到：插件 pubspec 只联邦 android/ios、Registry 没有 OHOS 包，但原生实现做的是 HTTP 上传、签名这类通用能力；写错：插件的 solution 里 `selected_layer` 写 F5、`status` 写 blocked，evidence 只有「Registry 无 OHOS 包」「只联邦 Android/iOS」，没有 F3 判断，也没写缺失的具体能力
- rule-7d644db93f92｜核心链路上、Dart 以 Future 等平台回调的插件不能只判阻断，要有 OHOS 插件｜读到：参考规格把插件放在核心功能链路上（如先上传取 URL 再调后续接口）；Dart 调用方用 `Future`、`Completer` 或监听等待平台回调；写错：插件记为 F5 blocked、没有任何 OHOS 插件，报告里归为 blocked non-core integration
