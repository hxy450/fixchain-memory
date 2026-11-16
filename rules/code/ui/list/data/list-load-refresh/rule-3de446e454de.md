# 列表页 push 去表单、保存后 back 回来时，加载放进 onPageShow，不只放 aboutToAppear

审的是：代码
触发（任一种）：
- 读到：源端列表的新增、编辑都进独立的详情路由，返回后列表要显示变更（列表带下拉刷新 RefreshLayout）；写错的样子：列表页只在 aboutToAppear() 里调加载，新增或编辑页保存后 router.back() 返回，列表没有任何重载
适用范围：用 router 在 @Entry 列表页和新增、编辑页之间 push / back 往返，列表数据靠网络拉取时
做法：
- 在列表页写 onPageShow(): void { this.load() }，返回时重新拉取；首次加载显示 loading，返回刷新时不再显示整页 loading
- 或者用返回结果、事件触发重载，同样区分首次加载和返回刷新的 loading 状态
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onPageShow?(): void：页面每次显示（含路由返回、回到前台）都调用，只对 @Entry 装饰的组件生效（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onPageShow）
- aboutToAppear?(): void：只在组件新实例创建后、build() 前调用一次；router 返回时列表页不重建，它不会再执行（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.aboutToAppear）
- 加了 onPageShow 重载、非首次加载不显示 loading 后，新增地址返回列表即回显：只靠 aboutToAppear 时新增结果不显示（出处：卡里修好并验证过）
- onPageHide?(): void：同族接口：页面每次隐藏时调用，同样只对 @Entry 组件生效（出处：鸿蒙 SDK 的 ets/component/common.d.ts，BaseCustomComponent.onPageHide）
未核实：源端从详情页返回后列表靠什么触发重载，卡里没有读到源端代码
来源：1 张卡，1 个应用
- case-03947f1730e7f74c490f（青商城）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；取值 3 ← 诊断
