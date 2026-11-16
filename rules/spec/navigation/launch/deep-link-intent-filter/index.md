# 清单里的深链 intent-filter

agent 会看到什么：读到 AndroidManifest 里带 VIEW / BROWSABLE、android:scheme / host / autoVerify 的 intent-filter，或导航模块里的深链路由器；规格里写深链的应用壳契约、skills.uris、domainVerify、锚点和验收拉起法

## 规矩

- rule-2c60a2c3fe7e｜源导航模块含深链路由器或 Manifest scheme 时，应用壳契约逐项收入深链入口或登记 skip｜读到：源导航模块里除路由表和底部 Tab 外，还有把 Uri 映射到路由的深链路由器类和深链 base URI 常量；AndroidManifest 的 Activity 带 VIEW/BROWSABLE 的 intent-filter（自定义 scheme 或 App Links 的 https 域名和 pathPrefix）；写错：契约或实施计划把应用壳概括成「路由表 + Tab」（Navigation + NavPathStack + Tabs + pageMap），复杂度记为 simple，源码锚点里没有深链路由器，也没写深链的目标符号；决策台账里又没有深链的 skip
- rule-54b71380035d｜规格写深链映射时，同时写 module.json5 skills.uris 和 want/newWant 解析｜读到：安卓清单里启动 Activity 有深链 intent-filter（VIEW + BROWSABLE，scheme / host / path，如 http/https、固定 host）；清单或 inventory 里有外部深链条目；写错：规格里深链只写了运行时一半（「启动后解析 URL」「UIAbility want/newWant listener + NavPathStack 路径解析」「skills 匹配 + onNewWant 等价」），没点名 module.json5 里 Ability 的 skills（actions、entities、uris 的 scheme/host/path）具体条目
- rule-3de995560318｜深链规格的 anchors 含 manifest 的 intent-filter，逐项列 scheme 和 host｜读到：AndroidManifest 的 <intent-filter android:autoVerify="true"> 含 VIEW / BROWSABLE 和多个 <data android:scheme>（如 https 与 http）、android:host；写错：深链规格的 anchors 不含 AndroidManifest.xml，uri 域只写 https 或自拟 scheme，漏掉 manifest 里的 http
- rule-1abbc827c687｜决策写「App Linking 承载」时，台账的替代方案和静态 AC 点名 domainVerify: true｜读到：源 intent-filter 带 android:autoVerify="true"；决策写「深链以 https App Linking 承载」；写错：台账的提议替代、技术必做项和静态 AC 只写 skills.uris 双声明，没有点名 "domainVerify": true
- rule-05e54fbd8ac9｜深链验收条目写隐式 Want 的拉起法，不用 aa start -b/-a 显式拉起｜读到：验收条目以清单深链为来源，要求外部 URL 打开对应页面；写错：验收条目或验收步骤里深链用例写成 aa start -b <bundleName> -a <abilityName> -U <url> 显式拉起
