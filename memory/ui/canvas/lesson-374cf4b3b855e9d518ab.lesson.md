# 对角ColorMatrix着色用逐像素乘法实现，不依赖合成模式

ID：`lesson-374cf4b3b855e9d518ab` · 版本：1

[本主题](index.md)

## 何时使用

绘制实现阶段，把Android ColorMatrixColorFilter逐通道着色迁移到ArkUI Canvas时

## 适用情境

源端用4×5对角ColorMatrix（R×r、G×g、B×b、A×a）给带明暗渐变的灰度模板着色；目标是ArkUI Canvas/OffscreenCanvas，候选中出现globalCompositeOperation混合模式（如multiply）。

## 原因

ArkUI Canvas的合成模式只声明了Porter-Duff类取值，未声明的值（如multiply）不报错、按source-over处理；source-in/source-atop类叠色只能得到平涂色，丢失模板明暗。

## 做法

1. 画出模板后getImageData，逐像素乘R/G/B/A系数再putImageData（或PixelMap readPixelsToBuffer/writeBuffer），与对角矩阵逐值等价，结果缓存复用。
2. 已有TODO或规格给出逐像素路线时，优先采用这条与矩阵逐值等价的路线。

## 可选检查

- 取着色结果内若干像素，与“模板像素×系数”的理论值比较；颜色恒定说明合成未生效

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-a9bc5d0e97c73f878586](../../../store/cases/case-a9bc5d0e97c73f878586/8c43c37fbfb766d31357daa70f317c72c8fa5bf02768ee97119c13ab1d61c3a5.json) · 结论：diagnosis, recommendation:2, recommendation:4
  卡片版本：`8c43c37fbfb766d31357daa70f317c72c8fa5bf02768ee97119c13ab1d61c3a5`
