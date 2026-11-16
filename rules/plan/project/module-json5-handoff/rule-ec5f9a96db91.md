# 规格里带裁决的入口配置 AC 进切片账本时，列入 integration_points / wires 并指定写者

审的是：计划与派工
触发（任一种）：
- 读到：规格的验收条目或替代路径写明「入口配置由 module.json5 shortcuts 承担」，并标明是裁决；写错的样子：切片账本的 integration_points / wires 里没有入口接线这一项，或列了却没指定写者
适用范围：把规格的验收条目提升到切片账本、分配跨文件接线时
做法：
- 把这条 AC 写进 integration_points / wires：写明要落的文件（module.json5 的 shortcuts 声明、EntryAbility 的 want 分支、路由分支）和负责写的切片或 closer
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 入口配置 AC 在「规格 → 切片账本」这一步漏掉后，worker 和 closer 都没再补，生成结束时没有 shortcuts 声明：漏在账本这一步就没有承接者（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-c699af1f5c3b03105480（DeepAI全能PPT）：做法第 1 步 ← 建议 4；取值 1 ← 诊断
