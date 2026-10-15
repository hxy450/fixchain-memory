# 多 viewType 列表按每类 holder 的根布局与运行时挂入的子视图定卡片外观：某一类专属的背景、圆角、描边不写进各类共用的 Builder

ID：`lesson-9de4c7648d23db5d7f86` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，为含普通项、推广项等多种 ViewHolder 的列表或网格确定卡片背景、描边与圆角，或参照兄弟页面的卡片实现时；规格准备阶段为列表页登记 item 布局时

## 适用情境

Android 列表同时有多类 holder：普通项的外观来自 holder 运行时 addView/inflate 的组件根视图（如 CardView 的 cardCornerRadius），推广项另有带圆角描边的背景 drawable；目标准备用一个共用 Builder 渲染各类卡片，或照搬兄弟页面已有的“白底 + 描边 + 圆角”卡片。

## 原因

只看到一类 item 布局里的背景就套给所有分支，会把该类的圆角与描边带到其他项上；普通项真正的外观藏在 holder 动态加入的视图里，不打开它就拿不到圆角真值。兄弟页面的卡片 Builder 也是迁移产物，其数值不能当源端真值。

## 做法

1. 逐类核对 item 根布局和 holder 的绑定代码；holder 把动态视图放进内容容器时，继续打开该视图的布局取背景与圆角（如 cardCornerRadius 对应的 dimen 真值）。
2. 只属于某一类的背景 drawable 只用在该类分支；共用 Builder 按 holder 类型取外观参数，不写死一套。参照兄弟页面的卡片实现时只借结构，圆角、描边、底色逐项回到本页源码核对。
3. 规格准备阶段，列表页的布局清单（如 layout_sources、recycler_item_layouts）包含各类 item 布局及其动态 inflate 的预览布局，不只登记某一类。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5b1b0e2ce03be0dc6d37](../../../store/cases/case-5b1b0e2ce03be0dc6d37/c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48`
