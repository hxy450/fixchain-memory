# 源端是原生 ViewPager 时不用 Swiper 缺省，改用 Scroll 按 ViewPager 规则定页和归位

审的是：代码
触发（任一种）：
- 读到：源码 import androidx.viewpager.widget.ViewPager，或继承基于 ViewPager 的三方壳；映射参考写「ViewPager / ViewPager2 → Swiper」；写错的样子：写成 Swiper().index(...).loop(false).indicator(false).cachedCount(n).onChange(...)，只把 setOffscreenPageLimit 映成 cachedCount，定页和归位沿用 Swiper 缺省
适用范围：实现阶段，源端翻页容器是原生 ViewPager（无自定义 Scroller）、目标要对齐它的拖动释放手感时
做法：
- 横向 Scroll 跟手；onWillStopDragging((velocity) => …) 里按 ViewPager#determineTargetPage 定页：|位移| > 25vp 且 |速度| > 400vp/s 按速度方向，否则当前页 + 页内偏移 + 0.4（前进）/ 0.6（后退）取整
- 归位用 scroller.scrollTo({ xOffset: 目标页 × 页宽, animation: { duration, curve } })：duration 有速度时 4×round(1000×|distance/velocity|)，否则 (pageDelta+1)×100，上限 600ms；curve 为五次缓出 (t−1)^5+1
- offscreenPageLimit = n 时只保留 |index − current| ≤ n 的页
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onWillStopDragging(handler: OnWillStopDraggingCallback): T（@since 20）；OnWillStopDraggingCallback = (velocity: number) => void：松手时拿到速度，在这里定页（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ScrollableCommonMethod.onWillStopDragging）
- onDidStopDragging(handler: OnDidStopDraggingCallback): T（@since 21）；OnDidStopDraggingCallback = (willFling: boolean) => void：拖动结束后的回调，可在这里发起归位（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ScrollableCommonMethod.onDidStopDragging）
- ScrollAnimationOptions { duration?: number（默认 1000）; curve?: Curve | ICurve（默认 Curve.Ease） }：scrollTo 的动画参数，要显式给时长和曲线（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAnimationOptions）
- function customCurve(interpolate: (fraction: number) => number): ICurve：可把 (t−1)^5+1 写成自定义曲线（出处：鸿蒙 SDK 的 ets/api/@ohos.curves.d.ts，curves.customCurve）
- duration = 4 * Math.round(1000 * Math.abs(distance / velocity))；无速度时 (int) ((pageDelta + 1) * 100)；Math.min(duration, MAX_SETTLE_DURATION)；插值 t -= 1.0f; return t * t * t * t * t + 1.0f：归位时长和曲线（distance 按页宽一半加距离影响修正）（出处：com.android.internal.widget.ViewPager#smoothScrollTo（框架内部的同源实现））
- 改成横向 Scroll + onWillStopDragging 定页 + onDidStopDragging 五次缓出归位后，慢拖 55% 停留、65% 翻页、快划翻页、末页回弹与安卓一致：这套写法上机验证过（出处：卡里修好并验证过）
未核实：OnWillStopDraggingCallback 的 velocity 单位声明里没写；卡里没写归位曲线用哪个接口实现，customCurve 是按声明给的写法；卡里记的是鸿蒙 SDK API 24，本机核实用的是 API 23
来源：1 张卡，1 个应用
- case-1bee3e42eae9e1092ceb（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 1、诊断；做法第 3 步 ← 诊断；取值 6 ← 诊断
