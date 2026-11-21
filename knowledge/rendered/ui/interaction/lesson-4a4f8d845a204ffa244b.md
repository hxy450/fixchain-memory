# Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，贴底内容栏直接锚定而不套全屏壳，条件遮罩与一次性动效层用根 Stack 条件子节点

## 何时使用

界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 与贴底栏的定位方式时；为页面加保存中、引导等全屏遮罩时；实现彩纸等一次性全屏动效的覆盖层时

## 适用情境

源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。也包括源 Compose Box 中返回按钮等可点击覆盖层之后，还有以 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高的底栏，目标 Stack 的 alignContent 改为 TopStart 后需要另找贴底方式。也包括源端在触发瞬间向窗口根视图添加全屏、不可点击的动效层并在播完后移除，目标改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。也包括按钮之上叠有同尺寸、不可点击的自绘进度环或加载圈（源端触摸落到下层按钮），目标 Stack 保留 z 序而点击只挂在最底层图片上。

## 原因

ArkUI 中没有 onClick 的容器同样参与命中测试（HitTestMode.Default 会阻塞兄弟），全尺寸上层会吞掉下层点击，hilog 表现为 Touch test result is empty。为还原源端 z 序重排子节点后，原先“浮层设 Transparent”的标注会落在错误的层上；调整对齐或几何会放大覆盖区。.overlay() 挂条件 builder 在条件为假时仍会产生拦截触摸的层，挂在带 padding 的容器上又只覆盖内容盒、盖不到底部安全区。另一应用中巡检修复者为让底栏贴底，在返回按钮之后新增 width/height('100%') 的 Column{ Blank(); 底栏 } 作定位壳；这个后声明、默认命中模式的全屏壳盖住了左上角返回按钮，点击无响应，直到给按钮加 zIndex 才恢复。另一应用把完成彩纸组件无条件挂在日视图、月历弹层和详情弹层上（100% 宽高、zIndex 100），空闲时只清空画布；内部 Canvas 设了 None，外层组件节点仍拦截，日视图不能点击和滑动，改为仅在播放期间条件挂载才恢复。

## 做法

1. 按最终声明顺序逐层检查：位于可点击兄弟之上、覆盖其区域且自身不处理点击的容器，显式写 hitTestBehavior(HitTestMode.Transparent)；重排子节点或修改对齐与几何后重新核对。 命中模式只作用于写它的节点：外层定位容器写 None 后，内部有尺寸的绘制子节点仍按 Default 命中，照样挡住外层容器下方的兄弟，要在这些子节点上各自写（外层写 Transparent 时下层兄弟仍参与命中）；可开合的浮层容器（如关闭态只剩平移到屏外的面板、遮罩按条件渲染的抽屉浮层）随状态切换，打开 Default、关闭 Transparent。
2. 源端按内容定高、align(BottomCenter) 贴底的底栏，在 Stack 中保持自身尺寸并直接锚到底部（position 的 bottom 边或 RelativeContainer 的对齐规则），不用满屏 Column + Blank 作定位壳；确需全屏壳时给壳设 Transparent，或让可点击的覆盖控件最后声明、提高 zIndex。
3. 页面级全屏遮罩用无 padding 的根 Stack 条件子节点实现（条件为假时不产生节点），不在带 padding 的容器上用 .overlay() 挂条件 builder；复用同仓遮罩时连同挂载层级一起复用。
4. 一次性全屏动效（彩纸、提示动画）按源端生命周期只在播放期间条件渲染，结束或取消回调里移除；不要让全屏组件常驻，只靠内部子节点的 HitTestMode.None 放行。 条件渲染只解决空闲期：源端播放期间也不拦截触摸时，在挂载实例上同样写 Transparent（写 None 只管实例这一层，组件内部按 Default 命中的节点仍会挡住下层兄弟，见第 1 步）——调用处的 width/height/zIndex 等通用属性会生成缺省命中的外层节点，组件内部根节点（含 Canvas）上的设置管不到它（见 lesson-6aeb4924b6d6ee3d15f6）。
5. 按钮上叠的进度环、加载层同样逐个决定命中：纯展示节点设 Transparent，或把 onClick 挂在整个 Stack 容器上，不只挂在最底层图片。

## 可选检查

- 调整 Stack 对齐、上层几何或新增定位壳后，对被覆盖区域的按钮逐个实际点击（不只看节点 clickable 与 bounds），检查 hilog 有无 Touch test result is empty。
- 一次性动效层改动后，空闲态用 dumpLayout 确认该节点不存在，再实测点击、横滑与折叠。

来源支持：7 张卡 · 6 次迁移 · 6 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1；Android SDK 平台资源 android-34。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕HitTestMode 各值（应用没有设 hitTestBehavior 时为 Default）：Default 自身和子节点响应触摸测试，阻塞被它遮住的兄弟节点，不影响祖先；Transparent 自身和子节点响应，不阻塞兄弟和祖先；None 自身不响应，不阻塞子节点、兄弟和祖先；Block 自身响应，阻塞子节点、兄弟和祖先。〔成立范围：依据是文档和声明注释，文档没有把阻塞兄弟限定在绑定了事件的节点上。None 只说节点自身：它的子节点被点中时照样按子节点自己的模式挡住下层兄弟（见下一条），Transparent 则连同子节点一起不阻塞兄弟。影响点击、触摸、拖拽、鼠标、悬浮和手势等事件。设了 enabled(false) 的组件及其子组件不发起触摸测试、直接回到父组件继续，不阻塞兄弟。API 20 起另有 BLOCK_HIERARCHY（阻止优先级较低的兄弟和父节点）和 BLOCK_DESCENDANTS（自身和全部后代都不响应）。〕
- 〔做法第 1 步〕Stack 里上层节点的子组件被点中时，上层节点设 None 仍挡住下层兄弟（子组件按 Default 命中后阻塞），只有给上层节点设 Transparent，下层兄弟才继续参与触摸测试。〔成立范围：依据是文档说明和 hitTestBehavior 文档的示例 4（上层全尺寸 Stack 里放按钮，点按钮时 None 下层背景收不到、Transparent 收得到）。点在上层节点没有子组件的区域时，None 和 Transparent 都放行。〕
- 〔做法第 4 步〕在调用处给自定义组件链式设通用属性（width、height、zIndex、hitTestBehavior 等）时，相当于给它套了一个不可见的容器组件，属性设在这个容器上，而不是组件 build 里的根节点上；这个容器没设 hitTestBehavior 时按 Default 命中。〔成立范围：依据是文档说明（文档示例是 @Component）；调用处一个通用属性都不设时，文档没有说会套容器。组件内部根节点或 Canvas 上写的 hitTestBehavior 管不到调用处生成的这层容器。〕
- 〔适用情境〕安卓 ViewGroup 分发 ACTION_DOWN 时从绘制顺序最上层的子 View 往下逐个尝试；View.onTouchEvent 只有在 clickable、long-clickable、context-clickable 或带 tooltip 时才消费事件，所以不可点击的上层 View（含 match_parent 的 FrameLayout 子层）不消费，触摸落到下层兄弟。〔成立范围：setOnClickListener、setOnLongClickListener 会把 View 设为可点击；Widget.Button 等控件样式自带 clickable=true；设了 OnTouchListener 且返回 true 也会消费；ScrollView 这类重写了 onTouchEvent 的滚动容器只要有子 View 就消费 ACTION_DOWN，不看是否 clickable；disabled 但 clickable 的 View 仍消费触摸（只是不响应），这与鸿蒙 enabled(false) 的组件不参与触摸测试相反。〕
- 〔做法第 2 步〕position 传 Edges 时以父组件内容区（父组件 padding 以内）的四边为基准，top、bottom、left、right 是到父内容区对应边的距离，在尺寸测量完成后生效；文档写明支持镜像模式的是 LocalizedEdges（start、end）。〔成立范围：依据是文档说明。同时设了 top 和 bottom 时只有 top 生效，同时设了 left 和 right 时只有 left 生效（不能靠两边一起设来拉伸）。父组件是 Row、Column、Flex 时设了 position 的子组件不占位；父组件是 RelativeContainer 且子组件设了 alignRules 时 position 不生效；父组件没设固定宽高时，参考第一个设了固定宽高的祖先定位；不能设在宽高为零的布局组件上。〕
- 〔做法第 2 步〕zIndex 只调整同一容器里兄弟组件之间的堆叠顺序，值大的盖在值小的上面；嵌在子容器里的组件设 zIndex，越不过它所在容器的兄弟。〔成立范围：依据是文档说明；不增减兄弟节点时动态改 zIndex，会在原层级顺序的基础上稳定排序。〕
