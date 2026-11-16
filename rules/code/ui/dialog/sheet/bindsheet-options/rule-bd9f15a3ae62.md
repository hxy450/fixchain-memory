# 页面有多个独立底部弹窗时，每个 bindSheet 绑在不同节点上，不在同一组件上链式绑两次

审的是：代码
触发（任一种）：
- 读到：页面并列两个以上 @Composable 底部弹窗组件，各自用独立的 visible 参数和状态控制显隐；写错的样子：同一个组件上连续写 .bindSheet($$this.showA, this.sheetA()).bindSheet($$this.showB, this.sheetB())
适用范围：把安卓页面上多个相互独立的底部弹窗映射成 ArkUI bindSheet 时
做法：
- 每个显隐状态的 .bindSheet 挂在不同的组件节点上（如一个挂内容或底栏容器、一个挂根容器），或合并成一个 bindSheet、在 builder 里按类型切换内容
- 写完后搜 bindSheet( 逐个核对：每个弹层状态各有唯一生效的绑定，且绑定节点在触发按钮可点击时已经渲染
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 同一组件上后写的 bindSheet 覆盖先写的，先写的状态置 true 也不弹出；把其中一个移到另一个节点后两个都能弹出：卡里修好并复验的行为（出处：卡里修好并验证过）
- bindSheet(isShow: boolean, builder: CustomBuilder, options?: SheetOptions): T：给组件绑定半模态页面（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindSheet）
未核实：声明和文档都没写同一组件多次 bindSheet 时谁生效，按卡里观察写
来源：1 张卡，1 个应用
- case-c7c5aa055fe76d9864b6（青商城）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
