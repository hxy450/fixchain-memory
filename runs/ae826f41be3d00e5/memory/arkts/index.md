# arkts

ArkTS 语言与 SDK 接口：类型、签名、严格模式限制与异步错误路径

[上一级](../index.md)

## 子主题

- [api-signatures](api-signatures/index.md) — 调用 ArkUI 组件属性方法或 SDK 接口时的参数类型、重载匹配与必填参数：@BuilderParam 传入 builder 的写法与 this 绑定，intl 格式化等接口不能省略的参数
- [async](async/index.md) — 源端同步调用改成 ArkTS 异步（Promise/async）后新增的失败分支、加载态，以及异步初始化与用户输入的先后顺序
- [strict-mode](strict-mode/index.md) — ArkTS 严格模式对写法的限制（throw、对象字面量类型、索引签名、类型收窄等），在不编译的生成批次或未接线文件里容易留到编译门
