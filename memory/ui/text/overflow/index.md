# ui/text/overflow

迁移多行折叠、断词和省略号行为时进入。

[上一级](../index.md)

## 本级经验

- [多行省略应核对末行渲染语义，而不是只匹配同名 API](lesson-81d7dc4cd74fcc3b10b6.lesson.md)
  - 时机：规格提取或实现阶段，为带 maxLines 与 Ellipsis 的多行文本选择目标端折叠方案时
  - 情境：源端按字符填充末行并紧接省略号，目标端同名 API 可能受默认 wordBreak 影响，按词丢弃后再显示带空格的省略标记。
  - 例外：产品允许目标平台的原生省略形态，或已验证当前 wordBreak、ellipsisMode 与字体配置能复现源端末行
