# 摘要行、价格行一类 Row 组：自定义组件不靠 Flex 基线对齐，内距逐行复制，靠右标签补文本对齐

ID：`lesson-c4990fef246323ffda03` · 版本：1

[本主题](index.md)

## 何时使用

页面转换阶段，翻译摘要行、价格行等由若干 Row 组成的列表块时

## 适用情境

源 Row 用 alignBy(LastBaseline) 对齐文本与自定义组件（如数量选择器）；各子 Row 各自 padding(horizontal)，分隔线在行外全宽；标签用 weight(1) + wrapContentWidth(End) 靠右。

## 原因

自定义组件没有可对齐的文本基线，来源改用 Flex 基线对齐后把它挤到了下一行；把各行 padding 上提到公共父容器会让分隔线跟着缩进；wrapContentWidth(End) 的靠右效果在权重布局里需要文本对齐补回。

## 做法

1. 单行文本与自定义控件对齐时，用 Row + alignItems(Center) + layoutWeight(1) 近似基线对齐（来源复核误差约 0.5dp），不直接用 Flex 的基线对齐。
2. 逐行复制 padding，不上提到外层；weight(1) + wrapContentWidth(End) 写成 layoutWeight 或 flexGrow 加 textAlign(End)。

## 可选检查

- 首次可构建时截图核对文本与控件的纵向位置。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-83dafcc0eaba740bd9c0](../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：recommendation:5, recommendation:6
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
