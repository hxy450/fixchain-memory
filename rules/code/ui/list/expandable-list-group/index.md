# ExpandableListView 的分组头

agent 会看到什么：读到 ExpandableListView（expandGroup、groupIndicator、indicatorLeft）和 BaseExpandableListAdapter.getGroupView；产物里 List / ListItemGroup 写的组头、展开状态和箭头

## 规矩

- rule-132590764af9｜ExpandableListView 未设组点击监听时，组头仍要 onClick 切换展开，箭头随状态变｜读到：ExpandableListView 只调 expandGroup(n)，全文没有 setOnGroupClickListener（或 OnGroupClickListener.onGroupClick 返回 false）；写错：组头没有 .onClick、没有展开状态，注释写「源码未设组点击监听，组头不可点，保真」，只渲染固定那一组的子项
- rule-c1e7f08b4770｜ExpandableListView 用默认 groupIndicator 时，组头左侧画平台 expander 图形｜读到：ExpandableListView 没自定义 android:groupIndicator，只写 android:indicatorLeft="?android:attr/expandableListPreferredItemIndicatorLeft"；适配器 getGroupView 不画箭头；写错：组头 Row 右端放了 SymbolGlyph（chevron_right / chevron_down）或其他系统符号，颜色写成黑色
