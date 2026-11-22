# Compose Switch 的 thumbContent（如选中时的勾选图标）等显式子内容，在目标原生开关没有对应参数时自绘承载，不假定 Toggle 会自动显示

## 何时使用

界面实现阶段（含公共组件抽取），把 M3 Switch 等带内容槽的源控件映射为 ArkUI Toggle 等原生控件时

## 适用情境

源端 Switch 传了 thumbContent = { if (checked) Icon(Icons.Rounded.Check) } 一类显式子内容；目标准备用 Toggle({ type: ToggleType.Switch })，写者认为原生开关打开时会自带勾选图标，或计划中的图标在落盘时被省略。

## 原因

源端显式传入的子内容是控件外观的一部分；目标原生控件只呈现自身参数能表达的外观，Switch 型 Toggle 没有滑块内容槽。未经核实就假定“原生也会显示”，图标会静默消失。

## 做法

1. 映射前对照目标控件的参数列表，确认源端每个内容槽（thumbContent、icon、leading/trailing 一类）都有承载位置；没有时自绘该控件（或用 Toggle 的 contentModifier（API 12 起）自定义内容区），图标用工程中已迁移的对应资源，按选中态显示。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕Toggle 只有 ToggleType.Button 时可以包含子组件，Switch 型不能放子组件
- 〔原因 / 做法第 1 步〕Switch 型 Toggle 的样式 SwitchStyle 只有 pointRadius、unselectedColor、pointColor、trackBorderRadius 四项，没有滑块内容或图标，开关打开时不会自动显示勾选图标
- 〔做法第 1 步〕Toggle.contentModifier（API 12 起）用 ContentModifier<ToggleConfiguration> 定制 Toggle 的内容区
