# 删除 FWD-REF 或宣布 seam 已解决前，确认对应区块已有数据来源，未接上的列为缺口

审的是：计划与派工
触发（任一种）：
- 读到：规格写明某组件的区块数据来自尚未接好的 seam（如「daily detail 与日历 seam」），代码里有对应的 `FWD-REF` 占位标记；写错的样子：`FWD-REF` 标记被删除，slice notes 只写「交给后续合并」，没有列出这个区块的数据仍未接入
适用范围：页面接线阶段清理 FWD-REF 占位、宣布 seam 已解决、写 slice notes 时
做法：
- 删除 FWD-REF 前逐项核对它指向的每个区块开关和数据字段都有真实赋值来源
- 没接上的保留 FWD-REF，并在 slice notes 的缺口里写明哪个区块、缺哪项数据、源端的查询在哪
来源：1 张卡，1 个应用
- case-9ccc879e5d89039f29f4（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
