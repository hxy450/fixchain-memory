# 源端退出分支调 finish() 时，目标在 Toast 结束后 terminateSelf，不写成 pop

审的是：代码
触发（任一种）：
- 读到：退出分支里 showToast 后调宿主 Activity 的 finish()（外部入口进来时结束页面，而不是回列表）；写错的样子：写成 navPathStack.pop()，注释「无独立任务栈时退化为 pop」
适用范围：源端某个分支 finish() 整个 Activity、另一个分支才 popBackStack 的页面
做法：
- finish 分支写成：显示 Toast，等 Toast 时长过后 (this.getUIContext().getHostContext() as common.UIAbilityContext).terminateSelf()，等待期间屏蔽输入
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- terminateSelf(): Promise<void>：销毁当前 Ability，对应源端结束 Activity（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.terminateSelf）
- getHostContext(): Context | undefined：页面里取所在 Ability 的上下文（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getHostContext）
- Toast 时长后 terminateSelf 并屏蔽输入后，与源端行为一致：修好后的写法（出处：卡里修好并验证过）
未核实：Toast 的等待时长卡里没给出具体值
来源：1 张卡，1 个应用
- case-aebac48fa7acdb86e57e（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；取值 3 ← 诊断
