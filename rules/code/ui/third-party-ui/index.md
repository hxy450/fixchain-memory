# 三方界面库

源端界面由三方库渲染：Activity 继承库的基类（如 AppIntro2）、布局里是库的自定义 View 节点（如 ColorPicker）、用库的 PagerAdapter / ViewPager 子类填页，目标端要照库里的尺寸、动画和手势写 ArkUI 时

## 触发族

- [三方库渲染的页面和控件](library-rendered-ui/index.md)（2 条）：读到 Activity 继承三方库的类、布局里只有库的自定义 View 节点、库的 PagerAdapter / ViewPager 子类填页，或调用库的配置方法；产物里注释写「库源不可见 → 自绘近似」、尺寸和动画常量凭猜测，或 Swiper + Image 少了库视图自带的手势
