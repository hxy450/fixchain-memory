# 类型约束

交回的代码里有 Record、索引签名、无类型的对象字面量、implements 和构造写法、process.getEnvironmentVar 这类可选值，或构建报 arkts-no-* 类型错误时

## 触发族

- [Record 类型和索引签名](record-index-signature/index.md)（3 条）：读到或写出 Record<K, V>、[key: string] 索引签名、标识符键的 Record 字面量，构建日志报 arkts-no-indexed-signatures / arkts-no-props-by-index / arkts-no-untyped-obj-literals
- [没有声明类型的对象字面量](untyped-object-literal/index.md)（3 条）：产物里对象字面量直接作实参、返回值、路由参数或类型（return { … }、{ id: item.id }、Array<{ … }>），构建日志报 arkts-no-untyped-obj-literals / arkts-no-obj-literals-as-types
- [接口的实现和类的构造写法](interface-impl-class-ctor/index.md)（3 条）：产物里把没 implements 的类实例或箭头函数对象字面量传给 interface 形参、新类写 constructor(public x)，构建日志报 arkts-no-structural-typing / arkts-no-ctor-prop-decls
- [构建报错里的 SDK 类型约束](sdk-type-errors/index.md)（2 条）：构建输出报 SDK 类型相关的错（arkts-implements-only-iface、Property 'byteLength' does not exist on type 'Buffer'）；产物里 implements SDK 声明的 class、Buffer 转 Uint8Array 的视图写法
- [process.getEnvironmentVar 读出的可选配置](environment-var-read/index.md)（1 条）：读到改写前的代码是 process.getEnvironmentVar('X') || '' 这类带缺省的回退链；产物里 const v = process.getEnvironmentVar('X') 之后直接读 v.length 或 Number(v)，没有 || '' / ?? '' 或判 undefined
