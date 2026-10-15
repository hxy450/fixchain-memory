# ui/interaction

点击命中与手势：Stack/弹窗覆盖层对下层点击的影响（含按钮上叠的进度环）、hitTestBehavior与防穿透、事件绑定和点击副作用、侧滑行的手势归属与滑删方向，以及事件触发时的坐标与锚点取值；含状态按钮的内容分支；源端监听回调被注释（死按钮）时的迁移与审计；根级硬件键盘快捷键与聚焦输入框的事件归属，Activity 级按键回调的挂载节点；源端只跟随首指的触控分支对 ArkUI 逐指派发的过滤。；带文字的勾选控件拆成勾选框加文字时的可点范围；Compose 点击修饰符默认按压指示的补齐，combinedClickable 长按自带的系统触感；点击时的按键音与振动，确认类点击的切态加可取消延时，GestureDetector 的 onFling 条件复刻

[上一级](../index.md)

## 本级经验

- [Activity 级 onKeyDown 映射到页面根节点的 onKeyEvent，并让页内至少一个组件可获焦，把焦点链带进本页](lesson-80e1d2c095a3698a7156.lesson.md)
  - 时机：页面实现与输入接线阶段，为源端 Activity 级硬件按键回调（onKeyDown、dispatchKeyEvent）选择 ArkUI onKeyEvent 的挂载节点时；接收“焦点获取归本任务”一类移交时
  - 情境：安卓源在 Activity 上覆写 onKeyDown 或 dispatchKeyEvent 处理方向键、MENU、Ctrl+Z 等，不依赖某个 View 持有焦点；目标页面是 Navigation 下的 NavDestination 或 @Entry 页，交互由内部 Canvas、自绘子组件或 Image + onClick 承载。也包括页内没有 Button/TextInput 或 focusable(true) 组件，源端按键控件是缺省可获焦的 ImageButton/Button。
  - 例外：源端在输入框获焦时放行部分按键（如判当前焦点为 EditText 才处理）：放行判据按根级快捷键放行输入框的规则处理，本条只决定挂载点与焦点链
- [Button 内按状态切换图标时写成一个 if/else 或单个 Image 按状态选资源，不写两个互斥的独立 if](lesson-ed5556325b6d8f510e2f.lesson.md)
  - 时机：界面实现阶段，为播放/暂停一类两态按钮编写 Button 的子内容时
  - 情境：源端按钮按状态切换图标，目标用 Button() { ... } 包裹图标，准备按两个状态分别写条件分支。
- [Compose combinedClickable 的长按自带系统触感：目标 LongPressGesture 不会振动，要在长按触发时显式调用一次长按触感](lesson-8a752faf9f5dff52e3ff.lesson.md)
  - 时机：界面实现阶段，把 Compose combinedClickable(onLongClick = …) 的长按交互转写为 ArkUI LongPressGesture 或长按事件时
  - 情境：源端条目用 combinedClickable(onLongClick = …) 处理长按，传 hapticFeedbackEnabled = true，或未传而所用 compose-foundation 版本签名中该参数默认为 true；长按回调里可能另有业务振动（如跳步时的重击感）；目标用 LongPressGesture 只回调业务逻辑。
  - 例外：源端显式写 hapticFeedbackEnabled = false；所用 compose-foundation 版本的 combinedClickable 签名里没有 hapticFeedbackEnabled 参数：不套用本条，先在该版本的长按实现里查有无系统触感调用再决定
- [Stack 中覆盖在可点击兄弟之上、自身不处理点击的层显式设 HitTestMode.Transparent，不假设它不参与命中](lesson-4a4f8d845a204ffa244b.lesson.md)
  - 时机：界面实现与巡检修复阶段，把 FrameLayout 或 Compose Box 叠放层转成 ArkUI Stack、确定各层 hitTestBehavior 时；为还原 z 序重排子节点，或调整 Stack 对齐与上层几何后
  - 情境：源 FrameLayout 中较晚声明、z 序更高的 match_parent 容器本身不可点击却覆盖下方按钮（Android 非 clickable 视图不消费触摸）；目标对应子层是 width/height('100%') 的容器。也包括按钮之上叠有同尺寸、不可点击的自绘进度环或加载圈（源端触摸落到下层按钮），目标 Stack 保留 z 序而点击只挂在最底层图片上。
  - 例外：上层本身绑定了点击或滑动手势（如侧滑行的内容层）：不改整层命中模式，把调整限定在按钮热区；源 Box 中按内容定高、贴底或贴顶的栏：保持自身尺寸直接锚定，不套全屏定位壳；页面级全屏遮罩与一次性全屏动效层：只在需要时作为根 Stack 条件子节点挂载
- [SwipeToDismissBox 的滑删方向按物理手势和 offset 符号写明，未覆写的触发阈值按源依赖版本的库默认值落实](lesson-7f5eba1b969bddfb34dc.lesson.md)
  - 时机：规格提取与界面实现阶段，转写 Material3 SwipeToDismissBox 的滑删方向与触发阈值、在列表行内自定义滑删手势时
  - 情境：源端用 enableDismissFromStartToEnd、EndToStart 等枚举描述方向，背景对齐方向与之配合；rememberSwipeToDismissBoxState 未传 positionalThreshold，触发条件来自 material3 库默认、不在源文件里；目标在列表行内用 Stack + PanGesture 一类写法自定义滑删。
- [修可侧滑行的按钮点击被内容层拦截时，把调整限定在按钮热区，不把承载滑动手势的整张内容层设为 HitTestMode.None](lesson-6677d286e690407d4af4.lesson.md)
  - 时机：界面缺陷修复阶段，为可侧滑列表行解决展开后操作按钮点击被上层内容拦截的命中冲突时
  - 情境：列表行用 Stack 叠放底层操作按钮与上层内容卡片，卡片以 translate 平移露出按钮，并在同一节点上绑定点击（未展开进详情、已展开则收起）与横向 PanGesture（展开或收起）。
  - 例外：覆盖层本身不处理任何点击或手势、只是遮住按钮：按非交互覆盖层设 Transparent
- [弹窗防穿透的 Block 只放在无子控件的遮罩层，内容面板与根容器保持 Default；改真弹窗 API 后删掉自绘防穿透](lesson-cf018b76af68b4c00895.lesson.md)
  - 时机：弹窗或浮层实现与改造阶段，为遮罩、内容面板、根容器设置 hitTestBehavior，或把页面内浮层迁到 showCustomDialog/showBindSheet、openCustomDialog 等真弹窗时
  - 情境：弹窗或底部面板采用“根 Stack + 遮罩 + 内容面板”结构，在根或内容面板上写 hitTestBehavior(HitTestMode.Block)（含 visible ? Block : None）防止点击穿透；面板内有按钮、checkbox、列表项等要响应点击的子控件。也包括源端用全屏空 clickable 拦截层防穿透、遮罩点击关闭、居中卡片阻止冒泡，目标在包住遮罩、卡片、滑杆与滚动区的弹层根 Stack 上写 Block。
  - 例外：上层是不处理点击、只需放行下层的展示层：用 Transparent，不属本条
- [接入已有专页时逐项兑现它的 @Event 回调契约：要求回传会话或结果的回调给出真实值或交父页分派，不用空值短路专页自带的导航](lesson-c061106fa1d809e518da.lesson.md)
  - 时机：界面实现阶段，把源端编辑项 Fragment 对应的现有 ArkTS 专页接入容器、实现专页回调时
  - 情境：源端工厂按 type 把同类数据分到不同 Fragment（如编辑页与选择页）；目标已有专页，经 @Event 要求父层回传会话或结果（回调参数里带 onReady 一类回调）再由专页自行导航，父容器里已有一个可复用的通用入口。
- [根级键盘快捷键不假定聚焦的输入框会吞掉全部按键事件](lesson-a10cde3d336eee4eebe7.lesson.md)
  - 时机：实现根级硬件键盘快捷键（媒体控制、导航），并要求输入框聚焦时放行时
  - 情境：源 onKeyUp 在当前焦点为 EditText 时放行；目标在入口页根组件 onKeyEvent 统一处理按键。
- [源端 onTouch 交给 GestureDetector 时，按其容差、长按、双击与抛掷速度条件复刻 onFling，不改成位移阈值状态机](lesson-2805bfc40262f9aa8d94.lesson.md)
  - 时机：输入控制的规格提取与实现阶段，把交给 GestureDetector 的滑动、抛掷手势映射为 ArkUI onTouch 或手势识别器时
  - 情境：源端 OnTouchListener 只 return gestureDetector.onTouchEvent(event)（new GestureDetector、extends SimpleOnGestureListener），方向判定写在 onFling/onScroll 里；目标准备在手势区域用 .onTouch 手写 Down/Move/Up 状态机，或用 PanGesture、SwipeGesture 等识别器替代。
  - 例外：源端 onTouch 自己按 getAction 分支、不经 GestureDetector：按原始动作桥接的首指过滤处理
- [源端 onTouch 自己按未掩码 getAction 只跟随首指时，先看手指由谁接收，再过滤 ArkUI 的逐指 Down/Up](lesson-68023ac5f088c72a775a.lesson.md)
  - 时机：输入控制的规格提取与实现阶段，把 Android onTouch 的 MotionEvent 动作分支和坐标读取映射为 ArkUI onTouch 的 TouchType 分支与触点来源时
  - 情境：源端 OnTouchListener 用未掩码的 event.getAction() 只匹配 ACTION_DOWN/MOVE/UP，以无索引的 getX()/getY()（指针索引 0）读坐标，附加手指的 POINTER_DOWN/UP 不进入任何分支；目标 ArkUI .onTouch 对每根手指都派发 TouchType.Down/Up，TouchEvent 同时提供 touches（含本次抬起手指在内的全部触点）与 changedTouches（本次变化的触点）。也包括源端多个兄弟控件（方向键、旋转键等）各自 setOnTouchListener，targetSdk≥11 且未设 splitMotionEvents=false，窗口默认分指，每个控件只收落在自己身上的指针流；目标每个按钮各挂 .onTouch，而 TouchEvent.touches 列出屏幕上全部手指。
  - 例外：源端用 getActionMasked() 处理 POINTER_DOWN/UP，或按 pointerId 跟踪多指时，按源端的多指语义逐指映射；源端 onTouch 只把事件交给 GestureDetector（new GestureDetector、extends SimpleOnGestureListener、return gestureDetector.onTouchEvent(event)）：按 GestureDetector 的触发条件复刻，不套用本条的计数过滤
- [源端可点击容器自带的按压反馈在 ArkUI onClick 容器上不会自动出现：用 stateStyles 的 pressed 态补状态层](lesson-fde79829831c2269e925.lesson.md)
  - 时机：界面实现阶段，把带 Modifier.clickable/toggleable/selectable，或 Card、Surface(onClick) 的 Compose 容器转成挂 onClick 的 ArkUI 容器时；把 ListView、PreferenceActivity 中由主题 listSelector 提供按压态的可点击行转成 ArkUI 列表行时
  - 情境：源端容器经 clickable/toggleable（可带 role = Button、Switch）或 Card/Surface(onClick) 响应点击，没有把 indication 设为 null，按压时由主题提供涟漪或状态层；目标用 Column/Row/Stack 加 .onClick 实现，ArkUI 通用容器默认没有按压反馈（Button 自带的按压效果除外）。 也包括 View 体系的 ListView、PreferenceActivity 行没有把 background 或 listSelector 设为 null，按压态由主题选择器（如 Holo 暗色 list_selector_holo_dark）提供；写者在 d.ts 里找不到通用容器的 stateEffect，就放弃了按压态。
  - 例外：源端显式 indication = null 或自定义 indication 时，按源端写法处理；目标用自带按压效果的 Button 承载点击时，不再叠加
- [源端在触发瞬间读取锚点窗口位置时，目标在点击回调里即时取坐标，onAreaChange 缓存只作兜底；锚点取源端传入的同一元素](lesson-963bf871aa4e910a8fc8.lesson.md)
  - 时机：界面实现与修复阶段，为从点击处发出的动效或气泡（完成彩纸、锚点提示）确定起点坐标与锚点元素时
  - 情境：源端在动效或弹窗被调用时用 getLocationInWindow 读取传入锚点 View 的当下窗口中心；目标列表项存在 translate 平移、LazyForEach/Repeat 节点复用或弹层内滚动，写者准备用 onAreaChange 缓存控件位置。
- [源端监听回调体或 Adapter 数据绑定被注释时按未启用行为迁移；审计不因“已裁定/集成点”注释放行与源端运行态相背的接线](lesson-f3e614f295aa409485fd.lesson.md)
  - 时机：界面实现阶段，转换带点击监听的控件或 item 布局中由 Adapter 绑定的自定义绘制 View 时；1:1 对齐审计与修复阶段，判定目标端交互接线或数据绑定是否与安卓运行态一致，或重写组件时决定是否保留随行的 onClick 时
  - 情境：安卓控件注册了 setOnClickListener，但回调体被整段注释（如选图调用被注释），XML 也可能写着 clickable；或 Adapter 对自定义绘制 View（曲线、进度、图表）的数据绑定整段被注释，只剩 XML 静态属性，ViewModel 仍计算着可能用于绑定的值。目标端按规格集成点把它接成可用功能，或据注释代码、ViewModel 中间值重建动态效果；代码注释可能自述源码为死码并写着“裁定/集成点”；项目要求 1:1 忠实复刻（含源码缺陷）。
  - 例外：项目决策明确要求启用该功能，且用户已知并接受与源端不同
- [源端确认类点击先切选中态播放动画再 postDelayed 回调时，按“切态 → 可取消延时 → 回调”实现，不直接跳转](lesson-7c4e24f2b4128502595b.lesson.md)
  - 时机：界面实现或 1:1 还原阶段，迁移同意、确认一类点击的反馈与回调时序时
  - 情境：源端点击处理先 setChecked(true, true) 等方式切到选中态并播放勾选动画，再经 Handler/View 的 postDelayed 延时后回调并关闭弹窗；处理逻辑可能在 DialogHelper 一类辅助类里；目标在页面内自建弹窗，用 onClick 直接调用同意逻辑。
  - 例外：源码中直接回调、不延时的分支（如二次确认弹窗的同意）：保持不延时
- [源端禁用态只靠代码换背景、文字色固定时，不用 .enabled(false) 整体降透明：显式切换背景与投影，在各激活路径内判态拦截](lesson-99080bd3bfc1bcbb9c5f.lesson.md)
  - 时机：规格提取阶段为 setEnabled/android:enabled 切换的控件写转换决策时；界面实现阶段落实控件禁用态外观与点击拦截时
  - 情境：源端在 setEnabled(false) 的同时 setBackgroundResource 换成没有 state_enabled 分支的灰色 drawable，textColor 是固定颜色而非 ColorStateList（AppCompat 按钮禁用时投影另归零）；映射参考把 setEnabled(false)/android:enabled 一律对到 .enabled(false)。
  - 例外：源端禁用外观本身来自 state_enabled 选择器或半透明（如 ColorStateList 的 disabled 项）时，按源端色值显式写出；目标默认禁用透明度恰与源值一致时才直接用 .enabled()
- [点击处理器里的按键音与振动迁移时，复制源音频并按源音频用途选 StreamUsage，加载完成后再播，振动声明权限](lesson-3fd89449423aa8b63769.lesson.md)
  - 时机：界面迁移阶段，实现按键音、点击振动这类点击副作用时
  - 情境：源端点击处理器经 SoundPool、MediaPlayer 或封装的播放工具播放 assets、res/raw 中的音效，经 Vibrator 振动，开关常由偏好控制；目标需要等价的播放与振动。
  - 例外：振动来自框架自带触感（如 Compose combinedClickable 的长按），不在处理器代码里：按长按触感的规则补调用
- [点击挂在源端真正持有点击的节点上；带文字的 CheckBox/RadioButton 拆成勾选控件加 Text 时整体可点、命中区按源宽度](lesson-fd3add7128663eb9998f.lesson.md)
  - 时机：界面实现与返修阶段，为由多个子控件拼成的搜索栏、入口条或设置行决定 onClick 挂在哪一层，或清理、重写其中的点击绑定时；把带文字的 CheckBox/RadioButton 拆成 ArkUI 勾选控件加 Text 时
  - 情境：源布局只在整条容器上绑定点击（如 LinearLayout 的 onClick 或 DataBinding 点击），内部图标、提示文字、“搜索”字样只负责展示；目标用 Row + Image + Text 模拟占位搜索框（不是 TextInput），点击后压栈进入目标页。也包括源端 Java 只对行内某个子 View（如右侧值文本）setOnClickListener，同页其他行绑定整行 layout；目标用 Row 承载这些设置行。也包括带文字的 CheckBox/RadioButton（XML 声明或代码动态创建，宽度来自 wrap_content、match_parent、alignParentLeft 加 toLeftOf 两端锚定或父容器默认 LayoutParams），目标 Checkbox/Radio 不带文字、需另配 Text；为折行给 Text 加 layoutWeight(1) 时连同点击挂在整行上。
- [迁移带点击绑定的控件时，按源点击处理器与 ViewModel 的分支逐项迁移副作用和状态转换，不只做状态取反和换图](lesson-55e33a0621c3008ab8b3.lesson.md)
  - 时机：界面迁移阶段，为布局中带 onClick 绑定、状态选图或滑动面板的控件编写 ArkUI 事件与状态逻辑时；还原由页面弹层触发的选择与写操作时
  - 情境：源布局控件用 android:onClick、数据绑定或 setOnClickListener 声明点击，或按 ViewModel 状态选图；实际行为（按键音、振动、偏好持久化、面板展开与回填、存储写入）写在 Fragment/Activity 的统一点击处理器（when (v.id) 分支）、ViewModel 或共享弹层组件中。也包括 ViewModel 里同项再点取消、前置为空即失败、同键累加写入等状态转换由页面弹层触发。
