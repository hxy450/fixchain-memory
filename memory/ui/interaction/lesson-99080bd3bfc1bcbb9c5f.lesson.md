# 源端禁用态只靠代码换背景、文字色固定时，不用 ArkUI .enabled(false)（会对整个组件降透明）：显式切换背景与投影，用 hitTestBehavior(HitTestMode.None) 或回调内判态拦截点击

ID：`lesson-99080bd3bfc1bcbb9c5f` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段为 setEnabled/android:enabled 切换的控件写转换决策时；界面实现阶段落实控件禁用态外观与点击拦截时

## 适用情境

源端在 setEnabled(false) 的同时 setBackgroundResource 换成没有 state_enabled 分支的灰色 drawable，textColor 是固定颜色而非 ColorStateList（AppCompat 按钮禁用时投影另归零）；映射参考把 setEnabled(false)/android:enabled 一律对到 .enabled(false)。

## 例外与边界

- 源端禁用外观本身来自 state_enabled 选择器或半透明（ColorStateList 的 disabled 项、Compose 组件默认禁用色）时，按源端色值显式写出；目标默认禁用透明度恰与源值一致时才直接用 .enabled()

## 原因

Android 的 setEnabled 只改状态，颜色由 drawable 与 textColor 选择器决定；ArkUI enabled(false) 会对整个组件（背景与文字）施加默认禁用透明度，源端“不透明灰底、纯白字”就变成发虚的浅灰。

## 做法

1. 先查源端禁用外观的来源：背景 drawable、textColor 有无 state_enabled 分支，按钮 stateListAnimator 在禁用时是否归零。只来自代码换背景时，规格写“禁用 = 换背景 + 不响应点击”，判据写禁用态取色等于源背景值、文字为源色。
2. 实现时不写 .enabled(false)：背景按启停态切换，禁用时投影置空，用 hitTestBehavior(HitTestMode.None) 拦截点击（或在回调内判态直接返回）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-787e380c801fb46d89a7](../../../store/cases/case-787e380c801fb46d89a7/8ed3ae69d0d0001dffb87b9977b37a46d74df1487b76c460ae8c208b1ed94954.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`8ed3ae69d0d0001dffb87b9977b37a46d74df1487b76c460ae8c208b1ed94954`
