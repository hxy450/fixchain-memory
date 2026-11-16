# 源码理解笔记的 Toast 决策按调用点记时长和文案加工，不记成统一 LONG

审的是：规格
触发（任一种）：
- 读到：源码里 Toast.LENGTH_SHORT 与 LENGTH_LONG 混用，部分文案带 toLowerCase 等加工；写错的样子：source-notes 或决策台账写「服务层 Toast 统一 3500ms 对齐 LENGTH_LONG」，或「Resource 无法 toLowerCase，目标直接用资源原文」
适用范围：写源码理解笔记、决策台账里关于 Toast 时长和文案的条目时
做法：
- 决策写成「时长按调用点映射：LENGTH_SHORT → 2000ms，LENGTH_LONG → 3500ms，公共封装带 duration 参数」
- 文案加工写成「经 getStringSync 取成 string 后保留源码的加工」，不写平台做不到
来源：1 张卡，1 个应用
- case-65c33c4172d6d208c5a5（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 3、诊断
