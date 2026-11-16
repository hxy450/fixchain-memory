# 页面路由与入口

目标端用 Navigation + pageMap、NavDestination、NavPathStack 装配页面，或者台账写了深链，派工、自检、交接摘要里写到页面可达、路由守卫、深链入口时

## 触发族

- [路由装配页的可达和闭合](routed-page-reachability/index.md)（3 条）：Navigation + pageMap 装配的启动页、选择器目标页和在 pageMap 注册的死码页，在 HANDOFF、自检、完成信封、收口里写的可达或完成说法
- [根 Navigation 壳与 NavDestination 页的分工](nav-shell-pages/index.md)（4 条）：派工、装配说明或跨切片草稿里，根 Navigation 壳上的机制（四向 expandSafeArea、共享转场、路由守卫）要各 NavDestination 页配合，或要按规格的映射写守卫表达式
- [交接摘要里剩余工作的深链入口](deep-link-summary/index.md)（2 条）：决策台账写了深链行为、受影响的验收条目是 P0，交接摘要或实施计划的剩余工作只写「Index = Navigation + NavPathStack」「module.json5 只加 requestPermissions」，没逐文件写深链入口
- [并行生成的页面共用的路由参数类](route-param-class-source/index.md)（1 条）：源端路由是带 {id} 占位的字符串模板，多个页面将由不同 agent 并行或分批生成；计划和派工说明里没规定路由参数类的唯一来源文件和字段，页面转换派工只说「路由注册归某切片」
