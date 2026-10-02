# 用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，按钮行先定高再让分隔线撑满

ID：`lesson-0a26e0cfc44a183d3a02` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级与卡片、按钮行的高度约束时

## 适用情境

源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，布局是固定宽、wrap_content 高的卡片，按钮行内有 layout_height=match_parent 的竖分隔 View；触发按钮位于 Tabs 子页或嵌套组件内。

## 例外与边界

- 改用 openCustomDialog、bindSheet 等系统弹窗 API 时，全窗遮罩由系统窗口负责，按真弹窗写法处理

## 原因

覆层挂在触发按钮所在的 Tab 子组件里，遮罩只盖到该子组件区域，底部 Tab 栏仍亮、仍可点；按钮行不定高而只给分隔线 Stretch 时，Stretch 子项会把行和卡片撑到父容器全高。来源中写者已读到 Dialog 由 Activity 创建、Theme.Dialog 浮动窗口、卡片 wrap_content 与按钮行实测高度，宿主根 Stack 上也已挂过同类弹窗，仍把覆层写进 Tab 内；真机 dump 显示卡片撑成全高、dim 未盖住 Tab 栏，随后才改为宿主根挂载并给按钮行定高。

## 做法

1. 源弹窗属于 Activity 窗口时，覆层挂在覆盖整个窗口的宿主根容器（如主页根 Stack），不挂在触发按钮所在的子组件；子组件通过共享状态或回调请求宿主显示和关闭，返回键拦截也放在宿主。
2. 转换按钮行里 match_parent 高的分隔 View 时，先给所在 Row 确定高度（取源按钮实测高度，或由 padding 与字号计算），再让分隔线 Stretch 或取 100%；不让未定高 Row 中的 Stretch 子项决定卡片高度。

## 可选检查

- 覆层写完用真机 dump 核两组 bounds：卡片高度接近源端实测，遮罩覆盖源 dim 覆盖的整个窗口（含底部 Tab 栏）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bf55dc1aedfb0f2a965e](../../../store/cases/case-bf55dc1aedfb0f2a965e/bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d`
