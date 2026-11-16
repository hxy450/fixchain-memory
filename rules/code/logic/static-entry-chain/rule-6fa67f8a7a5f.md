# 静态入口或全局状态单例要调需要 UI context 的服务时，在入口签名里显式注入 context 和回调

审的是：代码
触发（任一种）：
- 读到：目标服务方法需要 Context 参数（如用 new picker.DocumentViewPicker(context) 导出文件），源端是工具类静态方法直接起链；写错的样子：static 入口方法的签名里没有 context: Context、toast、结果回调参数，只能改状态；服务调用只写在组件按钮的 onClick 回调里（只有那里拿得到 context）
适用范围：目标把业务链放在静态方法或全局状态单例里，而服务依赖 UI context 时
做法：
- 入口签名显式加 context: Context、toast 和 onResult 回调，入口内直接调服务并收口；调用页传 this.getUIContext().getHostContext()、toast 和成功回调
- 或者由挂载着的组件监听入口发出的请求，在组件里拿 context 起链
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getUIContext(): UIContext：自定义组件取所属的 UIContext（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.getUIContext）
- getHostContext(): Context | undefined（@since 12）：从 UIContext 取 Ability 的 context，传给入口（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，UIContext.getHostContext）
- constructor(context: Context)（DocumentViewPicker，只支持 UIAbilityContext）：需要 context 的服务例子：文件导出的选择器（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，picker.DocumentViewPicker.constructor）
- 入口注入 context、toast 和 onResult，页面传 host context 和成功回调后，直调入口能完成整条链：卡里的修复写法（出处：卡里修好并验证过）
- constructor(context: Context)（AudioViewPicker，只支持 UIAbilityContext）：同族接口：音频选择器同样要 context（出处：鸿蒙 SDK 的 ets/api/@ohos.file.picker.d.ts，picker.AudioViewPicker.constructor）
未核实：卡里的工程 target 是 API 24，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-879046ceea442517d7ce（免费来电多多）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
