# 随状态或容器变化的颜色

agent 会看到什么：源端 Compose 颜色不是资源原色、而是随容器或状态算出来的写法（Surface(elevation > 0) 的叠白、color.copy(alpha = if (!enabled) 0.38f else 1f)），对应目标的 backgroundColor、fontColor 和按状态的 opacity

## 规矩

- rule-4ba4e90a3f99｜Text 写了显式 color 和禁用 alpha 时，目标写 fontColor 加按状态的 opacity｜读到：Text(color = <颜色>.copy(alpha = if (!enabled) 0.38f else 1f)) 这类写法；写错：目标 fontColor 用了按钮的品牌色，只靠 .enabled() 表示禁用，没有按状态设 opacity
- rule-21d4850a141b｜源组件套在 elevation > 0 的 Surface 里时，每种状态色都按源叠加公式算底色｜读到：Compose 源组件外面是 Surface(elevation = 2.dp) 这类 elevation > 0 的 Surface，Surface 的实现按 elevation 给底色叠白；写错：目标 .backgroundColor 直接用选中、未选中的资源原色，只核对了白底一种状态（白上叠白不变）就简化成原色
