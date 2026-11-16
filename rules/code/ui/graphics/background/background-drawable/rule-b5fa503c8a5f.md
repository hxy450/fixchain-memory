# 背景图带透明边缘时，目标的底色取页面背景色，不垫品牌色

审的是：代码
触发（任一种）：
- 读到：源布局头部容器的 android:background=@drawable/… 是带透明边缘（波浪、弧形收口）的位图；写错的样子：目标在 .backgroundImage($r('app.media.…')) 的组件上或下面垫了 .backgroundColor(...) 品牌色，透明处露出色块，弧形收口不见
适用范围：源布局里带透明边缘的背景位图迁成 ArkUI 组件背景时
做法：
- 背景图所在组件的底色与页面背景取同一个值（源页面背景色），写 .backgroundImage($r('app.media.<源 drawable 名>')) 配 .backgroundColor(<页面背景色>)，不用品牌色
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- backgroundColor(value: ResourceColor): T：组件底色，在背景图透明处露出来（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundColor）
- backgroundImage(src: ResourceStr | PixelMap, repeat?: ImageRepeat): T：组件背景图（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundImage）
- backgroundImage(src: ResourceStr | PixelMap, options?: BackgroundImageOptions): T：同族接口：带 BackgroundImageOptions 的背景图重载（@since 18）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.backgroundImage）
针对本应用要查的：
- 页面背景色：源工程布局 XML 里页面根布局（或包住头部的外层容器）的 android:background；根布局没写时看 Activity 主题的 android:windowBackground；读出颜色值，目标页面根容器和头部组件的 backgroundColor 都写这个值
来源：1 张卡，1 个应用
- case-d827908975df4e90ae2b（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 2、诊断
