# Compose Row 以 alignBy(LastBaseline) 对齐文本与自定义组件时，改用 Row 居中对齐，不用 Flex 基线对齐

ID：`lesson-c4990fef246323ffda03` · 版本：3

[本主题](index.md)

## 何时使用

页面转换阶段，翻译 Compose Row 中以 alignBy(LastBaseline)/alignByBaseline 对齐的文本与自定义组件（数量选择器等）时

## 适用情境

源 Row 的子项用 alignBy(LastBaseline) 对齐，其中一端是自定义组件或不含文本基线的控件；目标准备写 Flex/Row 的 ItemAlign.Baseline。

## 例外与边界

- 两端都是 Text（都有文本基线）时，可以用 Flex 的 ItemAlign.Baseline（enums.d.ts：Flex 容器内按文本基线对齐）

## 原因

ArkUI 自定义组件取不到可对齐的文本基线，Flex ItemAlign.Baseline 对它的结果不可预期，可能把控件排到文本下方；Flex 默认 FlexWrap.NoWrap（flex.d.ts:118），出现换行时另查 wrap 与宽度设置。

## 做法

1. 单行文本与自定义控件对齐时，用 Row + alignItems(VerticalAlign.Center)，文本侧 layoutWeight(1) 占剩余宽；不用 Flex 的 ItemAlign.Baseline 了事。

## 可选检查

- 首次可构建时截图核对文本与控件的纵向位置。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-83dafcc0eaba740bd9c0](../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：recommendation:5, diagnosis
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
