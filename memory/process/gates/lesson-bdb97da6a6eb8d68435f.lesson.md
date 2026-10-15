# 运行会改写源码的自愈脚本后先审阅其改动；异常尺寸、与已有显式尺寸重复或按错误密度换算的追加要回滚

ID：`lesson-bdb97da6a6eb8d68435f` · 版本：4

[本主题](index.md)

## 何时使用

结构收口阶段运行含图标尺寸自愈等会改写 .ets 的检测管线、决定是否接受其结果时；构建或验证阶段读到同一组件出现两组尺寸修饰时

## 适用情境

迁移管线在收口时自动运行图标尺寸自愈（icon-sizing 一类），会直接给 .ets 中的 Image 追加 .width/.height；页面 Image 已在同一行链式写好尺寸，资源可能是 jpg 启动图标。也包括自愈脚本按“媒体像素 ÷ 源密度”换算由 vector drawable 转来的 SVG，或源 drawable 位于无密度限定的 drawable/ 目录时脚本自行假定一个高密度回退，把图片写小。

## 原因

自愈脚本读错图片像素时，会在已定尺寸后追加异常大的宽高；ArkUI 后写生效，组件铺满屏幕，编译与检测计数都不报错。vector drawable 的 android:width/height 已是 dp，转成 SVG 后没有密度桶可依；安卓把无限定的 drawable/ 当作 mdpi（1x）基准（android-36.1 DisplayMetrics.DENSITY_DEFAULT = DENSITY_MEDIUM，BitmapFactory 对默认密度按此解码），脚本按其他密度回退相除后直接写回代码，改动不易被察觉。

## 做法

1. 跑完会改写源码的自愈脚本后，先读其改动记录（结果 JSON）或 git diff，再看检测收敛结果；新增尺寸远超屏幕（上万 vp）或与同组件已有显式 width/height 重复时，回滚该处并上报。
2. 图标尺寸自愈只处理缺少尺寸的 Image；同一组件已有显式尺寸的跳过，读不出合法像素尺寸时不写入。
3. 构建或验证中读到同一组件出现两组 width/height 时，按后写生效核对最终尺寸，异常值当场删除或上报。
4. 遇到 vector drawable 转来的 SVG 不做 ÷density，尺寸取源 drawable 的 android:width/height（已是 dp）；源图在无限定 drawable/ 目录时，安卓按 mdpi（1x）看待它，脚本按其他密度回退得出的结果只报告、不写回。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-500cf2e63e19988f0420](../../../store/cases/case-500cf2e63e19988f0420/616fd28a8d66d19b0a16cf8321628b824302afc7e0c2337064550223b689ef08.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`616fd28a8d66d19b0a16cf8321628b824302afc7e0c2337064550223b689ef08`
- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis, recommendation:7
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
