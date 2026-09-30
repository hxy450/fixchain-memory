# app/hybrid

Flutter 与原生混合工程：MethodChannel handler 的方法集合、flutter_boost 宿主页的事件通道、原生路由分流，以及 Flutter pub 插件在 OHOS 上的替代与本地兼容层

[上一级](../index.md)

## 子主题

- [plugins](plugins/index.md) — Flutter pub 插件的 OHOS 替代：无现成包时的选层与阻断判定、标记可用前的权限与运行核对、本地兼容层交给冻结 Dart 业务的对象契约（尺寸元数据、分辨率与 UI 线程负载）

## 本级经验

- [FlutterBoostDelegate.pushNativeRoute 按源端 when(pageName) 建 Flutter 页面名到鸿蒙路由的映射，不直接透传](lesson-6587c954fd44464a7382.lesson.md)
  - 时机：实现 flutter_boost 原生路由代理时，以及之后新增原生页面路由时
  - 情境：Flutter 侧用 pageName（如 xxx_native）请求打开原生页，源端 pushNativeRoute 用 when(page) 把各 pageName 分流到对应 Activity、其余忽略；flutter_boost 示例把 pageName 直接交给路由。
- [原生 MethodChannel handler 的方法集合按源原生分支全集与 Dart 调用点双向对照，不以契约列出的方法数为完成标准](lesson-e6b1032f702fc61940f2.lesson.md)
  - 时机：混合工程的通道契约提取与原生桥接实现阶段，确定鸿蒙侧 MethodChannel handler 要实现哪些方法时
  - 情境：Flutter 与原生共用一个 MethodChannel；契约只按 Dart 侧方法名枚举列方法，源 Android 原生 handler 还处理枚举以外的方法（如 log），Dart 侧用字符串字面量调用，或调用点当前被注释。
- [迁移嵌入 Flutter 页面的原生宿主时打开实际挂载的容器子类，逐项迁移事件监听与反向推送，不只挂 FlutterUIComponent](lesson-6717b958e274143453a8.lesson.md)
  - 时机：原生宿主迁移与规格提取阶段，把承载 Flutter 页面的 Activity/Fragment 转成 ArkTS 页面，确定宿主除挂容器外还要承担哪些原生↔Flutter 通信时
  - 情境：源端宿主经 flutter_boost 挂载的是自定义 FlutterBoostFragment 子类，在其中 addEventListener(通道名) 分发 Flutter 事件、sendEventToFlutter 反向推数据；事件名常量、桥接 Model 与宿主分散在不同源文件；契约可能把这类桥接标成“待 Feature Spec”。
