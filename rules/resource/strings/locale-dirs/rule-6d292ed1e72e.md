# 源语言目录缺的键在目标限定词目录里也留缺，不补机器翻译或 TODO 占位

审的是：资源
触发（任一种）：
- 读到：源端 values-xx/strings.xml 的键比默认 res/values/strings.xml 少，运行时缺键回退默认 values；写错的样子：目标 zh_CN/element/string.json 的键数与 base 相同，多出源端该语言目录没有的键，值是自动翻译或带 `[TODO: translate]`
适用范围：把安卓各语言字符串资源转成鸿蒙限定词目录的 string.json 时
做法：
- 限定词目录的 string.json 只放源端该语言目录里有的键，缺的键不写，让系统回退 base（与安卓回退默认 values 一致）；任务明确要求补译时才补
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 限定词目录中找不到该资源时，才去 base 目录中查找：缺键自动回退 base，不必补齐（出处：resource-categories-and-access.md，资源匹配）
- zh_CN 键集改为镜像 values-zh、删去补译的键后，这些文案回退 base 英文，与安卓一致：改后的效果（出处：卡里修好并验证过）
针对本应用要查的：
- 源端每个语言目录的键集：源工程 res/values-xx/strings.xml（及 arrays.xml、plurals.xml）里的 name；目标同名限定词目录的 string.json 只收这些 name
来源：1 张卡，1 个应用
- case-8a522021d6d10fded125（MifareClassicTool）：做法第 1 步 ← 建议 3、诊断；取值 2 ← 诊断
