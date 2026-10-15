# 源端禁用态只靠代码换背景、文字色固定时，不用 .enabled(false) 整体降透明：显式切换背景与投影，在各激活路径内判态拦截

ID：`lesson-99080bd3bfc1bcbb9c5f` · 版本：5

[本主题](index.md)

## 何时使用

规格提取阶段为 setEnabled/android:enabled 切换的控件写转换决策时；界面实现阶段落实控件禁用态外观与点击拦截时

## 适用情境

源端在 setEnabled(false) 的同时 setBackgroundResource 换成没有 state_enabled 分支的灰色 drawable，textColor 是固定颜色而非 ColorStateList（AppCompat 按钮禁用时投影另归零）；映射参考把 setEnabled(false)/android:enabled 一律对到 .enabled(false)。

## 例外与边界

- 源端禁用外观本身来自 state_enabled 选择器或半透明（如 ColorStateList 的 disabled 项）时，按源端色值显式写出；目标默认禁用透明度恰与源值一致时才直接用 .enabled()

## 原因

Android 的 setEnabled 只改状态，颜色由 drawable 与 textColor 选择器决定；ArkUI enabled(false) 会对整个组件（背景与文字）施加默认禁用透明度，源端“不透明灰底、纯白字”就变成发虚的浅灰。HitTestMode.None 只让本节点不参与命中，子节点照常命中，点击还可能落到下层兄弟或父级（enums.d.ts），并不是拦截。

## 做法

1. 先查源端禁用外观的来源：背景 drawable、textColor 有无 state_enabled 分支，按钮 stateListAnimator 在禁用时是否归零。只来自代码换背景时，规格写“禁用 = 换背景 + 不响应点击”，判据写禁用态取色等于源背景值、文字为源色。
2. 实现时不写 .enabled(false)：背景按启停态切换，禁用时投影置空；在点击回调内判态直接返回（本节点仍参与命中、挡住下层）；控件还有长按、按键等其他激活回调时，每条都加同样的判态守卫。改用 hitTestBehavior(HitTestMode.None) 时不当作拦截，先核对这次点击会不会落到下层兄弟、父级或子节点的点击处理上。
3. 这种替代只覆盖外观和已加守卫的激活路径：节点本身仍处于可用状态，焦点与读屏不会把它当作禁用。源端禁用对读屏有意义（Android 中 setEnabled(false) 使无障碍节点处于不可用状态）时，可用 accessibilityStateDescription 补一句禁用状态播报（本机 common.d.ts，API 23 起，只设置读屏的状态播报文本，不改变节点可用状态；API 23 以下没有这个接口）；仍需要完整禁用语义时，在规格里记下与源端的差异并上报，不把播报当作等价实现。

## 可选检查

- 补了状态播报时，开屏幕朗读确认禁用态的播报内容；这只验证播报文本，不验证节点禁用。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-787e380c801fb46d89a7](../../../store/cases/case-787e380c801fb46d89a7/8ed3ae69d0d0001dffb87b9977b37a46d74df1487b76c460ae8c208b1ed94954.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`8ed3ae69d0d0001dffb87b9977b37a46d74df1487b76c460ae8c208b1ed94954`
