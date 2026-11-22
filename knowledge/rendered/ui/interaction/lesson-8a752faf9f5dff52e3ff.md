# Compose combinedClickable 的长按自带系统触感：目标 LongPressGesture 不会振动，要在长按触发时显式调用一次长按触感

## 何时使用

界面实现阶段，把 Compose combinedClickable(onLongClick = …) 的长按交互转写为 ArkUI LongPressGesture 或长按事件时

## 适用情境

源端条目用 combinedClickable(onLongClick = …) 处理长按，hapticFeedbackEnabled 为 true（未显式关闭）；长按回调里可能另有业务振动（如跳步时的重击感）；目标用 LongPressGesture 只回调业务逻辑。

## 例外与边界

- 源端显式写 hapticFeedbackEnabled = false

## 原因

Compose 识别长按时由框架执行一次系统长按触感，不在回调代码里；ArkUI 的 LongPressGesture 不附带振动。只迁回调会丢掉长按的确认手感，把它并进回调里的业务振动又会改变两种反馈的先后与强度。

## 做法

1. 在长按手势触发时显式调用一次系统长按触感（vibrator 预置效果，声明 ohos.permission.VIBRATE），振动属性的 usage 取 'touch'（受触摸振动开关管控，和源端系统触感一样随用户关掉触感而不振；不写时为 'unknown'，不受特定开关管控），与回调里源端自带的业务振动分开调用；多个组件都有这类长按时共用一个触感入口。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕vibrator.startVibration 需要 ohos.permission.VIBRATE 权限；振动属性里的 usage 决定场景类型，不同场景类型受系统振动开关管控的规则不同
- 〔做法第 1 步〕预置振动效果随设备不同，文档建议用前先以 isSupportEffect 或 isSupportEffectSync 查询；通用的 HapticFeedback 预置效果（API 12 起）有 'haptic.effect.soft'（轻柔）、'haptic.effect.hard'（坚定）、'haptic.effect.sharp'（警示）
