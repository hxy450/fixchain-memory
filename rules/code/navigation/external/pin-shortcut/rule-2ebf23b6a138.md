# 源端 requestPinShortcut 固定快捷方式时，目标用 productViewManager 申请固定

审的是：代码
触发（任一种）：
- 读到：源端 ShortcutManager.isRequestPinShortcutSupported → requestPinShortcut 固定桌面快捷方式，删除对象时 disableShortcuts；写错的样子：目标的添加快捷方式入口只记 hilog 并弹「去添加服务卡片」一类的引导，移除链整体 no-op；文件头注释写「无三方应用 requestPinShortcut 公开 API」
适用范围：源端用 ShortcutManager 固定、禁用桌面快捷方式，目标是 HarmonyOS（AppGallery Kit，声明 @since 5.0.2(14)）时
做法：
- 固定：productViewManager.checkPinShortcutPermitted(context, shortcutId, want, labelResName, iconResName) 取到 CheckShortcutResult.tid，再 productViewManager.requestNewPinShortcut(context, tid)；源端 ShortcutInfo 的 id → shortcutId，Intent → want，短标签、图标 → 资源名
- 移除：对应源端 disableShortcuts 的地方，用 getPinShortcutInfos 找到已固定的快捷方式再 removePinShortcut
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- checkPinShortcutPermitted(context: common.UIAbilityContext, shortcutId: string, want: Want, labelResName: string, iconResName: string): Promise<CheckShortcutResult>：检查能否申请固定；label、icon 传资源键名（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.appgalleryservice.productViewManager.d.ts，productViewManager.checkPinShortcutPermitted）
- checkPinShortcutPermitted(context, shortcutId, want, label: string, foregroundIcon: string, backgroundIcon: string)：同族接口：另一个重载，label 传文字内容，前景、背景图标传沙箱路径（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.appgalleryservice.productViewManager.d.ts，productViewManager.checkPinShortcutPermitted）
- CheckShortcutResult.tid?: string：申请固定用的事务 ID，交给 requestNewPinShortcut（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.appgalleryservice.productViewManager.d.ts，CheckShortcutResult.tid）
- requestNewPinShortcut(context: common.UIAbilityContext, tid: string): Promise<void>；用户拒绝时抛 1006620007：真正发起固定（出处：鸿蒙 SDK 的 hms/ets/api/@hms.core.appgalleryservice.productViewManager.d.ts，productViewManager.requestNewPinShortcut）
- checkPinShortcutPermitted → requestNewPinShortcut 做出真实固定快捷方式，getPinShortcutInfos / removePinShortcut 实现移除：修好的做法（出处：卡里修好并验证过）
未核实：getPinShortcutInfos / removePinShortcut 在本机 SDK（API 23）的声明里搜不到，按卡写（卡里环境是 6.1.1(24)）
来源：1 张卡，1 个应用
- case-7f8dcb2d9341693d1225（omni-notes-hmos）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 诊断；取值 5 ← 诊断
