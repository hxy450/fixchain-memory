# 状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs 时把 Tabs 包进该 Column，不在 Tabs 上挂 padding 加背景色

ID：`lesson-fe10bd2491ca4ba82cb5` · 版本：1

[本主题](index.md)

## 何时使用

界面实现或修复阶段，为带 Tabs 等子页铺满容器的主框架页补源端状态栏实色带，决定避让 padding 与背景色挂在哪个组件时

## 适用情境

源 Activity 基类在 onCreate 设置实色状态栏；目标全屏布局，用测得的顶部避让值做 padding；宿主页的避让 padding 写在 Tabs（或 Swiper）上，TabContent 是满铺白底子页；工程其他页面已用“padding + 背景色挂在只包标题条的普通 Column”实现同一色带。

## 原因

在 Tabs 上同时设 padding(top) 与 backgroundColor，padding 区不一定露出 Tabs 自身背景：来源同一构建中，用包裹层写法的子页真机显示蓝色状态带，主框架顶部仍是白带；改为外层 Column 承担 padding 与背景后才显示连续色带。具体原因（TabContent 满铺覆盖或通用背景未绘制）材料未定论。写者写前已读到源端状态栏色与工程内已验证的包裹层写法，却以“与给 Tabs 设背景语义相同”否决了包裹层，该批只过了编译门。

## 做法

1. 避让 padding 与状态栏色放在只承担避让的普通 Column 包裹层上；宿主为 Tabs/Swiper 等由子页铺满的容器时把它包进该 Column：外层承接 layoutWeight、padding(top) 与背景色，Tabs 取 height('100%')。
2. 要在 Tabs、Swiper、Navigation 等特殊容器上依赖 padding 区显示自身背景时，先用最小实验或真机截图确认；不能真机验证就沿用已验证的写法，并在交付说明标出该页避让带颜色待真机确认。

## 可选检查

- 真机核色带时裁图放大或取色确认避让带颜色，并核实装机包包含本次改动（HAP 内字符串，或改后重装），再判断是代码问题还是装机陈旧。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-6910f2ad1e73fb272245](../../../store/cases/case-6910f2ad1e73fb272245/f0a68e36d44be53e71d0f06b4fbe45bee4b923296cb48e7f72c2654e2115367c.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`f0a68e36d44be53e71d0f06b4fbe45bee4b923296cb48e7f72c2654e2115367c`
