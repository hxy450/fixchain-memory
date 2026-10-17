# 可能为空的 TextView 迁 Text 时保留一行高：Android 空文本仍占一行字体高，ArkUI 空 Text 高为 0

ID：`lesson-6668f8800d3ddaaf52ed` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为可能显示空串的标题、正文预览、附件文字条确定渲染条件与行高时

## 适用情境

源 TextView 高为 wrap_content，文本可能为空（无标题、空正文、名称缺失），或为 visibility=invisible、setVisibility(INVISIBLE)；相邻元素（日期行、正文起始行）依赖它的占位定位；目标准备写 if (text !== '') 条件渲染，或用 Visibility.Hidden 后直接绑定可能为空的串。

## 例外与边界

- 源端该 TextView 为 GONE，或文本为空时代码将其设为 GONE

## 原因

Android TextView 的高度按字体度量计算，与内容是否为空无关；ArkUI Text 内容为空时高度为 0，Visibility.Hidden 保留的也是 0 高。条件渲染或空串都会让该行塌陷，下方元素上移。

## 做法

1. INVISIBLE（XML 或 Adapter 中 setVisibility）映射为 .visibility(Visibility.Hidden) 并保留节点，只有 GONE 才不渲染；运行时显隐以 Adapter bind/getView 中的 setText、setVisibility 分支为准。
2. 空串可能到达的 Text，在显示值为空时以单个空格或零宽空格 \u200B 占行，或给出与源字体度量一致的最小高度；再核对依赖它定位的相邻元素。

来源支持：1 张卡 · 迁移数未记录 · 应用数未记录

## 来源（按需复核）

- [case-0a592ebcc5ad2dd158e6](../../../store/cases/case-0a592ebcc5ad2dd158e6/e5f8608441060689148f8a1c5b72e51fd7091b2818e6255748020dccb6b10333.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`e5f8608441060689148f8a1c5b72e51fd7091b2818e6255748020dccb6b10333`
