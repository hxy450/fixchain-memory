# 分开单行文本盒与多行行距，不把 Compose lineHeight 同名直映为 ArkUI .lineHeight

## 何时使用

规格提取、主题实现或页面转换阶段，把 Compose 排版令牌落成 ArkUI 文本属性或据文本高度推算容器尺寸时；视觉修复阶段改写主题层行高公式时（前提：最终生效的样式未设 lineHeightStyle）

## 适用情境

源 TextStyle 声明 fontSize/lineHeight、未设 lineHeightStyle；目标准备给所有 Text 无条件设置 .lineHeight()，或把 lineHeight 数值当单行文本的实际盒高来推算横向列表等容器的显式高度；映射参考可能给出 lineHeight → .lineHeight() 的 1:1 对应。

## 例外与边界

- 当前源端的 LineHeightStyle、字体内边距或已有明确契约要求固定行盒时，保留该契约，不默认改成自然高度。
- 「未设 lineHeightStyle」要看最终生效的样式，不只看源码里的 TextStyle(...) 字面：未设时安卓端套用默认 LineHeightStyle（Proportional、Trim.Both）；而直接用 Material3 默认排版令牌、或在其上 copy 出的样式，带的是 LineHeightStyle（Center、Trim.None）（material3 1.4.0 如此，其他版本先查），不属于这条的前提——单行盒高以安卓端 dump 的盒高为准，不照这条删掉 .lineHeight。

## 原因

来源观察到源端单行按字体自然高度显示、行高只作用于行间，目标无条件 .lineHeight 却把单行盒撑到整行高，按行高推算的容器定高随之偏大。修复单行时又曾把未经实测的多行合成规则写成主题公式，破坏原本正确的段落行距。来源的 lineSpacing = lineHeight − fontSize 只在当时字体与工具链条件下经设备标定，不是跨字体、字号和 SDK 的通用公式。

## 做法

1. 规格与令牌分别表达“行间距离”和“单行文本盒高度”；源端单行保持自然高度时，不对所有 Text 无条件施加 .lineHeight，也不把样式 lineHeight 直接加进容器高度。
2. 多行沿用当前工程已成立的排版映射；已有条件匹配的标定支持时，可用 lineSpacing(LengthMetrics.fp(lineHeight − fontSize), { onlyBetweenLines: true })；只修单行时保留原本正确的多行路径，不顺带全局换公式。
3. 容器确需显式高度时，单行文本取字体自然高度（字号 × 字体 hhea (ascent+descent)/unitsPerEm）或令牌派生值，无法确定时用 onSizeChange 回读子项实高；空串是否保留高度服从源端行为，确需占位才设 minHeight。

## 可选检查

- 只有正在替换多行公式，或字体、字号、SDK 条件与已有依据不匹配时，用一个单行和一个多行样本核对盒高与行距。

来源支持：3 张卡 · 2 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕ArkUI Text 的 lineHeight 为 number 时单位是 fp；设置值不大于 0 时不限制行高，由系统按字号自适应；与 lineHeightMultiple（API 22 起）同时设有效值时 lineHeight 不生效
- 〔做法第 2 步〕Text 的 lineSpacing 选项 LineSpacingOptions.onlyBetweenLines 默认 false：false 时首行上方和尾行下方也有行间距；true 时行间距只在行与行之间（API 20 起）
- 〔做法第 2 步〕fp 与 vp 一样随屏幕像素密度换算，另外还随系统字体大小设置变化；vp 不随系统字体大小变化
- 〔原因 / 做法第 1 步〕源端 TextStyle 未设 lineHeightStyle 时，安卓端单行文本盒高是字体自然高度而不是样式 lineHeight；ArkUI Text 设 .lineHeight 时按每行完整行高排版，不裁首行上方和末行下方的余量，单行文本盒被撑到整行高
- 〔原因〕ArkUI Text 设 .lineHeight 时多行段落块高等于行数乘行高
- 〔原因〕bodyLarge 样式的单行文本按 .lineHeight 直译时 ArkUI 盒高 28vp，安卓端约 19dp
- 〔做法第 2 步〕用 lineSpacing 时 ArkUI 多行相邻行距等于 fontSize 加 lineSpacing（只由 Karla、Montserrat 16fp 的 dump 反推，其他字号、字体、SDK 未核）
