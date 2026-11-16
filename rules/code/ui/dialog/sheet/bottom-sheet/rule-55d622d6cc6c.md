# BottomSheetDialogFragment 的宿主嵌在壳内容区时用窗口级 bindSheet，不用页内浮层

审的是：代码
触发（任一种）：
- 读到：对话框类 extends BottomSheetDialogFragment，onCreateDialog 里设 BottomSheetBehavior.STATE_EXPANDED；宿主页嵌在主壳内容区（标题栏、底部导航由外层提供）；写错的样子：页面内容 Stack 里用 if 分支渲染遮罩加底对齐面板的页内浮层，遮罩和面板只能落在标题栏与底部导航之间；按钮写成扁平的 ButtonType.Normal 按钮
适用范围：迁移 BottomSheetDialogFragment 类面板、宿主页不是整窗页面时
做法：
- 用零尺寸锚点上的 bindSheet（mode 默认 SheetMode.OVERLAY，显示在窗口顶层）或共享面板组件承载，不在页面内容 Stack 里画浮层
- 定按钮样式前把面板子项的选中和未选中两种布局 XML 都读完
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- mode?: SheetMode，默认 SheetMode.OVERLAY：SheetOptions 的显示层级（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetOptions.mode）
- SheetMode.OVERLAY = 0：显示在当前 UIContext 对应窗口的顶层、所有页面之上，与弹窗同级：能盖住外层壳的标题栏和底部导航（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SheetMode.OVERLAY）
针对本应用要查的：
- 面板子项的按钮样式：源工程 res/layout 下面板子项的选中、未选中两份布局 XML（对话框代码里 inflate 的那两个）；读出背景、描边、文字颜色和图标，两态各写一套
来源：1 张卡，1 个应用
- case-c4e5b6ca6da92a568d18（AntennaPod）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
