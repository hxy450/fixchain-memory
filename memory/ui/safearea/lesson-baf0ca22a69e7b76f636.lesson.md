# 源端给根视图设状态栏高度的顶部 padding 并自绘底色时，目标在页面容器上设 padding 与背景色、系统栏保持透明

ID：`lesson-baf0ca22a69e7b76f636` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，把源端根视图（DecorView 或内容根）的状态栏 insets padding 与背景设色翻译为目标页面的避让方式和状态栏底色时

## 适用情境

源 Activity（常见于 Android 15+ 边到边分支）给 DecorView 或根布局 setBackgroundColor，并 setPadding(top = 状态栏 inset)，内容 View 在 onSizeChanged 中按自身宽高布局；目标为全屏沉浸窗口，页面里可能有带遮罩的弹窗。

## 原因

父视图 padding 会缩小子视图：内容从状态栏下沿开始，测得的高度是窗口高减状态栏高；状态栏区的底色由应用根视图绘制，覆盖整窗的弹窗遮罩能压暗它。写成“全屏尺寸再整体 Y 平移”会让布局高度偏大；把底色交给 setWindowSystemBarProperties 的 statusBarColor，状态栏改由系统栏窗口绘制，应用内对话框遮罩就压不到；遮罩若挂在被 padding 缩小的内容槽里，同样压不到状态栏区。

## 做法

1. 在承载内容的页面容器上设 backgroundColor(源端底色) 与 padding({ top: 状态栏避让值 })，子组件（如 Canvas）直接按自身得到的尺寸布局，不在布局输出上做 Y 平移；系统栏的 statusBarColor 设为透明。
2. 页内弹窗遮罩挂在未被顶部 padding 缩小的外层，才能像源端一样压暗状态栏区；遮罩上的卡片前景另行避让。
3. 规格按视图测量语义写契约：“内容区从状态栏下沿开始，布局高度 = 窗口高 − 状态栏高，状态栏区底色由页面容器绘制”，不写成“沿用全屏尺寸”或系统栏着色。
4. 规格或派工要求给系统栏着色，而写盘边界又排除了页面文件时，在交回的决策缺口里报告这一冲突，不只改 statusBarColor 迎合验收截图。

## 可选检查

- 页面有弹窗时打开一次，确认状态栏区域随遮罩一起压暗。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7cd8faf4310e45fc7a2e](../../../store/cases/case-7cd8faf4310e45fc7a2e/058a2ebaac13b4acff39192354a38802292fdc296946595c3c359a159701467b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`058a2ebaac13b4acff39192354a38802292fdc296946595c3c359a159701467b`
