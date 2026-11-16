# 原生 ViewPager 的定页和归位

agent 会看到什么：读到 androidx ViewPager（或基于它的三方壳）的 setCurrentItem、setOffscreenPageLimit、OnPageChangeListener，映射参考写 ViewPager → Swiper；产物里 Swiper 只配了 index、loop、cachedCount、onChange，松手后的定页和归位沿用 Swiper 缺省

## 规矩

- rule-b2b1c2e73c05｜源端是原生 ViewPager 时不用 Swiper 缺省，改用 Scroll 按 ViewPager 规则定页和归位｜读到：源码 import androidx.viewpager.widget.ViewPager，或继承基于 ViewPager 的三方壳；映射参考写「ViewPager / ViewPager2 → Swiper」；写错：写成 Swiper().index(...).loop(false).indicator(false).cachedCount(n).onChange(...)，只把 setOffscreenPageLimit 映成 cachedCount，定页和归位沿用 Swiper 缺省
