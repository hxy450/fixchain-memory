# Fragment 事务压栈打开的子页

agent 会看到什么：读到 FragmentTransaction 的 replace 或 hide + add 加 addToBackStack 在宿主内容区打开子页（含 page_type=sub_component、CardView 卡片式宿主）；产物里子页写成 NavDestination、pushPathByName 推出壳外或清栈切页

## 规矩

- rule-4061e7c7c192｜调用点按源端 API 区分清栈切页与壳内压栈，不把压栈子页写成清栈切页｜读到：源端调用点有的走清栈加载（替换内容区并保存最后页），有的走压栈加载（addToBackStack、不持久化），如区段「更多」、搜索、单集详情；写错：压栈的调用点在目标写成清栈切页（并保存最后页 tag），或写成 pushPathByName 推出壳外
- rule-6d303fef8f70｜源端壳内 hide+add+addToBackStack 压栈的子页，目标在壳状态里维护子回退栈｜读到：源端单 Activity 壳在内容区用 FragmentTransaction 的 hide(当前) + add(子 Fragment) + addToBackStack(...) 压栈加载子页，子页期间底部导航和迷你播放条仍在，工具栏随回退栈深度切换上箭头，带导航 tag 时同步底部导航选中；规格 AC 用「标:」点名壳路由的子页加载方法；写错：子页写成 pushPathByName 推到壳外的 NavDestination；返回首分支写 navPathStack.size() > 1 交系统弹栈；壳状态里没有子回退栈字段，壳路由只有清栈切页入口
- rule-a215b61a5ee7｜sub_component 子页转成 @Param 嵌入组件，由壳内容区承载，不包 NavDestination｜读到：meta.page_type=sub_component，规格写「Fragment，宿主 Activity」「Toolbar 返回 = popBackStack 返回上级」，源码经 addToBackStack 压栈打开；写错：页面写成 NavDestination(){…} 包裹、@Consumer 取 navPathStack、返回时 pop()，并在 pageMap 或路由表里注册了它
- rule-8e2933c6f2b6｜卡片式宿主里新增子页时，按源容器复刻卡片几何并用透明 DIALOG 路由｜读到：子 Fragment 经 `replace(R.id.<容器>, fragment).addToBackStack(...)` 进入卡片式宿主里（`CardView` 包住的）同一个容器；写错：新子页写成默认模式的 `NavDestination` 全屏 `Column`，只设安全区 padding 和不透明 `backgroundColor`，没有卡片几何，子页盖住整个屏幕
- rule-b61baae72283｜源端每次 replace 新 Fragment 时，目标用 pushPath 加 NEW_INSTANCE｜读到：已有详情 Fragment 时先 popBackStackImmediate() 再 replace(…, new 出来的 Fragment)，否则 replace + addToBackStack；每次都是新实例；写错：同一轮里 navPathStack.pop() 后 pushPathByName(同名页, param)，或只写 pushPathByName 并注释「addToBackStack 由 NavPathStack 天然保留」；同名 NavDestination 被栈复用，新页 onReady 不触发
- rule-b642eb2f976c｜源端 popBackStack() 时，目标把 pop 推迟到下一轮并在根页不出栈｜读到：返回分支调 popBackStack()（异步），并按 getBackStackEntryCount() == 1 判断是否回到列表根；写错：同步调 navPathStack.pop()，不判断栈深，会越过列表根
