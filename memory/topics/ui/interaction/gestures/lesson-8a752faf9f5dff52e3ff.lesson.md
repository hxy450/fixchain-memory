# Compose combinedClickable 的长按自带系统触感：目标 LongPressGesture 不会振动，要在长按触发时显式调用一次长按触感

ID：`lesson-8a752faf9f5dff52e3ff` · 版本：2 · 阶段：execute · 主题：[ui/interaction/gestures](index.md)

概要：长按手势显式补系统长按触感

信号：`combinedClickable`, `onLongClick`, `hapticFeedbackEnabled`, `LongPressGesture`, `ohos.permission.VIBRATE`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [Float 运算比较按 float32 后用 ===](../../../arkts/runtime-semantics/lesson-0deb51172ebdd2e056a9.lesson.md)（共享 1 张卡）
- [短提示音保留混播与播放中 start 不重启语义](../../../app/playback/lesson-5475edc47af05c1c6a5b.lesson.md)（共享 1 张卡）
- [拒绝输入用 maxLength 或 onWillChange](../input/lesson-617ffbd840398cf95efc.lesson.md)（共享 1 张卡）
- [Slider steps 翻步长：区间/(steps+1)](../selectors/lesson-d715fa78ada2e79a5fd2.lesson.md)（共享 1 张卡）
- [底部面板按实际高度定档，显式关 showClose](../../dialog/frame/lesson-df1f691759f84ba9e688.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-e332c2cc4929f36c08c7](../../../../../store/cases/case-e332c2cc4929f36c08c7/99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301.json) · 结论：diagnosis, rec-700c57bac6
  卡片版本：`99990fa89f7be35793b896d170fd65a4dbe46e7c285f99e1fd707e9d8d36f301`
