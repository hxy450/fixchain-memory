# 对话框接口的条目和回调参数

agent 会看到什么：读到 ViewModel 或 presenter 接口的对话框方法带条目列表和多个回调参数（选中某项、清空、onCancel），或 AlertDialog 的 setItems；产物里页面实现用 void 丢弃回调，或用 showAlertDialog 只显示拼起来的条目

## 规矩

- rule-a25184e7c55d｜对话框接口带多个回调参数时，页面把每个回调接到可点的项上，不用 void 丢弃｜读到：ViewModel 或 presenter 接口的对话框方法带条目列表和多个回调参数（选中某项、清空、另选、onCancel），注释写「N 个条目 + 固定尾项」；写错：页面实现里写 `void onPick` 这类 void 表达式丢弃回调，或用 showAlertDialog 只显示 entries.join('\n') 和一个确认按钮
