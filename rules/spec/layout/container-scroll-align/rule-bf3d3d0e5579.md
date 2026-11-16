# 规格写「左上角」「左对齐」这类位置时，同时写成 alignItems 或 alignSelf 要求

审的是：规格
触发（任一种）：
- 读到：源布局是没写 android:gravity 的纵向 LinearLayout，子项默认贴起始边；写错的样子：规格只写「返回按钮（左上角）」「左对齐」这类描述，没写目标 Column 要 alignItems(HorizontalAlign.Start) 或子项要 alignSelf；LinearLayout→Column 的映射条目没写两端默认交叉轴对齐不同
适用范围：规格里写纵向 LinearLayout 迁成 Column 后子项水平位置的那一处，含 LinearLayout→Column 的映射条目
做法：
- 每个位置描述都落成目标属性：「左上角」「左对齐」写明对应 Column 用 .alignItems(HorizontalAlign.Start)，或该子项用 .alignSelf(ItemAlign.Start)
- LinearLayout→Column 的条目写明：安卓纵向 LinearLayout 默认交叉轴是 start，ArkUI Column 的 alignItems 默认 HorizontalAlign.Center，源端没写 gravity 时目标要显式写 Start
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- LinearLayout 的 mGravity 默认是 Gravity.START | Gravity.TOP：源端默认贴起始边（出处：android.widget.LinearLayout#mGravity）
- Column.alignItems 默认值 HorizontalAlign.Center：目标默认居中，和源端默认不同（出处：ts-container-column.md，alignItems）
- alignSelf(value: ItemAlign): T：子项自己的交叉轴对齐，所有组件共有（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.alignSelf）
来源：1 张卡，1 个应用
- case-440adef4b89e0a02222a（免费来电多多）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3
