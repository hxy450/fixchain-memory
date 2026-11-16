# 源码里给用户的 Toast 和通知提示

agent 会看到什么：源码里有 Toast.makeText（LENGTH_SHORT / LENGTH_LONG 混用、文案带加工）或把接口返回的数据只经 Toast、Notification 交给用户，规格或源码笔记里把它记成统一时长、或没写怎么呈现

## 规矩

- rule-1b6e2a62c4a3｜源码理解笔记的 Toast 决策按调用点记时长和文案加工，不记成统一 LONG｜读到：源码里 Toast.LENGTH_SHORT 与 LENGTH_LONG 混用，部分文案带 toLowerCase 等加工；写错：source-notes 或决策台账写「服务层 Toast 统一 3500ms 对齐 LENGTH_LONG」，或「Resource 无法 toLowerCase，目标直接用资源原文」
- rule-175ffb4f8b71｜源端只经通知或 Toast 把接口返回的数据交给用户时，规格的 AC 写明它怎么呈现给用户｜读到：源端接口的成功回调（如 onData）把返回的数据（如验证码）交给发 Notification 或 Toast 的调用，界面本身不显示这个值；写错：规格只列了接口签名（如返回 Promise<string>）和「请求某数据」的 AC，没写返回的数据以什么方式交给用户
- rule-7c9284d69ebb｜页面映射表记 showSnackbar 的动作、关闭钮和时长，不只写 Snackbar → showToast｜读到：源码 showSnackbar(…, actionLabel, withDismissAction = true, SnackbarDuration.Short/Long)；映射参考里有「Snackbar → getUIContext().getPromptAction().showToast() 轻提示」一行；写错：页面规格的映射表只写「Snackbar → showToast 轻提示」，没记动作文案、withDismissAction、时长和调用方是否读 SnackbarResult
