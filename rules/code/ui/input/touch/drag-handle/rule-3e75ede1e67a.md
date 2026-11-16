# 用 OverlayManager 挂窗口级图层时只在需要的时段挂载，常驻就用帧节点根并切换命中

审的是：代码
触发（任一种）：
- 读到：源码在 ACTION_DOWN 里 startDrag(..., new View.DragShadowBuilder(v), ...)，拖拽阴影只在拖拽期间存在；写错的样子：aboutToAppear 里 getOverlayManager().addComponentContent(content) 挂一个常驻图层，根是自定义组件、内层 Stack 写 HitTestMode.None，整页不响应触摸
适用范围：用 OverlayManager 和 ComponentContent 实现拖拽阴影、浮层、弹层等窗口级图层时
做法：
- 只在需要显示的时段挂载：出现时 addComponentContent(content)，消失时 removeComponentContent(content)（如按阴影显隐监听挂载和摘除）
- 必须常驻时，根用帧节点（Stack）并按交互态切换 .hitTestBehavior；内层自定义组件上的 None 管不到外面那层代理节点
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- addComponentContent(content: ComponentContent, index?: number): void；removeComponentContent(content: ComponentContent): void：OverlayManager 挂载和摘除图层（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，OverlayManager.addComponentContent、OverlayManager.removeComponentContent）
- 自定义组件作 ComponentContent 根时被包进缺省命中的代理节点（BuilderProxyNode），内层 None 无效；改为随阴影显隐挂载 / 摘除、常驻浮层根改帧节点并随交互态切换命中后恢复：问题的来源和修复（出处：卡里修好并验证过）
未核实：代理节点（BuilderProxyNode）的命中行为是卡里上机观察，本机声明里没查到说明
来源：1 张卡，1 个应用
- case-d38fbc2e9b64b7c3338b（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
