# 语言目录缺脚手架身份键时，不填 'label' 等模板值让审计通过，从 base 或源端真值派生

审的是：资源
触发（任一种）：
- 读到：i18n 完整性审计报 `en_US` 等语言目录缺 `EntryAbility_label`、`EntryAbility_desc`、`module_desc`（key_missing）；写错的样子：语言目录的 `element/string.json` 里补上了这些键，值却是脚手架模板默认值（如 `"label"`、`"description"`）
适用范围：资源迁移阶段 i18n 补齐时，为语言限定目录补身份类字符串键
做法：
- 不写模板默认值；按 i18n 流程的异常规则报告 key_missing，或从 base 和源端真值（manifest 的 android:label 引用的字符串）派生
- 派生补入的身份键在迁移记录里标成「身份落地后必须复核」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 系统优先从与设备状态匹配的限定词目录取资源，找不到才去 base：语言目录里的模板值会盖过 base 里的正确值，英文环境下桌面标签显示模板值（出处：resource-categories-and-access.md，资源匹配）
- 键存在性审计只查键不查值，填模板值也会转 PASS：审计通过不代表值正确（出处：卡里修好并验证过）
针对本应用要查的：
- 应用名的真值：源工程 AndroidManifest.xml 里 `<application android:label="@string/…">` 引用的字符串，到 res/values 的字符串 XML 里按名字找；读出该字符串的值作为 EntryAbility_label 的来源；源端有对应语言目录的取该语言的值
来源：1 张卡，1 个应用
- case-a7791275ac232a60053d（DeepAI全能PPT）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；取值 2 ← 诊断
