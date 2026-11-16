# 翻页与标签页

源端有 ViewPager / ViewPager2、TabLayout 和它承载的子 Fragment，目标端有 Swiper、Tabs、TabContent、.tabBar、SwiperController 时

## 触发族

- [Swiper 的当前页和选中同步](swiper-index-sync/index.md)（8 条）：读到 ViewPager2 的 setCurrentItem / currentItem、onPageSelected 和 tab 点击切页；产物里 Swiper 的 .index(...)、SwiperController.changeIndex、.onChange 回写，以及父子组件之间 selectedIndex 的同步
- [逐页承载自绘视图的 Swiper 翻页](swiper-paged-canvas/index.md)（2 条）：读到 ViewPager2 逐页承载自绘的月、周视图并在翻页时加载相邻页；产物里是单个 Canvas 加 PanGesture 手动翻页，或在 onGestureSwipe 里直接写 Canvas 绑定的状态
- [Swiper 禁止滑动和容器的触摸拦截](swiper-swipe-disable/index.md)（3 条）：读到 ViewPager2 的 isUserInputEnabled = false、只有一页或拦截触摸；产物里 Swiper、Tabs、Stack 上的 .enabled(false)、disableSwipe、hitTestBehavior
- [ViewPager / Tab 承载的子 Fragment 页](pager-child-pages/index.md)（4 条）：读到 TabLayout / ViewPager 配了子 Fragment 列表；产物里 Tabs、Swiper 子页的内容和列表项、@Builder 槽位的参数、子页拿的导航栈，以及决定建几个子页的解析结果
- [TabContent 的 .tabBar 参数](tabcontent-tabbar-arg/index.md)（1 条）：产物里 TabContent 上 .tabBar(...) 传的是 { title: '…' } 这类不在任何重载里的对象字面量（编译报 10505001 No overload matches this call），还是字符串、@Builder、TabBarOptions
- [Web Swiper 组件的分页点和导航箭头](web-swiper-pagination-nav/index.md)（5 条）：读到源端（Web）的 Swiper 组件带 pagination、navigation，只 import 'swiper/css/…' 默认样式、没有 --swiper-theme-color 或样式覆盖；产物里自建分页点和导航箭头的形状、颜色（是否用了应用 accent 和令牌）、叠放位置和箭头素材
- [原生 ViewPager 的定页和归位](viewpager-snap-settle/index.md)（1 条）：读到 androidx ViewPager（或基于它的三方壳）的 setCurrentItem、setOffscreenPageLimit、OnPageChangeListener，映射参考写 ViewPager → Swiper；产物里 Swiper 只配了 index、loop、cachedCount、onChange，松手后的定页和归位沿用 Swiper 缺省
