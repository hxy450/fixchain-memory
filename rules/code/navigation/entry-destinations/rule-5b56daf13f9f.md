# 接线解除导航类前向占位时，pushPathByName 的目标页按规格导航表或源端 Intent 定，不按名字猜

审的是：代码
触发（任一种）：
- 读到：子组件只发事件或枚举值、带 `FWD-REF` 标记的导航回调没写目标页；路由表里同一前缀注册了多个名称相近的页面；写错的样子：接线代码里 pushPathByName('…') 的目标是按枚举名或页面名的字面相似度选的，另一个候选页在路由表里成了没有入口的孤儿页
适用范围：跨文件接线阶段，为子组件发出的导航事件选 NavPathStack 的目标页时
做法：
- 按触发控件到 UI 规格的「导航关系」表，或源端监听器里的 Intent / startActivity，找到实际目标 Activity，再写成它对应的目标页名：pushPathByName('<该 Activity 对应的页名>', param)
- 路由表里有多个名称相近的候选页时，先确认每个各对应哪个源 Activity 再写；确认不了就登记缺口，不猜一个已注册的页面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- pushPathByName(name: string, param: unknown, animated?: boolean): void：NavPathStack 按名字压入 NavDestination，name 就是路由表里注册的页名（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- pushDestinationByName(name: string, param: Object, animated?: boolean): Promise<void>：同族接口：按名字压入，返回 Promise（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushDestinationByName）
- replacePathByName(name: string, param: Object, animated?: boolean): void：同族接口：按名字替换栈顶（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.replacePathByName）
- 对照源端监听器把目标改成规格导航表给出的那个页，没有新增路由注册：修复只改了 pushPathByName 的目标名（出处：卡里修好并验证过）
针对本应用要查的：
- 导航事件的实际目标页：UI 规格页的「导航关系」表按触发控件找；或源工程里这个控件的点击、回调监听器中的 Intent / startActivity；读出目标 Activity，注意规格里标为已注释、非运行时导航的入口不算；再到目标路由表找它对应的页名
未核实：卡里记的环境没写鸿蒙 SDK 版本，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-5dc757ad90507a893798（话费流量查询助手）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
