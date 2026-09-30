# 转换 NestedScrollView/ScrollView 时只把源滚动容器内的子节点放进 Scroll，位于其前的固定头部留在 Scroll 外

ID：`lesson-46a0d7f239efac925d33` · 版本：3

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android 页面转成 ArkUI 时确定固定区域与 Scroll 的包含范围；以及规格提取阶段书写滚动容器的转换决策时

## 适用情境

源布局根为纵向 LinearLayout 或 RelativeLayout，顶部用户栏、工具栏或横幅位于 NestedScrollView 之前（RelativeLayout 中滚动容器以 layout_below 排在其下），滚动容器承载地图、主按钮、卡片、宫格等主体；目标用 ArkUI Scroll 实现。

## 原因

固定头部进了 Scroll 就会随内容滚动；内容不足一屏时 Scroll 还会把整组内容纵向居中，头部被整体下推。视觉修复若只调 padding 偏移，会掩盖层级错误。来源中执行者写首页前的批量读取恰好截掉了源布局的头部与滚动容器开标签，没有补读就把头部与地图、按钮、统计卡一起放进 Scroll；规格只写了“NestedScrollView → Scroll + Column”，没写哪些区域固定；之后的视觉轮只改顶部偏移，直到用户两次反馈顶部栏太靠下才改层级。另一应用首页的横幅是 NestedScrollView 的兄弟、滚动区 layout_below 横幅，生成者读到该层级后仍用 Blank(200) 与横幅一起放进 Scroll，横幅随内容滚动，直到用户要求“火车订票是固定的”才移出。

## 做法

1. 转换前按源布局确认滚动容器开、闭标签之间包含哪些子节点；在它之前的兄弟（RelativeLayout 中被 layout_below 锚定的视图）放在 Scroll 外，Scroll 用 layoutWeight(1) 或定位占剩余区域，只包裹原滚动区内容；不用 Blank 占位把固定区一起塞进 Scroll。
2. 规格写滚动容器的转换决策时写明滚动范围：哪些区域固定、距顶多少，哪些随滚动；不只写组件映射。
3. 视觉校验发现顶部区块位置偏差时，先查它是否处在滚动容器内（内容不足一屏时最明显），层级错误就改层级，不用 padding 偏移补偿。

## 来源（按需复核）

- [case-25f05bb6ccf6238a63a1](../../../../store/cases/case-25f05bb6ccf6238a63a1/12bb60e9468ba072bb8a9a389a250d67fa65854706daf99099d3acfbbc56dc5e.json) · 结论：diagnosis, recommendation:2
  卡片版本：`12bb60e9468ba072bb8a9a389a250d67fa65854706daf99099d3acfbbc56dc5e`
- [case-6147579e732da7b69f07](../../../../store/cases/case-6147579e732da7b69f07/35b7fe405516348d9c763959bc9434b39a5f44e926fbe53619360bc9dee509a1.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`35b7fe405516348d9c763959bc9434b39a5f44e926fbe53619360bc9dee509a1`
