# SearchView 提交映射到 Search.onSubmit 时，补上去空白为空不提交的判断

审的是：代码
触发（任一种）：
- 读到：SearchView（含 androidx.appcompat.widget.SearchView 及其子类）设置了 OnQueryTextListener，在 onQueryTextSubmit 里发起查询；写错的样子：Search 的 .onSubmit((value) => …) 里直接发起查询或置加载状态，没有 value.trim() 为空就返回的判断
适用范围：安卓 SearchView 的提交回调迁成 ArkUI Search.onSubmit 时
做法：
- .onSubmit((value: string) => { if (value.trim().length === 0) { return; } …原 onQueryTextSubmit 的逻辑… })；判空放在置加载状态之前
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- if (query != null && TextUtils.getTrimmedLength(query) > 0) 才回调 onQueryTextSubmit：源端框架自带的前置过滤：去空白后为空的查询不会提交（出处：android.widget.SearchView#onSubmitQuery）
- onSubmit(callback: Callback<string>): SearchAttribute：回调参数是搜索框当前文本；声明里没有说会过滤空文本（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.onSubmit）
- onSubmit(callback: SearchSubmitCallback): SearchAttribute；SearchSubmitCallback = (searchContent: string, event?: SubmitEvent) => void：带 SubmitEvent 的重载（@since 14），判空写法相同（出处：鸿蒙 SDK 的 ets/component/search.d.ts，SearchAttribute.onSubmit、SearchSubmitCallback）
- 空回车时 Search.onSubmit 照样回调；不判空就会进入查询流程，加载状态一直不复位：所以过滤要在目标端自己补（出处：卡里修好并验证过）
未核实：androidx.appcompat 版 SearchView 的同一过滤只在平台 android.widget.SearchView 源码里核到
来源：1 张卡，1 个应用
- case-f226842558d82e3f3ad9（AntennaPod）：做法第 1 步 ← 建议 2、诊断；取值 4 ← 诊断
