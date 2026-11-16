# 有系统贴卡入口时，onCreate 和 onNewWant 里用 tag.getTagInfo 取标签

审的是：代码
触发（任一种）：
- 读到：清单 intent-filter 带 android.nfc.action.TECH_DISCOVERED，被拉起的 Activity 是 singleTop，贴卡时以带 tag 的 intent 拉起或送达；写错的样子：EntryAbility 的 onCreate 不读 want 里的 TagInfo，也没有 onNewWant；只在页面里做 tag.on / registerForegroundDispatch 前台注册
适用范围：module.json5 声明了 TAG_FOUND skill 的入口 UIAbility
做法：
- onCreate(want, launchParam) 和 onNewWant(want, launchParam) 里都调 tag.getTagInfo(want)（放在 try/catch 里），取到的 TagInfo 交给处理贴卡的页面
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- function getTagInfo(want: Want): TagInfo：从拉起或送达的 want 里取标签（出处：鸿蒙 SDK 的 ets/api/@ohos.nfc.tag.d.ts，tag.getTagInfo）
- onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void：应用已在运行时贴卡，want 从这里送达（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.UIAbility.d.ts，UIAbility.onNewWant）
- 文档示例在 onCreate 里 try { tagInfo = tag.getTagInfo(want); } catch … 再检查 tagInfo、uid、technology：取标签的写法（出处：nfc-tag-access-guide.md，后台读取标签）
未核实：卡里的修复出自 API 24（6.1.1），本机声明是 API 23
来源：1 张卡，1 个应用
- case-d923c5dbfc1e66ce5f8b（MifareClassicTool）：做法第 1 步 ← 建议 1、诊断
