# 左点右滚的联动要迁移程序滚动保护，动画期间忽略 onScrollIndex 的中间索引

审的是：代码
触发（任一种）：
- 读到：源端用一个布尔标志位在左侧点击触发的 animateScrollToItem 期间屏蔽可见项回写（注释如「避免循环联动」）；写错的样子：目标 .onScrollIndex((start) => { 选中索引 = start }) 无条件写回，左侧点击 scrollToIndex(index, true) 的动画期间中间索引覆盖点击选中态
适用范围：左侧点击触发右侧动画滚动、右侧滚动又回写左侧选中态的双向联动
做法：
- 点击时记下目标索引并上锁；onScrollIndex 在上锁期间忽略不等于目标的索引，命中目标后解锁
- 加超时释放（防止停不到目标时一直锁住），连续点击时以最新目标覆盖旧目标
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 记待滚目标索引，程序滚动期间忽略非目标回调、命中目标后解锁，再补超时释放与快速连点覆盖：返修后的写法（出处：卡里修好并验证过）
- onScrollIndex(event: (start: number, end: number, center: number) => void): ListAttribute：动画滚动经过的每个分组都会触发它（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.onScrollIndex）
未核实：超时时长卡里取的是应用自己的值，未给通用数值
来源：1 张卡，1 个应用
- case-455133ba2c8a862f7ce2（青商城）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 1 ← 诊断
