# 汇总 Base handoff 时，建议 P-ID 登记进 registry 并写进 owner 切片接线项

审的是：计划与派工
触发（任一种）：
- 读到：Base handoff 里有「Suggested P-ID Allocations / 交主线程分配的建议」（带 owner、resolve_by）；写错的样子：汇总后的 registry 里没有这个 P-ID，owner 切片在 feature-plan 里的 integration_points 和 placeholders_planned 也没有这项（如 placeholders_planned: []）
适用范围：编排汇总阶段，回填 feature-plan 和各 Base handoff、进入下一阶段前
做法：
- 凡「交主线程分配」的建议 P-ID，进入 Stage 3 前登记进 registry 或转成源码 HANDOFF，并写进对应 owner 切片的 integration_points 和派工
- Stage 2 闸前 grep 各 handoff 的 Suggested / 待闭环 段，非空且未登记就阻断
未核实：主线程派给切片和收尾者的任务正文看不到，卡里没能确认其中是否提到这项
来源：1 张卡，1 个应用
- case-2880da61086b19aff2a4（实时公交）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
