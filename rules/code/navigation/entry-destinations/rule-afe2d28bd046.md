# 源端入口 startActivity 到二级页，目标写 pushPathByName 并注册路由，不用 Toast

审的是：代码
触发（任一种）：
- 读到：源端点击监听里 startActivity(Intent(...)) 到另一个 Activity；写错的样子：目标端对应入口的点击回调里只有 promptAction.showToast(...) 提示「本轮暂不可用」，或没有响应，或交给统一的 FWD-REF 占位回调；Navigation 的 navDestination 构建函数里没有目标页
适用范围：截图页入口直达的二级页已列入本轮范围、迁成 ArkUI Navigation 页面时
不适用的情形：用户明确说只做这几页时可以不实现入口，但要按下一条在交付总结里逐项列出
做法：
- 点击回调写成 this.pathStack.pushPathByName('<目标页名>', param)，替换 Toast 或占位回调
- 在 Navigation(...).navDestination(builder) 的构建函数里给这个页名加分支并建出目标页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 按页名入栈，animated 默认 true（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- navDestination(builder: (name: string, param: unknown) => void): NavigationAttribute：按页名建出目标页的构建函数，没有分支的页名 push 后不会显示（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavigationAttribute.navDestination）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：按页名入栈并返回 Promise（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：按页名替换栈顶（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
- Toast 改成 pushPathByName、主入口注册新路由后二级跳转闭环：改法的依据（出处：卡里修好并验证过）
针对本应用要查的：
- 每个入口对应的目标页：源工程截图页 Activity/Fragment 里点击监听的 startActivity(Intent(...))；目标工程主入口里 navDestination 构建函数的分支；每个 Intent 目标对应一个目标页名，push 的页名和 navDestination 的分支要一一对上
来源：1 张卡，1 个应用
- case-ae269ba9b3d5c8def239（骑行记录）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；例外 1 ← 建议 1、建议 3；取值 5 ← 诊断
