# 需先 init 的存储封装未初始化就读写时打错误日志，不静默返回默认值

审的是：代码
触发（任一种）：
- 写错的样子：封装里 context 或 preferences 实例为空时 getString 直接返回默认值、putString 直接 return，没有任何日志
适用范围：目标端封装的键值存储必须先 init(context) 才能读写时
做法：
- 未 init 时的每个读写分支先打错误日志（写明键名和「未初始化」），再返回；类注释写明必须先在应用最早的生命周期调 init(context)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function error(domain: number, tag: string, format: string, ...args: any[]): void：hilog 的错误级日志（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.error）
来源：1 张卡，1 个应用
- case-f93cb4842b050b7fb269（polypal-app-ohos）：做法第 1 步 ← 建议 3
