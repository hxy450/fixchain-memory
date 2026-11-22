# 裁定“大字体”是否迁移时看源端是否有随系统字号缩放的文本，而不是有无 fontScale 代码；需要时在 AppScope 声明 configuration 跟随系统字号

## 何时使用

规格的横切能力裁定阶段（i18n、深色、大字体、无障碍）判断系统字号缩放是否迁移时；派发应用身份或应用外壳任务、落定 AppScope/app.json5 的 configuration 时

## 适用情境

源应用主体可能是固定 px 字号的 Canvas 自绘，但仍有系统 AlertDialog、Toast、菜单或 sp 单位文本；Activity 是否在 configChanges 声明 fontScale 决定字号变化时重建还是回调；目标 HarmonyOS 应用默认不跟随系统字号（nonFollowSystem），需在 AppScope 配置 configuration profile 才会跟随并下发配置变化。改成跟随后，目标里不带单位的 fontSize（按 fp 计）和写成 fp 的字号都会随系统字号放大；源端用 px 或 dp 固定的字号（自绘文字、固定尺寸标签），在目标要写成 px 或 vp 才保持不随系统字号变化，不要随这次改动一起变成 fp。

## 原因

系统对话框等平台控件的 sp 文字随系统字号放大，Activity 还会因字号变化重建，这些都不需要应用写显式代码；以“没有 fontScale 处理代码”判为不适用，目标端就缺 configuration 声明，对话框文字不随系统字号变化，应用也收不到配置回调。应用身份步骤通常只覆盖名称、图标、版本与包名，configuration 不会被顺带写上。

## 做法

1. 逐项列出源端随系统字号缩放的文本来源（系统对话框、Toast、菜单、sp 文本），并读 Manifest configChanges；只有全部文本都是固定 px 自绘时才判为不适用。
2. 存在任一随系统字号缩放的文本时裁定迁移：AppScope/app.json5 增加 "configuration": "$profile:configuration"，profile 中 fontSizeScale 为 followSystem，fontSizeMaxScale 按源端系统字号上限取值（如 Android 14+ 的 200% 对应 "2"）；自绘的固定 px 字号保持不变。
3. 派发应用身份或应用外壳任务时，把 configuration 与 label、icon、版本号并列为核对项，确认引用的 profile 文件存在且取值符合决策。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 2、3 步〕app.json5 用 "configuration": "$profile:configuration" 引用 AppScope/resources/base/profile 下的配置文件，文件名可自定义，但要和 configuration 标签指定的资源名对应
- 〔适用情境 / 原因〕应用没有配置 configuration 的 fontSizeScale 时取缺省值 nonFollowSystem，应用字体大小不跟随系统；设为 followSystem 才跟随
- 〔做法第 2 步〕fontSizeMaxScale 是跟随系统后应用字体的最大放大倍数，只支持 1、1.15、1.3、1.45、1.75、2、3.2，缺省 3.2；系统放大倍数超过它时按它封顶（如配 1.75、系统调到 2 倍时 10fp 的字显示为 17.5fp）；fontSizeScale 为 nonFollowSystem 时该项不生效
- 〔原因 / 做法第 2 步〕设备上 AppScope 配置 fontSizeScale 为 followSystem、fontSizeMaxScale 为 "2" 时，修改系统字号后应用收到配置变化回调并重建，系统对话框里的文字随系统字号放大
- 〔适用情境 / 做法第 1 步〕安卓 Activity 的 android:configChanges 里有 fontScale 标志（用户选了新的全局字号）；没有声明这一项时，字号变化由系统重建 Activity
- 〔原因 / 做法第 1 步〕安卓的 sp（TypedValue.COMPLEX_UNIT_SP）是 scaled pixel，按用户的系统字号设置缩放；px 不随系统字号变化
- 〔做法第 2 步〕安卓框架（android-36.1 源码）的非线性字号缩放表预置的最大 fontScale 是 2.0
