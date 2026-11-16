# 窗口层重算顶部避让值时，除 windowSizeChange 外再挂 avoidAreaChange

审的是：代码
触发（任一种）：
- 写错的样子：EntryAbility 只挂 windowClass.on('windowSizeChange', …) 重算避让值（如 windowTopPadding），没有 on('avoidAreaChange', …)
适用范围：窗口层维护状态栏避让值、页面要随横竖屏切换更新避让时
做法：
- 再挂 windowClass.on('avoidAreaChange', (data) => { … })，在回调里用 data.type / data.area 重新计算避让值并写回窗口状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- on(type: 'avoidAreaChange', callback: Callback<AvoidAreaOptions>): void：当前窗口系统避让区变化的监听（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('avoidAreaChange')）
- AvoidAreaOptions { type: AvoidAreaType; area: AvoidArea }：回调带避让区类型和区域（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，AvoidAreaOptions）
- on(type: 'windowSizeChange', callback: Callback<Size>): void：只报窗口尺寸，不报避让区（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('windowSizeChange')）
- 横屏时系统隐藏状态栏，避让区变化晚于尺寸变化到达；补 avoidAreaChange 重测后避让值正确：只靠尺寸监听会拿到旧的避让值（出处：卡里修好并验证过）
未核实：卡里的行为出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-0a77d32c850d4767a2d4（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；取值 4 ← 诊断
