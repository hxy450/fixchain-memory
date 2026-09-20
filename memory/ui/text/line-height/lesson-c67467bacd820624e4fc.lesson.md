# TextStyle.lineHeight 与 ArkUI .lineHeight 同名不等价：Compose 单行文本盒不随 lineHeight 撑高

ID：`lesson-c67467bacd820624e4fc` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，为排版令牌（TextStyle → 统一 AttributeModifier）写 Source→ArkTS 映射契约并定难度时

## 适用情境

源是 Compose Material3 Typography，各 TextStyle 都带 lineHeight.sp；目标打算用一个 AttributeModifier 给全部 Text 套样式，页面里大量单行文本（Summary 行、卡片标题）与少量多行段落共用同一令牌。

## 例外与边界

- 目标只对多行段落施加 lineHeight、单行文本另有令牌

## 原因

Compose 默认 LineHeightStyle 下单行文本盒 = 字体 ascent+descent（Android dump 实测 bodyLarge 16sp 单行 ≈19dp），lineHeight 只作用于行间；ArkUI .lineHeight 把每一行含单行都撑到整行高（28vp）。F002 作者只 grep 到 text.d.ts 存在同名 lineHeight(number) 签名，就写成「sp→fp 1:1、难度低」的契约，Base-6 主题 worker 据此无条件 .lineHeight，Cart Summary 区 157vp vs 131dp、Total 行被 Checkout 栏遮住。

## 做法

1. 契约里写明两端语义差与目标写法：单行取字体自然高，行距只作用行间（lineSpacing onlyBetweenLines，或仅多行段落用 lineHeight），并标为行为等价难点而非「低」。
2. 契约附检查口径：任选一个单行 Text，比较 Android dump 文本盒高与目标端值。

## 检查

- Android dump 的单行 Text bounds 高 ≈ fontSize × 字体 hhea 比（Karla ≈1.169、Montserrat ≈1.219），目标端同一 Text 的 dump 高应在 ±1vp 内，不应等于 lineHeight。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- [case-4056358e68946ac061c6](../../../../store/cases/case-4056358e68946ac061c6/c064fce84bd61cbdd2a7d203b85e576c31033aba00f2dd902f4e42414cad012d.json) · 结论：diagnosis, recommendation:1
  卡片版本：`c064fce84bd61cbdd2a7d203b85e576c31033aba00f2dd902f4e42414cad012d`
