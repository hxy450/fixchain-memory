# 子页回传结果：来源页用 pushPathByName 的 onPop 接收时，子页成功出栈必须 pop(result)，裸 pop() 不触发 onPop

ID：`lesson-bd019a59d3ac23b2594e` · 版本：1

[本主题](index.md)

## 何时使用

跨页回传接线阶段，确定子页成功出栈的调用与来源页读取回传结果的触发点时；规格或基础设施阶段定义回传通道时

## 适用情境

源端用 savedStateHandle 的 addReturn/ConsumeReturn 在子页返回后把结果交给来源页；目标来源页用 NavPathStack.pushPathByName(name, param, onPop) 或共享返回值通道接收，生产页与消费页由不同任务分别实现。

## 原因

onPop 回调只在目标页以 pop(result) 出栈时执行；子页先写共享通道再裸 pop()，消费逻辑放在 onPop 里就永远不运行，新回复、编辑结果与封禁状态都不回显。两端分属不同写者，各自只看到自己那一半；收尾统一回传方式时若只改消费端，也不会暴露。

## 做法

1. 回传通道写清三件事：载荷类型、生产端出栈调用、消费端触发点；走 onPop 时生产端 pop(result)，走共享通道时消费端在 NavDestination.onShown 等回到页面的时机读取。
2. 子页写成功出栈前先查来源页的接收方式（是否带 onPop、判断什么 instanceof 类型），按它要求的实例 pop(result)；同时写共享通道也不省掉 result。
3. 对账时对每个 pushPathByName(..., onPop) 列出目标页全部成功出栈点，确认带 result 且类型与 onPop 判型一致；交接里写“同款”的其他调用点一并检索修改。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-60576c483fb94367a81b](../../../../store/cases/case-60576c483fb94367a81b/081ec648c7e111ac67a977b77900b200191cf312dbb5b8f380dfba0054d2c5fc.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`081ec648c7e111ac67a977b77900b200191cf312dbb5b8f380dfba0054d2c5fc`
