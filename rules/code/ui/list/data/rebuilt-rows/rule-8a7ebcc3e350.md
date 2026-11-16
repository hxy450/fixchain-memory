# removeAllViews 后逐项 addView 的行内容可能重复时，ForEach 键带位置标识

审的是：代码
触发（任一种）：
- 读到：源端一次计算里 removeAllViews() 后循环 inflate / addView 结果行，行内容可能完全相同（如多个相同的数据块）；写错的样子：ForEach 的 keyGenerator 只用显示内容拼键（如 `${a}_${b}_${c}`），不含条目序号；渲染模型 class 没有唯一标识字段
适用范围：把源端「清空容器后逐项添加」的动态结果区改成 ArkUI ForEach 数据驱动渲染时
做法：
- 渲染模型 class 加一个 key 字段，写入条目在本次结果里的位置标识（如分组号 + 组内序号），再按需拼内容字段；ForEach 的 keyGenerator 直接返回 item.key
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ForEach(arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string)：ForEach 的签名，第三个参数自定义键值（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 框架会对重复键值发运行时警告；UI 更新时出现重复键值，框架可能无法正常工作：只靠内容拼出的键遇到相同条目就重复，后面的条目可能渲染不出来（出处：arkts-rendering-control-foreach.md，键值生成规则）
- key(keyGenerator: (item: T, index: number) => string): RepeatAttribute<T>：同族接口：Repeat 的键值生成（出处：鸿蒙 SDK 的 ets/component/repeat.d.ts，RepeatAttribute.key）
- (dataSource: IDataSource, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): LazyForEachAttribute：同族接口：LazyForEach 的键值生成（出处：鸿蒙 SDK 的 ets/component/lazy_for_each.d.ts，LazyForEachInterface）
未核实：重复键下运行时具体渲染哪一项未单独核实；卡里的版本是 API 24，本机按 API 23 核对声明
来源：1 张卡，1 个应用
- case-74bcab538b062ee7cac8（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断
