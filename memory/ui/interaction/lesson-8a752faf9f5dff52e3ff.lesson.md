# Compose combinedClickable 的长按自带系统触感：目标 LongPressGesture 不会振动，要在长按触发时显式调用一次长按触感

ID：`lesson-8a752faf9f5dff52e3ff` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 Compose combinedClickable(onLongClick = …) 的长按交互转写为 ArkUI LongPressGesture 或长按事件时

## 适用情境

源端条目用 combinedClickable(onLongClick = …) 处理长按，传 hapticFeedbackEnabled = true，或未传而所用 compose-foundation 版本签名中该参数默认为 true；长按回调里可能另有业务振动（如跳步时的重击感）；目标用 LongPressGesture 只回调业务逻辑。

## 例外与边界

- 源端显式写 hapticFeedbackEnabled = false
- 所用 compose-foundation 版本的 combinedClickable 签名里没有 hapticFeedbackEnabled 参数：不套用本条，先在该版本的长按实现里查有无系统触感调用再决定

## 原因

hapticFeedbackEnabled 为 true 的 combinedClickable 在识别长按时由框架执行一次系统长按触感，不在回调代码里；ArkUI 的 LongPressGesture 不附带振动。只迁回调会丢掉长按的确认手感，把它并进回调里的业务振动又会改变两种反馈的先后与强度。

## 做法

1. 先从依赖声明确认 compose-foundation 版本，在该版本的 combinedClickable 签名里确认有 hapticFeedbackEnabled 参数及其默认值（看依赖源码包或 IDE 跳转；例：foundation 1.11.1 的 Clickable.kt 默认 true，长按时调用 performHapticFeedback(HapticFeedbackType.LongPress)），源端未传时按默认值判断。
2. 在长按手势触发时显式调用一次触感：vibrator.startVibration({ type: 'preset', effectId, count: 1 }, { usage: 'touch' })，effectId 从 @ohos.vibrator.d.ts 的 HapticFeedback 预置效果（EFFECT_SOFT、EFFECT_HARD、EFFECT_SHARP 等，API 12 起）中选定一个并在决策记录写明；调用前用 vibrator.isSupportEffect 检查，不支持时不振动；声明 ohos.permission.VIBRATE。
3. 与回调里源端自带的业务振动分开调用，同一次长按只触发一次。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, recommendation:7
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
