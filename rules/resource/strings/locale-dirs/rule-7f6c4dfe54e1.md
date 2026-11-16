# 源只有仅语言限定的 values-zh 时，目标落 zh/ 目录，不收窄成 zh_CN/

审的是：资源
触发（任一种）：
- 读到：源工程 res/values-zh/strings.xml 这类只带语言、不带地区的目录（没有 values-zh-rCN）；写错的样子：目标 resources 下生成的是 zh_CN/element/string.json，没有 zh/element/；映射记录写成 values-zh → zh_CN
适用范围：把安卓 values-* 语言目录批量映射成鸿蒙 resources 下的限定词目录时
做法：
- 按源限定词的粒度映射：仅语言的 values-<语言> 落 <语言>/element/（values-zh → zh/element/），带地区的 values-<语言>-r<地区> 才落 <语言>_<地区>/element/（values-zh-rCN → zh_CN/element/）
- 「最少生成 zh_CN」只在源里没有任何中文目录时用来补齐，不用来改写已有的限定词
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 语言、文字、国家或地区之间用下划线连接；语言是 2~3 个小写字母（zh），国家或地区是大写字母（CN）：限定词目录的命名：zh 是只按语言，zh_CN 是语言加地区（出处：resource-categories-and-access.md，限定词目录）
- 区域的可选组合：语言、语言_文字、语言_国家或地区、语言_文字_国家或地区：只写语言的 zh 目录是合法的区域限定词（出处：resource-categories-and-access.md，限定词目录与设备状态的匹配规则）
- 把 zh_CN 目录改名为 zh 后中文界面恢复；繁体另放 zh_TW / zh_HK：修好后的目录（出处：卡里修好并验证过）
未核实：zh_CN 目录对其他中文地区设备的匹配行为按卡写，本机未上机核实
来源：1 张卡，1 个应用
- case-bf53fdebb87671d9eba3（Cofi）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3；取值 3 ← 诊断
