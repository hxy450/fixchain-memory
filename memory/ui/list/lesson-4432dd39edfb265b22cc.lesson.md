# WaterFlow 多列时每个 FlowItem 先写 width('100%') 再加 padding：否则子卡片按瀑布流整宽测量、被列边界裁切

ID：`lesson-4432dd39edfb265b22cc` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把多列瀑布流（自适应列数或按窗口断点切列）转换为 WaterFlow/FlowItem，确定每个 FlowItem 及其子内容的宽度约束时

## 适用情境

源端用 LazyVerticalStaggeredGrid（Adaptive/Fixed 列）、StaggeredGridLayoutManager 等多列瀑布流；目标 WaterFlow 的 columnsTemplate 在宽窗下为两列及以上，FlowItem 内是根节点 width('100%') 的卡片或整块内容（头部引导块、尾部占位），FlowItem 上只加了 padding/margin 表达项间距。单列窗口下两者等宽，看不出问题。

## 原因

在已观察环境（HarmonyOS 6.1.1 / API 24 模拟器的宽窗）中，未设宽度的 FlowItem 自身按列宽排布，但其子组件的 width('100%') 按瀑布流可用宽度测量，卡片宽于所在列，超出部分被 WaterFlow 裁掉；单列时列宽等于瀑布流宽，偏差只在多列断点出现，仅以编译通过收口时不会暴露。未查到 ArkUI 文档对这一测量参照的说明，结论来自修复前后的布局实测。

## 做法

1. 每个 FlowItem（含头部整块、尾部占位）都写 .width('100%')，再在 FlowItem 上加 padding 表达源端项间距；不要假定列宽会自动成为子组件百分比宽度的参照。
2. 同工程已有 WaterFlow 页面时，沿用它们的 FlowItem 修饰链（宽度与内距的写法），同类信息流各页保持一致。
3. 源端把某项标为整行跨列（StaggeredGridItemSpan.FullLine 一类）时，width('100%') 只让它填满所在列；需要整行显示时用 WaterFlow 的分段（sections/WaterFlowSections，API 12 起，每段单独设列数）或把该项移到 WaterFlow 之外，按当前任务契约选择。

## 可选检查

- 规格把多列断点列为视觉验收项时，在一个多列宽度下用布局 dump 或截图核对 FlowItem 与其子卡片根节点的宽度一致

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-caa6af1dd62533f0f610](../../../store/cases/case-caa6af1dd62533f0f610/75590bd3ca2e56358680242b3746a5746b673fe8484a89c600f0ae129d83c364.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`75590bd3ca2e56358680242b3746a5746b673fe8484a89c600f0ae129d83c364`
