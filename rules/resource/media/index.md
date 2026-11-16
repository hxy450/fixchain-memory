# 图片和矢量图

源端 drawable 下有位图和 <vector>、<animated-vector>，布局或代码用 @drawable、R.drawable 引用图片，或 Compose 用 Icons.* 图标；目标端有 resources 下 media 目录里的图片和 SVG 时

## 触发族

- [矢量图标转 SVG 媒体资源](vector-to-svg/index.md)（10 条）：源 drawable 是 <vector>（android:pathData、viewportWidth / viewportHeight、fillColor 可能是 ?attr）或 <animated-vector>，Compose 用 Icons.Rounded.* 一类命名图标；产物里删掉矢量改用字符，SVG 的 viewBox 取了 dp 尺寸、fill 写成 none，路径凭记忆写，或动画矢量没在 resource-mapping 里标 unmappable
- [布局和代码引用的 @drawable 位图](drawable-bitmaps/index.md)（1 条）：源布局或代码引用 @drawable/…、R.drawable.…（ImageView 的 android:src、TextView 的 android:background），图在 drawable-xxhdpi 等密度目录；目标 resources/base/media 下没有这些原图，页面改成纯 Text，或拿近名、带后缀的别的图顶替
