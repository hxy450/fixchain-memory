# ACTION_SEND / ACTION_VIEW 的映射行写明源端隐式授予的 URI 读权限

审的是：规格
触发（任一种）：
- 读到：源端 Intent.ACTION_SEND 带 EXTRA_STREAM，或 ACTION_VIEW 打开媒体 URI，没写显式授权标志；写错的样子：映射行只写「startAbility sendData + image/jpeg + EXTRA_STREAM uri」，没写 URI 读授权
适用范围：规格提取时写分享、外部查看这类 Intent 到 Want 的映射行
做法：
- 映射行写明：源端由系统隐式授予接收方 URI 读权限，目标 Want 要加 wantConstant.Flags.FLAG_AUTH_READ_URI_PERMISSION
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- ACTION_SEND 带 EXTRA_STREAM 时，框架把它迁入 ClipData 并 addFlags(FLAG_GRANT_READ_URI_PERMISSION)：源码里看不到授权标志，授权是框架隐式加的（出处：android.content.Intent#migrateExtraStreamToClipData）
- FLAG_AUTH_READ_URI_PERMISSION = 0x00000001：目标端对应的读授权标志（出处：鸿蒙 SDK 的 ets/api/@ohos.app.ability.wantConstant.d.ts，wantConstant.Flags.FLAG_AUTH_READ_URI_PERMISSION）
未核实：规格作者写映射行前收到了哪些材料，卡里没有追到
来源：1 张卡，1 个应用
- case-3d6568f13ae09eb5090d（opencamera-hmos）：做法第 1 步 ← 建议 3
