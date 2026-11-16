# 源码自定义触底触发 helper 时，规格先读函数体，写清触发条件、时机和调用点实参

审的是：规格
触发（任一种）：
- 读到：源端列表调用自定义的触底 helper，函数体是 derivedStateOf { 末项可见判定 } 加 if (条件 && !重试态) LaunchedEffect(Unit) { 加载下一页 }；写错的样子：规格转换决策只写「helper → List.onReachEnd」或「onReachEnd / onScrollIndex」「onReachEnd / onDidScroll 阈值」，没写触发条件、触发时机和调用点的重试参数
适用范围：规格提取阶段为分页列表写触底追加加载的映射时
做法：
- 先读 helper 的函数体和它依赖的判定函数，映射写清：条件（totalItems > 0 且最后可见项下标 == totalItems - 1）、时机（由假变真触发一次；首屏未满也成立；数据或重试态变化后重判）、各调用点的重试实参（是否字面 false），不只写一个平台回调名
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onReachEnd(event: () => void): ListAttribute：滚动到末尾的事件回调，声明里没有末项可见状态的条件（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onReachEnd）
- 各列表改用 onScrollIndex 的 end 下标加总项数、重试态做上升沿判定后，首屏未满、追加后仍未满时都会继续加载：映射应指向状态判定，不是滚动事件（出处：卡里修好并验证过）
针对本应用要查的：
- 触底 helper 的完整条件和各调用点实参：源工程里定义该 helper 的 Compose 文件（函数体）、它调用的末项可见判定函数，以及每个列表页面里调用 helper 的那一行；读出判定表达式（是否要求 totalItems > 0、是否比较末项下标）、触发包装（derivedStateOf + LaunchedEffect 即由假变真触发），逐个调用点记下重试参数是变量还是字面 false
未核实：onReachEnd 首屏未铺满不触发、弹簧回弹重复触发，卡里依据修复审计的表述，没有核对文档
来源：1 张卡，1 个应用
- case-c9f6d4fc935ada70c215（jerboa）：做法第 1 步 ← 建议 1、诊断；取值 2 ← 诊断
