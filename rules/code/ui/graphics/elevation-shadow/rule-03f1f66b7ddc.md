# 各处 elevation 阴影集中到一个按 elevation 换算的共享函数，不在页面另写近似常量

审的是：代码
触发（任一种）：
- 读到：源端几处元素各自带不同的 elevation（如 elevation = 1.dp、2.dp、3.dp）；写错的样子：页面里另写与 elevation 无关的阴影常量，`.shadow({ radius: 常量, offsetY: 1 })`，注释写「视觉近似」，不同 elevation 的元素共用同一组数值
适用范围：目标工程里多个页面、组件都要把 Compose elevation 迁成 .shadow 时
做法：
- 建一个共享换算函数，参数是 UIContext 和 elevation 值 e，返回 { radius: ctx.vp2px(e), offsetY: ctx.vp2px(e / 2), color: '#40000000' }，每处按源端自己的 elevation 值调用
- 自查：搜 `.shadow({`，每个数值字段都要经过 vp2px 或这个共享函数
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 用按 elevation 换算的共享函数替换各处 px 直写后，几处投影强度恢复：卡里的修法（出处：卡里修好并验证过）
针对本应用要查的：
- 每处元素的源端 elevation：源工程 Compose 代码里该元素的 Modifier.shadow(elevation = …) 或 Surface 类容器的 elevation 实参，以及页面规格里写的 elevation；逐处读出 dp 值，作为共享函数的参数
来源：1 张卡，1 个应用
- case-6aedeaac4c252c3c5626（Jetsnack）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 1 ← 诊断
