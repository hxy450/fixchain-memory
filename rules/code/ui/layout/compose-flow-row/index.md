# Compose FlowRow 的换行排列

agent 会看到什么：读到 Compose 的 FlowRow（Arrangement.SpaceBetween、spacedBy），尤其 FlowRow 里再套 FlowRow 加尾随元素；产物里外层和内层都是 Flex({ wrap: FlexWrap.Wrap }) 加 .flexGrow(1)，或 onMeasureSize / onPlaceChildren 写的自定义布局

## 规矩

- rule-fc7bde37e194｜FlowRow 套 FlowRow 再跟尾随元素时，不用嵌套 wrap Flex，改用贪心换行自定义布局｜读到：Compose 的 FlowRow(SpaceBetween) { FlowRow(spacedBy 间距){ 左组 } ; 尾随元素 }，放得下时左组和尾随元素同一行两端对齐；写错：写成外层 Flex({ wrap: FlexWrap.Wrap, justifyContent: FlexAlign.SpaceBetween }) 套内层 wrap Flex，内层再加 .flexGrow(1)；尾随元素总是独占一行
