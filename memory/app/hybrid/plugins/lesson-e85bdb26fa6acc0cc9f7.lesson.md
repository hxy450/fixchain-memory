# 兼容层把选图结果包装成原 API 对象（如 AssetEntity）交给冻结 Dart 业务时，按全部消费方保留宽高等元数据，不以 0 占位

ID：`lesson-e85bdb26fa6acc0cc9f7` · 版本：3

[本主题](index.md)

## 何时使用

插件兼容层实现或返修阶段，决定原 API 对象带哪些元数据，或为性能删改其中的计算时

## 适用情境

Flutter 应用 Dart 冻结；本地兼容包把系统选择器结果或缓存副本包装成 AssetEntity 等原 API 对象，经共享入口分发给多个业务页面；下游有页面用对象宽高计算比例；修复者准备为省去整图解码删掉尺寸计算。

## 原因

兼容层返回对象的字段是冻结业务依赖的公开契约，只按报告的那条流程改变字段，其他消费方就会出错：宽高写成 0 时，下游按宽高比计算得到 0/0，布局约束变成 NaN 并报错；只为读尺寸整图解码，则是多余的一次全图解码。

## 做法

1. 改写兼容层返回对象前，在整个 lib 中检索该对象及其字段的消费方（如 .width/.height、assets.first.width、传给下游页的 imageWidth/imageHeight），记下依赖的字段；不只过滤到报告的流程。
2. 宽高从文件头读取（ImageSource.getImageInfo，或读取头信息的库），需要时按 EXIF 方向交换；读取失败给非零兜底，不用 0 占位，也不为取尺寸整图解码。

## 可选检查

- 改动共享选图入口后，至少打开一个依赖宽高的页面核对布局。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-64090e208edc24d57300](../../../../store/cases/case-64090e208edc24d57300/0756a248ab4a76e6552d3400a0989a2b2c6dd261eb316f12770137719651c4fc.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`0756a248ab4a76e6552d3400a0989a2b2c6dd261eb316f12770137719651c4fc`
- [case-d166fd60d66832c204bc](../../../../store/cases/case-d166fd60d66832c204bc/4648fa06f0a9fabfb6528377404ad8649b35325131d57ed0913b90e17ab3d92f.json) · 结论：recommendation:3
  卡片版本：`4648fa06f0a9fabfb6528377404ad8649b35325131d57ed0913b90e17ab3d92f`
