# 图片 ViewPager 来自三方库时，先列库内视图类，缩放平移等手势照库实现

审的是：代码
触发（任一种）：
- 读到：源码 import it.feio.android.simplegallery 之类三方库的 GalleryPagerAdapter / GalleryViewPager 填充 ViewPager，逐页视图在库内；写错的样子：目标写成 Swiper + Image(uri).objectFit(ImageFit.Contain)，没有双击缩放、捏合、平移、惯性和回弹，也没有放大后的边缘翻页判定
适用范围：源端图片查看器或分页视图由三方库提供时
做法：
- 先列出库内所有视图类（如 simplegallery 的 TouchImageView），再判断 Swiper + Image 是否足够
- 库视图自带的缩放、平移、双击、惯性、回弹属于既有行为，照库实现，不当作可省略的增强项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 按库里 TouchImageView 重建缩放、平移、fling、回弹后与源端一致：修复后的做法（出处：卡里修好并验证过）
针对本应用要查的：
- 库内的视图类和手势：库 AAR 反编译后的视图类清单（views 包），以及 res/layout；找出逐页使用的视图类，读它处理的手势（双击、捏合、拖动、惯性、边界回弹）和参数
来源：1 张卡，1 个应用
- case-74b07cb94daa311f36b1（omni-notes-hmos）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 4、诊断；取值 1 ← 诊断
