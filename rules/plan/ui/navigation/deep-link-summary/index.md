# 交接摘要里剩余工作的深链入口

agent 会看到什么：决策台账写了深链行为、受影响的验收条目是 P0，交接摘要或实施计划的剩余工作只写「Index = Navigation + NavPathStack」「module.json5 只加 requestPermissions」，没逐文件写深链入口

## 规矩

- rule-d9c3918ac48f｜会话可能压缩时，交接摘要的剩余文件清单逐文件写明深链入口｜读到：决策台账写了深链行为只改形态（如深链参数以字符串键传递），受影响的验收条目是 P0；写错：交接摘要或实施计划的剩余工作只写「Index = Navigation + NavPathStack + Tabs + pageMap」「module.json5 只加 requestPermissions」，没有 URI 解析函数、导航栈的深链处理、EntryAbility 的 onCreate/onNewWant 投递和 module.json5 的 skills.uris
- rule-c47090c8fc97｜计划拆分时把深链的 skills.uris 列为单独交付项并指定归属切片｜读到：规格里有源端 intent-filter 深链的映射；写错：切片计划只把「onCreate / onNewWant → 解析 → 路由」派给某切片，没有 module.json5 skills.uris 这一项；唯一涉及 module.json5 的配置任务派工写「其余字段零改动」
