# 源控件靠框架默认的行为（setError、预填光标、imeOptions）

agent 会看到什么：读到源控件只写了少数属性、其余靠框架默认：EditText.setError、onCreateDialog / onCreate 里 setText 预填、单行 EditText 不写 imeOptions、WebView 只 loadUrl 不调 getSettings；规格的转换决策只写组件对应，或写成实时校验、行内红字，没写默认行为和目标要显式设的属性

## 规矩

- rule-1a8cc808089f｜规格给每个迁移控件列一行「源端未显式设置、由框架默认决定的行为」及目标显式设置｜读到：源端控件只写了少数属性，其余靠框架默认：WebView 只 loadUrl 不调 getSettings，单行 EditText 不写 imeOptions，setError 只调一次；写错：规格转换决策只写组件对应（如「Web 组件加载 $rawfile」），没有「源端默认行为 vs 目标默认」一行，也没写目标要显式设置的属性
- rule-6164bd634151｜源端 setError 在规格里写「尾部错误图标 + 仅焦点框气泡 + 输入即清」，不写实时校验或行内红字｜读到：源端校验时调 EditText.setError(...)；写错：规格转换决策写「setError 字段校验 → TextInput .errorMessage / 错误状态变量，实时校验」，或写成输入框下常显红字
- rule-465b5bab5a4b｜源端 setText 预填输入框时，规格写明初始光标在开头、长文本从首行显示｜读到：源端 onCreateDialog 或 onCreate 里对 EditText 调 setText(...) 预填；写错：规格的预填只写了填入的值，没写初始光标位置和长文本从哪一行显示
