# 窗口位图背景按BitmapDrawable默认FILL拉伸铺满

ID：`lesson-db24eac3d20f6a1ea534` · 版本：1

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为安卓窗口级或视图级位图背景选择ArkUI填充模式时

## 适用情境

源以new BitmapDrawable(...)设置窗口或视图背景（未改gravity），背景位图宽高比与目标窗口不同；目标用全屏Image或backgroundImage承载。

## 例外与边界

- 源代码显式设置了Drawable的gravity或ImageView的scaleType，此时按显式值映射

## 原因

BitmapDrawable默认gravity为FILL，按宽高分别拉伸、不裁切；Cover等比放大会裁掉边缘，宽高比不同时两端同一归一化坐标上的内容必然不同。

## 做法

1. 映射为Image.objectFit(ImageFit.Fill)或backgroundImageSize(ImageSize.Fill)，并在规格中写明源Drawable类型和默认gravity。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3db3942c6851402bc500](../../../store/cases/case-3db3942c6851402bc500/251127f8fa91acb01a08f4eeeba1c14342af29fc1a80fd401b2697d8efd65249.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`251127f8fa91acb01a08f4eeeba1c14342af29fc1a80fd401b2697d8efd65249`
