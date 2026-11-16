# 巡检见到无调用点的处理函数时，回查源端控件，源端没有就按多余接线处理

审的是：计划与派工
触发（任一种）：
- 读到：目标页面里有没有任何 UI 或调用点的结果处理函数；源 Fragment 的 setOnClickListener、布局控件和 page spec 的组件表、导航表里都没有对应入口；写错的样子：巡检单把它判成「入口未渲染」类缺陷，依据写 plan 的 integration_points 或某几条 AC，fix 写「按 Android 可达入口补 UI/事件接线」
适用范围：UI 巡检判定页面缺失入口、写修复条目时
做法：
- 先回查源 Fragment 的 setOnClickListener、布局控件和 page spec 的组件表、导航表；源端没有对应控件时，条目写成多余接线（删除或移出页面），不写「入口未渲染」
- plan 的 integration_points 只当函数级接线，不当成 UI 要求写进修复条目
来源：1 张卡，1 个应用
- case-5e406619f9f3d3f028c6（话费流量查询助手）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2
