# 三方库渲染的页面和控件

agent 会看到什么：读到 Activity 继承三方库的类、布局里只有库的自定义 View 节点、库的 PagerAdapter / ViewPager 子类填页，或调用库的配置方法；产物里注释写「库源不可见 → 自绘近似」、尺寸和动画常量凭猜测，或 Swiper + Image 少了库视图自带的手势

## 规矩

- rule-5381be4ba0de｜图片 ViewPager 来自三方库时，先列库内视图类，缩放平移等手势照库实现｜读到：源码 import it.feio.android.simplegallery 之类三方库的 GalleryPagerAdapter / GalleryViewPager 填充 ViewPager，逐页视图在库内；写错：目标写成 Swiper + Image(uri).objectFit(ImageFit.Contain)，没有双击缩放、捏合、平移、惯性和回弹，也没有放大后的边缘翻页判定
- rule-8d8e2a99a083｜源端 UI 由三方库 AAR 渲染时，目标按解包反编译得到的库真值实现，不凭猜测近似｜读到：Activity extends 三方库类（如 AppIntro2），或布局里只有库的自定义 View 节点（如 com.larswerkman.holocolorpicker.ColorPicker 加 SVBar、OpacityBar），调用代码里有 addSVBar / addOpacityBar 之类库方法；写错：代码注释写「库源不可见 → 自绘近似」「源码不在本仓库 → 按 spec 自研等价」，圆点直径、间距、透明度、色环厚度等常量凭猜测或反推自 README
