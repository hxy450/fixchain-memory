# setResult+finish() 移植成一次 terminateSelfWithResult，带回结果码和 uri

审的是：代码
触发（任一种）：
- 读到：源码响应 MediaStore.ACTION_IMAGE_CAPTURE / ACTION_VIDEO_CAPTURE，结束时 setResult(RESULT_OK 或 RESULT_CANCELED, data) 再 finish()；写错的样子：目标结果函数的成功和失败分支都只调 this.context.terminateSelf()，注释说调用方会读回 want，结果码和 uri 没进 AbilityResult
适用范围：把 Activity 结果协议（被第三方用意图拉起、结束时回传结果）移植到鸿蒙 UIAbility 时
做法：
- 写成一次 context.terminateSelfWithResult({ resultCode: ok ? -1 : 0, want: { uri } })：RESULT_OK 对 -1，RESULT_CANCELED 对 0
- 写完检查结果函数里的成功标志和 uri 是否真的写进了 AbilityResult，不能只调用 terminateSelf()
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- terminateSelfWithResult(parameter: AbilityResult): Promise<void>：销毁自身并把结果码和数据回传给调用方（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.terminateSelfWithResult）
- terminateSelf(): Promise<void>：只销毁自身，不回传任何结果（出处：鸿蒙 SDK 的 ets/api/application/UIAbilityContext.d.ts，UIAbilityContext.terminateSelf）
- AbilityResult { resultCode: number; want?: Want }：resultCode 放结果码，want 放回传数据（如 uri），可为空（出处：鸿蒙 SDK 的 ets/api/ability/abilityResult.d.ts，AbilityResult）
- RESULT_OK = -1，RESULT_CANCELED = 0：源端结果码的取值，目标照搬（出处：android.app.Activity#RESULT_OK、android.app.Activity#RESULT_CANCELED）
- 修好后结果函数改为 async，先等保存队列，再 terminateSelfWithResult({ resultCode: -1 / 0, want.uri })：修好后的做法（出处：卡里修好并验证过）
- terminateSelfWithResult(parameter: AbilityResult): Promise<void>：同族接口：UIExtensionContentSession 上的同名方法（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIExtensionContentSession.d.ts，UIExtensionContentSession.terminateSelfWithResult）
未核实：卡里的行为在 target SDK 6.1.1(24) 下观察，本机核实用的声明是 API 23
来源：1 张卡，1 个应用
- case-76fcde297f6a5406e58f（opencamera-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
