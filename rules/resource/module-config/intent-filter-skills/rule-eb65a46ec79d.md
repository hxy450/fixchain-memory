# module.json5 skills 按源 intent-filter 逐条登记，各 action 不合并

审的是：资源
触发（任一种）：
- 读到：AndroidManifest.xml 的 <intent-filter> 有 android.intent.action.SEARCH、SEND、SEND_MULTIPLE、VIEW + <data android:scheme=…>；写错的样子：module.json5 的 skills 只有一条 ohos.want.action.sendData（uris 只有 "type": "*/*"），没有 ohos.want.action.search、ohos.want.action.sendMultipleData，分享项没有 utd、maxFileSupported
适用范围：源入口 Activity 有多条 intent-filter、目标是 UIAbility 的 module.json5 skills
做法：
- 一条 intent-filter 一条 skill：SEARCH → ohos.want.action.search；SEND → ohos.want.action.sendData、SEND_MULTIPLE → ohos.want.action.sendMultipleData，二者 entities 写 entity.system.default，uris 写 scheme file、utd general.object、maxFileSupported
- VIEW + scheme 的每条 → actions ["ohos.want.action.viewData"]，uris 写源端的 scheme（有 host 的照写 host）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ohos.want.action.search；ohos.want.action.sendData；ohos.want.action.sendMultipleData；ohos.want.action.viewData：四个 action 的字符串（出处：js-apis-ability-wantConstant.md，Action）
- utd：适用于分享等场景的标准化数据类型；maxFileSupported：一次能接收的最大文件数，需与 utd 配合，缺省 0：分享项 uris 的两个字段（出处：module-configuration-file.md，skills标签的 uris）
- 返修逐条登记 search、sendData（scheme file / utd general.object / maxFileSupported）、sendMultipleData 和两条 viewData 后，各入口可受理：修好后的配置（出处：卡里修好并验证过）
未核实：卡里没写 maxFileSupported 取多少；卡里的行为出自 HarmonyOS 6.1.1(24)，本机文档副本为 docs f41b9345
来源：1 张卡，1 个应用
- case-7b71b27d8bbbbbd73267（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 3 ← 诊断
