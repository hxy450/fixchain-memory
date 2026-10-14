# arkts

ArkTS 语言与 SDK 接口：类型、签名、V2 组件成员声明、严格模式限制与声明顺序、声明式 UI 语法与容器属性、数值语义与异步错误路径，以及不能编译时的写后自检；Java 标准库与语言语义（文本切分、格式化、日历、集合迭代序、有符号 byte）的等价实现

[上一级](../index.md)

## 子主题

- [api-signatures](api-signatures/index.md) — 调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数，成员名、所属类型与返回可空性的声明核对，依赖单位、默认行为与作用范围时读到字段注释而不以签名推定等价：@BuilderParam 槽内容的写法（箭头闭包只调用 @Builder、this 绑定），intl 格式化等接口不能省略的参数，源端单调计时的目标 API
- [async](async/index.md) — 源端同步调用改成 ArkTS 异步（Promise/async）后新增的失败分支、加载态，异步初始化与用户输入的先后顺序，依赖先后生效的连续平台调用在网关内串行，单线程执行器改成 Promise 串行队列后的重入，仓库方法前置失败分支（未初始化、未授权）的错误通道，以及 Kit API catch 值（BusinessError）的取消息与按错误码分类，以及源 API 以返回值表示被拒、以异常表示故障而目标都 reject 时的单次适配
- [decorators](decorators/index.md) — ArkUI V2 自定义组件的成员声明：装饰器是否带括号、@BuilderParam 默认值的写法、状态成员名与组件通用属性方法的冲突
- [numeric](numeric/index.md) — 数值语义：ArkTS number 与 Kotlin/Java 在除法、零分母与范围钳制上的差异，迁移比值和进度计算时要保留的保护，以及 Java long 常量超出安全整数范围时的拼接；Float 运算与相等比较的 float32 对齐
- [stdlib](stdlib/index.md) — Java 标准库与语言语义到 ArkTS 的等价实现：读行、split/trim、BOM、String.format 与 Locale、Calendar 周规则，HashSet/HashMap 迭代序、有符号 byte 比较与 switch 返回码；DecimalFormat、BigDecimal 舍入与 Float.toString 的数值转文本，位置参数的字面插入（避开 String.replace 替换模式）
- [strict-mode](strict-mode/index.md) — ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等）及类声明顺序（静态初始化器引用后声明的类），在不编译的生成批次或未接线文件里容易留到编译门
- [ui-syntax](ui-syntax/index.md) — 声明式 UI 语法：build() 与 @Builder 中可写的组件、条件与循环渲染形式（多行、花括号、不加分号），stateStyles 状态值的合法写法，以及 justifyContent 等容器专属属性的适用范围

## 本级经验

- [不能编译的生成或修复批次，写后把引用的常量、this 成员、跨文件导入名与 $r 资源键逐一对照声明、导出和资源定义；源端局部派生值改为经持有对象访问](lesson-e04e26f1f98116275982.lesson.md)
  - 时机：实现或修复阶段，在禁止编译的条件下一次写出大型 ArkTS 页面，或新建工具文件并在其他文件接线，并做写后自检时
  - 情境：整页由一次写入生成，常量区与状态区由写者自拟；源码在方法里用局部派生值（如 isX = current instanceof Y）控制菜单显隐，目标把该对象建模为可空状态；设计里决定的尺寸以具名常量在调用点引用。也包括把 Kotlin object 或 Java 静态工具类改写为 ArkTS 顶层 export function，又在基类等其他文件按源端 ClassName.method 写法导入调用。 也包括页面转换先按源值预估的键清单向共享 element/*.json 追加资源，再写组件里的 $r('app.float|color|string.*') 引用；同一容器各方向的 padding/margin 可能用到清单之外的键。
