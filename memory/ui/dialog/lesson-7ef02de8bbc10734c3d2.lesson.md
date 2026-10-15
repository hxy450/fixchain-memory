# 工程约定“路由统一用某框架”时，源端在当前页 show 的弹窗仍叠在宿主页上：路由约束只管页面跳转，不把弹窗改成路由页

ID：`lesson-7ef02de8bbc10734c3d2` · 版本：3

[本主题](index.md)

## 何时使用

规格提取阶段把 Android Dialog/BottomSheet 的呈现方式映射到 ArkUI 承载方式、工程有路由统一约束时；实现阶段按这类规格落地弹窗时

## 适用情境

Android 入口经 bottomDialog/Dialog 在当前 Activity 上 show 全宽底部面板（遮罩下仍见宿主页、点背景关闭、不入返回栈）；目标工程有“路由统一使用某路由框架（如 HMRouter）”的约束，且已有同名路由页可复用；规格援引该约束写成“用路由页承载等价弹层”。

## 例外与边界

- 规格选用路由页或独立窗口承载，且已确认该机制保留宿主页可见与点背景关闭、并在验收中写明对应检查时（见 how 第 2 步）

## 原因

路由页带来独立页面栈、伪造的遮罩和不同的关闭方式；路由约束管的是页面间跳转，不决定弹窗形态。

## 做法

1. 规格把源端呈现方式写成验收契约：叠在宿主页之上、遮罩下可见宿主页、点背景或取消关闭、不新增返回栈；承载映射为宿主页内 Stack 顶层叠层或 bindSheet/CustomDialog（按源类选择见 lesson-368c4592e4c7075c1871），关闭回调由宿主持有。
2. 确需路由承载时显式 .mode(NavDestinationMode.DIALOG)（nav_destination.d.ts，API 11：默认透明、出入栈不影响下层页生命周期），先确认它能保留宿主页可见与点背景关闭，并在验收中写明对应检查；不以标准 NavDestination 加半透明色块伪装遮罩。
3. 弹窗内的二级日历或选择器按父面板的挂载层选承载层，见 lesson-009212ca2c691b97d76c。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-504604963e18f4b6e2f3](../../../store/cases/case-504604963e18f4b6e2f3/2d6d9f26afdb00a773c7f7b41b7fef1e5a693fe0c73c340835a3b288d00d85bd.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`2d6d9f26afdb00a773c7f7b41b7fef1e5a693fe0c73c340835a3b288d00d85bd`
