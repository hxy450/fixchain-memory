# 摘要行、价格行一类 Row 组：自定义组件不靠 Flex 基线对齐，内距逐行复制，靠右标签补文本对齐

ID：`lesson-c4990fef246323ffda03` · 版本：4 · 阶段：execute · 主题：[ui/layout/constraints](index.md)

概要：基线对齐用 Row 居中近似，内距逐行复制，标签靠右对齐

信号：`alignBy(LastBaseline)`, `wrapContentWidth(End)`, `weight(1)`, `layoutWeight`, `flexGrow`, `textAlign(End)`, `alignItems`, `LastBaseline`

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

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [纵向容器默认起始对齐与贴顶在目标显式写出](lesson-08b9064f678f1635e647.lesson.md)（共享 1 张卡）
- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](../sizing/lesson-45f77b3088fa69398f9e.lesson.md)（共享 1 张卡）
- [M3 组件默认几何与留白从库 Tokens 分侧取值](../../theme/sources/lesson-5a82d62ff7e087616968.lesson.md)（共享 1 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](lesson-92aee54a305ea0bde363.lesson.md)（共享 1 张卡）
- [IntrinsicSize.Min 行先算固有高度写显式值](../intrinsic/lesson-cb1a12afca61db08ed9a.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-83dafcc0eaba740bd9c0](../../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：rec-80206d8b47, rec-cca8a6776d
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
