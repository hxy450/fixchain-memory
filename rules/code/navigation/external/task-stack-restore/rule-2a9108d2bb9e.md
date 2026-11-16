# TaskStackBuilder 父栈跳转，代码写成 clear 后按父链依次 pushPathByName

审的是：代码
触发（任一种）：
- 读到：源码 TaskStackBuilder.create(this).addNextIntentWithParentStack(intent).startActivities()，Manifest 有 android:parentActivityName；或规格把它映射成单次 pushPathByName；写错的样子：目标只写 navPathStack.pushPathByName(name, param, false)，注释写「带父栈入栈」「返回落回来源页」
适用范围：目标端用单个 Navigation + NavPathStack，父栈跳转可能从栈底以外的任意宿主页发起时
做法：
- 写成 navPathStack.clear(false) → 按父链依次 navPathStack.pushPathByName(<父页>, <参数>, false) → navPathStack.pushPathByName(<目标>, <参数>, false)
- 规格映射成单次 push 时对照源码与 Manifest 核对返回落点，冲突就按源端语义实现并标注差异；自检：非根页 → 抽屉 → 目标 → 返回应先回父页，再返回才退到后台
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- clear(animated?: boolean): void，animated 默认 true：清空导航栈；重建时传 false 不播转场（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.clear）
- pushPathByName(name: string, param: unknown, animated?: boolean): void，animated 默认 true：按名字压入 NavDestination（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- 修好后改为 clear(false) → push 父页 → push 目标（均 animated=false），设备上返回落到父页：修好后的做法（出处：卡里修好并验证过）
- 栈底那个 Intent 加 FLAG_ACTIVITY_NEW_TASK | FLAG_ACTIVITY_CLEAR_TASK | FLAG_ACTIVITY_TASK_ON_HOME：源端会清掉当前任务（出处：android.app.TaskStackBuilder#getIntents）
- pushPath(info: NavPathInfo, animated?: boolean): void：同族接口：按 NavPathInfo 压栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPath）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：替换栈顶（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
针对本应用要查的：
- 父链上的每个页面在目标端是不是 NavDestination：目标工程里 Navigation 所在页面和路由表（route_map 或 navDestination 注册处）；父页若注册为 NavDestination 就要 push；若是 Navigation 的根内容（不在 NavPathStack 里），clear 后直接 push 目标
来源：1 张卡，1 个应用
- case-ece3192169e927e18aa5（Privacy Friendly 2048）：做法第 1 步 ← 诊断、建议 1；做法第 2 步 ← 建议 3；取值 3 ← 诊断
