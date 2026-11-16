# 页面映射表记 showSnackbar 的动作、关闭钮和时长，不只写 Snackbar → showToast

审的是：规格
触发（任一种）：
- 读到：源码 showSnackbar(…, actionLabel, withDismissAction = true, SnackbarDuration.Short/Long)；映射参考里有「Snackbar → getUIContext().getPromptAction().showToast() 轻提示」一行；写错的样子：页面规格的映射表只写「Snackbar → showToast 轻提示」，没记动作文案、withDismissAction、时长和调用方是否读 SnackbarResult
适用范围：规格提取阶段，页面规格里写提示（Snackbar / Toast）映射的那几行
不适用的情形：showSnackbar 没有动作、没有关闭钮的纯提示，可以照通用映射写成 showToast
做法：
- 映射表里每处 showSnackbar 记一行：动作文案（有/无）、withDismissAction、时长（Short/Long/Indefinite）、调用方是否读 SnackbarResult；有动作、关闭钮或读结果的，映射写自绘 Snackbar，不写 showToast
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- showToast(options: promptAction.ShowToastOptions): void：Toast 没有返回值，ShowToastOptions 里没有动作钮、关闭钮字段，映射成它就丢了这些参数（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，PromptAction.showToast）
来源：1 张卡，1 个应用
- case-16e909b950f12edb0251（jerboa）：做法第 1 步 ← 建议 4；例外 1 ← 建议 4
