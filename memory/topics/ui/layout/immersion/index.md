# ui/layout/immersion

安全区沉浸：是否全屏、系统栏底色与避让带由哪一层承担

[上一级](../index.md)

## 本级经验

- [Tab 宿主不统一加顶部安全区，按子页源处理分别避让](lesson-48e9408812c28e934db8.lesson.md) · 阶段：spec/execute · 信号：ImmersionBar, statusBarView, titleBarMarginTop, fitsSystemWindows
- [expandSafeArea 非避让，前景按避让区补内距](lesson-a8452bfea5d42d3dcae3.lesson.md) · 阶段：execute · 信号：expandSafeArea, setWindowLayoutFullScreen, getWindowAvoidArea, TYPE_SYSTEM
- [根视图状态栏 padding 与底色由页面容器承担](lesson-baf0ca22a69e7b76f636.lesson.md) · 阶段：spec/execute · 信号：setPadding, DecorView, setBackgroundColor, statusBarColor
- [源窗口延伸到系统栏下才全屏，底部避让加在屏底层](lesson-0e1c846868f2683cc280.lesson.md) · 阶段：spec/execute · 信号：getWindowAvoidArea, TYPE_NAVIGATION_INDICATOR, TYPE_SYSTEM, bottomRect
- [状态栏实色带挂外层 Column，把 Tabs 包进该层](lesson-fe10bd2491ca4ba82cb5.lesson.md) · 阶段：execute/repair · 信号：Tabs, TabContent, Column, Swiper
