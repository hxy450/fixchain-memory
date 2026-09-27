# 判定 $r('app.media.X') 是否可用时检索全部限定词目录，按源布局的 drawable 名取图；确认缺失才登记缺口，不用文字字形、纯色底或近似图标替代

ID：`lesson-943544ce27bf04f9faf8` · 版本：1

[本主题](index.md)

## 何时使用

页面转换与截图对齐修复阶段，把源布局中的 @drawable 引用（头像、图标、装饰图、带透明边缘的头图、行尾箭头）落成 $r('app.media.X') 并确认资源是否已迁移时

## 适用情境

资源迁移把 drawable-xhdpi 等位图直接复制到 resources/xldpi/media 一类限定词目录，不在 base/media；构建日志对这些图只报“does not have a base resource”警告；工程里还有外观相近的通用图标（如生活指数图标）。

## 原因

只在 base/media 查找会把已迁移的资源判为缺失，写者随之用 Text('人')、Text('›') 之类字形、品牌色底或外观相近的通用图标代替，头像、箭头、提醒图标和透明波浪头图的收口都与源端不符；截图修复时按视觉相似挑图也会延续偏差。来源中页面转换者读到源布局列出的全部 drawable 名，只核对 base/media 就把四个资源判为不存在，改成字形占位并在透明头图下垫了品牌色；返修又从通用资源里挑近似图标。

## 做法

1. 判断资源可用性时检索 resources 下全部限定词目录（base、xldpi、dark 等）或按资源映射表核对；构建日志里的“does not have a base resource”说明文件在限定词目录，不是缺失。
2. 图标与装饰图按源布局的 src、drawableStart、background 中的 drawable 名取用，写完按源布局的 drawable 清单逐项对照组件中的引用；确认缺失时登记资源缺口，不以文字字形、纯色底或外观近似的图标替代。
3. 头图带透明边缘时，其下的底色取页面背景，不填品牌色。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-d827908975df4e90ae2b · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c9ff0dd2d732fa7105c9bc2252a15de9e80ccee5e3e828bdebba6830c8378e03`
