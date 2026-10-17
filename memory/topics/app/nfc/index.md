# app/nfc

NFC 读卡：能力三态前置检查、贴卡拉起的 skills 声明、按 UIAbility 前台派发与页面仿真

[上一级](../index.md)

## 本级经验

- [NFC 前台派发按 Ability 注册，页面用可见页表](lesson-a4ee90eabe3eef99ddbe.lesson.md) · 阶段：execute · 信号：enableForegroundDispatch, onNewIntent, tag.registerForegroundDispatch, onForeground
- [NFC 前置检查分不支持/关闭/可用三态，不折成布尔](lesson-5a140e45ecb578dd61ed.lesson.md) · 阶段：spec/execute · 信号：NfcAdapter, isEnabled(), Settings.ACTION_NFC_SETTINGS, canIUse
- [贴卡拉起声明 TAG_FOUND，开关只管系统派发](lesson-89368bd540176a43d4a2.lesson.md) · 阶段：spec/execute · 信号：android.nfc.action.TECH_DISCOVERED, tech-list, activity-alias, setComponentEnabledSetting
