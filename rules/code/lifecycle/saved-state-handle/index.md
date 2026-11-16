# SavedStateHandle 保存态和数据库值的先后

agent 会看到什么：读到源 ViewModel 用 SavedStateHandle 的 contains / get 守卫表单字段、保存态有值就不取数据库值，或规格 AC 写保存态优先；产物里 aboutToAppear 无条件用数据库值给表单字段赋值，或记成「无等价物，残余」

## 规矩

- rule-3cbb40039537｜源端 SavedStateHandle 守卫而 AC 要求保存态优先时，实现草稿持久化，不登记为无等价残余｜读到：源 ViewModel 每个表单字段由 if (!state.contains("…")) 守卫，只在 SavedStateHandle 没有该键时才取数据库值；写错：目标端 aboutToAppear 加载时无条件把数据库值赋给表单字段
