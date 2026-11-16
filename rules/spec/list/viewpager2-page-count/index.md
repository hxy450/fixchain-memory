# ViewPager2 加 FragmentStateAdapter 的实际页数

agent 会看到什么：读到 ViewPager2 + FragmentStateAdapter，getItemCount 返回只含一个元素的 listOf(…) 的 size，currentItem = 1 之类切页入口在单页下无效或隐藏；规格按组件类型或 navigation_mode 写「ViewPager2 → Swiper」，还给不存在的页预置 Swiper index

## 规矩

- rule-8d54a979ba76｜ViewPager2 的适配器恒为 1 页时，规格写「静态单页、不可横滑」，不按类型映射成 Swiper｜读到：ViewPager2 + FragmentStateAdapter，getItemCount 返回只含一个元素的 listOf(…) 的 size；切页入口（currentItem = 1 之类）在单页下无效或隐藏；写错：规格的容器映射写「ViewPager2 → Swiper」，理由是页面元数据的 navigation_mode 或组件类型；还写了为源端不存在的页「预置 Swiper index」，没有「单页、不可横滑」这条行为约束
