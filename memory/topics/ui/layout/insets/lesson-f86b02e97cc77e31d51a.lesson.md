# 源窗口按 adjustResize 避让软键盘（声明 adjustResize，或未声明 windowSoftInputMode 而窗口含可滚动视图）时设 KeyboardAvoidMode.RESIZE：各页都如此时在窗口级统一设置，否则在该页显示期间设置、离开时还原；不以默认 OFFSET 记作等价

ID：`lesson-f86b02e97cc77e31d51a` · 版本：3 · 阶段：spec/execute · 主题：[ui/layout/insets](index.md)

概要：源 adjustResize 时键盘避让设 RESIZE

信号：`adjustResize`, `windowSoftInputMode`, `imePadding`, `KeyboardAvoidMode.RESIZE`, `KeyboardAvoidMode.OFFSET`, `setKeyboardAvoidMode`, `getKeyboardAvoidMode`, `onShown`, `onHidden`, `loadContent`

## 何时使用

页面实现阶段，为含文本输入的页面（编辑表单等 NavDestination 子页）落实源端软键盘避让方式时；为未声明 windowSoftInputMode 的含输入框窗口确定目标避让方式时

## 适用情境

源 Activity 声明 windowSoftInputMode=adjustResize，页面在滚动内容或尾部用 imePadding 让键盘弹出时内容区收缩、仍可滚到末项；规格或页面元数据写明 adjustResize + imePadding 并要求等价避让；目标未设键盘避让模式，转换者不确定默认行为是否等价。 也包括源 Activity 未声明 windowSoftInputMode、内容含 ListView/ScrollView（平台隐式 adjustResize），规格只写“默认弹出”，召回因“源端未声明 adjustResize”而排除了本条。

## 原因

ArkUI 默认的 KeyboardAvoidMode.OFFSET 把页面整体上移以露出焦点输入框，顶部栏可能被推出屏幕、内容区不收缩；源端 adjustResize + imePadding 保留顶栏、收缩内容区。对默认行为不确定却以“保持默认并记录”收尾，会把可实现的避让语义降级。

## 做法

1. 源 Activity 各页都按 resize 避让（含平台隐式 adjustResize）时，在 EntryAbility 的 loadContent 成功回调里经窗口 UIContext 统一调用 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)；只有个别页需要时，在该页 NavDestination 的 onShown 中记下当前模式（getKeyboardAvoidMode）并调用 this.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)，onHidden 中还原。
2. 源端 imePadding 加在滚动内容尾部、为末项留出键盘空间时，核对 RESIZE 后末项能滚出键盘；仍被遮挡再按键盘高度补尾部留白，同一边界只避让一次。
3. 对目标默认模式与源端是否等价不确定时，先查 KeyboardAvoidMode 的 SDK 声明与说明再决定。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [源窗口延伸到系统栏下才全屏，底部避让加在屏底层](../immersion/lesson-0e1c846868f2683cc280.lesson.md)（共享 1 张卡）
- [声明 RTL 时保留 start/end 并镜像图标](../variants/lesson-786a04847bf10d364d9d.lesson.md)（共享 1 张卡）
- [三键导航按 TYPE_SYSTEM 底高判定后给导航栏着色](../../theme/tokens/lesson-8bc258c2833be65f4fcd.lesson.md)（共享 1 张卡）
- [平台差异只收敛做不到的一步，其余出口照源保留](../../../app/capability/degradation/lesson-9c973e50aaea054facdc.lesson.md)（共享 1 张卡）
- [expandSafeArea 非避让，前景按避让区补内距](../immersion/lesson-a8452bfea5d42d3dcae3.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-01833db0536ba02ed2ce](../../../../../store/cases/case-01833db0536ba02ed2ce/19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79.json) · 结论：diagnosis, rec-ecbbe824b0
  卡片版本：`19be163e103f323f9d0fb55e1aa2516564a0df2af7f113771337fa3e7f3c8f79`
- [case-c96bdbf4d2e0fb58e797](../../../../../store/cases/case-c96bdbf4d2e0fb58e797/690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3.json) · 结论：rec-fdd3099700, rec-2c2bc9fbbf
  卡片版本：`690e3e8044afac976d280680a439898d1d9c1767283cf4bcd2d13a82c3977cf3`
