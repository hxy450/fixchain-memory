# TECH_DISCOVERED 入口要在 module.json5 声明 TAG_FOUND skill

审的是：资源
触发（任一种）：
- 读到：<intent-filter> 里 <action android:name="android.nfc.action.TECH_DISCOVERED"/>，同名 <meta-data> 指向的 tech-list 列着 android.nfc.tech.NfcA 等；写错的样子：module.json5 的 skills 只有 entity.system.home / ohos.want.action.home，只在 requestPermissions 追加了 ohos.permission.NFC_TAG
适用范围：源端清单声明了 NFC TECH_DISCOVERED 系统派发入口、迁成 module.json5 时
做法：
- 入口 Ability 的 skills 里加："actions": ["ohos.nfc.tag.action.TAG_FOUND"]，"uris": 源 tech-list 里每个 android.nfc.tech.<技术> 一项 { "type": "tag-tech/<技术>" }
- requestPermissions 里声明 { "name": "ohos.permission.NFC_TAG" }
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- "actions" 必须包含 "ohos.nfc.tag.action.TAG_FOUND"，不能更改：系统贴卡拉起要的 action（出处：nfc-tag-access-guide.md，后台读取标签）
- "uris" 的 "type" 前缀必须是 "tag-tech/"，后接 NfcA/NfcB/NfcF/NfcV/IsoDep/Ndef/MifareClassic/MifareUL/NdefFormatable 之一，多个 type 分行写：技术名要和这个列表一致；安卓的 android.nfc.tech.MifareUltralight 在这里写作 MifareUL（出处：nfc-tag-access-guide.md，后台读取标签；android.nfc.tech.MifareUltralight）
- 技术类型的描述字符必须完整匹配并区分大小写：写错大小写会解析失败（出处：nfc-tag-access-guide.md，NFC标签前台读写或后台读写的选择）
- 权限名必须是 "ohos.permission.NFC_TAG"：requestPermissions 里的写法（出处：nfc-tag-access-guide.md，后台读取标签）
针对本应用要查的：
- 源端入口过滤的 NFC 技术：源工程 AndroidManifest 里 TECH_DISCOVERED 的 meta-data 指向的 res/xml 文件；读各 <tech-list> 里的 <tech> 类全名，去掉 android.nfc.tech. 前缀作为 tag-tech/ 后面的技术名
未核实：卡里的修复出自 API 24（6.1.1），本机文档副本未标 API 版本
来源：1 张卡，1 个应用
- case-d923c5dbfc1e66ce5f8b（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断
