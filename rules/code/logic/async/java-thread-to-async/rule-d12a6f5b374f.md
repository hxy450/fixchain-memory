# 源端阻塞等待接到「X 先于 Y」的验收时，等待链一路 Promise<void> 并逐层 await

审的是：代码
触发（任一种）：
- 读到：源端 void 方法内部阻塞等待队列、线程完成（Object.wait()、BlockingQueue），规格验收写「排空先于销毁」「先等待再重启」；目标端的等待方法是 async、返回 Promise<void>；写错的样子：调用方用 `void` 前缀丢弃等待方法返回的 Promise，或等待方法、销毁序列仍是 `(): void`，调用后立即销毁、重启
- 读到：跨切片 seam 承接源端用 Object.wait() / BlockingQueue 实现的阻塞等待，验收要求排序；写错的样子：seam 回调类型定成 `(() => void) | null`，调用方同步调用后立即执行后续动作
适用范围：把源端阻塞式等待转成 ArkTS 异步实现，并有「X 先于 Y」排序要求的等待链、seam 和生命周期回调
做法：
- 等待方法、销毁序列和 seam 类型都改成 async / `() => Promise<void>`，即使当前只是桩也这样定；调用方 await 之后再销毁、重启
- 不能 await 的生命周期回调（aboutToDisappear）只用 void 前缀发起 VM 上的一个 async 销毁序列，引擎销毁放在这个序列的 await 之后，页面里不另行同步销毁
- 用单测核对：队列有在途任务时，销毁序列和重启都不先执行销毁或重启
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aboutToDisappear?(): void：生命周期回调返回 void，框架不会等里面的 Promise，所以只能发起序列，顺序要在序列内部保证（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToDisappear）
- 等待方法和销毁序列改为 async 并 await，seam 改成 () => Promise<void>，重启改为 await 后执行；页面只发起销毁序列，引擎销毁在序列 await 之后：修好后的写法（出处：卡里修好并验证过）
未核实：卡里观察到的行为出自鸿蒙 SDK 6.1.1(24)，本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-742303a1abdd7ba274ec（opencamera-hmos）：做法第 1 步 ← 建议 1、建议 2、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 2 ← 诊断
