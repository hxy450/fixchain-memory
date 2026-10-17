# arkts/strict-mode

ArkTS 严格类型系统对对象字面量、接口实现、异常收窄与类声明顺序的限制，不编译时也会留到编译门

[上一级](../index.md)

## 本级经验

- [SDK 观察者声明为 class 时用类型标注的对象字面量](lesson-6e74f064efe2649fc295.lesson.md) · 阶段：execute/repair · 信号：errorManager.on('error'), ErrorObserver, onUnhandledException, onException
- [static 初始化器引用的类须先声明或从独立文件导入](lesson-f80ae7c3747420ef16f7.lesson.md) · 阶段：execute · 信号：AppStorageV2.connect, PersistenceV2.globalConnect, @ObservedV2, new Cls()
- [对象字面量写具名类，Record 替换用字段类或 Map](lesson-1696967d1320c7735732.lesson.md) · 阶段：execute/repair · 信号：Record&lt;string, Object&gt;, \[key: string\], Array&lt;{, constructor(public
- [接口参数用 implements 的具名类，不传函数字面量](lesson-931ef95a3d0cf202fe5b.lesson.md) · 阶段：execute/converge · 信号：Port, Repository, Adapter
- [重抛异常前先收窄为 Error，不直接 throw 变量](lesson-dbfae443e671c568e14e.lesson.md) · 阶段：execute/repair · 信号：throw error, instanceof Error, catch (, new Error(String(
