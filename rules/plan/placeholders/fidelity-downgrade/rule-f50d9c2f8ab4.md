# 资产已在、只缺状态帧时，不登记 resource-pending-asset 挂资源批次，在本文件实现

审的是：计划与派工
触发（任一种）：
- 读到：规格把动画矢量图标映射为 resource animation or equivalent symbol animation、要求 Keep observable state transition；目标里同名媒体已存在；写错的样子：代码注释、占位登记或报告里给这个引用加 P-RES-ASSET-… kind=resource-pending-asset，resolve_by 写资源批次（如 Batch resource closure），或登记成 deferred
适用范围：界面实现阶段登记占位和移交项时，引用的资产已存在、缺的是按状态选帧或动画语义的情形
做法：
- resource-pending-asset 只用于 resource-mapping 里没有真实值、暂用兜底占位资产的引用
- 资产在、缺状态或动画语义时，在本文件内用系统 symbol、Path 或状态分支实现；做不到就在报告里写明缺哪一帧，不挂到资源批次
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按资源规则，后续资源批次不会产出 path-morph 资产：挂到资源批次的这类登记永远不会被解决（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-753b41488ff67ec1d068（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 1 ← 诊断
