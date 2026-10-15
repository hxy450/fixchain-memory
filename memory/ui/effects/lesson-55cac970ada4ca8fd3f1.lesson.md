# 源端图片用 LightingColorFilter(mul, 0) 压暗时按通道乘色实现，不以半透明遮罩近似；同链路的模糊变换按源参数换算

ID：`lesson-55cac970ada4ca8fd3f1` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，迁移对背景图或封面使用 LightingColorFilter 乘色压暗（常与图片模糊变换一起）的页面时

## 适用情境

源端对 ImageView 或图片加载库载入的图片 setColorFilter(LightingColorFilter(mul, add))，add 为 0，常配合 BlurTransformation 一类模糊变换；目标用 Image 组件显示同一图片。

## 原因

LightingColorFilter 按通道计算 R' = R × mul.R / 255 + add.R（G、B 同理），不改 alpha（android/graphics/LightingColorFilter.java 注释）。纯黑覆盖层 opacity = 1 − m/255 只在 mul 三通道相等（R=G=B=m）且被盖区域不透明时等价：彩色乘数会丢掉色偏，透明像素也会被压暗，覆盖层还会压暗叠在图上的其他内容。以“无对等能力”为由只用半透明遮罩近似，视觉明显偏离且不易被后续发现。

## 做法

1. 对 Image 用 colorFilter 的 4×5 颜色矩阵逐通道乘色：new ColorFilter([r/255,0,0,0,0, 0,g/255,0,0,0, 0,0,b/255,0,0, 0,0,0,1,0])，r、g、b 取 mul 的三个通道，alpha 行保持不变（image.d.ts 的 colorFilter、units.d.ts 的 ColorFilter）。
2. mul 为灰色（R=G=B=m）且图片区域不透明时，也可用 opacity = 1 − m/255 的纯黑覆盖层，覆盖层只盖图片，不盖叠在图上的文字与按钮。
3. 同一图片还有模糊变换时用 blur 实现，参数取自源模糊变换，数值单位按同主题 Modifier.blur 单位经验先核。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4f627840679361f165a3](../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：recommendation:4
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-9058ac868b6feb3a04e0](../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:3
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
