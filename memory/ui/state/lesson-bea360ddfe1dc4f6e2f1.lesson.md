# 把 @Monitor 改成生产方显式回调时保留“被监听字段变化才执行”：回调入口比较上次值，不挂在每次状态提交上

ID：`lesson-bea360ddfe1dc4f6e2f1` · 版本：1

[本主题](index.md)

## 何时使用

编译修复或接线阶段，因 @Monitor 未绑定（嵌套路径告警等）改由 ViewModel 等生产方显式回调驱动页面视觉态时；派工或 handback 给出替代触发点清单时

## 适用情境

页面原用 @Monitor 监听运行态、结果等少数字段，处理函数含 animateTo、资源查询或动效等视觉动作，对应源端 LaunchedEffect(key)、animateColorAsState(targetValue)、AnimatedContent(targetState) 按目标值变化触发；替代方案在生产方多个路径（含每次定时提交）的尾部调用回调。

## 原因

@Monitor 只在被监听字段变化时触发；改成每次状态提交都调用的回调后，字段没变也会执行，每个周期都重放动画、查询资源，视觉语义变了，同步耗时也压低了周期速率。

## 做法

1. 回调入口记录并比较被监听字段的上次值，未变化直接返回；或只在真正改写这些字段的路径调用回调。
2. 执行替代触发清单前逐个核对新触发点是否会改变原监听字段，多出来的触发点加变化判断或在 handback 中提出，不因“清单是协调者给的”照做。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-31dcdb74eb848ff217c8](../../../store/cases/case-31dcdb74eb848ff217c8/360cfb87f8b2a47e9243a59d3a2beccef0b260bcbaed55d1f909b2a241f8fe46.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`360cfb87f8b2a47e9243a59d3a2beccef0b260bcbaed55d1f909b2a241f8fe46`
