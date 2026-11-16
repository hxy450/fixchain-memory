# 弹层根容器含可交互子节点时，不设 HitTestMode.Block，保持 Default

审的是：代码
触发（任一种）：
- 读到：源端模态浮层由全屏 `Modifier.fillMaxSize()` 加空 `clickable {}` 的拦截层（防穿透）、半透明遮罩 `clickable` 关闭、居中卡片三层组成；写错的样子：目标弹层根 `Stack` 上写了 .hitTestBehavior(HitTestMode.Block)，而它的子树里有 onClick、Scroll、Slider、Button 等交互控件
适用范围：用 ArkUI Stack 叠层还原全屏弹层、覆盖层，且根容器下有按钮、标签、滑杆、滚动等可交互子节点时
做法：
- 弹层根 Stack 不写 .hitTestBehavior(HitTestMode.Block)，保持 HitTestMode.Default（默认值，已会挡住被它遮住的下层兄弟）；防穿透交给源端那层全屏拦截层
- Block 只放在没有交互子节点的叶子层（如纯遮罩）；已写的 hitTestBehavior(HitTestMode.Block) 逐个看命中节点的子树，有交互控件就改成 Default，或把 Block 下移到叶子层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- HitTestMode.Block：自身响应命中测试，但挡住子节点和被它遮住的其他节点：挂在根容器上会让里面所有按钮、滑杆、滚动都收不到触摸（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Block）
- HitTestMode.Default：自身和子节点都响应命中测试，挡住被它遮住的其他节点：弹层根容器用它就能防穿透到下层，子节点照常可点（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，HitTestMode.Default）
- hitTestBehavior(value: HitTestMode): T，默认 HitTestMode.Default：设置组件的命中测试模式；不写就是 Default（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.hitTestBehavior）
- 根 Stack 从 Block 改成 Default 后，排序、标签、滑杆、关闭、遮罩与滚动在机上恢复：改法已上机验证（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-30d42aa2ba7c8354db17（Jetsnack）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、建议 3；取值 4 ← 诊断
