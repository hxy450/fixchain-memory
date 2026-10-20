# 可能为空的 wrap_content TextView 仍占一行高：ArkUI 空串 Text 高为 0，空态用零宽空格或行高兜底并保留节点

ID：`lesson-73ffccca482a384c3435` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为文本可能为空的 Text 节点（列表卡片标题、正文预览、附件文字条）确定渲染条件与行高时

## 适用情境

源布局里 wrap_content 的 TextView 可能拿到空串（无标题、空正文、名称缺失），XML 或 Adapter 把它置为 VISIBLE 或 INVISIBLE 而不是 GONE；相邻元素（日期行、正文起始行、文字条底色）依赖它的一行字体高度定位；目标用 ArkUI Text 渲染。

## 例外与边界

- 源端在文本为空时把该 TextView 设为 GONE：按不渲染处理

## 原因

Android 空文本 TextView 仍按字体度量占一行高，INVISIBLE 也保留这块空间；ArkUI Text 内容为空时高度为 0，Visibility.Hidden 只保留组件自身那份（为零的）尺寸。按 if (text !== '') 条件渲染，或只换成 Hidden，都会让相邻元素上移、文字条塌陷。

## 做法

1. 按源端显隐语义选写法：VISIBLE 与 INVISIBLE 都保留节点（INVISIBLE 用 .visibility(Visibility.Hidden)），只有 GONE 才条件不渲染；共享组件的显隐以 Adapter bind/getView 中的 setVisibility 分支为准，不以 XML 初值或文本是否为空判断。
2. 空串可能到达的 Text，显示值为空时换成零宽空格 '\u200B' 或单个空格，或按源字体行高给 lineHeight、constraintSize({ minHeight })，保证空态仍占一行；再核对依赖它定位的相邻元素。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-0a592ebcc5ad2dd158e6](../../../store/cases/case-0a592ebcc5ad2dd158e6/e5f8608441060689148f8a1c5b72e51fd7091b2818e6255748020dccb6b10333.json) · 结论：diagnosis, recommendation:2, recommendation:1
  卡片版本：`e5f8608441060689148f8a1c5b72e51fd7091b2818e6255748020dccb6b10333`
