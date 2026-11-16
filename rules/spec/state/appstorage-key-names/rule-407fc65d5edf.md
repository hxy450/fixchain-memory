# 规格 §状态管理里的 AppStorageV2 键只用字母、数字、下划线，不用点号命名空间

审的是：规格
触发（任一种）：
- 读到：源端只有成员字段、回调或单例状态，没有现成的存储键；规格模板 §状态管理 要求写出 AppStorageV2 / @Local 键名和类型；写错的样子：§状态管理 里新拟的 AppStorageV2 / PersistenceV2 键带「.」或「-」，写成「领域.字段」式命名空间；或者只写了分组的逻辑名，没写运行时键
适用范围：规格为跨组件共享状态新拟 AppStorageV2 / PersistenceV2 键名时
做法：
- §状态管理 直接写平台合法的运行时键：只用字母、数字和下划线，分组写成「领域_字段」，不用「.」或「-」做命名空间
- 想保留分组语义时分两列写「逻辑名」和「运行时键」，运行时键是合法键，不让实现者自行推断
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- key 可由字母、数字、下划线组成，长度不超过 255，使用非法字符或空字符的行为未定义：AppStorageV2.connect 的键规则（出处：arkts-new-appstoragev2.md，使用说明）
- PersistenceV2.globalConnect 的 key 同样可由字母、数字、下划线组成，长度不超过 255：PersistenceV2 全局连接的键规则（出处：js-apis-StateManagement.md，globalConnect18+）
- 点号键在运行时报 invalid AppStorageV2 key；改成下划线键后通过：点号命名空间键在目标端不可用（出处：卡里修好并验证过）
未核实：卡里看到的非法键报错出自 API 24（HarmonyOS 6.1.1），本机声明是 API 23；文档只说非法字符的行为未定义
来源：1 张卡，1 个应用
- case-bdf87ded9505fbbf72a5（opencamera-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
