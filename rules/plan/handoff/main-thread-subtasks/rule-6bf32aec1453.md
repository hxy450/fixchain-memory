# 子代理被告知由主线程处理的子任务，主线程宣布 Stage 完成前逐项勾销

审的是：计划与派工
触发（任一种）：
- 读到：子代理的回执或资源映射表里写着某些子任务（如启动图标层）「跳过、由主线程处理」；写错的样子：主线程宣布「Stage 0 全部完成」，移交项没有逐项勾销，模板残留（EntryAbility_label 值为 label、模板 background.png / startIcon.png）还在
适用范围：编排主线程收尾一个阶段、宣布完成时
做法：
- 宣布 Stage 完成前，把子代理移交给主线程的子任务逐项勾销，每项写明落到了哪个文件
- 收尾时 grep 模板残留：EntryAbility_label 的值是否还是 label，background.png / startIcon.png 是否还是模板图
来源：1 张卡，1 个应用
- case-4f7163b95249e9ede2ca（Cofi）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4
