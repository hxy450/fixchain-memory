# 规格照源保留崩溃退出时，不把入口补 errorManager.on('error') 写成既定项

审的是：规格
触发（任一种）：
- 读到：安卓源有会抛未捕获异常的路径（整数除零、数组负下标），且没有全局未捕获异常处理（没有 Thread.setDefaultUncaughtExceptionHandler）；写错的样子：规格里一边有「throw…使应用崩溃（照源复刻）」的验收项或台账条目，一边写「全局异常观察｜源无对应代码｜EntryAbility.onCreate 补 errorManager.on('error')（工程健壮性既定项）」
适用范围：规格提取阶段，给入口 UIAbility 补源端没有的全局异常观察器或全局错误兜底时
做法：
- 先查规格和决策台账里有没有照源复刻的崩溃项（缺陷验收项、「可观察行为=应用崩溃」的条目）；有就不加全局异常观察器
- 确需加时写成与这些崩溃复刻冲突的待批差异，写明这些路径在目标端的结果（进程不退出、画面停住），不写「工程健壮性既定项」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 注册后可以捕获到应用产生的js crash……观测器捕获到该异常时应用不退出：注册观察器改变了失败行为：未捕获异常不再结束进程，不只是多记一条日志（出处：js-apis-app-ability-errorManager.md，errorManager.on('error')）
- 注册观察器时两条崩溃路径抛异常后进程不退出、画面停住；去掉注册后出现 hilog「is about to exit due to RuntimeError」，进程消失，和安卓一致：上机看到的两种结果（出处：卡里修好并验证过）
- function on(type: 'error', observer: ErrorObserver): number：errorManager 的错误观察器注册，返回给 off 用的 observerId（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.on）
来源：1 张卡，1 个应用
- case-caee5090ea39aacf78ee（Bubble Shooter）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
