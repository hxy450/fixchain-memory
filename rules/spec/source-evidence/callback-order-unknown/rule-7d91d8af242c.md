# 两端异步终态没核实时，笔记和注释不写「同语义」，记进 decision_gaps

审的是：规格
触发（任一种）：
- 读到：源端 await 平台插件调用后才给成功/失败提示，目标 API 的 Promise 和完成事件分开（如 show() 与 on('shareCompleted')）；写错的样子：源码理解笔记（source-notes）或代码注释写「与源同语义」「与源同序」，但取消时 resolve 还是 reject 没有出处；信封的 decision_gaps 为 []，不确定项里也没有这个疑点
适用范围：把源端等待用户结果的平台调用映射到目标 API、两端何时 settle 尚未核实时
做法：
- 先读源插件实现和目标 d.ts/文档，把两端何时 settle、取消时 resolve 还是 reject 写进笔记并注明出处
- 做不到时把这个疑点记入 decision_gaps 或保留为不确定项，不在注释或 source-notes 里写「同语义」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- show(context: common.UIAbilityContext, options: ShareControllerOptions): Promise<void>，完成另由 on('shareCompleted') 通知：目标端终态拆成 Promise 和事件两路，不能默认和源端同语义（出处：鸿蒙 SDK 的 hms/ets/api/@hms.collaboration.systemShare.d.ts，ShareController.show）
来源：1 张卡，1 个应用
- case-096c031832b60ef8b78e（Countdate）：做法第 1 步 ← 建议 3、建议 1；做法第 2 步 ← 建议 3
