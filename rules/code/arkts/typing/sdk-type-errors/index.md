# 构建报错里的 SDK 类型约束

agent 会看到什么：构建输出报 SDK 类型相关的错（arkts-implements-only-iface、Property 'byteLength' does not exist on type 'Buffer'）；产物里 implements SDK 声明的 class、Buffer 转 Uint8Array 的视图写法

## 规矩

- rule-9e6dc5f84f60｜SDK 把观察者类型声明为 class 时，不写 implements，用标注该类型的对象字面量｜读到：要传给 SDK 的观察者或回调参数，类型在声明里是 export default class（如 ErrorObserver，供 errorManager.on('error', observer) 用）；写错：目标写 class X implements errorManager.ErrorObserver { … }，编译报 Classes cannot be specified in "implements" clause (arkts-implements-only-iface)
- rule-3344fdaf30ef｜ArkTS Buffer 转独立 Uint8Array 时按 length 分配后 copy，不用 .buffer 视图｜读到：构建输出报 Property 'byteLength' does not exist on type 'Buffer'；写错：代码里写 new Uint8Array(buf.buffer, buf.byteOffset, buf.length) 或 new Uint8Array(buffer.from(...).buffer)，或把 byteLength 机械替换成 length 后仍保留这种视图；真机抛 RangeError: The newByteLength is out of range
