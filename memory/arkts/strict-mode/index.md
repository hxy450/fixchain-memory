# arkts/strict-mode

ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等）及类声明顺序（静态初始化器引用后声明的类），在不编译的生成批次或未接线文件里容易留到编译门

[上一级](../index.md)

## 本级经验

- [ArkTS 里给对象字面量写显式 class/interface 类型；去掉 Record 时键已知用具名字段类、键不定用 Map，不改成索引签名](lesson-1696967d1320c7735732.lesson.md)
  - 时机：编码或返修阶段，为一组命名常量、主题令牌、键值集合或事件总线载荷确定类型声明，或按规范替换 Record/Object 时
  - 情境：代码用对象字面量承载间距、圆角等令牌，或用键值集合保存偏好、设置；目标文件可能还没被页面或 Ability 导入，或者并发 worker 被要求不跑全量构建，编译器暂时检查不到这些写法。或调用泛型事件总线 emit&lt;T extends Object&gt;(name, payload)，载荷只作信号、准备直接传 {}。 也包括把查询参数、请求体或路由参数写成内联对象字面量，直接传给声明为 Record&lt;string, string&gt; 或 Object 形参的请求封装与路由方法；在未标返回类型的 map 等回调里 return 对象字面量；用 Array&lt;{...}&gt; 声明 @State 集合元素；按编译报错改写类时写出 TS 风格的 constructor(public x)。 也包括为 toJson 或渲染属性构造 Record&lt;string, Object&gt; 字典时写 { color: value, opacity: 1 }、return { courseCount: … } 这类标识符键字面量，或把内联 { x, y } 当作 Object 值。
- [SDK 把观察者或回调类型声明为 class 时不写 implements：用以该类型标注的对象字面量传入](lesson-6e74f064efe2649fc295.lesson.md)
  - 时机：实现或修复阶段，为 errorManager.on('error') 一类需要观察者对象的系统 API 确定观察者的声明形态时
  - 情境：要传给 SDK 的观察者或回调参数在 d.ts 中声明为 class（如 application/ErrorObserver.d.ts 的 export default class ErrorObserver），写者按 TS 习惯准备用 class 实现它；生成或修复 worker 可能被要求不自行编译。
- [catch 中继续抛出时先把异常收窄为 Error，不直接 throw catch 变量](lesson-dbfae443e671c568e14e.lesson.md)
  - 时机：功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时
  - 情境：ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。
  - 例外：抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error
- [只含方法签名的自定义接口用 implements 它的具名类实现：不传箭头函数对象字面量；已有类实例交给新声明的接口参数时写适配类，ArkTS 不做结构化匹配](lesson-931ef95a3d0cf202fe5b.lesson.md)
  - 时机：实现或收口接线阶段，把依赖对象交给只含方法签名的端口或依赖接口，或把已有类实例传给新声明的接口参数时
  - 情境：项目自定义的依赖接口只声明方法；写者准备用箭头函数属性的对象字面量直接传参或先赋给该接口类型的变量，或把结构上恰好具备这些方法、却未声明 implements 的已有类实例直接传入。
  - 例外：接口类型由 SDK 声明为 class 时，按 SDK 观察者类型的写法传入以该类型标注的对象字面量
- [静态字段初始化器或模块级常量里把类当值使用时，该类要声明在使用者之前或从独立文件导入](lesson-f80ae7c3747420ef16f7.lesson.md)
  - 时机：数据层或状态实现阶段，在服务类中用静态字段持有共享状态（AppStorageV2.connect、new Cls()）并安排同文件模型类的位置时
  - 情境：服务类准备用 static 字段初始化器调用 AppStorageV2.connect(Cls, key, () =&gt; new Cls())、PersistenceV2.globalConnect 或 new Cls()，被引用的 @ObservedV2 类按原有布局追加在文件末尾；原先对它只有类型注解或方法体内的引用。
