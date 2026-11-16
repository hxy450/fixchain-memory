# 宿主容器和共享组件根都写了同一来源的 padding 时，删掉宿主一侧

审的是：代码
触发（任一种）：
- 读到：安卓宿主布局（承载 fragment 的 ViewPager）没有 padding，padding 写在 fragment 根 LinearLayout 上；写错的样子：宿主的 TabContent 或容器 .padding(...) 和共享组件根 .padding(...) 取的是同一个边距资源，四边内边距叠成两份
适用范围：接线时把共享组件放进宿主页容器，两边都写了 padding 时
做法：
- 对照宿主容器和组件根的 padding（按同一个边距资源名搜，例如模板常见的 activity_horizontal_margin），同一来源的边距只留在组件根上，删掉宿主一侧；宿主只保留它自己的（如底部避让）
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 宿主容器只保留底部避让，根 padding 由共享组件承担后，边距与安卓一致：修好后的写法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-4e7e0e12d7b6b08c08b0（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、诊断；取值 1 ← 诊断
