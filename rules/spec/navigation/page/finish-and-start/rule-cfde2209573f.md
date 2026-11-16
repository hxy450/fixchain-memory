# 多个安卓导航调用映射到单一 NavPathStack 时，规格写操作前后的栈和兜底，不用 clear() 回主页

审的是：规格
触发（任一种）：
- 读到：源端成功后 startActivity(主页) 配 FLAG_ACTIVITY_NEW_TASK，同时 finish() 当前页；目标的 Navigation 根内容是启动页；写错的样子：规格的映射表写「NEW_TASK → navPathStack.clear() + pushPathByName(主页)」，没写合并后「操作前栈 → 操作后栈」的净效果，也没写主页不在栈中时怎么办
适用范围：规格把安卓的多个导航调用映射到目标单一 NavPathStack 时（replacePathByName 声明 @since 12）
做法：
- 写出合并后的净效果，例如「[主页, 登录页] → [主页]」
- 写清目标做法和兜底：先 popToName(主页名)，返回 -1（主页不在栈中）时 replacePathByName(主页名, param)；Navigation 根内容是启动页时不用 clear() 表达回主页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- popToName(name: string, animated?: boolean): number：出栈到指定名字的页面；在栈中返回它的下标，不在返回 -1（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.popToName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：把当前栈顶替换为指定页面，当前页被销毁；param 必填（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
- clear(animated?: boolean): void：清空整个页面栈；根内容是启动页时清空后露出的是启动页（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.clear）
- 统一走一处导航：先 popToName(主页)，找不到时 replacePathByName(主页)：修好的写法（出处：卡里修好并验证过）
未核实：卡的目标 SDK 是 HarmonyOS 6.1.1(24)，本机声明是 API 23
来源：1 张卡，1 个应用
- case-8f54242f5eefd1e7e647（免费来电多多）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 4 ← 诊断
