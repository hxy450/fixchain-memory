# 清单 TECH_DISCOVERED 贴卡入口和启停它的开关分两行映射，入口对到 TAG_FOUND skill

审的是：规格
触发（任一种）：
- 读到：AndroidManifest 里 activity 或 activity-alias 的 intent-filter 带 android.nfc.action.TECH_DISCOVERED，meta-data 指向 tech-list 资源；偏好里用 PackageManager.setComponentEnabledSetting 启停这个 alias；写错的样子：映射基线把 TECH_DISCOVERED 入口写成「无对等 → 应用内开关模拟」并和 setComponentEnabledSetting 并成一个决策，或写「贴卡以 tag 回调事件替代 ACTION_TECH_DISCOVERED Intent」；规格里没有 skill 声明和 want 解析；HARD-DIV 行没写查证依据
适用范围：规格提取时映射安卓清单里声明的 NFC 系统派发入口及其运行时启停开关
做法：
- 系统派发入口单独一行：映射为 module.json5 skills 的 actions 含 "ohos.nfc.tag.action.TAG_FOUND"、uris 为 { "type": "tag-tech/<源 tech-list 里的技术>" }，入口 Ability 在 onCreate / onNewWant 里用 tag.getTagInfo(want) 取 TagInfo
- 运行时启停开关另起一行：第三方不能运行时启停 skill，只有这一行记为平台差异
- 写「无对等 / HARD-DIV」时在映射行写明查过的目标平台 NFC 与 skills 文档或 SDK；「不能动态禁用」不推出「整条入口无对等」
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- actions 必须包含 "ohos.nfc.tag.action.TAG_FOUND"；uris 的 type 前缀必须是 "tag-tech/"，后接 NfcA/NfcB/NfcF/NfcV/IsoDep/Ndef/MifareClassic/MifareUL/NdefFormatable 之一：鸿蒙后台读卡（系统派发拉起）的静态声明（出处：nfc-tag-access-guide.md，后台读取标签）
- function getTagInfo(want: Want): TagInfo：从拉起或送达的 want 里取标签（出处：鸿蒙 SDK 的 ets/api/@ohos.nfc.tag.d.ts，tag.getTagInfo）
- TECH_DISCOVERED 的 meta-data 指向含一个或多个 tech-list 的 XML，tech 写技术类全名，如 android.nfc.tech.NfcA：源端入口过滤的技术从这里读（出处：android.nfc.NfcAdapter#ACTION_TECH_DISCOVERED）
- setComponentEnabledSetting：设置包内组件（activity、receiver、service、provider）的启用状态：源开关只启停组件，不涉及前台派发（出处：android.content.pm.PackageManager#setComponentEnabledSetting）
针对本应用要查的：
- 源端入口过滤的 NFC 技术：源工程 AndroidManifest 里 TECH_DISCOVERED 的 meta-data 指向的 res/xml 文件；读各 <tech-list> 里的 <tech>，android.nfc.tech.<技术> 去掉包名写成 tag-tech/<技术>
未核实：卡里的修复出自 API 24（6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-d923c5dbfc1e66ce5f8b（MifareClassicTool）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2
