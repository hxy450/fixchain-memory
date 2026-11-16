# pushNativeRoute 按源端 when(pageName) 建映射，不透传 pageName

审的是：代码
触发（任一种）：
- 读到：源端 `FlutterBoostDelegate.pushNativeRoute` 里用 `when (pageName)` 把各 Flutter pageName 常量分到不同原生 Activity，其余忽略；写错的样子：目标 `pushNativeRoute` 把 `options.getPageName()` 直接交给路由的 `push`，没有 pageName→鸿蒙路由的映射，也没有占位
适用范围：迁移 flutter_boost 的 FlutterBoostDelegate、Flutter 页要打开原生页时
做法：
- 照源端 when 的每个分支写 `switch (options.getPageName()) { case '<pageName 常量值>': <打开对应鸿蒙页的路由>; break; … }`，源端忽略的 pageName 目标也不处理
- 目标页还没迁的分支先写 `hilog.warn(...)` 占位，新增该页路由时回填这张映射
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushNativeRoute 里按 pageName 映射到已迁的鸿蒙页，未迁的分支留 warn：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- Flutter pageName 常量值和它对应的原生页：源工程里 FlutterBoostDelegate 实现的 pushNativeRoute，以及定义 pageName 常量的文件；读出每个 when 分支的常量字符串和它启动的 Activity，换成目标工程里该页的路由名
来源：1 张卡，1 个应用
- case-b98aad1336d85a238cd7（polypal-app-ohos）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断
