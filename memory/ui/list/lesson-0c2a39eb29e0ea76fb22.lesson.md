# 滚动中计算条目可见比例或离顶最近的可见项时，用 onVisibleAreaChange 加即时位置查询，不用 onAreaChange

ID：`lesson-0c2a39eb29e0ea76fb22` · 版本：2

[本主题](index.md)

## 何时使用

列表界面实现阶段，把 onGloballyPositioned/boundsInWindow 一类随滚动变化的可见性计算（自动播放、曝光）迁到 ArkUI 时

## 适用情境

源端在 LazyColumn 条目上用 onGloballyPositioned + boundsInWindow 在滚动中计算可见比例并选最近项自动播放；目标准备在条目上挂 onAreaChange。

## 例外与边界

- onVisibleAreaChange 的可见比例只按父组件范围裁剪，不扣除叠在列表上的兄弟组件（悬浮标题栏、底栏等）和窗口遮挡；源端可见性计算要扣掉这类遮挡区域时，选最近项那一步用即时查询到的窗口位置自行扣除，不能只凭回调的比例。

## 原因

onAreaChange 面向组件尺寸与相对父容器位置的布局变化，来源修复判定列表滚动时它不随滚动回调（修复期判断，未另查 SDK 文档）；可见性因而停在首帧状态，自动播放不随滚动切换。onVisibleAreaChange 本身按可见比例阈值回调。

## 做法

1. 用 onVisibleAreaChange([0, 0.5, 1]) 接收可见比例变化，选最近项前用 componentUtils.getRectangleById 等即时查询各条目的窗口位置。
2. 实现后按验收的滚动场景（A、B 可见 → A 出视口 → B 出视口）自查切换。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-dfd68051bcdcc94eba9f](../../../store/cases/case-dfd68051bcdcc94eba9f/07a5310040b53c84865c2afcdfe94396e276549a1c5ea8d94f07ee774232607a.json) · 结论：recommendation:5
  卡片版本：`07a5310040b53c84865c2afcdfe94396e276549a1c5ea8d94f07ee774232607a`
