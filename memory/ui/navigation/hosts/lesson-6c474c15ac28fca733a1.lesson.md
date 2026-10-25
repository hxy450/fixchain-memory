# 路由表只注册以 NavDestination 为根的组件：Tab 内容组件兼作路由目标时由路由侧包一层帧

ID：`lesson-6c474c15ac28fca733a1` · 版本：2

[本主题](index.md)

## 何时使用

导航壳与路由表收口阶段，往 navDestination 映射的槽位填目标组件时

## 适用情境

同一个页面组件既嵌在底栏 Tab 里作内容组件（build 根是 Column 等普通容器），又是深链或按钮跳转的路由目标；路由表按 struct 名把它直接挂进 pageMap。

## 原因

Navigation 只把以 NavDestination 为根的组件当作目的地页渲染：普通组件 push 进栈后是空白页，也拿不到 NavDestinationContext 里的参数与返回事件。结构检查只核对槽位已注册，不核对组件根节点；路由形态报“未知”时被整批判为无问题，就再没有关口发现。

## 做法

1. 往槽位填组件前逐个确认目标 struct 的 build 根是否为 NavDestination；不是时在路由侧写一个以 NavDestination 为根的路由帧包住它，在帧的 onReady 解析参数后以 @Param 传入，并按源端处理系统栏避让与返回。
2. 结构检查对路由形态报未知时逐条核对根节点，不批量判为无问题。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-2e5a8c9bed405f41a6ce](../../../../store/cases/case-2e5a8c9bed405f41a6ce/3ed5c8eee4b7400167b2b343955257e6a051ee7cd6473f1e15ac1c056d2ce91c.json) · 结论：diagnosis, recommendation:5
  卡片版本：`3ed5c8eee4b7400167b2b343955257e6a051ee7cd6473f1e15ac1c056d2ce91c`
