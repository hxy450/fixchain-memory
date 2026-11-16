# 跳转移交给收口者时写 HANDOFF 条目或保留 FWD-REF，不只在报告里写待定

审的是：计划与派工
触发（任一种）：
- 读到：占位登记表里这个 P-ID 的触发条件包含路由到结果页；源端成功后启动结果页；写错的样子：报告里只写「由 closer 决定是否跳转」，FWD-REF 已删，也没有带 owner / what / verify 的 HANDOFF；或收口者只凭 Store 交接把 P-ID 改成 resolved、勾选了集成点
适用范围：切片 worker 把未完成的接线移交给 closer，以及 closer 关闭占位条目、勾选集成点时
做法：
- 确需移交时写成 HANDOFF（owner、what、verify，verify 可写成在目标文件里搜结果页的 push），或保留 FWD-REF 标记
- closer 把 P-ID 改成 resolved 或勾选导出集成点前，按源端调用链核对成功后的页面去向已经实现
来源：1 张卡，1 个应用
- case-3094b57f19bdd601c03e（美颜相机）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、建议 1
