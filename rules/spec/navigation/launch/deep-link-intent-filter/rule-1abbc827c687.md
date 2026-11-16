# 决策写「App Linking 承载」时，台账的替代方案和静态 AC 点名 domainVerify: true

审的是：规格
触发（任一种）：
- 读到：源 intent-filter 带 android:autoVerify="true"；决策写「深链以 https App Linking 承载」；写错的样子：台账的提议替代、技术必做项和静态 AC 只写 skills.uris 双声明，没有点名 "domainVerify": true
适用范围：规格与决策台账里为安卓 App Links 深链写替代方案、技术必做项和验收条目时
做法：
- 替代方案、技术必做项和静态 AC 各写一句具体配置项：「承载 https 的 browsable skill 声明 "domainVerify": true」，不只写 uris 双声明
- AC 的判定写成逐项对：action→actions、BROWSABLE→entities、data→uris、autoVerify→domainVerify，不只数 uris 条数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- domainVerify：布尔值，可缺省，缺省值为 false：AC 不点名时实现按缺省不写，就没有域名校验（出处：module-configuration-file.md，skills标签）
- App Linking 在 Deep Linking 基础上增加了域名校验环节：「App Linking 承载」落到配置上就是 domainVerify: true（出处：app-linking-startup.md，实现原理）
来源：1 张卡，1 个应用
- case-45402f380d6acbb30aa7（2048）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 2
