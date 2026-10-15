# 惰性列表条目带 Modifier.animateItem() 时，ArkUI 侧把数据增删放进 animateTo 并给 ListItem 挂转场

ID：`lesson-e3401517f6ed9a9a85ee` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把带 Modifier.animateItem() 的惰性列表条目翻译成 ArkUI List，或实现条目移除（关闭提示卡、删除项）时

## 适用情境

源端 LazyColumn/LazyRow 条目挂 Modifier.animateItem()，条目出现、消失与位置变化都有动画（Compose foundation 1.11.1 源码 LazyItemScope 中 fadeInSpec、placementSpec、fadeOutSpec 均有默认值）；目标用 List + ForEach/LazyForEach；部分移除由持久化写入后经数据流回推触发。

## 原因

animateItem 让条目的出现、消失和其余条目的位移都带动画；目标直接改数据源时条目瞬间出现或消失，其余条目跳位；移除时在 animateTo 闭包外同步置 false 也会绕过转场。

## 做法

1. 数据增删放进 animateTo，ListItem 挂插入/删除转场（如透明度）；源端有 animateItem 时其余条目的位移也要实现动画，不只做淡入淡出。
2. 删除由持久化写入后经数据流回推触发时，先完成写入，再在 animateTo 中改变驱动显示的状态，不在动画闭包外同步置 false。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-7ced02d9c41ab6f4919a](../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：recommendation:3
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
- [case-7d5b3583abd06943248f](../../../store/cases/case-7d5b3583abd06943248f/be28e286f2c5961d3c34a8a57df28d77cd5a345f9b4ff620dd610bd4975f4baf.json) · 结论：recommendation:3
  卡片版本：`be28e286f2c5961d3c34a8a57df28d77cd5a345f9b4ff620dd610bd4975f4baf`
