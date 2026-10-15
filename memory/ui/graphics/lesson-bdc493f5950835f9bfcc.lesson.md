# 位图图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 图标不设成盒子尺寸再 Contain

ID：`lesson-bdc493f5950835f9bfcc` · 版本：12

[本主题](index.md)

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain，或写“wrap_content → 无需设置，自动适应”。也包括工具栏按钮原本在组件上链式设置点击区宽高，替换成位图后又在同一 Image 上写图标宽高；多个列表页共用的推广角标；媒体留给后续批次拷贝；ImageView 用 padding 缩小可见图形、目标准备换成纯色形状。

## 例外与边界

- 图片位于权重行、列表或网格条目等只在一个轴上受限的父级中、固有尺寸超出该轴可给的空间时：ImageView 未设 adjustViewBounds（默认 false）时只夹紧超限的那一轴，另一轴保持密度缩放后的固有尺寸，盒子不等比收缩，FIT_CENTER/centerInside 只让位图在盒内等比缩小绘制；GridView/ListView 条目宽由列宽定死、高按 UNSPECIFIED 量出，格高＝固有高＋条目 padding。不为套用夹紧补宽高比（如 aspectRatio(1)）、不填经验值；只有 adjustViewBounds=true 时盒子才按宽高比收缩。查值：布局 XML 的 adjustViewBounds、layout_width/height、scaleType，res/drawable-<密度> 下的像素，固有像素＝(px×设备dpi＋目录dpi/2)/目录dpi（Bitmap.scaleFromDensity），Adapter.getView 的 setLayoutParams/setPadding；机制见 ImageView.onMeasure 与 GridView 对子项的 UNSPECIFIED 测量。写后与源端截图核对盒位置
- 资源是 vector drawable 转来的 SVG：固有尺寸取源 drawable 的 android:width/height（dp），不按密度目录换算

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。位图的固有 dp 由像素与所在密度目录决定（dp = px ÷ (目录 dpi/160)），没写尺寸时写者常凭经验值、相邻控件或仓内同族页面猜值，而这些已有值本身也是迁移产物。ArkUI 同一组件上后写的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 再把图标放大。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2，xxhdpi 为 px/3）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不把 Image 设成盒子尺寸再用 Contain。映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
2. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位，也不照抄仓内同族页面的尺寸。源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。
3. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row（槽宽取源布局的承载区宽度），Image 只设图标尺寸；不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。更换资源后重新换算。
4. 媒体留给后续批次拷贝时，尺寸仍按源资源像素在本页写定；源资源像素在 Android 仓里就能读到，不依赖媒体是否已拷贝。
5. ImageView 用 padding 缩小可见图形、目标换成纯色形状时，先分清资源属于哪个属性：android:src 的可见尺寸取布局尺寸减 padding（ImageView.java 在扣除 padding 的内容区绘制 src），padding 并入外边距，与同位的热区或进度环保持同心；android:background 铺满整个 View，padding 不缩小它（View.java setBackgroundBounds 按整个 View 设 bounds）。
6. 多张位图像素不同时逐项换算，或取统一外框配合 Contain；自检已测得位图像素时回到对应 Image 核对宽高是否写入，不只检查 objectFit。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：11 张卡 · 9 次迁移 · 9 个应用

## 来源（按需复核）

- [case-47b9e1107e4e4ecd40bd](../../../store/cases/case-47b9e1107e4e4ecd40bd/87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98.json) · 结论：recommendation:4
  卡片版本：`87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98`
- [case-4e7e0e12d7b6b08c08b0](../../../store/cases/case-4e7e0e12d7b6b08c08b0/01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115.json) · 结论：recommendation:2
  卡片版本：`01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115`
- [case-50d5978491b9ba48b899](../../../store/cases/case-50d5978491b9ba48b899/1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`1d0dc9fa70cf068c678afcbb27308a85366c39290f03c618b36fc6bcf443b897`
- [case-747484a613e86334516d](../../../store/cases/case-747484a613e86334516d/c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9`
- [case-84754321501fb68838ca](../../../store/cases/case-84754321501fb68838ca/3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a`
- [case-85db2e28957bc67387d9](../../../store/cases/case-85db2e28957bc67387d9/20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3.json) · 结论：diagnosis, recommendation:3
  卡片版本：`20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3`
- [case-9d7fa754a567e2ecec7e](../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：recommendation:4
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-ae26f8358584821ce4d4](../../../store/cases/case-ae26f8358584821ce4d4/739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364`
- [case-b911ada02f4ec55d7d14](../../../store/cases/case-b911ada02f4ec55d7d14/fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325`
- [case-bf7423609eeb65569b09](../../../store/cases/case-bf7423609eeb65569b09/be540d4029c933ce5a51a7108abccc29a3abe58fc5271ff5da0cf0a61f03561b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`be540d4029c933ce5a51a7108abccc29a3abe58fc5271ff5da0cf0a61f03561b`
- [case-e7f02c687378e98dc213](../../../store/cases/case-e7f02c687378e98dc213/f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8`
