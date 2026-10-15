# 转换 ScrollView/NestedScrollView 时只把源滚动容器内的子节点放进 Scroll，固定区留在外面；内容不满一屏时显式贴顶

ID：`lesson-46a0d7f239efac925d33` · 版本：6

[本主题](index.md)

## 何时使用

界面实现阶段，把 ScrollView/NestedScrollView 或纵向 Lazy 列表转成 ArkUI Scroll/List、确定固定区与滚动区边界和短内容位置时；借用相邻页面的页面骨架时；规格提取阶段书写滚动容器的转换决策时

## 适用情境

源布局根为纵向 LinearLayout 或 RelativeLayout，用户栏、工具栏、横幅或固定高度标题栏位于滚动容器之前（RelativeLayout 中滚动容器以 layout_below 排在其下，或与 layout_weight=1 的列表区同级）；目标用 Scroll 包 Column 承载内容，条目数可变、可能不足一屏。同工程相邻页面可能按其自身源码采用整页单一 Scroll。

## 例外与边界

- 源端固定区本就写在 ScrollView 内、随内容滚动时，按源结构放进 Scroll
- 空态在剩余区域中的纵向位置按空态定位的规则处理

## 原因

固定头部进了 Scroll 就随内容滚动；ArkUI Scroll 对矮于视口的子组件默认居中（设备实测，scroll.d.ts 未注明），而 NestedScrollView、LazyColumn 从顶部排列，内容不足一屏时整组被纵向下推，头部也跟着下移。给未定高的 Column 写 justifyContent 不改变它在 Scroll 中的位置；视觉修复若只调 padding 偏移，会掩盖层级错误。

## 做法

1. 转换前按源布局确认滚动容器开、闭标签之间包含哪些子节点；在它之前的兄弟（被 layout_below 锚定的视图、与 weight 列表区同级的固定标题栏）放在 Scroll/List 外，滚动区用 layoutWeight(1) 或定位占剩余区域，只包裹原滚动区内容；不用 Blank 占位把固定区一起塞进 Scroll。
2. 源内容从顶部排列时，给 Scroll 写 .align(Alignment.Top)（或 TopStart），或给 Scroll 的子容器加 constraintSize({ minHeight: '100%' })（Scroll 内的 '100%' 按视口高解析，设备实测、scroll.d.ts 未定义）并保持 justifyContent(FlexAlign.Start)；确认超出一屏后仍能滚动。可变长度条目列表优先映射为 List，条目默认从顶部排列。
3. 借用相邻页面骨架（如整页单一 Scroll）前，核对本页规格的结构描述、属性表与源 XML 中滚动容器的实际子树是否也是整页滚动。
4. 规格写滚动容器的转换决策时写明滚动范围：哪些区域固定、距顶多少，哪些随滚动；不只写组件映射。
5. 视觉校验发现顶部区块位置偏差时，先查它是否在滚动容器内、内容是否不满一屏；按源端重排卡片或缩短头部后，一并复查外层 Scroll 的对齐；层级错误就改层级，不用 padding 偏移补偿。

## 可选检查

- 需要确认时，用只有一条和不足一屏两种数据看首屏，首块应紧贴上方固定区。

来源支持：6 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-1afb71d7d28eee931ed4](../../../../store/cases/case-1afb71d7d28eee931ed4/86a7345cc3d51b39581ae0f7a50214171c7dbd6f62c5a642d0fb20b4e96cae77.json) · 结论：diagnosis, recommendation:1, recommendation:3
  卡片版本：`86a7345cc3d51b39581ae0f7a50214171c7dbd6f62c5a642d0fb20b4e96cae77`
- [case-25f05bb6ccf6238a63a1](../../../../store/cases/case-25f05bb6ccf6238a63a1/12bb60e9468ba072bb8a9a389a250d67fa65854706daf99099d3acfbbc56dc5e.json) · 结论：diagnosis, recommendation:2
  卡片版本：`12bb60e9468ba072bb8a9a389a250d67fa65854706daf99099d3acfbbc56dc5e`
- [case-6147579e732da7b69f07](../../../../store/cases/case-6147579e732da7b69f07/35b7fe405516348d9c763959bc9434b39a5f44e926fbe53619360bc9dee509a1.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`35b7fe405516348d9c763959bc9434b39a5f44e926fbe53619360bc9dee509a1`
- [case-6405389151d06d90f7cc](../../../../store/cases/case-6405389151d06d90f7cc/dda7c3254bb172c40bdb5c14da83b24e0a3b970fbf121e1be1fa054f0ee1e12e.json) · 结论：diagnosis, recommendation:2
  卡片版本：`dda7c3254bb172c40bdb5c14da83b24e0a3b970fbf121e1be1fa054f0ee1e12e`
- [case-9058ac868b6feb3a04e0](../../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:5
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
- [case-918a52ecd2f381adbd7d](../../../../store/cases/case-918a52ecd2f381adbd7d/ba381e72c0bd7272a86deaf354bbf13c8639022176d2c3526b2dabc79c0594b0.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4, recommendation:3
  卡片版本：`ba381e72c0bd7272a86deaf354bbf13c8639022176d2c3526b2dabc79c0594b0`
