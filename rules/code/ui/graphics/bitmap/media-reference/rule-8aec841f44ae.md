# 源布局的 src、drawableStart、装饰 ImageView 逐项对上目标同名 $r 引用，不按外观挑图

审的是：代码
触发（任一种）：
- 读到：源布局里有 ImageView 的 android:src、TextView 的 android:drawableStart、只作装饰的 ImageView，引用的是 @drawable/…；写错的样子：目标组件少了对应的 Image(...)（按钮前的图标、角上的装饰图、列表行图标没画，或行做成没绑图标的空列表），或用了名字不同、外观相近的通用图标 $r('app.media.…')
适用范围：把安卓布局里带图片引用的页面迁成 ArkUI 组件、写完交回时
做法：
- 从源布局列出每个 android:src、android:drawableStart 和装饰 ImageView 引用的 drawable 名，逐项确认目标组件里有同名的 $r('app.media.<名>')（Image 或 backgroundImage），缺的补上
- 图标按源布局的 drawable 名取用，不从通用资源里按视觉相似挑
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <attr name="drawableStart" format="reference|color" />：TextView 文字起始侧画的 drawable；迁成目标时是文字前的一张图，不能丢（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextView 的 drawableStart（按应用的 compileSdk 取对应平台））
- (src: PixelMap | ResourceStr | DrawableDescriptor | ImageContent): ImageAttribute：Image 组件的构造，源 drawable 写成 Image($r('app.media.<名>'))（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageInterface）
- backgroundImage(src: ResourceStr | PixelMap, repeat?: ImageRepeat): T：android:background 引用的位图写成组件背景图（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundImage）
来源：1 张卡，1 个应用
- case-d827908975df4e90ae2b（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 3
