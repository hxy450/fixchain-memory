# Compose 的 clickable / toggleable 点击修饰

agent 会看到什么：读到 Compose 的 Modifier.clickable / combinedClickable / toggleable 或 Card(onClick) 及其 role、enabled、indication 参数；产物里组件只挂了 .onClick(...)，缺按压态、.enabled(...)、accessibilityRole 或合并朗读

## 通用查法

### 源端 clickable 类修饰符逐个参数对应：按压态、enabled、角色和合并朗读都要写

审的是：代码
触发（任一种）：
- 读到：Compose 源码 Modifier.clickable / combinedClickable / toggleable(onClick, enabled = …, role = Role.…) 或 Card(onClick = …)，没有关掉默认 indication；写错的样子：目标组件只挂了 .onClick(...)，没有 .stateStyles({ pressed: … })、.enabled(...)、.accessibilityRole(...) 或合并朗读
适用范围：Compose 可点击、可切换的组件迁成 ArkUI 组件的点击反馈和语义时
做法：
- 逐个读出源端调用的参数：enabled 的条件、role、有没有关掉默认 indication（没关就是默认涟漪），以及标题、正文是否在同一个可点击容器里
- 每项写成显式写法：默认涟漪写 .stateStyles({ pressed: … })；enabled 写 .enabled(条件)；Role.Button 写 .accessibilityRole(AccessibilityRoleType.BUTTON)；整卡可点的容器写 .accessibilityGroup(true)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- stateStyles(value: StateStyles): T：按组件状态切换样式，StateStyles 里有 normal、pressed、disabled 等（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.stateStyles）
- enabled(value: boolean): T；false 时不响应点击：对应源端 clickable 的 enabled（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.enabled）
- accessibilityRole(role: AccessibilityRoleType): T（@since 18）：设置组件的无障碍角色，对应源端 role（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityRole）
- accessibilityGroup(value: boolean): T，默认 false：开启后组件和子组件被当成一个可选单元，读屏不再聚焦单个子组件（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.accessibilityGroup）
针对本应用要查的：
- 按压状态层的颜色和不透明度：源工程 Compose 主题里这个组件的内容色（MaterialTheme.colorScheme 的对应角色），以及应用依赖的 androidx.compose.material3 版本里的按压状态层定义；取内容色叠加按压层的不透明度，写进 pressed 里的 backgroundColor；例：卡里在可切换状态下加 10% 按压叠层后复审通过
未核实：Material 3 默认按压层不透明度是 10%，本机没有 Compose 源码可核
来源：2 张卡，1 个应用
- case-5a84af0e2f5c593b9f0c（Cofi）：做法第 2 步 ← 建议 4
- case-8dd5c1f1f269d142cc22（Cofi）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断

## 规矩

- rule-a1f68abe0f1f｜源用 clickable 或 Card onClick 时，目标用 stateStyles 补按压态｜读到：Compose 外层 `Modifier.toggleable(enabled = …, role = Role.Switch)` 或 `Modifier.clickable` 用默认涟漪；写错：目标只有 `.onClick(...)`，没有 `stateStyles` 的 pressed 态，按下没有反馈
- rule-de87c1652c15｜源 clickable 带 Role.Button 和 enabled 时，目标写按钮角色和 .enabled｜读到：源端可点击行 Modifier.clickable / combinedClickable(onClick, onLongClick, enabled = …, role = Role.Button)；写错：目标只写 .onClick(...) 加 LongPressGesture，没有 .accessibilityRole(AccessibilityRoleType.BUTTON)，也没有 .enabled(...)
- rule-d8d2de6cced7｜源端整卡 clickable(role = Button) 合并子文本时，目标容器合并朗读，独立关闭键单给 BUTTON｜读到：源端标题和正文放在同一个 Column.clickable(onClick, role = Role.Button) 里，关闭键是独立的 IconButton(onClick = …)；写错：目标只给外层容器挂 .onClick(...)，标题、正文各自被单独朗读，关闭键没有 accessibilityRole
- rule-95b6130d703c｜带 Modifier.clickable 的 Card，卡片级 onClick 放根容器，和内部关闭按钮分开｜读到：Compose 的 Card 带 Modifier.clickable(onClick = onClick)（合成的 view.xml 里该节点 clickable="true"），卡片内另有关闭/忽略按钮；写错：ArkUI 卡片根 Row/Column 上没有 .onClick，只有内部关闭图标写了 onClick
- rule-2df80ec3500f｜新建页内对话框的可见性状态时，每个状态都要有置 true 的触发点或登记 FWD-REF｜读到：规格导航关系表里有「卡片 → 对话框」这类触发行；源端 Compose 在状态为真时渲染对话框，触发组件带 Modifier.clickable(onClick = onClick)；写错：页面声明了 @Local 可见性状态和 @Builder overlay，全文件只在关闭时置 false，没有任何 = true 赋值，触发点也没登记 FWD-REF
