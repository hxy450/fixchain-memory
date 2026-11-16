# 入口接线的 HANDOFF 或自检要断言首屏可达，不以 grep 到启动 Builder 名或编译通过代替

审的是：计划与派工
触发（任一种）：
- 读到：入口由 Navigation + pageMap 装配，启动页经路由进入；写错的样子：入口接线的 HANDOFF 只写 verify=grep:启动 Builder 名，或自检只报编译 PASS、结构闭环 CONVERGED，没有一项核对空栈时的初始 pushPathByName
适用范围：入口 Navigation 接线的 HANDOFF 和自检项
做法：
- HANDOFF 的 verify 写成核对入口 aboutToAppear 里空栈时 pushPathByName 启动页的语句（或启动后的 UI dump），不写只核符号存在的 grep
来源：1 张卡，1 个应用
- case-d1b8189b8a745399dc3a（实时公交）：做法第 1 步 ← 建议 3
