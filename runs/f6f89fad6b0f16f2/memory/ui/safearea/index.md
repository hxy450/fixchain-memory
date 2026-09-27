# ui/safearea

沉浸式安全区：避让区测量与 px/vp 换算（状态栏、导航指示条），系统栏图标深浅，路由页内容原点与顶部 inset 的消费位置，Tab 宿主按各 Tab 沉浸设置处理顶部安全区，全屏页底部按钮、按键区与贴底弹层的避让及承载层，逐页落实前景避让

[上一级](../index.md)

## 本级经验

- [Tab 宿主按各 Tab 源 Fragment 的沉浸设置分别处理顶部安全区，Activity 只加在底栏的 padding 只加到 tabBar](lesson-48e9408812c28e934db8.lesson.md)
  - 时机：界面实现与规格阶段，实现 MainActivity/Tab 宿主的内容区内边距，以及转换作为 Tab 子组件的 Fragment 的顶部布局时
  - 情境：Android MainActivity 只给底栏容器加内边距，ViewPager 全宽；部分 Tab 的 Fragment 调用 ImmersionBar.titleBarMarginTop/fitsSystemWindows 让头图延伸到状态栏，其余 Tab 不沉浸；目标宿主可能给整个 Tabs 统一加顶部安全区和左右 padding，页面规格按 page_type（sub_component）自动标记“无需沉浸”。
- [getWindowAvoidArea 与 windowRect 的数值是 px：写入供 padding 消费的窗口模型前先 px2vp](lesson-cf111aadb8804649b578.lesson.md)
  - 时机：沉浸式安全区实现阶段，在 EntryAbility 或窗口服务里把避让区、窗口尺寸写进共享窗口模型时
  - 情境：目标用 setWindowLayoutFullScreen(true) 全屏，EntryAbility 通过 getWindowAvoidArea 取状态栏、导航条高度，通过 getWindowProperties().windowRect 取窗口尺寸，写入 AppStorageV2 共享的窗口模型；各页把这些值直接放进 .padding()/.height()，按 vp 解释。
- [全屏窗口下先确认路由页的内容原点：已在状态栏 inset 之下就只补源端顶距的剩余部分，背景需延伸到状态栏时在背景节点自身 expandSafeArea](lesson-c7ee1769ca29abd236d3.lesson.md)
  - 时机：界面实现阶段，为全屏窗口中的路由页（NavDestination/HMRouter 页，含 Tab 子页）确定顶部起点、状态栏 inset 的消费位置以及背景是否延伸到状态栏时
  - 情境：Android 页面在透明状态栏下用自屏幕顶部起算的固定顶距（layout_marginTop、getStatusBarsHeight）给顶栏留位，背景铺到状态栏后面；目标 EntryAbility 全屏并发布 windowTopPadding，入口只在 Navigation 宿主上 expandSafeArea(TOP)，页面经路由框架承载。
- [全屏窗口的底部避让：导航指示条取 bottomRect，贴底按钮、按键区、Tab 栏与 bindSheet 内容都叠加避让值，并加在占据屏幕底边的那一层](lesson-0e1c846868f2683cc280.lesson.md)
  - 时机：沉浸式安全区实现阶段，测量导航指示条避让区，并为底部按钮行、按键区、Tab 栏或贴底弹层确定底部间距及承载它的容器层时
  - 情境：目标页面在 setWindowLayoutFullScreen(true) 下用 getWindowAvoidArea 测避让值，写入页面或全局窗口模型；Android 源布局的底部按钮行、底部 sheet 没有导航栏间距（源窗口不延伸到导航栏下，BottomSheetDialog 由系统处理 inset）。或页面规格标注全屏页、需要沉浸式安全区，入口对 BOTTOM 边 expandSafeArea，根容器与底部内容层背景色不同。
- [系统栏图标深浅按源端状态栏配置设置，不照搬沉浸式模板的浅色文字默认值](lesson-824031d5fddf81036b54.lesson.md)
  - 时机：沉浸式窗口配置阶段，调用 setWindowSystemBarProperties 设置 statusBarContentColor/navigationBarContentColor 时
  - 情境：目标全屏窗口把系统栏背景设为透明，页面内容延伸到状态栏下；Android 源端 BaseActivity/主题用 ImmersionBar darkMode(true)、windowLightStatusBar 或白色状态栏配深色图标；沉浸式 skill 示意写“透明背景 + 浅色文字”。
