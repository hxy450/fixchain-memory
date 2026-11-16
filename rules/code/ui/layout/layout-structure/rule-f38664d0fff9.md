# 按 spec 重写页面时先读 spec 的页面结构或源布局 XML，不保留安卓没有的自创头部

审的是：代码
触发（任一种）：
- 读到：spec 的页面结构 / Android 可观察事实段或源布局 XML（根 android:background、标题和内容区的 layout_marginTop）写明了顶部结构；写错的样子：重写后保留了基线页面里安卓没有的自创头部（渐变头卡、大号白字加简介），根 .backgroundColor、标题区和内容起点与 spec 不符，报告仍称已对齐源页面
适用范围：按 spec 重写已有基线页面的界面实现任务
做法：
- 改动前先读 spec 的页面结构 / Android 可观察事实段或源布局 XML，再决定保留还是替换现有结构；基线里有相似元素不是保留的理由，安卓中不存在的头部去掉
- 按源复刻根背景色、标题行（位置、高度、字号字重、对齐）和内容区起点与底色
针对本应用要查的：
- 页面顶部结构：spec 的页面结构段，或源工程该页面的布局 XML；读根 android:background、标题的 layout_marginTop / 高度 / textSize / textStyle / gravity、内容区的起点和背景
来源：1 张卡，1 个应用
- case-6597b7f7858db941262c（android-train-ticket-vest7）：做法第 1 步 ← 建议 5；做法第 2 步 ← 诊断、建议 5
