# 列表迁移时逐项接上源端条目点击行为，ForEach 条目要有真的 .onClick，注释不算

审的是：代码
触发（任一种）：
- 读到：源端 adapter 的 onItemClickListener，或 RecyclerView.addOnItemTouchListener 的 onSingleTapUp 里对条目做了事（如把条目内容 setText 回填到输入框）；写错的样子：ForEach 条目的 Row / Column 只有样式链，没有 .onClick，上方注释却写着「点击回填输入框」
- 写错的样子：交回报告把条目点击列为已实现交互，目标文件里 ForEach 条目却找不到 .onClick
适用范围：页面 UI 转换阶段迁移 RecyclerView 列表的条目交互时
做法：
- 先枚举源端 onItemClickListener 和 addOnItemTouchListener 里的行为，在 ForEach 的每个条目上逐项接 .onClick(() => { … })，例如回填写成 .onClick(() => { this.<输入框绑定的状态> = item.<内容字段> })
- 报告把交互列为已实现前，在目标文件里搜到对应的事件代码，注释不能代替实现
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onClick(event: (event: ClickEvent) => void): T：CommonMethod 的点击事件，条目容器上直接挂（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onClick）
- (arr: Array<any>, itemGenerator: (item: any, index: number) => void, keyGenerator?: (item: any, index: number) => string): ForEachAttribute：ForEach 的调用签名，事件挂在 itemGenerator 里生成的条目组件上（出处：鸿蒙 SDK 的 ets/component/for_each.d.ts，ForEachInterface）
- 示例条目 Row 补 .onClick 回填输入框状态：修好后点击条目回填输入框、不跳页，与源端一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-77e4e8b4e16c3fc8e030（DeepAI全能PPT）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 3 ← 诊断
