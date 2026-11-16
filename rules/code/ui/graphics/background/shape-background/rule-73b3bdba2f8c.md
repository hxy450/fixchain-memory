# 参考兄弟页的卡片 Builder 时只借结构，圆角、描边、底色回本页源码核对

审的是：代码
触发（任一种）：
- 读到：兄弟页 .ets 里已有卡片 @Builder（白底、.border(...)、.borderRadius(...)）；写错的样子：本页卡片的圆角、描边、底色数值照搬兄弟页 Builder，没回本页安卓源码核对
适用范围：以兄弟页已有实现为模板写本页卡片样式时
做法：
- 只借用兄弟 Builder 的结构；圆角、描边宽度和颜色、底色逐项回到本页源布局（item 布局、holder 动态视图的布局、drawable）取值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 照搬兄弟页 Builder 的圆角后和本页源端 CardView 圆角不一致；改用本页源端的值后正确：兄弟实现不是真值（出处：卡里修好并验证过）
针对本应用要查的：
- 本页卡片的圆角、描边、底色：源工程里本页的 item 布局 XML、holder 动态加入视图的布局、android:background 指向的 drawable XML（<shape> 的 <corners>、<stroke>、<solid>）；逐项读出 radius、stroke width / color、solid color，解析 @dimen / @color 到具体值后写进目标端
来源：1 张卡，1 个应用
- case-5b1b0e2ce03be0dc6d37（组件岛Widget Island）：做法第 1 步 ← 建议 3；取值 1 ← 诊断
