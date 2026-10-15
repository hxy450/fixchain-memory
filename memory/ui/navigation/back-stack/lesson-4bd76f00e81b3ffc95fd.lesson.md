# 外部入口以 CLEAR_TOP 拉起已在栈中的主 Activity 时，目标在 onNewWant 先清 NavPathStack 再落 tab

ID：`lesson-4bd76f00e81b3ffc95fd` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段描述桌面卡片、通知、快捷方式等外部入口的返回栈后果时；入口实现阶段在 EntryAbility.onNewWant 与入口页处理热启动外部 Want 时

## 适用情境

源端外部入口（桌面卡片、通知等）用带 FLAG_ACTIVITY_CLEAR_TOP|NEW_TASK 的显式 Intent 拉起主 Activity 并落到某个 tab；目标为单例 UIAbility + 单 Navigation，热启动时只回调 onNewWant，NavPathStack 里可能压着详情页；规格可能只写“拉起后落到某 tab”。

## 例外与边界

- Intent 不带 CLEAR_TOP 时，按源端 flag 与 launchMode 推出的栈决定是否保留已压的页面

## 原因

CLEAR_TOP 决定热启动时清掉压在目标 Activity 之上的页面；它只在目标页已在栈中时生效，冷启动时看不出来。规格只写“落到某 tab”时，目标 onNewWant 切 tab 却不清栈，深链落在旧详情页下面，返回又回到该详情页。

## 做法

1. 规格对每个 Intent flag 写出可观察后果或登记豁免，不只留字面：CLEAR_TOP|NEW_TASK 写成“应用在前台且压着详情页时，外部入口热启动先清空详情栈再落到目标 tab”。
2. onNewWant 落 tab 前按源端 flag 决定是否 navPathStack.clear()；冷启动与热启动的入口解析走同一处理。

## 可选检查

- 有设备时进入某详情页后从外部入口拉起，应落在目标 tab，返回不再出现该详情页。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-902870a7e6081dd22611](../../../../store/cases/case-902870a7e6081dd22611/284e035e888445e55163417d78c23c597a0f406cdc57c5ccf6b9fdb55daa7fcc.json) · 结论：diagnosis, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`284e035e888445e55163417d78c23c597a0f406cdc57c5ccf6b9fdb55daa7fcc`
