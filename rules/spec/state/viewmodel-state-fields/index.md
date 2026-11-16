# ViewModel 的状态字段和格式化字段

agent 会看到什么：读到 ViewModel 用布尔状态切换覆盖层、数组常量当 Tab 文案，或用返回 LiveData<String> 的 getter 给文案模板 "${x}…" 插值；页面规格只是通用模板，状态契约只写原始数值字段

## 规矩

- rule-6fcde5695ad1｜多状态页面的规格列出状态变量、各状态可见节点、Tab 顺序和列表项字段｜读到：源页面由 ViewModel 的布尔状态切换两套覆盖层，Tab 文案来自 ViewModel 的数组常量，列表项来自 item 布局；写错：页面规格只是通用模板，只列可见文本并指向布局文件，没写状态变量、各状态的可见节点、Tab 顺序和列表项字段；功能 AC 列举模式的顺序和源数组不同
- rule-7d1d65f1ba63｜源端文案模板插入格式化文本字段时，规格写明插值的源 getter、类型和格式｜读到：源端文案写成 "${x}…"，x 来自观察一个 text 前缀、返回 LiveData<String> 的 getter；同一 ViewModel 另有同名的 LiveData<Integer> 原始数值字段；写错：规格状态契约只写了原始数值字段（如 xxx: number），格式化字段清单（@Computed）里没有它，验收条目只留「{x}…」占位，没写 x 是什么格式
