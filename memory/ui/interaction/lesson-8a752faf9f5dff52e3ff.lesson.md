# Compose combinedClickable 的长按自带系统触感：目标 LongPressGesture 不会振动，要在长按触发时显式调用一次长按触感

ID：`lesson-8a752faf9f5dff52e3ff` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose combinedClickable(onLongClick = …) 的长按交互转写为 ArkUI LongPressGesture 或长按事件时

## 适用情境

源端条目用 combinedClickable(onLongClick = …) 处理长按，hapticFeedbackEnabled 为 true（未显式关闭）；长按回调里可能另有业务振动（如跳步时的重击感）；目标用 LongPressGesture 只回调业务逻辑。

## 例外与边界

- 源端显式写 hapticFeedbackEnabled = false

## 原因

Compose 识别长按时由框架执行一次系统长按触感，不在回调代码里；ArkUI 的 LongPressGesture 不附带振动。只迁回调会丢掉长按的确认手感，把它并进回调里的业务振动又会改变两种反馈的先后与强度。

## 做法

1. 在长按手势触发时显式调用一次系统长按触感（vibrator 预置效果，声明 ohos.permission.VIBRATE），与回调里源端自带的业务振动分开调用；多个组件都有这类长按时共用一个触感入口。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:7
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
