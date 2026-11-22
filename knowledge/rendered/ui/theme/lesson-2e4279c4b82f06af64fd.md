# “页面零硬编码色值”只禁止字面色值，不禁止用 $r 引用语义色

## 何时使用

规格提取阶段书写颜色约束，或页面实现阶段解读规格里的颜色约束时

## 适用情境

规格或功能说明写有“页面代码零硬编码色值”“深浅色由资源限定词目录负责”等全局约束，而具体控件仍需要与源端一致的颜色。 也包括源端由应用内设置选择深浅档或多套调色板（经 MaterialTheme(colorScheme = …) 下发给所有页面），目标的色板令牌放在稍后建立的可观察主题对象里，而 color.json 只有一套 base/dark 资源色。

## 例外与边界

- 源端在多套调色板间切换，或应用内深浅档只保存在主题对象里、不经 ApplicationContext.setColorMode 应用时，页面主题色不以 $r 满足本条，改按第 1 步后半句读主题对象的色板令牌

## 原因

“零硬编码”的目的是把色值集中在 base/dark 资源里切换，$r('app.color.x') 引用恰好满足它。把它读成“不得设置颜色属性”，控件就退回平台默认色。来源中实现者已注意到按钮默认蓝与源端紫不同，却因这条约束放弃设置颜色。

## 做法

1. 主题只随系统深浅（或由 ApplicationContext.setColorMode 统一应用）且只有一套色板时，规格写这类约束时同时写明“颜色一律用 $r('app.color.<语义名>') 引用已迁移资源”，并在需要颜色的控件行给出具体资源名。源端在多套色板间切换，或应用内深浅档只保存在主题对象里时，$r 色键只有一套 base/dark 值、跟不上应用内切换：“零硬编码”改由可观察主题对象的色板令牌满足，页面主题色在渲染期读主题对象（见 lesson-7b19b801e0f21481d1d6），$r 只留给与色板无关的颜色（遮罩、启动窗等）。
2. 实现时遇到该约束，只避免 '#RRGGBB' 等字面色值，按源端语义把 backgroundColor、fontColor 等属性设为资源引用。应用内切换色板或深浅档时，这些属性设为主题对象的色板令牌。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 com.google.android.material:material 1.12.0、1.14.0。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕Button 没设置 buttonStyle 时取 ButtonStyleMode.EMPHASIZED，系统按样式自动给出强调背景色和文字色；backgroundColor、fontColor、role 也能设置颜色，实际效果以最后一次设置为准
- 〔原因〕ButtonOptions.type 不设置时，API 18 及之后默认 ButtonType.ROUNDED_RECTANGLE，API 18 之前默认 ButtonType.Capsule
- 〔原因 / 做法第 1 步〕material 包的 Widget.MaterialComponents.Button：backgroundTint 为 mtrl_btn_bg_color_selector（启用态 ?attr/colorPrimary，否则 12% 透明度的 ?attr/colorOnSurface），android:textColor 为 mtrl_btn_text_color_selector（默认项 ?attr/colorOnPrimary）（应用主题和控件没有另设 backgroundTint、textColor 时）
- 〔适用情境 / 做法第 1 步〕颜色模式限定词只有 dark（深色）和 light（浅色）两种取值，表示设备的颜色模式；dark 目录里的同名颜色资源在深色模式下替代 base 的值
