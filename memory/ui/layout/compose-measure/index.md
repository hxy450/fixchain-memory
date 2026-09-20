# ui/layout/compose-measure

从 Compose 源码推演实际渲染（度量副作用）

[上一级](../index.md)

## 本级经验

- [从 Compose 源码合成结构时先做 Row/Column 度量推演：fillMaxWidth 无 weight 子项之后的兄弟不会被绘制](lesson-017824fda8e1befa8477.lesson.md)
  - 时机：规格提取阶段，在没有真机 dump、只能从纯 Compose 源码合成页面结构与分页 spec 时，判定某个声明的子组件是否真的会被绘制
  - 情境：某个 Row/Column 里有一个不带 weight 的 fillMaxWidth()/fillMaxHeight() 子项，其后还跟着兄弟组件（IconButton/Text 等）；spec 或派工准备用「近乎不可见、parity 保留」描述该兄弟。
  - 例外：兄弟组件带 weight 或 Row 用了 IntrinsicSize/自定义度量使其仍分到宽度
