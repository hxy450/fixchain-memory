# 源布局有按状态切换的 Lottie 动画层时接入 @ohos/lottie 并迁移动画 JSON，不以静态兜底图静默替代

## 何时使用

界面实现阶段，转换含 LottieAnimationView 或 setAnimation("json/...") 的页面头图、背景等动画层时

## 适用情境

Android 页面在静态背景 ImageView 之上叠加 LottieAnimationView，代码按天气、昼夜等状态选择 assets/json 中的动画文件；目标工程尚无 lottie 依赖，静态兜底图已迁移。

## 例外与边界

- 接入动画时保留源端的播放方式和来源：布局里的 lottie_autoPlay、lottie_loop（以及代码里对播放、循环次数的设置）决定是否自动播放、是否循环，不要一律改成自动循环；动画文件按源端 lottie_fileName、lottie_rawRes、lottie_url 或 setAnimation 实际指向的那一份迁移
- 已迁移的静态背景图保留在动画层下面作为兜底，不因接入动画而删掉

## 原因

只迁静态兜底图、不接动画层，页面在所有状态下都显示同一张静态图，与源端的动态头图明显不符，且不会被编译或结构检查发现。来源中转换者读到 LottieAnimationView 叠层与 setBgAnimationByStatus 调用，派工还要求检测到动画信号时转入动画迁移流程，输出仍只有一张静态图，没有依赖、没有迁移 JSON、没有占位，报告也没提动画层；返修重建又改成固定夜景图，直到后来补上 lottie 组件。

## 做法

1. 看到 LottieAnimationView 或 setAnimation("json/...") 时，在 oh-package.json5 接入 @ohos/lottie，把 assets/json 动画文件迁入工程，并复刻状态到动画文件的选择表；静态图只作加载前或失败时的兜底。
2. 本文件完成不了动画层时登记占位并在报告写明，不以静态图静默替代。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 com.airbnb.android:lottie 6.6.6。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕LottieAnimationView 可在布局里用 lottie_fileName（字符串）、lottie_rawRes（资源引用）、lottie_url 指定动画来源，用 lottie_autoPlay、lottie_loop 指定播放方式（lottie 6.6.6）
