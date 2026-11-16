# 入口 errorManager.on('error') 按规格定：照源复刻崩溃时不注册，否则补注册

审的是：代码
触发（任一种）：
- 读到：入口 UIAbility 由模板改写（onCreate 只有 hilog.info），安卓源没有 UncaughtExceptionHandler 一类的全局异常处理；写错的样子：EntryAbility 或 AbilityStage 的 onCreate 没有 errorManager.on('error', …)，onDestroy 没有 off
- 读到：规格或台账把源端未捕获异常路径写成「照源复刻，可观察行为=应用崩溃」，源端没有 setDefaultUncaughtExceptionHandler；写错的样子：EntryAbility.onCreate 里有 errorManager.on('error', observer)，onDestroy 里 off
适用范围：入口 EntryAbility / AbilityStage 决定要不要注册全局未捕获异常观察器时
做法：
- 规格没保留源端崩溃时：onCreate 里 id = errorManager.on('error', { onUnhandledException, onException })，回调里至少用 hilog 记录；onDestroy 里 errorManager.off('error', id)
- 规格保留了源端崩溃退出（照源复刻的缺陷 AC、台账条目）时不注册：删掉 errorManager 导入、observerId 字段和成对的 on / off；确需加就登记成待批差异
- 自查：entry 的 ets 目录下搜 errorManager.on(，注册了的要在 onCreate 内，同文件 onDestroy 有对应的 errorManager.off
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function on(type: 'error', observer: ErrorObserver): number：注册错误观察器，返回观察器编号（off 时要用）（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.on）
- function off(type: 'error', observerId: number): Promise<void>；另有 off(type: 'error', observerId: number, callback: AsyncCallback<void>): void：按 on 返回的编号注销观察器，有 Promise 和回调两种重载（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.off）
- onUnhandledException(errMsg: string): void；onException?(errObject: Error): void：ErrorObserver 的两个回调：前者必写，收到异常信息和调用栈；后者可选，收到 Error 对象（出处：鸿蒙 SDK 的 ets/api/application/ErrorObserver.d.ts，ErrorObserver）
- import { errorManager } from '@kit.AbilityKit'：errorManager 由 AbilityKit 导出（出处：鸿蒙 SDK 的 ets/kits/@kit.AbilityKit.d.ts，errorManager）
- 观测器捕获到该异常时应用不退出：注册 on('error') 后 js crash 不再结束进程（出处：js-apis-app-ability-errorManager.md，errorManager.on('error')）
- 注册时两条崩溃路径进程不退出、画面停住；删掉注册后 hilog 出现「is about to exit due to RuntimeError」，进程消失：上机看到的两种结果（出处：卡里修好并验证过）
- function on(type: 'globalErrorOccurred', observer: GlobalObserver): void：同族接口：监听进程内任意线程的异常，文档同样写「观测器捕获到该异常时应用不退出」（@since 18）（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.on；js-apis-app-ability-errorManager.md，errorManager.on('globalErrorOccurred')）
未核实：两张卡说法冲突：case-0c59c27ee4ceac59cb60 要求入口不论源端有没有全局异常处理都注册 errorManager.on('error')（这项要求由验证阶段的崩溃风险硬规则提出）；case-caee5090ea39aacf78ee 实测注册后未捕获异常不再结束进程，规格把崩溃定为照源复刻时不注册；case-0c59c27ee4ceac59cb60 修复时观察器在 hilog.fatal 记录后调 new process.ProcessManager().exit(1)，建议里没写这一步；这样能否同时保住崩溃退出，卡里没有核对；进程不退出这一行为出自设备实测和文档，本地 d.ts 只有签名、不写这项行为
来源：2 张卡，2 个应用
- case-0c59c27ee4ceac59cb60（听音练习）：做法第 1 步 ← 建议 1、诊断；做法第 3 步 ← 建议 2
- case-caee5090ea39aacf78ee（Bubble Shooter）：做法第 2 步 ← 诊断、建议 1；取值 6 ← 诊断
