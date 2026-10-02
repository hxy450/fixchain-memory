# ui/interaction

点击命中与手势：Stack/弹窗覆盖层对下层点击的影响、hitTestBehavior与防穿透、事件绑定和点击副作用、侧滑行的手势归属与滑删方向，以及事件触发时的坐标与锚点取值；含状态按钮的内容分支。

[上一级](../index.md)

## 本级经验

- [Button 内按状态切换图标时写成一个 if/else 或单个 Image 按状态选资源，不写两个互斥的独立 if](lesson-ed5556325b6d8f510e2f.lesson.md)
  - 时机：界面实现阶段，为播放/暂停一类两态按钮编写 Button 的子内容时
  - 情境：源端按钮按状态切换图标，目标用 Button() { ... } 包裹图标，准备按两个状态分别写条件分支。
- [Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，贴底内容栏直接锚定而不套全屏壳，条件遮罩与一次性动效层用根 Stack 条件子节点](lesson-4a4f8d845a204ffa244b.lesson.md)
  - 时机：界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 与贴底栏的定位方式时；为页面加保存中、引导等全屏遮罩时；实现彩纸等一次性全屏动效的覆盖层时
  - 情境：源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。也包括源 Compose Box 中返回按钮等可点击覆盖层之后，还有以 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高的底栏，目标 Stack 的 alignContent 改为 TopStart 后需要另找贴底方式。也包括源端在触发瞬间向窗口根视图添加全屏、不可点击的动效层并在播完后移除，目标改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。
- [SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，不凭枚举名加“左滑/右滑”注释](lesson-7f5eba1b969bddfb34dc.lesson.md)
  - 时机：规格提取与界面实现阶段，转写 Material3 SwipeToDismissBox 的滑删方向、在列表行内自定义滑删手势时
  - 情境：源端用 enableDismissFromStartToEnd、EndToStart 等枚举描述方向，背景对齐方向与之配合；目标在列表行内用 Stack + PanGesture 一类写法自定义滑删。
- [修可侧滑行的按钮点击被内容层拦截时，把调整限定在按钮热区，不把承载滑动手势的整张内容层设为 HitTestMode.None](lesson-6677d286e690407d4af4.lesson.md)
  - 时机：界面缺陷修复阶段，为可侧滑列表行解决展开后操作按钮点击被上层内容拦截的命中冲突时
  - 情境：列表行用 Stack 叠放底层操作按钮与上层内容卡片，卡片以 translate 平移露出按钮，并在同一节点上绑定点击（未展开进详情、已展开则收起）与横向 PanGesture（展开或收起）。
- [弹窗防穿透的 Block 只放在无子控件的遮罩层，内容面板与根容器保持 Default；改真弹窗 API 后删掉自绘防穿透](lesson-cf018b76af68b4c00895.lesson.md)
  - 时机：弹窗或浮层实现与改造阶段，为遮罩、内容面板、根容器设置 hitTestBehavior，或把页面内浮层迁到 showCustomDialog/showBindSheet、openCustomDialog 等真弹窗时
  - 情境：弹窗或底部面板采用“根 Stack + 遮罩 + 内容面板”结构，在根或内容面板上写 hitTestBehavior(HitTestMode.Block)（含 visible ? Block : None）防止点击穿透；面板内有按钮、checkbox、列表项等要响应点击的子控件。也包括源端用全屏空 clickable 拦截层防穿透、遮罩点击关闭、居中卡片阻止冒泡，目标在包住遮罩、卡片、滑杆与滚动区的弹层根 Stack 上写 Block。
- [源端在触发瞬间读取锚点窗口位置时，目标在点击回调里取本次手势坐标或即时查询，onAreaChange 缓存只作兜底；锚点取源端传入的同一元素](lesson-963bf871aa4e910a8fc8.lesson.md)
  - 时机：界面实现与修复阶段，为从点击处发出的动效或气泡（完成彩纸、锚点提示）确定起点坐标与锚点元素时
  - 情境：源端在动效或弹窗被调用时用 getLocationInWindow 读取传入锚点 View 的当下窗口中心；目标列表项存在 translate 平移、LazyForEach/Repeat 节点复用或弹层内滚动，写者准备用 onAreaChange 缓存控件位置。
- [点击事件挂在源布局真正持有点击的节点上；清理重复绑定时保留整栏容器的事件](lesson-fd3add7128663eb9998f.lesson.md)
  - 时机：界面实现与返修阶段，为由多个子控件拼成的搜索栏、入口条决定 onClick 挂在哪一层，或清理其中的重复点击绑定时
  - 情境：源布局只在整条容器上绑定点击（如 LinearLayout 的 onClick 或 DataBinding 点击），内部图标、提示文字、“搜索”字样只负责展示；目标用 Row + Image + Text 模拟占位搜索框（不是 TextInput），点击后压栈进入目标页。
- [迁移带点击绑定的控件时按源点击处理器的分支逐项迁移副作用，不只做状态取反和换图](lesson-55e33a0621c3008ab8b3.lesson.md)
  - 时机：界面迁移阶段，为布局中带 onClick 绑定、状态选图或滑动面板的控件编写 ArkUI 事件与状态逻辑时
  - 情境：源布局控件用 android:onClick/数据绑定声明点击，或按 ViewModel 状态选图；实际行为（按键音、振动、偏好持久化、历史面板展开与回填）写在 Fragment 统一点击处理器、ViewModel 或第三方面板组件中；目标页需复刻这些开关与面板。 也包括源端 ViewModel 的选择与写操作（再次点击同一项即取消、前置为空即失败、同商品同规格累加写入本地购物车）由页面弹层触发。
