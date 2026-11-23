# WaterFlow 多列时每个 FlowItem 先写 width('100%') 再加 padding：否则子卡片按瀑布流整宽测量、被列边界裁切

## 何时使用

界面实现阶段，把多列瀑布流（自适应列数或按窗口断点切列）转换为 WaterFlow/FlowItem，确定每个 FlowItem 及其子内容的宽度约束时

## 适用情境

源端用 LazyVerticalStaggeredGrid（Adaptive/Fixed 列）、StaggeredGridLayoutManager 等多列瀑布流；目标 WaterFlow 的 columnsTemplate 在宽窗下为两列及以上，FlowItem 内是根节点 width('100%') 的卡片或整块内容（头部引导块、尾部占位），FlowItem 上只加了 padding/margin 表达项间距。单列窗口下两者等宽，看不出问题。

## 例外与边界

- 项间距原本写成 FlowItem 的 margin 时，补 width('100%') 的同时把它改成 FlowItem 的 padding，或改用 WaterFlow 的 columnsGap、rowsGap；不要让 width('100%') 和 margin 同时留在 FlowItem 上：外边距在计算位置时算作组件大小的一部分，会把项撑出列宽。

## 原因

在已观察环境（HarmonyOS 6.1.1 / API 24 模拟器的宽窗）中，未设宽度的 FlowItem 自身按列宽排布，但其子组件的 width('100%') 按瀑布流可用宽度测量，卡片宽于所在列，超出部分被 WaterFlow 裁掉；单列时列宽等于瀑布流宽，偏差只在多列断点出现，仅以编译通过收口时不会暴露。未查到 ArkUI 文档对这一测量参照的说明，结论来自修复前后的布局实测。

## 做法

1. 每个 FlowItem（含头部整块、尾部占位）都写 .width('100%')，再在 FlowItem 上加 padding 表达源端项间距；不要假定列宽会自动成为子组件百分比宽度的参照。
2. 同工程已有 WaterFlow 页面时，沿用它们的 FlowItem 修饰链（宽度与内距的写法），同类信息流各页保持一致。
3. 源端把某项标为整行跨列（StaggeredGridItemSpan.FullLine 一类）时，width('100%') 只让它填满所在列；需要整行显示时用 WaterFlow 的分段（sections/WaterFlowSections，API 12 起，每段单独设列数）或把该项移到 WaterFlow 之外，按当前任务契约选择。

## 可选检查

- 规格把多列断点列为视觉验收项时，在一个多列宽度下用布局 dump 或截图核对 FlowItem 与其子卡片根节点的宽度一致

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕多列 WaterFlow 里 FlowItem 没写宽度、其子卡片根节点写 width('100%') 时，设备上 FlowItem 按列宽排布，卡片却按瀑布流整宽测量（两列时约为列宽的 2 倍），超出列边界的内容被裁掉、第二列超出窗口；单列时两者等宽看不出
- 〔原因〕尺寸设置文档开头说明：组件尺寸用百分比设置时，按最近一个设置了固定大小的祖先节点的尺寸计算（width 小节写作以父容器宽度为基础值）；文档没有专门说明 FlowItem 的列宽是否算作这个参照
- 〔原因〕组件没有设置 width 时，默认宽度取完整容纳自身内容所需的宽度
- 〔适用情境〕WaterFlow 没有设置 columnsTemplate 时默认 '1fr'，即单列
- 〔做法第 1 步〕官方多列瀑布流示例在 columnsTemplate('1fr 1fr') 下也给 FlowItem 显式写 .width('100%')
- 〔做法第 3 步〕WaterFlow 分段的 SectionOptions.crossCount 在纵向布局时是该段的列数，默认 1，小于 1 按默认值处理
