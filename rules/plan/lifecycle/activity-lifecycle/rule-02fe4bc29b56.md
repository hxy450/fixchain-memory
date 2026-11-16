# 启动恢复的 HANDOFF 要写明「首帧前同步生效」这类时序约束

审的是：计划与派工
触发（任一种）：
- 读到：源入口 Activity.onCreate 在 super.onCreate 之前设主题，目标的恢复函数交给别的写者接到 EntryAbility.onCreate；写错的样子：`HANDOFF` 只写「在 EntryAbility.onCreate 调用 …」，没写首帧前完成的时序约束；接线方按原样补了一个不等待的 async 调用就把移交项记为已兑现
适用范围：为入口启动恢复（主题、语言等首帧前要生效的设置）登记移交项和收口时
做法：
- HANDOFF 里写明时序约束，如「首帧前同步生效，须在 loadContent 之前完成」；接线方看到 onCreate 调用的是 async 函数时，先确认它是否须在首帧前完成，不只补调用点
来源：1 张卡，1 个应用
- case-cc22f6cc1041c8cc1129（MifareClassicTool）：做法第 1 步 ← 建议 2
