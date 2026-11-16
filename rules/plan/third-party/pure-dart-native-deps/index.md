# 纯 Dart 选图包依赖的原生媒体插件

agent 会看到什么：读到 pubspec 或 .flutter-plugins-dependencies 里纯 Dart 的选图 UI 包（如 wechat_assets_picker）依赖读系统媒体库的原生插件（如 photo_manager），插件分类结果是 keep_pure_dart / keep_existing_override；插件处理只围绕待处理列表做替代，原生插件没有功能和权限审查却列进 verified_local_or_pinned

## 规矩

- rule-ed05ec4691bc｜纯 Dart 选图包判为 keep_pure_dart 时，追到它调用的原生媒体插件一并审查｜读到：pubspec 或 `.flutter-plugins-dependencies` 里，纯 Dart 的选图 UI 包（如 wechat_assets_picker）依赖读系统媒体库的原生插件（如 photo_manager）；插件分类结果是 `keep_pure_dart` / `keep_existing_override`；写错：插件处理只围绕 adapted_review、needs_substitution 待处理列表做替代，选图链的原生插件没有功能和权限审查记录，却被列进 `verified_local_or_pinned`
