# ShortcutManager 固定的桌面快捷方式

agent 会看到什么：读到源端 ShortcutManager 的 isRequestPinShortcutSupported、requestPinShortcut、disableShortcuts 和 ShortcutInfo；产物里添加、移除快捷方式的入口是 productViewManager 的申请固定，还是只有日志、引导弹窗和 no-op

## 规矩

- rule-2ebf23b6a138｜源端 requestPinShortcut 固定快捷方式时，目标用 productViewManager 申请固定｜读到：源端 ShortcutManager.isRequestPinShortcutSupported → requestPinShortcut 固定桌面快捷方式，删除对象时 disableShortcuts；写错：目标的添加快捷方式入口只记 hilog 并弹「去添加服务卡片」一类的引导，移除链整体 no-op；文件头注释写「无三方应用 requestPinShortcut 公开 API」
