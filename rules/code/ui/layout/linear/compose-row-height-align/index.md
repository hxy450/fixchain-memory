# Compose 行容器的高度和垂直对齐

agent 会看到什么：读到 Compose Row（没写 verticalAlignment，或 Modifier.height(IntrinsicSize.Min)）和按内容定高的横向滚动行（ScrollableTabRow、horizontalScroll）；产物里 Row / Scroll 的 alignItems 和 height

## 规矩

- rule-99e2a12d0aa5｜Compose Row 没写对齐时，目标 Row 显式写 alignItems(VerticalAlign.Top)｜读到：Compose `Row(...)` 的构造参数里没有 `verticalAlignment`；写错：对应的 ArkUI `Row()` 上没有 `.alignItems(...)`，沿用默认 VerticalAlign.Center，子组件被垂直居中
- rule-5467d24896c1｜Row 用 IntrinsicSize.Min 定高时，算出固有高度写显式 height，子项保留 top 偏移｜读到：Compose Row(Modifier.height(IntrinsicSize.Min)) 内子项 Modifier.fillMaxHeight().padding(top = …)；写错：目标 Row 没有显式 height，子项改成垂直居中并删掉源码的 top 偏移（以 P-20 百分比撑满为由）
- rule-ee127edc9333｜Compose 横向滚动行译成 Scroll(Horizontal) 时，交叉轴写显式高度，不用 'auto' 也不留空｜读到：Compose 里 PrimaryScrollableTabRow、ScrollableTabRow 或 Modifier.horizontalScroll 这类按内容定高的横向滚动行；写错：目标 Scroll 配 .scrollable(ScrollDirection.Horizontal) 却没写 .height(...)，或写成 .height('auto')
