# 系统 Kit 提供的能力不登记成「SDK 入仓」占位，forward-ref 只在真实入口建立后关闭

审的是：计划与派工
触发（任一种）：
- 读到：占位登记里有 forward-ref「华为账号登录入口（鸿蒙等价）建立」，resolve_by 指向本切片；写错的样子：实现留成恒返 null 后把这条 forward-ref 翻成 resolved，另登记一条 thirdparty-sdk 占位「华为账号 SDK(HMOS) 等价入仓」
适用范围：实现阶段更新占位登记、处理账号或渠道类 forward-ref 时
做法：
- 能力由系统 Kit 提供的（如 @kit.AccountKit），不登记「SDK 入仓」类触发器；forward-ref 只在真实调用链写好后翻成 resolved，依赖配置的另登记配置项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @kit.AccountKit 随鸿蒙 SDK 提供（hms/ets/kits 下）：不需要入仓（出处：鸿蒙 SDK 的 hms/ets/kits/@kit.AccountKit.d.ts）
来源：1 张卡，1 个应用
- case-0fef61d9f1aa5cc24534（DeepAI全能PPT）：做法第 1 步 ← 建议 3
