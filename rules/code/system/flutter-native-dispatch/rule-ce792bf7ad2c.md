# 重写 MethodChannel handler 时，方法集合取源原生 handler 分支与 Dart 调用点的并集

审的是：代码
触发（任一种）：
- 读到：源 Android 原生侧 setMethodCallHandler 里 when (call.method) 的分支含 Dart 方法枚举里没有的方法（如日志类 "log"），Dart 侧用字符串字面量 invokeMethod 调用，或调用点被注释；写错的样子：目标 ArkTS 的 onMethodCall 只有契约里按 Dart 枚举列出的 case，源原生侧处理的其余方法落到 default 的 notImplemented()，也没登记不迁移
适用范围：Flutter 与原生共用 MethodChannel、在鸿蒙侧用 ArkTS 重写原生 handler 时
做法：
- 把源原生 handler 的分支全集和 Dart 侧调用点（含字符串字面量和被注释的调用）双向对照；源原生侧处理、Dart 枚举没有的方法逐个写 case 实现，或写明不迁移的理由，不以契约里的方法数作完成标准
- 日志类方法照源端做：case 'log' 里用 hilog.info(domain, tag, 'Flutter log: %{public}s', 参数字符串) 打印，再像源端一样回 success
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function info(domain: number, tag: string, format: string, ...args: any[]): void：hilog 输出 INFO 级日志（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.info）
- 隐私标识分 {public} 和 {private}，缺省为 {private}；{public} 明文输出，{private} 以 <private> 回显：要看到通道传来的日志内容，格式串写 %{public}s（出处：js-apis-hilog.md，hilog.info）
- onMethodCall 加 case 'log'，用 hilog.info 打印 'Flutter log: %{public}s'，和源端 logD 做法一致：修复后的日志分支（出处：卡里修好并验证过）
针对本应用要查的：
- 源原生 handler 实际处理的方法名全集：源工程里调用 setMethodCallHandler 的 Kotlin / Java 文件中 when (call.method) / switch 的各分支，以及分支用到的方法名常量定义；把常量解析成字面量逐个列出，和 Dart 侧方法枚举、invokeMethod 字面量做双向差集
未核实：卡里的行为出自 API 22（HarmonyOS 6.0.2），本机声明是 API 23
来源：1 张卡，1 个应用
- case-1a0896800abf7e6439f2（polypal-app-ohos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；取值 3 ← 诊断
