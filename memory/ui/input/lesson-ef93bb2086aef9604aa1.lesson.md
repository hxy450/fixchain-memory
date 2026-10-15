# 源端同一控件既可编辑又分段着色（Spannable、visualTransformation）时用 RichEditor 承载，不拆成两态

ID：`lesson-ef93bb2086aef9604aa1` · 版本：3

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端常驻可编辑、带分段着色的输入框（EditText + Spannable 与输入过滤，或带 visualTransformation 的 Compose TextField）选择 ArkUI 编辑组件时

## 适用情境

源端数据单元是常驻可编辑的 EditText，文本以 setText(text, SPANNABLE) 分段着色，常挂输入过滤、宽度 wrap_content；或 Compose TextField/OutlinedTextField 以 visualTransformation（如按正则给 URL 段着色）在编辑态显示样式。规格可能写“TextArea + 分段 Span 着色”这类不可实现的组合，或写成“输入框内富文本高亮能力受限，编辑态降级为纯文本”；材料与映射参考里没有提到 RichEditor。

## 原因

TextArea 不承载 Span，组件选择与着色要求自相矛盾；改成“着色只读 Text ↔ 点击切换单色 TextArea”的双态，会丢掉常驻着色、插入色与按内容测宽，注释却称等价；在核对 RichEditor 之前就判为平台受限，会把可实现的编辑态高亮降级掉。

## 做法

1. 映射到能同时编辑与承载样式片段的组件：RichEditor 配控制器按段 addTextSpan，内容变化后按源端规则重设各段样式（如 URL 段着色）；写入前核对所选组件是否支持子 Span 或样式，不写“TextArea + Span”。
2. 实现阶段发现规格组件满足不了源行为时，先查同平台的可编辑富文本组件，不自行拆成双态；确需降级时在规格与占位登记中列出丢失的行为，不在注释中声称等价。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, recommendation:5
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-4a5592fd88f74b1c16a4](../../../store/cases/case-4a5592fd88f74b1c16a4/a1c7bb6a2ed0a2ff537c2684d91954958c7741fd9d1e7e687ac599208494ce2a.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`a1c7bb6a2ed0a2ff537c2684d91954958c7741fd9d1e7e687ac599208494ce2a`
