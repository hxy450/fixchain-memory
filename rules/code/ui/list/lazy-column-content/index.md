# LazyColumn 列表页的内容结构

agent 会看到什么：读到 Compose Screen 里 LazyColumn 的 items（按父项分组的卡片、isEmpty() 时的空态、列表卡片和状态 Tab）；产物里 List / ForEach 把子项拍平、没有空列表分支，或只用 Text(JSON.stringify(...)) 回显响应

## 规矩

- rule-de71f7763b8c｜安卓列表按父项分组成卡片、卡内列子项行时，目标按父项 ForEach 出卡片，不把子项拍平｜读到：安卓 Compose Screen 的 `LazyColumn` 里每个 item 是一张按父项（如商品）分组的卡片，卡内再列子项（如规格）行；目标数据模型已按父项聚合子项数组；写错：目标页面用嵌套 `ForEach` 把每个子项渲染成独立行，并在每行重复父项标题，没有父项卡片这一层
- rule-9ce70a7fcec4｜源列表在 isEmpty() 时渲染空态，目标 List 也要有空列表分支，复刻图标、标题和提示｜读到：源端 LazyColumn 的分区在列表 isEmpty() 时渲染内联空态组件（图标 + 标题 + 提示文案），这段在页面调用的子组件文件里；写错：目标 List 里只有 ForEach 设备行，没有 if (列表.length === 0) 的空态分支
- rule-fad2f168a8f0｜页面把接口响应 JSON.stringify 后塞进 Text 时视同占位，改成解析成模型、按 AC 渲染｜读到：安卓对应 Screen 渲染列表卡片、表单字段、状态 Tab 和操作按钮；规格 AC 列了分页、默认、增删改或状态筛选、领取等；写错：页面请求后 Text(JSON.stringify(await …)) 回显整段响应，没有模型、列表项、状态筛选和操作按钮；或照抄了同类回显壳的兄弟页面
