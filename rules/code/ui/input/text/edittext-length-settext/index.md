# EditText 的 maxLength 与程序写入（setText、TextWatcher）

agent 会看到什么：读过的源码里只有某个 EditText 声明了 android:maxLength，或程序用 setText 回填、载入后才 addTextChangedListener；交回的几个 TextInput 一并写了同一个 .maxLength、回填没按 maxLength 截断，或 onChange 把载入回显算成修改

## 规矩

- rule-c1b6283addec｜maxLength 等输入限制只加在源上声明了它的那个框，批量改写前逐框核对｜读到：一组 EditText 里只有某一个声明了 android:maxLength（或 android:inputType、android:singleLine），其他框没有；写错：几个对应的 TextInput 都写了同一个 .maxLength(...)，多由 replace_all 或多框模板批量改写时一并写回，源上没声明它的框也被限长
- rule-b0bf4c7995de｜粘贴或扫描回填写进带 maxLength 的输入框前，先截断到 maxLength 再赋值｜读到：EditText 带 android:maxLength，粘贴或程序回填用 setText(text) 写入；写错：目标的粘贴 / 回填回调直接把剪贴板或扫描结果赋给输入框绑定的状态变量，没有按该框的 maxLength 截断
- rule-e0302a510fec｜源端先载入文本再注册 TextWatcher 时，目标 onChange 把与已载入文本相同的回调视为回显｜读到：源端先 setText 载入已有文本，之后才 addTextChangedListener(TextWatcher)，载入不算修改；写错：目标 TextArea 的 onChange 无条件把变化计为修改，状态回写触发的 onChange 也标成已修改
