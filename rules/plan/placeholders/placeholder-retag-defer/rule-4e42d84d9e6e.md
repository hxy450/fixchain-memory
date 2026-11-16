# 收口处理 forward-ref-uncertain 条目时先回看源码，能实现就当场实现，不改 deferred

审的是：计划与派工
触发（任一种）：
- 读到：收口或验收阶段手里有 forward-ref-uncertain（`UNC`）条目，条目指向的源码行为已写明；写错的样子：条目被改成 deferred 或把 resolve_by 改成「verify visual tuning」，理由写「requires runtime scroll telemetry」之类，没有回看源码
适用范围：收口、验收阶段处理占位和移交项登记时
做法：
- 先打开条目指向的源码判断当前能否实现；能实现就当场实现并关掉条目，只有确需真机数据时才改为 deferred，并写明缺的是哪项数据
来源：1 张卡，1 个应用
- case-66f3c1649b7b5c4f38b5（Cofi）：做法第 1 步 ← 建议 4
