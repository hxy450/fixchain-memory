# 换外层容器后留下的布局修饰

agent 会看到什么：读到原先在 Column 里靠 .layoutWeight(1)、.justifyContent(...)、.alignItems(...) 撑满和居中的节点；产物里换成 Scroll 或移进 Refresh 后，这些修饰原样留在新容器或根节点上

## 规矩

- rule-05f637585267｜Column 换成 Scroll 时，尾部的 justifyContent/alignItems 移进内部 Column｜读到：原容器 `Column() {…}` 尾部挂着 `.layoutWeight(1).justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)` 一类的修饰链；写错：换成 `Scroll() { Column() {…} }` 时只替换了容器头和子项，`.justifyContent(...)`、`.alignItems(...)` 落到了 Scroll 上，编译报 Property 'justifyContent' does not exist on type 'ScrollAttribute'
- rule-cfd49bd6d88c｜靠 layoutWeight 填满居中的根节点移进 Refresh 后，改成 height('100%')｜读到：空态或引导 builder 的根 Column 用 .layoutWeight(1) + .justifyContent(FlexAlign.Center) 在 Column 父级里填满剩余空间并居中，现在要放进 Refresh 的内容；写错：移进 Refresh { ... } 后根 Column 仍是 .layoutWeight(1)，没有 .height('100%') 之类的显式高度
