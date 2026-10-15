# arkts/strict-mode

ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等）、SDK 类型与项目方法接口的实现写法，及类声明顺序（静态初始化器引用后声明的类）；在不编译的生成批次或尚未被导入、不进构建的新文件里容易留到编译门

[上一级](../index.md)

## 本级经验

- [ArkTS 里给对象字面量落到具名 class/interface 类型；去掉 Record 时键已知用具名字段类、键不定用 Map，不改成索引签名](lesson-1696967d1320c7735732.lesson.md)
  - 时机：编码或返修阶段，为命名常量、主题令牌、键值集合、请求参数、路由参数或事件总线载荷确定类型声明，或按规范替换 Record/Object 时
  - 情境：代码用对象字面量承载令牌、偏好或设置；把查询参数、请求体或路由参数写成内联对象字面量，传给声明为 Record&lt;string, string&gt; 或 Object 的形参；在未标返回类型的 map 等回调里 return 对象字面量；用 Array&lt;{...}&gt; 声明 @State 集合元素；调用泛型事件总线 emit&lt;T extends Object&gt;(name, payload) 时准备直接传 {}；为 toJson 或属性字典构造 Record&lt;string, Object&gt; 时写标识符键字面量，或把内联 { x, y } 当作 Object 值。
  - 例外：类型是只含方法签名的项目接口，或由 SDK 声明的观察者/回调类型时，按接口实现写法的经验（lesson-931ef95a3d0cf202fe5b）处理
- [catch 中继续抛出时先把异常收窄为 Error，非 Error 值包装时保留 message 与 code，不直接 throw catch 变量](lesson-dbfae443e671c568e14e.lesson.md)
  - 时机：功能实现或修复阶段，在 try/catch 中决定把捕获到的异常继续向上抛出时
  - 情境：ArkTS 严格模式工程中，catch 分支需要把当前任务的异常继续上报（例如过期任务的异常按取消处理、当前任务的异常上报），catch 变量没有 Error 类型保证；写码批次按约束不自行编译，或修改落在组编译之后。
  - 例外：抛出的值已经在同一分支里由 instanceof Error 等判断收窄为 Error
- [新建且尚未被页面或 Ability 导入的 .ets 文件不进入全量编译：落盘后接一处导入或单独做 ArkTS 检查，再报告构建通过](lesson-db3ea8446bdad793cd52.lesson.md)
  - 时机：编码阶段新建令牌、常量、工具或模型文件，或并发 worker 被要求不跑全量构建，准备以构建通过为依据报告完成时
  - 情境：新写的 .ets 文件还没有被任何页面、组件或 Ability 导入（如先建主题令牌类、之后再接线）；全量构建按入口的导入关系编译，构建日志显示通过。
- [给接口或类类型的参数传实现对象时按声明来源选写法：SDK 声明的类型用带类型标注的对象字面量，项目自定义的方法接口用 implements 具名类](lesson-931ef95a3d0cf202fe5b.lesson.md)
  - 时机：实现、修复或收口接线阶段，为 errorManager.on('error') 一类系统 API 准备观察者对象，或把依赖对象交给只含方法签名的端口接口、把已有类实例传给新声明的接口参数时
  - 情境：要传入的类型或由 SDK d.ts 声明（如 application/ErrorObserver.d.ts 的 export default class ErrorObserver），或是项目自定义、只声明方法的依赖接口；写者按 TS 习惯准备 implements 一个 class，或用箭头函数属性的对象字面量实现项目接口，或把结构上恰好具备这些方法、却未声明 implements 的已有类实例直接传入；生成或修复 worker 可能被要求不自行编译。
  - 例外：只含数据属性的接口或 class，按对象字面量落到具名类型的经验（lesson-1696967d1320c7735732）处理
- [静态字段初始化器或模块级常量里把类当值使用时，该类要声明在使用者之前或从独立文件导入](lesson-f80ae7c3747420ef16f7.lesson.md)
  - 时机：数据层或状态实现阶段，在服务类中用静态字段持有共享状态（AppStorageV2.connect、new Cls()）并安排同文件模型类的位置时
  - 情境：服务类准备用 static 字段初始化器调用 AppStorageV2.connect(Cls, key, () =&gt; new Cls())、PersistenceV2.globalConnect 或 new Cls()，被引用的 @ObservedV2 类按原有布局追加在文件末尾；原先对它只有类型注解或方法体内的引用。
