# 源页面声明 adjustResize 并用 imePadding 时，在该页显示期间设 KeyboardAvoidMode.RESIZE、离开时还原，不以默认 OFFSET 记作等价

ID：`lesson-f86b02e97cc77e31d51a` · 版本：1

[本主题](index.md)

## 何时使用

页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时

## 适用情境

源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；规格或页面元数据写明 adjustResize + imePadding 并要求等价避让；目标未设键盘避让模式，转换者不确定默认行为是否等价。

## 原因

ArkUI 默认的 KeyboardAvoidMode.OFFSET 把页面整体上移以露出焦点输入框，顶部栏可能被推出屏幕、内容区不收缩；源端 adjustResize + imePadding 保留顶栏、收缩内容区。对默认行为不确定却以“保持默认并记录”收尾，会把可实现的避让语义降级。

## 做法

1. 在该页 NavDestination 的 onShown 中记下当前模式（getKeyboardAvoidMode）并调用 this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)，onHidden 中还原；源 Activity 下各页面都按 resize 避让时可在窗口级统一设置。
2. 源端 imePadding 加在滚动内容尾部、为末项留出键盘空间时，核对 RESIZE 后末项能滚出键盘；仍被遮挡再按键盘高度补尾部留白，同一边界只避让一次。
3. 对目标默认模式与源端是否等价不确定时，先查 KeyboardAvoidMode 的 SDK 声明与说明再决定。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:3
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
