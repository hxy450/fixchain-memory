# Flutter 调原生的分发（pushNativeRoute、MethodChannel）

agent 会看到什么：读到源端原生侧 FlutterBoostDelegate.pushNativeRoute 里 when (pageName) 分到各原生 Activity、setMethodCallHandler 里 when (call.method) 的分支；产物里 pushNativeRoute 把 getPageName() 直接交给路由 push，或 onMethodCall 只有按 Dart 枚举列出的 case、其余落到 notImplemented()

## 规矩

- rule-a38dae3f4f4a｜pushNativeRoute 按源端 when(pageName) 建映射，不透传 pageName｜读到：源端 `FlutterBoostDelegate.pushNativeRoute` 里用 `when (pageName)` 把各 Flutter pageName 常量分到不同原生 Activity，其余忽略；写错：目标 `pushNativeRoute` 把 `options.getPageName()` 直接交给路由的 `push`，没有 pageName→鸿蒙路由的映射，也没有占位
- rule-ce792bf7ad2c｜重写 MethodChannel handler 时，方法集合取源原生 handler 分支与 Dart 调用点的并集｜读到：源 Android 原生侧 setMethodCallHandler 里 when (call.method) 的分支含 Dart 方法枚举里没有的方法（如日志类 "log"），Dart 侧用字符串字面量 invokeMethod 调用，或调用点被注释；写错：目标 ArkTS 的 onMethodCall 只有契约里按 Dart 枚举列出的 case，源原生侧处理的其余方法落到 default 的 notImplemented()，也没登记不迁移
