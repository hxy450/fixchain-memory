# 源应用名在 values-<语言> 有译名时，AppScope 也按源语言集合建语言目录写 app_name

审的是：资源
触发（任一种）：
- 读到：Manifest 的 application 或启动 Activity 的 android:label 引用的字符串在 values-<语言> 有译名；写错的样子：AppScope/resources 下只有 base/element/string.json，没有对应语言目录的 app_name；或只在 entry 的语言目录写了 EntryAbility_label
适用范围：落地应用身份（app.json5 的 label、入口 Ability 的 label）且源端应用名有语言译名时
做法：
- 按源语言集合同时建 AppScope/resources/<语言>/element/string.json 写 app_name 译名，并在 entry/src/main/resources/<语言>/element/string.json 写入口 Ability label 译名
- 身份裁决只给出 base 显示名时只把它当 base 值，不当作省略语言变体的依据；拿不准就上报，不为「保持简单」收窄
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 应用级名称（系统设置里的应用名）只读 AppScope 资源，AppScope 缺该语言目录就显示 base 名，entry 有译名也替代不了：要单独建 AppScope 的语言目录（出处：卡里修好并验证过）
- app.json5 的 label：标识应用的名称，取值为字符串资源的索引，以支持多语言；不可缺省：应用名靠资源按语言解析（出处：app-configuration-file.md，配置文件标签（label））
- 入口 UIAbility 未设置 icon 或 label 时，系统返回 app.json5 中的 icon 或 label：入口 Ability label 和应用 label 是两处，各自要有语言译名（出处：layered-image.md，配置优先级和生成策略）
针对本应用要查的：
- 源端有哪些语言的应用名译名：源工程 res/ 下所有 values-<语言>/strings.xml 里 android:label 引用的字符串；列出有这个字符串的语言目录，得到 AppScope 和 entry 都要覆盖的语言集合及各自译名
未核实：「应用级名称只读 AppScope 资源」出自卡里修好后的观察；文档写的是编译时 AppScope 资源合入模块同路径资源目录，二者的关系没在知识库里核清
来源：1 张卡，1 个应用
- case-d720656a9811d5cdd419（Sokoban）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断、建议 2
