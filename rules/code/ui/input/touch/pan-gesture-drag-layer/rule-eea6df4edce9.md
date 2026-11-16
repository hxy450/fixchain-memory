# 修侧滑行按钮被内容层拦截时只改按钮热区，不把带收起手势的内容层设成 HitTestMode.None

审的是：代码
触发（任一种）：
- 读到：修复单要求展开后点操作按钮只触发按钮自身动作；页面代码里 Stack 下层是操作按钮，上层内容卡片靠 translate 平移露出按钮，并同时绑了 .onClick(未展开进详情、已展开收起) 和 .parallelGesture(PanGesture({ direction: PanDirection.Horizontal })).onActionEnd(...)；写错的样子：内容卡片上加了 .hitTestBehavior(展开 ? HitTestMode.None : HitTestMode.Block)，展开后整张卡片连同它上面的横滑和点击收起一起失去命中，右滑关不上
适用范围：界面缺陷修复阶段，解决可侧滑列表行展开后操作按钮点击被内容层拦截的命中冲突时
做法：
- 先列出内容层上已绑定的全部交互（点击收起、横向 PanGesture 展开/收起），把修复限定在按钮热区：提高按钮层级（按钮层 .zIndex(比内容层大)）或只让按钮区域优先命中；不把整张内容层设为 HitTestMode.None
- 确需在展开态禁用内容层命中时，先把横向 PanGesture 从内容卡片上移到整行的 Stack 容器上，保证展开后从内容区或操作区都能右滑收起
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 删掉内容层的动态 HitTestMode.None，把横向 PanGesture 上移到整行 Stack 后，展开后能右滑收起：修好的写法（出处：卡里修好并验证过）
- hitTestBehavior(value: HitTestMode): T：组件的触摸测试模式（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- HitTestMode.None = 3：自身不响应触摸测试，不阻塞子节点、兄弟节点和祖先节点：内容层自己绑的 onClick、parallelGesture 随之全部收不到事件（出处：ts-appendix-enums.md，HitTestMode；鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode）
- HitTestMode.Block = 1：自身响应触摸测试，阻塞子节点、兄弟节点和祖先节点：未展开时内容层的模式（出处：ts-appendix-enums.md，HitTestMode）
- Stack 中多个节点触摸区域重叠时，默认只对最上层的节点做触摸测试：按钮层要在上层（zIndex 更大）才能先命中（出处：ts-appendix-enums.md，HitTestMode）
- zIndex(value: number): T：调整同一容器内兄弟组件的层级（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.zIndex）
未核实：translate 平移后内容层的命中区域是否仍覆盖按钮，卡里没核实
来源：1 张卡，1 个应用
- case-677059269bdbd772e57e（记得日历）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断
