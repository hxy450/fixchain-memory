# 源布局有按状态切换的 Lottie 动画层时接入 @ohos/lottie 并迁移动画 JSON，不以静态兜底图静默替代

ID：`lesson-ea55fe23fea47c1cfca3` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，转换含 LottieAnimationView 或 setAnimation("json/...") 的页面头图、背景等动画层时

## 适用情境

Android 页面在静态背景 ImageView 之上叠加 LottieAnimationView，代码按天气、昼夜等状态选择 assets/json 中的动画文件；目标工程尚无 lottie 依赖，静态兜底图已迁移。

## 原因

只迁静态兜底图、不接动画层，页面在所有状态下都显示同一张静态图，与源端的动态头图明显不符，且不会被编译或结构检查发现。来源中转换者读到 LottieAnimationView 叠层与 setBgAnimationByStatus 调用，派工还要求检测到动画信号时转入动画迁移流程，输出仍只有一张静态图，没有依赖、没有迁移 JSON、没有占位，报告也没提动画层；返修重建又改成固定夜景图，直到后来补上 lottie 组件。

## 做法

1. 看到 LottieAnimationView 或 setAnimation("json/...") 时，在 oh-package.json5 接入 @ohos/lottie，把 assets/json 动画文件迁入工程，并复刻状态到动画文件的选择表；静态图只作加载前或失败时的兜底。
2. 本文件完成不了动画层时登记占位并在报告写明，不以静态图静默替代。

## 来源（按需复核）

- [case-0dd25455d592a77ed652](../../../store/cases/case-0dd25455d592a77ed652/19d02d00861a1bd7de2ec6438327de64840673553c49ad924dd1632801b8a9d2.json) · 结论：diagnosis, recommendation:1
  卡片版本：`19d02d00861a1bd7de2ec6438327de64840673553c49ad924dd1632801b8a9d2`
