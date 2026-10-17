# ViewPager（含三方库封装的）迁 Swiper 只是结构对应：释放定页阈值、归位时长与曲线按 ViewPager 规则落实

ID：`lesson-fc05d6dfe9844a88815b` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端 ViewPager 页面确定目标翻页容器与需保留的拖动定页行为时

## 适用情境

源端用 androidx/support ViewPager，或 AppIntro、图库类三方库内部的 ViewPager；映射参考写“ViewPager → Swiper 标准映射”，目标准备沿用 Swiper 缺省的翻页阈值与回弹曲线。

## 例外与边界

- 源端是 ViewPager2（RecyclerView 加 PagerSnapHelper 定页），规则不同，按其源实现核对
- 决策台账以决策 ID 批准沿用目标容器缺省物理

## 原因

ViewPager 的抬手定页与归位动画是框架固定实现，不在应用源码里；Swiper 缺省的定页阈值与回弹曲线不同，且不开放这些参数，直接替换后慢拖、快划与末页越界的结果都与源端不一致。

## 做法

1. 规格写出 ViewPager 的定页与归位规则（androidx ViewPager.java 的 determineTargetPage 与 smoothScrollTo）：抬手位移超过 25dp（MIN_DISTANCE_FOR_FLING）且速度超过 400dp/s（MIN_FLING_VELOCITY）时按速度方向翻页，否则目标页 = 当前页 + (int)(页内偏移 + 截断量)，向后翻取 0.4、回退取 0.6；归位时长有速度时为 4 × round(1000 × |distance / velocity|) ms，否则为 (pageDelta + 1) × 100 ms，上限 600ms（MAX_SETTLE_DURATION），插值为 (t − 1)^5 + 1；offscreenPageLimit 一并写出。
2. Swiper 无法设定这些阈值与曲线时，改用横向 Scroll 加手势跟手，停止拖动时按上式定页，再按上式时长与曲线滚动归位；只保留源 offscreenPageLimit 范围内的页。
3. 三方翻页库仓内无源码时，先从依赖缓存或 AAR 反编译确认其容器是否原生 ViewPager、有无自定义 Scroller，再选规则。
4. 实现者收到只写“ViewPager → Swiper”的规格时，按第一步补定页与归位，或把缺口回报规格。

## 可选检查

- 在两端比较慢拖略过半停留、略多翻页、短促快划与末页越界四种手势的结果。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-1bee3e42eae9e1092ceb](../../../store/cases/case-1bee3e42eae9e1092ceb/341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`341c9452897eb8bf11090c600c5a436b37e1c719e3b0ce1f9227c30a577fb063`
