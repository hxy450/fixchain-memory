# Compose lineHeight 未配 lineHeightStyle 时，分开单行文本盒与多行行距，不直映为 ArkUI .lineHeight

ID：`lesson-2a2924aaebbfbea80780` · 版本：3

[本主题](index.md)

## 何时使用

规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时

## 适用情境

源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。

## 例外与边界

- 源 TextStyle 显式设置了 lineHeightStyle 时，不按本条的默认裁剪处理，按其设置推导单行盒高与行距

## 原因

观察到的源端行为是单行按字体自然高度显示、行高只作用于行间；目标无条件 .lineHeight 会把单行盒撑到整行高，按行高推算的容器定高随之偏大。只修单行时替换全局多行公式，又会破坏原本正确的段落行距。lineSpacing = lineHeight − fontSize 只在当时的字体与工具链条件下经设备标定，不是跨字体、字号和 SDK 的通用公式。

## 做法

1. 规格与令牌分别表达“行间距离”和“单行文本盒高度”；源端单行保持自然高度时，不对所有 Text 无条件施加 .lineHeight，也不把样式 lineHeight 直接加进容器高度。
2. 多行沿用当前工程已成立的排版映射；已有条件匹配的标定支持时，可用 lineSpacing(LengthMetrics.fp(lineHeight − fontSize), { onlyBetweenLines: true })；只修单行时保留原本正确的多行路径，不顺带全局换公式。
3. 容器确需显式高度时，单行文本取字体自然高度：字号 × (hhea.ascender − hhea.descender) / unitsPerEm（descender 为负值；已观察到按此式算出的单行高与 Android dump 实测吻合，lineGap 是否计入未核），或用令牌派生值；拿不到字体文件时用 onSizeChange 回读子项实高。可能为空串的文本加 constraintSize({ minHeight: 字体自然高度 }) 与源端对等（去掉 .lineHeight 后空串高度会变 0）。

## 可选检查

- 只有正在替换多行公式，或字体、字号、SDK 条件与已有依据不匹配时，用一个单行和一个多行样本核对盒高与行距。

来源支持：3 张卡 · 2 次迁移 · 1 个应用

## 来源（按需复核）

- [case-04c6d6166ebb2bcc3dfa](../../../store/cases/case-04c6d6166ebb2bcc3dfa/7587aeeb0c427386f8719b769100b69b0c3f4edf0e3b829f48862df53ccaabaf.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`7587aeeb0c427386f8719b769100b69b0c3f4edf0e3b829f48862df53ccaabaf`
- [case-4056358e68946ac061c6](../../../store/cases/case-4056358e68946ac061c6/5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`5a37ff393ac488101441f9a3889af9b15392ce1ebfecf83f56931f1255d3bc75`
- [case-d9d5f51887ff5d7afd17](../../../store/cases/case-d9d5f51887ff5d7afd17/17f344ed9be264b0b98b2e2b54e4f05fa1cdcd49074cf16f7e178d299848d9da.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`17f344ed9be264b0b98b2e2b54e4f05fa1cdcd49074cf16f7e178d299848d9da`
