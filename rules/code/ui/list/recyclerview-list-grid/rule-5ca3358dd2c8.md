# 页面主体是 RecyclerView 多类型 Adapter 时，逐个读 item 布局再实现区块，不凭标题推断

审的是：代码
触发（任一种）：
- 读到：页面布局只有 RecyclerView（常在 SwipeRefreshLayout 里）外壳，Adapter 用 addItemType 或 onCreateViewHolder 按类型 inflate 多个 item 布局，各区块的内容在绑定方法里填；写错的样子：目标区块只剩标题文字：Grid 绑空数组、横向 List 固定高度没有内容、趋势图写成纯文本列表，像占位卡片
适用范围：把以 RecyclerView 多类型 Adapter 承载主体内容的安卓页面转成 ArkUI 页面时
做法：
- 先从 addItemType / onCreateViewHolder 列出全部 item 布局并逐个读取，按 item 布局实现每个区块的控件、层级和尺寸
- 不只凭绑定代码或区块标题推断卡片内容；绑定代码只用来确定数据怎么填进 item 布局
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按各 item 布局重建头图、概览、逐小时、趋势图双态、双指标、4×2 网格后与源端一致：修好后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- Adapter 引用的全部 item 布局：源工程 Adapter 类里 addItemType(类型, R.layout.…) 或 onCreateViewHolder 里 inflate 的布局资源，再到 res/layout 下找对应 XML；一个类型一份布局，逐份读出控件树、尺寸和默认可见状态
来源：1 张卡，1 个应用
- case-5d12548f9d559985c27d（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
