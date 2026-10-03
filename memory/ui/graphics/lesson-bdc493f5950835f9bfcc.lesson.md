# 图标按资源固有 dp 显示、触摸盒放在外层：centerInside、wrap_content 或未设尺寸的图片不设成盒子尺寸再 Contain，同一 Image 上后写的槽位宽高会覆盖图标尺寸

ID：`lesson-bdc493f5950835f9bfcc` · 版本：5

[本主题](index.md)

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时；把工具栏的文字或系统符号按钮替换为位图 Image，确定图标显示尺寸与点击热区时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。 也包括工具栏按钮原本在组件上链式设置点击区宽高（如 .width(40).height(48)），替换成位图后又在同一 Image 前面写图标宽高；源图标在 drawable-xxhdpi，目标资源放在不分密度的 base/media。

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。另一应用中写者复刻绑定手机号弹窗时，同轮已按 hdpi 换算了两张插图，输入行的 drawableLeft 图标却照抄仓内同族页面的 24×24，源图标实为 20×29px、24×28px@hdpi（约 13×19、16×19vp）。 ArkUI 同一组件后设的 width/height 覆盖前值，图片盒于是等于点击槽，Contain 把 72px 的 xxhdpi 图标放大到约 40vp。另一应用的漫画阅读顶栏如此，写者已读到原图 72×72px 与 xxhdpi 来源，仍按未换算的 32vp 加槽位宽高写出。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。仓内同族页面已有的图标尺寸本身也是迁移产物，不能代替对源资源的换算。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
5. 把文字或符号按钮换成位图时，点击槽宽高放在外层 Stack/Row，Image 只设图标尺寸，不在同一 Image 修饰链里先写图标尺寸、再保留原槽位宽高。xxhdpi 资源按 px/3 换算（72×72px → 24×24vp，74×72px → 约 25×24vp），换资源后重新核对；槽宽取源布局的承载区宽度，与图标绘制尺寸分开核对。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：6 张卡 · 5 次迁移 · 5 个应用

## 来源（按需复核）

- [case-747484a613e86334516d](../../../store/cases/case-747484a613e86334516d/c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9`
- [case-84754321501fb68838ca](../../../store/cases/case-84754321501fb68838ca/3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a.json) · 结论：diagnosis, recommendation:1
  卡片版本：`3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a`
- [case-9d7fa754a567e2ecec7e](../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：recommendation:4
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-b911ada02f4ec55d7d14](../../../store/cases/case-b911ada02f4ec55d7d14/fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fe131fcb00a86b1a6fedf2b0291f225bf231772f1bfc5b5af79e9d0729a16325`
- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
- [case-e7f02c687378e98dc213](../../../store/cases/case-e7f02c687378e98dc213/f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8`
