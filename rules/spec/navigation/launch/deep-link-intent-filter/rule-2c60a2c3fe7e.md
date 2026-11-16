# 源导航模块含深链路由器或 Manifest scheme 时，应用壳契约逐项收入深链入口或登记 skip

审的是：规格
触发（任一种）：
- 读到：源导航模块里除路由表和底部 Tab 外，还有把 Uri 映射到路由的深链路由器类和深链 base URI 常量；AndroidManifest 的 Activity 带 VIEW/BROWSABLE 的 intent-filter（自定义 scheme 或 App Links 的 https 域名和 pathPrefix）；写错的样子：契约或实施计划把应用壳概括成「路由表 + Tab」（Navigation + NavPathStack + Tabs + pageMap），复杂度记为 simple，源码锚点里没有深链路由器，也没写深链的目标符号；决策台账里又没有深链的 skip
适用范围：写应用壳、导航这一类 feature 契约或实施计划，确定入口路由、启动入口和 module 配置要承载哪些源端导航能力时
做法：
- 先列出源导航模块的全部文件和入口能力：路由表、顶层 Tab、返回栈、深链路由器与深链常量、Manifest intent-filter 的 scheme 与 App Links；每项落到契约锚点和目标符号（URI 解析函数、EntryAbility 的 onCreate/onNewWant 投递、module.json5 的 skills.uris）
- 不做的项写进决策台账的 skip；台账已承认深链只是改形态（如参数改为字符串键传递）的，契约里保留承载它的这些入口
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 目标端深链入口有两处：module.json5 的 skills 标签里配 uris；UIAbility 的 onCreate() 或 onNewWant() 里获取、解析传入的链接：契约里深链要落到的两类目标位置（出处：deep-linking-startup.md，目标应用操作指导）
来源：1 张卡，1 个应用
- case-ff125779dc6d250b6a4a（Meshtastic）：做法第 1 步 ← 建议 1、建议 2；做法第 2 步 ← 建议 1、建议 2
