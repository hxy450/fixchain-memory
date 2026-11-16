# 列表

源端列表 Adapter 有多个 viewType、在 onBindViewHolder 里改写行视图，或者计划、派工里有 LazyForEach 换 Repeat、virtualScroll、列表键契约时

## 触发族

- [列表批量改写和键契约的计划与验收](list-refactor/index.md)（3 条）：计划、派工或验收涉及列表的批量改写（LazyForEach 换 Repeat、virtualScroll、短列表豁免）或列表键契约（P-05 键复用陷阱、@Trace 更新方式）
- [列表 Adapter 的 item 布局和绑定时的改写](adapter-bind-variants/index.md)（3 条）：源端列表 Adapter 有多个 viewType、在 onBindViewHolder / afterBindViewHolder 里改写行视图（setVisibility、改配按钮外观）或运行时 inflate 别的布局，页面清单、转换报告或占位登记只顾到了共享行组件的默认样子
