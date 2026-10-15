# 分开单行文本盒与多行行距，不把 Compose lineHeight 同名直映为 ArkUI .lineHeight

ID：`lesson-2a2924aaebbfbea80780` · 版本：1

[本主题](index.md)

## 何时使用

规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时

## 适用情境

源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。

## 例外与边界

- 当前源端的 LineHeightStyle、字体内边距或已有明确契约要求固定行盒时，保留该契约，不默认改成自然高度。

## 原因

来源观察到源端单行按字体自然高度显示、行高只作用于行间，目标无条件 .lineHeight 却把单行盒撑到整行高，按行高推算的容器定高随之偏大。修复单行时又曾把未经实测的多行合成规则写成主题公式，破坏原本正确的段落行距。来源的 lineSpacing = lineHeight − fontSize 只在当时字体与工具链条件下经设备标定，不是跨字体、字号和 SDK 的通用公式。

## 做法

1. 规格与令牌分别表达“行间距离”和“单行文本盒高度”；源端单行保持自然高度时，不对所有 Text 无条件施加 .lineHeight，也不把样式 lineHeight 直接加进容器高度。
2. 多行沿用当前工程已成立的排版映射；已有条件匹配的标定支持时，可用 lineSpacing(LengthMetrics.fp(lineHeight − fontSize), { onlyBetweenLines: true })；只修单行时保留原本正确的多行路径，不顺带全局换公式。
3. 容器确需显式高度时，单行文本取字体自然高度（字号 × 字体 hhea (ascent+descent)/unitsPerEm）或令牌派生值，无法确定时用 onSizeChange 回读子项实高；空串是否保留高度服从源端行为，确需占位才设 minHeight。

## 可选检查

- 只有正在替换多行公式，或字体、字号、SDK 条件与已有依据不匹配时，用一个单行和一个多行样本核对盒高与行距。

来源支持：3 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-04c6d6166ebb2bcc3dfa](../../../store/cases/case-04c6d6166ebb2bcc3dfa/7587aeeb0c427386f8719b769100b69b0c3f4edf0e3b829f48862df53ccaabaf.json) · 结论：diagnosis
  卡片版本：`7587aeeb0c427386f8719b769100b69b0c3f4edf0e3b829f48862df53ccaabaf`
- [case-4056358e68946ac061c6](../../../store/cases/case-4056358e68946ac061c6/5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75`
- [case-d9d5f51887ff5d7afd17](../../../store/cases/case-d9d5f51887ff5d7afd17/17f344ed9be264b0b98b2e2b54e4f05fa1cdcd49074cf16f7e178d299848d9da.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`17f344ed9be264b0b98b2e2b54e4f05fa1cdcd49074cf16f7e178d299848d9da`
