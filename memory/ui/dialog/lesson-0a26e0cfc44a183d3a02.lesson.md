# 用页内覆层承载 Activity 级 Dialog 时挂在覆盖整窗的宿主根，不挂在触发按钮所在的子组件

ID：`lesson-0a26e0cfc44a183d3a02` · 版本：4

[本主题](index.md)

## 何时使用

界面实现阶段，按项目已采用的页内覆层写法（条件渲染的全幅遮罩 + 卡片）改写 Android Dialog，确定覆层挂载层级时

## 适用情境

源弹窗由 Activity 创建（如 Fragment 中 new XxxDialog(getActivity(), ...)），样式继承 Theme.Dialog、windowIsFloating=true，源端 dim 覆盖整个窗口；触发按钮位于 Tabs 子页或嵌套组件内；项目已决定用页内覆层而不是系统弹窗 API。

## 例外与边界

- 改用 openCustomDialog、bindSheet 等系统弹窗 API 承载时不适用本条（本条只管页内覆层的挂载层级），承载形态按 lesson-368c4592e4c7075c1871 选择

## 原因

覆层挂在触发按钮所在的子组件里，遮罩只盖到该子组件区域，底部 Tab 栏不在遮罩下、仍是亮的，与源端覆盖整个窗口的 dim 不符。

## 做法

1. 源弹窗属于 Activity 窗口时，覆层挂在覆盖整个窗口的宿主根容器（如主页根 Stack），不挂在触发按钮所在的子组件；子组件通过共享状态或回调请求宿主显示和关闭，返回键拦截也放在宿主。

## 可选检查

- 覆层写完用真机 dump 核对遮罩覆盖源端 dim 覆盖的整个窗口（含底部 Tab 栏）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bf55dc1aedfb0f2a965e](../../../store/cases/case-bf55dc1aedfb0f2a965e/bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`bcb7663fe953c49cc6b18f293ae448fe649838e3a6f0e8e0e2d31020c4836d2d`
