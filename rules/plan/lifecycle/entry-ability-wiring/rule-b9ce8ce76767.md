# 入口装配的派工要列上注册全局未捕获异常观察器一项，不因安卓源没有而省略

审的是：计划与派工
触发（任一种）：
- 读到：安卓源里没有 UncaughtExceptionHandler 一类的全局异常处理代码；入口装配契约只要求改 loadContent、main_pages.json、Navigation 外壳与 pageMap、剔除模板；写错的样子：入口装配的派工或任务拆分里，EntryAbility 的改写项只有 loadContent 改向入口页、main_pages.json 只留入口页、Navigation 外壳与 pageMap、剔除 Hello World 模板这几项，没有「onCreate 注册 errorManager.on('error') 观察器、onDestroy 注销」
适用范围：HarmonyOS Stage 模型应用入口装配阶段的派工说明和任务拆分
做法：
- 在入口装配的改写项里加一项：「EntryAbility.onCreate 用 errorManager.on('error', observer) 注册全局未捕获异常观察器，回调里至少 hilog 记录；保存 observerId，onDestroy 里 errorManager.off('error', observerId)」
- 在这一项旁注明：这是没有安卓对应物的鸿蒙平台约束，不能以源码没有为由省略
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function on(type: 'error', observer: ErrorObserver): number：派工里要写的那个注册接口，返回 off 时要用的编号（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.errorManager.d.ts，errorManager.on）
来源：1 张卡，1 个应用
- case-0c59c27ee4ceac59cb60（听音练习）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 1
