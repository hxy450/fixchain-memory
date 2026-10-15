# 点击挂在源端真正持有点击的节点上；带文字的 CheckBox/RadioButton 拆成勾选控件加 Text 时整体可点、命中区按源宽度

ID：`lesson-fd3add7128663eb9998f` · 版本：4

[本主题](index.md)

## 何时使用

界面实现与返修阶段，为由多个子控件拼成的搜索栏、入口条或设置行决定 onClick 挂在哪一层，或清理、重写其中的点击绑定时；把带文字的 CheckBox/RadioButton 拆成 ArkUI 勾选控件加 Text 时

## 适用情境

源布局只在整条容器上绑定点击（如 LinearLayout 的 onClick 或 DataBinding 点击），内部图标、提示文字、“搜索”字样只负责展示；目标用 Row + Image + Text 模拟占位搜索框（不是 TextInput），点击后压栈进入目标页。也包括源端 Java 只对行内某个子 View（如右侧值文本）setOnClickListener，同页其他行绑定整行 layout；目标用 Row 承载这些设置行。也包括带文字的 CheckBox/RadioButton（XML 声明或代码动态创建，宽度来自 wrap_content、match_parent、alignParentLeft 加 toLeftOf 两端锚定或父容器默认 LayoutParams），目标 Checkbox/Radio 不带文字、需另配 Text；为折行给 Text 加 layoutWeight(1) 时连同点击挂在整行上。

## 原因

给子控件额外挂同一回调会形成重复绑定；按“重复绑定会重复压栈”的推测删掉外层容器的事件后，整栏就只剩子控件可点，点中间提示区没有反应；反过来源端只绑行内子 View 时，把点击挂到整行会扩大可点范围。Android 复合按钮的框与文字是一个可点控件，命中区等于它的测量宽度；拆开后文字不挂点击就只剩方框可点，为折行加的 layoutWeight(1) 又会把命中区撑满整行。

## 做法

1. onClick 按源布局里持有点击的节点挂：源端只有外层容器可点时只给外层 Row 绑定，不给文字、图标子控件再挂同一跳转。
2. 清理重复点击时先查源布局的点击持有者和视觉点击区域，保留覆盖整栏的外层事件、删除子控件事件；“重复压栈”一类推测先用日志或设备复现确认再改。
3. 以 Java 中 setOnClickListener 实际绑定的 View 为准：只绑定行内子 TextView 时只给对应 Text 加 onClick，整行 layout 被绑定时才给 Row 加；重写行块时检查 onClick 的挂载位置与注释是否一致。
4. 带文字的勾选控件把框与文字作为一个可点控件：外层容器统一 onClick，内层勾选控件 hitTestBehavior(HitTestMode.None) 避免双触发；命中区按源宽度，wrap_content 只覆盖框和文字，match_parent 或两端锚定才撑到右侧边界，为折行加的 layoutWeight(1) 不同时扩大可点范围。
5. 代码动态创建的复合按钮按父容器默认 LayoutParams 判断宽度：RadioGroup.addView 默认 WRAP_CONTENT，竖向 LinearLayout.addView 默认 MATCH_PARENT 宽；显式 setLayoutParams 以其为准。

## 可选检查

- 改完点搜索栏中间的提示区，确认外层节点 clickable=true，且只进入一次目标页。

来源支持：3 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-6d1435e3e9257286cfbf](../../../store/cases/case-6d1435e3e9257286cfbf/8c08b8945b1b30675cb22e23c59f23cee921bbbbb57ec78442df66ea581c8341.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`8c08b8945b1b30675cb22e23c59f23cee921bbbbb57ec78442df66ea581c8341`
- [case-784ba4ab52f98f7156b6](../../../store/cases/case-784ba4ab52f98f7156b6/4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5.json) · 结论：diagnosis, recommendation:3
  卡片版本：`4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5`
- [case-adacd41d159c24498006](../../../store/cases/case-adacd41d159c24498006/52623310cff384d4d631931cb3ba7842cfaf2b307a632155d9385c258313b9a4.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`52623310cff384d4d631931cb3ba7842cfaf2b307a632155d9385c258313b9a4`
