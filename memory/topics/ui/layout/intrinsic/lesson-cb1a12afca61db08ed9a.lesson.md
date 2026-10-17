# Row(height(IntrinsicSize.Min)) 先算出固有高度写成显式高度，再让子项按百分比撑满并保留源偏移

ID：`lesson-cb1a12afca61db08ed9a` · 版本：2 · 阶段：execute · 主题：[ui/layout/intrinsic](index.md)

概要：IntrinsicSize.Min 行先算固有高度写显式值

信号：`IntrinsicSize.Min`, `fillMaxHeight`, `align(Top)`, `padding(top)`, `height('100%')`, `Row`

## 何时使用

页面转换阶段，遇到 Row(height(IntrinsicSize.Min)) 且子项 fillMaxHeight、带 padding(top) 等偏移时

## 适用情境

源 Row 以固有最小高度定高，高度由最高的子项（如按钮的最小触控尺寸）决定；子项用 fillMaxHeight 并在内部偏移；目标端没有固有尺寸测量，迁移陷阱表提示不定高父级下的百分比子项会撑满。

## 原因

Row 不定高时子项的百分比高度与偏移无从落地；实现者还可能以“不定高父级下百分比会撑满”为由删掉源码偏移、改成垂直居中，而给父级定高后百分比本可正常使用。

## 做法

1. 先算出固有高度（最高子项的尺寸），给 Row 写显式 height，再让子项 height('100%') 并保留源码的对齐和偏移（如 align(Top) + padding(top)）。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [纵向容器默认起始对齐与贴顶在目标显式写出](../constraints/lesson-08b9064f678f1635e647.lesson.md)（共享 1 张卡）
- [fillMaxWidth 先占满剩余宽，后续兄弟按实得宽判断](../sizing/lesson-45f77b3088fa69398f9e.lesson.md)（共享 1 张卡）
- [库与框架组件默认几何先查 SDK/库 res 分侧取](../../theme/sources/lesson-5a82d62ff7e087616968.lesson.md)（共享 1 张卡）
- [Stack 子项 .align() 无效，对齐用满高容器](../constraints/lesson-92aee54a305ea0bde363.lesson.md)（共享 1 张卡）
- [基线对齐用 Row 居中近似，内距逐行复制，标签靠右对齐](../constraints/lesson-c4990fef246323ffda03.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-83dafcc0eaba740bd9c0](../../../../../store/cases/case-83dafcc0eaba740bd9c0/63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6.json) · 结论：rec-ade91c4178
  卡片版本：`63799a14d87533825a0449dd85653c66535fbb31296be482c5feada55b5522a6`
