# 各语言目录的入口 Ability label 取同一语言源 app_name 的解析结果，不手抄字面量

审的是：资源
触发（任一种）：
- 读到：Manifest 里 application 和启动 Activity 的 android:label 都引用 @string/app_name，values-<语言>/strings.xml 里有 app_name 译名；写错的样子：entry/src/main/resources/<语言>/element/string.json 里 EntryAbility_label 的值和该语言源 app_name 不一致（如少了字），转换脚本里它是手写的字面量
适用范围：用转换脚本写各语言 string.json，并给目标端补写派生键（如入口 Ability 的 label）时
做法：
- 派生键的值直接引用同一次从源文件解析出的结果：<语言> 目录的 EntryAbility_label = 源 values-<语言> 的 app_name，不手抄字面量
- 写后逐个语言目录断言派生键等于对应源值；断言与源值不符时以源为准，先在脚本里搜同一字面量的所有出现处一起改，再判断错的是断言还是数据
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 语言限定词目录由 2~3 个小写字母组成（如 zh、en），取值按 ISO 639：源 values-<语言> 对应目标 resources/<语言>/element/string.json（出处：resource-categories-and-access.md，资源目录的限定词目录（语言））
- 入口 Ability label 改成与该语言源 app_name 一致后，应用首选语言设为该语言时读回正确：修好后的结果（出处：卡里修好并验证过）
针对本应用要查的：
- 各语言的应用名译名：源工程 res/values-<语言>/strings.xml 里 android:label 引用的那个字符串（通常是 app_name）；逐语言读出该字符串的值，作为目标同语言目录入口 Ability label 和 AppScope app_name 的值
来源：1 张卡，1 个应用
- case-d720656a9811d5cdd419（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
