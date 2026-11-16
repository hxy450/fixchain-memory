# 路由装配页的可达和闭合

agent 会看到什么：Navigation + pageMap 装配的启动页、选择器目标页和在 pageMap 注册的死码页，在 HANDOFF、自检、完成信封、收口里写的可达或完成说法

## 规矩

- rule-2dfd5ab93f5d｜入口接线的 HANDOFF 或自检要断言首屏可达，不以 grep 到启动 Builder 名或编译通过代替｜读到：入口由 Navigation + pageMap 装配，启动页经路由进入；写错：入口接线的 HANDOFF 只写 verify=grep:启动 Builder 名，或自检只报编译 PASS、结构闭环 CONVERGED，没有一项核对空栈时的初始 pushPathByName
- rule-d8fa816268b3｜目标页没有回传字段或加载/选中仍是 FWD-REF 时，完成信封登记未闭合，不把入口标成出口｜读到：目标页的参数类只携带初始值、没有结果回传字段，或它的加载 / 选中处理仍是 `FWD-REF` 前向引用；写错：完成信封把「打开选择器」的入口当成已完成的真实出口，没有登记回传缺口或未闭合的 `FWD-REF`
- rule-dd1c8c87e2a1｜已转换并在 pageMap 注册的死码页，页内占位要兑现或撤销注册，不改标成永久披露｜读到：页面被判为死码，但目标的路由 pageMap 里注册了它，可以按名进入；写错：收口时把页内功能占位改成「死码域披露……永久保留——合法外部延迟」，债务闸不再报 GAP，功能仍是空壳
