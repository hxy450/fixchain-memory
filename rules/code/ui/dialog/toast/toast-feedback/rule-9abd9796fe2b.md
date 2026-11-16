# 规格把 Toast 上移到调用层时，服务失败仍按 AC 写明的源端原文提示

审的是：代码
触发（任一种）：
- 读到：规格 AC 写了服务两个失败分支各自的 Toast 原文：结果为空时一句固定文案，请求异常时显示异常的 message；写错的样子：服务两种失败都只返回 ''，异常的 message 只进 console.error，页面弹自造的通用 $r('app.string.…') 文案
适用范围：服务层实现时，规格写了失败提示原文、又把 Toast 放到调用层
做法：
- 服务接收 UIContext，在各失败分支调 uiContext.getPromptAction().showToast({ message: … })：结果为空时 message 用 AC 写的那句原文，请求异常时 message 用异常的 message
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showToast(options: promptAction.ShowToastOptions): void：PromptAction 弹 Toast（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.showToast）
- message: string | Resource：ShowToastOptions 的提示文本，可直接传字符串或资源（出处：鸿蒙 SDK 的 ets/api/@ohos.promptAction.d.ts，ShowToastOptions.message）
- getPromptAction(): PromptAction：从 UIContext 取 PromptAction（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getPromptAction）
针对本应用要查的：
- 每个失败分支的提示原文：规格里这项服务的验收条目（AC），或源工程里服务实现的失败分支；固定文案照抄；写着显示异常信息的，运行时取异常对象的 message
来源：1 张卡，1 个应用
- case-f63ccb39dd60e2abb04b（jerboa）：做法第 1 步 ← 建议 5、诊断
