# centerInside 或 wrap_content 的图标按资源固有 dp 显示，外层保留触摸盒；ImageFit.Contain 会放大小图标

ID：`lesson-bdc493f5950835f9bfcc` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 ImageButton/ImageView 的固定触摸盒与 scaleType、或 wrap_content/drawableLeft 图标翻译成 ArkUI Image 尺寸时；复用已完成页面的控件行时

## 适用情境

源图标按钮是固定 dp 盒加 scaleType=centerInside，或图标以 wrap_content、TextView drawableLeft/Start 显示，渲染尺寸取决于资源像素与密度目录；映射参考把 centerInside 对到 ImageFit.Contain。

## 原因

centerInside 只缩不放，小于盒子的图标按固有尺寸居中；Contain 会等比放大到盒子，图标被放大成触摸盒尺寸。wrap_content 图标没有写尺寸时，写者常凭经验值或相邻控件猜值。来源中播放页生成者照映射表写成满盒 Contain，另一页以它为范式照抄；弹层写者只确认资源存在就写了经验值。

## 做法

1. 查图标资源所在的密度目录，按像素换算固有 dp（xhdpi 为 px/2）；外层保留源触摸盒并居中，内层 Image 设固有 dp，不要把 Image 设成盒子尺寸再用 Contain。
2. 映射表写 centerInside → Contain 时，先判断图标是否小于盒子：小于就按固有尺寸显示，只有大于盒子才缩小。
3. wrap_content 或 drawableLeft 图标同样取资源固有 dp；输入里没有资源尺寸时先读取图片尺寸，不用经验值占位。

## 可选检查

仅在适用条件不确定、与当前输入冲突或需要验证关键假设时按需执行；优先复用已有证据和正常测试。
不因读取本条经验而额外启动验证流程；项目原有必需测试照常执行。

- dumpLayout 读取图标 bounds 除以屏幕密度，与 Android 固有 dp 逐项对比。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-747484a613e86334516d · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`eaae961f5765e01e237e4579fed0b6a2ee1d5afd78e6bc1a93150013aea6017c`
- case-e7f02c687378e98dc213 · 结论：diagnosis, recommendation:1
  卡片版本：`34fb4fceaba5843191b7ca3753e5a63734a28177ddfc53ad34bba5ee33994c01`
