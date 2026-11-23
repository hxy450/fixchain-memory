# 源端翻页容器是 ViewPager（含三方壳封装）时按其松手定页与归位规则实现，不沿用 Swiper 缺省翻页物理

## 何时使用

规格提取与界面实现阶段，为源端 ViewPager（androidx/support ViewPager，或引导页、图库查看器等基于它的三方壳）选择目标翻页容器并写翻页交互约束时

## 适用情境

源 Activity 直接使用 ViewPager，或继承基于 ViewPager 的三方壳（库为 AAR、仓内无源码），未自定义 Scroller、未覆写定页；映射参考或规格只写「ViewPager → Swiper 标准映射」，目标准备用 Swiper(index, loop:false) 承接，只把 offscreenPageLimit 映成 cachedCount。

## 例外与边界

- 源端是 ViewPager2 等不基于 ViewPager 的翻页容器，或自定义了 Scroller、覆写了定页逻辑：按其自身实现另行核对
- 项目已批准沿用目标平台翻页物理并登记为差异
- 改用横向 Scroll 自行定页时，Swiper 原来顺带提供的东西要在新实现里补齐：源端 OnPageChangeListener 的选中页、滚动中、滚动状态回调，setCurrentItem 代码切页（带动画与不带动画两种），以及页面指示；只换掉翻页物理，不丢这些对外行为。

## 原因

ViewPager 的松手定页与归位是框架固定行为：位移与速度同时过阈值才按速度方向翻页，否则按页内偏移加截断系数取整；归位时长随速度或页差变化并有上限，曲线为五次缓出。Swiper 缺省按自身规则翻页（约过半即翻）并用自己的动画曲线；把结构映射当成行为等价，慢拖、短促快划与末页越界的落点和手感都与源端不同。三方壳在仓库里没有源码，也不等于没有可核行为。

## 做法

1. 先确认实际翻页容器：源端直接使用 ViewPager，或三方壳制品中的翻页视图继承 ViewPager 且未自定义 Scroller、未覆写定页时适用本条；壳没有仓内源码就解包制品核对，不把映射表的「ViewPager → Swiper」当作行为等价。
2. 规格行为约束写出定页与归位规则（出处：androidx.viewpager.widget.ViewPager.java 的 determineTargetPage 与 smoothScrollTo，support 库同名类一致；用前对照所用依赖版本）：松手时总位移 > MIN_DISTANCE_FOR_FLING（25dp）且速度 > MIN_FLING_VELOCITY（400dp/s），速度为正（手指右移）落到 currentPage、否则 currentPage + 1；未达阈值时 targetPage = currentPage + (int)(pageOffset + truncator)，currentPage 为左缘所在页、pageOffset 为其滑出比例，truncator 在 currentPage ≥ 当前项时取 0.4、否则 0.6，即两个方向都要拖过约六成页宽才翻页。归位时长：速度 > 0 时为 4 × round(1000 × |distance / velocity|) ms（distance 为半页宽经 distanceInfluenceForSnapDuration 修正的距离），否则 (pageDelta + 1) × 100 ms，上限 MAX_SETTLE_DURATION 600ms，插值 f(t) = (t − 1)^5 + 1；offscreenPageLimit 一并写出。
3. 实现前在本机 SDK 的 swiper.d.ts 核对能否设置松手翻页阈值与按速度计算的归位时长；不能时改用横向 Scroll 承载各页、拖动跟手，在松手回调（SDK 提供 onWillStopDragging 时取其速度，单位 vp/s，符号按内容滚动方向；ViewPager 以手指右移为正，代入上式前统一符号）按上式算目标页，再按归位时长与五次缓出滚到页边，保留页按 offscreenPageLimit（当前页两侧各 N 页）。规格没写翻页物理时实现者按上式补齐并回报规格缺项。

## 可选检查

- 有参照机时，两端分别做慢拖约五成半与六成半后松手、短促快划、末页越界四种手势，落点应一致。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码（com.android.internal.widget.ViewPager，support-v4 ViewPager 的框架内拷贝）。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕ViewPager 松手定页（从左到右布局）：总位移超过 MIN_DISTANCE_FOR_FLING 且速度超过 MIN_FLING_VELOCITY 时按速度方向定页（速度为负翻到下一页，否则留在当前左缘所在页）；未达阈值时按页内偏移加截断系数取整，截断系数在左缘所在页 ≥ 当前项时为 0.4、否则 0.6；框架内拷贝另有边缘拉伸时不按速度翻页的判断
- 〔原因 / 做法第 2 步〕ViewPager 的阈值常量：MIN_DISTANCE_FOR_FLING = 25dp，MIN_FLING_VELOCITY = 400dp/s（按屏幕密度换成像素），MAX_SETTLE_DURATION = 600ms
- 〔原因 / 做法第 2 步〕ViewPager 归位时长：速度不为 0 时为 4 × round(1000 × |distance / velocity|) 毫秒（distance 为半页宽经 distanceInfluenceForSnapDuration 修正），否则为 (|dx| / (页宽 + 页间距) + 1) × 100 毫秒，上限 600 毫秒；插值器为 (t − 1)^5 + 1
- 〔做法第 2 步〕ViewPager 没有另设 offscreenPageLimit 时为 1；设小于 1 的值时按 1 处理并打警告日志
- 〔原因〕Swiper 没有另设 curve 时动画曲线为 interpolatingSpring(-1, 1, 328, 34) 弹簧曲线
- 〔原因〕Swiper 按子元素翻页时，判定翻页的拖拽距离阈值为子元素宽度的 50%（按组翻页时为 Swiper 宽度的 50%）
- 〔做法第 3 步〕onWillStopDragging（API 20 起）在滚动组件滑动离手时触发，鼠标滚轮滑动不触发；回调的 velocity 是离手速度，单位 vp/s，内容向上滚动为正、向下为负
- 〔做法第 3 步〕onDidStopDragging（API 21 起）在滚动组件结束拖动时触发，参数 willFling 表示拖拽结束后是否还有惯性动效
- 〔做法第 3 步〕ScrollAnimationOptions 没有另设时 duration 为 1000 毫秒（小于 0 按默认值）、curve 为 Curve.Ease、canOverScroll 为 false
