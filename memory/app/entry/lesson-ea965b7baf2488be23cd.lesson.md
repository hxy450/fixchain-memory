# 裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号

ID：`lesson-ea965b7baf2488be23cd` · 版本：1

[本主题](index.md)

## 何时使用

规格的横切能力裁定阶段（i18n、深色、大字体、无障碍）判断系统字号缩放是否迁移时；派发应用身份或应用外壳任务、落定 AppScope/app.json5 的 configuration 时

## 适用情境

源应用主体可能是固定 px 字号的 Canvas 自绘，但仍有系统 AlertDialog、Toast、菜单或 sp 单位文本；Activity 是否在 configChanges 声明 fontScale 决定字号变化时重建还是回调；目标 HarmonyOS 应用默认不跟随系统字号（nonFollowSystem），需在 AppScope 配置 configuration profile 才会跟随并下发配置变化。

## 原因

系统对话框等平台控件的 sp 文字随系统字号放大，Activity 还会因字号变化重建，这些都不需要应用写显式代码；以“没有 fontScale 处理代码”判为不适用，目标端就缺 configuration 声明，对话框文字不随系统字号变化，应用也收不到配置回调。应用身份步骤通常只覆盖名称、图标、版本与包名，configuration 不会被顺带写上。

## 做法

1. 逐项列出源端随系统字号缩放的文本来源（系统对话框、Toast、菜单、sp 文本），并读 Manifest configChanges；只有全部文本都是固定 px 自绘时才判为不适用。
2. 存在任一随系统字号缩放的文本时裁定迁移：AppScope/app.json5 增加 "configuration": "$profile:configuration"，profile 中 fontSizeScale 为 followSystem，fontSizeMaxScale 按源端系统字号上限取值（如 Android 14+ 的 200% 对应 "2"）；自绘的固定 px 字号保持不变。
3. 派发应用身份或应用外壳任务时，把 configuration 与 label、icon、版本号并列为核对项，确认引用的 profile 文件存在且取值符合决策。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-a824609ada4969e6d96c](../../../store/cases/case-a824609ada4969e6d96c/908019d8b78ca79b9ac18fb80f8f376c83afecb1b39477e21fbda7dc145035f5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`908019d8b78ca79b9ac18fb80f8f376c83afecb1b39477e21fbda7dc145035f5`
