# 源布局容器（NestedScrollView、LinearLayout）的滚动范围和默认对齐

agent 会看到什么：读到源布局里顶部栏在 NestedScrollView 之前、滚动容器只包下方内容，或纵向 LinearLayout 没写 android:gravity、子项默认贴起始边；规格只写「NestedScrollView → Scroll + Column」「左上角」「左对齐」，没写哪些栏固定、Column 的 alignItems / alignSelf

## 规矩

- rule-4df816f61991｜规格的转换决策写明滚动范围：哪些栏固定、NestedScrollView 只包哪些内容｜读到：源布局里顶部用户栏或工具栏在 NestedScrollView 之前、带固定 marginTop，滚动容器只包下方内容；写错：规格只写「NestedScrollView → Scroll + Column」的组件映射和「顶部 N vp 起始」，没写哪些栏固定不随滚动、Scroll 包含哪些子节点
- rule-bf3d3d0e5579｜规格写「左上角」「左对齐」这类位置时，同时写成 alignItems 或 alignSelf 要求｜读到：源布局是没写 android:gravity 的纵向 LinearLayout，子项默认贴起始边；写错：规格只写「返回按钮（左上角）」「左对齐」这类描述，没写目标 Column 要 alignItems(HorizontalAlign.Start) 或子项要 alignSelf；LinearLayout→Column 的映射条目没写两端默认交叉轴对齐不同
