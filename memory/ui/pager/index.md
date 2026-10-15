# ui/pager

分页与标签容器：ViewPager/ViewPager2 到 Swiper 的页数（恒为一页用普通容器）与禁滑方式（disableSwipe，不用 enabled(false)），初始页定位、自绘 tab 与分页的双向联动，Tab 列表默认选中的一次性初始化，自绘日历的翻页容器以及相邻页数据的合并提交与查询范围

[上一级](../index.md)

## 本级经验

- [ViewPager2 的适配器恒为一页时不写成 Swiper，按静态单页用普通容器直嵌](lesson-540747e352d7f006016d.lesson.md)
  - 时机：规格提取阶段为 ViewPager/ViewPager2 选择目标容器并写明手势行为时；实现阶段落地该容器时
  - 情境：源页面用 ViewPager2（+FragmentStateAdapter），但适配器实际只有一页（getItemCount 恒为 1、fragment 列表单元素），切页入口隐藏或在单页下无效；通用映射表或页面元数据只按类型给出 ViewPager2 → Swiper。
  - 例外：适配器页数随数据变化、可能多于一页时，按可滑分页容器处理
- [分页容器的初始页用 Swiper.index 状态绑定，不在 onReady 里立即调用 changeIndex](lesson-ccccf83dc93ae809ccfb.lesson.md)
  - 时机：界面实现阶段，把源端 ViewPager 的初始定位（post 里 setCurrentItem）与首播触发转写成 ArkUI Swiper 时
  - 情境：源端装好数据后在 view.post 等延后回调里 setCurrentItem(index, false)，并靠 onPageSelected 启动当前页；目标在 NavDestination.onReady 读路由参数，Swiper 位于按列表非空条件渲染的分支里。
- [只禁手势的 ViewPager2 映射为 Swiper 的 disableSwipe(true)，不用 enabled(false)](lesson-a468f2cb12577cc1a774.lesson.md)
  - 时机：界面实现阶段，把只禁手势滑动、由 Tab 点击切页的 ViewPager/ViewPager2 转成 Swiper 时；给承载可交互子页的容器设置交互属性时
  - 情境：源端 ViewPager2 承载多个可交互 Fragment，以 isUserInputEnabled=false（或拦截 onTouch/onInterceptTouchEvent）只禁止手势滑动，由底部 Tab 点击 setCurrentItem 切页；目标用 Swiper 加自定义底栏实现同一主壳。
  - 例外：源端是 setEnabled(false) 禁用整个控件时，按禁用控件处理
- [源端“首批数据到达后默认选中首项并通知父级”迁成 @Param 子组件时只初始化一次：items 引用更新只同步高亮，不重置初始化标志、不回调第 0 项](lesson-b6abeeb9b9476b1f1f4d.lesson.md)
  - 时机：页面或子组件转换阶段，把源端 Tab 列表的默认选中与父分页联动写成 ArkUI V2 的 @Param/@Monitor/@Event 逻辑时
  - 情境：源端 Tab Fragment 只在一次性装载分类后选中首项并回调父 ViewPager，翻页时父级只调用 setSelect(position) 同步；目标子组件接收 @Param items/selectedIndex，并经 @Event 让父 Swiper 切页，父组件可能每次渲染都重新映射出 items 数组。
- [翻页视图的相邻页数据按源端先合并、落定后一次提交，查询范围按页面实际格子的首尾日期](lesson-85b33ff729ab0514a20a.lesson.md)
  - 时机：数据接线与修复阶段，为分页日历实现首次加载、按方向预加载与相邻页数据提交时
  - 情境：源端并发查询当前页和前后页，合并后一次提交给视图，查询范围取自按格子计算的起止日期（含上月末与下月初）；目标在滑动手势回调中触发预加载，结果到达就写入正在移动的 Canvas。
- [自绘 tab 行加分页容器要分别接通“页→tab”和“tab→页”两个方向](lesson-27aa2e80a3a4d7724450.lesson.md)
  - 时机：界面实现阶段，把自定义 tab 行与 ViewPager2 转写成自绘 Row/@Builder tab 加受控 Swiper 并接线联动时
  - 情境：源端用普通 TextView 充当 tab，点击切页写在 Fragment 代码里（可能在数据加载函数末尾），布局 XML 与 onPageSelected 只体现选中样式和滑动高亮；目标不用原生 Tabs。
- [自绘月历、周历的横向翻页由 Swiper 承载（每页一个 Canvas，关闭 Canvas 自带横向手势），“自绘”只约束格子绘制](lesson-d4e63d27885d9e348723.lesson.md)
  - 时机：界面实现或缺陷修复阶段，为 Canvas 自绘的日、月、周历确定横向翻页容器时；需求点名 ViewPager 或 Swiper 效果时
  - 情境：源端用 ViewPager2，或配了 PagerSnapHelper 等分页吸附的 RecyclerView，逐页承载月、周视图，并在滑动回调中联动高度；目标用单个 Canvas 绘制月格，以 PanGesture 改写页偏移手动翻页；需求要求跟手分页、拖动中看到相邻页、快滑切页与回弹。
  - 例外：源端本身在单个自定义 View 里用手势翻页，没有分页容器；源端是没有分页吸附的自由滚动 RecyclerView 时不套此条，按滚动列表处理
