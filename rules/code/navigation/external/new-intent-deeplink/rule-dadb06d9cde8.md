# onNewWant 写入的 want 快照要带 revision 并由已存在的页面观察，不只在构造时读一次

审的是：代码
触发（任一种）：
- 读到：源 Activity 为 standard 启动；目标 UIAbility 为 singleton，`onNewWant` 把新 want 写进共享快照；写错的样子：快照只在 `onCreate` / `onNewWant` 写入，VM 只在构造函数里拷贝一次（注释却说新 want 覆盖旧值），页面不观察，也没有 revision
适用范围：集成阶段实现第三方拉起 want 的解析与消费、目标为 singleton UIAbility 时
做法：
- 逐个写入点核对消费点：快照带 `revision`（每次写入 +1），页面用 `@Monitor('<快照>.revision')` 或回调观察，触发重新应用启动参数
- 应用新请求前串行等旧的相机、录像、保存结束，再重跑模式与朝向判定；切换期间禁用交互
- 回传结果时按 revision 校验，旧请求的结果失效、不重放
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- declare type MonitorDecorator = (value: string, ...args: string[]) => MethodDecorator：@Monitor 接收要监听的属性路径，可以一次传多个（出处：鸿蒙 SDK 的 ets/component/common.d.ts，Monitor、MonitorDecorator）
- onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void：已运行实例收到新 want 的入口，写入快照的地方（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onNewWant）
- 快照加 revision，页面 @Monitor 触发重新应用，串行等旧操作结束，结果按 revision 防重放：修好后的写法（出处：卡里修好并验证过）
未核实：卡里记的鸿蒙 SDK 是 6.1.1(24)，本机核实用 API 23
来源：1 张卡，1 个应用
- case-7621afac5fee30a13731（opencamera-hmos）：做法第 1 步 ← 建议 4、建议 3、诊断；做法第 2 步 ← 建议 3、诊断；做法第 3 步 ← 建议 3、诊断；取值 3 ← 诊断
