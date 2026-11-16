# 三方 SDK 与插件

规格、skill 映射表、pubspec 或 .flutter-plugins-dependencies 里有要平台 Key 的厂商 SDK（如 com.amap.api）、Flutter 插件和它依赖的原生插件时

## 触发族

- [计划里要平台 Key 的厂商 SDK](vendor-sdk/index.md)（2 条）：规格或 skill 映射表里有高德等要平台 Key 的厂商 SDK（com.amap.api、PoiSearchV2），计划的步骤只挂了 hmos-sdk-docs 或连它都没有，scope 里没有 ohpm 依赖、初始化和 Key 注入
- [纯 Dart 选图包依赖的原生媒体插件](pure-dart-native-deps/index.md)（1 条）：读到 pubspec 或 .flutter-plugins-dependencies 里纯 Dart 的选图 UI 包（如 wechat_assets_picker）依赖读系统媒体库的原生插件（如 photo_manager），插件分类结果是 keep_pure_dart / keep_existing_override；插件处理只围绕待处理列表做替代，原生插件没有功能和权限审查却列进 verified_local_or_pinned
