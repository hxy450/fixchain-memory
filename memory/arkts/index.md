# arkts

ArkTS 语言与 SDK 接口：类型、签名、V2 组件成员声明、严格模式限制、数值语义与异步错误路径，以及不能编译时的写后自检

[上一级](../index.md)

## 子主题

- [api-signatures](api-signatures/index.md) — 调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数，成员名、所属类型与返回可空性的声明核对：@BuilderParam 传入 builder 的写法与 this 绑定，intl 格式化等接口不能省略的参数
- [async](async/index.md) — 源端同步调用改成 ArkTS 异步（Promise/async）后新增的失败分支、加载态，异步初始化与用户输入的先后顺序，以及仓库方法前置失败分支（未初始化、未授权）的错误通道
- [decorators](decorators/index.md) — ArkUI V2 自定义组件的成员声明：装饰器是否带括号、@BuilderParam 默认值的写法、状态成员名与组件通用属性方法的冲突
- [numeric](numeric/index.md) — 数值语义：ArkTS number 与 Kotlin 在除法、零分母与范围钳制上的差异，迁移比值和进度计算时要保留的保护
- [strict-mode](strict-mode/index.md) — ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等），在不编译的生成批次或未接线文件里容易留到编译门

## 本级经验

- [不能编译的整页生成，写后把引用的常量与 this 成员逐一对照声明；源端局部派生值改为经持有对象访问](lesson-e04e26f1f98116275982.lesson.md)
  - 时机：页面实现阶段，在禁止编译的条件下一次写出大型 ArkTS 页面并做写后自检时
  - 情境：整页由一次写入生成，常量区与状态区由写者自拟；源码在方法里用局部派生值（如 isX = current instanceof Y）控制菜单显隐，目标把该对象建模为可空状态；设计里决定的尺寸以具名常量在调用点引用。
