# 源端单一提示宿主（SnackbarHost、三方提示条库的全局队列）用唯一宿主按源端排队与时长展示；每个结果态要有渲染分支，catch 写入的状态要有消费方

ID：`lesson-187c725b1bb9d8d1bf4d` · 版本：4

[本主题](index.md)

## 何时使用

页面转换与功能接线阶段，把源端 Snackbar 结果反馈和规格里的操作状态落成 ArkUI 提示，并给成功与失败分支接通界面时；把三方提示条库（makeText(...).show() 一类全局队列提示）迁成目标提示组件时

## 适用情境

源端页面只有一个 SnackbarHost，按顺序显示操作结果，showSnackbar 可能带 actionLabel；目标规格给出含 error 的操作状态，并要求失败时报错且不留成功状态；目标页用条件渲染的底部浮层或单槽定时器实现提示。 也包括源端经三方提示条库显示（Lib.makeText(activity, 文案, 样式, 容器).show()），库内管理器全局串行排队、提供 cancelAll，应用侧只留样式常量；目标准备做成页面自持、@Param visible 驱动的单条组件。 也包括通用映射表把 Snackbar 写成 promptAction.showToast，共享提示组件据此只调用 Toast。

## 原因

拆成多个互不排斥的浮层会叠在一起；单槽覆盖会丢掉 SnackbarHostState 中排队等待的结果，把带动作的提示按固定秒数自动关闭会让动作来不及点；定义了 error 枚举却没有渲染分支，失败就没有任何提示；catch 只写状态不渲染，验收条目写了也等于没做。三方提示条库的队列在库内，页面自持的单条组件只能表达一次性提示，连续结果互相覆盖，也没有 cancelAll。

## 做法

1. 用一个宿主管理当前提示，任何时刻最多一条：源端 showSnackbar 挂起排队时，后续提示入队，当前提示结束（超时、点动作或关闭）后再取下一条；源端调用方显式取消旧提示，或当前决策批准只保留最新结果时，才改为新提示替换旧提示。源端 showSnackbar 带 actionLabel、withDismissAction 或读取 SnackbarResult 时，不按通用映射表改成 showToast（Toast 没有动作与关闭钮，也不回传结果），由该宿主实现动作、关闭钮与结果。
2. 源端经三方提示条库显示时，做成应用级单例队列加宿主组件（宿主放在库调用传入的容器对应位置），提供 cancelAll；显示时长、入场与出场动画、出队时机与是否拦截触摸按库实现取值（取库制品核对；例：Crouton 管理器在入场动画加显示时长后移除、出场动画结束才放下一条、不拦截触摸），不凭样式常量类自定过渡时长。
3. 时长按源端调用推导：显式传 duration 时照用；未传时 Material3 showSnackbar 无 actionLabel 为 Short（4 秒），有 actionLabel 为 Indefinite，常驻到点动作、关闭或离页；与评审口径不同时在迁移报告登记差异。
4. 状态接口列出的每个结果态都在 build 里找到渲染分支；确要留给接线阶段，在占位登记里写明“某态需渲染什么”，不只登记状态回填。每个 catch 写入的状态都要有消费它的分支，不同操作不借用同一个状态。

来源支持：4 张卡 · 已知 3 次迁移（部分未记录） · 已知 2 个应用（部分未记录）

## 来源（按需复核）

- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：diagnosis, recommendation:4
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-16e909b950f12edb0251](../../../store/cases/case-16e909b950f12edb0251/28d112a27b9b47906a4e3406f86c88a5bea25e266e222866401d9558335f86b6.json) · 结论：diagnosis, recommendation:1, recommendation:4
  卡片版本：`28d112a27b9b47906a4e3406f86c88a5bea25e266e222866401d9558335f86b6`
- [case-2f11f734c53d33bee770](../../../store/cases/case-2f11f734c53d33bee770/df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15`
- [case-cfa31a0f8f73caf9c2ab](../../../store/cases/case-cfa31a0f8f73caf9c2ab/55a32e80e90566ff6308fdfe101d216ac8b4845166cf0494f41c7926649575d5.json) · 结论：diagnosis, recommendation:4
  卡片版本：`55a32e80e90566ff6308fdfe101d216ac8b4845166cf0494f41c7926649575d5`
