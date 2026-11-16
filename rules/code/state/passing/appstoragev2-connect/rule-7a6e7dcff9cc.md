# static 字段初始化器或模块级常量把类当值用时，这个类要声明在使用者之上或从别的文件 import

审的是：代码
触发（任一种）：
- 写错的样子：服务类里 `static readonly x: S = AppStorageV2.connect(S, KEY, () => new S())!`、PersistenceV2.globalConnect({ type: S, … }) 或 `static … = new S()`，而 @ObservedV2 class S 声明在同一文件的服务类下方；编译报 Class 'S' used before its declaration
适用范围：ArkTS 数据层、状态实现里，把原来只在类型注解或方法体内引用的后置类改成在类定义期即时求值时
做法：
- 被 static 初始化器或模块级常量即时求值的类（connect 的第一个参数、globalConnect 的 type、new 的类），挪到同一文件的使用者之上，或拆到独立 model 文件再 import；只在类型注解或方法体内引用的才可以放在后面，不沿用「辅助类追加到文件末尾」的旧布局
- 或者把共享状态改成静态 getter：static get state(): S { return AppStorageV2.connect(S, KEY, () => new S())! }，每次调用时 connect，同一 key 返回同一实例，不在类定义期求值
- 工程里没有可用的编译脚本时，交付前用 rg -n "static .*= .*(connect|new )" 找出即时求值处，按行号核对被引用的类声明在前，回执注明尚未编译
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- let a = new A(); 在 class A {} 之前 → 报错 Class 'A' used before its declaration；访问 A.a 静态属性同样报错：类在声明前被求值即报错（出处：faqs-arkts-module.md，class声明前实例化、class声明前访问其静态属性）
- 函数体里的 A.a、new A() 在类声明之后才调用就正常，在声明之前调用报 A is not initialized：方法体内的引用可以放在类声明前面，只要调用发生在声明执行之后（出处：faqs-arkts-module.md，在函数中访问未提前声明的类的静态属性）
- static connect<T extends object>(type: TypeConstructorWithArgs<T>, keyOrDefaultCreator?: string | StorageDefaultCreator<T>, defaultCreator?: StorageDefaultCreator<T>): T | undefined：key 已有值就返回它，否则用 defaultCreator 生成后返回；第一个参数是类本身，会被即时求值（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，AppStorageV2.connect）
- static globalConnect<T extends object>(type: ConnectOptions<T>): T | undefined；ConnectOptions.type: TypeConstructorWithArgs<T>：同族接口：PersistenceV2（继承 AppStorageV2）的全局连接，type 里同样传类本身（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.StateManagement.d.ts，PersistenceV2.globalConnect、ConnectOptions.type）
- 改成每次调用 connect 的静态 getter，并把三个状态类移到服务类之前：修好后能编译的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-6bf0193f50046a0568e3（青商城）：做法第 1 步 ← 建议 1、建议 2、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 4；取值 5 ← 诊断
