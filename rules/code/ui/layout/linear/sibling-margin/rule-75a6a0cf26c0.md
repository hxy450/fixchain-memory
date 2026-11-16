# 源只在一侧设外边距时按原样翻译，用 Row 的 space 或单侧 margin，不拆成两侧对称

审的是：代码
触发（任一种）：
- 读到：顶栏里第一个图标只写 android:layout_marginRight（如 10dp），第二个图标贴父容器的 paddingHorizontal；写错的样子：目标给每个图标都写 .margin({ left: 5, right: 5 }) 这类两侧对称外边距，最右侧外距被放大
适用范围：源端相邻控件之间只有一侧外边距、末尾控件贴父容器内边距时
做法：
- 写成 Row({ space: 源 margin 数值 })，或只给第一个控件写 .margin({ right: 源数值 })；末尾控件不加外边距，靠父容器 padding 对齐
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- RowOptions.space?: string | number：Row 子项之间的间距（出处：鸿蒙 SDK 的 ets/component/row.d.ts，RowOptions.space）
来源：1 张卡，1 个应用
- case-639b36918b1cd5c1bbe8（android-train-ticket-vest7）：做法第 1 步 ← 建议 4、诊断
