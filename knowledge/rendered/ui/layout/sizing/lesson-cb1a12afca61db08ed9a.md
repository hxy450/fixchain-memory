# Row(height(IntrinsicSize.Min)) 先算出固有高度写成显式高度，再让子项按百分比撑满并保留源偏移

## 何时使用

页面转换阶段，遇到 Row(height(IntrinsicSize.Min)) 且子项 fillMaxHeight、带 padding(top) 等偏移，固有高度由尺寸固定的子项（如按钮的最小触控尺寸）决定时

## 适用情境

源 Row 以固有最小高度定高，高度由最高的子项（如按钮的最小触控尺寸）决定；子项用 fillMaxHeight 并在内部偏移；目标端没有固有尺寸测量，迁移陷阱表提示不定高父级下的百分比子项会撑满。

## 例外与边界

- 源 Row 没写 verticalAlignment 时 Compose 按顶部对齐，ArkUI Row 的 alignItems 不写时默认 VerticalAlign.Center；给 Row 定高后，不撑满高度的子项要显式写 alignItems(VerticalAlign.Top) 才保留源端的纵向位置。

## 原因

Row 不定高时子项的百分比高度与偏移无从落地；实现者还可能以“不定高父级下百分比会撑满”为由删掉源码偏移、改成垂直居中，而给父级定高后百分比本可正常使用。

## 做法

1. 先算出固有高度（最高子项的尺寸），给 Row 写显式 height，再让子项 height('100%') 并保留源码的对齐和偏移（如 align(Top) + padding(top)）。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕组件尺寸用百分比设置时，按最近一个设置了固定大小的祖先节点的尺寸计算；父 Row 没有定高时，子项的 height('100%') 落到更上层定了高的祖先上，所以看起来会撑满
- 〔做法第 1 步〕align 设置组件内容在自身绘制区域内的对齐方式，应用没有另设时默认 Alignment.Center
