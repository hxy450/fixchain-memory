# 源端点击触发的导航 effect，逐个落成目标 onClick 里的 router.pushUrl 带参跳转

审的是：代码
触发（任一种）：
- 读到：源 Fragment 里的点击（`setOnClickListener`、适配器的点击回调）调 ViewModel，ViewModel 发出的导航 effect 在 Fragment 里经 `navigate(R.id.…, bundleOf(…))` 跳到详情页或编辑页；写错的样子：目标里对应的卡片、列表项、空状态按钮没有 `.onClick`，或者整页没有 `router.pushUrl` 调用
- 读到：页面规格（`page_NNNN`）或 `ui-manifest` 写了这一页的导航出口：点击卡片或整项跳详情页、创建按钮跳编辑页；写错的样子：代码里找不到与每个导航出口对应的 `router.pushUrl` 调用
适用范围：源端用 Navigation Component 在 Fragment 间跳转，目标页面用 ArkUI 页面或 Tabs 内嵌组件、要自行完成跳转并传参时
做法：
- 从源 Fragment 处理导航 effect 的分支反查：每个 effect 跳到哪个 Fragment、bundleOf 里带什么参数、由哪个点击发出，列成「可交互元素→目标页+参数」清单，不只对齐看得见的元素
- 清单每项写成实际调用：import router from '@ohos.router'；.onClick(() => { router.pushUrl({ url: 'pages/<目标页>', params: { <bundle 的键>: <值> } }) })，不带参数的目标省掉 params
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function pushUrl(options: RouterOptions): Promise<void>：@ohos.router 的页面跳转；声明里标了 @deprecated since 18，推荐改用 UIContext.Router#pushUrl（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，router.pushUrl）
- RouterOptions.url: string；RouterOptions.params?: Object：url 是目标页路径（取自页面列表，如 pages/detail/detail）；params 是带给目标页的数据，对应源端 bundleOf 的键值（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，RouterOptions.url、RouterOptions.params）
- router.pushUrl({ url: 'pages/<目标页>', params: { <键>: <值> } }) 接到卡片、列表项和创建按钮的 onClick 后，跳转正常：验证过的接线写法（出处：卡里修好并验证过）
- pushUrl(options: router.RouterOptions): Promise<void>：同族接口：UIContext 的 Router 类的 pushUrl，参数同样是 RouterOptions（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，Router.pushUrl）
- function replaceUrl(options: RouterOptions): Promise<void>：同族接口：router.replaceUrl，替换当前页而不是压栈（出处：鸿蒙 SDK 的 ets/api/@ohos.router.d.ts，router.replaceUrl）
针对本应用要查的：
- 这一页有哪些导航出口、各带什么参数：源 Fragment 里处理 ViewModel 导航 effect 的分支（navigate 的目标和 bundleOf 的键）、适配器和按钮的点击回调；页面规格和 ui-manifest 的导航出口一栏；每个出口记下目标页和参数键，再对到目标页的组件和 router 调用
未核实：卡里的跳转验证在目标 API 24（兼容 22）上做，本机核对用的是 API 23 的声明
来源：1 张卡，1 个应用
- case-be539ffd7751410d8ad6（星途清单）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 诊断、建议 1；取值 3 ← 诊断
