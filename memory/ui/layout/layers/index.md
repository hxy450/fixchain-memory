# ui/layout/layers

运行时addView、全屏底层、状态覆盖层与 BottomSheetBehavior 管理的布局内面板：确定视图挂在哪里、如何叠放及几何范围；点击命中与事件时坐标属于ui/interaction。；Box 中贴底栏在 Stack 中的锚定，页面级全屏遮罩与一次性动效层的条件挂载。

[上一级](../index.md)

## 本级经验

- [BottomSheetBehavior 面板映射：容器可见性与面板状态分离，位于底栏之上的面板用布局内实现](lesson-9f45b5d79206b5654aff.lesson.md)
  - 时机：界面实现与规格提取阶段，把由 BottomSheetBehavior 管理、初始收起的播放器等面板翻译为 ArkUI 壳布局与状态机时
  - 情境：源面板由 BottomSheetBehavior（app:layout_behavior、behavior_peekHeight）管理，位于 CoordinatorLayout 内、底部导航之上；app:behavior_hideable 未设或为 false，且代码未调用 setHideable(true)；可见性方法只切换容器 VISIBLE/GONE；目标可选窗口级 bindSheet 或 Stack 加 translate。
  - 例外：behavior_hideable=true 或代码调用 setHideable(true) 时，面板可进入 STATE_HIDDEN，按源端的 HIDDEN 状态及其出口实现
- [为已转换页面接线时保留“全屏底层 + 按状态切换的前景层”骨架；底层 SDK 不可用也不把全屏承载改成固定高度卡片](lesson-4de4283ec625be7e976c.lesson.md)
  - 时机：功能接线任务面对页面转换阶段已写出的页面、决定保留还是重写布局骨架时；巡检修复处理“缺少全屏底层承载”一类发现时
  - 情境：Android 页面以全屏 MapView/导航视图等为底层，前景由 ViewModel 布尔状态切换两套覆盖层；导航类页面可能 FEATURE_NO_TITLE、只承载底层视图；目标端对应 SDK 暂不可用，页面转换阶段已写出带全屏占位底图与两态覆盖层的骨架。
  - 例外：已转换页面的骨架经核对与源布局不符时，按源布局修正骨架，不保留错误结构
- [同一源控件既有只构造不绘制的底层实例、又有经绘制方法刷新的活动实例时，共享组件要能表达构造态：按层分别写可见状态，不把绘制方法里的隐藏分支无条件化](lesson-1e279118c32645022ac2.lesson.md)
  - 时机：规格提取与共享组件实现阶段，为棋盘、网格等分层控件定义组件状态参数，以及页面给各层传参时
  - 情境：源端自定义 View 构造时就设好背景与底色、保持 VISIBLE；页面为背景层逐格 new 实例并 addView，但只对活动层调用 drawItem 一类方法，该方法才在空值时 setVisibility(INVISIBLE)（背景层的 setVisibility 可能被注释掉）；目标把两层交给同一共享组件、按数值决定可见性。
- [在预览底部新增可选背景层时，逐层处理压在它上面的不透明内容：已选背景时上层透明或与背景合成，做不到就登记该分支的限制](lesson-cba11443f9a59fdaf4f7.lesson.md)
  - 时机：组件详情或编辑页的界面实现阶段，给预览区接入用户可选的背景，并确定它与现有预览内容的叠放顺序时
  - 情境：目标预览由静态网络预览图（Image + Contain）或铺满的白色占位层展示组件；源端选中背景后把它设为组件自身的背景 Drawable 并重绘；目标另建一个独立背景层，放在现有预览内容之下。
- [源 Box 中按内容定高、align(BottomCenter) 贴底的栏，在 Stack 中保持自身尺寸直接锚到底部，不套全屏壳](lesson-29fc0f8f62759fb1b254.lesson.md)
  - 时机：界面实现与巡检修复阶段，把 Compose Box 或 FrameLayout 中叠放的顶栏、底栏迁到 ArkUI Stack，确定它们的定位方式时
  - 情境：源页面在同一 Box(fillMaxSize) 里叠放可滚动内容、返回按钮等可点击覆盖控件，以及以 Modifier.align(Alignment.BottomCenter) 定位、按内容定高的底栏（顶栏同理只占自身高度）；目标 Stack 的 alignContent 改为 TopStart 等之后需另找贴底方式；项目映射参考可能注明 .align() 不能定位 Stack 子项。
  - 例外：栏在源端本身就是 match_parent 的全屏层：按全屏层的命中规则处理
- [运行时 addView 挂到根部的播放器面等按运行时层级实现：尺寸取 LayoutParams 或根容器默认参数，不按 XML 占位定几何](lesson-c3dcc5a25a0ad59c53c1.lesson.md)
  - 时机：界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时
  - 情境：源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0)），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。
- [页面级全屏遮罩与一次性全屏动效层只在需要时作为条件子节点挂载，不常驻、不用 .overlay() 条件 builder](lesson-b11aa934976f6da6b4bd.lesson.md)
  - 时机：界面实现阶段，为页面加保存中、引导等全屏遮罩，或实现彩纸等一次性全屏动效的覆盖层时
  - 情境：页面要在带安全区 padding 的根容器上加全屏遮罩；或源端在触发瞬间向窗口根视图（rootView/decorView）添加全屏、不可点击的动效层并在播完后移除，目标准备改成常驻挂载、带 zIndex 的全屏自定义组件，只给内部 Canvas 设 HitTestMode.None。同仓可能已有用根 Stack 条件子节点实现的同类遮罩。
