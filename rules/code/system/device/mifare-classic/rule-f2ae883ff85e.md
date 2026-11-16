# 源全局当前标签是 android.nfc.Tag 时，目标存 TagInfo，不收窄成 MifareClassicTag

审的是：代码
触发（任一种）：
- 读到：全局当前标签字段类型是 android.nfc.Tag，setTag 对任何技术的卡都赋值，之后才判断是否支持 MIFARE Classic；写错的样子：目标全局状态把当前标签声明成 tag.MifareClassicTag，非 MIFARE Classic 卡写入 null，在场判断写成 `!== null`
适用范围：迁移保存当前 NFC 标签的全局状态时
做法：
- 全局当前标签存回调拿到的 tag.TagInfo（任意技术），在场判断按这个 TagInfo 是否为空；需要 MIFARE Classic 连接时再 tag.getMifareClassic(tagInfo) 取出另存
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- export interface TagInfo { uid: number[]; technology: number[]; … }：任意技术的标签信息，technology 列出支持的技术（出处：鸿蒙 SDK 的 ets/api/@ohos.nfc.tag.d.ts，tag.TagInfo）
- function getMifareClassic(tagInfo: TagInfo): MifareClassicTag：从 TagInfo 取 MIFARE Classic 连接对象（出处：鸿蒙 SDK 的 ets/api/@ohos.nfc.tag.d.ts，tag.getMifareClassic）
- 在场判断改按最近一次的 TagInfo 后，非 MIFARE Classic 卡也能显示和预填 UID：修复后保留的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-3735da03c6e544339df6（MifareClassicTool）：做法第 1 步 ← 诊断；取值 3 ← 诊断
