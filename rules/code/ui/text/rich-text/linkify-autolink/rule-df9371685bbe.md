# 按多个正则把文本切成 run 时，命中和间隔文本按原位置顺序输出，单测断言拼接等于原文

审的是：代码
触发（任一种）：
- 读到：源端在同一文本节点上用 Linkify.addLinks 跑多个 Pattern，再按 start + getSpanStart / getSpanEnd 原位挂 span，文本顺序不变；写错的样子：切分循环里把每个命中直接 push 成 LINK run，间隔文本先收进另一个数组、循环结束后再输出；单测只测正则命中与捕获组
适用范围：目标端自研解析器把一段文本按多个正则（自动链接、用户/社区简写等）切成有序 run 再交给 StyledString / Span 渲染时
做法：
- 单次扫描合并各规则的命中区间、按起点排序后依次输出「间隔文本、命中」；或每遇到一个命中，先即时输出它前面的间隔文本再输出命中
- 单测用「前文 + 链接 + 后文」断言：所有 run 的文本拼接等于原文，链接 run 的位置不变
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Linkify.addLinks 先 gatherLinks 收集各规则命中，pruneOverlaps 去掉重叠，再按每个命中的 start / end 原位 applyLink：源端链接只是挂在原文位置上的 span，不改变文本顺序（出处：android.text.util.Linkify#addLinks）
- 按文本节点先 Linkify 再用户/社区简写，位置交错输出，重叠的丢弃：修复后的切分方式（出处：卡里修好并验证过）
未核实：卡里 compileSdk 37，框架源码按本机 android-36.1 核实
来源：1 张卡，1 个应用
- case-8b307e33adf3d2817a04（jerboa）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 2 ← 诊断
