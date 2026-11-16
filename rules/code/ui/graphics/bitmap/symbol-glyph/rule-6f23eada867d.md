# 源 Text 里的 emoji 迁成目标 Text 原样保留，不换成 SymbolGlyph 系统符号

审的是：代码
触发（任一种）：
- 读到：源端 Text("⭐") 这类 emoji 字面文本（如 ListItem 的 leadingContent）；写错的样子：目标写 SymbolGlyph($r('sys.symbol.star_fill')) 一类系统符号替代 emoji
适用范围：源界面用 Text 显示 emoji、迁成 ArkUI 时
做法：
- 写成 Text('<原 emoji>')，字符照抄源端
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- emoji 恢复为 Text 文本：修复后与源端一致（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-0848ab137044cb92d1bc（Cofi）：做法第 1 步 ← 诊断；取值 1 ← 诊断
