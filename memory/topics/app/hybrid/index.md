# app/hybrid

Flutter 与原生桥接契约：通道方法集、事件通道、路由映射，以及交给冻结 Dart 的对象语义与行为等价核对

[上一级](../index.md)

## 本级经验

- [Flutter 宿主迁移要打开实际容器子类逐项迁事件桥接](lesson-6717b958e274143453a8.lesson.md) · 阶段：spec/execute · 信号：FlutterBoostFragment, addEventListener, sendEventToFlutter, FlutterUIComponent
- [pushNativeRoute 按页面名建路由映射表不透传](lesson-6587c954fd44464a7382.lesson.md) · 阶段：execute · 信号：FlutterBoostDelegate, pushNativeRoute, pageName, flutter_boost
- [兼容层返回对象保留宽高语义，大图先在原生侧缩放](lesson-e85bdb26fa6acc0cc9f7.lesson.md) · 阶段：execute/repair · 信号：AssetEntity, ImageSource, getImageInfo, compressAndGetFile
- [插件标可用前追到原生实现核对权限与返回状态](lesson-4b7012d4bdceef5e8c36.lesson.md) · 阶段：verify · 信号：requestPermissions, ohosPermissions, photoAccessHelper, Permission.storage
- [通道方法集按原生分支全集与 Dart 调用点双向对照](lesson-e6b1032f702fc61940f2.lesson.md) · 阶段：spec/execute · 信号：MethodChannel, setMethodCallHandler, call.method, invokeMethod
