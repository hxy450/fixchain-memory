# 规格要改本页输出以外的配置文件时，登记 deferred-work 并在返回信封列出

审的是：计划与派工
触发（任一种）：
- 读到：规格要求修改本页输出文件以外的配置文件（如「module.json5 EntryAbility orientation: …」），登记表约定 module.json5 配置属 deferred-work、归属步骤或触发条件必填；写错的样子：只在转换报告的「交由后续」里写一句（如「module.json5 orientation=… → 入口装配段」），占位登记表里没有 kind=deferred-work 的条目，返回信封也没列；或交给职责不覆盖该项的步骤（如入口 Navigation 装配）
适用范围：页面转换阶段，规格里有本页输出文件以外的配置项时
做法：
- 在登记表里登记 kind=deferred-work，location=该配置文件，resolve_by=计划中确有该项的步骤
- 在返回信封里逐项列出这些 deferred-work，不只写在转换报告里
来源：1 张卡，1 个应用
- case-11ff372c001b24f1dce2（GameOfLife）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
