# 写成恒 false 的「平台无对等」能力和标志

agent 会看到什么：读到规格或台账写「平台无对等 → 恒 false」、账本里 approved 的等价实现，或源端在多处 if 里消费的标志；产物里写成 readonly … = false 的恒 false、两个分支返回同一值（? X : X）、persist 恒返回 false，注释写「HarmonyOS 无…」「契约位保留」「本管线无入口」

## 通用查法

### 产物里有恒 false 或「无对等」「无入口」收口时，先在 SDK 声明和源码里各查一次再定

审的是：代码
触发（任一种）：
- 读到：规格或台账写「PD-C…：平台无对等 → 恒 false」，或源端在多处 if 里消费一个由别处置位的 boolean 标志；写错的样子：代码里有 `readonly …: boolean = false`、两支相同的 `? X : X`、恒 return false，注释写「HarmonyOS 无…」「契约位保留」「本管线无入口」
适用范围：实现规格或台账里判为平台无对等、批准等价实现的能力，或源端消费的标志在目标端暂找不到置位入口时
做法：
- 能力类：在鸿蒙 SDK 声明里按能力名和源端 API 的关键词搜一次（如 PiPWindow、isPiPEnabled）；有声明就照它实现、只在运行期按结果降级，与规格冲突时上报，不写恒 false
- 标志类：到源工程里找这个标志的全部赋值处和触发它的菜单项、按钮，逐个在目标端实现；找不到才登记规格缺口，不静默收口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function isPiPEnabled(): boolean：例：规格判为平台无对等的画中画，声明里有检测接口（出处：鸿蒙 SDK 的 ets/api/@ohos.PiPWindow.d.ts，PiPWindow.isPiPEnabled）
针对本应用要查的：
- 判为无对等的能力在 SDK 里有没有接口：鸿蒙 SDK 的 ets/api 下 @ohos.*.d.ts 声明，按能力名和源端 API 的关键词搜（画中画、通知授权、后台任务这一类）；搜到 function 或 interface 声明就记下签名，按它实现或上报决策冲突
- 源端标志的置位者：源工程里定义该标志的类（多半是页面继承的基类）里所有给它赋值的地方，以及触发这些赋值的菜单项或按钮；列出每个置位入口和条件，在目标端逐个实现
来源：3 张卡，2 个应用
- case-997587966a65e79790b5（AntennaPod）：做法第 2 步 ← 建议 3
- case-a78ca40d4f9b42be76bb（Cofi）：做法第 1 步 ← 建议 4
- case-f93a2f80bafd58105489（Cofi）：做法第 1 步 ← 建议 2

## 规矩

- rule-1d8ae0048116｜规格判定平台无对等时，实现前在 SDK 声明里 grep 一次，API 存在就上报冲突｜读到：规格或台账写「PD-C…：平台无对等 → 恒 false」；写错：代码写成 `readonly …: boolean = false` 的恒 false 常量或无效设置行，注释写「HarmonyOS 无…」
- rule-200eff1f6bfa｜账本批准等价实现的后台计时、通知授权和画中画回退，服务层要真实现，只在运行期降级｜读到：决策账本里「经平台后台任务 / 通知抽象保留后台计时语义」「精确 PiP 不可用时用应用内紧凑回退」为 approved；源端用前台 Service、带动作的进度通知、POST_NOTIFICATIONS 或 enterPictureInPictureMode；写错：平台服务的 getStatus 两个分支返回同一个值（`? X : X`）、persist 恒返回 false、没有通知和动作；requestNotificationPermission 直接置授权 false；后台开关打开即复位 false；hasPiPPermission 写死 false
- rule-2302786f91d1｜源端消费的标志在目标端“无入口”时去源码找置位者，不写“契约位保留”收口｜写错：目标代码注释写 `恒false`、`契约位保留`、“本管线无入口”，源端在多处 if 里消费的那个标志在目标端从不置位，或写成 UI 观察不到的普通字段
