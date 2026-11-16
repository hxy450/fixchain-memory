# SDK 把观察者类型声明为 class 时，不写 implements，用标注该类型的对象字面量

审的是：代码
触发（任一种）：
- 读到：要传给 SDK 的观察者或回调参数，类型在声明里是 export default class（如 ErrorObserver，供 errorManager.on('error', observer) 用）；写错的样子：目标写 class X implements errorManager.ErrorObserver { … }，编译报 Classes cannot be specified in "implements" clause (arkts-implements-only-iface)
适用范围：ArkTS 代码向系统 API 传入观察者、回调对象，而参数类型在 SDK 声明里是 class 时
做法：
- 先查声明里这个类型是 class 还是 interface；是 class 就写 const observer: errorManager.ErrorObserver = { onUnhandledException: (errMsg: string): void => { … }, onException: (errObject: Error): void => { … } }，再 errorManager.on('error', observer)
- 保存 on 返回的 number，onDestroy 里用它 errorManager.off('error', id) 反注册；字段类型也写成 errorManager.ErrorObserver
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function on(type: 'error', observer: ErrorObserver): number：注册错误观察者，返回观察者编号（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.on）
- function off(type: 'error', observerId: number): Promise<void>：按编号反注册（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.off）
- export default class ErrorObserver { onUnhandledException(errMsg: string): void; onException?(errObject: Error): void }：ErrorObserver 声明为 class，不能被 implements（出处：鸿蒙 SDK 的 ets/api/application/ErrorObserver.d.ts，ErrorObserver）
- ArkTS 中只有接口可以被 implements，类不允许被 implements（arkts-implements-only-iface，错误码 10605051）：TS 里 class 当接口 implements 的写法在 ArkTS 不成立（出处：typescript-to-arkts-migration-guide.md，类不允许implements）
- export default class ApplicationStateObserver：同族接口：同样声明为 class 的观察者类型（出处：鸿蒙 SDK 的 ets/api/application/ApplicationStateObserver.d.ts，ApplicationStateObserver）
- export default class AbilityStartCallback：同族接口：同样声明为 class 的回调类型（出处：鸿蒙 SDK 的 ets/api/application/AbilityStartCallback.d.ts，AbilityStartCallback）
- 改成标注 errorManager.ErrorObserver 的对象字面量后构建通过：返修的写法（出处：卡里修好并验证过）
未核实：卡里的编译结果出自 HarmonyOS 6.1.1(24) / 6.0.1(21)，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-28990049b25bf1086836（DeepAI全能PPT）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 7 ← 诊断
