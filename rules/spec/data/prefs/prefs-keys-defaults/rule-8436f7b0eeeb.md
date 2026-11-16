# 源端对非空状态做 == null 判断时，规格记成永不触发的死分支，不译成首启或未初始化

审的是：规格
触发（任一种）：
- 读到：Compose 显示条件里对状态变量写 == null / != null，而该变量由 collectAsState(initial = false) 收集，Flow 的 getter 映射成 preferences[KEY] == true 或带 ?: 默认值；写错的样子：规格把这个条件写成「首次进入」「设置未初始化（…== null）」时触发弹窗或权限请求
适用范围：规格提取阶段把源端显示条件里的 null 判断翻成页面触发条件时
做法：
- 先核该变量的声明类型和来源：collectAsState 的 initial 值、Flow getter 的映射（== true 或 ?: 默认值）；是非空类型的，写成「恒 false（或恒 true）的死分支，源端可观察行为 = 从不触发」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- collectAsState(initial = false) 收集 preferences[KEY] == true 映射出的 Flow<Boolean> 时，变量 == null 恒为 false，对应弹窗在源端从不出现：按非空类型判定分支不可达（出处：卡里修好并验证过）
针对本应用要查的：
- 状态变量是不是可空类型：源工程里该变量的 collectAsState / collectAsStateWithLifecycle 调用（看 initial），以及它收集的 Flow 的 getter（DataStore 读取处的 map 表达式）；initial 非空且 getter 用 == true 或 ?: 默认值映射的，类型是非空 Boolean，== null 判断恒为 false
来源：1 张卡，1 个应用
- case-3b4906429163bc7ea455（Cofi）：做法第 1 步 ← 建议 1、诊断；取值 1 ← 诊断
