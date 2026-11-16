# ViewPager 翻页的释放定页和归位动画

agent 会看到什么：读到源码 import androidx.viewpager.widget.ViewPager（OnPageChangeListener、setOffscreenPageLimit），或 Activity 继承基于 ViewPager 的三方壳（如 AppIntro2）、库是 AAR 没有源码；规格只写「ViewPager → Swiper 标准映射」「默认即可对齐」「三方库无源码 → 按 Swiper 自研」，没有释放阈值、归位时长和曲线

## 规矩

- rule-d2628265ae84｜源页面用 ViewPager（含三方壳封装）时，规格写出释放定页、归位时长曲线和 offscreenPageLimit｜读到：源码 import androidx.viewpager.widget.ViewPager（OnPageChangeListener、setOffscreenPageLimit），或 Activity 继承基于 ViewPager 的三方壳（如 AppIntro2），库是 AAR、仓内无源码；写错：规格只写「ViewPager → Swiper 标准映射」「Swiper 为翻页标准容器」「默认即可对齐」「三方库无源码 → 按 Swiper 自研」，没有释放阈值、归位时长和曲线
