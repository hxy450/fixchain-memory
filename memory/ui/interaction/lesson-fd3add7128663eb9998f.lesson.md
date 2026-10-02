# 点击事件挂在源端真正持有点击的节点上：源端只绑整栏就挂外层，只绑行内子 View 就只挂该子控件；清理重复绑定时保留整栏容器的事件

ID：`lesson-fd3add7128663eb9998f` · 版本：2

[本主题](index.md)

## 何时使用

界面实现与返修阶段，为由多个子控件拼成的搜索栏、入口条或设置行决定 onClick 挂在哪一层，或清理、重写其中的点击绑定时

## 适用情境

源布局只在整条容器上绑定点击（如 LinearLayout 的 onClick 或 DataBinding 点击），内部图标、提示文字、“搜索”字样只负责展示；目标用 Row + Image + Text 模拟占位搜索框（不是 TextInput），点击后压栈进入目标页。也包括源端 Java 只对行内某个子 View（如右侧值文本）setOnClickListener，同页其他行绑定整行 layout；目标用 Row 承载这些设置行。

## 原因

给子控件额外挂同一回调会形成重复绑定；返修若按“重复绑定会重复压栈”的推测删掉外层容器的事件，整栏就只剩子控件可点，点中间提示区没有反应。来源中生成期写者正确绑定了整栏，又给“搜索”文字多挂了同一回调；返修者没查源布局也没复现，就删了整栏事件、保留文字事件，用户随即报告搜索框点击没反应。另一应用中返修者读到源端只给手机号行右侧的值文本绑定点击，上下文压缩后摘要只剩“四个点击入口”，重写该行时仍把 onClick 挂在整行 Row 上，后续审计才收窄到值文本。

## 做法

1. onClick 按源布局里持有点击的节点挂：源端只有外层容器可点时只给外层 Row 绑定，不给文字、图标子控件再挂同一跳转。
2. 清理重复点击时先查源布局的点击持有者和视觉点击区域，保留覆盖整栏的外层事件、删除子控件事件；“重复压栈”一类推测先用日志或设备复现确认再改。
3. 以 Java 中 setOnClickListener 实际绑定的 View 为准：只绑定行内子 TextView 时只给对应 Text 加 onClick，整行 layout 被绑定时才给 Row 加；重写行块时检查 onClick 的挂载位置与注释是否一致。

## 可选检查

- 改完点搜索栏中间的提示区，确认外层节点 clickable=true，且只进入一次目标页。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-784ba4ab52f98f7156b6](../../../store/cases/case-784ba4ab52f98f7156b6/4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5.json) · 结论：diagnosis, recommendation:3
  卡片版本：`4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5`
- [case-adacd41d159c24498006](../../../store/cases/case-adacd41d159c24498006/52623310cff384d4d631931cb3ba7842cfaf2b307a632155d9385c258313b9a4.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`52623310cff384d4d631931cb3ba7842cfaf2b307a632155d9385c258313b9a4`
