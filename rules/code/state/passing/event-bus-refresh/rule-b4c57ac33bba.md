# 源端用EventBus订阅事件刷新时，目标在aboutToAppear订阅、aboutToDisappear释放

审的是：代码
触发（任一种）：
- 读到：源 Fragment 里有 @Subscribe 标注的 onEventMainThread(…Event)（EventBus），如登录成功事件到达后重载账号和列表数据；或规格 AC 的源锚点写着这个回调；写错的样子：目标常驻 Tab 的子组件只在 aboutToAppear 里加载一次数据，没有订阅工程事件总线上对应的事件，aboutToDisappear 里也没有释放
适用范围：安卓 Fragment 通过 EventBus 订阅事件（尤其登录成功这类账号事件）来重载数据，迁成 ArkUI 常驻 Tab 的子组件（aboutToAppear 只执行一次）时
做法：
- 在组件的 aboutToAppear() 里订阅工程事件总线上对应的事件（登录类用工程已有的登录成功 topic），回调里重读登录态和这一页的数据；不要只在 aboutToAppear 里调一次加载
- 在 aboutToDisappear() 里释放这份订阅（取消订阅或销毁订阅 owner），订阅和释放成对写
- 源端每个 @Subscribe 回调各对应一处订阅；登录页成功后只 pop 返回时，刷新只能靠这份订阅
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aboutToAppear?(): void：自定义组件的新实例创建后、执行 build() 之前调用；实例不重建就不会再调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToAppear）
- aboutToDisappear?(): void：自定义组件析构销毁之前调用，释放订阅放在这里（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToDisappear；arkts-page-custom-components-lifecycle.md，自定义组件生命周期）
- 常驻 Tab 子组件的 aboutToAppear 只执行一次；登录页成功后只 pop 返回，不会再触发加载：只在 aboutToAppear 加载时，登录后页面停在未登录时的数据（出处：卡里修好并验证过）
- aboutToAppear 里启动订阅（登录成功事件），aboutToDisappear 里释放；事件到达即重读登录态和页面数据：修好后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 工程里已有的事件总线和账号事件 topic：目标工程里事件总线模块的 .ets/.ts 文件，按登录、账号类 topic 名和订阅、释放方法找；用它的订阅方法和配套的释放方法；发布端已在登录持久化后发布的，只补消费者
- 源端事件回调里重载的是哪些数据：源工程里规格 AC 源锚点指向的 Fragment 源文件，按 @Subscribe 和 onEventMainThread 找；回调体里调用的加载方法就是事件到达后要重读的数据
未核实：源端回调里具体重载哪些数据，卡里以 AC 描述为准，没读到回调方法体
来源：1 张卡，1 个应用
- case-46ac36102451125de693（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2、建议 1；做法第 2 步 ← 建议 2、诊断；做法第 3 步 ← 建议 1、诊断；取值 3 ← 诊断；取值 4 ← 诊断
