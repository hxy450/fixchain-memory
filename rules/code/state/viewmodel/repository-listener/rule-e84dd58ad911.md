# 页面向单例仓库 addListener 时，回调存成字段并在 aboutToDisappear 里移除，不传内联箭头函数

审的是：代码
触发（任一种）：
- 读到：源端页面用 observeAsState() / collectAsState() / DisposableEffect 观察数据，观察随组合退出自动结束；目标数据层是单例，提供 addListener / removeListener（按回调引用移除）；写错的样子：页面 aboutToAppear 里写 services.preferences.addListener(snapshot => {...}) 内联回调、不存字段；页面没有 aboutToDisappear，或 aboutToDisappear 里没有对应的 removeListener
适用范围：把源端随界面生命周期自动结束的观察翻成对应用级单例的手动订阅时，页面组件的注册和释放
做法：
- 每写一次 addListener / on / subscribe，同一次补丁里把回调存成字段（private onChange = (v: <类型>) => {...}）或保存返回的句柄；aboutToDisappear 里 removeListener(this.onChange) 或 handle.remove()
- 逐页列出注册点，和 aboutToDisappear 的释放清单一一对照；同页已为某个监听写了释放，其余监听也逐个补齐
- 交付前 grep：addListener( 后直接跟箭头函数的调用，以及有 addListener 却没有 aboutToDisappear / removeListener 的页面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- aboutToDisappear?(): void，组件即将消失时调用；里面不要改状态变量：释放监听的位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomComponent.aboutToDisappear）
- 修好后回调存为字段，在 aboutToDisappear 调原有的 removeListener；数据库监听保存返回的句柄并调 remove()：修好后的做法（出处：卡里修好并验证过）
- off(type: 'change', callback?: Callback<string>): void：同族接口：Preferences 的变化订阅同样按回调注销，不传 callback 时注销全部（出处：鸿蒙 SDK 的 ets/api/@ohos.data.preferences.d.ts，Preferences.off）
- function off(eventId: string, callback: Callback<EventData>): void：同族接口：emitter 按回调注销，只对通过 on / once 注册过的那个回调生效（出处：鸿蒙 SDK 的 ets/api/@ohos.events.emitter.d.ts，emitter.off）
未核实：卡里的行为在 target SDK 6.0.1(21) 下观察，本机核实用的声明是 API 23
来源：1 张卡，1 个应用
- case-054901ca662ae6c66988（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 2 ← 诊断
