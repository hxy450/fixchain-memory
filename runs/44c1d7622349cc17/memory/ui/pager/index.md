# ui/pager

分页与标签容器：ViewPager/ViewPager2 到 Swiper 的页数与手势、初始页定位、自绘 tab 与分页的双向联动

[上一级](../index.md)

## 本级经验

- [分页容器的初始页用 Swiper.index 状态绑定，不在 onReady 里立即调用 changeIndex](lesson-ccccf83dc93ae809ccfb.lesson.md)
  - 时机：界面实现阶段，把源端 ViewPager 的初始定位（post 里 setCurrentItem）与首播触发转写成 ArkUI Swiper 时
  - 情境：源端装好数据后在 view.post 等延后回调里 setCurrentItem(index, false)，并靠 onPageSelected 启动当前页；目标在 NavDestination.onReady 读路由参数，Swiper 位于按列表非空条件渲染的分支里。
- [只有一页或禁用了滑动的 ViewPager2 不写成可滑的 Swiper](lesson-540747e352d7f006016d.lesson.md)
  - 时机：规格提取阶段为 ViewPager/ViewPager2 选择目标容器并写明手势行为时；实现阶段落地该容器时
  - 情境：源页面用 ViewPager2 + FragmentStateAdapter，但适配器实际只有 1 页（或 isUserInputEnabled=false），切页入口隐藏或无效；通用映射表或页面元数据只按类型给出 ViewPager2 → Swiper。
- [自绘 tab 行加分页容器要分别接通“页→tab”和“tab→页”两个方向](lesson-27aa2e80a3a4d7724450.lesson.md)
  - 时机：界面实现阶段，把自定义 tab 行与 ViewPager2 转写成自绘 Row/@Builder tab 加受控 Swiper 并接线联动时
  - 情境：源端用普通 TextView 充当 tab，点击切页写在 Fragment 代码里（可能在数据加载函数末尾），布局 XML 与 onPageSelected 只体现选中样式和滑动高亮；目标不用原生 Tabs。
