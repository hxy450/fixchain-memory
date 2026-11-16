# 源布局用 ViewPager 承载子 Fragment 的列表时，先读子 Fragment 和 item 布局再写

审的是：代码
触发（任一种）：
- 读到：页面 XML 有 TabLayout + ViewPager，页面 Fragment 代码里给 ViewPager 配了子 Fragment 列表（tab 标题一组、子 Fragment 一组）；写错的样子：目标端对应子页的 List / ListItem 是按截图或猜测写的；读过的文件里没有子 Fragment 的布局 XML 和 RecyclerView 的 item 布局，列表项的字段、分组和源端不符
适用范围：迁移由 ViewPager / 子 Fragment 承载内容的安卓页面时，子页里的列表和空态
做法：
- 顺着页面代码里 ViewPager 的 adapter 找到每个 tab 的子 Fragment，读它 inflate 的布局 XML，再读其中 RecyclerView 的 Adapter 用的 item 布局
- 目标端每个子页按子 Fragment 的布局写，列表项按 item 布局写 ListItem 的内容；没读到 item 布局前不按截图补写列表
针对本应用要查的：
- 每个 tab 对应的子 Fragment 及其布局：源工程里页面 Fragment / Activity 的 Kotlin 或 Java 代码中给 ViewPager 设 adapter 的地方（FragmentPagerAdapter 的 getItem、FragmentStateAdapter 的 createFragment，或传进 adapter 的 Fragment 列表）；得到子 Fragment 类后看它 onCreateView 或 ViewBinding inflate 的布局资源名，再打开 res/layout 下同名 XML
- 列表项的布局：子 Fragment 里 RecyclerView 绑定的 Adapter 类；看 onCreateViewHolder 里 inflate 的布局资源名，打开 res/layout 下同名 XML，按其中的控件写 ListItem
来源：1 张卡，1 个应用
- case-bd76c218ac0773e443e3（android-train-ticket-vest7）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
