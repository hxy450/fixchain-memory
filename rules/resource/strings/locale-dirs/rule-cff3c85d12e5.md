# 语言目录只放源端有的文字资源，不复制 base 的 color/float 等 element 文件

审的是：资源
触发（任一种）：
- 读到：Android 源的 values-<locale> 只含 strings.xml / arrays.xml（文字资源），color、dimen、bool、integer 只在 values/ 和 values-land 等非语言目录；写错的样子：目标 resources/<语言_地区>/element/ 下出现 color.json、float.json、boolean.json、integer.json，内容是 base 同名文件的整份副本
- 读到：i18n 完整性审计报告语言目录 `key_missing`，findings 只列 string / strarray 键；写错的样子：补齐时写通配脚本：base/element/*.json 在语言目录没有同名文件就整份复制，回执是「建文件 N 个、补键 0 个」
适用范围：迁移资源、补 i18n 审计缺项时，目标 resources 下各语言限定目录的 element 文件
做法：
- 语言目录的 element 只放源端 values-<locale> 实际有的类型（string.json、strarray.json、plural.json）；color.json、float.json、boolean.json、integer.json 只留在 base 和 horizontal、ldpi 等非语言限定目录
- 补审计缺项按 findings 里的具体 key 和文件类型，只把该键补进它所在的 string.json / strarray.json；缺的是 string / strarray 以外的键时不复制 base 文件，修正审计范围或按回退到 base 接受
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 限定词目录匹配优先级从高到低：移动国家码和移动网络码 > 区域（语言、语言_文字、语言_国家或地区…）> 横竖屏 > 设备类型 > 颜色模式 > 屏幕密度：语言目录里的副本优先于 horizontal、ldpi 等目录，会遮蔽那里的覆盖值（出处：resource-categories-and-access.md，限定词目录与设备状态的匹配规则）
- 在限定词目录中找不到该资源时，才去 base 目录查找：语言目录缺非文字键时会回退到 base，不用补（出处：resource-categories-and-access.md，资源匹配）
- element 目录的文件名：boolean.json、color.json、float.json、intarray.json、integer.json、plural.json、strarray.json、string.json，每个文件只含同一类型：按类型判断哪些是文字资源（出处：resource-categories-and-access.md，资源组目录）
- 语言目录里的 color/float/boolean/integer 副本遮蔽了 horizontal 的覆盖值和 base 后来改的颜色；删掉这些副本、只留 base、dark、horizontal、ldpi 的 element 文件后恢复：修好后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 源端每个语言目录实际有哪些资源类型：源工程 res/values-<locale>/ 下的 XML 文件及其中的 <string>、<string-array>、<plurals> 等标签；只有这些类型在目标的同一语言目录里出现，其余类型不建文件
未核实：卡里看到的遮蔽出自 API 24（6.1.1）的目标工程，本机核对用的是文档副本和 API 23 的 SDK
来源：1 张卡，1 个应用
- case-0a7b2dfdeda43ad845ca（omni-notes-hmos）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 1、建议 3；取值 4 ← 诊断
