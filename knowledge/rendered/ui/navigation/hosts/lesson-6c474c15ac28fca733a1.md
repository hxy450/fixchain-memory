# 路由表只注册以 NavDestination 为根的组件：Tab 内容组件兼作路由目标时由路由侧包一层帧

## 何时使用

导航壳与路由表收口阶段，往 navDestination 映射的槽位填目标组件时

## 适用情境

同一个页面组件既嵌在底栏 Tab 里作内容组件（build 根是 Column 等普通容器），又是深链或按钮跳转的路由目标；路由表按 struct 名把它直接挂进 pageMap。改法只在路由侧加帧：被包的 Tab 内容组件本身保持原样（根节点不改成 NavDestination），它在 Tab 里的嵌入用法不变。

## 原因

Navigation 只把以 NavDestination 为根的组件当作目的地页渲染：普通组件 push 进栈后是空白页，也拿不到 NavDestinationContext 里的参数与返回事件。结构检查只核对槽位已注册，不核对组件根节点；路由形态报“未知”时被整批判为无问题，就再没有关口发现。

## 做法

1. 往槽位填组件前逐个确认目标 struct 的 build 根是否为 NavDestination；不是时在路由侧写一个以 NavDestination 为根的路由帧包住它，在帧的 onReady 解析参数后以 @Param 传入，并按源端处理系统栏避让与返回。
2. 结构检查对路由形态报未知时逐条核对根节点，不批量判为无问题。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕NavDestination 是 Navigation 子页面的根容器，承载子页面的特殊属性和生命周期（标题栏、返回事件、NavDestinationContext 等都挂在它上面）
- 〔原因〕build 根是普通容器（不是 NavDestination）的 Tab 内容组件直接挂进 navDestination 映射、被 push 进栈时，显示为空白页
