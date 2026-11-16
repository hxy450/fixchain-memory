# 注入点在子组件内部创建的 VM 上时，子组件加回调参数把 VM 交给页面

审的是：代码
触发（任一种）：
- 读到：占位登记要求页面给覆盖层的 ViewModel 注入数据源（捕获结果读面、振幅源），而 VM 由子组件在内部 new 出来；写错的样子：页面只写 Overlay({ engine }) 这类构造，子组件 aboutToAppear 里只登记别的 sink，没有把内部 VM 交出去的回调，页面够不着注入点
适用范围：页面需要给子组件内部创建的 ViewModel 注入数据源时
做法：
- 子组件加回调参数 onViewModelReady?: (model: VM | null) => void：内部 VM 建好后调用 onViewModelReady(vm)，销毁时调用 onViewModelReady(null)；页面在回调里给 VM 注入数据源
- 补一条单测：注入后对应读数（ISO、振幅等）非空
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 子组件新增 onViewModelReady(model | null)，页面经它注入捕获结果和振幅源后读数显示：修好后的交接通道（出处：卡里修好并验证过）
- aboutToAppear?(): void；aboutToDisappear?(): void：子组件里建 VM 和交还 null 的时机（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToAppear、BaseCustomComponent.aboutToDisappear）
来源：1 张卡，1 个应用
- case-775c2298a494ebceb71c（opencamera-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
