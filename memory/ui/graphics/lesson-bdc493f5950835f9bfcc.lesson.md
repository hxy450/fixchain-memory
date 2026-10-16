# 图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸

ID：`lesson-bdc493f5950835f9bfcc` · 版本：10

[本主题](index.md)

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时；把 GridView/ListView 适配器条目或 LinearLayout 权重行里的 wrap_content 位图确定盒尺寸时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。 也包括多个列表页共用的推广卡片里，角标 ImageView 为 wrap_content 加 centerInside，位图在 drawable-xxhdpi，媒体留给后续批次拷贝。也包括 ImageView 用 padding 缩小可见图形（如圆形垫底），目标准备换成纯色形状。也包括轮播标题图一类 wrap_content ImageView，位图只在 drawable-xhdpi，目标 Image 只设 objectFit、未设宽高，映射参考写“wrap_content → 无需设置，自动适应”。 也包括 GridView/ListView 适配器条目里 wrap_content 的 ImageView，或纵向 LinearLayout 里 wrap_content 加 layout_weight 的 ImageView：未设 adjustViewBounds，位图只在低密度目录（如 drawable-ldpi），按设备密度放大后宽于列宽或父宽。

## 例外与边界

- 图片位于权重行或定尺寸父格中、固有尺寸大于父级可给的空间时：只在父级给出上限的那一轴夹紧图片盒，位图在盒内等比缩小（FIT_CENTER/Contain），不按固有尺寸溢出，也不填经验值；写后与源端截图核对盒位置。ImageView 未设 adjustViewBounds（默认 false）时 onMeasure 对宽、高分别 resolveSize，未超限的轴仍是密度缩放后的固有尺寸，盒子不等比收缩，这个尺寸也是 LinearLayout 量子项、分余量所用的自然尺寸；GridView/ListView 只把条目宽定为列宽，条目高按 UNSPECIFIED 测得（固有高加条目 padding），不为套用本例外给格子补宽高比（如 aspectRatio(1)）。只有 adjustViewBounds=true 时盒子才按位图比例收缩。固有像素按 Bitmap.scaleFromDensity 取整：(px×设备dpi+目录dpi/2)/目录dpi（本机 android-36.1 源码 Bitmap.java）

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。另一应用中写者复刻绑定手机号弹窗时，同轮已按 hdpi 换算了两张插图，输入行的 drawableLeft 图标却照抄仓内同族页面的 24×24，源图标实为 20×29px、24×28px@hdpi（约 13×19、16×19vp）。 ArkUI 同一组件后设的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 把 72px 的 xxhdpi 图标放大到约 40vp。另一应用的漫画阅读顶栏如此，写者已读到原图 72×72px 与 xxhdpi 来源，仍按未换算的 32vp 加槽位宽高写出。 父格往往只在一个轴上定尺寸：ImageView 未设 adjustViewBounds 时只有超限的轴被夹紧，centerInside/FIT_CENTER 只让位图在盒内缩小绘制，盒子本身不等比收缩；把盒子按宽高比缩小，或给列表格子补方形比例，会改变行高、行距与一屏可见行数。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。仓内同族页面已有的图标尺寸本身也是迁移产物，不能代替对源资源的换算。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
5. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row，Image 只设图标尺寸，不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。xxhdpi 资源按 px/3 换算（72×72px → 24×24vp，74×72px → 约 25×24vp），换资源后重新核对；槽宽取源布局的承载区宽度，与图标绘制尺寸分开核对。
6. 媒体留给后续批次拷贝时，尺寸仍在本页按源资源像素写定，或登记成可机械校验的交接，不只记“待资源 sweep”。
7. 带 padding 的 ImageView 背景图换成纯色形状时，可见尺寸取布局尺寸减 padding，padding 并入外边距，与同位的热区或进度环保持同心。
8. 多张位图像素不同时逐项换算，或取统一外框配合 Contain；自检已测得位图像素时回到对应 Image 核对宽高是否写入，不只检查 objectFit。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：12 张卡 · 10 次迁移 · 10 个应用

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
- [case-85db2e28957bc67387d9](../../../store/cases/case-85db2e28957bc67387d9/20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`20bff0cc2958613a8fe30f66317dc6e21b1990b04b3a795803527480b673f1a3`
- [case-9d7fa754a567e2ecec7e](../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：recommendation:4
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-ae26f8358584821ce4d4](../../../store/cases/case-ae26f8358584821ce4d4/739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364`
- [case-b911ada02f4ec55d7d14](../../../store/cases/case-b911ada02f4ec55d7d14/fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325`
- [case-bf7423609eeb65569b09](../../../store/cases/case-bf7423609eeb65569b09/be540d4029c933ce5a51a7108abccc29a3abe58fc5271ff5da0cf0a61f03561b.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`be540d4029c933ce5a51a7108abccc29a3abe58fc5271ff5da0cf0a61f03561b`
- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
- [case-e7f02c687378e98dc213](../../../store/cases/case-e7f02c687378e98dc213/f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8`
