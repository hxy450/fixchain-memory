# 固定桌面快捷方式（requestPinShortcut）迁 AppGallery Kit productViewManager，不判“无三方 pin API”

ID：`lesson-fe5cf66672ce205ee0d7` · 版本：3 · 阶段：spec/execute · 主题：[app/entry](index.md)

概要：固定快捷方式用 productViewManager

信号：`requestPinShortcut`, `isRequestPinShortcutSupported`, `disableShortcuts`, `ShortcutManager`, `productViewManager`, `checkPinShortcutPermitted`, `requestNewPinShortcut`, `removePinShortcut`, `getPinShortcutInfos`, `1006620007`

## 何时使用

规格提取与实现阶段，迁移 ShortcutManager(Compat).requestPinShortcut、isRequestPinShortcutSupported、disableShortcuts 的固定与移除链时

## 适用情境

源端在条目上提供“固定到桌面”，删除条目时禁用或移除对应快捷方式；本地技能参考没有快捷方式章节，写者准备以“三方应用无 pin API”登记平台差异，或改成卡片引导等替代形态。

## 原因

固定快捷方式由 AppGallery Kit 的 productViewManager 提供，不在 module.json5 静态 shortcuts 或通用配置参考里；只查本地参考就判“无对等”，会把固定与移除链整条裁掉。

## 做法

1. 固定：productViewManager.checkPinShortcutPermitted(context, shortcutId, want, label, icon…) 取得结果中的 tid，再 requestNewPinShortcut(context, tid)；用户拒绝（1006620007）、已存在（1006620003）、数量已达上限（1006620004）按源端提示分支处理（SDK @hms.core.appgalleryservice.productViewManager.d.ts，5.0.2(14) 起）。
2. 移除：源端删除条目时禁用快捷方式的，用 getPinShortcutInfos 查已固定项并 removePinShortcut(context, shortcutId)（同一 d.ts，6.1.1(24) 起，801 表示设备不支持；快捷方式 ID 不存在 1006620010、用户拒绝删除 1006620013 也要分支处理）；工程最低 API 低于 24 时登记版本门槛与回退。
3. 快捷方式 want 中的 bundleName 与 uri 用运行时 bundleName 生成，不写字面量。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [shortcuts 元数据挂 Ability 下，不挂模块级](lesson-67118603fcc769a5edc9.lesson.md)（共享 1 张卡）
- [成本类降级按范围裁剪，闸门自动批准不算改判](../../process/unapproved-deviation/lesson-7827e0707780cb7546ee.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-7f8dcb2d9341693d1225](../../../../store/cases/case-7f8dcb2d9341693d1225/9bc002a9ae47b1515ae4f83a7641866747bdf2d6e5d4dae238785c21ea360875.json) · 结论：diagnosis, rec-a5247e93fa
  卡片版本：`9bc002a9ae47b1515ae4f83a7641866747bdf2d6e5d4dae238785c21ea360875`
