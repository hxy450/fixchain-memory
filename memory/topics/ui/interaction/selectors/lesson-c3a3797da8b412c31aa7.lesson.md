# Compose Switch 的 thumbContent（如选中时的勾选图标）等显式子内容，在目标原生开关没有对应参数时自绘承载，不假定 Toggle 会自动显示

ID：`lesson-c3a3797da8b412c31aa7` · 版本：2 · 阶段：execute · 主题：[ui/interaction/selectors](index.md)

概要：Switch thumbContent 无对应参数时自绘

信号：`thumbContent`, `Switch`, `Toggle`, `ToggleType.Switch`, `contentModifier`, `Icons.Rounded.Check`

## 何时使用

界面实现阶段（含公共组件抽取），把 M3 Switch 等带内容槽的源控件映射为 ArkUI Toggle 等原生控件时

## 适用情境

源端 Switch 传了 thumbContent = { if (checked) Icon(Icons.Rounded.Check) } 一类显式子内容；目标准备用 Toggle({ type: ToggleType.Switch })，写者认为原生开关打开时会自带勾选图标，或计划中的图标在落盘时被省略。

## 原因

源端显式传入的子内容是控件外观的一部分；目标原生控件只呈现自身参数能表达的外观，Switch 型 Toggle 没有滑块内容槽。未经核实就假定“原生也会显示”，图标会静默消失。

## 做法

1. 映射前对照目标控件的参数列表，确认源端每个内容槽（thumbContent、icon、leading/trailing 一类）都有承载位置；没有时自绘该控件（或在当前 SDK 支持时用 Toggle 的 contentModifier 自定义内容），图标用工程中已迁移的对应资源，按选中态显示。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [单一 SnackbarHost 用唯一宿主按源排队定时长](../../state/feedback/lesson-187c725b1bb9d8d1bf4d.lesson.md)（共享 1 张卡）
- [编译修复只改报错行，不删功能或换异义替代](../../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [宿主 onBackPressed 自顶向下关闭页内覆盖层](../../navigation/back-stack/lesson-396d54479492828eeea3.lesson.md)（共享 1 张卡）
- [remember 按首次或 key 变才求值](../../state/lifecycle/lesson-3b4a96141329db62a6af.lesson.md)（共享 1 张卡）
- [缺枚举的 FontWeight 写数值，不换近名](../../text/typography/lesson-605038b091e03c26c005.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, rec-58fd798e29
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
