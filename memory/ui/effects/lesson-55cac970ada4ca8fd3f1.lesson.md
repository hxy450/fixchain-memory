# 源端图像模糊、乘法压暗与折叠态着色按参数等价实现

ID：`lesson-55cac970ada4ca8fd3f1` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，迁移折叠头部等使用图片模糊、LightingColorFilter 压暗和按折叠状态切换工具栏图标颜色的页面时

## 适用情境

源背景图经模糊变换与 LightingColorFilter(mul, 0) 处理，工具栏图标由专门的着色管理类按折叠阈值切换颜色。

## 原因

以“无对等图片模糊链”为由只用半透明遮罩近似、用固定次要色代替状态着色，视觉明显偏离且不易被后续发现。

## 做法

1. 模糊按源变换参数与处理顺序核对 blur 的映射；LightingColorFilter 的加色为 0、RGB 三通道乘数相同且为 m（0–255）时，可在透明度与合成方式相符的前提下，用 opacity = 1 − m/255 的纯黑覆盖层表达该乘法压暗（来源为 0xff666666、0xff828282）。有色乘数、非零加色或不同透明度/合成条件另行核对，不能把整个 ARGB 整数直接代入 m/255。
2. 写前读取规格锚点中的状态着色实现类，移植折叠阈值与展开、折叠两态颜色。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4f627840679361f165a3](../../../store/cases/case-4f627840679361f165a3/8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8.json) · 结论：recommendation:4
  卡片版本：`8b0f7cc40d821777a77dc3bf68c6739f335039023414e9bcb04404d5b4ac02e8`
- [case-9058ac868b6feb3a04e0](../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:3
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
