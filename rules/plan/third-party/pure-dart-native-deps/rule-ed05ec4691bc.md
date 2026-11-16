# 纯 Dart 选图包判为 keep_pure_dart 时，追到它调用的原生媒体插件一并审查

审的是：计划与派工
触发（任一种）：
- 读到：pubspec 或 `.flutter-plugins-dependencies` 里，纯 Dart 的选图 UI 包（如 wechat_assets_picker）依赖读系统媒体库的原生插件（如 photo_manager）；插件分类结果是 `keep_pure_dart` / `keep_existing_override`；写错的样子：插件处理只围绕 adapted_review、needs_substitution 待处理列表做替代，选图链的原生插件没有功能和权限审查记录，却被列进 `verified_local_or_pinned`
适用范围：Flutter 工程适配 OHOS 的插件判定阶段，图片、媒体选择链上的插件
做法：
- 对图片/媒体选择链展开传递依赖：上层纯 Dart 包也追到它实际调用的原生插件，把该原生插件列为要做功能与权限审查的一项
- 记录里写明 keep_pure_dart、keep_existing_override 只说明依赖怎么解析，不算审查通过，不能据此标 verified
针对本应用要查的：
- 选图链上的上层包实际调用了哪些原生插件：源工程的 `.flutter-plugins-dependencies`（列出各平台的原生插件）和上层包自己的 pubspec 依赖；上层包 pubspec 里依赖、且出现在 `.flutter-plugins-dependencies` 的 ohos 段的插件，就是要审的原生插件
来源：1 张卡，1 个应用
- case-96b417fb2e059d43f8bf（app-photo-shop-flutter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1
