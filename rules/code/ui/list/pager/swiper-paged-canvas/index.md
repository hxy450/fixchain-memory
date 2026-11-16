# 逐页承载自绘视图的 Swiper 翻页

agent 会看到什么：读到 ViewPager2 逐页承载自绘的月、周视图并在翻页时加载相邻页；产物里是单个 Canvas 加 PanGesture 手动翻页，或在 onGestureSwipe 里直接写 Canvas 绑定的状态

## 规矩

- rule-7553a16b5668｜源端用 ViewPager2 逐页承载自绘月/周视图时，目标用 Swiper 三页各放一个 Canvas｜读到：布局里 `androidx.viewpager2.widget.ViewPager2`（或 RecyclerView）逐页承载月、周视图，registerOnPageChangeCallback / onPageSelected 里切月；写错：ArkTS 只有一个 Canvas，用 PanGesture 改 pageOffsetX 手动翻页，修复时只调拖动阈值、回弹曲线和动画时长
- rule-5f1b4f791944｜相邻页数据按源端先合并再一次提交，拖动中只写缓存，Swiper 落定后再替换｜读到：源端并发查询当前、上、下月，await 后合并成 map，再一次调用 setEventData 一类的提交方法；写错：ArkTS 在 onGestureSwipe 里触发预加载，结果在拖动中直接写进 Canvas 绑定的状态，落定后 onChange 又刷新一次
