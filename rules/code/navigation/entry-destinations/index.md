# 点击入口跳到哪一页

agent 会看到什么：读到源端点击监听里 startActivity(Intent) 到别的 Activity、工厂按类型分给不同 Fragment、工具栏各按钮各自的 setOnClickListener、SDK 弹窗配置里的各个回调；产物里入口的 onClick 有没有 pushPathByName / router.pushUrl 到对的页、注册了路由，还是只有 Toast 或 FWD-REF 占位

## 规矩

- rule-afe2d28bd046｜源端入口 startActivity 到二级页，目标写 pushPathByName 并注册路由，不用 Toast｜读到：源端点击监听里 startActivity(Intent(...)) 到另一个 Activity；写错：目标端对应入口的点击回调里只有 promptAction.showToast(...) 提示「本轮暂不可用」，或没有响应，或交给统一的 FWD-REF 占位回调；Navigation 的 navDestination 构建函数里没有目标页
- rule-964e7e411c8c｜契约写安卓点击启动独立 Activity 并带参数时，目标用 router.pushUrl 带等价参数跳转｜读到：源端点击里 startActivity(intent) 并 putExtra 当前项和类型等参数，或规格写「入口 → 某 Activity，传 …」；写错：目标端 onClick 里打开页内的简化面板，没有 router.pushUrl 到对应的共享页面，或跳转时没带源端那些参数
- rule-5b56daf13f9f｜接线解除导航类前向占位时，pushPathByName 的目标页按规格导航表或源端 Intent 定，不按名字猜｜读到：子组件只发事件或枚举值、带 `FWD-REF` 标记的导航回调没写目标页；路由表里同一前缀注册了多个名称相近的页面；写错：接线代码里 pushPathByName('…') 的目标是按枚举名或页面名的字面相似度选的，另一个候选页在路由表里成了没有入口的孤儿页
- rule-267e4254b9a8｜源端工厂把相近类型映射到不同 Fragment 时，目标端各保留各的去向｜读到：源端工厂（按类型字符串 when / switch 返回不同 Fragment）把几个相近类型分给不同 Fragment：一个点击进编辑页，另几个进选择页；写错：目标端把这几个类型合并进同一个选择处理（同一个回调、同一个 pushPathByName 目标），原本进编辑页的类型也去了选择页
- rule-bdb284ef42ef｜替换或重排已有工具栏按钮时，按安卓监听代码的按钮→目标表逐个改 onClick，不沿用旧槽位回调｜读到：安卓 Activity 给顶栏每个按钮分别 setOnClickListener，目标各不相同（同一面板的不同 tab、另一个 Activity、评论列表）；行为说明里给出了按钮→目标的绑定表；写错：目标工具栏里只换了 SymbolGlyph / Image / Text 的显示内容，.onClick(...) 还是被替换占位槽位原来的回调；两个不同按钮跳同一个 router.pushUrl 目标，或某个 sheet 分支已没有按钮能打开
- rule-57cd5aeee7b9｜自绘弹层替代源端 SDK 弹窗时，源配置里的每个回调都映射到 onClick 和路由｜读到：源端启动页给第三方隐私弹窗配置对象注册了多个回调：服务协议链接、隐私政策链接各自 startActivity 打开 WebView 页，另有同意、拒绝回调；写错：自绘弹层里协议文字只是 Text(...).fontColor(...) 或 .fontWeight(...)，没有 .onClick，也没有 `FWD-REF` 占位；只有取消、确定接了回调
- rule-a49fd7b3b5dc｜接入已有专页时逐项实现它的 @Event 回调契约，要回传结果的不用空值短路｜读到：已有 ArkTS 子页声明了 @Event 回调，参数里带回传函数（如 onReady: (id: string) => void），子页只有拿到非空结果才 pushPathByName 进入下一页；写错：容器实现这个回调时改调别的处理再回传空值（onReady('')），或不调用回传函数，子页自带的导航被跳过
- rule-78e148ddcff2｜只依赖本地平台 API 的源端动作，在本切片直接实现，不写只有 FWD-REF 注释的空方法｜读到：源端 onClick / onResume 里调用缓存大小统计、清理缓存或跳应用市场详情的方法；写错：目标的点击处理方法体只有 `FWD-REF` 注释，没有实现
- rule-5fe890c1a59d｜源端点击触发的导航 effect，逐个落成目标 onClick 里的 router.pushUrl 带参跳转｜读到：源 Fragment 里的点击（`setOnClickListener`、适配器的点击回调）调 ViewModel，ViewModel 发出的导航 effect 在 Fragment 里经 `navigate(R.id.…, bundleOf(…))` 跳到详情页或编辑页；写错：目标里对应的卡片、列表项、空状态按钮没有 `.onClick`，或者整页没有 `router.pushUrl` 调用
- rule-b5cffa0f5838｜可见入口的点击处理只有 FWD-REF 注释和 return 时，按源码目标实现跳转｜读到：源端点击回调打开固定 URL 的 WebView 页，或带列表索引参数打开详情 Fragment；写错：目标端对应的点击处理函数体只有 `// FWD-REF: …` 注释和 `return;`
- rule-8e7002a4fe98｜onClick 回调体不能只有注释；实现不了的写 TODO: 占位并登记，或报未完成｜写错：`.onClick(() => { // Navigate … })` 这类回调体只有注释或为空，注释里也没有 `TODO:`，占位登记里没有它
- rule-3709ca669221｜写 fail-loud 占位前逐项核对源端实现和目标端等价组件，两者都有就接线，不笼统报「契约未确认」｜读到：源端这些动作（分享、附件、前序、添加后续、更多菜单）在共享的 DialogFragment 或公共分享弹层里已有实现；写错：动作分发的兜底分支（`default` / else）统一弹「该操作所需契约尚未确认，暂不可用」之类的提示，把多个可见动作都落进去
- rule-78cc3726b640｜源页面里每个 setOnClickListener 在目标都有对应 onClick，含非 initView 函数里的｜读到：源 Activity / Fragment 的 lazyLoadData、initListener 等非 initView 函数里有 setOnClickListener，或 currentItem / setCurrentItem 一类交互调用；写错：目标对应的组件没有 .onClick，交互只按布局 XML 和页面回调转写
- rule-aee8c267b0c7｜源列表首项是调色盘、相册、图库入口时，接到对应页面并把结果写进编辑配置｜读到：源 Fragment 的 onItemClick 里第 0 项（或特殊项）弹调色盘对话框、打开相册或图库，其余项把选中的 bean 写入编辑配置；写错：目标列表项 onClick 里只切换选中标记，首项不打开调色盘或图库，选中结果也没写进编辑会话的配置
