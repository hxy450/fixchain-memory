# 源端单一 SnackbarHost 的结果反馈用唯一宿主按源端排队与时长展示；每个结果态都要有渲染分支，catch 写入的状态要有消费方

ID：`lesson-187c725b1bb9d8d1bf4d` · 版本：3 · 阶段：execute · 主题：[ui/state/feedback](index.md)

概要：单一 SnackbarHost 用唯一宿主按源排队定时长

信号：`SnackbarHost`, `Snackbar`, `actionLabel`, `SnackbarDuration`, `showSnackbar`, `SnackbarHostState`, `Indefinite`

## 何时使用

页面转换与功能接线阶段，把源端 Snackbar 结果反馈和规格里的操作状态落成 ArkUI 提示，并给成功与失败分支接通界面时

## 适用情境

源端页面只有一个 SnackbarHost，按顺序显示操作结果，showSnackbar 可能带 actionLabel；目标规格给出含 error 的操作状态，并要求失败时报错且不留成功状态；目标页用条件渲染的底部浮层或单槽定时器实现提示。

## 原因

拆成多个互不排斥的浮层会叠在一起；单槽覆盖会丢掉 SnackbarHostState 中排队等待的结果，把带动作的提示按固定秒数自动关闭会让动作来不及点；定义了 error 枚举却没有渲染分支，失败就没有任何提示；catch 只写状态不渲染，验收条目写了也等于没做。来源中转换者把唯一宿主拆成两个浮层，失败界面留给后续却没登记“要渲染失败提示”；接线者读到了“失败要报错”的验收条目，两个 catch 都只写状态，备份失败还写进了恢复状态。

## 做法

1. 用一个宿主管理当前提示，任何时刻最多一条：源端 showSnackbar 挂起排队时，后续提示入队，当前提示结束（超时、点动作或关闭）后再取下一条；源端调用方显式取消旧提示，或当前决策批准只保留最新结果时，才改为新提示替换旧提示。
2. 时长按源端调用推导：显式传 duration 时照用；未传时 Material3 showSnackbar 无 actionLabel 为 Short（4 秒），有 actionLabel 为 Indefinite，常驻到点动作、关闭或离页；与评审口径不同时在迁移报告登记差异。
3. 状态接口列出的每个结果态都在 build 里找到渲染分支；确要留给接线阶段，在占位登记里写明“某态需渲染什么”，不只登记状态回填。每个 catch 写入的状态都要有消费它的分支，不同操作不借用同一个状态。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [编译修复只改报错行，不删功能或换异义替代](../../../process/check-gaming/lesson-29744eb694376e8acaca.lesson.md)（共享 1 张卡）
- [宿主 onBackPressed 自顶向下关闭页内覆盖层](../../navigation/back-stack/lesson-396d54479492828eeea3.lesson.md)（共享 1 张卡）
- [remember 按首次或 key 变才求值](../lifecycle/lesson-3b4a96141329db62a6af.lesson.md)（共享 1 张卡）
- [缺枚举的 FontWeight 写数值，不换近名](../../text/typography/lesson-605038b091e03c26c005.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）

来源支持：2 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, rec-3fd604396e
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-2f11f734c53d33bee770](../../../../../store/cases/case-2f11f734c53d33bee770/df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15.json) · 结论：diagnosis, rec-bc7c00d6df, rec-7d7d1c9d44, rec-c98cfa745d, rec-5579065517
  卡片版本：`df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15`
