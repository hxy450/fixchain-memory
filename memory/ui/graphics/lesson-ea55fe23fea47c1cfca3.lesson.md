# 源布局有按状态切换的 Lottie 动画层时接入 @ohos/lottie 并迁移动画 JSON，不以静态兜底图静默替代

ID：`lesson-ea55fe23fea47c1cfca3` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，转换含 LottieAnimationView 或 setAnimation("json/...") 的页面头图、背景等动画层时

## 适用情境

Android 页面在静态背景 ImageView 之上叠加 LottieAnimationView，代码按业务状态（如天气、昼夜）调用 setAnimation 选择 assets/json 中的动画文件；目标工程尚无 lottie 依赖，静态兜底图已迁移。

## 原因

只迁静态兜底图、不接动画层，页面在所有状态下都显示同一张静态图，与源端的动态头图明显不符，且编译与结构检查都发现不了。

## 做法

1. 看到 LottieAnimationView 或 setAnimation("json/...") 时，在 oh-package.json5 接入 @ohos/lottie，把源端 assets/json 中用到的动画 JSON 迁入工程；放置目录、path 写法与加载、释放接口按安装后 oh_modules/@ohos/lottie 的 README 与类型声明确定，不凭记忆写参数。状态切换时按复刻的“状态 → 动画文件”选择表换加载的文件。
2. 静态图按源布局保留为动画层下方的底图，不以它静默替代动画层。
3. 先接入依赖并迁移可获得的动画 JSON；只有跨文件分工导致本文件不能接线时，才登记写明负责方与完成条件的缺口。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-0dd25455d592a77ed652](../../../store/cases/case-0dd25455d592a77ed652/19d02d00861a1bd7de2ec6438327de64840673553c49ad924dd1632801b8a9d2.json) · 结论：diagnosis, recommendation:1
  卡片版本：`19d02d00861a1bd7de2ec6438327de64840673553c49ad924dd1632801b8a9d2`
