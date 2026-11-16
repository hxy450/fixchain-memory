# 插件选层前从缓存源码提取 MethodChannel 契约，channels 为空不下 F5 结论

审的是：规格
触发（任一种）：
- 读到：插件包的 Dart 源码和 *_android、platform_interface 实现里有 `MethodChannel` 名、方法、参数和平台回调的事件；写错的样子：插件的 solution 里 `channels` 是空列表，却给了 F5 / blocked 结论
适用范围：插件适配阶段为未决插件选替代层级之前
做法：
- 选层前从本地缓存源码（含 *_android 实现与 platform_interface）提取 MethodChannel 名、每个方法及其参数、平台回调的事件名，写进 channels
- channels 为空时不给 F5 结论，先补齐契约再判断
针对本应用要查的：
- 插件的 Channel 契约：本机 pub 缓存里该插件包、它的 *_android 实现包和 platform_interface 包的源码，按 MethodChannel 构造和方法名分派处找；记下通道名字符串、每个方法名和参数键、平台侧回调 Dart 的事件名
来源：1 张卡，1 个应用
- case-075213be62b42126e39f（app-photo-shop-flutter）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
