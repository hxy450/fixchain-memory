# 状态栏实色避让带挂在只承担避让的外层 Column：宿主是 Tabs 时把 Tabs 包进该 Column，不在 Tabs 上挂 padding 加背景色

## 何时使用

界面实现或修复阶段，为带 Tabs 等子页铺满容器的主框架页补源端状态栏实色带，决定避让 padding 与背景色挂在哪个组件时

## 适用情境

源 Activity 基类在 onCreate 设置实色状态栏；目标全屏布局，用测得的顶部避让值做 padding；宿主页的避让 padding 写在 Tabs（或 Swiper）上，TabContent 是满铺白底子页；工程其他页面已用“padding + 背景色挂在只包标题条的普通 Column”实现同一色带。

## 例外与边界

- 只把 Tabs 上的避让 padding 与背景色（连同 layoutWeight）移到外层 Column，Tabs 自身的页签栏、控制器、onChange 等配置留在 Tabs 上不动。
- 工程里已经用包裹层写法、真机上避让带颜色正确的页面不在这条的改动范围内。

## 原因

在 Tabs 上同时设 padding(top) 与 backgroundColor，padding 区不一定露出 Tabs 自身背景：来源同一构建中，用包裹层写法的子页真机显示蓝色状态带，主框架顶部仍是白带；改为外层 Column 承担 padding 与背景后才显示连续色带。具体原因（TabContent 满铺覆盖或通用背景未绘制）材料未定论。写者写前已读到源端状态栏色与工程内已验证的包裹层写法，却以“与给 Tabs 设背景语义相同”否决了包裹层，该批只过了编译门。

## 做法

1. 避让 padding 与状态栏色放在只承担避让的普通 Column 包裹层上；宿主为 Tabs/Swiper 等由子页铺满的容器时把它包进该 Column：外层承接 layoutWeight、padding(top) 与背景色，Tabs 取 height('100%')。
2. 要在 Tabs、Swiper、Navigation 等特殊容器上依赖 padding 区显示自身背景时，先用最小实验或真机截图确认；不能真机验证就沿用已验证的写法，并在交付说明标出该页避让带颜色待真机确认。

## 可选检查

- 真机核色带时裁图放大或取色确认避让带颜色，并核实装机包包含本次改动（HAP 内字符串，或改后重装），再判断是代码问题还是装机陈旧。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕宿主页把顶部避让的 padding(top) 和 backgroundColor 同时挂在 Tabs 上、TabContent 是满铺白底子页时，真机上 padding 区显示为白带，不显示 Tabs 上设的背景色（HarmonyOS 6.0.2，API 22 真机）
