# 列表有多种 viewType 时逐类核对卡片样式，单一类型的背景不写进共用 Builder

审的是：代码
触发（任一种）：
- 读到：RecyclerView.Adapter 有多个 getItemViewType 分支，只有某一类（如推广项）的 item 布局里有 android:background="@drawable/…" 的圆角描边背景，普通项布局没有背景；写错的样子：目标端一个 @Builder 同时渲染各类卡片，背景层把那一类的白底 + .border(...) + .borderRadius(...) 写给所有分支
适用范围：把含多种 ViewHolder 的安卓列表 / 网格迁成 ArkUI List / Grid、用共用 Builder 渲染卡片时
做法：
- 逐类核对：每个 viewType 的 item 根布局，以及 holder 运行时 addView 或 inflate 的子视图，分别定背景、描边和圆角
- 只属于某一类的样式写在该类自己的分支里，或作为 Builder 参数传入，不写进所有分支共用的背景层
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T；半径受组件尺寸限制，最大为宽或高的一半：卡片圆角（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- 把推广项的圆角描边背景套到普通项后圆角和源端不一致；普通项改用源端组件根视图的圆角后正确：验证过的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 每个 viewType 的卡片外观来源：源工程 Adapter 的 getItemViewType / onCreateViewHolder，各 holder 类 inflate 的 res/layout XML，以及 holder 里 addView 进容器的视图；逐类记下根布局的 background、CardView 的 cardCornerRadius、描边 drawable，按类分别写到目标端分支
未核实：修复统一改成普通项的圆角后，推广项是否要单独保留自己的圆角描边，卡里没核
来源：1 张卡，1 个应用
- case-5b1b0e2ce03be0dc6d37（组件岛Widget Island）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 2 ← 诊断
