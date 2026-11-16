# 会话可能压缩时，交接摘要的剩余文件清单逐文件写明深链入口

审的是：计划与派工
触发（任一种）：
- 读到：决策台账写了深链行为只改形态（如深链参数以字符串键传递），受影响的验收条目是 P0；写错的样子：交接摘要或实施计划的剩余工作只写「Index = Navigation + NavPathStack + Tabs + pageMap」「module.json5 只加 requestPermissions」，没有 URI 解析函数、导航栈的深链处理、EntryAbility 的 onCreate/onNewWant 投递和 module.json5 的 skills.uris
适用范围：应用壳和导航的实施计划、上下文压缩前的交接摘要
做法：
- 剩余文件清单逐文件写上深链入口：路由文件的 scheme 常量、URI 解析函数和子路由表；导航栈的深链处理和待处理投递；EntryAbility 的 onCreate 与 onNewWant 读 want.uri；首页应用深链；module.json5 的 skills.uris
来源：1 张卡，1 个应用
- case-ff125779dc6d250b6a4a（Meshtastic）：做法第 1 步 ← 建议 2、诊断
