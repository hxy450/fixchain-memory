# 源码混用 Toast 的 SHORT 和 LONG 时，Toast 封装带 duration 参数、逐处照源映射

审的是：代码
触发（任一种）：
- 读到：源码 Toast.makeText(…, Toast.LENGTH_SHORT) 和 Toast.LENGTH_LONG 在同一文件或同一公共方法里混用；写错的样子：目标 showToast({ message, duration }) 全部用同一个时长（如只定义一个 LONG 常量 3500），或公共 Toast 封装只有 message 参数、duration 写死
适用范围：把源端 Toast.makeText 调用翻译成目标公共 Toast 封装或 showToast 调用时
做法：
- 公共 Toast 封装把时长做成每次调用的参数（如 showToast(message, duration)），SHORT 传 2000、LONG 传 3500，不按多数调用写死一个值
- 在源文件里 grep Toast.LENGTH_SHORT 与 LENGTH_LONG，逐个调用点原样映射；源文件两种都有、目标只定义了一个时长常量时，回到每个 SHORT 调用点补齐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Toast.LENGTH_SHORT = 0；Toast.LENGTH_LONG = 1：源端这两个是时长档位，不是毫秒，不能直接当 duration 传（出处：android.widget.Toast#LENGTH_SHORT、LENGTH_LONG）
- SHORT → 2000ms，LONG → 3500ms：修好后的映射（出处：卡里修好并验证过）
- duration?: number，默认 1500；小于 1500 自动改成 1500，最大 10000（ms）：ShowToastOptions 的时长（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，ShowToastOptions.duration）
- showToast(options: promptAction.ShowToastOptions): void：UIContext 上的 PromptAction 弹 Toast（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.showToast）
未核实：卡里修好时的目标 SDK 是 6.1.1(24)，本机核实声明用的是 API 23
来源：1 张卡，1 个应用
- case-65c33c4172d6d208c5a5（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、建议 2；取值 2 ← 诊断、建议 1
