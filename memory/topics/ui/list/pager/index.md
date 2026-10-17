# ui/list/pager

ViewPager 到 Swiper：页数与禁滑方式、初始页用 index 绑定、自绘 tab 双向联动与日历翻页容器

[上一级](../index.md)

## 本级经验

- [ViewPager 定页阈值与归位时长按其规则落实](lesson-fc05d6dfe9844a88815b.lesson.md) · 阶段：spec/execute · 信号：ViewPager, Swiper, determineTargetPage, smoothScrollTo
- [分页日历相邻页并发查询，Swiper 落定后一次提交](lesson-85b33ff729ab0514a20a.lesson.md) · 阶段：execute/repair · 信号：Swiper, Canvas, onAnimationEnd, onGestureSwipe
- [初始页用 Swiper.index，非 onReady 切页](lesson-ccccf83dc93ae809ccfb.lesson.md) · 阶段：execute · 信号：Swiper.index, changeIndex, onReady, SwiperController
- [单页不用 Swiper；禁滑用 disableSwipe](lesson-540747e352d7f006016d.lesson.md) · 阶段：spec/execute · 信号：ViewPager2, disableSwipe, isUserInputEnabled, Swiper
- [自绘 tab 加 Swiper 双向联动分别接通](lesson-27aa2e80a3a4d7724450.lesson.md) · 阶段：execute · 信号：ViewPager2, onPageSelected, setCurrentItem, currentItem
- [自绘日历翻页用 Swiper 承载，每页一 Canvas](lesson-d4e63d27885d9e348723.lesson.md) · 阶段：execute/repair · 信号：Swiper, Canvas, PanGesture, ViewPager2
