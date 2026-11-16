# EditText.setError 的字段错误提示

agent 会看到什么：读到源码校验时对 EditText 调 setError(...)；产物里 TextInput 下面条件渲染的红字 Text、.showError(...)，或尾部错误图标加浮层气泡、改字即清的写法

## 规矩

- rule-329a0b157ac8｜源码对 EditText 调 setError 时，目标用尾部错误图标加获焦浮层、输入即清，不用行内红字｜读到：源码对 EditText 调用 setError(...)（多在字段校验处）；写错：目标在 TextInput 下面条件渲染错误 Text（if (…Error) Text(...) 小字号红字，出错时撑高弹窗或表单），或用 TextInput 的 .showError(...)；没有尾部错误图标和获焦浮层
