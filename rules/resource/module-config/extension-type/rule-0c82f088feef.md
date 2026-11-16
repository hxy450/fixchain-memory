# 扩展条目的 type 要与基类对应，AppServiceExtensionAbility 写 appService

审的是：资源
触发（任一种）：
- 读到：目标源文件 extends AppServiceExtensionAbility（或 WorkSchedulerExtensionAbility）；写错的样子：module.json5 的 extensionAbilities 里该条目写 "type": "service"（或别的与基类不对应的 type）
适用范围：在 module.json5 的 extensionAbilities 里登记扩展能力、尤其是因编译错误换过基类之后
做法：
- 按基类写 type：AppServiceExtensionAbility ↔ "appService"，WorkSchedulerExtensionAbility ↔ "workScheduler"
- 交付前 grep 源文件的「extends X」和对应条目的 type 一一核对；构建 schema 通过不代表类与 type 对应
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- type=service 安装报 9568344 和 not allow use privilege extension；按基类改成 type=appService 后安装成功：两种 type 的真机结果（出处：卡里修好并验证过）
- appService（20+）：AppServiceExtensionAbility；workScheduler：延时任务的 ExtensionAbility；service：三方配置无法安装，需特权：type 的取值（出处：module-configuration-file.md，type标签）
- import WorkSchedulerExtensionAbility, { WorkSchedulerExtensionContext } from '@ohos.WorkSchedulerExtensionAbility'：WorkSchedulerExtensionAbility 从 @kit.BackgroundTasksKit 导出（出处：鸿蒙 SDK 的 ets/kits/@kit.BackgroundTasksKit.d.ts）
未核实：卡里环境是 API 22（HarmonyOS 6.0.2），本机声明是 API 23
来源：1 张卡，1 个应用
- case-b92afb07b8ec2465afcf（CleanSweep）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
