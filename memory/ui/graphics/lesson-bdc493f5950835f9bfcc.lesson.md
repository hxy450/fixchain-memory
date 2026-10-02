# centerInside、wrap_content 或未设尺寸的图片按资源固有 dp 显示，外层保留触摸盒；ImageFit.Contain 会放大小图标

ID：`lesson-bdc493f5950835f9bfcc` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时；为不设尺寸的 Compose Image(painterResource) 确定目标尺寸时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。也包括 Compose Image(painterResource(vector drawable)) 不设尺寸、按 drawable 声明的 dp 固有尺寸与 ContentScale.Fit 显示，目标 SVG 由 vector drawable 转来。

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。另一应用把 wrap_content 加 10dp padding 的切换图片写成 34×34 固定框再叠 padding(10)，可视图形只剩约 14vp，修复按 180×81px 资源改为 60×30vp、Contain。由 vector drawable 转来的 SVG，其 width/height 已是 dp，再按密度目录相除会把图缩小数倍。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位；源端图片另带 padding 时，按固有比例定宽高后再加 padding，不用固定正方形框再叠 padding 压缩可视图形。
4. 资源是 vector drawable 转来的 SVG 时，固有尺寸取源 drawable 的 android:width/height（dp），不再除密度；源端按 Fit 显示、可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。

## 可选检查

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

来源支持：4 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-747484a613e86334516d](../../../store/cases/case-747484a613e86334516d/c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9`
- [case-9d7fa754a567e2ecec7e](../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：recommendation:4
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
- [case-e7f02c687378e98dc213](../../../store/cases/case-e7f02c687378e98dc213/f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8.json) · 结论：diagnosis, recommendation:1
  卡片版本：`f677d5dd553cd45d59f7923188d8619553ab21da646d51a68e575b3586c406c8`
