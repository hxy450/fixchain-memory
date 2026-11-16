# SearchView 迁成 Search

agent 会看到什么：源端的 SearchView（工具栏菜单里的 actionView、OnQueryTextListener.onQueryTextSubmit 里发起查询和改界面状态），对应目标 Search 组件的外观、onSubmit 和提交后才出现的界面状态

## 规矩

- rule-c3e9f3b1d9a6｜工具栏里展开的 SearchView 迁成 Search 用透明底，不加胶囊底色，提示色取 textColorHint｜读到：菜单项的 actionView 是 SearchView（或其子类），showAsAction 带 collapseActionView，挂在 Toolbar / MaterialToolbar 上；源码和布局没给它声明容器底色；写错：Search 上写了 .backgroundColor(…) 填充色（胶囊底），或者没写 .placeholderColor(…)，放大镜颜色和工具栏图标不一致
- rule-05a046a6ccc1｜SearchView 提交映射到 Search.onSubmit 时，补上去空白为空不提交的判断｜读到：SearchView（含 androidx.appcompat.widget.SearchView 及其子类）设置了 OnQueryTextListener，在 onQueryTextSubmit 里发起查询；写错：Search 的 .onSubmit((value) => …) 里直接发起查询或置加载状态，没有 value.trim() 为空就返回的判断
- rule-36aba4406d12｜源码在回调里才设置的界面状态，目标用回调后置位的状态门控，不改成静态派生｜读到：源码在回调或它调用的方法里（如 SearchView.OnQueryTextListener#onQueryTextSubmit 触发的查询方法）才显示某个尾部按钮、进度或空态，onCreateView 进入页面时不调用这个方法；写错：build() 里用只由参数或数据派生的静态条件（如 `list.length > 0 || …`）渲染这部分，注释写成「由 build 派生」，首屏就出现；没有一个只在回调执行后才置位的 @Local 状态
- rule-f36413344fa4｜复刻 SearchView 时展开、焦点、提交、收起、菜单重建分成独立状态，不用一个布尔加取消图标｜读到：源端 SearchView 作菜单 actionView，有 expandActionView / collapseActionView、OnActionExpandListener、setOnQueryTextFocusChangeListener；写错：页面里一个布尔同时表示「展开」和「焦点」，展开态只渲染 TextInput 加取消图标，取消时清空了事；没有 collapse 出口、菜单重建时收起、空串不提交、提交后收键盘
- rule-157623058aaf｜菜单状态挂在输入框焦点上时绑定 TextInput 的 onFocus/onBlur，不用手工布尔开关｜读到：源端 SearchView.setOnQueryTextFocusChangeListener 按焦点切换菜单显隐；规格写「搜索焦点下某些菜单可见、其他隐藏」；写错：标题栏用一个点击时手工翻转的布尔量决定展开态和菜单矩阵，TextInput 没有 .onFocus / .onBlur，展开时不 requestFocus
