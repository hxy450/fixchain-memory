# 源端翻页容器是 ViewPager（含三方壳封装）时按其松手定页与归位规则实现，不沿用 Swiper 缺省翻页物理

ID：`lesson-d854f88ae2bbf882e85f` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端 ViewPager（androidx/support ViewPager，或引导页、图库查看器等基于它的三方壳）选择目标翻页容器并写翻页交互约束时

## 适用情境

源 Activity 直接使用 ViewPager，或继承基于 ViewPager 的三方壳（库为 AAR、仓内无源码），未自定义 Scroller、未覆写定页；映射参考或规格只写「ViewPager → Swiper 标准映射」，目标准备用 Swiper(index, loop:false) 承接，只把 offscreenPageLimit 映成 cachedCount。

## 例外与边界

- 源端是 ViewPager2 等不基于 ViewPager 的翻页容器，或自定义了 Scroller、覆写了定页逻辑：按其自身实现另行核对
- 项目已批准沿用目标平台翻页物理并登记为差异

## 原因

ViewPager 的松手定页与归位是框架固定行为：位移与速度同时过阈值才按速度方向翻页，否则按页内偏移加截断系数取整；归位时长随速度或页差变化并有上限，曲线为五次缓出。Swiper 缺省按自身规则翻页（约过半即翻）并用自己的动画曲线；把结构映射当成行为等价，慢拖、短促快划与末页越界的落点和手感都与源端不同。三方壳在仓库里没有源码，也不等于没有可核行为。

## 做法

1. 先确认实际翻页容器：源端直接使用 ViewPager，或三方壳制品中的翻页视图继承 ViewPager 且未自定义 Scroller、未覆写定页时适用本条；壳没有仓内源码就解包制品核对，不把映射表的「ViewPager → Swiper」当作行为等价。
2. 规格行为约束写出定页与归位规则（出处：androidx.viewpager.widget.ViewPager.java 的 determineTargetPage 与 smoothScrollTo，support 库同名类一致；用前对照所用依赖版本）：松手时总位移 > MIN_DISTANCE_FOR_FLING（25dp）且速度 > MIN_FLING_VELOCITY（400dp/s），速度为正（手指右移）落到 currentPage、否则 currentPage + 1；未达阈值时 targetPage = currentPage + (int)(pageOffset + truncator)，currentPage 为左缘所在页、pageOffset 为其滑出比例，truncator 在 currentPage ≥ 当前项时取 0.4、否则 0.6，即两个方向都要拖过约六成页宽才翻页。归位时长：速度 > 0 时为 4 × round(1000 × |distance / velocity|) ms（distance 为半页宽经 distanceInfluenceForSnapDuration 修正的距离），否则 (pageDelta + 1) × 100 ms，上限 MAX_SETTLE_DURATION 600ms，插值 f(t) = (t − 1)^5 + 1；offscreenPageLimit 一并写出。
3. 实现前在本机 SDK 的 swiper.d.ts 核对能否设置松手翻页阈值与按速度计算的归位时长；不能时改用横向 Scroll 承载各页、拖动跟手，在松手回调（SDK 提供 onWillStopDragging 时取其速度）按上式算目标页，再按归位时长与五次缓出滚到页边，保留页按 offscreenPageLimit（当前页两侧各 N 页）。规格没写翻页物理时实现者按上式补齐并回报规格缺项。

## 可选检查

- 有参照机时，两端分别做慢拖约五成半与六成半后松手、短促快划、末页越界四种手势，落点应一致。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-1bee3e42eae9e1092ceb](../../../store/cases/case-1bee3e42eae9e1092ceb/341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063`
