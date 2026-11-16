# 有 productFlavors 时 app_name 取台账指定 flavor 的值，不取默认或第一个

审的是：资源
触发（任一种）：
- 读到：源工程 src/<flavor>/res/values/strings.xml 里各 flavor 各有 app_name、app_package，派工说明或决策台账指定了某个 flavor；写错的样子：AppScope/resources/base/element/string.json 的 app_name 是另一个 flavor 的值，或者入口 UIAbility 的 label 引用了一个另写的同值串而不是 app_name
适用范围：源端用 productFlavors 区分应用身份串、落地 AppScope 字符串和入口 label 时
做法：
- 按派工或台账指定的 flavor 一次选定全部身份串（app_name、app_package、applicationIdSuffix），写进 AppScope 的 string.json；台账的 flavor 指定对这些串都适用，不只对包名
- app.json5 的 label 写 $string:app_name，module.json5 入口 UIAbility 的 label 也引用 app_name
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- "label": "$string:app_name"：app.json5 的应用名引用 AppScope/resources/base/element/string.json 里 name 为 app_name 的资源（出处：layered-image.md，配置分层图标和应用名称）
- label：取值为字符串资源的索引，字符串长度不超过 63 字节，不可缺省：app.json5 的 label 规则（出处：app-configuration-file.md，配置文件标签（表1 label））
针对本应用要查的：
- 指定 flavor 的身份串：源工程 src 下该 flavor 目录的 res/values/strings.xml，按 app_name、app_package 找；flavor 看派工说明和决策台账；取该 flavor 下的字面值；main 或别的 flavor 的值不用
来源：1 张卡，1 个应用
- case-d78a91fb9dfa366ec2ee（omni-notes-hmos）：做法第 1 步 ← 建议 2；做法第 2 步 ← 诊断
