# Row(height(IntrinsicSize.Min)) 先算出固有高度写成显式高度，再让子项按百分比撑满并保留源偏移

ID：`lesson-cb1a12afca61db08ed9a` · 版本：1

[本主题](index.md)

## 何时使用

页面转换阶段，遇到 Row(height(IntrinsicSize.Min)) 且子项 fillMaxHeight、带 padding(top) 等偏移时

## 适用情境

源 Row 以固有最小高度定高，高度由最高的子项（如按钮的最小触控尺寸）决定；子项用 fillMaxHeight 并在内部偏移；目标端没有固有尺寸测量，迁移陷阱表提示不定高父级下的百分比子项会撑满。

## 原因

Row 不定高时子项的百分比高度与偏移无从落地；实现者还可能以“不定高父级下百分比会撑满”为由删掉源码偏移、改成垂直居中，而给父级定高后百分比本可正常使用。

## 做法

1. 先算出固有高度（最高子项的尺寸），给 Row 写显式 height，再让子项 height('100%') 并保留源码的对齐和偏移（如 align(Top) + padding(top)）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-83dafcc0eaba740bd9c0](../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：recommendation:3
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
