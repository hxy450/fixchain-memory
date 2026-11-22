# Stack 上层全尺寸容器和页面级遮罩会参与命中测试：不处理点击的覆盖层显式 Transparent，贴底内容栏直接锚定而不套全屏壳，条件遮罩与一次性动效层用根 Stack 条件子节点

## 何时使用

界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 与贴底栏的定位方式时；为页面加保存中、引导等全屏遮罩时；实现彩纸等一次性全屏动效的覆盖层时

## 适用情境

源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器；或页面要在带安全区 padding 的根容器上加全屏遮罩。也包括源 Compose Box 中返回按钮等可点击覆盖层之后，还有以 Modifier.align(Alignment.BottomCenter) 贴底、按内容定高的底栏，目标 Stack 的 alignContent 改为 TopStart 后需要另找贴底方式。也包括源端在触发瞬间向窗口根视图添加全屏、不可点击的动效层并在播完后移除，目标改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。也包括按钮之上叠有同尺寸、不可点击的自绘进度环或加载圈（源端触摸落到下层按钮），目标 Stack 保留 z 序而点击只挂在最底层图片上。

## 原因

ArkUI 中没有 onClick 的容器同样参与命中测试（HitTestMode.Default 会阻塞兄弟），全尺寸上层会吞掉下层点击，hilog 表现为 Touch test result is empty。为还原源端 z 序重排子节点后，原先“浮层设 Transparent”的标注会落在错误的层上；调整对齐或几何会放大覆盖区。.overlay() 挂条件 builder 在条件为假时仍会产生拦截触摸的层，挂在带 padding 的容器上又只覆盖内容盒、盖不到底部安全区。另一应用中巡检修复者为让底栏贴底，在返回按钮之后新增 width/height('100%') 的 Column{ Blank(); 底栏 } 作定位壳；这个后声明、默认命中模式的全屏壳盖住了左上角返回按钮，点击无响应，直到给按钮加 zIndex 才恢复。另一应用把完成彩纸组件无条件挂在日视图、月历弹层和详情弹层上（100% 宽高、zIndex 100），空闲时只清空画布；内部 Canvas 设了 None，外层组件节点仍拦截，日视图不能点击和滑动，改为仅在播放期间条件挂载才恢复。

## 做法

1. 按最终声明顺序逐层检查：位于可点击兄弟之上、覆盖其区域且自身不处理点击的容器，显式写 hitTestBehavior(HitTestMode.Transparent)；源端该层本身消费触摸（设了 clickable、longClickable，或挂了点击监听，如用来挡住下层操作的加载遮罩）时，它本来就该拦截，保持 Default，不改成 Transparent。重排子节点或修改对齐与几何后重新核对。 命中模式只作用于写它的节点：外层定位容器写 None 后，内部有尺寸的绘制子节点仍按 Default 命中，照样挡住外层容器下方的兄弟，要在这些子节点上各自写（外层写 Transparent 时下层兄弟仍参与命中）；可开合的浮层容器（如关闭态只剩平移到屏外的面板、遮罩按条件渲染的抽屉浮层）随状态切换，打开 Default、关闭 Transparent。
2. 源端按内容定高、align(BottomCenter) 贴底的底栏，在 Stack 中保持自身尺寸并直接锚到底部（position 的 bottom 边或 RelativeContainer 的对齐规则），不用满屏 Column + Blank 作定位壳；确需全屏壳时给壳设 Transparent，或让可点击的覆盖控件最后声明、提高 zIndex。
3. 页面级全屏遮罩用无 padding 的根 Stack 条件子节点实现（条件为假时不产生节点），不在带 padding 的容器上用 .overlay() 挂条件 builder；复用同仓遮罩时连同挂载层级一起复用。
4. 一次性全屏动效（彩纸、提示动画）按源端生命周期只在播放期间条件渲染，结束或取消回调里移除；不要让全屏组件常驻，只靠内部子节点的 HitTestMode.None 放行。 条件渲染只解决空闲期：源端播放期间也不拦截触摸时，在挂载实例上同样写 Transparent（写 None 只管实例这一层，组件内部按 Default 命中的节点仍会挡住下层兄弟，见第 1 步）——调用处的 width/height/zIndex 等通用属性会生成缺省命中的外层节点，组件内部根节点（含 Canvas）上的设置管不到它（见 lesson-6aeb4924b6d6ee3d15f6）。
5. 按钮上叠的进度环、加载层同样逐个决定命中：纯展示节点设 Transparent，或把 onClick 挂在整个 Stack 容器上，不只挂在最底层图片。

## 可选检查

- 调整 Stack 对齐、上层几何或新增定位壳后，对被覆盖区域的按钮逐个实际点击（不只看节点 clickable 与 bounds），检查 hilog 有无 Touch test result is empty。
- 一次性动效层改动后，空闲态用 dumpLayout 确认该节点不存在，再实测点击、横滑与折叠。

来源支持：7 张卡 · 6 次迁移 · 6 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因〕安卓 FrameLayout 的子视图按栈绘制，最后加入（声明越晚）的在最上面
- 〔适用情境 / 做法第 5 步〕安卓 View.onTouchEvent 只有视图带 CLICKABLE、LONG_CLICKABLE、CONTEXT_CLICKABLE（或 TOOLTIP）标志时才消费触摸；没设 clickable 的容器、进度环、ProgressBar 不吞点击，事件继续派给下层视图
- 〔原因 / 做法第 1 步〕ArkUI 组件不写 hitTestBehavior 时为 HitTestMode.Default：自身和子节点都响应触摸命中，并阻塞被它遮住的其他节点；没有 onClick 的容器同样参与命中
- 〔做法第 1 步〕HitTestMode.Transparent：自身和子节点照常响应命中，同时允许被它遮住的其他节点参与命中；HitTestMode.None：自身不响应命中，子节点仍按各自的模式响应
- 〔做法第 1 步〕Stack 里多个节点的触摸区域重叠、最上层节点的子组件被命中时，默认只对最上层节点做触摸测试；只有最上层节点设了 HitTestMode.Transparent，下层节点才参与触摸测试
- 〔做法第 1 步〕HitTestMode.None、Transparent 只作用于写它的节点：外层容器写了 None，内部有尺寸的子节点仍按 Default 命中，照样挡住外层容器下方的兄弟控件
- 〔原因 / 做法第 3 步〕overlay 浮层覆盖在所绑定组件的上方，会阻塞用户对浮层下方组件的全部交互
- 〔原因 / 做法第 3 步〕遮罩用 overlay 挂在带 padding 的容器上时只覆盖内容盒，底部 padding 带不变暗
- 〔原因 / 做法第 4 步〕全屏自定义组件常驻挂载（100% 宽高、高 zIndex）时，即使内部 Canvas 设了 HitTestMode.None，下层页面仍点不动、滑不动
- 〔做法第 4 步〕自定义组件的 aboutToAppear 在新实例创建之后、build() 执行之前调用
- 〔做法第 2 步〕StackOptions.alignContent 不写时为 Alignment.Center，Stack 里所有子项共用这一个对齐方式
- 〔做法第 2 步〕position 设置组件相对父组件的绝对位置；API 12 起可传 Edges（top、left、bottom、right），按 bottom 边锚定
- 〔做法第 2 步〕zIndex 只决定同一容器内兄弟组件的显示层级，值大的在上
