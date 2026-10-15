# 源窗口按 resize 避让软键盘时设 KeyboardAvoidMode.RESIZE（含未声明的隐式 adjustResize），不用默认 OFFSET

ID：`lesson-f86b02e97cc77e31d51a` · 版本：4

[本主题](index.md)

## 何时使用

页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时；规格提取阶段为未声明 windowSoftInputMode 的含输入框窗口确定目标避让方式时

## 适用情境

源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；目标未设键盘避让模式，转换者不确定默认行为是否等价。也包括 manifest、主题与代码都未设 adjust 值，窗口里有显示中的滚动容器（ListView、ScrollView 或带竖向滚动条、android:isScrollContainer=true 的视图），规格只写“默认弹出”。

## 例外与边界

- 源窗口带 FLAG_FULLSCREEN：adjustResize 被忽略、窗口不缩放（android-36.1 WindowManager.java 说明），平台隐式 resize 同样不适用

## 原因

ArkUI 默认的 KeyboardAvoidMode.OFFSET 把页面整体上移以露出焦点输入框，顶部栏可能被推出屏幕、内容区不收缩；源端 adjustResize + imePadding 保留顶栏、收缩内容区。未设 adjust 值时，安卓按窗口内是否有显示中（isShown）的已登记滚动容器取 adjustResize，否则取 adjustPan（android-36.1 ViewRootImpl）；判据是可见的滚动容器，不是控件类名，不可见的列表不算。对默认行为不确定却以“保持默认并记录”收尾，会把可实现的避让语义降级。

## 做法

1. 先定源窗口实际调整方式：查 manifest、主题与代码（setSoftInputMode）的 adjust 值与 FLAG_FULLSCREEN；都未设 adjust 时，窗口内有显示中的滚动容器取 adjustResize，否则取 adjustPan（对应 OFFSET）。
2. 源 Activity 各页都按 resize 避让时，在 EntryAbility 的 loadContent 成功回调里经窗口 UIContext 统一调用 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)；只有个别页需要时，在该页 NavDestination 的 onShown 中记下当前模式（getKeyboardAvoidMode）并调用 this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)，onHidden 中还原。
3. 源端 imePadding 加在滚动内容尾部、为末项留出键盘空间时，核对 RESIZE 后末项能滚出键盘；仍被遮挡再按键盘高度补尾部留白，同一边界只避让一次。
4. 对目标默认模式与源端是否等价不确定时，先查 KeyboardAvoidMode 的 SDK 声明与说明再决定。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, recommendation:3
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-c96bdbf4d2e0fb58e797](../../../store/cases/case-c96bdbf4d2e0fb58e797/690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3.json) · 结论：recommendation:2, recommendation:4, recommendation:1
  卡片版本：`690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3`
