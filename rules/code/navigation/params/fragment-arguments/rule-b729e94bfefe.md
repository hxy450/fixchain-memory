# @Entry 页经 router 进入且有必填入参时，在 aboutToAppear 里 getParams 取参

审的是：代码
触发（任一种）：
- 读到：源 Fragment 用 requireArguments().getString(键) / navArgs() 取参，导航图目的地声明了 <argument>；写错的样子：目标页登记进 main_pages.json、加了 @Entry，入参却是默认 '' 的普通成员，没有 router.getParams() 或 NavPathStack 取参代码，aboutToAppear 里 if (this.参数) 才加载
- 写错的样子：发送端 router.pushUrl({ url, params: {…} }) 的键名和目标页 getParams() 读的键名不一致
适用范围：带入参的源端 Fragment 迁成 ArkTS 页面，且页面经 router.pushUrl 或 Navigation 进入时
做法：
- 参数成员写成 @State，在 aboutToAppear() 里读 router.getParams() 返回对象中的对应键，校验非空后再加载数据
- 走 Navigation 时从 NavPathStack 取参：pathStack.getParamByName(目的地名) 或 getParamByIndex(下标)
- 给页面补 @Entry 或登记 main_pages.json 时，对照源端每处 requireArguments / navArgs 的键，目标页要有对应取参代码，键名和发送端 params 一致
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getParams(): Object：取当前页面的 params；声明标 @deprecated since 18，@useinstead ohos.arkui.UIContext.Router#getParams（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，router.getParams）
- function pushUrl(options: RouterOptions): Promise<void>；RouterOptions 的 params?: Object：发送端把入参放进 RouterOptions.params，目标页 getParams() 读同名键（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，router.pushUrl、RouterOptions.params）
- getParamByName(name: string): Array<unknown>：NavPathStack 按目的地名取参，返回栈里同名目的地的全部参数（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getParamByName）
- getParamByIndex(index: number): unknown | undefined：NavPathStack 按下标（从 0 起）取参，不在栈里返回 undefined（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getParamByIndex）
- @State 参数成员 + aboutToAppear 里读 router.getParams() 后加载：改成这样后，经 router.pushUrl({ url, params }) 进入的页面能拿到入参并正常显示（出处：卡里修好并验证过）
未核实：卡里上机的目标 SDK 是 6.1.1(24)，本机核实用的是 API 23；Navigation 取参这一步卡里没有上机验证
来源：1 张卡，1 个应用
- case-b3ded04b6b14f7ce8c8b（星途清单）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；做法第 3 步 ← 建议 3；取值 5 ← 诊断
