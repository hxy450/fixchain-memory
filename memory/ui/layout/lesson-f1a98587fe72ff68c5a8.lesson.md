# 页面转换逐项落实源 XML 的 gone 节点、固定尺寸点击容器与 tools:listitem 行布局

ID：`lesson-f1a98587fe72ff68c5a8` · 版本：1

[本主题](index.md)

## 何时使用

页面转换阶段，把 Android 页面 XML 翻译为 ArkUI 结构与几何时

## 适用情境

源布局含 visibility=gone 的标题等节点、固定尺寸的点击容器（如 40×48dp 的返回 ImageView），列表 RecyclerView 用 tools:listitem 引用独立的 item 布局；迁移用的页面快照是合成的，可能把 gone 节点列为可见文本。

## 原因

只按快照或主布局写，会渲染源端隐藏的节点、把点击区缩成图标大小，列表行也缺少 item 布局里的图标与右侧信息列。来源中转换者读到了 40×48dp 返回区、visibility=gone 的“搜索结果”标题和 tools:listitem 引用，写出的返回图只有 16×16，标题无条件显示，也没有打开 item 布局，结果行缺地址图标和距离列。

## 做法

1. visibility=gone 的节点不渲染（或按源端条件显示）；快照可见文本与源 XML 可见性冲突时以源 XML 为准。
2. 固定尺寸的点击容器按其宽高作为热区，图标尺寸另按 src 与 scaleType 取。
3. 列表行结构打开 tools:listitem（或适配器 inflate 的）item 布局，取图标、文字层级与右侧列。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-436d1b16d79796c667d6](../../../store/cases/case-436d1b16d79796c667d6/fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70.json) · 结论：diagnosis, recommendation:4
  卡片版本：`fc0a6307eebf5b3bce1a7c1f60a97bf1685ed3251e7fcbb0728afeab5ff1ac70`
