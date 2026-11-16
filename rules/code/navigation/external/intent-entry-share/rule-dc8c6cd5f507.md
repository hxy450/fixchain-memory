# 源端跳转前判断目标能否启动时，目标守卫查注册名或 pageName 非空，不查导航栈成员

审的是：代码
触发（任一种）：
- 读到：源端跳转前对构造出的目标 Intent 做 isIntentAvailable 一类判断（能否被解析启动），热启分支直接 startActivity 目标页；写错的样子：宿主导航执行器的守卫写成 navPathStack.getAllPathName().indexOf(pageName) < 0 → return false
适用范围：外部入口（桌面快捷方式、本地通知、推送深链）经宿主 Navigation 冷启暂存、热启直跳分发到目标页时的守卫
做法：
- 守卫改查目标是否已注册或路由命中：pageName 在 pageMap 注册名集合里，或只在 pageName === '' 时拒绝
- 不用 getAllPathName() 一类栈成员检查；写完按冷启（栈里只有启动页）和热启（栈里只有主页）各推演一次，确认首跳目标能 pushPathByName 入栈
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getAllPathName(): Array<string>：NavPathStack 上返回当前栈里所有页名，查的是栈成员，不是注册表；冷启首跳和热启直跳的目标本来不在栈里（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getAllPathName）
- getIndexByName(name: string): Array<number>：同族接口：NavPathStack 上按名字查栈内下标，同样只查栈内（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getIndexByName）
- getParamByName(name: string): Array<unknown>：同族接口：NavPathStack 上按名字取栈内页的参数，同样只查栈内（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.getParamByName）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：守卫放行后按页名入栈（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- 守卫改为 pageName === '' 才拒绝后，冷启暂存和热启直跳的目标页都能入栈：修复后的守卫语义（出处：卡里修好并验证过）
未核实：卡里的行为出自目标 SDK 6.1.1(24) / 6.0.1(21)，声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-c699af1f5c3b03105480（DeepAI全能PPT）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 5 ← 诊断
