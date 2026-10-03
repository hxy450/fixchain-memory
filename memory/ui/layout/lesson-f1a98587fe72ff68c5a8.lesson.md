# 页面转换逐项落实源 XML 的 gone 节点（代码只绑点击、没有设为可见的入口也不渲染）、固定尺寸点击容器与 tools:listitem 行布局

ID：`lesson-f1a98587fe72ff68c5a8` · 版本：2

[本主题](index.md)

## 何时使用

页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时；迁移标题栏或工具栏图标按钮并决定是否显示时

## 适用情境

源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。 也包括 Activity 对 visibility=gone 的标题栏图标 findViewById 并绑定跳转（如打开搜索页），全文没有 setVisibility(VISIBLE)；目标工程其他页面已有同类入口的现成写法。

## 原因

只按快照或主布局写，会渲染源端隐藏的节点、把点击区缩成图标大小，列表行也缺少 item 布局里的图标与右侧信息列。来源中转换者读到了 40×48dp 返回区、visibility=gone 的“搜索结果”标题和 tools:listitem 引用，写出的返回图只有 16×16，标题无条件显示，也没有打开 item 布局，结果行缺地址图标和距离列。 点击监听只说明代码可达，不说明控件可见；照搬目标工程其他页面的入口惯例，会把源端隐藏的入口生成为可见按钮。另一应用的分类页标题栏即如此：写者首稿按源布局留了空占位，后来改成照其他页面加了搜索入口。

## 做法

1. visibility=gone 的节点不渲染（或按源端条件显示）；快照可见文本与源 XML 可见性冲突时以源 XML 为准。
2. 固定尺寸的点击容器按其宽高作为热区，图标尺寸另按 src 与 scaleType 取。
3. 列表行结构打开 tools:listitem（或适配器 inflate 的）item 布局，取图标、文字层级与右侧列。
4. 判定图标按钮是否显示时，先看 XML 初始 visibility，再查代码中对该 View 的全部 setVisibility；只有 findViewById 与点击监听、没有 VISIBLE 分支的 gone 入口不生成。目标工程其他页面的写法只决定怎样实现，不决定源页是否有该入口；有截图时新增可见元素前先用截图核对，协调者追加的入口要求与源布局或截图冲突时先回报冲突。
5. 源端靠左右对称让中间控件居中时，隐藏一侧用同尺寸空占位（如返回键对侧的 44×44 空 Row）保持居中，不放可点击图标。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-436d1b16d79796c667d6](../../../store/cases/case-436d1b16d79796c667d6/fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70.json) · 结论：diagnosis, recommendation:4
  卡片版本：`fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70`
- [case-a348083ad18c6f87030f](../../../store/cases/case-a348083ad18c6f87030f/ff4ca14c213bc58cab29a246315afb07ff950c3ead8d54b4816a9b98629adda5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`ff4ca14c213bc58cab29a246315afb07ff950c3ead8d54b4816a9b98629adda5`
