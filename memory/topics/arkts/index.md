# arkts

ArkTS 语言与 ArkUI 声明层的编译约束：接口签名核对、严格类型限制、组件 DSL 规则与运行时语义差异

[上一级](../../index.md)

## 子主题

- [api-signatures](api-signatures/index.md) — 调用 SDK/ArkUI 接口或引用跨文件声明时，参数类型、重载、成员名与语义注释须按声明核对而非凭记忆推定（6 条）
- [runtime-semantics](runtime-semantics/index.md) — 源端同步调用或数值运算改成 ArkTS 后的运行时差异：异步失败分支、初始化顺序、错误通道与 number 边界（4 条）
- [strict-mode](strict-mode/index.md) — ArkTS 严格类型系统对对象字面量、接口实现、异常收窄与类声明顺序的限制，不编译时也会留到编译门（5 条）
- [ui-syntax](ui-syntax/index.md) — 自定义组件成员声明与 build()/@Builder 的 DSL 规则：装饰器写法、插槽传参、渲染语句与容器专属属性（5 条）
