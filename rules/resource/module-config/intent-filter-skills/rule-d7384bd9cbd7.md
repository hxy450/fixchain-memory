# 深链 intent-filter 要映射成 module.json5 的 skills，不只解析 want.uri

审的是：资源
触发（任一种）：
- 读到：Activity 的 <intent-filter> 带 VIEW 和 <data android:scheme/android:host/android:pathPrefix>；写错的样子：该 UIAbility 的 skills 只有 entity.system.home 那一项，没有带 viewData 和 uris 的 skill，代码里却在解析 want.uri
- 读到：源码里有 `scheme://host` 形式的自定义 scheme 深链常量；写错的样子：入口 UIAbility 的 skills 只有 entity.system.home，没有 uris
适用范围：安卓外部深链（https/http 或自定义 scheme）迁成 UIAbility 时，module.json5 里它的 skills
做法：
- skills 里另建一个 skill（不并进 entity.system.home 那项）："actions": ["ohos.want.action.viewData"]，"entities": ["entity.system.browsable"]，"uris": [...]
- 源端每个 scheme+host 组合写一条 uris：{"scheme": <android:scheme>, "host": <android:host>, "pathStartWith": <android:pathPrefix>}，https、http 各一条
- 和 onCreate/onNewWant 读 want.uri 的解析同一步完成，写完逐条对照源端每个 intent-filter 有没有匹配的 uris
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- {"actions": ["ohos.want.action.viewData"], "entities": ["entity.system.browsable"], "uris": [{"scheme": "https", "host": <host>, "pathStartWith": "/"}, {"scheme": "http", "host": <host>, "pathStartWith": "/"}]}：源端 VIEW + DEFAULT + BROWSABLE、scheme https/http、pathPrefix "/" 的 intent-filter 对应的 skill；补上后外部链接才路由到该 Ability（出处：卡里修好并验证过）
- 补上 actions viewData + uris {scheme, host} 的独立 skill（含源端自定义 scheme://host）后，外部深链能拉起并路由，修复保留：注册 scheme 是自定义 scheme 深链能拉起入口的前提（出处：卡里修好并验证过）
- 默认的入口 skill（entity.system.home / ohos.want.action.home）里不能配跳转链接，要另建独立的 skill 对象；多个跳转场景各建一个：深链那一项要新增，不要把 viewData、browsable、uris 塞进 home 那一项（出处：deep-linking-startup.md，配置module.json5文件）
- "actions": ["ohos.want.action.viewData"]：深链 skill 的 actions 不能为空，为空会匹配失败（出处：deep-linking-startup.md，配置module.json5文件）
- uris 的 scheme 必填（只配 type 时除外），host 只在配了 scheme 时生效；port、path | pathStartWith | pathRegex（三选一：全匹配、前缀、正则）只有 scheme 和 host 都配置时才生效：源端 data 的 scheme、host、port、path、pathPrefix 分别写到 scheme、host、port、path、pathStartWith；android:pathPattern 是简单通配符，转 pathRegex 时要改写成正则（出处：module-configuration-file.md，skills标签（uris标签说明）；Android SDK 平台资源 data/res/values/attrs_manifest.xml，AndroidManifestData 的 path / pathPrefix / pathPattern（按应用的 compileSdk 取对应平台））
- uris 里的字符串标签不支持 $string 资源索引：scheme、host、pathStartWith 写字面量（出处：module-configuration-file.md，skills标签（表8 uris标签说明））
- actions 含 "ohos.want.action.viewData"、entities 含 "entity.system.browsable"、uris 含 scheme 为 https 且 host 为域名的元素：文档对网址类链接接收方的 skills 要求，和 https 深链那张卡的写法一致（出处：app-linking-startup.md，声明应用关联的网站域名）
- Deep Linking 的 scheme 可以自定义，但不能以 ohos 开头，不建议用 https、http、file 等系统保留值：自拟 scheme 时的限制，保留 scheme 可能拉起系统默认应用；https 域名链接按上一条 App Linking 的写法（出处：deep-linking-startup.md，配置module.json5文件）
针对本应用要查的：
- 要注册的 scheme、host、端口和路径：源工程 AndroidManifest.xml 里该 Activity 下深链 <intent-filter> 的 <data> 元素；源码里 scheme://host 形式的深链 base URI 常量；每个 scheme 和 host 的组合写成一条 uris，android:pathPrefix 的值原样写进 pathStartWith；android:port、android:path / pathPattern 也逐条读出写到对应字段
未核实：case-6bc0c044e9bb2281aa01 的行为出自 HarmonyOS 6.0.1(21)，case-6b58da0df30e3479800e 的出自 target SDK 26.0.0，本机按 API 23 的声明和 docs f41b9345 核对；case-ff125779dc6d250b6a4a 只写了补 uris，没写是否单独成一个 skill 对象、actions 和 entities 怎么写；case-6b58da0df30e3479800e 写了独立 skill 和 viewData，没写 entities；这几点出自文档和 https 深链那张卡
来源：3 张卡，3 个应用
- case-6b58da0df30e3479800e（Countdate）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1、建议 3；取值 2 ← 诊断
- case-6bc0c044e9bb2281aa01（Cofi）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 建议 1；取值 1 ← 诊断
- case-ff125779dc6d250b6a4a（Meshtastic）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断；做法第 3 步 ← 建议 2、诊断；取值 2 ← 诊断
