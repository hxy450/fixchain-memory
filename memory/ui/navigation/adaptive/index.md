# ui/navigation/adaptive

宽窗自适应导航结构：列表-详情分栏的进入条件、各目的地的 pane 角色（列表、详情、全宽 push）与无详情时的占位，分栏宽度阈值的来源

[上一级](../index.md)

## 本级经验

- [宽窗列表-详情分栏按当前目的地的 pane 角色进入：只有详情目的地进右侧 pane，同一顶层下 push 的其他页面保持全宽](lesson-b0992775b0a4c114e04b.lesson.md)
  - 时机：应用壳与导航实现阶段，用 Navigation 的 Split/Stack 模式或自绘双栏模拟源端按目的地 pane 元数据（listPane、detailPane）决定分栏的宽窗列表-详情布局，确定何时进入分栏、哪些页面进入详情 pane 时
  - 情境：源端用 ListDetailSceneStrategy、ListDetailPaneScaffold 等列表-详情布局，各目的地带 pane 元数据（listPane、detailPane 或没有元数据）；目标在单个 Navigation 中按宽度断点切 NavigationMode.Split，列表所在顶层下还能 push 搜索、设置等非详情页。
  - 例外：Navigation 不设 mode 时默认 NavigationMode.Auto：宽度不小于 600vp 就自动分栏，push 的页面都显示在右侧内容区。要让栈顶为非详情目的地时全宽显示，得按栈顶角色显式切到 NavigationMode.Stack，不能靠默认值。
