# 裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境〕AppScope/app.json5 不写 configuration 时，应用字体大小按不跟随系统（nonFollowSystem）处理：不随系统字号缩放，应用也无法通过环境变量订阅感知系统字号的变化；要跟随，须让 configuration 指向 AppScope/resources/base/profile 下的配置文件并把 fontSizeScale 设为 followSystem。〔成立范围：对象：Stage 模型应用 app.json5 的 configuration 标签及其 profile。条件：配成 followSystem 后也只有按 fp 指定的字号随系统缩放（Text 的 fontSize 传 number 时按 fp），按 vp、px 写的字号不变。依据是文档说明。最常见的不成立情形：应用调用了 ApplicationContext.setFontSizeScale，此时即使配置 followSystem 也不再跟随系统。〕
- 〔做法第 2 步〕fontSizeMaxScale 只接受 1、1.15、1.3、1.45、1.75、2、3.2，缺省为 3.2；它是跟随系统时的放大上限，系统倍数超过它时按它封顶（上限 1.75、系统 2 倍时 10fp 文字显示为 17.5fp）；fontSizeScale 为 nonFollowSystem 时不生效。〔成立范围：对象：configuration profile 中的 fontSizeMaxScale（字符串）。条件：Text 等组件自己设了 maxFontScale 时，实际倍数还受组件的上限约束。依据是文档说明；填表外的值时系统怎样处理文档没写。最常见的不成立情形：fontSizeScale 没写或为 nonFollowSystem，上限写什么都不起作用。〕
- 〔做法第 2 步〕调用 ApplicationContext.setFontSizeScale 设置应用字体大小后，应用字体不再跟随系统变化，也不再支持订阅系统字体大小的变化。〔成立范围：对象：ApplicationContext.setFontSizeScale（只能在主线程调用）。条件：与 configuration 的 followSystem 同时存在时以接口设置的倍数为准，但设的值超过 fontSizeMaxScale 时实际按 fontSizeMaxScale 生效。依据是文档说明。最常见的不成立情形：应用从不调用 setFontSizeScale，是否跟随只由 configuration 决定。〕
