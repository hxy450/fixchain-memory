# 页面 layout_sources 的文件在 layout-* 下有同名变体时，meta 记下变体和断点语义

审的是：规格
触发（任一种）：
- 读到：源 res 下有 layout-sw600dp/、layout-land/、layout-w<N>dp/ 等限定符目录，其中有和主布局或 <include> 布局同名的 XML；写错的样子：页面 meta.json 的 layout_sources 只列 base layout/ 下的文件，没有同名变体，也没写断点语义；页面 spec 同样只列 base include
适用范围：页面数据提取和页面 spec 阶段，填写 layout_sources 时
做法：
- 对 layout_sources 的每个文件在 res/layout-*/ 下找同名 XML，把 sw600dp、land、w<N>dp 变体连同断点语义（sw600dp → 最小宽度 ≥ 600vp，land → 宽 > 高）记入 meta.json 和页面 spec
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- smallestScreenWidthDp：screenWidthDp 和 screenHeightDp 在横竖两个方向上的最小值，对应 sw 限定符：sw600dp 比的是窗口宽高里较小的那个，不随旋转变化（出处：android.content.res.Configuration#smallestScreenWidthDp）
针对本应用要查的：
- 每个布局文件有哪些限定符变体：源工程 res/ 下所有 layout-* 目录，按 layout_sources 里的文件名找同名 XML（含 include 进来的子布局）；记下目录名（限定符）和文件；逐个比较变体与 base 的根布局方向和排列（如 vertical 与 horizontal）
来源：1 张卡，1 个应用
- case-69a2766b2050118ebd5a（omni-notes-hmos）：做法第 1 步 ← 建议 2
